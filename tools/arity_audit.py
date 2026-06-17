import re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 1) documented arity of each (...) function, from lib headers' trailing comments
arity={}
for hdr in ['lib/libfns.h','lib/eaclib.h']:
    if not os.path.exists(hdr): continue
    for line in open(hdr,encoding='utf-8',errors='ignore'):
        m=re.search(r'([A-Za-z_]\w*)\s*\(\s*\.\.\.\s*\)\s*;\s*/\*\s*\((.*?)\)', line)
        if not m: continue
        fn, params = m.group(1), m.group(2).strip()
        if params=='' or params=='void': n=0
        else:
            d=0; n=1
            for ch in params:
                if ch in '([{': d+=1
                elif ch in ')]}': d-=1
                elif ch==',' and d==0: n+=1
        arity[fn]=n

def strip_noncode(t):
    t=re.sub(r'/\*.*?\*/',lambda m:'\n'*m.group(0).count('\n'),t,flags=re.S)  # block comments (keep line count)
    t=re.sub(r'//[^\n]*',' ',t)                   # line comments
    t=re.sub(r'"(?:[^"\\]|\\.)*"','""',t)         # string literals
    return t

def splitargs(s):
    out=[]; d=0; cur=''
    for ch in s:
        if ch in '([{': d+=1
        elif ch in ')]}': d-=1
        if ch==',' and d==0: out.append(cur); cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur)
    return out

SKIP={'sprintf','printf','fprintf','sscanf','scanf'}  # format-fns audited separately
hits=[]
for f in glob.glob('game/**/*.cpp',recursive=True)+glob.glob('*.cpp'):
    if 'backup' in f.replace('\\','/').split('/'): continue
    txt=strip_noncode(open(f,encoding='utf-8',errors='ignore').read())
    for m in re.finditer(r'\b([A-Za-z_]\w*)\s*\(', txt):
        fn=m.group(1)
        if fn not in arity or fn in SKIP: continue
        want=arity[fn]
        if want<2: continue
        i=m.end()-1; d=0; j=i
        while j<len(txt):
            if txt[j]=='(': d+=1
            elif txt[j]==')':
                d-=1
                if d==0: break
            j+=1
        inner=txt[i+1:j].strip()
        got=0 if inner=='' else len(splitargs(inner))
        if got<want:
            ln=txt[:i].count('\n')+1
            hits.append((f.replace('\\','/'),ln,fn,want,got))
print("calls with FEWER args than documented arity (>=2-arg fns, excl. format):", len(hits))
from collections import Counter
for fn,c in Counter(h[2] for h in hits).most_common():
    print("  %-22s %d call(s)  (wants %d)"%(fn,c,arity[fn]))
print('---')
for f,ln,fn,w,g in hits:
    print('  %s:%d  %s  wants=%d got=%d'%(f,ln,fn,w,g))
