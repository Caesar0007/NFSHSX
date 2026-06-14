/* link_runtime.cpp -- hand-written defs for genuinely-undefined runtime intrinsics +
 * data globals (PSX LINK phase, first-light residual). ccpsx supports gcc inline asm
 * with cop2 regs (cf. syslib/psx/libgte/MSC02.cpp). cfront needs spaced colons (: :). */

/* GTE ops are declared in drawc_externs.h WITHOUT extern "C" => C++ linkage
 * (gte_rtps__Fv / gte_lwc2__Fii / gte_swc2__FiPv). Define them as C++ to match. */
void gte_rtps(void){ __asm__ __volatile__(".word 0x4a180001"); }   /* RTPS */
void gte_rtpt(void){ __asm__ __volatile__(".word 0x4a280030"); }   /* RTPT */
void gte_lwc2(int reg, int data){   /* data -> GTE data register reg (mtc2) */
    switch (reg) {
    case 0: __asm__ __volatile__("mtc2 %0,$0" : : "r"(data)); break;
    case 1: __asm__ __volatile__("mtc2 %0,$1" : : "r"(data)); break;
    case 2: __asm__ __volatile__("mtc2 %0,$2" : : "r"(data)); break;
    case 3: __asm__ __volatile__("mtc2 %0,$3" : : "r"(data)); break;
    case 4: __asm__ __volatile__("mtc2 %0,$4" : : "r"(data)); break;
    case 5: __asm__ __volatile__("mtc2 %0,$5" : : "r"(data)); break;
    case 6: __asm__ __volatile__("mtc2 %0,$6" : : "r"(data)); break;
    case 7: __asm__ __volatile__("mtc2 %0,$7" : : "r"(data)); break;
    case 8: __asm__ __volatile__("mtc2 %0,$8" : : "r"(data)); break;
    case 9: __asm__ __volatile__("mtc2 %0,$9" : : "r"(data)); break;
    case 10: __asm__ __volatile__("mtc2 %0,$10" : : "r"(data)); break;
    case 11: __asm__ __volatile__("mtc2 %0,$11" : : "r"(data)); break;
    case 12: __asm__ __volatile__("mtc2 %0,$12" : : "r"(data)); break;
    case 13: __asm__ __volatile__("mtc2 %0,$13" : : "r"(data)); break;
    case 14: __asm__ __volatile__("mtc2 %0,$14" : : "r"(data)); break;
    case 15: __asm__ __volatile__("mtc2 %0,$15" : : "r"(data)); break;
    case 16: __asm__ __volatile__("mtc2 %0,$16" : : "r"(data)); break;
    case 17: __asm__ __volatile__("mtc2 %0,$17" : : "r"(data)); break;
    case 18: __asm__ __volatile__("mtc2 %0,$18" : : "r"(data)); break;
    case 19: __asm__ __volatile__("mtc2 %0,$19" : : "r"(data)); break;
    case 20: __asm__ __volatile__("mtc2 %0,$20" : : "r"(data)); break;
    case 21: __asm__ __volatile__("mtc2 %0,$21" : : "r"(data)); break;
    case 22: __asm__ __volatile__("mtc2 %0,$22" : : "r"(data)); break;
    case 23: __asm__ __volatile__("mtc2 %0,$23" : : "r"(data)); break;
    case 24: __asm__ __volatile__("mtc2 %0,$24" : : "r"(data)); break;
    case 25: __asm__ __volatile__("mtc2 %0,$25" : : "r"(data)); break;
    case 26: __asm__ __volatile__("mtc2 %0,$26" : : "r"(data)); break;
    case 27: __asm__ __volatile__("mtc2 %0,$27" : : "r"(data)); break;
    case 28: __asm__ __volatile__("mtc2 %0,$28" : : "r"(data)); break;
    case 29: __asm__ __volatile__("mtc2 %0,$29" : : "r"(data)); break;
    case 30: __asm__ __volatile__("mtc2 %0,$30" : : "r"(data)); break;
    case 31: __asm__ __volatile__("mtc2 %0,$31" : : "r"(data)); break;
    default: break;
    }
}
void gte_swc2(int reg, void *ptr){  /* GTE data register reg -> *ptr (swc2) */
    switch (reg) {
    case 0: __asm__ __volatile__("swc2 $0,0(%0)" : : "r"(ptr) : "memory"); break;
    case 1: __asm__ __volatile__("swc2 $1,0(%0)" : : "r"(ptr) : "memory"); break;
    case 2: __asm__ __volatile__("swc2 $2,0(%0)" : : "r"(ptr) : "memory"); break;
    case 3: __asm__ __volatile__("swc2 $3,0(%0)" : : "r"(ptr) : "memory"); break;
    case 4: __asm__ __volatile__("swc2 $4,0(%0)" : : "r"(ptr) : "memory"); break;
    case 5: __asm__ __volatile__("swc2 $5,0(%0)" : : "r"(ptr) : "memory"); break;
    case 6: __asm__ __volatile__("swc2 $6,0(%0)" : : "r"(ptr) : "memory"); break;
    case 7: __asm__ __volatile__("swc2 $7,0(%0)" : : "r"(ptr) : "memory"); break;
    case 8: __asm__ __volatile__("swc2 $8,0(%0)" : : "r"(ptr) : "memory"); break;
    case 9: __asm__ __volatile__("swc2 $9,0(%0)" : : "r"(ptr) : "memory"); break;
    case 10: __asm__ __volatile__("swc2 $10,0(%0)" : : "r"(ptr) : "memory"); break;
    case 11: __asm__ __volatile__("swc2 $11,0(%0)" : : "r"(ptr) : "memory"); break;
    case 12: __asm__ __volatile__("swc2 $12,0(%0)" : : "r"(ptr) : "memory"); break;
    case 13: __asm__ __volatile__("swc2 $13,0(%0)" : : "r"(ptr) : "memory"); break;
    case 14: __asm__ __volatile__("swc2 $14,0(%0)" : : "r"(ptr) : "memory"); break;
    case 15: __asm__ __volatile__("swc2 $15,0(%0)" : : "r"(ptr) : "memory"); break;
    case 16: __asm__ __volatile__("swc2 $16,0(%0)" : : "r"(ptr) : "memory"); break;
    case 17: __asm__ __volatile__("swc2 $17,0(%0)" : : "r"(ptr) : "memory"); break;
    case 18: __asm__ __volatile__("swc2 $18,0(%0)" : : "r"(ptr) : "memory"); break;
    case 19: __asm__ __volatile__("swc2 $19,0(%0)" : : "r"(ptr) : "memory"); break;
    case 20: __asm__ __volatile__("swc2 $20,0(%0)" : : "r"(ptr) : "memory"); break;
    case 21: __asm__ __volatile__("swc2 $21,0(%0)" : : "r"(ptr) : "memory"); break;
    case 22: __asm__ __volatile__("swc2 $22,0(%0)" : : "r"(ptr) : "memory"); break;
    case 23: __asm__ __volatile__("swc2 $23,0(%0)" : : "r"(ptr) : "memory"); break;
    case 24: __asm__ __volatile__("swc2 $24,0(%0)" : : "r"(ptr) : "memory"); break;
    case 25: __asm__ __volatile__("swc2 $25,0(%0)" : : "r"(ptr) : "memory"); break;
    case 26: __asm__ __volatile__("swc2 $26,0(%0)" : : "r"(ptr) : "memory"); break;
    case 27: __asm__ __volatile__("swc2 $27,0(%0)" : : "r"(ptr) : "memory"); break;
    case 28: __asm__ __volatile__("swc2 $28,0(%0)" : : "r"(ptr) : "memory"); break;
    case 29: __asm__ __volatile__("swc2 $29,0(%0)" : : "r"(ptr) : "memory"); break;
    case 30: __asm__ __volatile__("swc2 $30,0(%0)" : : "r"(ptr) : "memory"); break;
    case 31: __asm__ __volatile__("swc2 $31,0(%0)" : : "r"(ptr) : "memory"); break;
    default: break;
    }
}

extern "C" {
void _bzero_w(int *p, int n){ while (n-- > 0) *p++ = 0; }  /* static-in-INTR.cpp; cross-TU refs */
unsigned fixedinverse(int x);
unsigned rinverse(int x){ return fixedinverse(x); }   /* alias attr ignored; forward */
void trap(unsigned int code){ (void)code; }   /* EA panic/div-trap; return (do not brick boot) */
/* PAD_state: NOT a gap -- real PAD_state__Fi exists; link_aliases.s tail-calls it. */
short _rsqrt_tbl[256];   /* GTE inverse-sqrt table (BSS, filled at GTE init; idx<0xC0) */
} /* extern "C" */

/* tScreen::fSuppressLoadingText single global (was per-TU `static int` in a header). */
int _7tScreen_fSuppressLoadingText;
