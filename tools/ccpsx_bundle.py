#!/usr/bin/env python3
"""ccpsx_bundle.py -- bundle all build_obj/*.obj into ONE PsyQ library build_obj/nfs4.lib
via PSYLIB2 (chunked /a adds, each call short enough for PSYLINK's ~512B cmdline buffer).

Why a lib: PSYLINK cannot take 515 .obj on its command line (hard ~512-byte buffer). A lib
is one file; PSYLINK then pulls modules transitively from a root obj. nfs4.lib is also the
natural single ship-artifact ("the whole reconstructed game as a PsyQ .lib").

Prereq: tools/ccpsx_objs.py (build_obj/*.obj). Run: python tools/ccpsx_bundle.py
"""
import os, glob, subprocess, shutil

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSYLIB = r'C:\Temp\psq43\PSSN\PSYLIB2.EXE'
ENV    = dict(os.environ, SN_PATH='C:/Temp/psq43/PSSN', PSYQ_PATH='C:/Temp/psq43/PSSN')
OBJDIR = os.path.join(ROOT, 'build_obj')
SHORT  = os.path.join(OBJDIR, 's')   # short-named copies (NNN.obj) for cmdline brevity
LIB    = os.path.join(SHORT, 'nfs4.lib')

def main():
    os.makedirs(SHORT, exist_ok=True)
    objs = sorted(glob.glob(os.path.join(OBJDIR, '*.obj')))
    mapping = {}
    for i, o in enumerate(objs):
        sn = '%03d.obj' % i
        shutil.copy(o, os.path.join(SHORT, sn))
        mapping[sn] = os.path.basename(o)
    import json
    json.dump(mapping, open(os.path.join(SHORT, '_map.json'), 'w'))
    if os.path.exists(LIB):
        os.remove(LIB)
    names = ['%03d.obj' % i for i in range(len(objs))]
    CH = 40   # ~40 * 8 = 320 bytes/call, under the buffer
    added = 0
    for i in range(0, len(names), CH):
        chunk = names[i:i+CH]
        r = subprocess.run([PSYLIB, '/q', '/a', 'nfs4.lib'] + chunk, env=ENV, cwd=SHORT,
                           capture_output=True, text=True)
        if r.returncode != 0:
            print('CHUNK FAIL @%d: %s' % (i, (r.stdout or r.stderr)[:200])); return
        added += len(chunk)
    # verify module count via /l
    r = subprocess.run([PSYLIB, '/l', 'nfs4.lib'], env=ENV, cwd=SHORT, capture_output=True, text=True)
    nmod = r.stdout.count("Module '")
    print('nfs4.lib: added %d objs, %d modules in archive, %d bytes'
          % (added, nmod, os.path.getsize(LIB)))

if __name__ == '__main__':
    main()
