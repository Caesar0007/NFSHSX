/* syslib/psx/libapi/L10.cpp -- RECONSTRUCTED from nfs4-f.exe (disasm-v3).
 *   obj L10.obj ; libapi.lib.  ChangeClearRCnt -- PSX kernel API trampoline (BIOS 0xC0:0xA).  MIPS-target
 *   asm (jumps to BIOS); x86 fallback stub (real impl in PSX BIOS / OpenBIOS).
 */
#if defined(__mips__)
extern "C" __attribute__((naked)) int ChangeClearRCnt(int t, int m)
{ __asm__ __volatile__(".set noreorder
	 li $t2,0xC0
	 jr $t2
	 li $t1,0xA
	 .set reorder"); }
#else
extern "C" int ChangeClearRCnt(int t, int m)
{
    return 0;
}
#endif
