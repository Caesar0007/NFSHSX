import re, glob, os
ROOT = r'C:/Temp/claud/reconstructed_headers/tree'
os.chdir(ROOT)
spec = re.compile(r'%[-+ #0]*\d*(?:\.\d+)?[diouxXeEfgGcsp]')
def splitargs(s):
    out=[]; d=0; cur=''
    for ch in s:
        if ch in '([{': d+=1
        elif ch in ')]}': d-=1
        if ch==',' and d==0: out.append(cur); cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur)
    return out
hits=[]
for f in glob.glob('game/**/*.cpp', recursive=True)+glob.glob('*.cpp'):
    if 'backup' in f.replace('\\','/').split('/'): continue
    txt=open(f, encoding='utf-8', errors='ignore').read()
    # map: in each function, variable -> max %-spec count of any string literal assigned to it
    varspec={}
    for m in re.finditer(r'(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"', txt):
        n=len(spec.findall(m.group(2)))
        varspec[m.group(1)]=max(varspec.get(m.group(1),0), n)
    for m in re.finditer(r'\b(?:sprintf|printf|fprintf|sscanf)\s*\(', txt):
        nm=txt[m.start():m.end()-1].strip()
        i=m.end()-1; d=0; j=i
        while j<len(txt):
            if txt[j]=='(': d+=1
            elif txt[j]==')':
                d-=1
                if d==0: break
            j+=1
        args=splitargs(txt[i+1:j])
        fmtidx = 0 if nm=='printf' else 1
        if len(args)<=fmtidx: continue
        fa=args[fmtidx].strip()
        fm=re.search(r'"((?:[^"\\]|\\.)*)"', fa)
        if fm:
            nspec=len(spec.findall(fm.group(1))); kind='inline'; shown=fm.group(1)[:24]
        elif re.fullmatch(r'\w+', fa) and fa in varspec:
            nspec=varspec[fa]; kind='var:'+fa; shown='(var)'
        else:
            continue
        nsup=len(args)-fmtidx-1
        if nspec>nsup:
            ln=txt[:i].count('\n')+1
            hits.append((f.replace('\\','/'),ln,nm,nspec,nsup,kind,shown))
print("format-fn undercount bugs (inline + variable-fmt):", len(hits))
for f,ln,nm,ns,su,k,sh in hits:
    print('  %s:%d  %s specs=%d args=%d  [%s] "%s"'%(f,ln,nm,ns,su,k,sh))
