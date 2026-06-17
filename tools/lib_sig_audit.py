#!/usr/bin/env python3
"""lib_sig_audit.py -- compare libfns.h (...) doc-arities against the REAL signatures
in the reconstructed EA-lib sources (eaclib/**/*.cpp), and flag call sites that drop
args vs the REAL arity.

This catches the bug class NEITHER runtime scanner can: a (...) fn whose doc UNDER-counts
AND every call site consistently passes the wrong (low) count -> consistency scanner sees
agreement, arity_audit sees got==doc, but the REAL signature (from the lib source that
DEFINES the fn) proves args are dropped. This is how the intsincos / FILE_readsync class
is found at the root.

Run:  python tools/lib_sig_audit.py
"""
import re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# exclude genuinely-variadic format fns (covered by sprintf_audit*) and libgcc/soft-float
# intrinsics (__adddf3 etc.) whose source takes a `double` as 2 split int-halves -- an ABI
# artifact, not a real arg count, so source-vs-call comparison is meaningless for them.
FMT = {'sprintf', 'printf', 'fprintf', 'sscanf', 'scanf', 'fscanf', 'snprintf',
       'vsprintf', 'vprintf'}
def skip_fn(fn):
    return fn in FMT or fn.startswith('__')

def arity_of(params):
    params = params.strip()
    if params in ('', 'void'):
        return 0
    d = 0; n = 1
    for ch in params:
        if ch in '([{': d += 1
        elif ch in ')]}': d -= 1
        elif ch == ',' and d == 0: n += 1
    return n

def balanced_doc_arity(line, openparen_idx):
    i = openparen_idx; d = 0; j = i
    while j < len(line):
        if line[j] == '(': d += 1
        elif line[j] == ')':
            d -= 1
            if d == 0: break
        j += 1
    return arity_of(line[i + 1:j])

# 1) (...) fns + documented arity from the headers
doc_arity = {}
variadic = set()
for hdr in ['lib/libfns.h', 'lib/eaclib.h']:
    if not os.path.exists(hdr):
        continue
    for line in open(hdr, encoding='utf-8', errors='ignore'):
        mf = re.search(r'\b([A-Za-z_]\w*)\s*\(\s*\.\.\.\s*\)\s*;', line)
        if not mf:
            continue
        fn = mf.group(1); variadic.add(fn)
        cm = re.search(r'/\*\s*\(', line)
        if cm:
            doc_arity[fn] = balanced_doc_arity(line, cm.end() - 1)

# 2) REAL signatures from EA-lib source DEFINITIONS (extern "C" type name(params) { )
# strip block comments first (defs are not in comments)
def strip_block(t):
    return re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), t, flags=re.S)

DEF = re.compile(
    r'(?:extern\s*"C"\s*)?'           # optional linkage
    r'(?:[A-Za-z_][\w\s\*]*?\s|\*\s*)' # return type (>=1 token, may end in *)
    r'\b([A-Za-z_]\w*)\s*'            # fn name
    r'\(([^;{}]*)\)\s*'              # (params) -- no ; { } inside
    r'\{',                            # body opener
    re.S)

real_arity = {}
real_src = {}
SRC_GLOBS = ['eaclib/**/*.cpp', 'syslib/**/*.cpp', 'syslib/**/*.c']
src_files = []
for g in SRC_GLOBS:
    src_files += glob.glob(g, recursive=True)
for f in src_files:
    txt = strip_block(open(f, encoding='utf-8', errors='ignore').read())
    for m in DEF.finditer(txt):
        fn, params = m.group(1), m.group(2)
        if fn in variadic:
            real_arity[fn] = arity_of(params)
            real_src[fn] = (f.replace('\\', '/'), params.strip())

# 3) compare doc vs real; report mismatches
print("=== libfns.h (...) DOC-ARITY vs EA-lib SOURCE real-arity ===")
have_real = sorted(fn for fn in (set(doc_arity) & set(real_arity)) if not skip_fn(fn))
mismatches = [fn for fn in have_real if doc_arity[fn] != real_arity[fn]]
print("%d (...) fns have a reconstructed lib source; %d arity mismatches:"
      % (len(have_real), len(mismatches)))
for fn in mismatches:
    src, params = real_src[fn]
    print("  %-20s doc=%d real=%d   %s  [%s]"
          % (fn, doc_arity[fn], real_arity[fn], '(' + params + ')', src))

# 4) for under-counted docs, check call sites vs REAL arity (hidden dropped-arg bugs)
def strip_noncode(t):
    t = strip_block(t)
    t = re.sub(r'//[^\n]*', ' ', t)
    t = re.sub(r'"(?:[^"\\]|\\.)*"', '""', t)
    return t

def splitargs(s):
    out = []; d = 0; cur = ''
    for ch in s:
        if ch in '([{': d += 1
        elif ch in ')]}': d -= 1
        if ch == ',' and d == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return out

# check ALL fns with a reconstructed source (>=2 real args) -- a drop vs REAL arity is
# a bug regardless of whether the doc over- or under-counts.
check = {fn for fn in real_arity if real_arity[fn] >= 2 and not skip_fn(fn)}
print("\n=== call sites passing FEWER than REAL (lib-source) arity (dropped-arg) ===")
hits = []
for f in glob.glob('game/**/*.cpp', recursive=True) + glob.glob('*.cpp'):
    if 'backup' in f.replace('\\', '/').split('/'):
        continue
    txt = strip_noncode(open(f, encoding='utf-8', errors='ignore').read())
    for m in re.finditer(r'\b([A-Za-z_]\w*)\s*\(', txt):
        fn = m.group(1)
        if fn not in check:
            continue
        i = m.end() - 1; d = 0; j = i
        while j < len(txt):
            if txt[j] == '(': d += 1
            elif txt[j] == ')':
                d -= 1
                if d == 0: break
            j += 1
        got = 0 if txt[i + 1:j].strip() == '' else len(splitargs(txt[i + 1:j]))
        if got < real_arity[fn]:
            ln = txt[:i].count('\n') + 1
            hits.append((f.replace('\\', '/'), ln, fn, real_arity[fn], got))
print("%d hidden dropped-arg call sites:" % len(hits))
for f, ln, fn, real, got in hits:
    print("  %s:%d  %s  real=%d got=%d" % (f, ln, fn, real, got))
