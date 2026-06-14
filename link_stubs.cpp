/* link_stubs.cpp -- hand-written definitions for genuine-gap symbols (PSX LINK phase).
 * Separate from the auto-generated link_trampolines.cpp so the generator never overwrites these.
 *
 * Critical-section helpers: empty no-ops in the original single-threaded PSX build. The eaclib
 * sources define them as `static inline void XXX_enterCS(void) {}` (file-local), so cross-TU
 * callers that reference them externally are unresolved. Provide the exported (no-op) definitions.
 * Linkage matches the unresolved-symbol names: ASYNC/FILE/STREAM are extern "C"; FROOT is C++ (__Fv).
 */
extern "C" void ASYNC_enterCS(void)  {}
extern "C" void ASYNC_leaveCS(void)  {}
extern "C" void FILE_enterCS(void)   {}
extern "C" void FILE_leaveCS(void)   {}
extern "C" void STREAM_enterCS(void) {}
extern "C" void STREAM_leaveCS(void) {}
void FROOT_enterCS(void) {}   /* C++ linkage -> FROOT_enterCS__Fv */
void FROOT_leaveCS(void) {}   /* C++ linkage -> FROOT_leaveCS__Fv */
