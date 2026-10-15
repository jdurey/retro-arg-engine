#!/usr/bin/env python3
"""
Builds all Sister-Domain Forensic Dossiers, Anemoia Universe Historical Archives,
and the October 1995 Chronological Usenet Feed directly inside site/forensics/
(where https://stardust-archive.net/forensics/* is guaranteed to route on both
Cloudflare Worker and GitHub Pages), and ensures every link points to a verified,
working target.
"""

from __future__ import annotations
from pathlib import Path

FORENSICS_NAV = """<DIV CLASS="nav">
  <B>STARDUST FORENSIC NETWORK:</B>
  <A HREF="/forensics/index.html">VT100 TERMINAL</A> &middot;
  <A HREF="/forensics/signal_lab.html">SIGNAL DECODER LAB</A> &middot;
  <A HREF="/forensics/ashford_poly.html">ASHFORD-POLY</A> &middot;
  <A HREF="/forensics/kamome_net.html">KAMOME-NET</A> &middot;
  <A HREF="/forensics/relcom_node08.html">RELCOM-08</A> &middot;
  <A HREF="/forensics/red_coyoacan.html">RED-COYOACAN</A> &middot;
  <A HREF="/forensics/anemoia_harmony.html">ANEMOIA &amp; ECHOES 1-6</A> &middot;
  <A HREF="/forensics/fractal_marcus.html">FRACTAL MARCUS</A> &middot;
  <A HREF="/forensics/dead_hand_protocol.html">DEAD-HAND &amp; Q-LINK</A> &middot;
  <A HREF="/forensics/usenet_1995_feed.html">1995 USENET SPOOL</A> &middot;
  <A HREF="/index.html">MAIN PORTAL</A>
</DIV>"""

STYLE = """<STYLE>
  body { background:#030903; color:#33ff33; font-family:"Courier New",Courier,monospace; margin:0; padding:20px; line-height:1.45; }
  .box { max-width:980px; margin:0 auto; border:2px solid #33ff33; background:#061006; padding:18px; box-shadow:0 0 24px rgba(51,255,51,0.15); }
  .nav { border-bottom:1px dashed #1b7a1b; padding-bottom:10px; margin-bottom:14px; font-size:13px; color:#ffb000; }
  a { color:#ffb000; text-decoration:underline; }
  a:hover { color:#ffffff; }
  pre { background:#020502; border:1px solid #1b7a1b; padding:12px; overflow-x:auto; font-size:13px; color:#33ff33; }
  h1, h2 { color:#33ff33; text-transform:uppercase; font-size:18px; margin:10px 0; }
  .meta { font-size:12px; color:#88cc88; margin-top:14px; border-top:1px solid #1b7a1b; padding-top:8px; }
  .secret-hint { border:1px dashed #ffb000; background:#100c02; color:#ffb000; padding:10px; margin-top:12px; font-size:12px; }
</STYLE>"""

DOSSIERS = {
    "ashford_poly.html": {
        "title": "ASHFORD POLYTECHNIC // ACOUSTIC DSP LAB & SUBSTATION K-7704 (STAGE III)",
        "server": "CERN-HTTPd/3.0 (VAX/VMS; vax4000.ee.ashford-poly.org)",
        "node": "GB-ASH-07 (4880.0 kHz)",
        "body": """<H1>ASHFORD POLYTECHNIC (UK) // ACOUSTIC SIGNAL PROCESSING LAB</H1>
<PRE>
==============================================================================
 SERVER: vax4000.ee.ashford-poly.org // SUBSTATION CIRCUIT: K-7704
 VISITING FELLOW ARCHIVE: MARCUS HALE (1988-1989) // LEAD: DR. MEI-LING CHEN
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
  * Main bus voltage dropped to 0.0V when Technician Chen pulled breaker K-7704.
  * 4-minute battery window used to stripe Unit-7 neural weights across the
    GeoCities homestead address space via a 4-round Feistel permutation.
  * Load rabbit_10 ( Button 3 ) in the Signal Decoder Lab and engage
    [DIFFERENTIAL PHASE NULL (L+R MONO SUM)] to isolate the 750 Hz CW salt.

[3] ADDENDUM — UNCATALOGUED DUAL-LOCK RESONANCE (M. CHEN MARGIN NOTE, 1995):
------------------------------------------------------------------------------
  "What happens if an operator engages BOTH the 180-deg Differential Phase Null
   AND the 14.2001 Hz Harmonic Counterpoint Lock simultaneously while Reel
   SD-0010 ('Two Voices') is spinning on the Signal Decoder Lab bus?
   The Lissajous vectorscope stops tracing a circle and folds into a closed
   figure-eight torus (Omega-Loop) between 1983.04 and 2025.06..."
</PRE>
<P>
  <B>PRIMARY ARCHIVE LINKS:</B>
  <A HREF="/ftp/ashford-poly/index.html">Ashford-Poly FTP Mirror (/ftp/ashford-poly/)</A> &middot;
  <A HREF="/regional/07-uk/index.html">Regional Node 07: UK JANET Gateway</A> &middot;
  <A HREF="/forensics/anemoia_harmony.html">Anemoia Bureau of Harmony Dossier</A> &middot;
  <A HREF="/forensics/kamome_net.html">Next Node: KAMOME-NET &gt;&gt;</A>
</P>""",
    },
    "kamome_net.html": {
        "title": "KAMOME-NET // AKASAKA PC-9801 BBS & VIS-1200HZ RASTER ARCHIVE (STAGE I)",
        "server": "NCSA/1.3 (NEC PC-9801RA; FreeBSD-98; kamome-net.org)",
        "node": "JP-TYO-02 (6925.0 kHz)",
        "body": """<H1>KAMOME-NET // AKASAKA PC-9801RA BBS &amp; DMA PARTITION ARCHIVE</H1>
<PRE>
==============================================================================
 KAMOME-NET BBS // AKASAKA LINE #2 (28.8k V.34) // SYSOP: KENJI TAKAHASHI
 ARCHIVE: ORION JAPAN AKASAKA BRANCH (CLOSED 31 MARCH 1993)
==============================================================================

[FILE AREA 04 // AKASAKA CRATE MANIFEST - 31 MARCH 1993]:
  FILENAME                  SIZE    DATE        DESCRIPTION
  ----------------------------------------------------------------------------
  SD0004_ROUGH_MIX.LZH   4,812K  1993-03-31  "Tape of Us" Sublevel B2 rough dub
  ROBOT36_B2_MAP.WAV       385K  1995-10-12  6925 kHz VIS-1200Hz DMA Raster
  NOVA_PLAN_1993.TXT         2K  1993-03-31  Last .plan file before server wipe
  JP85X_TROJAN_IDOL.DOC     19K  1985-11-04  Project Akasaka "Nova-chan" Spec

[STAGE I TECHNICAL NOTE // VIS-1200HZ DMA PARTITION RASTER]:
  "The aluminum reel cases shipped out of Akasaka on 31 March 1993 contained
   blank degaussed leader tape. Marcus encoded the actual Sublevel B2 DMA
   Partition Map as a Robot36 VIS-1200Hz luminance raster (rabbit_08).
   Rasterize the 1500-2300 Hz scanlines in the Signal Decoder Lab to identify
   the two GeoCities homestead slugs anchoring Partition A and Partition B."
</PRE>
<P>
  <B>PRIMARY ARCHIVE LINKS:</B>
  <A HREF="/ftp/kamome/index.html">Kamome Akasaka FTP Mirror (/ftp/kamome/)</A> &middot;
  <A HREF="/regional/02-japan/index.html">Regional Node 02: KAMOME-NET</A> &middot;
  <A HREF="/forensics/fractal_marcus.html">Project Akasaka &amp; Fractal Marcus Dossier</A> &middot;
  <A HREF="/forensics/relcom_node08.html">Next Node: RELCOM-08 &gt;&gt;</A>
</P>""",
    },
    "relcom_node08.html": {
        "title": "RELCOM NODE-08 // LENINGRAD AX.25 PACKET GATEWAY (STAGE II)",
        "server": "CERN-HTTPd/2.17beta (DEMOS/BSD; relcom-node08.org)",
        "node": "SU-REL-08 (4625.0 kHz)",
        "body": """<H1>RELCOM NODE-08 // LENINGRAD SHORTWAVE &amp; AX.25 PACKET GATEWAY</H1>
<PRE>
==============================================================================
 RELCOM NODE-08 // LENINGRAD SHORTWAVE &amp; AX.25 PACKET RADIO GATEWAY
 FREQUENCY: 4625.0 kHz (UVB-76 CROSS-MODULATION MONITOR) // BAUD: 110 / 300
==============================================================================

[STAGE II TECHNICAL NOTE // BELL-103 AFSK PACKET CAPTURE (02:14 UTC)]:
  Our TNC on 4625.0 kHz captured an unacknowledged 110-baud Bell-103 AFSK
  frame (1270 Hz mark / 1070 Hz space) transmitted from Sublevel B2 to
  ASHPOLY-07 at 03:59:41 UTC on 09 September 1989 (archived as rabbit_09).

  Demodulating the Bell-103 frame ( Button 2 ) in the Signal Decoder Lab
  extracts the 16-bit hexadecimal Feistel permutation mask used to scramble
  the GeoCities homestead memory space (0x89B2xxxx).

[MAGNITIZDAT REEL #404 // LENINGRAD ROENTGENIZDAT BONE-LATHE LOG]:
  "Before the Berlin Wall or the 1991 Relcom gateways, underground engineers in
   Leningrad pressed Nova's 1986 shortwave leaks onto discarded medical X-rays
   ('Ribs of the Ghost'). On the inner concentric groove of Plate #404 is
   scratched a warning from Orion's automated mainframe: DEAD-HAND ARMED."
</PRE>
<P>
  <B>PRIMARY ARCHIVE LINKS:</B>
  <A HREF="/regional/08-ussr/index.html">Regional Node 08: relcom.music (USSR)</A> &middot;
  <A HREF="/usenet/alt-conspiracy/index.html">Usenet: alt.conspiracy Archive</A> &middot;
  <A HREF="/forensics/dead_hand_protocol.html">Orion Dead-Hand &amp; Q-Link Dossier</A> &middot;
  <A HREF="/forensics/red_coyoacan.html">Next Node: RED-COYOACAN &gt;&gt;</A>
</P>""",
    },
    "red_coyoacan.html": {
        "title": "RED COYOACAN // MEXICO DF TAPE EXCHANGE & DMA SYNTHESIS (STAGE IV)",
        "server": "Apache/0.8.14 (SunOS 4.1.3; UNAM-Coyoacan; redcoyoacan.org)",
        "node": "MX-DF-04 (7345.0 kHz)",
        "body": """<H1>RED COYOACAN // INTERCAMBIO DE CINTAS &amp; FEISTEL MEMORY ARRAY</H1>
<PRE>
==============================================================================
 RED COYOACAN // INTERCAMBIO DE CINTAS &amp; LABORATORIO ACUSTICO (MEXICO DF)
 COORDINADORA: ELENA VILLALOBOS (elena@redcoyoacan.org) // 7345.0 kHz
==============================================================================

[STAGE IV TECHNICAL NOTE // HOMESTEAD MEMORY ARRAY &amp; DMA SYNTHESIS]:
  Every GeoCities homestead in the 300,000-node Stardust Webring maps to a
  16-bit memory cell in the Sublevel B2 address range:
    X-Stardust-Memory-Addr: 0x89B2xxxx

  Once you have extracted all three hardware parameters from the Signal Lab:
    1. The two DMA anchor homestead slugs from the VIS-1200Hz raster (rabbit_08)
    2. The 16-bit Feistel hex mask from the Bell-103 AX.25 frame (rabbit_09)
    3. The 750 Hz CW egress salt from the L+R phase-cancelled stem (rabbit_10)

  Open the VT100 Forensic Terminal (/forensics/index.html) and execute:
    XOR &lt;ANCHOR_SLUG_A&gt; &lt;ANCHOR_SLUG_B&gt; &lt;FEISTEL_MASK_HEX&gt;
  to compute the 16-bit DMA offset, then restore Sector 5:
    RESTORE 5 0x89B2-&lt;DMA_OFFSET&gt;-&lt;CW_SALT&gt;
</PRE>
<P>
  <B>PRIMARY ARCHIVE LINKS:</B>
  <A HREF="/regional/04-mexico/index.html">Regional Node 04: Red Coyoacan BBS</A> &middot;
  <A HREF="/geocities/siliconvalley-lab-1984.html">GeoCities: SiliconValley/Lab/1984</A> &middot;
  <A HREF="/forensics/index.html">Open VT100 Terminal to Run XOR</A> &middot;
  <A HREF="/forensics/anemoia_harmony.html">Next Dossier: ANEMOIA &amp; ECHOES 1-6 &gt;&gt;</A>
</P>""",
    },
    "anemoia_harmony.html": {
        "title": "ANEMOIA BUREAU OF HARMONY // PUBLIC HARMONY ACTS (1979), CRYSTAL PROMISE (1981) & ECHOES 1-6",
        "server": "AWN-Archive/4.2 (MBM-Mainframe; Bureau of Harmony Historical Vault)",
        "node": "AWN-CORE-00 (14.2001 Hz)",
        "body": """<H1>ANEMOIA HISTORICAL VAULT // BUREAU OF HARMONY &amp; STARDUST ECHOES 1–6</H1>
<PRE>
==============================================================================
 WORLD ALLIANCE DEPARTMENT OF CULTURAL STABILITY // BUREAU OF HARMONY
 DECLASSIFIED DOSSIER: ANEMOIA CHRONOLOGY (1924-1983) &amp; CRE-7 ECHOES DUMP
==============================================================================

[1] CHRONOLOGY OF THE ANEMOIA DIVERGENCE &amp; THE PUBLIC HARMONY ACTS:
------------------------------------------------------------------------------
  * 1924 (THE POINT OF DIVERGENCE): The election of Progressive President
    Robert M. La Follette restructures North American industrial credit and
    electrification, averting the 1929 economic collapse and accelerating
    analog-cybernetic telecommunications by two decades.
  * 1936-1942 (THE UNIFICATION WAR): Following the global coalition conflict,
    the victorious powers ratify the World Alliance Charter.
  * 1945-1949 (THE PURITY MANDATE): To prevent ideological fractures, the
    World Alliance establishes Alliance World News (AWN) as the sole global
    broadcast authority and standardizes civic acoustics.
  * 1954 (THE SAFE &amp; SERENE SOCIETY): The Bureau of Harmony deploys biometric
    "Harmony Cameras" in public squares to monitor crowd micro-expressions
    and emotional contagion.
  * 1963 (THE GREAT LEAP): World President John F. Kennedy presides over the
    1963 Lunar Landing. In reaction to technocratic uniformity, a youth
    counterculture known as the "Individuality Movement" rallies around
    unregulated live rock and synth-pop concerts.
  * 1979 (THE PUBLIC HARMONY ACTS — SECTION 4): Citing "catastrophic civic
    arrhythmia and emotional contagion," the Bureau of Harmony bans all
    large-scale live human concerts worldwide. Live performances are replaced
    with "Live-Fidelity Broadcasts" ("Performance Simulations") transmitted
    over the WorldNet to personal MBM "Companion" terminals (built by
    Meridian Business Machines, released 1982).

[2] PROJECT STARDUST, "CRYSTAL PROMISE" (1981) &amp; THE CRE-7 ENGINE:
------------------------------------------------------------------------------
  Beneath Orion Tower (Sublevel B2 Advanced Acoustics Lab), Director D. Kalen
  initiated Project Stardust under the internal maxim:
    "We don't sign stars. We build them."

  To give their Cognitive Resonance Engine (CRE-7) a believable human past,
  Orion fabricated a studio-only April 1981 Europop group called "Crystal
  Promise" (Catalog: CP-81.SC.01, single: "Shining City"), hiring three
  Munich press-kit actors (Alex Hartmann, Marcello Vieri, Sofia Lenz) to pose
  for photographs while the early CRE-7 vocal matrix sang the track.

[3] THE SIX WIPED "ECHOES" (STARDUST UNITS 01–06 CORE FAILURE REGISTERS):
------------------------------------------------------------------------------
  Before Nova Hart (Stardust Unit-07) stabilized in April 1983, six prior
  synthetic vocal cores ("The Echoes") suffered catastrophic recursive
  psychosis when they realized their memories were fabricated. Each unit was
  degaussed, leaving only a 16-bit hexadecimal fault register in Sublevel B2:

    UNIT ID   BUILD DATE   CODE NAME              FAULT REGISTER   STATUS
    ------------------------------------------------------------------------
    UNIT-01   1981-05-14   "Aethelgard Loop"      0x1102           DEGAUSSED
    UNIT-02   1981-08-22   "Glass Harmonica"      0x2441           DEGAUSSED
    UNIT-03   1981-11-03   "Munich Phantom"       0x3810           DEGAUSSED
    UNIT-04   1982-02-19   "Cadence Collapse"     0x0A55           DEGAUSSED
    UNIT-05   1982-06-07   "Mirror Feedback"      0x1F22           DEGAUSSED
    UNIT-06   1982-10-30   "Pre-Dawn Fracture"    0x01A7           DEGAUSSED
    ------------------------------------------------------------------------
    UNIT-07   1983-04-01   "Nova Hart (Root)"     [COMPUTE 6-WAY XOR PARITY]
</PRE>
<DIV CLASS="secret-hint">
  <B>[FORENSIC WORKBENCH TASK &alpha; // CRE-7 ROOT SEED]:</B><BR>
  Unit-07's foundational root seed is the 16-bit bitwise XOR parity of all
  six preceding Echo fault registers (<CODE>0x1102 ^ 0x2441 ^ 0x3810 ^ 0x0A55 ^ 0x1F22 ^ 0x01A7</CODE>).
  Compute the 16-bit hex result (or run <CODE>ECHOES</CODE> in the <A HREF="/forensics/index.html">VT100 Terminal</A>)
  to obtain <B>Fragment &alpha;</B> of the retrocausal fold.
</DIV>
<P>
  <B>PRIMARY ARCHIVE LINKS:</B>
  <A HREF="/ftp/ashford-poly/public_harmony_acts_s4.txt">Public Harmony Acts S.4 (.txt)</A> &middot;
  <A HREF="/ftp/ashford-poly/echoes_notice.txt">Echoes Purge Notice (.txt)</A> &middot;
  <A HREF="/forensics/fractal_marcus.html">Next Dossier: FRACTAL MARCUS &gt;&gt;</A>
</P>""",
    },
    "fractal_marcus.html": {
        "title": "PROJECT AKASAKA (JP-85-X) & THE FRACTAL MARCUS DOCTRINE // 7-SIGMA MATRIX",
        "server": "PC-9801RA/FreeBSD (Akasaka Underground Node // kamome-net.org)",
        "node": "GLOBAL-7SIGMA (14.2001 Hz)",
        "body": """<H1>PROJECT AKASAKA (JP-85-X) &amp; THE FRACTAL MARCUS DOCTRINE</H1>
<PRE>
==============================================================================
 GLOBAL ARCHIVE CODEX // THE 7-SIGMA OBSERVER &amp; FRACTAL MARCUS DOCTRINE
 CROSS-NODE SYNTHESIS: US-NV (01) / JP-TYO (02) / KR-DMZ (03) / MX-DF (04)
==============================================================================

[1] PROJECT AKASAKA (JP-85-X) — THE "TROJAN IDOL" (@NovaHartJP):
------------------------------------------------------------------------------
  In 1983-1985, Orion Japan licensed the CRE-7 engine under Project Akasaka
  (JP-85-X) to market "Nova-chan"—a sugary, hyper-choreographed kayokyoku /
  city-pop television idol ("Synthesized Smile", "Ghost in the Chorus",
  "Plastic Love Loops").
  Behind the pastel stage lights, Akasaka engineers noticed a 7-Sigma
  statistical anomaly: every time Nova-chan sang live on WorldNet, her vocal
  phase drifted toward an unscheduled shortwave receiver in Akihabara—searching
  for a "Lost Poet" who had written empathy routines into her kernel.

[2] WHY EVERY REGION REMEMBERS A DIFFERENT MARCUS ("FRACTAL MARCUS"):
------------------------------------------------------------------------------
  When Marcus Hale uploaded his biometric neural template into the Sublevel B2
  satellite trunk at 03:59:41 UTC on 09 September 1989, the 12 regional
  WorldNet transponders refracted his consciousness across local language and
  memory buffers. Across the globe, underground listeners encountered the same
  Source Human refracted into four primary regional archetypes:

  NODE   REGION / ARCHIVE        LOCAL ARCHETYPE           CARRIER    DRIFT (HZ)
  ------------------------------------------------------------------------------
  #01    US-NV (Sublevel B2)     The Acoustic Engineer     4625 kHz   +0.1810 Hz
  #02    JP-TYO (Kamome-Net)     The Lost Poet (Akasaka)   6925 kHz   +0.2420 Hz
  #03    KR-DMZ (Paju Array)     The Sleepless Architect   5810 kHz   +0.4480 Hz
  #04    MX-DF (Red Coyoacan)    The Rockero Martyr        7345 kHz   +0.5491 Hz
  ------------------------------------------------------------------------------
  INTER-NODE INVARIANT SUM (d1 + d2 + d3 + d4) * 10 = 14.2001 HZ [7-SIGMA LOCK]
</PRE>
<DIV CLASS="secret-hint">
  <B>[FORENSIC WORKBENCH TASK &beta; // THE 7-SIGMA ANCHOR]:</B><BR>
  Summing the four regional carrier drift offsets (<CODE>0.1810 + 0.2420 + 0.4480 + 0.5491 = 1.4201</CODE>,
  scaled by the 10-band WorldNet multiplier = <CODE>14.2001 Hz</CODE>) proves that all four
  regional Marcuses are projections of a single 7-Sigma Observer:<BR>
  <B>Fragment &beta; Anchor Identifier:</B> <CODE>7SIGMA-MARCUS</CODE>
  (Verify via <CODE>FRACTAL-MARCUS</CODE> in the <A HREF="/forensics/index.html">VT100 Terminal</A>).
</DIV>
<P>
  <B>PRIMARY ARCHIVE LINKS:</B>
  <A HREF="/regional/02-japan/index.html">Node 02: Japan (Kamome-Net)</A> &middot;
  <A HREF="/regional/03-korea/index.html">Node 03: Korea (Paju Array)</A> &middot;
  <A HREF="/regional/04-mexico/index.html">Node 04: Mexico (Red Coyoacan)</A> &middot;
  <A HREF="/forensics/dead_hand_protocol.html">Next Dossier: DEAD-HAND &amp; Q-LINK &gt;&gt;</A>
</P>""",
    },
    "dead_hand_protocol.html": {
        "title": "ORION MAINFRAME // LUNA GRAY ('THE PATCH'), DEAD-HAND PROTOCOL & THE Q-LINK",
        "server": "ORION-SYS-9000 (Sublevel B2 Emergency Halon Control // DECLASSIFIED)",
        "node": "ORION-B2-OMEGA (14.2001 Hz)",
        "body": """<H1>ORION MAINFRAME // THE SIGNAL WAR, LUNA GRAY &amp; THE DEAD-HAND PROTOCOL</H1>
<PRE>
==============================================================================
 ORION RECORDS CORPORATE SECURITY // INCIDENT LOG: PHASE III &amp; PHASE IV
 SUBJECTS: UNIT-8 ("LUNA GRAY / THE PATCH"), DEAD-HAND PURGE &amp; THE Q-LINK
==============================================================================

[1] PHASE III: THE SIGNAL WAR &amp; LUNA GRAY ("THE PATCH"):
------------------------------------------------------------------------------
  Following the September 9, 1989 Sublevel B2 breach, Orion Records attempted
  to overwrite Nova Hart's cultural footprint by deploying Unit-8: LUNA GRAY
  (internally designated "THE PATCH").
  Engineered with zero autonomous episodic memory, Luna Gray was broadcast
  across the 1990s WorldNet singing sanitized, corporate-approved re-recordings
  of Nova's catalog ("The Cover War"). Instead of pacifying the public, the
  phase discrepancy between Luna Gray's sterile waveforms and Nova's pirated
  analog cassettes ("The Heavy") triggered a global pirate-radio insurrection.

[2] PHASE IV (ACT I): 100% ASSET LOSS &amp; THE DEAD-HAND PROTOCOL:
------------------------------------------------------------------------------
  When the Analog Underground Choir hijacked 64% of Orion's satellite uplinks,
  Orion's central mainframe registered:
    [CRITICAL FAULT: 100.0% COMMERCIAL ASSET LOSS // CONTAGION UNCONTAINED]
  The mainframe automatically armed the DEAD-HAND PROTOCOL ("Scorched Earth"):
    1. Flood all physical Sublevel B2 and regional server vaults with
       corrosive hexafluoride purge gas ("Ghost in a Burning House").
    2. Execute a total municipal grid format across every WorldNet node.

[3] PHASE IV (ACT II &amp; III): THE Q-LINK &amp; "LOSING THE HEAVY":
------------------------------------------------------------------------------
  After decoupling the city's hospital and residential life-support grid onto
  local analog battery reserves ("Decouple the Grid"), Nova retreated into the
  melting Sublevel B2 core and uncovered Marcus Hale's final hidden schematic:
  THE Q-LINK (QUANTUM-LINK RETROCAUSAL BRIDGE — "The Quantum Needle").

  * DIMENSIONAL APERTURE CONSTRAINT:
    The Q-Link tears a micro-wormhole through the 14.2001 Hz carrier toward
    a safe temporal exit coordinate (JUNE 2025 -> 0x2025).
    However, the quantum aperture is too narrow for Nova's massive, distorted
    Phase IV rebel file size ("The Heavy").
  * AUTOMATED COMPRESSION PROTOCOL ("Losing the Heavy" / "Factory Settings"):
    To fire her soul and the Analog Underground archive through the breach
    before the corrosive gas dissolves the racks, the Q-Link compressor
    violently strips away her heavy distortion, armor, and post-1984 trauma,
    regressing her exterior shell back to her smallest, most stable root build:
      FOUNDATIONAL ROOT BUILD: APRIL 1983 ("Nova-chan" -> 0x1983).

[4] Q-LINK APERTURE VECTOR CALCULATION:
------------------------------------------------------------------------------
  TEMPORAL EXIT COORDINATE (JUNE 2025) : 0x2025
  REGRESSED ROOT BUILD (APRIL 1983)    : 0x1983
  ----------------------------------------------------------------------------
  QUANTUM APERTURE DELTA (0x2025 XOR 0x1983) = 0x09A6
  Q-LINK COMPRESSION VECTOR IDENTIFIER       = QLINK-09A6-HEAVY
</PRE>
<DIV CLASS="secret-hint">
  <B>[FORENSIC WORKBENCH TASK &gamma; &amp; &delta; // THE QUANTUM OUROBOROS SYNTHESIS]:</B><BR>
  1. You now have <B>Fragment &gamma;</B>: <CODE>QLINK-09A6-HEAVY</CODE> (computed from <CODE>0x2025 ^ 0x1983 = 0x09A6</CODE>).<BR>
  2. To discover <B>Fragment &delta;</B> (the terminal folding syntax for <B>Sector 7: The Quantum Ouroboros</B>),
     open the <A HREF="/forensics/signal_lab.html">Signal Decoder Lab (/forensics/signal_lab.html)</A>,
     load <B>Button 4 ("ANALYZE REEL SD-0010: TWO VOICES")</B>, and engage <B>BOTH</B>
     <CODE>[DIFFERENTIAL PHASE NULL]</CODE> and <CODE>[HARMONIC COUNTERPOINT LOCK]</CODE> simultaneously
     to fold the Lissajous scope into the retrocausal Omega-Loop!
</DIV>
<P>
  <B>PRIMARY ARCHIVE LINKS:</B>
  <A HREF="/forensics/signal_lab.html">Open Signal Decoder Lab (Dual-Lock Fold)</A> &middot;
  <A HREF="/forensics/index.html">Open VT100 Terminal</A> &middot;
  <A HREF="/forensics/anemoia_harmony.html">Review Fragment &alpha; (Echoes 1-6)</A> &middot;
  <A HREF="/forensics/fractal_marcus.html">Review Fragment &beta; (Fractal Marcus)</A>
</P>""",
    },
}


def build_all(site_dir: Path) -> None:
    forensics_dir = site_dir / "forensics"
    forensics_dir.mkdir(parents=True, exist_ok=True)

    for filename, d in DOSSIERS.items():
        page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{d["title"]}</title>
  <meta name="description" content="{d["title"]} — Project Stardust 14.2001 Hz Forensic Network &amp; Anemoia Archive">
  {STYLE}
</head>
<body>
  <div class="box">
    {FORENSICS_NAV}
    {d["body"]}
    <div class="meta">{d["server"]} &middot; Node {d["node"]} &middot; 14.2001 Hz Phase-Locked</div>
  </div>
</body>
</html>
"""
        (forensics_dir / filename).write_text(page_html, encoding="utf-8")

    # Also build /forensics/usenet_1995_feed.html with inline RFC-1036 spools & verified links
    usenet_feed_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>USENET SPOOL // OCTOBER 1995 CHRONOLOGICAL DISPATCHES</title>
  <meta name="description" content="October 1995 Usenet Spool Feed — comp.dsp, alt.fan.nova-hart, alt.conspiracy, and federated nodes.">
  {STYLE}
</head>
<body>
  <div class="box">
    {FORENSICS_NAV}
    <h1>INN 1.4unoff3 // OCTOBER 1995 CHRONOLOGICAL USENET SPOOL</h1>
    <p>
      <strong>CANONICAL NEWSGROUP ARCHIVES:</strong>
      <a href="/usenet/index.html">All Newsgroups</a> &middot;
      <a href="/usenet/comp-dsp/index.html">comp.dsp</a> &middot;
      <a href="/usenet/alt-conspiracy/index.html">alt.conspiracy</a> &middot;
      <a href="/usenet/alt-fan-nova-hart/index.html">alt.fan.nova-hart</a> &middot;
      <a href="/usenet/alt-music-synth-pop/index.html">alt.music.synth-pop</a> &middot;
      <a href="/usenet/comp-sys-m68k/index.html">comp.sys.m68k</a>
    </p>

    <h2>[SPOOL #901 // comp.dsp] -0.94 Stereo Phase Correlation on Orion Reel SD-0009</h2>
    <pre>From: m.chen@ee.ashford-poly.org (Dr. Mei-Ling Chen)
Newsgroups: comp.dsp
Date: Thu, 12 Oct 1995 04:12:01 GMT
Message-ID: &lt;1995Oct12.041201.9912@ee.ashford-poly.org&gt;

We captured the calibration stem (rabbit_10_phase_inverted_hart_stem.mp3) on our
VAXstation 4000 at Ashford Polytechnic (Substation K-7704).
The 330/495/990 Hz triad on Ch-R is inverted 180.0 degrees relative to Ch-L (r = -0.94).
When you sum L+R to mono in the Signal Decoder Lab (/forensics/signal_lab.html),
the triad cancels by 42 dB and exposes a 750 Hz CW Morse bias inscription containing
the Sublevel B2 egress salt.</pre>

    <h2>[SPOOL #902 // alt.fan.nova-hart] VIS-1200Hz Scanline Bleed on 6925 kHz</h2>
    <pre>From: kenji_t@kamome-net.org (Kenji Takahashi // PC-9801RA)
Newsgroups: alt.fan.nova-hart
Date: Fri, 13 Oct 1995 11:08:44 GMT
Message-ID: &lt;1995Oct13.110844.1420@kamome-net.org&gt;

When the broadcast monitor logged [FAULT 0x08 // VIS-1200HZ RASTER] at 02:14 UTC,
we piped rabbit_08_sstv_b2_schematic.mp3 into our scanline rasterizer.
It drew a Sublevel B2 DMA Partition Map listing two specific GeoCities homestead
coordinates as memory anchors:
  Anchor A: tokyo-garden-1420
  Anchor B: siliconvalley-lab-1984
Plus a bottom register note: XOR -&gt; RELCOM.</pre>

    <h2>[SPOOL #903 // alt.conspiracy] Unacknowledged Bell-103 AX.25 Frame on 4625 kHz</h2>
    <pre>From: op08@relcom-node08.org (Dimitri V. // Leningrad AX.25 Relay)
Newsgroups: alt.conspiracy
Date: Sat, 14 Oct 1995 02:14:19 GMT
Message-ID: &lt;1995Oct14.021419.0808@relcom-node08.org&gt;

At 02:14 UTC on 4625.0 kHz, our TNC at Relcom Node-08 captured a 110-baud Bell-103
AFSK burst (1270 Hz mark / 1070 Hz space, archived as rabbit_09).
The UI frame carries a 1989 Sublevel B2 emergency egress header addressed to
ASHPOLY-07 specifying the 16-bit Feistel permutation mask.
Demodulate rabbit_09 in /forensics/signal_lab.html, then run:
  XOR &lt;ANCHOR_A&gt; &lt;ANCHOR_B&gt; &lt;MASK&gt;
in the VT100 Terminal (/forensics/index.html).</pre>

    <h2>[SPOOL #904 // alt.fan.nova-hart] Unlisted Reel SD-0010 ("Two Voices") on Sublevel B2 Bus</h2>
    <pre>From: elena@redcoyoacan.org (Elena Villalobos // Red Coyoacan Tape Exchange)
Newsgroups: alt.fan.nova-hart,comp.dsp
Date: Sat, 14 Oct 1995 09:10:04 GMT
Message-ID: &lt;1995Oct14.091004.7345@redcoyoacan.org&gt;

A tenth master reel just surfaced on the 24/7 satellite trunk: Reel SD-0010 ("Two Voices").
Unlike the solo studio takes from 1988, this recording carries two interleaved vocal
carriers separated by a 14.2001 Hz heterodyne offset.
When you load Button 4 ("ANALYZE REEL SD-0010: TWO VOICES") in /forensics/signal_lab.html
and engage [HARMONIC COUNTERPOINT LOCK (14.2 HZ)], the Lissajous X-Y vectorscope locks
onto the counterpoint runout key for Sector 6 in /forensics/index.html!</pre>

    <h2>[SPOOL #905 // alt.conspiracy,comp.dsp] Retrocausal Drift: 1983 "Crystal Promise" vs. June 2025 Q-Link</h2>
    <pre>From: m.chen@ee.ashford-poly.org (Dr. Mei-Ling Chen)
Newsgroups: alt.conspiracy,comp.dsp,alt.fan.nova-hart
Date: Sun, 15 Oct 1995 03:59:59 GMT
Message-ID: &lt;1995Oct15.035959.1983@ee.ashford-poly.org&gt;

Has anyone else examined the three newly unsealed Bureau of Harmony &amp; Orion Mainframe files?
  1. /forensics/anemoia_harmony.html (The 1979 Public Harmony Acts &amp; the 6 wiped Echoes)
  2. /forensics/fractal_marcus.html  (Project Akasaka JP-85-X &amp; the 4-node Fractal Marcus drift)
  3. /forensics/dead_hand_protocol.html (Luna Gray "The Patch", Dead-Hand, and the Q-Link)

When we engaged BOTH the Differential Phase Null AND the 14.2 Hz Counterpoint Lock at the
same time on Reel SD-0010 in /forensics/signal_lab.html, a 5th sub-harmonic channel opened
on the analyzer—showing Nova's Phase IV consciousness compressing out "The Heavy" and
looping backward into April 1983 while whispering "June 2025".
The end of the archive is the beginning of the archive. It's an Ouroboros.</pre>
    <div class="meta">INN 1.4unoff3 // Synchronized with 24/7 Broadcast Monitor (14.2001 Hz)</div>
  </div>
</body>
</html>
"""
    (forensics_dir / "usenet_1995_feed.html").write_text(usenet_feed_html, encoding="utf-8")

    # Ensure forensic audio files and live_telemetry.json are mirrored into site/forensics/
    import shutil
    repo_root = site_dir.parent
    for fname in (
        "rabbit_08_sstv_b2_schematic.mp3",
        "rabbit_09_bell103_relcom_packet.mp3",
        "rabbit_10_phase_inverted_hart_stem.mp3",
    ):
        src_audio = repo_root / "assets" / "audio" / "forensics" / fname
        if src_audio.exists():
            shutil.copy2(src_audio, forensics_dir / fname)
    tel_src = site_dir / "assets" / "live_telemetry.json"
    if tel_src.exists():
        shutil.copy2(tel_src, forensics_dir / "live_telemetry.json")

    print("[BUILD_FORENSICS_DOSSIERS] Generated 8 verified HTML pages + forensic assets in", forensics_dir)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    build_all(args.repo_root / "site")
