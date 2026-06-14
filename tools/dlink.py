#!/usr/bin/env python3
"""Authoritative first-light link (durable copy in tools/).
ccpsx-direct: force-include ALL build_obj/s/NNN.obj so every unresolved ref is
exposed (ccpsx writes a psylink response file + auto-adds crt0/stdlibs). Parses
unresolved + multiply-defined and writes build_obj/s/_unres.txt.

Pipeline to refresh from source:
  python tools/ccpsx_objs.py            # compile all TUs -> build_obj/*.obj
  ccpsx -c link_aliases.s    -o build_obj/link_aliases.obj
  ccpsx -c link_trampolines.cpp ...      # (already part of objs build)
  python tools/ccpsx_bundle.py          # short-name copies + nfs4.lib
  python tools/dlink.py                  # link + measure
"""
import subprocess, os, re, glob

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S     = os.path.join(ROOT, 'build_obj', 's')
CCPSX = r'C:\Temp\psq43\PSSN\CCPSX.EXE'
ENV = dict(os.environ, SN_PATH='C:/Temp/psq43/PSSN', PSYQ_PATH='C:/Temp/psq43/PSSN',
           PATH='C:/Temp/psq43/PSX43/psx/bin;C:/Temp/psq43/PSSN;' + os.environ.get('PATH',''))
objs = sorted(os.path.basename(p) for p in glob.glob(os.path.join(S, '[0-9]*.obj')))
stdlibs = ['-llibgte','-llibgpu','-llibgs','-llibetc','-llibapi','-llibcard',
           '-llibmcrd','-llibspu','-llibsnd','-llibcd','-llibpad','-llibpress',
           '-llibmath','-llibc2']
argv = [CCPSX] + objs + ['-o','nfs4.cpe'] + stdlibs
r = subprocess.run(argv, env=ENV, cwd=S, capture_output=True, text=True, timeout=600)
out = (r.stdout or '') + (r.stderr or '')
open(os.path.join(S, '_dlink_out.txt'), 'w').write(out)

unres, multi = [], []
for line in out.splitlines():
    m = re.search(r"Symbol '([^']+)' not defined", line);      m and unres.append(m.group(1))
    m = re.search(r"'([^']+)' (?:is )?unresolved", line, re.I); m and unres.append(m.group(1))
    m = re.search(r"Symbol '([^']+)' multiply defined", line);  m and multi.append(m.group(1))
unres = sorted(set(unres)); multi = sorted(set(multi))
open(os.path.join(S, '_unres.txt'), 'w').write("\n".join(unres) + ("\n" if unres else ""))

cpe = os.path.join(S, 'nfs4.cpe')
print("rc=%d  objs=%d" % (r.returncode, len(objs)))
print("CPE bytes:", os.path.getsize(cpe) if os.path.exists(cpe) else 'NONE')
print("unresolved:", len(unres), " multiply-defined:", len(multi))
if multi: print("  MULTI:", multi[:30])
if unres and len(unres) <= 60:
    print("  UNRES:", ' '.join(unres))
