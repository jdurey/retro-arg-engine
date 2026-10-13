// Multi-Apex Sister Domain Federation & Legacy Protocol Gateway (Project Stardust v5)
// Supports both direct apex hostnames:
//   - ashford-poly.org   (Academic Acoustic DSP & Substation K-7704 Lab)
//   - kamome-net.org     (PC-9801 Akasaka BBS & Shift-JIS Idol Archive)
//   - relcom-node08.org  (Leningrad Amateur Packet Radio AX.25 Relay)
//   - redcoyoacan.org    (Mexico DF Rockero Cassette & Phase-Stem Exchange)
// and path-mounted mirrors under https://stardust-archive.net/federation/<domain>/...

export const SISTER_DOMAINS = {
  "ashford-poly.org": {
    title: "ASHFORD POLYTECHNIC // DEPARTMENT OF ACOUSTIC SIGNAL PROCESSING (1995)",
    serverHeader: "CERN-HTTPd/3.0 (VAX/VMS; Ashford-Poly-DSP)",
    nodeCode: "GB-ASH-07",
    freqKhz: "4880.0",
    dyadToken: "ASHFORD-",
    body: `<PRE>
==============================================================================
 ASHFORD POLYTECHNIC UNIVERSITY (UK) // ACOUSTIC DSP LABORATORY
 SERVER: vax4000.ee.ashford-poly.org // SUBSTATION CIRCUIT: K-7704
 VISITING FELLOW ARCHIVE: MARCUS HALE (1988-1989)
==============================================================================

[1] FORTRAN-77 SUB-CARRIER PHASE-LOCKED LOOP (14_2hz_pll_filter.f77):
------------------------------------------------------------------------------
      PROGRAM STARDUST_PLL
C     ORION SUBLEVEL B2 BIAS DEMODULATOR - M. HALE / M. CHEN (1989)
      REAL SAMPLE, CARRIER, PHASE, LOCK_HZ
      PARAMETER (LOCK_HZ = 14.2001)
C     NOTE: SUM LEFT + RIGHT CHANNELS TO CANCEL 180-DEG MASKING CHORD
C     BEFORE DEMODULATING 750 HZ CW MORSE STREAM FOR SECTOR 5.
      PRINT *, 'CARRIER LOCKED AT ', LOCK_HZ, ' HZ'
      PRINT *, 'DYAD FRAGMENT ALPHA: ASHFORD-'
      END

[2] SUBSTATION K-7704 POWER BREACH TELEMETRY (09 SEP 1989 03:58 UTC):
------------------------------------------------------------------------------
  • Main bus voltage dropped to 0.0V when Technician Chen pulled breaker K-7704.
  • 4-minute battery window used to stripe Unit-7 neural weights across the
    GeoCities homestead address space via Feistel XOR seed 0x3A5F.
  • Combine our dyad token (ASHFORD-) with the Akasaka PC-98 BBS token on
    kamome-net.org to unlock Sector 5 in the Forensic Terminal.
</PRE>
<P>[ <A HREF="/forensics/signal_lab.html">Launch Interactive SSTV / Phase Cancellation Lab</A> |
<A HREF="/terminal/index.html">Open VT100 Terminal</A> |
<A HREF="/federation/kamome-net.org/index.html">Next Sister Node: kamome-net.org &gt;&gt;</A> ]</P>`,
  },
  "kamome-net.org": {
    title: "KAMOME-NET // AKASAKA PC-9801 BBS & NOVA HART MIRROR (1995)",
    serverHeader: "NCSA/1.3 (NEC PC-9801RA; FreeBSD-98)",
    nodeCode: "JP-TYO-02",
    freqKhz: "6925.0",
    dyadToken: "KAMOME-1420",
    body: `<PRE>
==============================================================================
 ╔╦╗╔═╗╔╦╗╔═╗╔╦╗╔═╗   KAMOME-NET BBS // AKASAKA LINE #2 (28.8k V.34)
  ║ ╠═╣║║║║ ║║║║╠═    SYSOP: KENJI_T // HOST: NEC PC-9801RA + YM2608 OPNA
  ╩ ╩ ╩╩ ╩╚═╝╩ ╩╚═╝   ARCHIVE: ORION JAPAN AKASAKA BRANCH (CLOSED 1993-03-31)
==============================================================================

[FILE AREA 04 // AKASAKA CRATE MANIFEST - 31 MARCH 1993]:
  FILENAME                  SIZE    DATE        DESCRIPTION
  ----------------------------------------------------------------------------
  SD0004_ROUGH_MIX.LZH   4,812K  1993-03-31  "Tape of Us" Sublevel B2 rough dub
  ROBOT36_B2_MAP.WAV       385K  1995-10-12  6925 kHz SSTV raster of Vault B2
  NOVA_PLAN_1993.TXT         2K  1993-03-31  Last .plan file before server wipe

[EXTRACTED .PLAN // NOVA7@KAMOME-NET.ORG]:
  "They packed the 2-inch master reels into aluminum cases at midnight,
   but Marcus hid the phase-inverted stem inside the runout groove.
   Dyad Fragment Beta: KAMOME-1420
   (Combine with Ashford Polytechnic token -> RESTORE 5 ASHFORD-KAMOME-1420)"
</PRE>
<P>[ <A HREF="/forensics/signal_lab.html">Decode SSTV &amp; Phase Stem</A> |
<A HREF="/terminal/index.html">Open VT100 Terminal</A> |
<A HREF="/federation/relcom-node08.org/index.html">Next Sister Node: relcom-node08.org &gt;&gt;</A> ]</P>`,
  },
  "relcom-node08.org": {
    title: "RELCOM NODE-08 // LENINGRAD AMATEUR PACKET RADIO AX.25 GATEWAY",
    serverHeader: "CERN-HTTPd/2.17beta (DEMOS/BSD; Relcom-Node08)",
    nodeCode: "SU-REL-08",
    freqKhz: "4625.0",
    dyadToken: "0x3A5F",
    body: `<PRE>
==============================================================================
 RELCOM NODE-08 // LENINGRAD SHORTWAVE &amp; AX.25 PACKET RADIO GATEWAY
 FREQUENCY: 4625.0 kHz (UVB-76 CROSS-MODULATION MONITOR) // BAUD: 110 / 300
==============================================================================

[CAPTURED BELL-103 AFSK UI FRAME // 02:14 UTC]:
  FM RELCOM-08 TO STARDUST-ALL UI PID=F0
  *** RELCOM-NODE08 AX.25 FRAME // XOR-DYAD: 0x3A5F // SECTOR-5-KEY: ASHFORD-KAMOME-1420 ***

[VIRTUAL MEMORY XOR SPECIFICATION]:
  Every GeoCities homestead in the 300,000-node Stardust swarm maps to a
  16-bit offset in the 0x89B20000 Sublevel B2 memory array.
  Paired nodes satisfy: paired_id = (node_id ^ 0x3A5F) % DOMAIN.
  Run 'XOR tokyo-garden-1420 siliconvalley-lab-1984' in the VT100 terminal
  to inspect the reconstructed stardust.c source line.
</PRE>
<P>[ <A HREF="/forensics/signal_lab.html">Demodulate Bell-103 AFSK Audio</A> |
<A HREF="/terminal/index.html">Open VT100 Terminal</A> |
<A HREF="/federation/redcoyoacan.org/index.html">Next Sister Node: redcoyoacan.org &gt;&gt;</A> ]</P>`,
  },
  "redcoyoacan.org": {
    title: "RED COYOACAN // MEXICO DF ROCKERO CASSETTE & STEM EXCHANGE (1995)",
    serverHeader: "Apache/0.8.14 (SunOS 4.1.3; UNAM-Coyoacan)",
    nodeCode: "MX-DF-04",
    freqKhz: "7345.0",
    dyadToken: "PHASE-180",
    body: `<PRE>
==============================================================================
 RED COYOACAN // INTERCAMBIO DE CINTAS &amp; LABORATORIO ACUSTICO (MEXICO DF)
 COORDINADORA: ELENA VILLALOBOS (elena@redcoyoacan.org) // 7345.0 kHz
==============================================================================

[COMPARACION DE MATRICES // CASSETTE CrO2 GENERACION 3]:
  1. Heartstrike - Live in Monterrey 1986 (B-Side Runout: 14.2 Hz Sub-Carrier)
  2. Steel Thunder (1987 VHS Hi-Fi Stereo Track - Unfiltered 16 kHz Master)
  3. Nova Hart - "Tape of Us" (Sublevel B2 Rough Mix / 180-deg Phase Stem)

[NOTA TECNICA PARA OPERADORES]:
  El canal derecho (R) del tema "rabbit_10_phase_inverted_hart_stem.mp3"
  tiene la onda portadora invertida 180 grados respecto al canal izquierdo (L).
  Al activar [PHASE CANCELLATION (L+R MONO SUM)] en el Laboratorio de Senales,
  el acorde enmascarador desaparece por completo y queda limpio el codigo
  Morse de 750 Hz: ASHFORD-KAMOME-1420.
</PRE>
<P>[ <A HREF="/forensics/signal_lab.html">Abrir Laboratorio de Cancelacion de Fase</A> |
<A HREF="/terminal/index.html">Open VT100 Terminal</A> |
<A HREF="/federation/ashford-poly.org/index.html">Back to ashford-poly.org &gt;&gt;</A> ]</P>`,
  },
};

export function renderSisterDomainHtml(domainKey) {
  const info = SISTER_DOMAINS[domainKey];
  if (!info) return null;
  return `<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<HTML><HEAD><TITLE>${info.title}</TITLE>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
<META NAME="description" CONTENT="${info.title} - Project Stardust 14.2001 Hz Federated Node ${info.nodeCode}">
</HEAD>
<BODY BGCOLOR="#030903" TEXT="#33FF33" LINK="#FFB000" VLINK="#CC8800">
${info.body}
<HR>
<ADDRESS>${info.serverHeader} &middot; Node ${info.nodeCode} (${info.freqKhz} kHz) &middot; 14.2001 Hz Carrier Locked</ADDRESS>
</BODY></HTML>\n`;
}

export function handleFederationRequest(url) {
  const host = url.hostname.toLowerCase().replace(/^www\./, "");
  let domainKey = SISTER_DOMAINS[host] ? host : null;
  if (!domainKey) {
    const m = /^\/federation\/([^/]+)(?:\/.*)?$/.exec(url.pathname);
    if (m && SISTER_DOMAINS[m[1].toLowerCase()]) {
      domainKey = m[1].toLowerCase();
    }
  }
  if (!domainKey) return null;
  const info = SISTER_DOMAINS[domainKey];
  const html = renderSisterDomainHtml(domainKey);
  const headers = new Headers({
    "Content-Type": "text/html; charset=utf-8",
    "Server": info.serverHeader,
    "X-Powered-By": "Stardust-Federation",
    "X-Federation-Node": info.nodeCode,
    "X-Stardust-Dyad-Token": info.dyadToken,
    "Cache-Control": "public, max-age=3600",
  });
  return new Response(html, { status: 200, headers });
}
