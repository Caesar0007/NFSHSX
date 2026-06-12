/* syslib/psx/libcard/C171.cpp -- RECONSTRUCTED from nfs4-f.exe (disasm-v3).
 *   obj libcard.lib(C171.OBJ): _card_info -- request the directory/status info for the card on
 *   channel `chan`.  This is a thin tail-call thunk into the PSX BIOS A0 jump table, entry 0xAB
 *   (_card_info / get_card_info).  The PSX form loads the table base into $t2, the call index into
 *   $t1, and jumps (jr, not jal) so the BIOS routine returns straight to our caller with $a0..$a3
 *   passed through untouched.  On the host there is no BIOS, so the #else path is a no-op stub. */

/* @0x80109D10 : _card_info -- BIOS A0:0xAB thunk. */
extern "C" int _card_info(int chan)
{
#if defined(__mips__)
    __asm__ volatile("li $t2,0xA0\n\t"
                     "jr $t2\n\t"
                     "li $t1,0xAB\n\t");
    return 0;                       /* tail-call: control never returns here */
#else
    (void)chan;
    return 0;                       /* BIOS unavailable on host */
#endif
}
