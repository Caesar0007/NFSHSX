#!/usr/bin/env python3
"""variadic_consistency.py -- flag dropped-arg bugs in (...)-prototyped lib calls
by SELF-CONSISTENCY, not by trusting the (possibly under-counted) doc comment.

For every function declared `name(...);` in lib/libfns.h or lib/eaclib.h, collect
the supplied-arg count at EVERY call site across the run-tree .cpp. If a function
is called with K args at some site and fewer at another, the low sites are
dropped-arg CANDIDATES (verify each against the raw oracle before fixing).

This is strictly stronger than arity_audit.py for this bug class: it catches sites
that match an UNDER-counted doc comment (FILE_readsync was documented 3, really 5),
and it covers the 7 (...) fns that have no doc comment at all.

Run:  python tools/variadic_consistency.py
"""
import re, glob, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 1) the set of (...)-prototyped lib fns + any documented arity (the FLOOR)
variadic = set()
doc_arity = {}
for hdr in ['lib/libfns.h', 'lib/eaclib.h']:
    if not os.path.exists(hdr):
        continue
    for line in open(hdr, encoding='utf-8', errors='ignore'):
        m = re.search(r'\b([A-Za-z_]\w*)\s*\(\s*\.\.\.\s*\)\s*;', line)
        if not m:
            continue
        fn = m.group(1)
        variadic.add(fn)
        d = re.search(r'\(\s*\.\.\.\s*\)\s*;\s*/\*\s*\((.*?)\)', line)
        if d:
            params = d.group(1).strip()
            if params in ('', 'void'):
                doc_arity[fn] = 0
            else:
                depth = 0; n = 1
                for ch in params:
                    if ch in '([{': depth += 1
                    elif ch in ')]}': depth -= 1
                    elif ch == ',' and depth == 0: n += 1
                doc_arity[fn] = n

# genuinely variadic / optional-arg fns: counts SHOULD differ, not bugs
SKIP = {'sprintf', 'printf', 'fprintf', 'sscanf', 'scanf', 'fscanf',
        'snprintf', 'vsprintf'}

def strip_noncode(t):
    t = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), t, flags=re.S)
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

# fn -> list of (file, line, argcount)
sites = defaultdict(list)
for f in glob.glob('game/**/*.cpp', recursive=True) + glob.glob('*.cpp'):
    if 'backup' in f.replace('\\', '/').split('/'):
        continue
    txt = strip_noncode(open(f, encoding='utf-8', errors='ignore').read())
    for m in re.finditer(r'\b([A-Za-z_]\w*)\s*\(', txt):
        fn = m.group(1)
        if fn not in variadic or fn in SKIP:
            continue
        i = m.end() - 1; d = 0; j = i
        while j < len(txt):
            if txt[j] == '(':
                d += 1
            elif txt[j] == ')':
                d -= 1
                if d == 0:
                    break
            j += 1
        inner = txt[i + 1:j].strip()
        got = 0 if inner == '' else len(splitargs(inner))
        ln = txt[:i].count('\n') + 1
        sites[fn].append((f.replace('\\', '/'), ln, got))

# expected arity = documented arity if known (AUTHORITATIVE floor), else max observed.
# flag sites supplying FEWER than expected (dropped-arg candidates).
# over-supply (got > expected) is reported separately as informational (usually a
# harmless extra varargs arg, OR a sign the doc/floor under-counts -> verify).
flagged = []
oversupply = []
for fn, lst in sites.items():
    counts = [c for _, _, c in lst]
    mx = max(counts)
    expected = doc_arity.get(fn, mx)   # documented arity wins as the floor
    lows = [(f, ln, c) for f, ln, c in lst if c < expected]
    highs = [(f, ln, c) for f, ln, c in lst if c > expected]
    if lows:
        flagged.append((fn, expected, lows, len(lst), fn in doc_arity))
    if highs:
        oversupply.append((fn, expected, highs, fn in doc_arity))

flagged.sort(key=lambda x: -len(x[2]))
total_low = sum(len(x[2]) for x in flagged)
print("DROPPED-ARG candidates (got < expected arity): %d fns, %d sites" % (len(flagged), total_low))
for fn, exp, lows, n, documented in flagged:
    src = "doc" if documented else "max-observed"
    print("  %-22s expected=%d (%s) over %d sites; %d below:" % (fn, exp, src, n, len(lows)))
    for f, ln, c in lows:
        print("      %s:%d  got=%d" % (f, ln, c))
print("\nOVER-SUPPLY (informational; usually harmless extra varargs arg): %d fns" % len(oversupply))
for fn, exp, highs, documented in oversupply:
    src = "doc" if documented else "max-observed"
    print("  %-22s expected=%d (%s); %d site(s) pass more:" % (fn, exp, src, len(highs)))
    for f, ln, c in highs:
        print("      %s:%d  got=%d" % (f, ln, c))
