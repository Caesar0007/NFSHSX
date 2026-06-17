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
files = glob.glob('game/**/*.cpp', recursive=True) + glob.glob('*.cpp')
for f in files:
    if 'backup' in f.replace('\\','/').split('/'): continue
    txt=open(f, encoding='utf-8', errors='ignore').read()
    for m in re.finditer(r'\bsprintf\s*\(', txt):
        i=m.end()-1; d=0; j=i
        while j < len(txt):
            if txt[j]=='(': d+=1
            elif txt[j]==')':
                d-=1
                if d==0: break
            j+=1
        args=splitargs(txt[i+1:j])
        if len(args) < 2: continue
        fm=re.search(r'"((?:[^"\\]|\\.)*)"', args[1].strip())
        if not fm: continue
        nspec=len(spec.findall(fm.group(1)))
        nsup=len(args)-2
        if nspec > nsup:
            ln=txt[:i].count('\n')+1
            hits.append((f.replace('\\','/'), ln, nspec, nsup, fm.group(1)[:34]))
print("sprintf undercount bugs (inline-fmt only):", len(hits))
for f,ln,ns,su,fmt in hits:
    print('  %s:%d  specs=%d args=%d  "%s"' % (f,ln,ns,su,fmt))
