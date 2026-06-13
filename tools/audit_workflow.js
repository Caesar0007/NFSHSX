export const meta = {
  name: 'audit-disasm-v3',
  description: 'Per-function audit: reconstructed NFS4-F C++ vs disasm-v3 oracle (read-only; emits findings for human review, fixes NOTHING)',
  phases: [
    { title: 'Audit',  detail: 'one agent per file-bin: cross-check every function/data-object vs the disasm-v3 oracle' },
    { title: 'Verify', detail: 'adversarially re-check each HIGH finding against the oracle to kill false positives' },
  ],
}

const TREE   = 'C:/Temp/claud/reconstructed_headers/tree'
const ORACLE = 'C:/Temp/symdump-disasm/disasm-v3.txt'

const BINS = [["game/common/vtables_tmenu.cpp"],["game/common/collide.cpp"],["game/common/vtables_tscreen.cpp"],["game/common/speech.cpp"],["game/psx/hud.cpp","game/common/aih_opp.cpp"],["game/common/audiocmn.cpp","syslib/psx/libcd/iso9660.cpp"],["materialized_data.cpp","frontend/common/femenuextended.cpp","syslib/psx/libsn/CLOSE.cpp"],["game/common/cars.cpp","game/common/aih_play.cpp"],["game/psx/drawc.cpp","game/common/vtables_tlist.cpp"],["game/common/vtables_tpausemenu.cpp","game/common/bworldSm.cpp"],["syslib/psx/libgpu/SYS.cpp","eaclib/psx/eacpsxz/nfile.cpp","syslib/psx/libsn/SNMAIN.cpp"],["game/common/r3dcar.cpp","game/common/aispeeds.cpp"],["game/common/camera.cpp","game/psx/flare.cpp","eaclib/psx/eacpsxz/shptype.cpp"],["game/psx/draww.cpp","eaclib/psx/eacpsxz/stream.cpp","frontend/psx/mdec.cpp"],["game/common/aistate.cpp","game/common/newton.cpp","frontend/psx/vsprintf.cpp"],["game/common/vtables_tdialog.cpp","frontend/common/femenuoptions.cpp"],["frontend/common/femenudefs.cpp","syslib/psx/libmcrd/LIBMCRD.cpp","game/common/smack.cpp"],["frontend/common/front.cpp","game/common/ai.cpp","eaclib/psx/sndpsxz/splay.cpp"],["game/common/aiphysic.cpp","game/common/vtables_tscreen2.cpp","game/common/aidelaycar.cpp"],["game/common/aih_btccop.cpp","game/common/physics.cpp","game/common/sim.cpp"],["frontend/common/screencarselect.cpp","eaclib/psx/spchpsxz/spchpick.cpp","frontend/common/screenmain.cpp","game/psx/nfs2mem.cpp"],["game/common/aih_cop.cpp","game/common/aih_btcperp.cpp","eaclib/psx/eacpsxz/cdfs.cpp","eaclib/psx/sndpsxz/sdriver.cpp"],["game/psx/hrzsku.cpp","game/common/audioclc.cpp","game/common/bworld.cpp","game/common/hudpmx.cpp"],["game/common/vtables_aistate.cpp","game/common/track.cpp","game/common/vtables_aihigh.cpp","eaclib/psx/sndpsxz/spktplay.cpp"],["game/common/replay.cpp","frontend/psx/memcard.c","game/common/audiomus.cpp","frontend/common/femenu.cpp","syslib/psx/libgte/REG11.cpp"],["syslib/psx/libcd/drv.cpp","frontend/common/screencontroller.cpp","game/psx/night.cpp","frontend/common/fecars.cpp","syslib/psx/libmcrd/USERFUNC.cpp"],["eaclib/psx/eacpsxz/nasync.cpp","eaclib/psx/sndpsxz/sst.cpp","frontend/common/feapp.cpp","game/common/object.cpp","frontend/psx/psxfront.cpp"],["game/common/ailife.cpp","game/common/spchevnt.c","syslib/psx/libcd/cdcont.cpp","eaclib/psx/eacpsxz/fileroot.cpp","eaclib/psx/spchpsxz/spchevnt.cpp","eaclib/psx/eacpsxz/cluttype.cpp"],["game/psx/texture.cpp","frontend/common/fedialog.cpp","eaclib/psx/eacpsxz/memstd.cpp","game/common/nfs3.cpp","syslib/psx/libcd/cdread.cpp","frontend/common/screentrackrecords.cpp"],["game/common/copspeak.cpp","eaclib/psx/sndpsxz/sdpacket.cpp","game/common/AIWORLD.cpp","game/common/pausemenu.cpp","frontend/common/fetourn.cpp","eaclib/psx/spchpsxz/spchbank.cpp"],["game/common/aihigh.cpp","eaclib/psx/eacpsxz/nsync.cpp","syslib/psx/libpad/PAD.cpp","game/common/aiinit.cpp","game/common/anim.cpp","game/common/aih_traf.cpp"],["game/common/aiperson.cpp","syslib/psx/libpad/PADMAIN.cpp","frontend/common/fememcard.cpp","syslib/psx/libcd/stream.cpp","frontend/common/screencongrats.cpp","game/psx/weather.cpp","eaclib/psx/eacpsxz/fixddiv.cpp"],["game/common/audioeng.cpp","game/common/aidatarecord.cpp","game/common/render.cpp","syslib/psx/libetc/INTR.cpp","syslib/psx/libpad/PADCMD.cpp","game/common/aih_basicperp.cpp","game/psx/cario.cpp"],["eaclib/psx/eacpsxz/unhuff.cpp","syslib/psx/libcd/streamhelp.cpp","syslib/psx/libcd/stcdint.cpp","eaclib/psx/eacpsxz/setfont.cpp","frontend/common/screenmemcard.cpp","eaclib/psx/sndpsxz/stagpat.cpp","game/common/audiotrk.cpp","game/psx/draw.cpp"],["game/common/vtables_aidatarecord.cpp","syslib/psx/libpad/PADPORTD.cpp","syslib/psx/2mbyte/2mbyte.cpp","game/common/aih_basiccop.cpp","eaclib/psx/eacpsxz/syncfile.cpp","game/common/aitriger.cpp","frontend/common/fescreen.cpp","syslib/psx/libpress/LIBPRESS.cpp","syslib/psx/libmcrd/BIOS.cpp","eaclib/psx/eacpsxz/crc.cpp"],["eaclib/psx/sndpsxz/slib.cpp","syslib/psx/libpress/VLC.cpp","game/common/vtables_object.cpp","game/common/stats.cpp","game/common/mpause.cpp","eaclib/psx/spchpsxz/spchrand.cpp","eaclib/psx/sndpsxz/snddata.cpp","game/psx/force.cpp","frontend/common/feaudio.cpp","eaclib/psx/spchpsxz/spchrule.cpp","game/common/AITUNE.cpp"],["game/common/input.cpp","frontend/psx/movie.cpp","syslib/psx/libpad/MCXMAIN.cpp","frontend/common/fetv.cpp","syslib/psx/libgpu/FONT.cpp","eaclib/psx/sndpsxz/spatkey.cpp","eaclib/psx/sndpsxz/sdma.cpp","game/common/aicop.cpp","eaclib/psx/spchpsxz/spchinit.cpp","game/common/mathnfs.cpp","syslib/psx/libpad/PADENTRY.cpp","eaclib/psx/sndpsxz/sserver.cpp","eaclib/psx/eacpsxz/textcrnt.cpp"],["game/psx/textureprocess.cpp","frontend/common/screenpost.cpp","game/psx/overlays.cpp","eaclib/psx/eacpsxz/matrix.cpp","frontend/common/fetextrender.cpp","frontend/common/fecredits.cpp","syslib/psx/libcd/TYPE.cpp","eaclib/psx/eacpsxz/locatbig.cpp","eaclib/psx/eacpsxz/vramfxya.cpp","frontend/common/fetracks.cpp","game/psx/font.cpp","frontend/common/statchk.cpp","syslib/psx/libcd/event.cpp","eaclib/psx/eacpsxz/primate.cpp","game/psx/trackspec.cpp"],["game/psx/skidmark.cpp","frontend/common/screentracks.cpp","frontend/common/screentournselect.cpp","syslib/psx/libetc/INTR_DMA.cpp","eaclib/psx/sndpsxz/spvoices.cpp","game/common/souffle.cpp","eaclib/psx/spchpsxz/spchdata.cpp","frontend/psx/video.cpp","frontend/common/screenaudio.cpp","frontend/common/fecheats.cpp","game/common/aiscript.cpp","game/psx/sfx.cpp","frontend/common/screenusername.cpp","frontend/common/screenpinkslips.cpp","eaclib/psx/eacpsxz/fastmovf.cpp","eaclib/psx/eacpsxz/xform.cpp","eaclib/psx/sndpsxz/ssysinit.cpp","eaclib/psx/eacpsxz/shpdepth.cpp"],["eaclib/psx/sndpsxz/sdfx.cpp","game/common/dashhud.cpp","eaclib/psx/sndpsxz/salloc.cpp","eaclib/psx/eacpsxz/resize.cpp","eaclib/psx/sndpsxz/smemman.cpp","game/common/chunk.cpp","game/psx/device.cpp","frontend/common/stattool.cpp","syslib/psx/libpad/PADSEQD.cpp","eaclib/psx/eacpsxz/timer.cpp","frontend/common/fevideowall.cpp","eaclib/psx/eacpsxz/nloadpk.cpp","eaclib/psx/eacpsxz/inittmr.cpp","eaclib/psx/eacpsxz/savegp.cpp","eaclib/psx/eacpsxz/atanfunc.cpp","eaclib/psx/eacpsxz/wildcard.cpp","game/common/control.cpp","frontend/common/screentrophyroom.cpp","eaclib/psx/eacpsxz/movf.cpp","syslib/psx/libgte/MSC02.cpp","syslib/psx/libapi/FIRST.cpp"],["syslib/psx/libetc/INTR_VB.cpp","syslib/psx/libcard/INIT.cpp","syslib/psx/libcard/PATCH.cpp","eaclib/psx/eacpsxz/shpsubs.cpp","syslib/psx/libcd/toc.cpp","syslib/psx/libetc/VSYNC.cpp","syslib/psx/libcd/cdread2.cpp","game/psx/psxcontroller.cpp","game/common/clock.cpp","syslib/psx/libcard/CARDINIT.cpp","frontend/common/fetools.cpp","eaclib/psx/eacpsxz/fixdatan.cpp","eaclib/psx/eacpsxz/systask.cpp","eaclib/psx/eacpsxz/asinfunc.cpp","eaclib/psx/sndpsxz/sdmemman.cpp","syslib/psx/libc/QSORT.cpp","frontend/common/feinput.cpp","eaclib/psx/eacpsxz/isincos.cpp","game/common/trgsfx.cpp","eaclib/psx/sndpsxz/ssysserv.cpp","eaclib/psx/eacpsxz/random.cpp","eaclib/psx/sndpsxz/sbremove.cpp","eaclib/psx/eacpsxz/unref.cpp","syslib/psx/libds/DSCB.cpp","game/common/simqueue.cpp","syslib/psx/libapi/COUNTER.cpp","syslib/psx/libgpu/P34.cpp"],["eaclib/psx/eacpsxz/addtimer.cpp","game/common/schedule.cpp","game/psx/fe3dmenu.cpp","syslib/psx/libc/SPRINTF.cpp","syslib/psx/libetc/VMODE.cpp","eaclib/psx/sndpsxz/sdresolv.cpp","eaclib/psx/eacpsxz/trnspos.cpp","game/common/quatern.cpp","game/psx/trsproj.cpp","eaclib/psx/eacpsxz/locatshp.cpp","eaclib/psx/sndpsxz/sfxlevel.cpp","eaclib/psx/spchpsxz/spchsamp.cpp","eaclib/psx/eacpsxz/fixdsin.cpp","frontend/psx/drawshp.cpp","syslib/psx/libsn/operators.cpp","link_data.cpp","syslib/psx/libmath/DIVDF3.cpp","eaclib/psx/sndpsxz/spat2hdr.cpp","eaclib/psx/eacpsxz/unbtree.cpp","eaclib/psx/eacpsxz/sinfunc.cpp","syslib/psx/libcard/END.cpp","syslib/psx/libmath/MULDF3.cpp","eaclib/psx/eacpsxz/textfor.cpp","game/common/color.cpp","game/common/fei.cpp","eaclib/psx/sndpsxz/ssysreal.cpp","address.cpp","eaclib/psx/sndpsxz/saetodv.cpp","eaclib/psx/sndpsxz/seffect.cpp","game/common/genericpmx.cpp","eaclib/psx/sndpsxz/sbend.cpp","eaclib/psx/eacpsxz/isqrt.cpp","frontend/common/screentrophyinfo.cpp","frontend/common/screentrackinfo.cpp","eaclib/psx/sndpsxz/sgettag.cpp","game/psx/platform.cpp"],["eaclib/psx/sndpsxz/sdtimrem.cpp","game/psx/audio.cpp","eaclib/psx/sndpsxz/sdplapat.cpp","eaclib/psx/eacpsxz/threads.cpp","eaclib/psx/eacpsxz/trnsmult.cpp","eaclib/psx/sndpsxz/smath64.cpp","eaclib/psx/sndpsxz/sstsetpr.cpp","syslib/psx/libmath/ADDDF3.cpp","eaclib/psx/eacpsxz/loadshp.cpp","eaclib/psx/eacpsxz/fixdsqrt.cpp","eaclib/psx/eacpsxz/getm.cpp","eaclib/psx/sndpsxz/sdmemlu.cpp","eaclib/psx/sndpsxz/svol.cpp","syslib/psx/libgte/PATCHGTE.cpp","eaclib/psx/sndpsxz/sbadd.cpp","syslib/psx/libmath/FERR.cpp","eaclib/psx/eacpsxz/blkfill.cpp","eaclib/psx/eacpsxz/callback.cpp","game/common/group.cpp","game/common/gmesetup.cpp","eaclib/psx/eacpsxz/exit.cpp","eaclib/psx/sndpsxz/sclcptch.cpp","eaclib/psx/eacpsxz/math64a.cpp","eaclib/psx/sndpsxz/scdvol.cpp","syslib/psx/libcd/cdtables.cpp","eaclib/psx/sndpsxz/sballoc.cpp","eaclib/psx/sndpsxz/sbdload.cpp","eaclib/psx/sndpsxz/saetolrv.cpp","eaclib/psx/sndpsxz/sbhdrcpy.cpp","syslib/psx/libmath/FIXSFSI.cpp","syslib/psx/libmath/FLTSISF.cpp","eaclib/psx/eacpsxz/fsincos.cpp","syslib/psx/libmath/DIVSF3.cpp","link_dat.cpp","link_defs.cpp","eaclib/psx/eacpsxz/fixdmult.cpp","bigbuf.cpp","eaclib/psx/eacpsxz/trnsfrm.cpp","frontend/psx/fetexture.cpp","eaclib/psx/sndpsxz/saelib.cpp","eaclib/psx/sndpsxz/s3dpos.cpp","eaclib/psx/eacpsxz/fxform.cpp","syslib/psx/libgpu/EXT.cpp","eaclib/psx/eacpsxz/stricmp.cpp","eaclib/psx/eacpsxz/isqrttbl.cpp","eaclib/psx/sndpsxz/smasterv.cpp","eaclib/psx/sndpsxz/sstsetgs.cpp","game/common/aidebug.cpp","game/common/audedit.cpp","eaclib/psx/sndpsxz/sstsetgl.cpp","eaclib/psx/sndpsxz/spvtolrv.cpp","syslib/psx/libapi/A09.cpp"],["eaclib/psx/sndpsxz/srandom.cpp","eaclib/psx/sndpsxz/sgetvol.cpp","eaclib/psx/sndpsxz/sgetdata.cpp","frontend/common/felines.cpp","frontend/common/femission.cpp","eaclib/psx/pad.c","frontend/common/fefades.cpp","eaclib/psx/spchpsxz/spchrslv.cpp","eaclib/psx/sndpsxz/spitch.cpp","eaclib/psx/sndpsxz/sover.cpp","frontend/common/mcrd.cpp","eaclib/psx/sndpsxz/stimerem.cpp","eaclib/psx/sndpsxz/sstrstat.cpp","eaclib/psx/sndpsxz/srrange.cpp","eaclib/psx/sndpsxz/sstgetrp.cpp","eaclib/psx/sndpsxz/sbirmpat.cpp","eaclib/psx/sndpsxz/sstautov.cpp","eaclib/psx/sndpsxz/sdcdvol.cpp","eaclib/psx/sndpsxz/sbvalid.cpp","eaclib/psx/sndpsxz/sdspuirq.cpp","game/common/scene.cpp","eaclib/psx/sndpsxz/sbhdrsze.cpp","eaclib/psx/sndpsxz/sstopall.cpp","eaclib/psx/sndpsxz/ssine.cpp","syslib/psx/libcd/cddebug.cpp","syslib/psx/libgte/COR_01.cpp","syslib/psx/libgte/REG03.cpp","syslib/psx/libgte/FOG_01.cpp","syslib/psx/libgte/MSC00.cpp","eaclib/psx/sndpsxz/splysdef.cpp","syslib/psx/libgte/FGO_01.cpp","syslib/psx/libgte/FGO_06.cpp","syslib/psx/libc/BSEARCH.cpp","eaclib/psx/sndpsxz/sstop.cpp","game/common/chunkvis.cpp","syslib/psx/libc/C47.cpp","syslib/psx/libc/MEMCMP.cpp","eaclib/psx/eacpsxz/joystkn.cpp","eaclib/psx/sndpsxz/sstovrhd.cpp","syslib/psx/libc/MEMMOVE.cpp","syslib/psx/libc/C25.cpp","syslib/psx/libc/C24.cpp","syslib/psx/libc/C23.cpp","syslib/psx/libc/C36.cpp","eaclib/psx/sndpsxz/sststat.cpp","syslib/psx/libc/C43.cpp","eaclib/psx/sndpsxz/sstvol.cpp","eaclib/psx/eacpsxz/shpclut.cpp","syslib/psx/libsn/PUREV.cpp","syslib/psx/libmath/MULSF3.cpp","syslib/psx/libpad/WAITRC2.cpp","syslib/psx/libmath/TRUDFSF2.cpp","eaclib/psx/sndpsxz/sautovol.cpp","syslib/psx/libsn/READ.cpp","game/common/textsys.cpp","frontend/common/screendisplay.cpp","game/common/paths.cpp","eaclib/psx/sndpsxz/span.cpp","eaclib/psx/sndpsxz/slimits.cpp","eaclib/psx/eacpsxz/crossprd.cpp","eaclib/psx/eacpsxz/blkmov.cpp","eaclib/psx/sndpsxz/s3dlow.cpp","eaclib/psx/eacpsxz/fixdinv.cpp","game/psx/unpack.c","link_init.cpp","syslib/psx/libapi/A39.cpp","game/common/aih_hum.cpp","syslib/psx/libsn/WRITE.cpp","eaclib/psx/sndpsxz/sstgetv.cpp"],["syslib/psx/libmath/EXTSFDF2.cpp","syslib/psx/libmath/ADDMANT.cpp","syslib/psx/libmath/MAINASU.cpp","syslib/psx/libmath/DBSHIFTU.cpp","syslib/psx/libmath/DBSHIFT.cpp","syslib/psx/libmath/FIXDFSI.cpp","game/common/udff.cpp","syslib/psx/libmath/GTDF2.cpp","syslib/psx/libmath/LTDF2.cpp","eaclib/psx/sndpsxz/sdata.cpp","syslib/psx/libmath/FLTSIDF.cpp","eaclib/psx/eacpsxz/meminit.cpp","frontend/common/screengrid.cpp","frontend/common/screenoptions.cpp","syslib/psx/libgpu/P16.cpp","syslib/psx/libgpu/P17.cpp","frontend/common/records.cpp","syslib/psx/libgpu/P12.cpp","syslib/psx/libgpu/P18.cpp","syslib/psx/libgte/COR_03.cpp","frontend/common/fecolor.cpp","syslib/psx/libgpu/P19.cpp","syslib/psx/libgte/COR_02.cpp","frontend/common/screencameras.cpp","syslib/psx/libgpu/P00.cpp","eaclib/psx/eacpsxz/devsys.cpp","frontend/common/screendemo.cpp","syslib/psx/libgpu/P01.cpp","syslib/psx/libgpu/P10.cpp","syslib/psx/libgpu/P11.cpp","syslib/psx/libgpu/P06.cpp","syslib/psx/libgpu/P09.cpp","syslib/psx/libc/C26.cpp","syslib/psx/libc/C27.cpp","game/psx/textpix.c","syslib/psx/libc/C21.cpp","syslib/psx/libc/C37.cpp","syslib/psx/libc/C38.cpp","syslib/psx/libc/C30.cpp","syslib/psx/libc/C31.cpp","game/psx/drawdbg.cpp","game/psx/draw2.cpp","game/common/simplemem.cpp","game/psx/loading.cpp","game/psx/rpause.cpp","syslib/psx/libc/C16.cpp","eaclib/psx/eacpsxz/_test_matrix.cpp","game/common/fastrand.cpp","syslib/psx/libapi/PAD.cpp","eaclib/psx/eacpsxz/textcode.cpp","syslib/psx/libcard/C171.cpp","game/psx/ddvfont.cpp","syslib/psx/libcard/A78.cpp","syslib/psx/libcard/C172.cpp","syslib/psx/libc/C46.cpp","syslib/psx/libc/CTYPE0.cpp","syslib/psx/libc/C40.cpp","syslib/psx/libc/C42.cpp","syslib/psx/libc/C52.cpp","game/common/minfront.cpp","game/common/new.cpp","game/psx/textpsx.c","game/psx/profile.cpp","syslib/psx/libapi/A08.cpp","syslib/psx/libapi/A07.cpp","frontend/psx/mmeffect.cpp","frontend/psx/memdsp.cpp","game/psx/debug.cpp","frontend/psx/cache.cpp","frontend/psx/mdecstat.cpp","link_ida.cpp","link_ptr.cpp","frontend/psx/endcode.cpp","link_hwreg.cpp","syslib/psx/libsn/LSEEK.cpp","syslib/psx/libsn/OPEN.cpp","syslib/psx/libsn/CREAT.cpp","syslib/psx/libsn/FSINIT.cpp","frontend/psx/readpix.cpp","syslib/psx/libsn/SNWRITE.cpp","syslib/psx/libapi/A53.cpp","game/psx/filedbg.cpp","syslib/psx/libsn/SNREAD.cpp","syslib/psx/libapi/A11.cpp","syslib/psx/libapi/L03.cpp","syslib/psx/libapi/L02.cpp","syslib/psx/libc/A63.cpp","syslib/psx/libapi/L10.cpp","game/common/debugvar.cpp","syslib/psx/libapi/C57.cpp","syslib/psx/libapi/C114.cpp","syslib/psx/libapi/C73.cpp","syslib/psx/libapi/C68.cpp","syslib/psx/libc/C19.cpp","syslib/psx/libcard/A80.cpp","syslib/psx/libcard/A76.cpp","syslib/psx/libcard/CARD.cpp","eaclib/psx/eacpsxz/nullfunc.cpp","syslib/psx/libcard/A75.cpp","game/common/async.cpp","game/common/aispeech.cpp","syslib/psx/libcard/A74.cpp","syslib/psx/libc/C63.cpp","syslib/psx/libapi/A37.cpp","syslib/psx/libapi/A36.cpp","syslib/psx/libapi/A51.cpp","syslib/psx/libapi/A50.cpp","syslib/psx/libapi/A25.cpp","syslib/psx/libapi/A13.cpp","syslib/psx/libapi/A12.cpp","syslib/psx/libapi/A24.cpp","syslib/psx/libapi/A23.cpp","syslib/psx/libapi/A52.cpp","frontend/common/fecntl.cpp","syslib/psx/libapi/A69.cpp","syslib/psx/libapi/C112.cpp","syslib/psx/libapi/A91.cpp","syslib/psx/libapi/A67.cpp","syslib/psx/libapi/A65.cpp","syslib/psx/libapi/A54.cpp","syslib/psx/libgte/REG13.cpp","syslib/psx/libapi/A66.cpp"]]

const FINDINGS_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    audited:   { type: 'integer', description: 'number of functions/data-objects actually cross-checked against the oracle' },
    not_found: { type: 'integer', description: 'count of functions/breadcrumbs that could not be located in the oracle' },
    findings: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          file:          { type: 'string' },
          function:      { type: 'string', description: 'function/method signature or data symbol name' },
          va:            { type: 'string', description: 'oracle VA e.g. 0x800F6D18, or "" if located by name only' },
          severity:      { type: 'string', enum: ['HIGH','MED','LOW'] },
          category:      { type: 'string', enum: ['signature','control-flow','constant','struct-offset','sign-width','missing-op','extra-op','data-value','not-found','other'] },
          disasm_says:   { type: 'string', description: 'what the oracle shows; quote the VA/line' },
          code_does:     { type: 'string', description: 'what the reconstructed C++ does; quote the line' },
          suggested_fix: { type: 'string' },
          confidence:    { type: 'string', enum: ['high','medium','low'] },
        },
        required: ['file','function','va','severity','category','disasm_says','code_does','suggested_fix','confidence'],
      },
    },
  },
  required: ['audited','findings'],
}

const VERDICT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    isReal:             { type: 'boolean', description: 'true ONLY if this is a genuine behavior-changing discrepancy vs the oracle' },
    corrected_severity: { type: 'string', enum: ['HIGH','MED','LOW','NONE'] },
    reasoning:          { type: 'string', description: 'cite the exact oracle VA/line and the C++ line you compared' },
  },
  required: ['isReal','corrected_severity','reasoning'],
}

const RULES = `You are auditing a reverse-engineered PSX game (NFS4 High Stakes, 1999) reconstructed as
recompilable C++. The reconstructed tree root is ${TREE}. The AUTHORITATIVE ORACLE is the
disassembly at ${ORACLE} (~13MB, VA-indexed pseudo-C). The oracle is the FINAL authority over
both the reconstructed C++ and any compiler/Ghidra output. Your job is to find places where the
reconstructed C++ does NOT faithfully match the oracle's behavior.

ORACLE FORMAT (study this):
  __<mangled>:                                  <- C++ function label (mangled name)
  // demangled: tListIterator::Value(tPlayer)   <- demangled C++ signature
  <ret> /*$v0*/ __<mangled>(<this> /*$s0*/, ...)<- proto w/ register-annotated params
  // proto: u_long * FntFlush(int id)  [libgpu.h]<- (alt header form for C funcs)
  // obj: libgpu.lib(FONT.OBJ)
  0x800F6D18  $sp += -0x50                       <- VA-indexed body, ABI register names
  0x800F6D54  if($a0 < 0x0) goto &lbl_800F6D74
  ...
Registers: $a0..$a3 = incoming args 0..3, $v0/$v1 = return, $s0..$s7 saved, $t0..$t9 temp,
$sp/$fp/$ra/$gp. Struct fields appear as *((T*)(OFFSET+$base)). DATA appears as
'.word &lbl_VA' / '.byte N' / '.ascii "..."'.

HOW TO ANCHOR each reconstructed function to the oracle (do NOT read the 13MB file whole):
  (A) VA breadcrumb present (e.g. a comment '/* @0x800F6D18 */' or '@0x800F6D18'):
      Grep the oracle for that VA -> get the line number -> Read a window
      (offset = matchLine-4, limit 150-400) to capture header + full body.
  (B) No VA (most frontend/ C++ methods): Grep the oracle for the demangled name, e.g.
      pattern 'tListIterator::Value' (matches the '// demangled:' line) OR the mangled label.
      Then Read the window around it. Class ctors/dtors anchor via 'Class::Class' / 'Class::~Class'.
Use the Grep tool (output_mode content, -n) to get line numbers, then the Read tool with
offset/limit for the window. NEVER Read the whole oracle.

WHAT TO COMPARE (semantic equivalence, function by function):
  - signature: return type and argument count/types/order ($a0=arg0...). Oracle proto is truth.
  - control-flow: branch CONDITIONS (<, <=, ==, signed vs unsigned), loop bounds, early returns,
    switch/jump-table targets, short-circuit order.
  - constant: immediate values, magic numbers, struct sizes, shift/mask amounts, array strides.
  - struct-offset: each field access offset must match the oracle's *((T*)(N+$base)).
  - sign-width: signed vs unsigned compares; load width lb/lbu/lh/lhu/lw -> char/uchar/short/ushort/int.
  - missing-op / extra-op: an operation present in the oracle but absent in C++ (or vice-versa).
  - data-value: for vtables_*.cpp, materialized_data.cpp, *_data/table files -> each C++ initializer
    word/slot (&Func, value, string) must match the oracle's '.word/.byte/.ascii' at that VA. For a
    vtable, slot K's '&Function' must equal the oracle's target at that slot.

REPORT ONLY REAL discrepancies that change runtime behavior or violate the proto signature.
DO NOT report (these are NOT findings): cosmetic/style, comment wording, local/param NAMES,
mathematically-equivalent reformulations, register-allocation differences, harmless signed/unsigned
that compiles identically, guarded-asm ': :' vs '::', or differences that are clearly just the
reconstruction's faithful idiom. When unsure whether something is behavior-changing, mark it MED
or LOW with confidence 'low' rather than inflating to HIGH.

EFFICIENCY: BIOS trampolines (single 'li $9,N; li $10,0xB0; jr $10' call) -> just confirm the
func number and B0/A0/C0 table match; one quick check each. Spend your effort on real logic.
If a function/VA cannot be located in the oracle, count it in not_found and (only if it looks like
a genuine problem, e.g. a whole function missing) emit a LOW 'not-found' finding; otherwise skip it
(it may be inlined, a weak/duplicate symbol, or our own linkage scaffolding like link_*.cpp).

OUTPUT: set 'audited' to how many functions/data-objects you actually cross-checked. Put every real
discrepancy in 'findings'. Be terse and specific: quote the oracle VA/line in disasm_says and the
C++ line in code_does. It is normal and GOOD for many bins to return zero findings.`

const auditPrompt = (files, idx) =>
`${RULES}

=== YOUR BIN (#${idx}): audit these ${files.length} file(s), every function in each ===
${files.map(f => '  - ' + TREE + '/' + f).join('\n')}

Work through each file: Read it, enumerate its functions/data-objects, anchor each to the oracle
(VA or name), compare, and record real discrepancies. Then emit the FINDINGS schema.`

const verifyPrompt = (f) =>
`You are an adversarial verifier. Another auditor flagged a possible discrepancy between the
reconstructed NFS4 C++ and the authoritative oracle. Your DEFAULT stance is skeptical: prove it is
real, or refute it. Re-derive independently from primary sources; do not trust the claim's wording.

Reconstructed tree: ${TREE}
Oracle (final authority, ~13MB VA-indexed pseudo-C): ${ORACLE}  (Grep for the VA/name, Read a window; never read it whole)

CLAIM:
  file:        ${f.file}
  function:    ${f.function}
  va:          ${f.va || '(name-anchored)'}
  category:    ${f.category}
  severity:    ${f.severity}
  disasm_says: ${f.disasm_says}
  code_does:   ${f.code_does}
  suggested_fix: ${f.suggested_fix}

Open the actual reconstructed function in ${f.file} AND the actual oracle window for ${f.function}.
Compare them yourself. Decide: is this a GENUINE behavior-changing discrepancy (or a real
signature/data mismatch)? Reject it if it is mathematically equivalent, a naming/style difference,
a faithful idiom, or the claim misread the oracle. Set corrected_severity to your own assessment
(NONE if not a real issue). Cite the exact oracle VA/line and C++ line in reasoning.`

log(`disasm-v3 audit: ${BINS.length} bins / ${BINS.reduce((a,b)=>a+b.length,0)} files / ~4871 VA-anchored fns`)

const perBin = await pipeline(
  BINS,
  (files, _orig, idx) =>
    agent(auditPrompt(files, idx), { label: `audit:bin${idx}(${files.length}f)`, phase: 'Audit', schema: FINDINGS_SCHEMA }),
  (res, _files, idx) => {
    const findings = (res && Array.isArray(res.findings)) ? res.findings : []
    const highs = findings.filter(f => f.severity === 'HIGH')
    const rest  = findings.filter(f => f.severity !== 'HIGH')
    if (!highs.length) return findings
    return parallel(highs.map(f => () =>
      agent(verifyPrompt(f), { label: `verify:bin${idx}:${String(f.function || f.va).slice(0, 28)}`, phase: 'Verify', schema: VERDICT_SCHEMA })
        .then(v => ({ ...f, verdict: v }))
        .catch(() => ({ ...f, verdict: { isReal: true, corrected_severity: f.severity, reasoning: '(verify agent errored; kept as-is)' } }))
    )).then(verified => [...verified, ...rest])
  }
)

const all = perBin.filter(Boolean).flat()
const isConfirmedHigh = f => f.severity === 'HIGH' && (!f.verdict || f.verdict.isReal)
const confirmedHigh = all.filter(isConfirmedHigh)
const rejectedHigh  = all.filter(f => f.severity === 'HIGH' && f.verdict && !f.verdict.isReal)
const med = all.filter(f => f.severity === 'MED')
const low = all.filter(f => f.severity === 'LOW')

return {
  bins: BINS.length,
  files: BINS.reduce((a, b) => a + b.length, 0),
  total_findings: all.length,
  confirmed_high: confirmedHigh.length,
  rejected_high: rejectedHigh.length,
  med: med.length,
  low: low.length,
  findings: all,
}
