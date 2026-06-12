/* bigbuf.cpp -- RECONSTRUCTED (src nfs4\bigbuf.obj, tree root -- a link/overlay-control TU).
 *
 *   bigBuf @0x80010000 is the FE (front-end) OVERLAY LOAD BUFFER. The entire front-end overlay
 *   -- front.rdata (0x80010000-0x800128EF) + front.text (..0x8005125F) + front.data (..0x80052B37)
 *   + front.bss (..0x80054547), ~0x44548 bytes total -- is DMA'd from CD into this single fixed
 *   buffer (classic PSX overlay mechanism). FE code/data is addressed as bigBuf+offset; 6 modules
 *   (feapp, feaudio, fecars, minfront, nfs3, fe3dmenu) reference it as `extern char bigBuf[]`.
 *   bigbuf.obj's SYM FILE-block is empty (no TUSummary) -- bigBuf is a linker-placed buffer symbol.
 *
 *   CONTENT = the CD file "front.bin" (the compiled FE-overlay image). nfs3.cpp's
 *   LoadFrontendOverlay() does:  asyncloadfileat("front.bin", bigBuf);  -- i.e. front.bin (these
 *   exact front.rdata+text+data+bss bytes) is DMA'd from disc into bigBuf at runtime. So at the
 *   source level bigBuf is just the destination buffer; its loaded contents are the FE modules.
 *
 *   Defined here once so the 6 externs resolve at whole-tree link. SIZE = 0x44548 -- CONFIRMED
 *   EXACT (not an estimate) by address.obj: FrontEndAddress(0x80054548) - FrontStartAddress
 *   (0x80010000) = 0x44548 = sizeof bigBuf. Sub-overlays DMA into this shared buffer. Zero-init
 *   (.bss). @0x80010000 breadcrumb.
 */
#include "nfs4_types.h"
char bigBuf[0x44548];   /* @0x80010000  FE-overlay load buffer (0x44548 B; size pinned by address.obj) */
/* end of bigbuf.cpp */
