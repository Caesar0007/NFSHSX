/* syslib/psx/libcard/END.cpp -- RECONSTRUCTED from nfs4-f.exe (disasm-v3).
 *   obj libcard.lib(END.OBJ): _ExitCard -- exit handler: restore the BIOS B0[0x56] table-6 handler
 *   that _patch_card overwrote (zero it back), then flush the cache.  Kernel-only -> __mips__-guarded. */

extern "C" int  EnterCriticalSection(void); /* @0x8010698C */
extern "C" void ExitCriticalSection(void);  /* @0x8010696C */
extern "C" void FlushCache(void);           /* BIOS A0:0x44 @0x800F43D4 */

#if defined(__mips__)
static int *_bios_b0_table(int idx)
{
    int *t;
    __asm__ volatile("move $t1,%1\n\t li $t2,0xB0\n\t jalr $t2\n\t nop\n\t move %0,$v0"
                     : "=r"(t) : "r"(idx) : "$t1", "$t2", "$ra", "$v0", "memory");
    return t;
}
#endif

/* @0x8010CBC0 : _ExitCard -- un-patch the card handler and flush. */
extern "C" int _ExitCard(void)
{
    EnterCriticalSection();
#if defined(__mips__)
    {
        int *tbl = _bios_b0_table(0x56);
        int *evt = (int *)tbl[6];                /* *(24+tbl) */
        int  i;
        for (i = 0; i < 3; i++)                  /* restore the 3 overlaid words to 0 */
            ((unsigned int *)((char *)evt + 112))[i] = 0;
    }
#endif
    FlushCache();
    ExitCriticalSection();
    return 0;
}
