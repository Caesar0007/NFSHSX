/* link_ida.cpp -- AGGREGATION TU. Module-owned globals resolved via IDA
 * (NFS4-v3-work.i64 / nfs4-f.exe.i64) that were extern-declared but never
 * defined. Zero image -> zero-init typed; nonzero primitive -> byte-exact. */
#include "nfs4_types.h"

extern "C" {

CarIO_textureInfo CarIO_textureName[51]; /* FIXME nonzero 612B - byte-exact pending */ /* @8011e804 612B */
int Cdinfo;                                                                      /* @80146cc4 2844B */
Input_tDeviceList Device_gDeviceList[5]; /* FIXME nonzero 60B - byte-exact pending */ /* @8011ec18 60B */
PAD_COMMON Padglobal[2];                                                         /* @8013e8f0 16B */
int Weather_gLastProcessTime[2];                                                 /* @8013de54 12B */
unsigned int _stacksize = 0x8000;                                                /* @80136cd0 4B */
int asyncfilehandle;                                                             /* @8013deb0 48B */
int debounce[2];                                                                 /* @80052b60 8B */
AnimDef            * gAnimDefs; /* FIXME nonzero 280B - byte-exact pending */    /* @80115c48 280B */
u_long hilight_colors[5] = {0x700a00,0x400a00,0x300300,0x180300,0x180300};       /* @8011f4b4 20B */
int hoff[6] = {0x4d,0x1,0x0,0x0,0x0,0x0};                                        /* @8013dac0 24B */
sim_queue inputQueue;                                                            /* @8013e0f4 524B */
char          * loading_languageNames[6]; /* FIXME nonzero 24B - byte-exact pending */ /* @80120d00 24B */
long nextTick;                                                                   /* @80051738 4B */
Input_tResults output[2];                                                        /* @8013ddc8 28B */
int systemtasksubs;                                                              /* @8013e980 256B */

}
