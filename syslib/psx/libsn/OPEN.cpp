/* syslib/psx/libsn/OPEN.cpp -- RECONSTRUCTED (disasm-v3). obj OPEN.obj ; libsn.lib.
 * PCopen @0x80106CA4 -- host open via `break 0x103`; returns handle (v1) on success, -1 on error. */
#if defined(__mips__)
extern "C" __attribute__((naked)) int PCopen(const char *name, int mode)
{ __asm__ __volatile__(".set noreorder\n\t move $a2,$a1\n\t move $a1,$a0\n\t break 0x103\n\t"
                       "beqz $v0,1f\n\t move $v0,$v1\n\t li $v0,-1\n\t 1: jr $ra\n\t nop\n\t .set reorder"); }
#else
extern "C" int PCopen(const char *name, int mode) { (void)name; (void)mode; return -1; }
#endif
