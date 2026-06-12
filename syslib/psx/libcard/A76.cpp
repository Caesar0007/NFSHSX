/* syslib/psx/libcard/A76.cpp -- RECONSTRUCTED from nfs4-f.exe (disasm-v3).
 *   obj libcard.lib(A76.OBJ): StopCARD2 -- BIOS B0:0x4C (StopCard) tail-call thunk. */

/* @0x8010CBB0 : StopCARD2 -- BIOS B0:0x4C thunk. */
extern "C" void StopCARD2(void)
{
#if defined(__mips__)
    __asm__ volatile("li $t2,0xB0\n\t jr $t2\n\t li $t1,0x4C\n\t");
#endif
}
