"""Generate flat->member trampolines, but ONLY for (Class, method) pairs that are REAL
C++ members (scraped from 'Class::method' definitions in the .cpp tree). Avoids matching
real free functions whose first arg merely happens to be a pointer."""
import os, re, glob, subprocess
ROOT='C:/Temp/claud/reconstructed_headers/tree'
INC='C:/Temp/psq43/PSX43/psx/include'
ENV=dict(os.environ, SN_PATH='C:/Temp/psq43/PSSN', PSYQ_PATH='C:/Temp/psq43/PSSN')
CCPSX=r'C:\Temp\psq43\PSSN\CCPSX.EXE'
OUT=ROOT+'/link_trampolines.cpp'

# 1. real members (Class,method)->ret  from 'ret Class::method(' definitions
members={}
defre=re.compile(r'^([A-Za-z_][\w\s\*&]*?[\s\*&])([A-Za-z_]\w*)::(~?[A-Za-z_]\w*)\s*\(')
for cpp in glob.glob(ROOT+'/**/*.cpp', recursive=True):
    if '/backup/' in cpp.replace('\\','/'): continue
    for line in open(cpp, encoding='utf-8', errors='replace'):
        if '::' not in line or '(' not in line: continue
        m=defre.match(line)
        if m:
            ret=m.group(1).strip(); cls=m.group(2); meth=m.group(3)
            members.setdefault((cls,meth), ret)
classes={c for c,_ in members}
print('real members:', len(members), ' classes:', len(classes))

# 2. flat method-trampoline candidates from *_externs.h
proto=re.compile(r'^([A-Za-z_][\w\s\*&:]*?[\s\*&])([A-Za-z_]\w*)\s*\(([^()]*)\)\s*$')
def split_top(s): return [a.strip() for a in s.split(',') if a.strip()]
def arg_classname(a):
    if '*' not in a: return None
    t=a[:a.index('*')].strip()           # type before first *
    t=re.sub(r'^(const|struct|class)\s+','',t).strip()
    return t if t in classes else None

cands={}
for h in glob.glob(ROOT+'/**/*_externs.h', recursive=True):
    if '/backup/' in h.replace('\\','/'): continue
    for raw in open(h, encoding='utf-8', errors='replace'):
        for part in raw.split(';'):
            part=part.strip()
            if '(' not in part or ')' not in part or '...' in part: continue
            if part.startswith(('//','*','/*','#','extern','class','struct','typedef')): continue
            m=proto.match(part)
            if not m: continue
            ret=m.group(1).strip(); name=m.group(2); args=split_top(m.group(3))
            if not args: continue
            cls=arg_classname(args[0])
            if not cls or (cls,name) not in members: continue
            norm=lambda a: re.sub(r'\s+','',re.sub(r'\b(struct|class|const)\b','',a))
            key=(name, tuple(norm(a) for a in args))
            cands.setdefault(key,(ret,name,args,cls))
print('member-trampoline candidates:', len(cands))

def emit(ret,name,args,cls):
    params=[]
    for i,a in enumerate(args):
        t=re.sub(r'\b[A-Za-z_]\w*\s*$','',a).strip() or a   # type, drop param name
        params.append('%s a%d'%(t,i))
    call=', '.join('a%d'%i for i in range(1,len(args)))
    body='a0->%s(%s)'%(name,call)
    if re.sub(r'\s+','',ret)=='void': inner='  %s;'%body
    else: inner='  return (%s)(%s);'%(ret,body)
    return '%s %s(%s) {\n%s\n}\n'%(ret, name, ', '.join(params), inner)

def write(active):
    with open(OUT,'w',encoding='utf-8') as w:
        w.write('/* link_trampolines.cpp -- AUTO-GENERATED flat->member bridges (LINK phase). */\n')
        w.write('#include "nfs4_types.h"\n\n')
        for k in active:
            ret,name,args,cls=cands[k]; w.write(emit(ret,name,args,cls))

def compile_once():
    r=subprocess.run([CCPSX,'-Xm','-O2','-G4','-I',INC,'-c',OUT,'-o','C:/Temp/nfs4-clean/_tramp.obj'],
                     env=ENV, capture_output=True, text=True, cwd=ROOT)
    return r.returncode,(r.stdout or '')+(r.stderr or '')

active=list(cands.keys())
for it in range(60):
    write(active)
    rc,out=compile_once()
    if rc==0:
        print('COMPILE OK: %d trampolines (%d dropped)'%(len(active),len(cands)-len(active))); break
    bad=set(); curfn=None
    for ln in out.splitlines():
        fm=re.search(r"In (?:function|method) `.*?\b([A-Za-z_]\w*)\s*\(", ln)
        if fm: curfn=fm.group(1)
        if curfn and re.search(r'no matching function|no member|redefinition|undeclared|not a member|cannot|conflicting|ambiguous', ln):
            bad.add(curfn)
    before=len(active)
    active=[k for k in active if cands[k][1] not in bad]
    if len(active)==before:
        print('iter %d rc=%d no-progress. errs:'%(it,rc))
        print('\n'.join(l for l in out.splitlines() if 'link_trampolines' in l)[:1600]); break
    print('iter %d: dropped %d names, %d left'%(it,before-len(active),len(active)))
print('wrote', OUT, 'with', len(active), 'trampolines')
