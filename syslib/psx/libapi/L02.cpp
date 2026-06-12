/* syslib/psx/libapi/L02.cpp -- RECONSTRUCTED from nfs4-f.exe (disasm-v3).
 *   obj L02.obj ; libapi.lib.  SysEnqIntRP -- PSX kernel API trampoline (BIOS 0xC0:0x2).  MIPS-target
 *   asm (jumps to BIOS); x86 fallback stub (real impl in PSX BIOS / OpenBIOS).
 */
#if defined(__mips__)
extern "C" __attribute__((naked)) void *SysEnqIntRP(int pri, long *rp)
{ __asm__ __volatile__(".set noreorder
	 li $t2,0xC0
	 jr $t2
	 li $t1,0x2
	 .set reorder"); }
#else
extern "C" void *SysEnqIntRP(int pri, long *rp)
{
    return 0;
}
#endif
