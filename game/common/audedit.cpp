/* game/common/audedit.cpp -- RECONSTRUCTED from Ghidra 12.0.4 decompile + PsyQ SYM v3.
 *   bworld.obj (GAME\COMMON\bworld.cpp) = 20 fns: BWorld road geometry build/render
 *   (chunk visibility, build lists, spike belt, glare effects, render contexts). Self-contained.
 *   Verified vs disasm-v2.txt. NOT original source; SYM-faithful, recompilable C++.
 */
#include "../../nfs4_types.h"
#include "audedit_externs.h"


/* ---- audedit.obj-owned globals (SYM-typed; .data=real EXE bytes, .bss=zero) ---- */
CAudioList   *gGameAudioList;   /* @0x8013c730  (bss(zero)) */


/* ---- intra-TU forward declarations ---- */
void AudList_PurgeAudio(void);
void AudList_LoadAudioFile(int AudioFileIndex);


/* ---- AudList_PurgeAudio__Fv  [@0x8007b52c] ---- */
void AudList_PurgeAudio(void)
{
  if (gGameAudioList != (CAudioList *)0x0) {
    purgememadr(gGameAudioList);
  }
  return;
}

/* ---- AudList_LoadAudioFile__Fi  [@0x8007b554] ---- */
void AudList_LoadAudioFile(int AudioFileIndex)
{
  char fname [128];
  
  Track_MakeTrackPathName("");
  sprintf(fname,"%s%02d.aud");
  gGameAudioList = (CAudioList *)loadfileadrz(fname,(void *)0x0);
  return;
}
