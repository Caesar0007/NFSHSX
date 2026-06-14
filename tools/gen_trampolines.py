"""Flat->member trampolines for the PSX LINK phase. v4 = v3 (member-as-free) + ctor/dtor
flat wrappers (placement-new ctor / explicit dtor)."""
import os, re, glob, subprocess
ROOT='C:/Temp/claud/reconstructed_headers/tree'
INC='C:/Temp/psq43/PSX43/psx/include'
ENV=dict(os.environ, SN_PATH='C:/Temp/psq43/PSSN', PSYQ_PATH='C:/Temp/psq43/PSSN')
CCPSX=r'C:\Temp\psq43\PSSN\CCPSX.EXE'
OUT=ROOT+'/link_trampolines.cpp'

def norm(s):
    s=re.sub(r'\s+','',re.sub(r'\b(struct|class|const)\b','',s))
    return s.replace('shortint','short').replace('longint','long').replace('unsignedint','unsigned').replace('signedint','int')
def split_params(s):
    out=[]; d=0; cur=''
    for ch in s:
        if ch in '<([': d+=1
        elif ch in '>)]': d-=1
        if ch==',' and d==0: out.append(cur.strip()); cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur.strip())
    return out
def ptype(p):
    p=p.strip(); return re.sub(r'\b[A-Za-z_]\w*\s*$','',p).strip() or p

# members + ctor/dtor availability
members={}
defre=re.compile(r'^([A-Za-z_][\w\s\*&]*?[\s\*&])([A-Za-z_]\w*)::(~?[A-Za-z_]\w*)\s*\(([^)]*)\)')
ctordefs=re.compile(r'^\s*([A-Za-z_]\w*)::\1\s*\(([^)]*)\)')   # Class::Class(
dtordefs=re.compile(r'^\s*([A-Za-z_]\w*)::~\1\s*\(')
has_dctor=set(); has_dtor=set()
for cpp in glob.glob(ROOT+'/**/*.cpp', recursive=True):
    if '/backup/' in cpp.replace('\\','/'): continue
    for line in open(cpp, encoding='utf-8', errors='replace'):
        if '::' not in line or '(' not in line: continue
        m=defre.match(line)
        if m:
            members.setdefault((m.group(2),m.group(3)),[]).append((m.group(1).strip(),[ptype(x) for x in split_params(m.group(4))]))
        c=ctordefs.match(line)
        if c and not split_params(c.group(2)): has_dctor.add(c.group(1))   # default ctor
        d=dtordefs.match(line)
        if d: has_dtor.add(d.group(1))
classes={c for c,_ in members}
print('members',len(members),'classes',len(classes),'default-ctor',len(has_dctor),'dtor',len(has_dtor))

proto=re.compile(r'^([A-Za-z_][\w\s\*&:]*?[\s\*&])([A-Za-z_]\w*)\s*\(([^()]*)\)\s*$')
def first_class(a):
    if '*' not in a: return None
    t=re.sub(r'^(const|struct|class)\s+','',a[:a.index('*')].strip()).strip()
    return t if t in classes else None

memb={}; cdtor={}
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
            key=(name,tuple(norm(ptype(a)) for a in args))
            mm=re.match(r'^(\w+)_(ctor|dtor|dt|ct)$', name)
            if mm:
                cls=mm.group(1); kind=mm.group(2)
                if kind in ('ctor',) and cls in has_dctor:
                    cdtor.setdefault(key,(name,args,cls,'ctor'))
                elif kind in ('dtor','dt') and cls in has_dtor:
                    cdtor.setdefault(key,(name,args,cls,'dtor'))
                continue
            cls=first_class(args[0])
            if cls and (cls,name) in members:
                memb.setdefault(key,(ret,name,args,cls))
print('member-trampolines',len(memb),' cdtor-trampolines',len(cdtor))

def emit_memb(ret,name,args,cls):
    at=[ptype(a) for a in args]; params=['%s a%d'%(t,i) for i,t in enumerate(at)]
    nm=len(args)-1; ov=None; mr=None
    for r,ps in members[(cls,name)]:
        if len(ps)==nm: ov=ps; mr=r; break
    cp=[]
    for j in range(1,len(args)):
        flat=at[j]; mp=ov[j-1] if ov else None
        if mp is not None and '&' not in flat and '*' in flat and ('&' in mp or '*' not in mp):
            cp.append('*(%s*)a%d'%(mp.replace('&','').strip(),j) if norm(flat)=='void*' else '*a%d'%j)
        else: cp.append('a%d'%j)
    body='a0->%s(%s)'%(name,', '.join(cp))
    if norm(ret)=='void': inner='  %s;'%body
    elif mr is not None and norm(mr)=='void': inner='  %s;\n  return (%s)0;'%(body,ret)
    else: inner='  return (%s)(%s);'%(ret,body)
    return '%s %s(%s) {\n%s\n}\n'%(ret,name,', '.join(params),inner)

def emit_cdtor(name,args,cls,kind):
    at=[ptype(a) for a in args]; params=['%s a%d'%(t,i) for i,t in enumerate(at)]
    if kind=='ctor':
        inner='  new((void*)a0) %s();'%cls
    else:
        inner='  ((%s*)a0)->~%s();'%(cls,cls)
    return 'void %s(%s) {\n%s\n}\n'%(name,', '.join(params),inner)

def write(am,ac):
    with open(OUT,'w',encoding='utf-8') as w:
        w.write('/* link_trampolines.cpp -- AUTO-GENERATED flat->member bridges (LINK phase). */\n')
        w.write('#include "nfs4_types.h"\n')
        w.write('#include <stddef.h>\n')
        w.write('inline void* operator new(size_t, void* p) { return p; }\n\n')
        for k in am: w.write(emit_memb(*memb[k]))
        for k in ac: w.write(emit_cdtor(*cdtor[k]))

def compile_once():
    r=subprocess.run([CCPSX,'-Xm','-O2','-G4','-I',INC,'-c',OUT,'-o','C:/Temp/nfs4-clean/_tramp.obj'],
                     env=ENV,capture_output=True,text=True,cwd=ROOT)
    return r.returncode,(r.stdout or '')+(r.stderr or '')

am=list(memb); ac=list(cdtor)
for it in range(120):
    write(am,ac)
    rc,out=compile_once()
    if rc==0:
        print('COMPILE OK: %d member + %d cdtor = %d trampolines'%(len(am),len(ac),len(am)+len(ac))); break
    bad=set(); cur=None
    for ln in out.splitlines():
        fm=re.search(r"In (?:function|method) `[^`]*?\b([A-Za-z_]\w*)\s*\(([^`]*)\)'", ln)
        if fm: cur=(fm.group(1), tuple(norm(x) for x in split_params(fm.group(2))))
        if cur and re.search(r'no matching|no member|redefinition|undeclared|not a member|cannot|conflicting|ambiguous|invalid|private|protected|abstract', ln):
            bad.add(cur)
    b4=len(am)+len(ac)
    am=[k for k in am if (memb[k][1],tuple(norm(ptype(a)) for a in memb[k][2])) not in bad and k not in bad]
    ac=[k for k in ac if (cdtor[k][0],tuple(norm(ptype(a)) for a in cdtor[k][1])) not in bad and k not in bad]
    if len(am)+len(ac)==b4:
        print('iter %d stuck:'%it); print('\n'.join(l for l in out.splitlines() if 'link_trampolines' in l)[:1600]); break
    print('iter %d: %d left'%(it,len(am)+len(ac)))
print('FINAL: %d member + %d cdtor'%(len(am),len(ac)))
