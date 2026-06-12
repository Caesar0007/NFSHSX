/* syslib/psx/libcard/A80.cpp -- RECONSTRUCTED from nfs4-f.exe (disasm-v3).
 *   obj libcard.lib(A80.OBJ): _new_card -- tell the BIOS to accept a freshly-inserted card on the
 *   next access (clears the "card changed" latch).  Thin tail-call thunk into the PSX BIOS B0 jump
 *   table, entry 0x50 (allow_new_card).  See C171.cpp for the thunk convention. */

/* @0x8010A090 : _new_card -- BIOS B0:0x50 thunk. */
extern "C" void _new_card(void)
{
#if defined(__mips__)
    __asm__ volatile("li $t2,0xB0\n\t"
                     "jr $t2\n\t"
                     "li $t1,0x50\n\t");
#endif
    /* host: no BIOS, nothing to do */
}
