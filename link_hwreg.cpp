/* link_hwreg.cpp -- AGGREGATION TU. PSX hardware-register names referenced as
 * `extern volatile` VARIABLES by the eaclib/sound TUs (vs `#define` MMIO macros in
 * libcd/libspu). Types confirmed via NFS4-clean.c Ghidra export (word=u16, dword=u32)
 * + tree extern decls. Defined here as typed globals so the tree links self-contained.
 * NOTE: faithful PSX build should map these to MMIO 0x1F801xxx (SPU/CD/DMA) -- follow-up. */
extern "C" {
volatile short         CD_VOL_L;
volatile short         CD_VOL_R;
volatile unsigned int  D4_BCR;
volatile unsigned int  D4_CHCR;
volatile unsigned int  D4_MADR;
volatile unsigned int  DPCR;
volatile short         EXT_VOL_L;
volatile short         EXT_VOL_R;
volatile short         SOUND_RAM_DATA_TRANSTER_CTRL;
volatile unsigned short SPUSTAT;
volatile unsigned int  SPU_ADDR;
volatile unsigned int  SPU_DELAY;
volatile short         SPU_MAIN_VOL_L;
volatile short         SPU_MAIN_VOL_R;
volatile unsigned int  SPU_VOICE_CHN_FM_MODE;
volatile unsigned int  SPU_VOICE_CHN_NOISE_MODE;
}
