/* syslib/psx/libsn/SNREAD.cpp -- RECONSTRUCTED (disasm-v3). obj SNREAD.obj ; libsn.lib.
 * _SN_read @0x8010C708 -- low-level host read via `break 0x105` (args already in $a0..$a3 from PCread). */
#if defined(__mips__)
extern "C" __attribute__((naked)) int _SN_read(int chan, int fd, int len, int buff)
{ __asm__ __volatile__(".set noreorder\n\t break 0x105\n\t jr $ra\n\t nop\n\t .set reorder"); }
#else
extern "C" int _SN_read(int chan, int fd, int len, int buff) { (void)chan;(void)fd;(void)len;(void)buff; return -1; }
#endif
