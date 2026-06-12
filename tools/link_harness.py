#!/usr/bin/env python3
"""Whole-tree LINK harness for the NFS4-F reconstruction.
Compiles every non-backup .cpp to a host -m32 object (from its own dir so relative
includes resolve), then uses `nm` to compute the global symbol balance:
  - which symbols are DEFINED somewhere in the tree
  - which are UNDEFINED (referenced but never defined) across all objects
The residual undefined set = what still makes the tree NOT self-contained.
Run:  python3 link_harness.py
"""
import os, subprocess, sys, re, json
from collections import defaultdict

ROOT = r"C:/Temp/claud/reconstructed_headers/tree"
OBJ  = r"C:/Temp/claud/_link_obj"
os.makedirs(OBJ, exist_ok=True)
CXX  = "g++"
FLAGS = ["-m32","-std=gnu++98","-fpermissive","-w","-c","-fno-exceptions"]

def find_tus():
    out=[]
    for dp,_,fs in os.walk(ROOT):
        if "backup" in dp.replace("\\","/").split("/"): continue
        for f in fs:
            if f.startswith("_test_"): continue           # validation scaffolds, not NFS4 source (use host libm/printf)
            if f.endswith(".cpp") or f.endswith(".c"):   # .c TUs (spchevnt/memcard/pad/unpack/textpsx/textpix)
                out.append(os.path.join(dp,f))
    return sorted(out)

def main():
    tus=find_tus()
    print("TUs: %d"%len(tus))
    compile_fail=[]; objs=[]
    for i,tu in enumerate(tus):
        d=os.path.dirname(tu); base=os.path.basename(tu)
        # unique obj name from relative path
        rel=os.path.relpath(tu,ROOT).replace("\\","_").replace("/","_").replace(".cpp",".o").replace(".c","_c.o")
        op=os.path.join(OBJ,rel)
        xflag=["-x","c++"] if base.endswith(".c") else []   # force C++ for the .c TUs
        r=subprocess.run([CXX]+xflag+FLAGS+[base,"-o",op],cwd=d,
                         capture_output=True,text=True)
        if r.returncode!=0:
            compile_fail.append((tu,r.stderr))
        else:
            objs.append(op)
        if (i+1)%50==0: print("  ...%d/%d compiled (%d fail)"%(i+1,len(tus),len(compile_fail)))
    print("compiled OK: %d ; FAILED: %d"%(len(objs),len(compile_fail)))

    # symbol balance via nm
    defined=set(); undef=defaultdict(list)
    for op in objs:
        r=subprocess.run(["nm",op],capture_output=True,text=True)
        for ln in r.stdout.splitlines():
            parts=ln.split()
            if len(parts)==2 and parts[0]=="U":
                undef[parts[1]].append(op)
            elif len(parts)>=3:
                typ=parts[-2]; nm=parts[-1]
                if typ in "TtDdBbRrGgWwVvSs":
                    defined.add(nm)
    unresolved=sorted(s for s in undef if s not in defined)
    print("defined syms: %d ; distinct undefined: %d ; UNRESOLVED (undef-not-defined): %d"
          %(len(defined),len(undef),len(unresolved)))

    json.dump({
        "tus":len(tus),"compiled":len(objs),"failed":len(compile_fail),
        "compile_fail":[t for t,_ in compile_fail],
        "unresolved":unresolved,
        "unresolved_refs":{s:[os.path.basename(o) for o in undef[s]] for s in unresolved},
    },open(r"C:/Temp/claud/_link_report.json","w"),indent=1)
    # dump compile errors
    with open(r"C:/Temp/claud/_link_compile_errors.txt","w") as fh:
        for t,e in compile_fail:
            fh.write("=== %s ===\n%s\n"%(t,e))
    print("report -> C:/Temp/claud/_link_report.json")
    print("\nFirst 40 unresolved:")
    for s in unresolved[:40]: print("  ",s)

if __name__=="__main__":
    main()
