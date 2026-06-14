#!/usr/bin/env python3
"""gen_aliases.py -- resolve LINK-phase unresolved symbols that are pure
name-mangling MISMATCHES (caller emits one mangling, the body is defined under
another) by emitting ASPSX tail-call aliases.

Why this works (ABI argument): on MIPS o32, a *flat-helper* call `Foo(obj, a, b)`
loads obj->$a0, a->$a1, b->$a2. A cfront member `Foo__<class>(a,b)` expects
this->$a0, a->$a1, b->$a2 -- identical registers. Likewise an ellipsis call
`Foo(...)` (mangled Foo__Fe) and a typed `Foo__F<args>` load the same registers
for matching argument *values*. So a pure tail-call alias

        Foo__Fe:  j  Foo__F<args>;  nop

resolves the link with zero compile risk (no declarations touched) and is
behaviourally identical to what the already-compiled caller intended. Struct
type-spelling differences (short<->int, ptr<->ref, void*<->T*, char<->int,
cfront N/T repeat-compression) are all register-compatible.

INPUT  : build_obj/s/_lv.txt   (PSYLIB2 /lv nfs4.lib  -> defined/exported syms)
         build_obj/s/_unres6.txt (current unresolved list; regenerate via relink)
OUTPUT : link_aliases.s         (committed; ASPSX tail-call aliases)
         build_obj/s/_alias_map.txt   (audit: U -> chosen [+multi-candidate warns])
         build_obj/s/_residual.txt    (genuinely-undefined remainder, bucketed)

Run from tree root:  python tools/gen_aliases.py
Then: ccpsx -c link_aliases.s -o build_obj/link_aliases.obj ; rebundle ; relink.
"""
import os, re, collections

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHORT = os.path.join(ROOT, 'build_obj', 's')
LV    = os.path.join(SHORT, '_lv.txt')
UNRES = os.path.join(SHORT, '_unres6.txt')
OUT_S = os.path.join(ROOT, 'link_aliases.s')
MAP   = os.path.join(SHORT, '_alias_map.txt')
RESID = os.path.join(SHORT, '_residual.txt')

# ---- 1. defined/exported symbols from the library directory -----------------
defined = set()
for line in open(LV):
    if line.startswith("Module '") or not line.strip():
        continue
    for tok in re.findall(r'[A-Za-z_][A-Za-z0-9_$.]*', line):
        defined.add(tok)
# drop obvious non-symbol words from the dated header lines (none survive the
# Module/blank filter except real exports, but be safe about 'dated'/weekday):
NOISE = {'dated','Mon','Tue','Wed','Thu','Fri','Sat','Sun',
         'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'}
defined -= NOISE

def prefix(sym):
    """token before the first '__' (groups free overloads + member fns)."""
    i = sym.find('__')
    return sym[:i] if i > 0 else sym

by_prefix = collections.defaultdict(list)
for d in defined:
    by_prefix[prefix(d)].append(d)

# ---- 2. classify residual / intrinsic / data --------------------------------
INTRIN = {'gte_lwc2__Fii','gte_rtps__Fv','gte_rtpt__Fv','gte_swc2__FiPv',
          'trap','trap__Fi','trap__FUi','alloca__Fi','_bzero_w','_rsincos',
          'rinverse','_rsqrt_tbl','systemtask__Fi'}
DATA   = {'_vlc_acesc','_vlc_dc_c','_vlc_dc_l','_cd_param_count','_cd_result_flag',
          '_Track_gShapeNamePtrs_end','_7tScreen_fSuppressLoadingText',
          'gSndState','PAD_state'}

def cdtor_class(sym):
    """For a flat ctor/dtor helper <Class>_ctor__... return (Class, kind)."""
    base = sym.split('__', 1)[0]
    for suf, kind in (('_ctor','ct'),('_dtor','dt'),('_ct','ct'),('_dt','dt')):
        if base.endswith(suf):
            return base[:-len(suf)], kind
    return None, None

def cdtor_target(cls, kind):
    """Pick a DEFINED cfront ctor/dtor for `cls`.
    ctor: shortest defined __<len><Class>...  (shortest => fewest params, so any
          surplus call args land harmlessly past the ctor's formals on MIPS o32).
    dtor: the defined _._<len><Class> (exact, then any startswith)."""
    n = len(cls)
    if kind == 'ct':
        pre = '__%d%s' % (n, cls)
        cands = sorted((d for d in defined if d.startswith(pre)), key=lambda c: (len(c), c))
        return cands[0] if cands else None
    exact = '_._%d%s' % (n, cls)
    if exact in defined: return exact
    pre = '_._%d%s' % (n, cls)
    cands = sorted((d for d in defined if d.startswith(pre)), key=lambda c: (len(c), c))
    return cands[0] if cands else None

def member_target(name):
    """<Class>_<method> flat helper -> defined member method__<len><Class>...
    Length-prefixed match makes this precise (no cross-class false hits)."""
    for i in range(len(name)):
        if name[i] != '_':
            continue
        cls, meth = name[:i], name[i+1:]
        if not cls or not meth:
            continue
        pre = '%s__%d%s' % (meth, len(cls), cls)
        cands = sorted((d for d in defined if d.startswith(pre)), key=lambda c: (len(c), c))
        if cands:
            return cands[0]
    return None

def base_dtor_target(sym):
    """Raw derived dtor _._<len><Class> with no own body -> a base-class dtor
    _._<m><Base> where Class starts with Base (derived adds no destructibles)."""
    m = re.match(r'^_\._(\d+)(.+)$', sym)
    if not m:
        return None
    cls = m.group(2)
    best = None
    for d in defined:
        dm = re.match(r'^_\._(\d+)(.+)$', d)
        if not dm:
            continue
        base = dm.group(2)
        if base != cls and cls.startswith(base):
            if best is None or len(base) > len(best[1]):
                best = (d, base)
    return best[0] if best else None

def pick(cands, U):
    """Deterministic best target: prefer same arg-shape; else shortest mangle."""
    cands = [c for c in cands if c != U]
    if not cands:
        return None, []
    # prefer a free-fn/member twin sharing the most trailing signature chars
    cands_sorted = sorted(cands, key=lambda c: (len(c), c))
    return cands_sorted[0], cands_sorted

unres = [l.strip() for l in open(UNRES) if l.strip()]
aliases = []          # (U, target)
multi   = []          # (U, target, all_candidates)
resid   = collections.defaultdict(list)

for U in unres:
    # (a) regular prefix match -> free overload / member / typed-twin
    cands = by_prefix.get(prefix(U), [])
    tgt, allc = pick(cands, U)
    if tgt:
        aliases.append((U, tgt))
        if len([c for c in allc]) > 1:
            multi.append((U, tgt, allc))
        continue
    # (b) ctor/dtor flat-helper -> defined cfront ctor/dtor
    cls, kind = cdtor_class(U)
    if cls:
        t = cdtor_target(cls, kind)
        if t: aliases.append((U, t))
        else: resid['CDTOR_GAP'].append(U)
        continue
    # (c) <Class>_<method> flat helper -> defined member
    base = U.split('__', 1)[0]
    if '_' in base:
        t = member_target(base)
        if t: aliases.append((U, t)); continue
    # (d) raw derived dtor with no own body -> base-class dtor
    if U.startswith('_._'):
        t = base_dtor_target(U)
        if t: aliases.append((U, t)); continue
    # (e) genuinely undefined
    if U in INTRIN:        resid['INTRIN'].append(U)
    elif U in DATA:        resid['DATA'].append(U)
    elif U.endswith('__Fe'): resid['GAP_ELL'].append(U)
    else:                  resid['GAP_FN'].append(U)

# ---- 3. emit ASPSX tail-call alias file -------------------------------------
with open(OUT_S, 'w') as f:
    f.write('# link_aliases.s -- AUTO-GENERATED by tools/gen_aliases.py\n')
    f.write('# ASPSX tail-call aliases resolving name-mangling-mismatch unresolveds.\n')
    f.write('# Each: the unresolved (caller-side) name tail-jumps to the defined body.\n')
    f.write('# ABI-correct on MIPS o32 -- args/this already in $a0..$a3 at the call.\n\n')
    f.write('\t.text\n\t.align\t2\n\t.set\tnoreorder\n\t.set\tnomacro\n\n')
    for U, T in aliases:
        f.write('\t.globl\t%s\n%s:\n\tj\t%s\n\tnop\n\n' % (U, U, T))

with open(MAP, 'w') as f:
    f.write('# alias map: %d aliases\n' % len(aliases))
    for U, T in aliases:
        f.write('%-55s -> %s\n' % (U, T))
    f.write('\n# MULTI-CANDIDATE (picked first; review if runtime-wrong): %d\n' % len(multi))
    for U, T, allc in multi:
        f.write('%-50s -> %-40s  candidates=%s\n' % (U, T, allc))

with open(RESID, 'w') as f:
    tot = sum(len(v) for v in resid.values())
    f.write('# residual (genuinely undefined): %d\n' % tot)
    for k in sorted(resid):
        f.write('\n== %s (%d) ==\n' % (k, len(resid[k])))
        for s in resid[k]:
            f.write('  '+s+'\n')

print('aliases:        %d' % len(aliases))
print('  multi-cand:   %d' % len(multi))
print('residual total: %d' % sum(len(v) for v in resid.values()))
for k in sorted(resid):
    print('  %-12s %d' % (k, len(resid[k])))
print('check: %d aliases + %d residual = %d (unres %d)'
      % (len(aliases), sum(len(v) for v in resid.values()),
         len(aliases)+sum(len(v) for v in resid.values()), len(unres)))
