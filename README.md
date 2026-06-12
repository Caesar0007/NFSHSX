# NFSHSX — Need for Speed: High Stakes (NFS4, PSX) → recompilable C++

A source-level reconstruction of the PlayStation build of *Need for Speed: High Stakes*
(NFS4, SLUS‑006.20) — translating the original linked `.obj` modules back into faithful,
**self-contained, recompilable C++**.

The original game executable is **not** included (it is copyrighted EA material and is used
only as a debug oracle). This repository contains only reconstructed source.

## Status

Reconstruction of executable code is **complete** — every function whose code exists in the
game binary has been reconstructed and links. Verified by a whole‑tree link harness:

```
838 → 196 unresolved symbols
196 = 99 method-hygiene + 89 cdtor-hygiene + 8 inline/host non-gaps + 0 genuine missing-code gaps
```

The remaining **188 are linkage-hygiene** (function bodies exist as C++ members; some call
sites still reference the flat cfront‑style `extern "C"` names) — being resolved with thin
`extern "C"` trampolines. The **8 inline/host** symbols (`alloca`, GTE `cop2` intrinsics,
`trap`/`break`, `operator delete`, x86 `__chkstk_ms`) are compiler/inline constructs, correct
as-is and never external in a real PsyQ build.

## Layout

```
eaclib/    EA cross-platform + PSX library (math, sound, spch, fixed-point, matrix)
frontend/  Front-end menus / screens (common + PSX)
game/      Gameplay: AI, physics, cars, audio, HUD, track, replay (common + PSX)
syslib/    PsyQ system libraries (libgpu, libgte, libcd, libspu, libpad, ...)
lib/       Shared cross-module declarations (libfns.h, ...)
nfs4_types.h    Reconstructed type system (~500 structs, ABI-exact for mipsel -m32)
link_*.cpp / materialized_data.cpp   Materialized absolute-VA data + globals
tools/     Verification harness (whole-tree compile + nm/c++filt symbol balance)
```

## Methodology

Each `.obj` was reconstructed from a triple-source authority:

- **disasm-v3** — trusted MIPS disassembly (authoritative for code, args, returns).
- **PsyQ SYM (v3)** — symbol/field/local names (PsyQ MND dump).
- **Ghidra C/C++ export** — structural decompilation (cross-checked against disasm; Ghidra
  is known to drop args under "unknown calling convention" and occasionally emit wrong
  constants, so every call's arguments are verified against the disassembly).

Goal / seal criteria: the tree compiles fresh from itself alone (host `g++ -m32 -std=gnu++98`),
0 unresolved absolute VAs in code, every materialized item carries a `/* @0xVA */` breadcrumb.

## Verifying self-containment

```
python tools/link_harness.py    # compile every TU to a host -m32 object
python tools/link_analyze.py    # nm + c++filt symbol balance -> _link_analysis.json
```

(The harness paths in `tools/` may need adjusting to your checkout location.)

## Credits

Reconstruction is decompilation-to-source; this is **not** original EA source.
Thanks to Ben Lincoln for the *"This Dust Remembers What It Once Was"* tooling that the
original decomp effort was built on.
