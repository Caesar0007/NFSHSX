/* syslib/psx/libcard/A74.cpp -- RECONSTRUCTED from nfs4-f.exe (disasm-v3).
 *   obj libcard.lib(A74.OBJ): InitCARD2 -- BIOS B0:0x4A (InitCard) tail-call thunk. See C171.cpp. */

/* @0x8010C9C0 : InitCARD2(val) -- BIOS B0:0x4A thunk. */
extern "C" void InitCARD2(int val)
{
#if defined(__mips__)
    __asm__ volatile("li $t2,0xB0\n\t jr $t2\n\t li $t1,0x4A\n\t");
#else
    (void)val;                          /* BIOS unavailable on host */
#endif
}
