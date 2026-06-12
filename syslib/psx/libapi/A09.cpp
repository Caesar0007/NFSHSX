/* syslib/psx/libapi/A09.cpp -- RECONSTRUCTED from nfs4-f.exe (disasm-v3).
 *   obj A09.obj ; libapi.lib.  CloseEvent -- PSX kernel API trampoline (BIOS 0xB0:0x9).  Faithful MIPS-target asm
 *   (jumps to the BIOS / issues the syscall); x86 fallback is a stub (real impl lives in the PSX BIOS).
 */
#if defined(__mips__)
extern "C" __attribute__((naked)) long CloseEvent(long event)
{ __asm__ __volatile__(".set noreorder
	 li $t2,0xB0
	 jr $t2
	 li $t1,0x9
	 .set reorder"); }
#else
extern "C" long CloseEvent(long event)
{
    return 0;
}
#endif
