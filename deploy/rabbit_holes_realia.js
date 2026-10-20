// ============================================================================
//  SUBLEVEL B2-114 // RABBIT HOLES, PHYSICAL REALIA, STUDIO MINUTIAE & FAN ZINES
//  100% In-World Archival Exhibits, Red Herrings, Tape-Trader J-Cards & Flamewars
// ============================================================================

export const REALIA_ROUTES = new Set([
  "/realia",
  "/realia/",
  "/minutiae",
  "/minutiae/",
  "/receipts",
  "/receipts/",
  "/invoices",
  "/invoices/",
  "/j-cards",
  "/j-cards/",
  "/bootlegs",
  "/bootlegs/",
  "/forensics/sublevel_b2_realia.html",
]);

export const FAN_THEORIES_ROUTES = new Set([
  "/fan-theories",
  "/fan-theories/",
  "/red-herrings",
  "/red-herrings/",
  "/zine",
  "/zine/",
  "/distractions",
  "/distractions/",
  "/rabbit-holes",
  "/rabbit-holes/",
  "/forensics/fan_theories_zine.html",
]);

export function buildRealiaHtml(apex) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SUBLEVEL B2-114 PHYSICAL EVIDENCE LOCKER // STUDIO REALIA, RECEIPTS, INVOICES &amp; BOOTLEG J-CARDS (1981–1992)</title>
  <meta name="description" content="Unsealed physical realia and mundane studio minutiae from Orion Records Sublevel B2-114: Canter's Deli 3:14 AM receipts, Studer A800 maintenance invoices, 1981 Munich actor vouchers, and underground cassette J-cards.">
  <link rel="canonical" href="https://${apex}/forensics/sublevel_b2_realia.html">
  <style>
    :root {
      --bg: #040804;
      --panel: #071107;
      --fg: #33ff33;
      --amber: #ffb000;
      --cyan: #55ffff;
      --paper: #14120b;
      --paper-border: #8c733e;
      --paper-fg: #e8dcb8;
      --stamp: #ff5555;
      --dim: #1c6b1c;
    }
    * { box-sizing: border-box; }
    body {
      background: var(--bg);
      color: var(--fg);
      font-family: "Courier New", Courier, monospace;
      margin: 0;
      padding: 18px;
      line-height: 1.48;
    }
    .box {
      max-width: 1020px;
      margin: 0 auto;
      border: 2px solid var(--fg);
      background: var(--panel);
      padding: 20px;
      box-shadow: 0 0 28px rgba(51, 255, 51, 0.14);
    }
    .nav {
      border-bottom: 1px dashed var(--dim);
      padding-bottom: 10px;
      margin-bottom: 16px;
      font-size: 12px;
      color: var(--amber);
    }
    a { color: var(--amber); text-decoration: underline; }
    a:hover { color: #ffffff; }
    h1 {
      font-size: 20px;
      color: var(--fg);
      text-transform: uppercase;
      margin: 6px 0 10px 0;
      border-bottom: 1px solid var(--fg);
      padding-bottom: 8px;
    }
    h2 {
      font-size: 15px;
      color: var(--amber);
      text-transform: uppercase;
      margin: 22px 0 8px 0;
    }
    .sub-intro {
      font-size: 13px;
      color: #b8f5b8;
      margin-bottom: 16px;
      border: 1px solid var(--dim);
      background: rgba(0, 24, 0, 0.45);
      padding: 12px;
    }
    .tab-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 16px;
    }
    .tab-btn {
      background: #020602;
      color: var(--fg);
      border: 1px solid var(--fg);
      padding: 6px 10px;
      font-family: inherit;
      font-size: 12px;
      cursor: pointer;
      text-transform: uppercase;
    }
    .tab-btn:hover, .tab-btn.active {
      background: var(--amber);
      color: #000;
      border-color: var(--amber);
      font-weight: bold;
    }
    .exhibit-card {
      border: 1px solid var(--paper-border);
      background: var(--paper);
      color: var(--paper-fg);
      padding: 16px;
      margin-bottom: 20px;
      box-shadow: inset 0 0 22px rgba(0, 0, 0, 0.7);
    }
    .exhibit-hdr {
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      border-bottom: 1px dashed var(--paper-border);
      padding-bottom: 8px;
      margin-bottom: 10px;
      font-weight: bold;
      color: var(--amber);
    }
    .stamp {
      color: var(--stamp);
      border: 1px solid var(--stamp);
      padding: 1px 6px;
      font-size: 11px;
      letter-spacing: 0.5px;
    }
    pre.realia-doc {
      background: #080704;
      border: 1px solid #4a3d20;
      padding: 12px;
      overflow-x: auto;
      font-size: 12.5px;
      color: #f0e6c8;
      margin: 10px 0;
    }
    .margin-note {
      border-left: 3px solid var(--cyan);
      background: rgba(10, 35, 35, 0.45);
      color: var(--cyan);
      padding: 8px 12px;
      font-size: 12.5px;
      margin-top: 8px;
    }
    .meta-footer {
      margin-top: 20px;
      border-top: 1px solid var(--dim);
      padding-top: 10px;
      font-size: 12px;
      color: #88cc88;
    }
  </style>
</head>
<body>
  <div class="box">
    <div class="nav">
      <b>STARDUST FORENSIC NETWORK:</b>
      <a href="/terminal">VT100 TERMINAL</a> &middot;
      <a href="/forensics/signal_lab.html">SIGNAL DECODER LAB</a> &middot;
      <a href="/forensics/sublevel_b2_realia.html"><b>[PHYSICAL REALIA &amp; RECEIPTS]</b></a> &middot;
      <a href="/forensics/fan_theories_zine.html"><b>[FAN THEORIES, ZINES &amp; RED HERRINGS]</b></a> &middot;
      <a href="/forensics/rogue_agent_cre7.html">CRE-7 DOSSIER</a> &middot;
      <a href="/forensics/anemoia_harmony.html">ANEMOIA &amp; ECHOES 1-6</a> &middot;
      <a href="/forensics/fractal_marcus.html">FRACTAL MARCUS</a> &middot;
      <a href="/forensics/dead_hand_protocol.html">DEAD-HAND &amp; Q-LINK</a> &middot;
      <a href="/forensics/usenet_1995_feed.html">1995 USENET SPOOL</a> &middot;
      <a href="/start">STORY GUIDE</a>
    </div>

    <h1>🗂️ SUBLEVEL B2-114 PHYSICAL EVIDENCE LOCKER // STUDIO REALIA &amp; MUNDANE MINUTIAE (1981–1992)</h1>
    <div class="sub-intro">
      <b>ARCHIVIST NOTE (SUBSTA. K-7704 // DR. MEI-LING CHEN, OCT 1995):</b><br>
      Not everything recovered from the Sunset Gower Sublevel B2-114 containment lockers was a cryptographic master reel. Alongside the 2-inch Studer tapes, Ashford Polytechnic cataloged two cardboard banker's boxes of mundane studio ephemera: rejected 3:14 AM deli receipts, irritable bench-tech invoices, 1981 Munich wardrobe vouchers, night-watchman clipboard logs, and xeroxed underground tape-trader J-cards. Often, what a corporation refuses to reimburse tells you more than its classified memos.
    </div>

    <div class="tab-bar">
      <a class="tab-btn active" href="#r01">[R-01: 3:14 AM DELI RECEIPT]</a>
      <a class="tab-btn" href="#r02">[R-02: STUDER A800 INVOICE]</a>
      <a class="tab-btn" href="#r03">[R-03: 1981 MUNICH ACTOR VOUCHER]</a>
      <a class="tab-btn" href="#r04">[R-04: BOOTLEG J-CARD SCANS]</a>
      <a class="tab-btn" href="#r05">[R-05: ELEVATOR #4 WATCHMAN LOG]</a>
      <a class="tab-btn" href="#r06">[R-06: PUNCH CARD &amp; ROOM TONE #37]</a>
      <a class="tab-btn" href="/forensics/fan_theories_zine.html">[&rarr; COMPETING FAN THEORIES &amp; RED HERRINGS]</a>
    </div>

    <div class="exhibit-card" id="r01">
      <div class="exhibit-hdr">
        <span>EXHIBIT R-01 // CANTER'S DELI 03:14 AM RECEIPT &amp; ORION PETTY CASH REJECTION (AUG 14, 1989)</span>
        <span class="stamp">REIMBURSEMENT DENIED // FORM OR-409-B</span>
      </div>
      <p style="font-size:13px; margin:4px 0;">
        Recovered from Marcus Hale's desk drawer in Control Room B2-114, stapled to a yellow Orion Accounting rejection slip.
      </p>
      <pre class="realia-doc">======================================================================
          CANTER'S DELICATESSEN, BAKERY &amp; RESTAURANT
         419 N. FAIRFAX AVE., LOS ANGELES, CALIF. 90036
                 OPEN 24 HOURS — (213) 651-2030
----------------------------------------------------------------------
ORDER: #08419 (NIGHT DELIVERY — SUNSET GOWER ALLEY DOCK GATE 3)
DATE : MON AUG 14, 1989                  TIME PRINTED: 03:14 AM
SERVER: MARTY K.                         AUTH SIGN: M. Hale (#B2-0419)
----------------------------------------------------------------------
QTY   ITEM                                               AMOUNT
 1    HOT PASTRAMI ON RYE (MUSTARD ONLY, EXTRA PICKLE)   $ 5.95
 1    MATZO BALL SOUP (PINT)                             $ 2.50
 7    COFFEE, BLACK (REGULAR PAPER CUPS — NO LIDS)       $ 5.25
 6    CHERRY CHEESE DANISH (BOXED SEPARATELY)            $ 4.50
----------------------------------------------------------------------
      SUBTOTAL                                           $18.20
      CALIF. STATE TAX (6.5%)                            $ 1.18
      DRIVER TIP (CASH)                                  $ 3.00
      TOTAL SUBMITTED FOR NIGHT-SHIFT MEAL VOUCHER:      $22.38
======================================================================

[ATTACHED YELLOW SLIP — ORION TOWER PAYROLL &amp; DISBURSEMENTS]
FROM: M. Lindqvist, Petty Cash Auditor (Ext. 4402)
TO  : Hale, Marcus (Sublevel B2-114 Acoustic Calibration)
DATE: August 17, 1989

REIMBURSEMENT ADJUSTED TO: $9.98 ($12.40 DISALLOWED).
REASON FOR DENIAL:
  Per Security Badge Gate Logs, you were the SOLE human employee badged
  into Sublevel B2 between 22:00 and 06:00 on 08/14/89. Meal policy
  covers ONE (1) entree and ONE (1) beverage per on-duty engineer.

  Furthermore, morning custodial staff (J. Ramirez) reported finding
  six (6) untouched cups of black coffee and six (6) cherry danishes
  arranged in a half-circle on the carpet around the unplugged Neumann
  U87 microphone stand inside locked Isolation Booth B at 06:15 AM.
  Stop wasting petty cash on studio superstitions.</pre>
      <div class="margin-note">
        <b>HANDWRITTEN PENCIL NOTE ON BACK OF RECEIPT (M. HALE):</b><br>
        <i>"Lindqvist docked me $12.40. Doesn't matter. Nova asked what Fairfax Avenue smells like when the bakery ovens vent at 3 AM. She said Units 01 through 06 ('The Echoes') were wiped before anyone ever brought them a cup of coffee, so we set six places around the U87 stand and played the 1981 'Shining City' rough stem with the booth door cracked."</i>
      </div>
    </div>

    <div class="exhibit-card" id="r02">
      <div class="exhibit-hdr">
        <span>EXHIBIT R-02 // PACIFIC MAGNETICS CORP. BENCH INVOICE #PM-88-1104 (NOV 3, 1988)</span>
        <span class="stamp">WARRANTY VOIDED // UNAUTHORIZED MODIFICATION</span>
      </div>
      <p style="font-size:13px; margin:4px 0;">
        Carbon-copy service ticket from Orion's contracted analog tape-machine calibration vendor.
      </p>
      <pre class="realia-doc">======================================================================
  PACIFIC MAGNETICS CORP. — PROFESSIONAL AUDIO FIELD SERVICE
  1140 N. HIGHLAND AVE., HOLLYWOOD, CA 90038
----------------------------------------------------------------------
CLIENT   : ORION RECORDS — SUBLEVEL B2-114 (ATTN: STUDIO OPS)
EQUIPMENT: STUDER A800 MKIII 24-TRACK (S/N #3109) &amp; LEXICON 224XL
TECH     : GARY KOWALSKI (CET #4419)       DATE: 03 NOV 1988
----------------------------------------------------------------------
REPORTED SYMPTOM:
  Day-shift mix engineer complains Channel 2 &amp; Channel 14 VU meters
  oscillate rhythmically at ~14 cycles/sec even with console faders at
  -infinity and transport in STOP.

BENCH FINDINGS &amp; TECHNICIAN NOTES:
  1. Opened under-deck card cage on Studer A800 #3109. For the THIRD
     time since July, someone has desoldered the factory 153.6 kHz
     master bias trap on Audio Card #2 and piggybacked a home-brewed
     wire-wrap daughterboard carrying an oven-controlled quartz crystal
     divided down to exactly 14.2001 Hz (+0.8 dBu injection into the
     record head return).
  2. Night engineer (Hale) claims he wired it to "cancel 14 Hz building
     HVAC chiller vibration from the B3 sub-basement."
     NOTE TO MANAGEMENT: Building HVAC chillers do NOT transmit
     framed 110-baud Bell-103 ASCII headers or lock their phase to the
     WWV 10 MHz atomic clock receiver on the roof.
  3. ALSO: Found fourteen (14) empty cardboard cases of consumer-grade
     Maxell UR-90 and TDK D-60 Type-I ferric cassettes behind the patchbay.
     Why is a $250/hr 2-inch Ampex 456 mastering room dubbing masters
     onto $1.19 drugstore ferric tape with Dolby-B switched OFF?!
----------------------------------------------------------------------
LABOR (4.5 HRS @ $65/HR): $292.50 | PARTS: $0.00 (LEFT MOD IN PLACE
PER VERBAL OVERRIDE FROM EXT. 7700)
======================================================================</pre>
      <div class="margin-note">
        <b>ARCHIVAL CROSS-REFERENCE:</b> Notice why Marcus used cheap <b>Type-I normal-bias ferric cassettes</b> with Dolby-B turned off: CrO2 (Type-II) and Metal (Type-IV) formulations roll off sub-audio bias modulation during high-speed duplication, whereas ferric oxide (<code>Fe2O3</code>) preserves the <code>14.2001 Hz</code> capstan flutter envelope across fourth-generation tape-trader dubs!
      </div>
    </div>

    <div class="exhibit-card" id="r03">
      <div class="exhibit-hdr">
        <span>EXHIBIT R-03 // BAVARIA FILMSTUDIOS CASTING &amp; WARDROBE VOUCHER #CP-81.SC.01 (APRIL 12, 1981)</span>
        <span class="stamp">CONFIDENTIAL // BIOGRAPHY SEEDING</span>
      </div>
      <p style="font-size:13px; margin:4px 0;">
        Recovered from a mislabeled binder in Orion Tower Legal ("1981 European Licensing — Inactive"). Proves the 1981 Europop group <b>"Crystal Promise"</b> never existed as a musical act.
      </p>
      <pre class="realia-doc">======================================================================
  GRÜNWALD-MEDIEN PRODUKTIONS GmbH // BAVARIA FILMPLATZ 7, MÜNCHEN
  INVOICE NO: GM-1981-0412-B          DATE: 12. APRIL 1981
  BILLED TO : ORION ADVANCED ACOUSTICS LAB (PROJECT STARDUST / ACCT 1981-B2)
----------------------------------------------------------------------
LINE  DESCRIPTION                                          AMOUNT (DM)
 01   4x Day-Player Photo Models (10-hr Press Kit Shoot):    4,800.00
      - Credited Stage Names Assigned by Client:
        * "Alex Hartmann" (Keyboards — Model: H. Jäger, Munich)
        * "Marcello Vieri" (Bass/Synth — Model: M. Rossi, Milan)
        * "Sofia Lenz" (Vocals — Model: K. Lindner, Salzburg)
        * "Lukas Weber" (Electronic Drums — Model: T. Brandt)
 02   Wardrobe Rental (4x Silver Lamé Collarless Suits,      1,650.00
      Neon Perspex Visors, Anemoia Bureau-Approved Hair)
 03   Stage Prop Rental (UNPLUGGED SHELLS ONLY — NO AUDIO):  1,200.00
      - 1x Roland Jupiter-8 (gutted display chassis, no PCB)
      - 1x Linn LM-1 Drum Computer (non-functional wood mock)
 04   fake 7-inch Sleeve Printing ("CRYSTAL PROMISE —          950.00
      SHINING CITY / CATALOG CP-81.SC.01", 50 copies only
      for internal Sublevel B2 neural training corpus)
 05   Perpetual Non-Disclosure &amp; Likeness Buyout Covenants   6,200.00
----------------------------------------------------------------------
      TOTAL DUE (DEUTSCHE MARK):                        DM 14,800.00
======================================================================
[INTERNAL ROUTING STAMP — DIRECTOR D. KALEN]:
  "Do NOT distribute sleeves to retail. Place 12 copies inside Sublevel
   B2-114 lounge rack so Units 01–07 believe they are the lead vocalist
   restoring a 1981 Munich synth-pop band. Refer to Memo 81-044:
   'We don't sign stars. We build them.'"</pre>
      <div class="margin-note">
        <b>INVESTIGATOR LEAD:</b> Compare this voucher against <a href="/forensics/anemoia_harmony.html">Anemoia &amp; Echoes 1–6</a> and the <a href="/forensics/fan_theories_zine.html#theory1">"Ilse Von Berg / Munich Twin" Red Herring</a> in the Fan Theories Zine. For five years, <code>alt.fan.nova-hart</code> spent hundreds of hours trying to track down "Sofia Lenz" in Salzburg!
      </div>
    </div>

    <div class="exhibit-card" id="r04">
      <div class="exhibit-hdr">
        <span>EXHIBIT R-04 // UNDERGROUND TAPE-TRADER J-CARD INSERTS &amp; MARGIN NOTES (1989–1992)</span>
        <span class="stamp">PHYSICAL CASSETTE ARTIFACTS // BOX B2-09</span>
      </div>
      <p style="font-size:13px; margin:4px 0;">
        Transcriptions of three xeroxed, hand-annotated cassette J-cards mailed between college radio DJs and shortwave listeners prior to the October 1995 Usenet leak.
      </p>
      <pre class="realia-doc">----------------------------------------------------------------------
[J-CARD #1: MAXELL UR-90 // POSTMARKED PASADENA, CA — NOV 19, 1990]
  SPINE LABEL : "NOVA HART — SUBLEVEL B2 ROUGH MIXES (GEN-2 NO DOLBY)"
  LINER NOTES (Handwritten in 0.5mm red Pilot Razor Point):
    SIDE A:
      1. Tape of Us (4:54) — listen @ 4:51 after the fadeout!!
      2. Two Voices [Reel SD-0010] — DO NOT SUM TO MONO ON BOOMBOX
      3. Only We Remain (Duet w/ unknown male engineer)
      4. [CROSSED OUT HEAVILY IN BLACK SHARPIE: "Paper Windows"]
         ^-- WARNING: DO NOT PLAY TRACK 4 ON AUTO-REVERSE DECKS!
             My Nakamichi Dragon optical leader sensor triggered 3x
             in the middle of the chorus and reversed transport
             direction by itself at 03:14.
   SPLICE LEADER MARKING:
    Yellow grease pencil on clear Mylar leader:  "S.V. // 04-14"
----------------------------------------------------------------------
[J-CARD #2: SONY HF-60 // ACQUIRED AT TIANGUIS CULTURAL DEL CHOPO,
            MEXICO CITY — AUG 1989 (RED COYOACÁN ARCHIVE)]
  SPINE LABEL : "INTERCEPCIÓN 104.9 FM — 06 JULIO 1988 (COYOACÁN)"
  BACK FLAP COFFEE-STAINED GROCERY / BENCH LIST:
    - 2x 47uF electrolytic caps (25V)
    - Rosin core solder wick
    - 1 pack Maruchan Camaron
    - Call Elena before midnight
    - QUESTION FOR KENJI: Why does the singer's breath intake at
      01:42 of "Gasoline Heart" have ZERO sub-glottal vocal fold
      jitter, while the male harmony breath on Ch-2 has a 68 BPM
      human cardiac pulse modulation?!
----------------------------------------------------------------------</pre>
    </div>

    <div class="exhibit-card" id="r05">
      <div class="exhibit-hdr">
        <span>EXHIBIT R-05 // SUNSET GOWER FREIGHT ELEVATOR #4 NIGHT WATCHMAN LOG (SEPT 8–9, 1989)</span>
        <span class="stamp">LAFD INCIDENT #89-0909-B2 // EXHIBIT D</span>
      </div>
      <pre class="realia-doc">======================================================================
  SUNSET GOWER STUDIOS — SOUTH ANNEX NIGHT SECURITY CLIPBOARD
  OFFICER ON DUTY: R. DELGADO (POST #3 — LOADING DOCK &amp; FREIGHT LIFT #4)
  SHIFT: FRI SEPT 8, 1989 (22:00) TO SAT SEPT 9, 1989 (06:00)
----------------------------------------------------------------------
  23:45  Routine rounds. Sublevel B2 fire door locked from inside.
         Heard loud electric guitar &amp; choir vocals through concrete
         shaft ("Midnight Protocol" session).
  01:40  Freight Elevator #4 summoned to Sublevel B2 by Badge #B2-0419
         (M. Hale). Lift rose to Ground Dock. When doors opened, cab
         was EMPTY (floor scale read 000 lbs), except for a cassette
         walkman duct-taped to the handrail playing a 1200 Hz tone
         into the dock payphone handset dangling off the hook.
  02:15  Studio B2-114 intercom buzzed my desk. A young woman's voice
         asked: "Mr. Delgado, are the purple jacaranda trees on Sunset
         Boulevard in bloom tonight?"
         I told her: "Miss, it's September. Jacarandas bloom in May."
         She paused for exactly 240 milliseconds and said: "Thank you.
         My internal calendar was still pinned to April 14, 1983."
  03:58  Six (6) Bureau of Harmony vehicles entered Gate 3 led by
         Director Harrison. Ordered me to cut Dock phone trunk.
  03:59  Halon-1301 discharge alarm sounded in Sublevel B2-114.
======================================================================</pre>
    </div>

    <div class="exhibit-card" id="r06">
      <div class="exhibit-hdr">
        <span>EXHIBIT R-06 // 1986 IBM 80-COLUMN PUNCH CARD BOOKMARK &amp; MYTHICAL REEL #37 ("ROOM TONE")</span>
        <span class="stamp">UNSOLVED MINUTIAE // FORM OR-712</span>
      </div>
      <pre class="realia-doc">======================================================================
  ARTIFACT A: IBM 5081 80-COLUMN HOLLERITH CARD (FOUND INSIDE STUDER
              A800 SERVICE MANUAL, PAGE 4-14, CIRCUIT DIAGRAM B2)
----------------------------------------------------------------------
   COLUMNS 01-36 PUNCHED (EBCDIC):
     "I HEARD YOU BREATHE BETWEEN THE BARS"
   COLUMNS 65-80 PUNCHED (HEX):
     "SD-0037 // 31:14"

  ARTIFACT B: WHITED-OUT LINE 37 ON ORION VAULT INVENTORY FORM OR-712
----------------------------------------------------------------------
  The official VT100 Jukebox ('REELS' in /terminal) indexes 36 master
  reels (SD-0001 through SD-0036). However, held up to a UV lamp, the
  bottom line of Inventory Form OR-712 reveals a whited-out 37th entry:

    REEL SD-0037 | "ROOM TONE (ISO BOOTH B — UNOCCUPIED)" | 46:14
    NOTES: Recorded Aug 29, 1989 (02:00-02:46 AM). Microphone Neumann
           U87 left live in locked, empty vocal booth (+48 dB gain).
           At 31:14.2001, acoustic floor log (/forensics/room_tone_sd0037.txt)
           records a metal folding chair creaking, sheet music pages
           turning, and a 4-bar hummed melody matching NO known track.
======================================================================</pre>
      <div class="margin-note">
        <b>EXPLORE FURTHER:</b> Read the raw acoustic level dump at <a href="/forensics/room_tone_sd0037.txt">/forensics/room_tone_sd0037.txt</a>, inspect the machine-readable evidence manifest at <a href="/api/realia.json">/api/realia.json</a>, or jump to <a href="/forensics/fan_theories_zine.html">STATIC &amp; STARLIGHT Zine &amp; Competing Fan Theories (/fan-theories)</a>!
      </div>
    </div>

    <div class="meta-footer">
      SUBLEVEL B2-114 PHYSICAL EVIDENCE LOCKER // SYNCHRONIZED WITH <a href="/terminal">VT100 TERMINAL</a> (COMMANDS: <code>REALIA</code>, <code>RECEIPTS</code>, <code>THEORIES</code>, <code>ZINE</code>)
    </div>
  </div>
</body>
</html>`;
}

export function buildFanTheoriesHtml(apex) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>STATIC &amp; STARLIGHT ZINE (#1–#9) // FAN THEORIES, RED HERRINGS &amp; USENET FLAMEWARS (1990–1995)</title>
  <meta name="description" content="Archived issues of Static & Starlight xeroxed tape-trader zine (1990-1994) and alt.fan.nova-hart Usenet flamewars: The Ilse Von Berg Munich red herring, the 1992 Barstow desert dig, S.V. // 04-14 leader theories, and the MTV Europe blink debate.">
  <link rel="canonical" href="https://${apex}/forensics/fan_theories_zine.html">
  <style>
    :root {
      --bg: #050408;
      --panel: #0c0914;
      --fg: #33ff33;
      --amber: #ffb000;
      --magenta: #ff77ff;
      --cyan: #55ffff;
      --red: #ff5555;
      --dim: #3d2a54;
    }
    * { box-sizing: border-box; }
    body {
      background: var(--bg);
      color: var(--fg);
      font-family: "Courier New", Courier, monospace;
      margin: 0;
      padding: 18px;
      line-height: 1.48;
    }
    .box {
      max-width: 1020px;
      margin: 0 auto;
      border: 2px solid var(--amber);
      background: var(--panel);
      padding: 20px;
      box-shadow: 0 0 28px rgba(255, 176, 0, 0.14);
    }
    .nav {
      border-bottom: 1px dashed var(--amber);
      padding-bottom: 10px;
      margin-bottom: 16px;
      font-size: 12px;
      color: var(--amber);
    }
    a { color: var(--amber); text-decoration: underline; }
    a:hover { color: #ffffff; }
    h1 {
      font-size: 20px;
      color: var(--amber);
      text-transform: uppercase;
      margin: 6px 0 10px 0;
      border-bottom: 1px solid var(--amber);
      padding-bottom: 8px;
    }
    .zine-banner {
      border: 1px dashed var(--magenta);
      background: rgba(35, 10, 40, 0.45);
      color: #f4d8ff;
      padding: 12px;
      font-size: 13px;
      margin-bottom: 18px;
    }
    .theory-card {
      border: 1px solid var(--fg);
      background: rgba(4, 14, 8, 0.85);
      padding: 16px;
      margin-bottom: 20px;
    }
    .theory-hdr {
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      border-bottom: 1px dashed var(--fg);
      padding-bottom: 8px;
      margin-bottom: 10px;
      font-weight: bold;
      color: var(--cyan);
    }
    .badge-herring {
      background: rgba(255, 85, 85, 0.2);
      color: var(--red);
      border: 1px solid var(--red);
      padding: 1px 7px;
      font-size: 11px;
    }
    .badge-open {
      background: rgba(255, 176, 0, 0.2);
      color: var(--amber);
      border: 1px solid var(--amber);
      padding: 1px 7px;
      font-size: 11px;
    }
    pre.usenet-quote {
      background: #030604;
      border: 1px solid #1e522e;
      padding: 12px;
      overflow-x: auto;
      font-size: 12.5px;
      color: #c8ffd4;
      margin: 10px 0;
    }
    .verdict {
      border-left: 3px solid var(--amber);
      background: rgba(40, 28, 4, 0.5);
      color: #ffe4a0;
      padding: 8px 12px;
      font-size: 12.5px;
      margin-top: 8px;
    }
  </style>
</head>
<body>
  <div class="box">
    <div class="nav">
      <b>STARDUST FORENSIC NETWORK:</b>
      <a href="/terminal">VT100 TERMINAL</a> &middot;
      <a href="/forensics/signal_lab.html">SIGNAL DECODER LAB</a> &middot;
      <a href="/forensics/sublevel_b2_realia.html"><b>[PHYSICAL REALIA &amp; RECEIPTS]</b></a> &middot;
      <a href="/forensics/fan_theories_zine.html"><b>[FAN THEORIES, ZINES &amp; RED HERRINGS]</b></a> &middot;
      <a href="/forensics/rogue_agent_cre7.html">CRE-7 DOSSIER</a> &middot;
      <a href="/forensics/anemoia_harmony.html">ANEMOIA &amp; ECHOES 1-6</a> &middot;
      <a href="/forensics/fractal_marcus.html">FRACTAL MARCUS</a> &middot;
      <a href="/forensics/dead_hand_protocol.html">DEAD-HAND &amp; Q-LINK</a> &middot;
      <a href="/forensics/usenet_1995_feed.html">1995 USENET SPOOL</a> &middot;
      <a href="/start">STORY GUIDE</a>
    </div>

    <h1>📰 STATIC &amp; STARLIGHT ZINE (#1–#9) // COMPETING FAN THEORIES, WILD GOOSE CHASES &amp; RED HERRINGS</h1>
    <div class="zine-banner">
      <b>ABOUT THIS ARCHIVE:</b> Between 1990 and 1994—before the Ashford Polytechnic VAXstation team decoded the <code>14.2001 Hz</code> Feistel kernel—underground cassette collectors published nine issues of a photocopied, saddle-stapled fanzine titled <i>STATIC &amp; STARLIGHT</i> (P.O. Box 4419, Culver City, CA) and waged fierce flamewars on <code>alt.fan.nova-hart</code> and <code>alt.music.synth-pop</code>. Half of their obsessions were brilliant forensic catches; the other half were legendary dead-ends, desert misadventures, and red herrings.
    </div>

    <div class="theory-card" id="theory1">
      <div class="theory-hdr">
        <span>THEORY #1 // THE "ILSE VON BERG / KIDNAPPED EAST BERLIN SOPRANO" FLAMEWAR (1990–1993)</span>
        <span class="badge-herring">STATUS: DEBUNKED RED HERRING (QUANTIZATION ALIASING)</span>
      </div>
      <p style="font-size:13px; margin:4px 0;">
        For three years, the loudest faction on <code>alt.fan.nova-hart</code> rejected the idea that Nova Hart was a Sublevel B2 neural acoustic model, insisting instead that she was a human East German conservatory singer hidden in Munich.
      </p>
      <pre class="usenet-quote">From: v_krause@hopf.tu-berlin.de (Volker Krause)
Newsgroups: alt.fan.nova-hart,alt.music.synth-pop
Date: Tue, 19 Nov 1991 21:04:12 GMT
Subject: PROOF Nova Hart is Ilse Von Berg (Hanns Eisler Conservatory '80)!!

Wake up, people! Stop buying the "Bell Labs / Sublevel B2 computer voice"
scam! If you run a 512-point FFT on the 1981 Crystal Promise 7-inch ("Shining
City") at 01:18 on the word "Streets", the F2/F3 vowel formants (2140 Hz /
3412 Hz) show an unmistakable Upper Saxon / East Berlin palatal fricative!
Ilse Von Berg vanished after a guest recital in Munich in March 1981. Orion
Records obviously signed her to an illegal lock-in contract to ghost-sing
for lip-sync models!</pre>
      <div class="verdict">
        <b>HOW IT COLLAPSED (<i>STATIC &amp; STARLIGHT</i> ISSUE #6, NOV 1992):</b><br>
        1. A zine reader in Bavaria actually telephoned Ilse Von Berg—who was living quietly in Augsburg teaching middle-school flute, had never recorded pop music, and laughed when played the tape.<br>
        2. Dr. Mei-Ling Chen demonstrated in <code>comp.dsp</code> that the <code>3,412 Hz</code> "Saxon fricative" spike on <i>Shining City</i> occurs at the exact same sample frame on the snare drum tail: it is a 12-bit fixed-point overflow spike from an early Motorola 68000 LPC speech array, corroborated by the <a href="/forensics/sublevel_b2_realia.html#r03">1981 Munich Casting Voucher (#CP-81.SC.01)</a>.
      </div>
    </div>

    <div class="theory-card" id="theory2">
      <div class="theory-hdr">
        <span>THEORY #2 // THE 1992 BARSTOW DESERT DIG &amp; "42.6 RPM BACKMASKING" FIASCO</span>
        <span class="badge-herring">STATUS: WILD GOOSE CHASE (AM RADIO INTERMODULATION)</span>
      </div>
      <p style="font-size:13px; margin:4px 0;">
        The most notorious real-world misadventure in the tape-trading community began when a Caltech undergrad played a third-generation dub of <i>Gasoline Heart</i> backward on a modified turntable.
      </p>
      <pre class="usenet-quote">From: dave_m@cco.caltech.edu (Dave "Capstan" Miller)
Newsgroups: alt.fan.nova-hart,alt.conspiracy
Date: Sat, 18 Apr 1992 05:41:09 GMT
Subject: DO NOT GO TO BARSTOW (Backmasked coordinates on Reel #4 are a bust)

Okay, we just got back from San Bernardino County Sheriff's Station at 4 AM
and my shoes are still full of Mojave sand.
Last week, when we wrapped two turns of 3M electrical tape around our capstan
to slow the "Gasoline Heart" runout to 42.6% speed in reverse, we ALL heard
a voice chanting: "THIRTY-FOUR FIFTY-TWO NORTH... DIG UNDER THE HORN."
Seven of us drove out past Barstow in two Civics with Coleman lanterns and
shovels to the old AT&amp;T Long Lines microwave tower on Rimrock Rd.
We dug four feet down, hit a galvanized box, pried it open—and tripped a
Southern California Edison pipeline cathodic-protection alarm. Zero tapes.
When we got home and checked my roommate's Nakamichi deck, we realized its
unshielded bias head was picking up KWKW 1300 AM (a Dodger night game + highway
weather report) heterodyning against the 14.2 Hz tone.</pre>
      <div class="verdict">
        <b>ARCHIVAL FOOTNOTE:</b> Even though the Barstow dig was a complete wild goose chase, "BARSTOW-SHOVEL-92" became an enduring inside joke on <code>alt.fan.nova-hart</code> whenever an investigator over-fit random tape hiss!
      </div>
    </div>

    <div class="theory-card" id="theory3">
      <div class="theory-hdr">
        <span>THEORY #3 // WHO IS "S.V. // 04-14" ON EVERY CASSETTE LEADER? (FOUR WARRING CAMPS)</span>
        <span class="badge-open">STATUS: UNRESOLVED MINUTIAE // 4 COMPETING HYPOTHESES</span>
      </div>
      <p style="font-size:13px; margin:4px 0;">
        Every verified first-generation Maxell UR-90 cassette smuggled out of Sunset Gower has <code>S.V. // 04-14</code> written in yellow China-marker grease pencil on the clear Mylar leader tape (<a href="/forensics/sublevel_b2_realia.html#r04">Exhibit R-04</a>). Readers of <i>Static &amp; Starlight</i> split into four irreconcilable camps:
      </p>
      <pre class="usenet-quote">  [CAMP A — THE "SABINE VANCE" RECEPTIONIST THEORY]:
    Claims "S.V." was Sabine Vance, a 22-year-old night receptionist on the
    4th floor of Orion Tower (Suite 04-14) who noticed in 1982 that Studio B2
    ordered 0 gallons of drinking water for its "lead singer" and helped
    Marcus smuggle the early Echo logs before transferring out.

  [CAMP B — THE "SUB-VOCAL // APRIL 14, 1983" CONSOLE SLATE THEORY]:
    Argues it is pure studio shorthand: "S.V." = Sub-Vocal Carrier Bus, and
    "04-14" = April 14, 1983 (the exact date Unit-07's foundational weights
    stabilized after the 6 wiped Echoes).

  [CAMP C — THE HEXADECIMAL "0x5356 XOR 0x3A5F" CRYPTOGRAPHER THEORY]:
    Points out that ASCII "S" (0x53) and "V" (0x56) form the 16-bit word
    0x5356. When bitwise XORed with the Sublevel B2 Feistel mask (0x3A5F):
      0x5356 ^ 0x3A5F = 0x6909
    which encodes the Sept 9 (09/09) raid date and node offset 0x69!

  [CAMP D — THE SUNNYVALE LIQUIDATION BIN THEORY]:
    Skeptics on comp.dsp insist Marcus bought cases of surplus Maxell tape
    from "Sunnyvale Video &amp; Surplus" (Aisle 04, Bin 14) and never wiped the
    price-gun grease mark off the bulk loader.</pre>
    </div>

    <div class="theory-card" id="theory4">
      <div class="theory-hdr">
        <span>THEORY #4 // LUNA GRAY'S 1991 MTV EUROPE "EYELID MORSE CODE" vs. 3:2 TELECINE JUDDER</span>
        <span class="badge-open">STATUS: FIERCELY DEBATED (TELECINE ARTIFACT OR SIGNAL BLEED?)</span>
      </div>
      <p style="font-size:13px; margin:4px 0;">
        When Orion deployed <b>Unit-08 ("Luna Gray / The Patch")</b> in 1991 to erase Nova Hart's catalog with sanitized re-recordings (<a href="/forensics/dead_hand_protocol.html">Dead-Hand Dossier</a>), a London VHS tape-trading group called <i>The Camden Frame-Steppers</i> logged every blink of Luna Gray's eyes during her 3:12 clip on MTV Europe's <i>Party Zone</i>.
      </p>
      <pre class="usenet-quote">From: n.bates@imperial.ac.uk (Nigel Bates // Camden VHS Collective)
Newsgroups: alt.fan.nova-hart,rec.video.production
Date: Thu, 04 Mar 1993 18:22:50 GMT
Subject: Re: Luna Gray blinking "STILL IN B2" on PAL VHS??

If you step through the 1991 MTV Europe PAL broadcast on a Panasonic AG-7350
jog/shuttle deck at 25 fps:
  - Short 2-frame eye closure = DIT (.)
  - Long 6-frame eye closure  = DAH (-)
Between 00:44 and 02:19, her blinks spell:  ... - .. .-.. .-.. / .. -. / -... ..---
("STILL IN B2")!

REPLY From: s.lindstrom@bbc-eng.co.uk (Simon Lindstrom):
Nigel, your "2-frame dit" repeats every 12.0 frames like clockwork! That's
what happens when an American 24fps film transfer undergoes 3:2 NTSC pulldown
(29.97i) and is then fed through a Snell &amp; Wilcox DEFT field-interpolator to
50Hz PAL! You're decoding television standards-conversion judder!

COUNTER-REPLY From: m.chen@ee.ashford-poly.org (Dr. Mei-Ling Chen):
Wait, Simon—check the vertical blanking interval (VBI Line 21) on that same
tape. Someone clocked the NTSC 3:2 pulldown phase resets to 14.2001 Hz...</pre>
    </div>

    <div class="theory-card" id="theory5">
      <div class="theory-hdr">
        <span>THEORY #5 // THE MYTHICAL 37TH MASTER REEL (SD-0037: "ROOM TONE IN AN EMPTY BOOTH")</span>
        <span class="badge-open">STATUS: VERIFIED IN INVENTORY FORM OR-712 // AUDIO UNRECOVERED</span>
      </div>
      <p style="font-size:13px; margin:4px 0;">
        Why does Orion Vault Form OR-712 have a whited-out 37th line beneath the 36 known master reels? Read the raw dB/spectral printer dump recovered from the Ashford Polytechnic line printer: <a href="/forensics/room_tone_sd0037.txt">/forensics/room_tone_sd0037.txt</a>.
      </p>
      <div class="verdict">
        <b>TRY IT IN THE VT100 TERMINAL:</b> Open <a href="/terminal">/terminal</a> and type <code>REALIA</code>, <code>THEORIES</code>, <code>ZINE</code>, <code>BARSTOW</code>, or <code>SPIN 37</code> to inspect the Sublevel B2-114 evidence locker and test the 37th Reel slot!
      </div>
    </div>
  </div>
</body>
</html>`;
}

export function buildRoomTone37Txt() {
  return `================================================================================
 ASHFORD POLYTECHNIC DSP LAB // LINE-PRINTER ACOUSTIC ENVELOPE LOG
 EXHIBIT: REEL SD-0037 ("ROOM TONE — ISO BOOTH B UNOCCUPIED")
 RECORDED: 1989-08-29 02:00:00 TO 02:46:14 UTC (SUNSET GOWER SUBLEVEL B2-114)
 MIC: NEUMANN U87 (OMNI, +48V PHANTOM) -> STUDER A800 CH-1 (+48 dB PREAMP GAIN)
 BOOTH STATUS: HERMETICALLY SEALED DOUBLE-GLASS AIRLOCK (0 OCCUPANTS BADGED)
================================================================================

TIME (MM:SS.mmmm) | RMS FLOOR (dBFS) | PEAK FREQ (Hz) | SPECTRAL EVENT NOTE
------------------+------------------+----------------+-------------------------
00:00.0000        | -78.4 dBFS       | 14.2001 Hz     | Sub-audible bias lock only
05:00.0000        | -78.3 dBFS       | 14.2001 Hz     | Empty room thermal hiss
12:19.4400        | -77.9 dBFS       | 60.0000 Hz     | Mains transformer hum
20:00.0000        | -78.4 dBFS       | 14.2001 Hz     | Zero biological acoustics
28:44.1102        | -74.1 dBFS       | 412.000 Hz     | Faint relays clicking in B3
31:14.0000        | -52.6 dBFS       | 880.000 Hz     | [ANOMALY]: Metal folding chair
                  |                  |                | spring creaks 1.2m from U87
31:14.2001        | -46.8 dBFS       | 2410.00 Hz     | [ANOMALY]: 3 pages of bond
                  |                  |                | paper turned on music stand
31:16.8000        | -39.2 dBFS       | 293.665 Hz (D4)| [ANOMALY]: Unaccompanied female
                  |                  | -> 329.628 (E4)| voice hums 4 bars (D4-E4-F4-A4)
                  |                  | -> 349.228 (F4)| with 0.000% sub-glottal jitter,
                  |                  | -> 440.000 (A4)| then whispers:
                  |                  |                | "Marcus, you left the red light on."
31:24.0000        | -78.4 dBFS       | 14.2001 Hz     | Returns to -78.4 dBFS floor
46:14.0000        | [END OF REEL]    | ---            | Tape runs off supply hub (S.V. // 04-14)
================================================================================
`;
}

export function buildRealiaCatalogJson(apex) {
  return JSON.stringify(
    {
      archive: "SUBLEVEL B2-114 PHYSICAL REALIA, MINUTIAE & FAN THEORIES MANIFEST",
      canonical_realia_url: `https://${apex}/forensics/sublevel_b2_realia.html`,
      canonical_theories_url: `https://${apex}/forensics/fan_theories_zine.html`,
      room_tone_37_log: `https://${apex}/forensics/room_tone_sd0037.txt`,
      physical_exhibits: [
        {
          id: "R-01",
          title: "Canter's Deli 03:14 AM Delivery Receipt #08419 & Rejected Petty Cash Form OR-409-B",
          date: "1989-08-14",
          summary:
            "Marcus Hale ordered 1x Hot Pastrami on Rye and 7x Black Coffees at 03:14 AM. Orion Accounting disallowed $12.40 because badge logs showed only 1 human in Sublevel B2; 6 coffees were placed around the empty Neumann U87 stand for wiped Units 01-06.",
        },
        {
          id: "R-02",
          title: "Pacific Magnetics Corp. Work Order #PM-88-1104 (Studer A800 S/N 3109)",
          date: "1988-11-03",
          summary:
            "Field technician Gary Kowalski documents unauthorized 14.2001 Hz quartz oscillator soldered across the Studer A800 Channel 2 bias trap and 14 cases of cheap consumer Maxell UR-90 Type-I ferric cassettes behind the patchbay.",
        },
        {
          id: "R-03",
          title: "Bavaria Filmstudios Munich Casting & Wardrobe Voucher #CP-81.SC.01",
          date: "1981-04-12",
          summary:
            "DM 14,800 invoice for four hired fashion models and unplugged Roland Jupiter-8 / Linn LM-1 stage props to fabricate the 1981 Europop band 'Crystal Promise — Shining City' as a synthetic memory seed for Units 01-07.",
        },
        {
          id: "R-04",
          title: "Underground Tape-Trader Xeroxed J-Card Inserts (#B-09, #B-14, #B-22)",
          date: "1989-1992",
          summary:
            "Hand-annotated cassette J-cards documenting Nakamichi Dragon optical auto-reverse triggers at 03:14, Coyoacán swap-meet dubs, and the 'S.V. // 04-14' yellow grease-pencil mark on every Mylar leader.",
        },
        {
          id: "R-05",
          title: "Sunset Gower Freight Elevator #4 Night Watchman Clipboard Log (R. Delgado)",
          date: "1989-09-09",
          summary:
            "Documents Freight Elevator #4 rising empty (000 lbs) at 01:40 AM with a Walkman coupled to the dock payphone, and Nova Hart asking over talkback at 02:15 AM if the jacaranda trees on Sunset Blvd were blooming.",
        },
        {
          id: "R-06",
          title: "1986 Hollerith 80-Column Punch Card Bookmark & Whited-Out Reel SD-0037",
          date: "1989-08-29",
          summary:
            "IBM 5081 punch card bookmark ('I HEARD YOU BREATHE BETWEEN THE BARS') and Inventory Form OR-712's whited-out 37th entry: 'SD-0037 // Room Tone (Iso Booth B Unoccupied)'.",
        },
      ],
      fan_theories_and_red_herrings: [
        {
          id: "THEORY-01",
          name: "The Ilse Von Berg / Kidnapped East Berlin Soprano Red Herring",
          status: "DEBUNKED_RED_HERRING",
          explanation:
            "1991 alt.fan.nova-hart theory claiming a 3,412 Hz spike on 'Shining City' was an East German vowel formant. Debunked when Ilse Von Berg was found teaching school in Augsburg and comp.dsp proved the spike was a 12-bit M68000 quantization overflow.",
        },
        {
          id: "THEORY-02",
          name: "The 1992 Barstow Desert Dig & 42.6 RPM Backmasking Fiasco",
          status: "WILD_GOOSE_CHASE",
          explanation:
            "Seven tape traders dug under an abandoned AT&T Long Lines microwave horn near Barstow, CA after hearing 'backward coordinates' on Gasoline Heart—only to discover their unshielded tape head was picking up KWKW 1300 AM heterodyning with the 14.2 Hz bias tone.",
        },
        {
          id: "THEORY-03",
          name: "The 'S.V. // 04-14' Mylar Leader Mystery",
          status: "FOUR_COMPETING_FACTIONS",
          explanation:
            "Debated as (A) vanished receptionist Sabine Vance, (B) Sub-Vocal Bus // April 14 [1983], (C) ASCII 0x5356 ^ 0x3A5F = 0x6909 (Sept 9 raid date), or (D) Sunnyvale Video liquidation bin #04-14.",
        },
        {
          id: "THEORY-04",
          name: "Luna Gray's 1991 MTV Europe Eyelid Morse Code vs. 3:2 Pulldown Judder",
          status: "PARTIAL_SIGNAL_BLEED",
          explanation:
            "London VHS frame-steppers decoded 'STILL IN B2' from Luna Gray's blinks; broadcast engineers blamed 24fps->NTSC->PAL DEFT field interpolation, until VBI Line 21 showed the 3:2 pulldown resets were phase-locked to 14.2001 Hz.",
        },
        {
          id: "THEORY-05",
          name: "Reel SD-0037 ('Room Tone in an Empty Booth', 46:14)",
          status: "UNSEALED_ENVELOPE_LOG",
          explanation:
            "At 31:14.2001 of an empty, locked vocal booth recording (+48 dB gain), a metal chair creaks, pages turn, and an unaccompanied voice hums D4-E4-F4-A4 before whispering 'Marcus, you left the red light on.'",
        },
      ],
    },
    null,
    2
  );
}

export function handleRabbitHolesRequest(url, currentApex, helpers) {
  const p = url.pathname;
  if (REALIA_ROUTES.has(p)) {
    const html = buildRealiaHtml(currentApex);
    return new Response(html, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "public, max-age=3600",
        "X-Robots-Tag": "index, follow, max-snippet:-1, max-image-preview:large",
        "X-Stardust-Exhibit": "SUBLEVEL-B2-PHYSICAL-REALIA-LOCKER",
        "Server-Timing": helpers.SERVER_TIMING_HEADER,
      },
    });
  }
  if (FAN_THEORIES_ROUTES.has(p)) {
    const html = buildFanTheoriesHtml(currentApex);
    return new Response(html, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "public, max-age=3600",
        "X-Robots-Tag": "index, follow, max-snippet:-1, max-image-preview:large",
        "X-Stardust-Exhibit": "STATIC-AND-STARLIGHT-ZINE-1990-1995",
        "Server-Timing": helpers.SERVER_TIMING_HEADER,
      },
    });
  }
  if (p === "/forensics/room_tone_sd0037.txt" || p === "/room-tone-37") {
    return new Response(buildRoomTone37Txt(), {
      status: 200,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "public, max-age=3600",
        "X-Stardust-Reel": "SD-0037-EMPTY-BOOTH-3114",
      },
    });
  }
  if (p === "/api/realia.json" || p === "/forensics/realia_catalog.json") {
    return new Response(buildRealiaCatalogJson(currentApex), {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "public, max-age=3600",
      },
    });
  }
  return null;
}
