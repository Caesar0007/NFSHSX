#!/usr/bin/env python3
"""ccpsx_objs.py -- compile every TU to a real PSX .obj under PsyQ 4.3 ccpsx.

Mirrors ccpsx_gate.py's flags/env exactly (the byte-match-proven set), but emits real
object files into build_obj/ (flat, name-mangled by relpath) instead of -o nul. Output
objs feed tools/ccpsx_link.py (PSYLINK) to find the authoritative link frontier.

Run:  python tools/ccpsx_objs.py
Writes: build_obj/*.obj  +  _ccpsx_objs.json (per-TU obj path / status)
"""
import os, subprocess, json, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CCPSX = r'C:\Temp\psq43\PSSN\CCPSX.EXE'
ENV   = dict(os.environ, SN_PATH='C:/Temp/psq43/PSSN', PSYQ_PATH='C:/Temp/psq43/PSSN')
INC   = 'C:/Temp/psq43/PSX43/psx/include'
FLAGS = ['-Xm', '-O2', '-G4', '-I', INC, '-c']
OBJDIR = os.path.join(ROOT, 'build_obj')

def find_tus():
    out = []
    for dp, _, fs in os.walk(ROOT):
        parts = dp.replace('\\', '/').split('/')
        if 'backup' in parts or '.git' in parts or 'tools' in parts or 'build_obj' in parts:
            continue
        for f in fs:
            if f.startswith('_test_') or f.startswith('_ccpsxtest'):
                continue
            if f.endswith('.cpp') or f.endswith('.c'):
                out.append(os.path.join(dp, f))
    return sorted(out)

def objname(rel):
    # flatten relpath -> unique obj name (dir__file.obj)
    return rel.replace('\\', '/').replace('/', '__').rsplit('.', 1)[0] + '.obj'

def main():
    os.makedirs(OBJDIR, exist_ok=True)
    tus = find_tus()
    print('ccpsx_objs: %d TUs -> %s' % (len(tus), OBJDIR))
    results, npass = [], 0
    for i, tu in enumerate(tus):
        rel = os.path.relpath(tu, ROOT).replace('\\', '/')
        obj = os.path.join(OBJDIR, objname(rel))
        lang = ['-x', 'c++'] if tu.endswith('.c') else []
        try:
            r = subprocess.run([CCPSX] + lang + FLAGS + [tu, '-o', obj],
                               env=ENV, capture_output=True, text=True, timeout=60)
            ok = (r.returncode == 0 and os.path.exists(obj))
        except subprocess.TimeoutExpired:
            ok = False
        if ok:
            npass += 1
            results.append({'tu': rel, 'obj': objname(rel), 'ok': True})
        else:
            results.append({'tu': rel, 'ok': False})
        if (i + 1) % 100 == 0:
            print('  ...%d/%d (obj=%d)' % (i + 1, len(tus), npass))
    print('=== %d/%d objs emitted ===' % (npass, len(tus)))
    json.dump({'total': len(tus), 'pass': npass, 'results': results},
              open(os.path.join(ROOT, '_ccpsx_objs.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
