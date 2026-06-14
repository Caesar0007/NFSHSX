"""Generate flat->member trampolines for the PSX LINK phase. v3:
per-signature compile-drop (keeps good overloads) + ref/value-vs-pointer arg adaptation."""
import os, re, glob, subprocess
ROOT='C:/Temp/claud/reconstructed_headers/tree'
INC='C:/Temp/psq43/PSX43/psx/include'
ENV=dict(os.environ, SN_PATH='C:/Temp/psq43/PSSN', PSYQ_PATH='C:/Temp/psq43/PSSN')
CCPSX=r'C:\Temp\psq43\PSSN\CCPSX.EXE'
OUT=ROOT+'/link_trampolines.cpp'

def norm(s): return re.sub(r'\s+','',re.sub(r'\b(struct|class|const)\b','',s))

def split_params(s):
    out=[]; depth=0; cur=''
    for ch in s:
        if ch in '<([': depth+=1
        elif ch in '>)]': depth-=1
        if ch==',' and depth==0: out.append(cur.strip()); cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur.strip())
    return out

def ptype(p):
    p=p.strip()
    return re.sub(r'\b[A-Za-z_]\w*\s*$','',p).strip() or p

members={}
defre=re.compile(r'^([A-Za-z_][\w\s\*&]*?[\s\*&])([A-Za-z_]\w*)::(~?[A-Za-z_]\w*)\s*\(([^)]*)\)')
for cpp in glob.glob(ROOT+'/**/*.cpp', recursive=True):
    if '/backup/' in cpp.replace('\\','/'): continue
    for line in open(cpp, encoding='utf-8', errors='replace'):
        if '::' not in line or '(' not in line: continue
        m=defre.match(line)
        if not m: continue
        ret=m.group(1).strip(); cls=m.group(2); meth=m.group(3)
        ps=[ptype(x) for x in split_params(m.group(4))]
        members.setdefault((cls,meth),[]).append((ret,ps))
classes={c for c,_ in members}
print('members:',len(members),'classes:',len(classes))

proto=re.compile(r'^([A-Za-z_][\w\s\*&:]*?[\s\*&])([A-Za-z_]\w*)\s*\(([^()]*)\)\s*$')
def first_class(a):
    if '*' not in a: return None
    t=re.sub(r'^(const|struct|class)\s+','',a[:a.index('*')].strip()).strip()
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
            ret=m.group(1).strip(); name=m.group(2); args=split_params(m.group(3))
            if not args: continue
            cls=first_class(args[0])
            if not cls or (cls,name) not in members: continue
            cands.setdefault((name,tuple(norm(ptype(a)) for a in args)),(ret,name,args,cls))
print('candidates:',len(cands))

def emit(ret,name,args,cls):
    argtypes=[ptype(a) for a in args]
    params=['%s a%d'%(t,i) for i,t in enumerate(argtypes)]
    nmember=len(args)-1; ov=None; movret=None
    for r,ps in members[(cls,name)]:
        if len(ps)==nmember: ov=ps; movret=r; break
    callparts=[]
    for j in range(1,len(args)):
        flat=argtypes[j]; mp=ov[j-1] if ov else None
        if mp is not None and '&' not in flat and '*' in flat and ('&' in mp or '*' not in mp):
            if norm(flat)=='void*':
                base=mp.replace('&','').strip()          # cast void* to member type before deref
                callparts.append('*(%s*)a%d'%(base,j))
            else:
                callparts.append('*a%d'%j)
        else:
            callparts.append('a%d'%j)
    body='a0->%s(%s)'%(name,', '.join(callparts))
    if norm(ret)=='void':
        inner='  %s;'%body
    elif movret is not None and norm(movret)=='void':
        inner='  %s;\n  return (%s)0;'%(body,ret)   # member is void; flat expects a value
    else:
        inner='  return (%s)(%s);'%(ret,body)
    return '%s %s(%s) {\n%s\n}\n'%(ret,name,', '.join(params),inner)

def write(active):
    with open(OUT,'w',encoding='utf-8') as w:
        w.write('/* link_trampolines.cpp -- AUTO-GENERATED flat->member bridges (LINK phase). */\n')
        w.write('#include "nfs4_types.h"\n\n')
        for k in active: w.write(emit(*cands[k]))

def compile_once():
    r=subprocess.run([CCPSX,'-Xm','-O2','-G4','-I',INC,'-c',OUT,'-o','C:/Temp/nfs4-clean/_tramp.obj'],
                     env=ENV,capture_output=True,text=True,cwd=ROOT)
    return r.returncode,(r.stdout or '')+(r.stderr or '')

active=list(cands.keys())
for it in range(80):
    write(active)
    rc,out=compile_once()
    if rc==0:
        print('COMPILE OK: %d trampolines (%d dropped)'%(len(active),len(cands)-len(active))); break
    bad=set(); cur=None
    for ln in out.splitlines():
        fm=re.search(r"In (?:function|method) `[^`]*?\b([A-Za-z_]\w*)\s*\(([^`]*)\)'", ln)
        if fm:
            cur=(fm.group(1), tuple(norm(x) for x in split_params(fm.group(2))))
        if cur and re.search(r'no matching|no member|redefinition|undeclared|not a member|cannot|conflicting|ambiguous|invalid', ln):
            bad.add(cur)
    before=len(active)
    active=[k for k in active if k not in bad]
    if len(active)==before:
        bn=set(re.findall(r'\b([A-Za-z_]\w*)\s*\(', '\n'.join(l for l in out.splitlines() if 'link_trampolines' in l and re.search(r'no matching|no member|undeclared|cannot|conflicting',l))))
        active=[k for k in active if k[0] not in bn]
        if len(active)==before:
            print('iter %d stuck:'%it); print('\n'.join(l for l in out.splitlines() if 'link_trampolines' in l)[:1800]); break
    print('iter %d: dropped %d, %d left'%(it,before-len(active),len(active)))
print('FINAL trampolines:',len(active))
