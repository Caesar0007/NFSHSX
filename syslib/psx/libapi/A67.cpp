/* syslib/psx/libapi/A67.cpp -- RECONSTRUCTED from nfs4-f.exe (disasm-v3).
 *   obj A67.obj ; libapi.lib.  nextfile -- PSX kernel API trampoline (BIOS 0xB0:0x43).  Faithful MIPS-target asm
 *   (jumps to the BIOS / issues the syscall); x86 fallback is a stub (real impl lives in the PSX BIOS).
 */
#if defined(__mips__)
extern "C" __attribute__((naked)) void *nextfile(void *dir)
{ __asm__ __volatile__(".set noreorder
	 li $t2,0xB0
	 jr $t2
	 li $t1,0x43
	 .set reorder"); }
#else
extern "C" void *nextfile(void *dir)
{
}
#endif
