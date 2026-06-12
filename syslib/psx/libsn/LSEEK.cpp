/* syslib/psx/libsn/LSEEK.cpp -- RECONSTRUCTED (disasm-v3). obj LSEEK.obj ; libsn.lib.
 * PClseek @0x80106D1C -- host lseek via `break 0x107`; returns offset (v1) on success, -1 on error. */
#if defined(__mips__)
extern "C" __attribute__((naked)) int PClseek(int fd, int offset, int mode)
{ __asm__ __volatile__(".set noreorder\n\t move $a3,$a2\n\t move $a2,$a1\n\t move $a1,$a0\n\t break 0x107\n\t"
                       "beqz $v0,1f\n\t move $v0,$v1\n\t li $v0,-1\n\t 1: jr $ra\n\t nop\n\t .set reorder"); }
#else
extern "C" int PClseek(int fd, int offset, int mode) { (void)fd;(void)offset;(void)mode; return -1; }
#endif
