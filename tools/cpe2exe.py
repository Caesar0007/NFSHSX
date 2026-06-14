#!/usr/bin/env python3
"""cpe2exe.py -- convert a ccpsx CPE into a PS-X EXE (the runnable artifact for
PCSX-Redux / no$psx / real hardware loaders).

Replaces the unusable converters: NFS1's C:\\Temp\\nfs1-clean\\cpe2psx.exe segfaults
on this CPE, and PsyQ cpe2x.exe is a DOS binary (needs DOSBox).

IMPORTANT: link the CPE with `ccpsx -Xo0x80010000 ...` so load addresses are in
PSX RAM (the default base is 0x0 -> won't run; see tools/dlink.py).

CPE chunk format (SN Systems):
  "CPE\\x01" then chunks:
    0x00 end
    0x01 load   : u32 addr, u32 len, data[len]
    0x03 setreg : u16 reg, u32 val            (reg 0x90=PC, 0x91=GP)
    0x08 setreg : u16 _, u16 reg, u32 val     (9-byte; ccpsx emits PC here)

Usage: python tools/cpe2exe.py <in.cpe> [out.exe]   (default out = in stem + .exe)
"""
import sys, struct, os

def cpe2exe(cpe_path, exe_path):
    d = open(cpe_path, 'rb').read()
    if d[:4] != b'CPE\x01':
        raise SystemExit('not a CPE: %s' % cpe_path)
    i = 4; loads = []; pc = 0; gp = 0
    while i < len(d):
        t = d[i]; i += 1
        if   t == 0x00: break
        elif t == 0x01:
            addr, ln = struct.unpack('<II', d[i:i+8]); i += 8
            loads.append((addr, d[i:i+ln])); i += ln
        elif t == 0x08:
            _, reg, val = struct.unpack('<HHI', d[i:i+8]); i += 8
            if reg == 0x90: pc = val
            elif reg == 0x91: gp = val
        elif t == 0x03:
            reg, val = struct.unpack('<HI', d[i:i+6]); i += 6
            if reg == 0x90: pc = val
            elif reg == 0x91: gp = val
        else:
            raise SystemExit('unknown CPE tag 0x%02x @%d' % (t, i-1))
    if not loads:
        raise SystemExit('no load chunks')
    lo = min(a for a, _ in loads); hi = max(a + len(b) for a, b in loads)
    text_addr = lo & ~0x7ff
    text_size = ((hi + 0x7ff) & ~0x7ff) - text_addr
    img = bytearray(text_size)
    for a, b in loads:
        img[a-text_addr:a-text_addr+len(b)] = b
    hdr = bytearray(0x800)
    hdr[0:8] = b'PS-X EXE'
    struct.pack_into('<I', hdr, 0x10, pc)
    struct.pack_into('<I', hdr, 0x14, gp)
    struct.pack_into('<I', hdr, 0x18, text_addr)
    struct.pack_into('<I', hdr, 0x1c, text_size)
    struct.pack_into('<I', hdr, 0x30, 0x801FFF00)   # stack base
    hdr[0x4c:0x4c+54] = b'Sony Computer Entertainment Inc. for North America area'
    open(exe_path, 'wb').write(bytes(hdr) + bytes(img))
    print('wrote %s  pc=%08x text=%08x size=%d (%d loads, %d KB image)'
          % (exe_path, pc, text_addr, text_size, len(loads), text_size//1024))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('usage: cpe2exe.py <in.cpe> [out.exe]')
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(inp)[0] + '.exe'
    cpe2exe(inp, out)
