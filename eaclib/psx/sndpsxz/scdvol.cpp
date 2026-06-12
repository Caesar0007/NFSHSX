/* eaclib/psx/sndpsxz/scdvol.cpp -- RECONSTRUCTED from nfs4-f.exe. NOT original source.  *** 1/1 ***
 *   Source obj : nfs4\eaclib\psx\scdvol.obj ; archive C:\nfs4\EACLIB\PSX\SNDPSXZ.LIB (xlsx col12 / SYM v3)
 *   1 fn @0x800FAA44.  SNDcdvol -- public CD-audio volume/pan setter; caches the master-scaled level and
 *   forwards (pan,vol) to the platform layer.  Ghidra nfs4-f.exe.c (scdvol) + IDA sig.
 *   Ghidra-ism: IDA typed 1 arg, but vol_l/vol_r are both passed on to iSNDplatformcdpanvol (kept 2).
 */
extern "C" int  sndgs[];        /* (signed char)sndgs[0xf] byte1 (@+0x3d) = master volume */
extern "C" short DAT_80136cae;  /* @0x80136CAE : master-scaled CD level cache */
extern "C" void iSNDplatformcdpanvol(int pan, int vol);   /* sdcdvol */

extern "C" void SNDcdvol(int vol_l, int vol_r);   /* @0x800FAA44 */

/* SNDcdvol @0x800FAA44 : cache (vol_l * masterVol)/0x7f and apply the CD pan/volume. */
extern "C" void SNDcdvol(int vol_l, int vol_r)
{
    DAT_80136cae = (short)((vol_l * (int)*((signed char *)sndgs + 0x3d)) / 0x7f);
    iSNDplatformcdpanvol(vol_l, vol_r);
}
