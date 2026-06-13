#!/usr/bin/env python3
"""ccpsx_link.py -- PSYLINK all build_obj/*.obj + PsyQ libs; report the authoritative
(GNU-v2-mangled) link frontier = unresolved external symbols.

PSYLINK takes args DIRECTLY on argv (no useful @command-file). Structure:
  PSYLINK /c /m /l <libdir> obj1 obj2 ... ,out.cpe,out.sym,out.map,lib1.lib lib2.lib ...
Run from cwd=build_obj with relative obj names so 515 objs fit the ~32KB cmdline limit.

Run:  python tools/ccpsx_link.py
Writes _ccpsx_link.txt (full PSYLINK output) + prints the unresolved-symbol frontier.
"""
import os, glob, subprocess, re

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSYLINK = r'C:\Temp\psq43\PSSN\PSYLINK.EXE'
ENV     = dict(os.environ, SN_PATH='C:/Temp/psq43/PSSN', PSYQ_PATH='C:/Temp/psq43/PSSN')
LIBDIR  = r'C:\Temp\psq43\PSX43\psx\lib'
OBJDIR  = os.path.join(ROOT, 'build_obj')
LIBS = ['libgte', 'libgpu', 'libgs', 'libetc', 'libapi', 'libcard', 'libmcrd', 'libspu',
        'libsnd', 'libcd', 'libpad', 'libpress', 'libmath', 'libc2', 'libc', 'libsn']

def main():
    names = [os.path.basename(o) for o in sorted(glob.glob(os.path.join(OBJDIR, '*.obj')))]
    libtok = ',_link.cpe,_link.sym,_link.map,' + LIBS[0] + '.lib'
    argv = [PSYLINK, '/c', '/m', '/l', LIBDIR] + names + [libtok] + [l + '.lib' for l in LIBS[1:]]
    print('PSYLINK: %d objs + %d libs (cmdline %d chars)' % (len(names), len(LIBS), sum(len(a)+1 for a in argv)))
    r = subprocess.run(argv, env=ENV, cwd=OBJDIR, capture_output=True, text=True, timeout=300)
    out = (r.stdout or '') + (r.stderr or '')
    open(os.path.join(ROOT, '_ccpsx_link.txt'), 'w').write(out)
    # PSYLINK unresolved-reference lines
    unres = sorted(set(re.findall(r"[Uu]nresolved reference to [\'\"]?([A-Za-z0-9_$.]+)", out)
                       + re.findall(r"Unsatisfied .*?[\'\"]([A-Za-z0-9_$.]+)", out)))
    nerr = re.search(r'(\d+) error', out)
    print('RC=%d  %s' % (r.returncode, (nerr.group(0) if nerr else '')))
    print('--- output tail ---')
    for ln in out.splitlines()[-20:]:
        print('  ' + ln)
    print('--- %d unresolved symbols (frontier) ---' % len(unres))
    for s in unres:
        print('  ' + s)

if __name__ == '__main__':
    main()
