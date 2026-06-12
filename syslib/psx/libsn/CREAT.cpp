/* syslib/psx/libsn/CREAT.cpp -- RECONSTRUCTED (disasm-v3). obj CREAT.obj ; libsn.lib.
 * PCcreat @0x80106CD0 -- host creat via `break 0x102` (a1=name, a2=0); handle (v1) on success else -1. */
#if defined(__mips__)
extern "C" __attribute__((naked)) int PCcreat(const char *name, int mode)
{ __asm__ __volatile__(".set noreorder\n\t move $a1,$a0\n\t move $a2,$zero\n\t break 0x102\n\t"
                       "beqz $v0,1f\n\t move $v0,$v1\n\t li $v0,-1\n\t 1: jr $ra\n\t nop\n\t .set reorder"); }
#else
extern "C" int PCcreat(const char *name, int mode) { (void)name; (void)mode; return -1; }
#endif
