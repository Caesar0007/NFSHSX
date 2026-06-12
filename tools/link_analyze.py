#!/usr/bin/env python3
"""Analyze _link_obj/*.o with linkage-normalization.
Canonicalize every symbol to a base identifier (demangle via c++filt, drop params,
strip leading underscores) so a C-linkage reference (_foo) and a C++ definition
(__Z3foov) collapse to the same key 'foo'. Then:
  - TRUE-UNRESOLVED = base ids referenced but defined by NO object (real gaps).
  - LINKAGE-MISMATCH = base id IS defined, but raw decorated ref != raw decorated def
    (i.e. one side C, other C++) -> header hygiene, not a missing symbol.
"""
import os, subprocess, re, json
from collections import defaultdict

OBJ=r"C:/Temp/claud/_link_obj"
objs=[os.path.join(OBJ,f) for f in os.listdir(OBJ) if f.endswith(".o")]

def base_id(sym):
    # demangle; strip params; strip leading underscores; keep last ::comp for members
    d=subprocess.run(["c++filt","-p",sym],capture_output=True,text=True).stdout.strip()
    d=d.split("(")[0].strip()            # drop function params
    d=re.sub(r"^_+","",d)                 # strip PE leading underscores (C names)
    return d

# gather raw defined/undef per object
raw_def=defaultdict(set)   # rawsym -> set(obj)
raw_undef=defaultdict(set)
for op in objs:
    r=subprocess.run(["nm",op],capture_output=True,text=True)
    for ln in r.stdout.splitlines():
        p=ln.split()
        if len(p)==2 and p[0]=="U":
            raw_undef[p[1]].add(op)
        elif len(p)>=3 and p[-2] in "TtDdBbRrGgWwVvSs":
            raw_def[p[-1]].add(op)

# batch-demangle unique raw syms.
# PE prepends ONE extra '_' to every symbol: a C fn 'foo' -> '_foo'; a C++ fn
# 'CarIO_StartUp()' -> '__Z13CarIO_StartUpv'.  c++filt needs '_Z...' (single _),
# so strip exactly one leading underscore BEFORE demangling.
allsyms=sorted(set(raw_def)|set(raw_undef))
def pe_strip(s): return s[1:] if s.startswith("_") else s
proc=subprocess.run(["c++filt","-p"],input="\n".join(pe_strip(s) for s in allsyms),
                    capture_output=True,text=True)
dem=dict(zip(allsyms,proc.stdout.splitlines()))
def canon(s):
    d=dem.get(s,pe_strip(s)).split("(")[0].strip()
    return re.sub(r"^_+","",d)

def_base=set(canon(s) for s in raw_def)
undef_base=defaultdict(set)
for s,objset in raw_undef.items():
    undef_base[canon(s)] |= objset

true_unresolved=sorted(b for b in undef_base if b not in def_base)
linkage_mismatch=sorted(b for b in undef_base if b in def_base)

# split true-unresolved into DAT_ vs other, data-ish vs fn-ish
dat=[b for b in true_unresolved if re.match(r"_?DAT_[0-9a-fA-F]{6,}$",b)]
other=[b for b in true_unresolved if b not in set(dat)]

print("objects:",len(objs))
print("distinct defined base-ids:",len(def_base))
print("distinct undefined base-ids:",len(undef_base))
print("TRUE-UNRESOLVED (defined nowhere):",len(true_unresolved))
print("   of which DAT_xxxx:",len(dat))
print("   of which other:",len(other))
print("LINKAGE-MISMATCH (defined, but C/C++ decoration differs):",len(linkage_mismatch))

json.dump({
 "true_unresolved":true_unresolved,
 "dat":sorted(dat),
 "other_unresolved":sorted(other),
 "linkage_mismatch":linkage_mismatch,
 "other_refs":{b:sorted(os.path.basename(o) for o in undef_base[b]) for b in other},
}, open(r"C:/Temp/claud/_link_analysis.json","w"), indent=1)
print("\n-> C:/Temp/claud/_link_analysis.json")
print("\nOTHER true-unresolved (non-DAT), first 60:")
for b in other[:60]: print("  ",b)
