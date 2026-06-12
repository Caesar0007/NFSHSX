#!/usr/bin/env python3
"""ccpsx_gate.py — authoritative PsyQ 4.3 ccpsx compile gate for the whole tree.

Compiles every TU with the REAL PsyQ 4.3 toolchain (ccpsx -Xm -O2 -G4, the
byte-match-proven flags) and reports the ccpsx-compatibility baseline. Modern
g++/link_harness.py is only a fast pre-gate; THIS is the seal bar.

Run:  python tools/ccpsx_gate.py [--list]
Writes: _ccpsx_gate.json  (per-file status + first error + category histogram)
"""
import os, subprocess, re, json, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CCPSX = r'C:\Temp\psq43\PSSN\CCPSX.EXE'
ENV   = dict(os.environ, SN_PATH='C:/Temp/psq43/PSSN', PSYQ_PATH='C:/Temp/psq43/PSSN')
INC   = 'C:/Temp/psq43/PSX43/psx/include'                 # PsyQ 4.3 headers
FLAGS = ['-Xm', '-O2', '-G4', '-I', INC, '-c']

# error categories (first matching pattern wins). ccpsx writes diagnostics to STDOUT.
CATS = [
    ('label-no-stmt',    r'label must be followed by statement'),
    ('fnptr-mismatch',   r"passing `void ?\(\*\)"),                    # void(*)() vs void(*)(T)
    ('arg-count',        r'too (few|many) arguments'),                 # hygiene mismatch
    ('this/arg-type',    r'passing `[^`]+\*?\' as argument'),          # wrong arg/this type
    ('ptr-int-compare',  r'comparison between pointer and integer'),
    ('ptr-int-assign',   r"assignment to `[^`]+\*' from `int'"),
    ('in-chrg-shadow',   r'__in_chrg'),
    ('overload',         r'no matching function|no match(ing)? for'),
    ('ansi-forbids',     r'ANSI C\+\+ forbids'),
    ('undeclared',       r'undeclared|was not declared|undefined'),
    ('no-member',        r'has no member|no member named'),
    ('redecl',           r'redeclaration|redefinition|conflicting'),
    ('parse',            r'parse error|syntax error|expected'),
    ('no-include-path',  r'No include path'),
    ('no-such-file',     r'No input files|No such file'),
]

CONTEXT = re.compile(r': In (method|function|constructor|destructor|member)|In file included from|At (top level|global scope)|At this point|candidates are|In instantiation')

def categorize(out):
    # real error lines look like  path:LINE: message  and are not ccpsx context lines
    errlines = [l for l in out.splitlines()
                if l.strip() and 'warning' not in l.lower()
                and re.search(r':\d+:', l) and not CONTEXT.search(l)]
    for line in errlines:
        for name, pat in CATS:
            if re.search(pat, line):
                return name, re.sub(r'^.*?:\d+:', '', line).strip()[:90]
    if errlines:
        return 'other', re.sub(r'^.*?:\d+:', '', errlines[0]).strip()[:90]
    # fall back to any non-warning, non-context line
    for line in out.splitlines():
        if line.strip() and 'warning' not in line.lower() and not CONTEXT.search(line):
            return 'other2', line.strip()[:90]
    return 'unknown', ''

def find_tus():
    out = []
    for dp, _, fs in os.walk(ROOT):
        parts = dp.replace('\\', '/').split('/')
        if 'backup' in parts or '.git' in parts or 'tools' in parts:
            continue
        for f in fs:
            if f.startswith('_test_'):
                continue
            if f.endswith('.cpp') or f.endswith('.c'):
                out.append(os.path.join(dp, f))
    return sorted(out)

def main():
    tus = find_tus()
    print('ccpsx gate: %d TUs (ccpsx -Xm -O2 -G4)' % len(tus))
    results = []
    cathist = {}
    npass = 0
    for i, tu in enumerate(tus):
        rel = os.path.relpath(tu, ROOT).replace('\\', '/')
        # Our type system (nfs4_types.h) is C++-unified (classes/ctors/(*pfn)(...)):
        # the handful of .c TUs must be driven through the C++ frontend, exactly as the
        # original EA unified build did. (.cpp files auto-select C++.)
        lang = ['-x', 'c++'] if tu.endswith('.c') else []
        try:
            r = subprocess.run([CCPSX] + lang + FLAGS + [tu, '-o', os.devnull],
                               env=ENV, capture_output=True, text=True, timeout=60)
            ok = (r.returncode == 0)
            if ok:
                npass += 1
                results.append({'tu': rel, 'ok': True})
            else:
                cat, line = categorize((r.stdout or '') + '\n' + (r.stderr or ''))
                cathist[cat] = cathist.get(cat, 0) + 1
                results.append({'tu': rel, 'ok': False, 'cat': cat, 'err': line})
        except subprocess.TimeoutExpired:
            cathist['timeout'] = cathist.get('timeout', 0) + 1
            results.append({'tu': rel, 'ok': False, 'cat': 'timeout', 'err': '>60s'})
        if (i + 1) % 50 == 0:
            print('  ...%d/%d  (pass=%d)' % (i + 1, len(tus), npass))
    nfail = len(tus) - npass
    print('\n=== ccpsx baseline: %d pass / %d FAIL (of %d) ===' % (npass, nfail, len(tus)))
    print('--- failure categories ---')
    for c, n in sorted(cathist.items(), key=lambda kv: -kv[1]):
        print('  %-16s %d' % (c, n))
    json.dump({'total': len(tus), 'pass': npass, 'fail': nfail,
               'cathist': cathist, 'results': results},
              open(os.path.join(ROOT, '_ccpsx_gate.json'), 'w'), indent=1)
    if '--list' in sys.argv:
        print('\n--- failing TUs ---')
        for r in results:
            if not r['ok']:
                print('  [%-14s] %s' % (r.get('cat', '?'), r['tu']))
                if r.get('err'):
                    print('        %s' % r['err'])

if __name__ == '__main__':
    main()
