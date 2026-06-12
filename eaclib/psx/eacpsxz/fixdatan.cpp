/* eaclib/psx/eacpsxz/fixdatan.cpp -- RECONSTRUCTED from nfs4-f.exe. NOT original source.
 *   Source obj : nfs4\eaclib\psx\fixdatan.obj (EACPSXZ.LIB).  1 fn @0x800ED528 : fixedatan.
 *   FULL reconstruction (disasm-v3 MIPS); NOT a stub.  atan2(y,x) in a 16-bit angle unit
 *   (full circle = 0x10000, 0x4000 = 90 deg).  Octant-reduces to ratio = min/max, looks up
 *   atan(ratio) in a 257-entry table (@0x80137868, obj-local -> inlined) with 16-bit interpolation
 *   over a 64-bit ratio (the EA make64/divu64 path), then maps the octant back to the full circle.
 *   (The 8-way octant remap is reconstructed via the atan2 identity and cross-checked vs atan2.)
 */

static const int kAtanTbl[257] = {
    0,41,81,122,163,204,244,285,
    326,367,407,448,489,529,570,610,
    651,692,732,773,813,854,894,935,
    975,1015,1056,1096,1136,1177,1217,1257,
    1297,1337,1377,1417,1457,1497,1537,1577,
    1617,1656,1696,1736,1775,1815,1854,1894,
    1933,1973,2012,2051,2090,2129,2168,2207,
    2246,2285,2324,2363,2401,2440,2478,2517,
    2555,2594,2632,2670,2708,2746,2784,2822,
    2860,2897,2935,2973,3010,3047,3085,3122,
    3159,3196,3233,3270,3307,3344,3380,3417,
    3453,3490,3526,3562,3599,3635,3670,3706,
    3742,3778,3813,3849,3884,3920,3955,3990,
    4025,4060,4095,4129,4164,4199,4233,4267,
    4302,4336,4370,4404,4438,4471,4505,4539,
    4572,4605,4639,4672,4705,4738,4771,4803,
    4836,4869,4901,4933,4966,4998,5030,5062,
    5094,5125,5157,5188,5220,5251,5282,5313,
    5344,5375,5406,5437,5467,5498,5528,5559,
    5589,5619,5649,5679,5708,5738,5768,5797,
    5826,5856,5885,5914,5943,5972,6000,6029,
    6058,6086,6114,6142,6171,6199,6227,6254,
    6282,6310,6337,6365,6392,6419,6446,6473,
    6500,6527,6554,6580,6607,6633,6660,6686,
    6712,6738,6764,6790,6815,6841,6867,6892,
    6917,6943,6968,6993,7018,7043,7068,7092,
    7117,7141,7166,7190,7214,7238,7262,7286,
    7310,7334,7358,7381,7405,7428,7451,7475,
    7498,7521,7544,7566,7589,7612,7635,7657,
    7679,7702,7724,7746,7768,7790,7812,7834,
    7856,7877,7899,7920,7942,7963,7984,8005,
    8026,8047,8068,8089,8110,8131,8151,8172,
    8192,
};

extern "C" void make64(int *out, int y, unsigned int shift);   /* @0x800FE488 math64a.obj */
extern "C" int  divu64(int hi, int lo, unsigned int den);      /* @0x800FE4E0 math64a.obj */

extern "C" int fixedatan(int x, int y)   /* @0x800ED528 */
{
    int oct = 0;
    if (y < 0) { y = -y; oct |= 2; }      /* bit1: y negative */
    if (x < 0) { x = -x; oct |= 4; }      /* bit2: x negative */

    int a2;
    if (x == y) {
        a2 = 0x2000;                       /* 45 deg */
    } else {
        unsigned num, den;
        if (y < x) { num = (unsigned)y; den = (unsigned)x; oct |= 1; }  /* bit0: |x| dominant */
        else       { num = (unsigned)x; den = (unsigned)y; }
        int buf[2];                                       /* min/max ratio: EA make64 + divu64       */
        make64(buf, (int)num, 32);                        /* (@0x800FE488/E4E0; NOT libgcc __udivdi3) */
        unsigned r    = (unsigned)divu64(buf[1], buf[0], den);  /* (num<<32)/den as a 0.32 fraction   */
        unsigned idx  = r >> 24;
        unsigned frac = (r >> 8) & 0xFFFF;
        int d = kAtanTbl[idx + 1] - kAtanTbl[idx];
        a2 = kAtanTbl[idx] + (int)(((long long)d * (long long)frac) >> 16);
    }

    switch (oct) {                         /* octant -> full circle (0x4000 == 90 deg) */
    case 0:  return 0x4000 - a2;           /* q1, y dominant */
    case 1:  return a2;                    /* q1, x dominant */
    case 2:  return a2 - 0x4000;           /* q4, y dominant */
    case 3:  return -a2;                   /* q4, x dominant */
    case 4:  return 0x4000 + a2;           /* q2, y dominant */
    case 5:  return 0x8000 - a2;           /* q2, x dominant */
    case 6:  return 0xC000 - a2;           /* q3, y dominant */
    default: return 0x8000 + a2;           /* 7: q3, x dominant */
    }
}
