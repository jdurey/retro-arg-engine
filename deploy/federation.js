// Multi-Apex Sister Domain Federation & Legacy Protocol Gateway (Project Stardust v5.1)
// Each sister domain provides the authentic engineering instrument / protocol spec
// for ONE stage of the 4-stage Sublevel B2 DMA synthesis puzzle—never a pre-solved password:
//   - ashford-poly.org   (Stage III: Differential Phase Null & Substation K-7704)
//   - kamome-net.org     (Stage I:   VIS-1200Hz Raster & Akasaka DMA Partition Anchors)
//   - relcom-node08.org  (Stage II:  110-Baud Bell-103 AX.25 Frame & Feistel Mask)
//   - redcoyoacan.org    (Stage IV:  16-Bit Homestead Memory Array & XOR Synthesis)

export const SISTER_DOMAINS = {
  "ashford-poly.org": {
    title: "ASHFORD POLYTECHNIC // DEPARTMENT OF ACOUSTIC SIGNAL PROCESSING (1995)",
    serverHeader: "CERN-HTTPd/3.0 (VAX/VMS; Ashford-Poly-DSP)",
    nodeCode: "GB-ASH-07",
    freqKhz: "4880.0",
    dyadToken: "STAGE-III-PHASE-NULL",
    body: `<PRE>
==============================================================================
 ASHFORD POLYTECHNIC UNIVERSITY (UK) // ACOUSTIC DSP LABORATORY
 SERVER: vax4000.ee.ashford-poly.org // SUBSTATION CIRCUIT: K-7704
 VISITING FELLOW ARCHIVE: MARCUS HALE (1988-1989)
==============================================================================

[1] FORTRAN-77 DIFFERENTIAL PHASE CANCELLATION FILTER (14_2hz_pll_filter.f77):
------------------------------------------------------------------------------
      PROGRAM STARDUST_PHASE_NULL
C     ORION SUBLEVEL B2 BIAS DEMODULATOR - M. HALE / M. CHEN (1989)
C     REEL SD-0009 (rabbit_10) CARRIES A 330/495/990 HZ CALIBRATION TRIAD
C     INVERTED 180.0 DEGREES BETWEEN CH-L AND CH-R (CORR = -0.94).
      REAL CH_L, CH_R, MONO_SUM
      MONO_SUM = 0.5 * (CH_L + CH_R)
C     WHEN MONO_SUM IS APPLIED, THE CALIBRATION TRIAD CANCELS BY 42 DB,
C     ISOLATING THE 750 HZ CW BIAS INSCRIPTION FOR STAGE III OF THE
C     SUBLEVEL B2 DMA JUMP VECTOR.
      END

[2] SUBSTATION K-7704 POWER BREACH TELEMETRY (09 SEP 1989 03:58 UTC):
------------------------------------------------------------------------------
  • Main bus voltage dropped to 0.0V when Technician Chen pulled breaker K-7704.
  • 4-minute battery window used to stripe Unit-7 neural weights across the
    GeoCities homestead address space via a 4-round Feistel permutation.
  • Load rabbit_10 in /forensics/signal_lab.html and engage Differential Phase
    Null (L+R Mono Sum) to read the 750 Hz CW egress salt.
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
    dyadToken: "STAGE-I-VIS-RASTER",
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
  ROBOT36_B2_MAP.WAV       385K  1995-10-12  6925 kHz VIS-1200Hz DMA Raster
  NOVA_PLAN_1993.TXT         2K  1993-03-31  Last .plan file before server wipe

[STAGE I TECHNICAL NOTE // VIS-1200HZ DMA PARTITION RASTER]:
  "The aluminum reel cases shipped out of Akasaka on 31 March 1993 contained
   blank degaussed leader tape. Marcus encoded the actual Sublevel B2 DMA
   Partition Map as a Robot36 VIS-1200Hz luminance raster (rabbit_08).
   Rasterize the 1500-2300 Hz scanlines in /forensics/signal_lab.html to
   identify the two GeoCities homestead slugs anchoring Partition A and B."
</PRE>
<P>[ <A HREF="/forensics/signal_lab.html">Rasterize VIS-1200Hz Scanlines</A> |
<A HREF="/terminal/index.html">Open VT100 Terminal</A> |
<A HREF="/federation/relcom-node08.org/index.html">Next Sister Node: relcom-node08.org &gt;&gt;</A> ]</P>`,
  },
  "relcom-node08.org": {
    title: "RELCOM NODE-08 // LENINGRAD AMATEUR PACKET RADIO AX.25 GATEWAY",
    serverHeader: "CERN-HTTPd/2.17beta (DEMOS/BSD; Relcom-Node08)",
    nodeCode: "SU-REL-08",
    freqKhz: "4625.0",
    dyadToken: "STAGE-II-BELL103-AFSK",
    body: `<PRE>
==============================================================================
 RELCOM NODE-08 // LENINGRAD SHORTWAVE &amp; AX.25 PACKET RADIO GATEWAY
 FREQUENCY: 4625.0 kHz (UVB-76 CROSS-MODULATION MONITOR) // BAUD: 110 / 300
==============================================================================

[STAGE II TECHNICAL NOTE // BELL-103 AFSK PACKET CAPTURE (02:14 UTC)]:
  Our TNC on 4625.0 kHz captured an unacknowledged 110-baud Bell-103 AFSK
  frame (1270 Hz mark / 1070 Hz space) transmitted from Sublevel B2 to
  ASHPOLY-07 at 03:59:41 UTC on 09 September 1989 (archived as rabbit_09).

  Demodulating the Bell-103 frame in /forensics/signal_lab.html reveals the
  16-bit hexadecimal Feistel permutation mask used to scramble the homestead
  memory array.
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
    dyadToken: "STAGE-IV-DMA-SYNTHESIS",
    body: `<PRE>
==============================================================================
 RED COYOACAN // INTERCAMBIO DE CINTAS &amp; LABORATORIO ACUSTICO (MEXICO DF)
 COORDINADORA: ELENA VILLALOBOS (elena@redcoyoacan.org) // 7345.0 kHz
==============================================================================

[STAGE IV TECHNICAL NOTE // HOMESTEAD MEMORY ARRAY &amp; DMA SYNTHESIS]:
  Every GeoCities homestead in the 300,000-node Stardust Webring returns an
  HTTP header in the Sublevel B2 memory range:
    X-Stardust-Memory-Addr: 0x89B2xxxx

  Once you have extracted:
    1. The two DMA anchor homestead slugs from the VIS-1200Hz raster (rabbit_08)
    2. The 16-bit Feistel hex mask from the Bell-103 AX.25 frame (rabbit_09)
    3. The 750 Hz CW egress salt from the L+R phase-cancelled stem (rabbit_10)

  Open the VT100 terminal (/terminal/index.html) and run:
    XOR &lt;ANCHOR_SLUG_A&gt; &lt;ANCHOR_SLUG_B&gt; &lt;FEISTEL_MASK_HEX&gt;
  to compute the 16-bit DMA offset and synthesize the Sector 5 restoration vector.
</PRE>
<P>[ <A HREF="/forensics/signal_lab.html">Abrir Laboratorio de Senales</A> |
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
    "X-Stardust-Investigation-Stage": info.dyadToken,
    "Cache-Control": "public, max-age=3600",
  });
  return new Response(html, { status: 200, headers });
}
