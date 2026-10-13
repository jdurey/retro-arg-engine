#!/usr/bin/env python3
"""
Project Stardust — 1995-1996 GeoCities Interest Directory & Anemoia Worldbuilding Engine
Generates all 20 "MATCH YOUR INTEREST TO A NEIGHBORHOOD" pages for GeoCities:
  1. ARTS             (interest-arts)
  2. AUTOS            (interest-autos)
  3. BUSINESS         (interest-business)
  4. COMPUTERS        (interest-computers)
  5. CULTURE          (interest-culture)
  6. EDUCATION        (interest-education)
  7. ENTERTAINMENT    (interest-entertainment)
  8. ENVIRONMENT      (interest-environment)
  9. FAMILY           (interest-family)
  10. FASHION         (interest-fashion)
  11. FOOD            (interest-food)
  12. GAMES           (interest-games)
  13. GAY & LESBIAN   (interest-gay-lesbian)
  14. GOVERNMENT      (interest-government)
  15. HEALTH          (interest-health)
  16. KIDS            (interest-kids)
  17. MUSIC           (interest-music)
  18. PEOPLE          (interest-people)
  19. RECREATION      (interest-recreation)
  20. SCIENCE FICTION (interest-scifi)

Each page is a deep, period-authentic 1995-1996 HTML 3.2 community hub set in the
Anemoia universe—grounded in 90s hardware, Steel Thunder (1987), Heartstrike,
Orion Corporation's consumer divisions, BBS/Usenet culture, and everyday 90s life,
without centering on Nova Hart.
"""

from __future__ import annotations
import html
import json
import subprocess
from pathlib import Path

INTEREST_SPECS = [
    {
        "label": "ARTS",
        "slug": "interest-arts",
        "hood": "SoHo/Studio & Paris/LeftBank",
        "hood_slug": "hood_soho-studio",
        "bg": "#FDFBF2",
        "text": "#111111",
        "link": "#990000",
        "vlink": "#551A8B",
        "banner_color": "#880000",
        "title": "GeoCities Arts — The SoHo Xerography, Mail-Art & Zine Rack (1995)",
        "curator": "Mara Vance (mara_v@nyx.net) // Mercer St. Late-Shift Copy & Bindery, NYC",
        "counter": "014892",
        "updated": "1995-10-11",
        "marquee": "*** OCTOBER ZINE SWAP DEADLINE: SEND 2 FIRST-CLASS STAMPS + YOUR 1/2-LEGAL PHOTOCOPY ZINE TO P.O. BOX 419 CANAL ST ***",
        "lead": (
            "Welcome to the GeoCities Arts & Independent Print Commons. You won't find glossy "
            "museum gift-shop JPEGs here—most of us are scanning halftone collages on flatbed "
            "UMAX scanners at 150 DPI so your 14.4k modem doesn't choke. This hub connects "
            "photocopy zinesters, rubber-stamp mail artists, Deluxe Paint IV pixel-pushers, "
            "and 16mm scratch-film projectionists across SoHo, Paris, and Vienna."
        ),
        "ascii_title": "KONICA 3035 TONER DENSITY & ZINE FOLDING SPEC (8.5 x 14 LEGAL)",
        "ascii_box": r"""  +-------------------------------------------------------------------+
  |  [PAGE 8 (BACK)]   |   [PAGE 1 (COVER)]   <-- LETRASET 24PT BOLD  |
  |  Staple Saddle     |   Paste-up with 3M SprayMount (No Scotch     |
  |  along center      |   tape! Tape edges cast black shadow lines   |
  |  crease (2x Bostitch)|  when the drum corona wire gets dirty!)    |
  +--------------------+----------------------------------------------+
  |  PRO TIP: Set Exposure Slider to -2 (LIGHT) for newspaper         |
  |  clippings and +3 (DARK) for pencil cross-hatching.               |
  +-------------------------------------------------------------------+""",
        "sections": [
            (
                "What's on the Zine Rack — Autumn 1995 Reviews",
                [
                    "<b>TONER &amp; BONE #7</b> (Chicago, 28 pp., digest size, $1.50 or trade): "
                    "Hand-typed on an IBM Selectric II with a script ball. Features a four-page "
                    "interview with a projectionist who ran 35mm midnight reels of <i>Steel Thunder</i> "
                    "and Czech stop-motion shorts at the Biograph until the platter motor caught fire.",
                    "<b>MERCER STREET HALFTONE #12</b> (SoHo/NYC, 16 pp., $1 + two 32¢ stamps): "
                    "Our house zine. Includes a comparative teardown of Letraset dry-transfer "
                    "sheets vs. Aldus PageMaker 5.0 PostScript halftones, plus photographs of "
                    "abandoned pneumatic mail tubes under Lower Manhattan.",
                    "<b>LE PETIT FORMAT #4</b> (Lyon/Paris, bilingual French/English, 10 FF or IRC): "
                    "Dedicated to disposable camera exposures taken from night trains between "
                    "Gare de Lyon and Geneva.",
                ],
            ),
            (
                "The Great Digital Gradient Debate: Letraset vs. Kai's Power Tools",
                [
                    "Every week someone posts to <tt>alt.zines</tt> asking whether they should "
                    "ditch their X-Acto knives and wax-coaters for CorelDRAW 5 and Kai's Power Tools "
                    "texture generators. Here is our manifesto: a neon rainbow fractal sphere on a "
                    "laser-printed cover does not make a magazine. When you photocopy a photograph "
                    "four generations down on 20-pound canary bond, the grain starts telling the "
                    "truth. Keep your wax rollers warm.",
                ],
            ),
        ],
        "table_headers": ["Homestead / Zine", "Medium & Equipment", "Trade Terms"],
        "table_rows": [
            ["SoHo/Studio/3104 — The Paste-Up Desk", "Konica 3035, Wax Coater, Rapidograph 00", "Trade 1-for-1 or two 32c stamps"],
            ["Paris/LeftBank/2208 — Atelier Gris", "Super-8 Tri-X Reversal & Linocut", "1 International Reply Coupon (IRC)"],
            ["Vienna/Strasse/1902 — Kunst-Keller", "Amiga 2000 + Deluxe Paint IV IFF Art", "Floppy swap (880KB DD AmigaDOS)"],
            ["SoHo/Gallery/4410 — Glass Negative", "Cyanotype & Pinhole Oatmeal Tin Cameras", "Postcard exchange worldwide"],
        ],
        "guestbook": [
            ("Toby_K", "Portland, OR", "1995-10-09", "Used your -2 exposure trick on the library Canon copier last night. Zero tape shadows! Sending issue #3 of 'Rain Gutter' tomorrow."),
            ("Sabine", "Berlin-Kreuzberg", "1995-10-04", "Anyone have spare sheets of Letraset Futura Extra Bold 36pt? All the stationery shops here only stock laser labels now."),
        ],
    },
    {
        "label": "AUTOS",
        "slug": "interest-autos",
        "hood": "Heartland/Plains & Colosseum/Track",
        "hood_slug": "hood_heartland-plains",
        "bg": "#101418",
        "text": "#E0E6ED",
        "link": "#FFCC00",
        "vlink": "#FF8800",
        "banner_color": "#223344",
        "title": "GeoCities Autos — B-Body & Boost: The 1986-1995 Turbo Garage",
        "curator": "Danny 'Torque' Kowalski (dkowalski@crl.com) // Dayton, Ohio",
        "counter": "028410",
        "updated": "1995-10-12",
        "marquee": "*** WARNING: NEVER RUN 18 PSI ON A STOCK MITSUBISHI G54B CAST PISTON WITHOUT RICHENING SECONDARY INJECTOR DUTY CYCLE ***",
        "lead": (
            "Pull up a milk crate and mind the transmission fluid pan. This corner of GeoCities "
            "is for shade-tree mechanics keeping late-80s intercooled turbo coupes, GM G-bodies, "
            "and square-headlight Japanese rally homologation specials out of the crusher. "
            "No lease-special aero sedans allowed."
        ),
        "ascii_title": "GM 12-PIN ALDL DIAGNOSTIC CONNECTOR -> RS-232 LAPTOP INTERFACE",
        "ascii_box": r"""   [PIN F: +12V]  [PIN E: 160/8192 BAUD DATA]  [PIN B: DIAG SHORT]  [PIN A: GND]
    |              |                            |                    |
    +---[10k]------+---> 2N2222 BASE            +--[JUMPER TO A FOR BLINK CODES]
                         EMITTER -> DB9 PIN 5 (GND)
                         COLLECTOR -> DB9 PIN 2 (RXD) ON TOSHIBA T1200 DOS LAPTOP""",
        "sections": [
            (
                "Settling the 'Steel Thunder' (1987) Refinery Pursuit Car Mystery",
                [
                    "For eight years, <tt>rec.autos.makers.chrysler</tt> and <tt>rec.autos.sport.tech</tt> "
                    "have argued about the matte-black widebody fastback that jumps the flood-control "
                    "channel at the 42-minute mark of <b><i>Steel Thunder</i> (1987)</b>. If you freeze-frame "
                    "the Japanese CAV LaserDisc on frame 61,408, you can clearly see the six-lug "
                    "16x8SHP rear alloy wheels and the three-piece wraparound spoiler: the stunt team "
                    "used three 1987 Chrysler Conquest TSi / Mitsubishi Starion widebodies fitted with "
                    "muffler-shop straight pipes and over-shimmed wastegates.",
                    "Stunt coordinator Hal Needham's second-unit mechanic confirmed in the May '88 issue "
                    "of <i>AutoWeek</i> that Car #2 survived the Long Beach shoot with a bent strut tower "
                    "and is still sitting under a tarp in Pacoima.",
                ],
            ),
            (
                "Why You Should Stockpile R-12 Freon Cans Before December 31",
                [
                    "With the federal CFC-12 production ban taking full effect at the end of this year, "
                    "local auto parts counters have jacked 12-ounce cans of DuPont Freon from $1.99 to "
                    "$18.50. Before you let a quick-lube shop pump R-134a and ester oil into your 1986 "
                    "Harrison R4 radial compressor without swapping the parallel-flow condenser, read our "
                    "mineral-oil flush guide below.",
                ],
            ),
        ],
        "table_headers": ["Chassis / Engine", "Stock Boost / Quarter Mile", "Common Failure Point"],
        "table_rows": [
            ["1987 Buick Grand National (3.8L LC2 SFI)", "14.5 PSI // 13.9s @ 98 mph", "Plastic vacuum T-fittings & nylon timing gear"],
            ["1988 Chrysler Conquest TSi (2.6L G54B)", "10.5 PSI // 15.1s @ 91 mph", "Cracked exhaust manifold between #3 and #4"],
            ["1991 GMC Syclone (4.3L LB4 AWD Turbo)", "14.0 PSI // 13.4s @ 99 mph", "Water-to-air intercooler pump impeller failure"],
            ["1989 Toyota Supra Turbo (3.0L 7M-GTE)", "6.8 PSI // 15.0s @ 93 mph", "Factory head-bolt torque (58 ft-lbs -> re-torque to 72!)"],
        ],
        "guestbook": [
            ("Boosted87", "Dearborn, MI", "1995-10-10", "Built your 2-transistor ALDL cable for $3.40 at RadioShack. Logged 4 degrees of knock retard at WOT in 3rd gear—fuel pump relay was dropping 1.4 volts!"),
            ("Mitch_S", "Bakersfield, CA", "1995-10-02", "I knew that car in Steel Thunder was a Starion! My brother owed me a six-pack over that bet since 1989."),
        ],
    },
    {
        "label": "BUSINESS",
        "slug": "interest-business",
        "hood": "SiliconValley/Park & Tokyo/Ginza",
        "hood_slug": "hood_siliconvalley-lab",
        "bg": "#F4F6F8",
        "text": "#001B33",
        "link": "#003399",
        "vlink": "#444466",
        "banner_color": "#002B55",
        "title": "GeoCities Business — Pacific Rim Venture & Post-Bubble Ledger (1995)",
        "curator": "Arthur Pendelton, CFA (apendelton@netcom.com) // San Jose & Minato-ku",
        "counter": "009314",
        "updated": "1995-10-13",
        "marquee": "*** MARKET WIRE: NETSCAPE (NSCP) HOLDS $58 AFTER AUGUST IPO SURGE // NIKKEI 225 HOVERS NEAR 17,900 ***",
        "lead": (
            "Independent equity analysis, telecom tariff benchmarks, and post-bubble corporate "
            "archeology across Silicon Valley and Tokyo. Written in plain HTML 3.2 so you can "
            "read it over a CompuServe or Netcom PPP dialer without waiting for 40KB of "
            "gratuitous stock-photo handshakes to render."
        ),
        "ascii_title": "1995 DEDICATED INTERNET LEASED-LINE COST MODEL (PACIFIC BELL TAR)",
        "ascii_box": r"""  CIRCUIT TYPE          BANDWIDTH    INSTALL FEE    MONTHLY ISP + LOOP   HARDWARE REQ
  ------------------------------------------------------------------------------------
  28.8k V.34 Dial-Up    28.8 kbps    $0.00          $19.95 (Flat Netcom) USR Sportster
  ISDN BRI (2B+D)       128 kbps     $175.00        $68.00 + 1.2c/min    Ascend Pipeline 50
  Frame Relay (56k CIR) 56 kbps      $650.00        $390.00 / mo         Cisco 2501 + CSU/DSU
  Full T-1 (DS1)        1.544 Mbps   $1,800.00      $1,450.00 / mo       Cisco 2501 + Adtran""",
        "sections": [
            (
                "Case Study: Why Orion Corporation Shuttered Its Akasaka Consumer Media Division",
                [
                    "To understand the 1990–1995 Japanese corporate balance-sheet unwind, look no "
                    "further than <b>Orion Corporation's</b> March 31, 1993 reorganization of its "
                    "Akasaka audiovisual subsidiary. During the 1985–1989 cheap-capital boom, "
                    "Orion poured billions of yen into custom neural-synthesis vocal R&amp;D and "
                    "automated mastering suites. When the Nikkei 225 collapsed from its December 29, "
                    "1989 peak of 38,915, Orion's main bank forced a write-down of the entire "
                    "Tokyo studio annex, folding the surviving patent portfolio into a quiet "
                    "Geneva licensing shell while pivoting domestic retail to safe, low-margin "
                    "adult-contemporary releases like <i>Luna Gray</i>.",
                ],
            ),
            (
                "The 'CD-ROM Shovelware' Inventory Glut of Q4 1995",
                [
                    "Walk into any Egghead Software or CompUSA this week and count the jewel cases "
                    "in the $9.99 bargain bin: <i>The 1994 Multimedia Encyclopedia of Frogs</i>, "
                    "<i>Interactive Lawn Care on CD-ROM</i>, and thirty different clip-art discs. "
                    "Venture capitalists on Sand Hill Road are finally realizing that pressing "
                    "650 megabytes of QuickTime 1.6 postage-stamp video onto polycarbonate does not "
                    "constitute a defensible moat when 28.8k dial-up nodes are doubling every "
                    "six months.",
                ],
            ),
        ],
        "table_headers": ["Sector / Ticker", "1995 Valuation Thesis", "Risk Rating"],
        "table_rows": [
            ["Regional Dial-Up ISPs (POPs)", "High subscriber growth; vulnerable to RBOC telco entry", "MODERATE"],
            ["Multimedia CD-ROM Publishers", "Severe retail channel stuffing & consignment returns", "HIGH RISK"],
            ["60ns EDO DRAM Fabricators", "Spot prices holding at $32/MB due to Windows 95 upgrades", "BULLISH"],
            ["Analog Magnetic Tape (Type II/IV)", "Secular decline in North America; resilient in Eastern Europe/LatAm", "NEUTRAL"],
        ],
        "guestbook": [
            ("K_Watanabe", "Otemachi, Tokyo", "1995-10-11", "Your breakdown of the 1993 Akasaka real-estate write-offs is spot on. Half of the 4th-floor studio rack gear ended up in Akihabara surplus alleys."),
            ("G_Mercer", "Palo Alto, CA", "1995-10-06", "Quoted your Frame Relay vs. ISDN table to our VP of MIS today. Saved us from signing a 3-year T1 contract we don't need yet."),
        ],
    },
    {
        "label": "COMPUTERS",
        "slug": "interest-computers",
        "hood": "SiliconValley/Lab & Vienna/Strasse",
        "hood_slug": "hood_siliconvalley-lab",
        "bg": "#000044",
        "text": "#FFFFFF",
        "link": "#00FFFF",
        "vlink": "#FFFF00",
        "banner_color": "#006666",
        "title": "GeoCities Computers — The Jumper Block: 486/Pentium & The 16MB Truth",
        "curator": "Bozidar 'Boz' Novak (bnovak@mcs.com) // comp.sys.ibm-pc.hardware FAQ Maintainer",
        "counter": "064119",
        "updated": "1995-10-14",
        "marquee": "*** PUBLIC SERVICE ANNOUNCEMENT: 16MB OF 60NS EDO RAM IS ALL YOU WILL EVER NEED. STOP LETTING MAGAZINE ADS SELL YOU 32MB! ***",
        "lead": (
            "No Java applets, no `<BLINK>` tags, and no bloated BMPs. This is a hardware jumper, "
            "DMA channel, and CONFIG.SYS optimization sanctuary for builders running AMD 486DX4-100 "
            "VLB rigs, early Pentium P54C boards, OS/2 Warp 3, and Slackware 2.3."
        ),
        "ascii_title": "ISA BUS IRQ / DMA SURVIVAL MATRIX (NO PLUG-AND-PRAY EDITION)",
        "ascii_box": r"""  IRQ  DEFAULT ASSIGNMENT         SAFE OVERRIDE / JUMPER NOTES
  ---------------------------------------------------------------------------
  IRQ 3  COM2 / COM4 (Modem)      Set internal USR 28.8k to COM2 / IRQ 3
  IRQ 5  LPT2 (Unused!)           MANDATORY FOR SOUND BLASTER 16 / AWE32!
  IRQ 7  LPT1 (Dot Matrix/Laser)  Set Gravis Ultrasound GF1 here if dual-card
  IRQ 10 Free 16-bit ISA Slot     NE2000 Coax Ethernet or Adaptec AHA-1542CF
  DMA 1  8-bit Low Audio DMA      Sound Blaster PCM playback
  DMA 5  16-bit High Audio DMA    Sound Blaster 16-bit stereo full-duplex""",
        "sections": [
            (
                "The 16MB RAM Manifesto: Why Anything Over 16 Megabytes Is Pure Marketing",
                [
                    "At $34 per megabyte for 72-pin 60ns EDO SIMMs, a pair of 8MB sticks costs $544. "
                    "Yet computer-superstore salesmen are telling college freshmen they need 32MB "
                    "just to write term papers! Let's look at the engineering facts: first, half of "
                    "the Socket 3 and early Socket 5 motherboards on the market (especially budget "
                    "SIS and Opti chipsets with 128KB of L2 SRAM) <b>cannot even cache memory above "
                    "16MB or 32MB</b> without a second tag-RAM chip—meaning adding a third SIMM "
                    "actually <i>slows down</i> your system!",
                    "Second, with a clean `CONFIG.SYS` loading `HIMEM.SYS` and `EMM386.EXE NOEMS` "
                    "(giving you 621KB of free conventional memory), or under OS/2 Warp 3 and "
                    "Linux kernel 1.2.13, 16MB leaves 11MB of untouched RAM disk even while compiling "
                    "a 16,384-point FFT in C. Write tighter code instead of buying more silicon.",
                ],
            ),
            (
                "Overclocking the AMD 5x86-P75 (133 MHz) on a 40 MHz VESA Local Bus",
                [
                    "If you set your Biostar MB-8433UUD bus clock jumpers (`JP14-JP16`) from 33 MHz "
                    "to 40 MHz with a 4x multiplier (160 MHz core!), remember to add **1 wait state** "
                    "to your VLB Tseng Labs ET4000/W32p video card (`JP1 CLOSED`). At 0 wait states "
                    "on a 40 MHz bus, the pixel clock scrambles hardware cursors in XFree86 3.1.2.",
                ],
            ),
        ],
        "table_headers": ["Component", "1995 Sweet-Spot Pick", "Why It Beats the Hype"],
        "table_rows": [
            ["CPU + Board", "AMD Am486DX4-100 (Write-Back) + PCI/VLB VIP", "Outruns a Pentium 60 in integer DSP at half the heat"],
            ["Sound Card", "Gravis Ultrasound Max (1MB onboard RAM)", "32 hardware-mixed channels with 0% CPU overhead in MOD trackers"],
            ["Hard Drive", "Quantum Fireball 1080A (1.08 GB, 5400 RPM)", "Fast PIO Mode 4 transfers; quiet bearings"],
            ["Monitor", "NEC MultiSync XV15 (15-inch, 1024x768 @ 76Hz)", "Zero flicker; flat square shadow-mask tube"],
        ],
        "guestbook": [
            ("LinusFan_AT", "Graz, Austria", "1995-10-13", "Thank you for the Tag-RAM note! Pulled my extra 8MB SIMM out of my 128KB L2 cache board and Doom timedemo went UP by 4.2 fps!"),
            ("IRQ_Hell", "Toronto, ON", "1995-10-08", "Plug-and-Play on my new SB16 Vibra kept grabbing IRQ 10 from my SCSI card. Swapped it for an old jumpered CT1740—instant peace."),
        ],
    },
    {
        "label": "CULTURE",
        "slug": "interest-culture",
        "hood": "Paris/LeftBank & Vienna/Choir",
        "hood_slug": "hood_paris-leftbank",
        "bg": "#FAF0E6",
        "text": "#221810",
        "link": "#800020",
        "vlink": "#4A2E35",
        "banner_color": "#4A1C24",
        "title": "GeoCities Culture — Café Minitel & The Late-Century Urban Flâneur",
        "curator": "Claire Beaumont (cbeaumont@fdn.fr) // Lyon & Paris 5e",
        "counter": "011205",
        "updated": "1995-10-10",
        "marquee": "*** NOUVEAU: ARCHIVE OF 3615 VIDEOTEX SCREENS & NIGHT-TRAIN CASSETTE FIELD RECORDINGS (PARIS -> VIENNA) ***",
        "lead": (
            "Before the World Wide Web arrived with its gray Mosaic backgrounds, millions of "
            "French households already lived inside the amber glow of the Minitel 1B terminal. "
            "This salon documents the transition from national Videotex networks, late-night "
            "pirate FM micro-transmitters, and European café zine culture into the global net."
        ),
        "ascii_title": "MINITEL 1B (TELIC ALCATEL) 40-COLUMN VIDEOTEX FRAME GEOMETRY",
        "ascii_box": r"""  +----------------------------------------+
  | 3615 CAFE * SALON LITTERAIRE  1,29F/mn |
  |----------------------------------------|
  | > "La nuit n'est jamais complète;      |
  |    il y a toujours une porte ouverte   |
  |    sur la fréquence."                  |
  |                                        |
  | Tapez votre message............ [ENVOI]|
  | Sommaire....................... [SUITE]|
  +----------------------------------------+""",
        "sections": [
            (
                "In Defense of the Walkman WM-DD9 and the 90-Minute Solitude",
                [
                    "There is a peculiar rhythm to walking through the rain in the 13th arrondissement "
                    "with a quartz-locked Sony WM-DD9 clipped to your coat pocket. Unlike a portable "
                    "CD player—which skips if you step off a curb too briskly—a well-calibrated "
                    "amorphous-head cassette player turns the city into a continuous tracking shot. "
                    "When Side A clicks off after 45 minutes, the mechanical silence reminds you to "
                    "look up at the streetlamps.",
                ],
            ),
            (
                "From 'Bande FM Libre' (1981) to the 1995 Micro-Web",
                [
                    "Many of the people building personal homepages in Paris/LeftBank today cut their "
                    "teeth in the early 1980s soldering 15-watt FM transmitters in attic bedrooms "
                    "for France's free-radio explosion (<i>Radio Ivre</i>, <i>Fréquence Gaie</i>, "
                    "<i>Radio Carbone 14</i>). Commercial consolidation swallowed the FM dial by 1990, "
                    "but HTML tables and cheap dial-up shells have reopened the attic studio.",
                ],
            ),
        ],
        "table_headers": ["City / Quarter", "Nocturnal Landmark (1995)", "Soundtrack on the Tape Deck"],
        "table_rows": [
            ["Paris — Rue Mouffetard", "24h Tabac & Public Télécarte Booth #4", "Etienne Daho /Les Rita Mitsouko (CrO2 dub)"],
            ["Vienna — Mariahilfer Straße", "Café Sperl back-table newspaper rack", "Falco & Austrian Elektronische Welle compilations"],
            ["Berlin — Oranienstraße", "SO36 Poster Kiosk & Spätkauf", "Post-Wall warehouse dubs & industrial 7-inches"],
            ["Athens — Exarchia Square", "Vinyl basement shops on Arachovis St.", "Rebetiko 78rpm transfers & late-80s synth wave"],
        ],
        "guestbook": [
            ("Luc_B", "Brussels, Belgium", "1995-10-08", "Still have my Alcatel Minitel terminal plugged into the wall socket next to my 486. The keyboard clack is unmistakable."),
            ("Elena_M", "Milan, Italy", "1995-10-01", "Your essay on the WM-DD9 vs Discman anti-shock buffers made me smile. Long live metal tape!"),
        ],
    },
    {
        "label": "EDUCATION",
        "slug": "interest-education",
        "hood": "Athens/Forum & SiliconValley/Heights",
        "hood_slug": "hood_athens-forum",
        "bg": "#FFFFEE",
        "text": "#000000",
        "link": "#004400",
        "vlink": "#336633",
        "banner_color": "#004422",
        "title": "GeoCities Education — The VAX/VMS Campus Lab & LaTeX Survival Guide",
        "curator": "Colin Marsh (cmarsh@ee.ashford-poly.org) // Undergraduate EE Lab Proctor",
        "counter": "019402",
        "updated": "1995-10-12",
        "marquee": "*** NOTICE TO ALL UNDERGRADS: DO NOT SEND UNCOMPRESSED .PS FILES > 4MB TO printer 'lp0-laser' DURING EXAM WEEK ***",
        "lead": (
            "Compiled at 03:40 AM in Basement Room B-12 of the Electrical Engineering Annex "
            "while waiting for a SPICE transient simulation to converge. This page collects "
            "practical survival notes for university students living on 5MB campus UNIX/VMS "
            "disk quotas, HP-48GX infrared programs, and coin-operated photocopy cards."
        ),
        "ascii_title": "HP-48GX RPN STACK CHEAT SHEET FOR SECOND-ORDER BUTTERWORTH FILTERS",
        "ascii_box": r"""  4:  [ R_LOAD (Ohms) ]        KEYS:  [<<] [DUP] [2] [*] [PI] [*]
  3:  [ F_CUTOFF (Hz) ]               [*] [INV] [SWAP] [/] [>>]
  2:  1.41421356 (sqrt(2))     OUTPUT: Level 2 -> L_henries
  1:  3.14159265 (pi)                  Level 1 -> C_farads
  (Beam via IR port during lab practicals at your own academic peril!)""",
        "sections": [
            (
                "How to Stretch a 4.0 MB University UNIX Home Directory Quota",
                [
                    "When the department sysadmin sets `edquota` to a hard limit of 4,096 kilobytes "
                    "on `/home/undergrad`, a single core dump (`core`) or cached Netscape `~/.netscape-cache` "
                    "directory will lock you out of X11 login (`Disk quota exceeded`). Step one: "
                    "immediately symlink `~/.netscape-cache` to `/tmp/$USER_cache`. Step two: keep "
                    "all your Fortran-77 and C source files compressed with `gzip -9` and use a "
                    "Makefile rule that pipes directly to `gcc -x c -`.",
                ],
            ),
            (
                "Why Every Engineering Student Should Learn LaTeX 2.09 Instead of Word 6.0",
                [
                    "Watch a classmate try to number forty-two partial differential equations in "
                    "Microsoft Word 6.0 on a 4MB Mac LC III: by page 14, the equation editor "
                    "corrupts the OLE object table and shifts every figure into the margin. Write "
                    "your lab reports in plain ASCII `.tex` on a green-screen DEC VT220, run `dvips`, "
                    "and collect crisp Computer Modern typography from the LaserWriter IIg.",
                ],
            ),
        ],
        "table_headers": ["Campus Resource", "Location / Hostname", "Proctor's Warning"],
        "table_rows": [
            ["DEC VAXstation 4000 Cluster", "vax1..vax8.ee.ashford-poly.org", "Log out properly or someone will alias your `ls` to `sl`"],
            ["HP LaserJet 4Si MX (Duplex)", "Basement B-14 (`lpr -Plp0`)", "Paper tray #2 jams if humidity exceeds 65%"],
            ["Sun SPARCstation IPX (Color)", "Lab C-04 (Workstation #3)", "Mouse pad optical grid is worn out—bring your own"],
            ["Engineering Library Microfiche", "3rd Floor West Wing", "IEEE Transactions 1965-1988 on 24x fiche cards"],
        ],
        "guestbook": [
            ("Dave_K", "UMIST Manchester", "1995-10-11", "The /tmp symlink trick for Netscape cache just saved my final-year project account. Cheers mate!"),
            ("S_Lindholm", "KTH Stockholm", "1995-10-05", "Can confirm HP-48GX IR range is exactly 14 inches across a lab bench if you remove the battery door."),
        ],
    },
    {
        "label": "ENTERTAINMENT",
        "slug": "interest-entertainment",
        "hood": "Hollywood/Hills & Hollywood/Lot",
        "hood_slug": "hood_hollywood-hills",
        "bg": "#0A0A12",
        "text": "#F0F0F5",
        "link": "#FF3333",
        "vlink": "#CC6666",
        "banner_color": "#660000",
        "title": "GeoCities Entertainment — CELLULOID & CHROME: The 'Steel Thunder' (1987) Vault",
        "curator": "Vance Sterling (vsterling@primenet.com) // Burbank LaserDisc & VHS Hi-Fi Archivist",
        "counter": "052918",
        "updated": "1995-10-14",
        "marquee": "*** WIDESCREEN FOREVER: SAY NO TO 4:3 PAN-AND-SCAN BUTCHERY OF 2.35:1 ANAMORPHIC ACTION CINEMA! ***",
        "lead": (
            "Dedicated to practical-effects action cinema (1982–1994), Japanese import CAV "
            "LaserDiscs, JVC Super-VHS editing decks, and the definitive production archive "
            "for Director Jack Vance's 1987 high-octane masterpiece <b><i>Steel Thunder</i></b>."
        ),
        "ascii_title": "LASERDISC VS. VHS HI-FI TECHNICAL COMPARISON ('STEEL THUNDER' 1988 PRESSING)",
        "ascii_box": r"""  SPECIFICATION          DOMESTIC VHS (ORION HOME VIDEO)   JP CAV LASERDISC (PILF-1088)
  -------------------------------------------------------------------------------------
  Horizontal Resolution  240 TV Lines (Composite)          425 TV Lines (Direct RF)
  Aspect Ratio           1.33:1 Pan & Scan (Cropped!)      2.35:1 Letterboxed Matte
  Audio Track            Helical AFM Hi-Fi Stereo          Uncompressed 16-bit PCM + CX
  Refinery Explosion     Cut by 4.5 seconds (MPAA R)       Uncut 18-camera pyrotechnics""",
        "sections": [
            (
                "Anatomy of a Practical Stunt: The Long Beach Refinery Jump in 'Steel Thunder'",
                [
                    "Today's Hollywood directors want to replace real stuntmen with Silicon Graphics "
                    "wireframes. Go back and put on Side 2, Chapter 19 of <b><i>Steel Thunder</i> (1987)</b>: "
                    "when Detective Frank Kestrel (played by Royce Sterling) launches the black "
                    "turbo coupe across 110 feet of open drainage canal between two exploding "
                    "butane spheres while <b>Heartstrike's</b> <i>'Run With The Fire'</i> hits the "
                    "key change, there isn't a single optical composite in the frame.",
                    "Twenty-two gallons of naphthalene and four Primacord sequenced charges were "
                    "detonated 0.4 seconds after the rear tires cleared the ramp. The shockwave "
                    "actually cracked the 35mm Arriflex 35BL lens housing on Camera B—and they "
                    "kept the take in the movie!",
                ],
            ),
            (
                "Hunting the Lost 134-Minute San Diego Preview Workprint",
                [
                    "Before Orion Pictures trimmed 19 minutes out of <i>Steel Thunder</i> to squeeze "
                    "an extra nightly screening into multiplexes in July 1987, a 134-minute workprint "
                    "was screened once in San Diego. That cut includes the complete 6-minute night "
                    "dockyard shootout scored with an instrumental synth-bass suite that never "
                    "appeared on the retail cassette soundtrack. If you have a time-coded 3/4-inch "
                    "U-Matic studio dub, email me immediately.",
                ],
            ),
        ],
        "table_headers": ["Release Edition", "Catalog #", "Collector Notes & Rarity"],
        "table_rows": [
            ["1988 Japan CAV 2-Disc Special Box", "PILF-1088", "Includes 12-page bilingual stunt blueprint booklet ($140 import)"],
            ["1987 US Rental VHS (Big Box)", "OHV-8704", "Foil-embossed silver cover; un-attenuated Hi-Fi bass track"],
            ["1987 Soundtrack LP / CrO2 Cassette", "ORION-ST87", "Features Heartstrike ('Run With The Fire') & 4 synth instrumentals"],
            ["1991 UK PAL Widescreen VHS", "ORV-9112", "4% PAL speedup pitches the guitar solo up ~70 cents"],
        ],
        "guestbook": [
            ("LD_junkie", "Seattle, WA", "1995-10-12", "Just calibrated my Pioneer CLD-D704 with Video Essentials and spun PILF-1088. That refinery bass drop rattled the drywall."),
            ("ActionFan85", "Sydney, Australia", "1995-10-03", "My dad worked security at the Long Beach shoot! He still has a charred yellow crew jacket from Second Unit."),
        ],
    },
    {
        "label": "ENVIRONMENT",
        "slug": "interest-environment",
        "hood": "RainForest/Canopy & EnchantedForest/Dell",
        "hood_slug": "hood_rainforest-canopy",
        "bg": "#0B1E11",
        "text": "#D8F3DC",
        "link": "#74C69D",
        "vlink": "#52B788",
        "banner_color": "#1B4332",
        "title": "GeoCities Environment — Canopy Watch & Solar-Powered Packet Telemetry",
        "curator": "Dr. Harlan Vance & Elena Soto (canopy@igc.apc.org) // Olympic Peninsula & Monteverde",
        "counter": "008741",
        "updated": "1995-10-11",
        "marquee": "*** PACKET NODE 'TREE-04' (145.050 MHZ): BATTERY 13.4V // CANOPY HUMIDITY 94% //BAROMETER 1011.2 HPA ***",
        "lead": (
            "Field notes from researchers, amateur radio operators, and forest canopy climbers "
            "using 5-watt solar AX.25 packet transceivers and Campbell Scientific CR10 data "
            "loggers to monitor old-growth microclimates, acid-rain pH trends, and amphibian "
            "chorus populations without stringing copper wire through the woods."
        ),
        "ascii_title": "OLD-GROWTH DOUGLAS FIR CANOPY PLATFORM & SOLAR AX.25 RELAY",
        "ascii_box": r"""         \  |  /   <-- 2m J-Pole Antenna @ 62 meters AGL (Line-of-sight 85 km)
      .---*---*---.
     /  SOLAR 20W  \  --> 12V Gel-Cell in Pelican Case + PacComm Tiny-2 TNC
    '-------+-------'
            |  [Campbell CR10 Logger: Temp / PAR Light / Bark Moisture]
         ===|===  <-- 450-year-old Pseudotsuga menziesii Crown Platform""",
        "sections": [
            (
                "Why 1200-Baud VHF Packet Radio Beats Satellite Uplinks in the Cloud Forest",
                [
                    "University grant committees love buying $12,000 commercial satellite phones "
                    "that die the first time epiphytic moss grows over the dish feedhorn. For "
                    "$280 per tree, we bolt an Icom IC-2AT handheld, a PacComm Tiny-2 TNC, and "
                    "a 20-watt Siemens solar panel into an ammo can 200 feet up in the canopy. "
                    "Every four hours, the logger bursts 400 bytes of microclimate CSV data down "
                    "to the valley university gateway (`igc.apc.org`).",
                ],
            ),
            (
                "Good News From the Stratosphere: NOAA Halocarbon Trends in 1995",
                [
                    "For the first time since measurements began at Mauna Loa and Barrow, atmospheric "
                    "growth rates of trichlorofluoromethane (CFC-11) and dichlorodifluoromethane "
                    "(CFC-12) have flattened out following the Montreal Protocol phase-out. The "
                    "Antarctic spring ozone hole is still deep this October, but the chemistry proves "
                    "that international treaties backed by hard atmospheric spectroscopy actually work.",
                ],
            ),
        ],
        "table_headers": ["Monitoring Station", "Elevation / Biome", "Live Telemetry Schedule"],
        "table_rows": [
            ["Hoh River Platform #4 (WA, USA)", "58m AGL // Temperate Sitka Spruce", "00:15, 06:15, 12:15, 18:15 UTC on 145.05 MHz"],
            ["Monteverde Cloud Node (Costa Rica)", "1,540m ASL // Tropical Montane Cloud", "Hourly store-and-forward via TI0PKT"],
            ["Black Forest pH Collector (Germany)", "1,120m ASL // Norway Spruce Stand", "Weekly upload to `de.sci.umwelt`"],
            ["Tasman Kelp Acoustic Buoy (Australia)", "12m Depth // Giant Kelp Holdfast", "Hydrophone spectrum digest every Sunday"],
        ],
        "guestbook": [
            ("KE6_Eco", "Arcata, CA", "1995-10-09", "Used your silicone potting compound recipe on our redwood thermistor leads—survived three weeks of horizontal coastal fog!"),
            ("M_Berger", "Freiburg, Germany", "1995-10-01", "Downloading your CR10 calibration macros for our soil-pH loggers. Great resource."),
        ],
    },
    {
        "label": "FAMILY",
        "slug": "interest-family",
        "hood": "Heartland/Prairie & Heartland/Valley",
        "hood_slug": "hood_heartland-plains",
        "bg": "#FFFDF5",
        "text": "#222222",
        "link": "#0055AA",
        "vlink": "#663366",
        "banner_color": "#2B547E",
        "title": "GeoCities Family — The Henderson Homestead: Taurus Wagon Logs & Heathkit Weather",
        "curator": "Greg & Linda Henderson (ghenderson54@aol.com) // Overland Park, Kansas",
        "counter": "003188",
        "updated": "1995-10-08",
        "marquee": "*** CONGRATULATIONS TO KEVIN FOR MAKING 2ND CHAIR TROMBONE IN SHAWNEE MISSION JUNIOR HIGH BAND! ***",
        "lead": (
            "Welcome to the Henderson Family Home Page on the World Wide Web! Greg is a "
            "claims adjuster who built our Heathkit ID-4001 weather station in 1988, Linda "
            "runs the church bell-choir newsletter in Print Shop Deluxe, Kevin (13) is "
            "obsessed with building Estes model rockets, and Barnaby is our 9-year-old Basset Hound."
        ),
        "ascii_title": "THE 1995 HENDERSON HOUSEHOLD TELEPHONE & MODEM TREATY",
        "ascii_box": r"""  +--------------------------------------------------------------------+
  | RULE 1: NO DIALING INTO AOL OR COMPUSERVE BETWEEN 5:00 PM & 8:30 PM|
  |         (Grandma calls from Wichita at 6:30 PM sharp on Wednesdays)|
  | RULE 2: Disable Call Waiting (*70,) ONLY if downloading a file     |
  |         under 15 minutes. Write time started on the kitchen pad!   |
  | RULE 3: Whoever leaves the 25-foot beige phone cord stretched      |
  |         across the hallway stairs loses computer privileges!       |
  +--------------------------------------------------------------------+""",
        "sections": [
            (
                "1995 Summer Road Trip Log: 2,410 Miles in the 1991 Ford Taurus Wagon",
                [
                    "In July we packed the roof carrier on the '91 Taurus GL Wagon (3.0L Vulcan V6, "
                    "light titanium metallic) and drove from Overland Park out to Rocky Mountain "
                    "National Park and back via Cheyenne. Total fuel consumed: 94.8 gallons "
                    "(25.4 MPG highway, even with the A/C running across western Kansas!). "
                    "Lowest gas price spotted: <b>$1.04/gallon</b> for 87 octane in Colby, KS.",
                ],
            ),
            (
                "Greg's Basement Workbench: Fixing the VCR Blinking '12:00' & Idler Tire",
                [
                    "If your 1988 Panasonic OmniVision VHS deck eats tapes on rewind or refuses to "
                    "eject, don't throw it away and buy a cheap plastic 2-head deck! Nine times "
                    "out of ten, the rubber idler tire (`Part #VXP0521`, $2.75 from MCM Electronics) "
                    "has glazed over. Clean the capstan shaft with 91% isopropyl alcohol on a "
                    "chamois swab—never a cotton Q-tip!",
                ],
            ),
        ],
        "table_headers": ["Month (1995)", "Overland Park High / Low (Heathkit ID-4001)", "Rainfall & Yard Notes"],
        "table_rows": [
            ["July 1995", "103°F (Jul 13) / 64°F", "3.8 in. — Crabgrass near driveway; replaced Toro mower plug"],
            ["August 1995", "99°F (Aug 19) / 66°F", "1.9 in. — Tomatoes came in early; Linda canned 18 quarts"],
            ["September 1995", "91°F (Sep 4) / 39°F", "2.4 in. — Put plastic storm-window film on basement casements"],
            ["October 1995", "78°F (Oct 2) / 34°F", "1.1 in. — Cleaned gutters; drained garden hose bibs"],
        ],
        "guestbook": [
            ("Uncle_Bob", "Tulsa, OK", "1995-10-07", "Greg, the photo of Barnaby asleep on the heat register took 45 seconds to load from top to bottom and had us all laughing!"),
            ("W0_Weather", "Lincoln, NE", "1995-09-29", "Nice Heathkit ID-4001 setup! Where did you find replacement cups for the rooftop anemometer?"),
        ],
    },
    {
        "label": "FASHION",
        "slug": "interest-fashion",
        "hood": "Tokyo/Ginza & SoHo/Gallery",
        "hood_slug": "hood_tokyo-garden",
        "bg": "#141414",
        "text": "#E8E8E8",
        "link": "#FF66AA",
        "vlink": "#CC66CC",
        "banner_color": "#441133",
        "title": "GeoCities Fashion — RAYON, NYLON & NEOPRENE: 1995 Street & Thrift Index",
        "curator": "Rina Matsuda & Jules (rina_m@twics.com) // Jingumae (Ura-Harajuku) & Lower East Side",
        "counter": "021504",
        "updated": "1995-10-13",
        "marquee": "*** AUTUMN/WINTER 95-96 DISPATCH: BALLISTIC NYLON MESSENGER BAGS, CASIO DBC-610 SILVER, & LOOPWHEEL SWEATSHIRTS ***",
        "lead": (
            "Forget department-store runway syndication. This index documents what people "
            "are actually wearing in the back-alleys of Jingumae (Ura-Harajuku), Broadway "
            "thrift bins in SoHo, and Manchester record fairs in October 1995: technical "
            "fleece, deadstock 1970s suede Pumas, and brushed-aluminum personal electronics "
            "worn as tailoring."
        ),
        "ascii_title": "SPOTTING AUTHENTIC 1986 'HEARTSTRIKE' WORLD IGNITION TOUR RAGLANS",
        "ascii_box": r"""      .---.   .---.
     /  \  '-'  /  \   <-- NECK TAG MUST BE 1985-86 BLUE 'SCREEN STARS BEST'
    / /|       |\ \       (50% Combed Cotton / 50% Polyester, Made in USA)
   /_/ |  [HS] | \_\   <-- Front Chest: 3-color plastisol lightning crest
       |  1986 |       <-- Single-stitch hem at bottom (NO double-needle
       '-------'           overlock—double-stitch means a 1993 bootleg!)""",
        "sections": [
            (
                "Hardware as Wardrobe: The Brushed-Titanium & Translucent Polycarbonate Shift",
                [
                    "Look at the industrial design coming out of Tokyo this autumn: the Nikon 28Ti "
                    "with its analog chronograph dials on top of a black titanium body, the Sony "
                    "MZ-E3 MiniDisc walkman in champagne anodized aluminum, and translucent "
                    "'skeleton' Casio G-Shock DW-6900s. Clothing is following hardware: charcoal "
                    "melton wool coats paired with reflective 3M Scotchlite piping and Velcro "
                    "courier straps.",
                ],
            ),
            (
                "The Ura-Harajuku Small-Batch Print Ethos (Nowhere / Propeller Backstreets)",
                [
                    "While big Shibuya department stores discount leftover 1991 Italian suits, "
                    "tiny 12-square-meter shops down Cat Street are numbering heavyweight "
                    "loopwheel T-shirts by hand from 1 to 100 and packaging them in heat-sealed "
                    "anti-static electronics bags.",
                ],
            ),
        ],
        "table_headers": ["Item / Piece", "1995 Street Price (Tokyo / NYC)", "Authenticity Tell"],
        "table_rows": [
            ["Casio DataBank DBC-610A (Silver)", "¥6,800 // $49.95", "16-button calculator keypad with raised rubber membrane"],
            ["1986 Heartstrike Budokan Tour Raglan", "¥12,000 (Harajuku vintage) // $18 (Thrift)", "Single-stitch 3/4 black sleeves; Akasaka promoter stamp"],
            ["Manhattan Portage Cordura 1000D Bag", "¥9,500 // $58.00", "Red woven label + 2-inch seat-belt webbing strap"],
            ["Deadstock 1982 Adidas München (Made in W. Germany)", "¥24,000 // $85.00", "Gum sole with metric size molded inside heel cup"],
        ],
        "guestbook": [
            ("Koji_98", "Shimokitazawa, Tokyo", "1995-10-12", "Found a 1986 Heartstrike Yokohama Stadium crew jacket at Chicago thrift on Meiji-dori yesterday. Single stitch and heavy satin!"),
            ("Chloe_NY", "East Village, NYC", "1995-10-05", "Your single-stitch vs double-stitch guide saved me $25 on St. Marks Place today."),
        ],
    },
    {
        "label": "FOOD",
        "slug": "interest-food",
        "hood": "BourbonStreet/Delta & Paris/Cafe",
        "hood_slug": "hood_bourbonstreet-delta",
        "bg": "#FFF8E7",
        "text": "#2B1B17",
        "link": "#B22222",
        "vlink": "#6E2C00",
        "banner_color": "#7B241C",
        "title": "GeoCities Food — The 24-Hour Formica Booth & rec.food.cooking Spool",
        "curator": "Marty Thibodeaux (martyt@delphi.com) // New Orleans & Highway 61",
        "counter": "017630",
        "updated": "1995-10-12",
        "marquee": "*** STOP PUTTING SUN-DRIED TOMATOES ON EVERYTHING! // NEW: 1995 HABANERO GARLIC MASH FERMENTATION LOG ***",
        "lead": (
            "Real food for people who eat at 2:00 AM after a gig or a server upgrade. "
            "No celebrity diet shakes, no fat-free SnackWell's propaganda, and no "
            "raspberry vinaigrette on iceberg lettuce. Just cast-iron gumbo roux timings, "
            "`rec.food.cooking` chile-head hot sauce recipes, and our national registry of "
            "24-hour neon diners with working tabletop jukeboxes."
        ),
        "ascii_title": "THE CAJUN ROUX COLOR & SMOKE-POINT TIMELINE (CAST IRON SKILLET)",
        "ascii_box": r"""  TIME (MED HEAT)   COLORHEX / SHADE         AROMA & APPLICATION
  ----------------------------------------------------------------------------
  00:00 - 04:00     Blonde (#F5DEB3)         Raw flour gone; étouffée base
  05:00 - 12:00     Peanut Butter (#CD853F)  Toasted hazelnut; crawfish stew
  13:00 - 25:00     Copper Penny (#8B4513)   Deep nutty; chicken & andouille
  26:00 - 38:00     Dark Chocolate (#3B1E08) DO NOT ANSWER THE PHONE! (Gumbo!)
  38:30+            Black Specks             BURNT — Dump it out & start over!""",
        "sections": [
            (
                "The 1995 Sun-Dried Tomato & Espresso Bar Invasion: A Field Report",
                [
                    "Five years ago, if you ordered a cup of coffee in Seattle or Minneapolis, "
                    "a waitress named Dot poured it out of an orange-lip Bunn-O-Matic decanter "
                    "for sixty-five cents with free refills. Today, every dry-cleaner on the block "
                    "has been converted into a fern-filled espresso lounge serving $2.75 double "
                    "tall hazelnut lattes and focaccia sandwiches buried under half a jar of "
                    "oil-packed sun-dried tomatoes.",
                    "Don't get me wrong—I love a dark-roast pull from a manual La Pavoni lever "
                    "machine—but we maintain this directory to protect the endangered 24-hour "
                    "Formica counter where the hashbrowns are griddled under a bacon press.",
                ],
            ),
            (
                "Midnight Sysadmin Fuel: The Jolt Cola & Szechuan Dumpling Protocol",
                [
                    "Tested across three consecutive weekend database migrations: two 12-ounce cans "
                    "of Jolt Cola ('All the Sugar and Twice the Caffeine' — 71.2 mg per can) paired "
                    "with pan-fried pork potstickers dipped in black Chinkiang vinegar and roasted "
                    "chili oil.",
                ],
            ),
        ],
        "table_headers": ["24-Hour Diner", "Highway / City", "Signature 03:00 AM Order & Jukebox"],
        "table_rows": [
            ["Camellia Grill", "Carrollton Ave, New Orleans", "Pecan Waffle + Chili Cheese Omelette (Counter stools only)"],
            ["Blue Benn Diner (Silk City Car)", "Route 7, Bennington, VT", "Cider-belly pancakes; Seeburg 200 Wall-O-Matic"],
            ["Twin Anchors / Lou Mitchell's", "Jackson Blvd, Chicago, IL", "Skillet eggs & thick-cut toast before the early Loop train"],
            ["Rae's Restaurant", "Pico Blvd, Santa Monica, CA", "Buttermilk biscuits & gravy ($2.65); used in 14 movie shoots"],
        ],
        "guestbook": [
            ("ChileHead_NM", "Las Cruces, NM", "1995-10-10", "Made your fermented Red Savina + carrot brine mash. Took the paint off my spoon. 10/10."),
            ("NightOwl_95", "Jersey City, NJ", "1995-10-03", "Please add the Tick Tock Diner on Route 3 in Clifton! Chrome exterior and Taylor ham 24/7."),
        ],
    },
    {
        "label": "GAMES",
        "slug": "interest-games",
        "hood": "TimesSquare/Arcade & TimesSquare/Dungeon",
        "hood_slug": "hood_timessquare-arcade",
        "bg": "#08060C",
        "text": "#00FF66",
        "link": "#FFCC00",
        "vlink": "#CC6600",
        "banner_color": "#2A1205",
        "title": "GeoCities Games — WADSMITH'S DEN: DOOM II BSP Trees & 60Hz Shmups",
        "curator": "Marcus 'SegFault' Vance (segfault@iquest.net) // Indianapolis & DWANGO Node",
        "counter": "089412",
        "updated": "1995-10-14",
        "marquee": "*** NEW WAD UPLOAD: 'REFINERY_DM.WAD' (INSPIRED BY THE 1987 FILM STEEL THUNDER) — ZERO VISPLANE OVERFLOWS! ***",
        "lead": (
            "If you strafe-50 with mouse + keyboard while your roommate still uses arrow keys, "
            "you're in the right place. Home to `DEU 5.21` / `DCK 2.2` DOOM II level architects, "
            "DB9 serial null-modem soldering guides, 16-bit Japanese vertical shoot-'em-up "
            "imports, and the hunt for the lost 1987 Data East <i>Steel Thunder</i> LaserDisc "
            "arcade prototype."
        ),
        "ascii_title": "DB9 TO DB9 SERIAL NULL-MODEM PINOUT (SOLDER YOUR OWN FOR $2.50!)",
        "ascii_box": r"""   PC #1 (COM1: 16550A UART)                     PC #2 (COM1: 16550A UART)
   -------------------------                     -------------------------
   Pin 2 (RXD)  <------------------------------->  Pin 3 (TXD)
   Pin 3 (TXD)  <------------------------------->  Pin 2 (RXD)
   Pin 4 (DTR)  <------------------------------->  Pin 6 (DSR) + Pin 1 (DCD)
   Pin 5 (GND)  <------------------------------->  Pin 5 (GND)
   Pin 7 (RTS)  <------------------------------->  Pin 8 (CTS)
   RUN COMMAND:  sersetup.exe -irq 4 -port 0x3f8 -9600 -deathmatch -altdeath -nomonsters""",
        "sections": [
            (
                "Preventing 'Visplane Overflow' (128 Limit) in Complex Deathmatch Arenas",
                [
                    "Nothing ruins a 4-player IPX LAN match faster than DOOM.EXE dumping back to "
                    "DOS with `R_FindPlane: no more visplanes` when someone opens a courtyard door. "
                    "Remember: a visplane is created not just per sector, but every time two visible "
                    "subsectors have different floor/ceiling heights, light levels, or flats! "
                    "Keep your outdoor catwalks at a uniform `144` light level and run `RMB 2.1` "
                    "to pack your `REJECT` lump properly.",
                ],
            ),
            (
                "The Unreleased 1987 Data East 'Steel Thunder' LaserDisc Arcade Cabinet",
                [
                    "In November 1987, <i>RePlay Magazine</i> ran a 2-inch blurb from the AMOA Expo "
                    "in Chicago mentioning a sit-down hydraulic cockpit game built by Data East "
                    "around a Sony LDP-1450 LaserDisc player using actual aerial and refinery "
                    "chase footage from Orion's <b><i>Steel Thunder</i></b>. Because the 1984–1985 "
                    "LaserDisc arcade crash had spooked operators, only four location-test cabinets "
                    "were ever shipped. One was last seen at an arcade on the Santa Cruz Beach "
                    "Boardwalk in 1991.",
                ],
            ),
        ],
        "table_headers": ["Title / Platform", "Release / Format", "Frame Rate & Sound Chip"],
        "table_rows": [
            ["DOOM II: Hell on Earth (id Software)", "1994 // MS-DOS 32-bit DOS4GW", "35 FPS cap // OPL3 / General MIDI / GUS"],
            ["Lords of Thunder (Winds / Hudson)", "1993 // PC Engine Super CD-ROM²", "60 Hz locked // Redbook CD Guitar Shred"],
            ["Command & Conquer (Westwood)", "Sept 1995 // 2-CD MS-DOS SVGA", "Act On Instinct FM/PCM streaming audio"],
            ["Wipeout (Psygnosis)", "Sept 1995 // Sony PlayStation", "30 FPS // Cold Storage techno soundtrack"],
        ],
        "guestbook": [
            ("FragMaster_TX", "Richardson, TX", "1995-10-13", "Downloaded REFINERY_DM.WAD over 28.8k last night. The BFG trap on the oil derrick catwalk is pure evil."),
            ("PCE_Import", "Akihabara / SF", "1995-10-06", "If anyone hasn't played Batsugun on Saturn yet, sell your 3DO immediately and import it."),
        ],
    },
    {
        "label": "GAY & LESBIAN",
        "slug": "interest-gay-lesbian",
        "hood": "SoHo/Lofts & Paris/LeftBank",
        "hood_slug": "hood_soho-studio",
        "bg": "#190B28",
        "text": "#F5E6FF",
        "link": "#FF99FF",
        "vlink": "#CC88FF",
        "banner_color": "#4A154B",
        "title": "GeoCities Gay & Lesbian — The Lavender Switchboard & Out-In-Cyberspace Ring",
        "curator": "Julian Vance & Sam Rivera (lavender_bbs@well.com) // Castro SF & Greenwich Village",
        "counter": "016440",
        "updated": "1995-10-11",
        "marquee": "*** WELCOME TO THE OUT-IN-CYBERSPACE WEBRING (STATION #14) // PGP 2.6.2 KEYRING UPDATED OCT 1995 ***",
        "lead": (
            "Since 1986, long before commercial ISPs existed, queer sysops kept community "
            "switchboards alive over late-night FidoNet echoes (`BMUG`, `SOC.MOTSS`, `GLBT-NET`) "
            "and independent photocopy zines. This homestead collects safe-harbor dial-up "
            "directories, independent 16mm festival calendars, and Hi-NRG / synth-pop "
            "12-inch vinyl preservation lists."
        ),
        "ascii_title": "PGP 2.6.2 PUBLIC KEY FINGERPRINT & ANONYMOUS REMAILER CHAIN",
        "ascii_box": r"""  pub  1024/8F4A19C1 1995/02/14 Lavender Switchboard <lavender_bbs@well.com>
       Key fingerprint = 4E 91 A0 2C  14 20 89 B2  77 04 3A 5F  D8 9A C2 11
  [TO ROUTE VIA PENET.FI OR REMAILER]:
  ::
  Anon-To: soc-motss-digest@well.com
  Latent-Time: +0:45""",
        "sections": [
            (
                "How Rural Dial-Up & Usenet Changed Everything (1985–1995)",
                [
                    "If you live in San Francisco, New York, London, or Amsterdam, you can walk "
                    "down the street to an independent bookshop like *A Different Light* or pick up "
                    "a free weekly paper. If you are nineteen years old in a town of 4,000 people "
                    "with a shared family phone line and a 2400-baud modem, finding `soc.motss` or "
                    "a GeoCities homepage at 1:00 AM is the first time you realize there is an "
                    "entire world waiting for you.",
                ],
            ),
            (
                "The 128-BPM Vault: Preserving 1983–1989 Hi-NRG & Italo-Synth 12-Inch Dubs",
                [
                    "Major labels are letting the greatest 12-inch club mixes of the 1980s rot in "
                    "climate-uncontrolled warehouses because they only want to reissue 3-minute "
                    "radio edits on CD compilations. Our tape-swap circle transfers original "
                    "Patrick Cowley, Sylvester, Bronski Beat, and rare 1985 Japanese synth-pop "
                    "promos at 15 IPS onto DAT and Type IV Metal cassettes.",
                ],
            ),
        ],
        "table_headers": ["Community Node / Zine", "City / Network", "Focus & Access"],
        "table_rows": [
            ["The Lavender Switchboard BBS", "San Francisco (415) // FidoNet 1:125/412", "28.8k V.34; community calendar & resource library"],
            ["3615 GAI-PIED / Messagerie", "Paris // Minitel & Francophone Web", "Bilingual European travel & cultural listings"],
            ["Reel Out 16mm Film Collective", "SoHo, NYC & Toronto", "Archival 16mm & Super-8 underground screenings"],
            ["PGP Safe-Harbor Remailer Guide", "Worldwide // Cypherpunks Type-I", "Step-by-step privacy instructions for shared PCs"],
        ],
        "guestbook": [
            ("Alex_UK", "Manchester, UK", "1995-10-09", "Found your page from a terminal in the polytechnic library. Thank you for the PGP guide and the reading list."),
            ("M_Castro", "San Francisco, CA", "1995-10-02", "Anyone have the 9-minute 1984 Bobby O remix on 12-inch vinyl? Willing to trade a sealed TDK MA-R90 metal tape!"),
        ],
    },
    {
        "label": "GOVERNMENT",
        "slug": "interest-government",
        "hood": "Area51/Vault & Pentagon/Quarters",
        "hood_slug": "hood_area51-vault",
        "bg": "#050A05",
        "text": "#33FF33",
        "link": "#FFB000",
        "vlink": "#CC8800",
        "banner_color": "#113311",
        "title": "GeoCities Government — THE BLACK MAILBOX: FOIA Logs & Groom Lake Scanners",
        "curator": "Chuck 'DesertRat' Mercer (desertrat@intermind.net) // Hwy 375, Rachel, NV",
        "counter": "044719",
        "updated": "1995-10-14",
        "marquee": "*** ALERT: USAF CONDEMNATION OF FREEDOM RIDGE & WHITE SIDES PEAK TOOK EFFECT APRIL 1995 — USE TIKABOO PEAK TRAIL! ***",
        "lead": (
            "Since the Air Force seized 3,972 acres of public BLM land around Freedom Ridge "
            "this past April to block our telescopes, the perimeter watchers have moved 26 "
            "miles east to Tikaboo Peak (elevation 7,991 ft) and onto the World Wide Web. "
            "Here you'll find verified Realistic Pro-2006 UHF/VHF scanner frequencies, "
            "FOIA appeal templates (`5 U.S.C. § 552`), and declassified Defense communication "
            "relay maps."
        ),
        "ascii_title": "NELLIS RANGE / GROOM LAKE PERIMETER SCANNER BANK (PRO-2006)",
        "ascii_box": r"""  CH#   FREQUENCY     MOD   CALLSIGN / OBSERVED TRAFFIC
  ---------------------------------------------------------------------------
  01    118.400 MHz   AM    McCarran "JANET" Terminal Gate (737-200 Red Stripe)
  02    255.800 MHz   AM    Groom Lake Tower ("Dreamland" Control)
  03    138.300 MHz   FM    "Cammo Dude" Jeep Cherokee Perimeter Security Net
  04    004.625 MHz   USB   Shortwave Marker Anomaly (Cross-Modulation Log)
  05    409.675 MHz   FM    Nevada Test Site (NTS) Mercury Trunk Repeater""",
        "sections": [
            (
                "How to Write a Freedom of Information Act (FOIA) Request That Doesn't Get Binned",
                [
                    "Most amateurs write a two-page rambling letter asking for 'all files on secret "
                    "aircraft' and get rejected under the `b(1)` National Security and 'overly "
                    "broad' clauses. The secret to FOIA is requesting **contract numbers, environmental "
                    "impact assessments, and electrical substation work orders**. In March 1994, a "
                    "routine FOIA request for 1988–1989 commercial satellite transponder lease "
                    "invoices (`Operation PUBLIC HARMONY`) returned 14 pages of redacted trunk "
                    "routing sheets linking a Nevada microwave dish (`37.242°N, 115.810°W`) to a "
                    "private audio contractor in Los Angeles.",
                ],
            ),
            (
                "The Tikaboo Peak Packing List: Shooting 1000mm Mirror Lenses at Dawn",
                [
                    "If you hike Tikaboo Peak with a Celestron C90 1000mm f/11 spotting scope and "
                    "Kodak Ektachrome 400 pushed one stop, shoot between 05:45 and 06:30 AM before "
                    "the desert floor solar shimmer turns the Groom dry lakebed into soup.",
                ],
            ),
        ],
        "table_headers": ["FOIA Docket / Site", "Agency / Location", "Declassification Status (1995)"],
        "table_rows": [
            ["BLM Public Land Order 6986", "Dept. of Interior / Groom Range", "PUBLIC — 3,972 acres closed April 10, 1995"],
            ["Operation PUBLIC HARMONY (1988)", "USAF / Contract Audio Trunk", "PARTIAL — 85% redacted under Exemption (b)(1)"],
            ["AUTOVON / DSN Switch Directory", "Defense Info Systems Agency", "UNCLASSIFIED — Multi-level precedence & preemption"],
            ["Substation K-7704 Grid Fault", "UK/US Joint Academic Relay", "ARCHIVED — Referenced in Ashford Poly DSP logs"],
        ],
        "guestbook": [
            ("Scanner_Bob", "Tonopah, NV", "1995-10-12", "Logged six Janet 737 flights between 06:10 and 08:45 AM Tuesday on 118.400 MHz before they switched to UHF at the range boundary."),
            ("K_Vance", "Arlington, VA", "1995-10-04", "Your tip on requesting EPA hazardous-waste manifests instead of operational logs is pure gold."),
        ],
    },
    {
        "label": "HEALTH",
        "slug": "interest-health",
        "hood": "SiliconValley/Pines & Vienna/Waltz",
        "hood_slug": "hood_siliconvalley-lab",
        "bg": "#F2F9F6",
        "text": "#102820",
        "link": "#006644",
        "vlink": "#336655",
        "banner_color": "#004D33",
        "title": "GeoCities Health — CRT Refresh Rates, Model M Wrists & Late-Shift Ergonomics",
        "curator": "Dr. Nora Lindqvist (nlindqvist@ki.se) // Occupational Ergonomics & VDT Lab",
        "counter": "007419",
        "updated": "1995-10-09",
        "marquee": "*** CHECK YOUR MONITOR VERTICAL REFRESH RATE NOW: 60 HZ INTERLACED SVGA IS AN EYE-STRAIN HAZARD! ***",
        "lead": (
            "As millions of office workers and students move from paper desks to spending "
            "eight hours a day in front of 14-inch Cathode Ray Tubes (VDTs), occupational "
            "clinics are seeing an explosion of Repetitive Strain Injury (RSI) and 60 Hz "
            "flicker headaches. Here is evidence-based ergonomics for keyboard operators, "
            "audio engineers, and night-shift sysadmins."
        ),
        "ascii_title": "XFREE86 MODELINE CALCULATOR: 800x600 @ 75 HZ NON-INTERLACED",
        "ascii_box": r"""  # Add to /etc/XF86Config to eliminate 60Hz fluorescent beat-frequency flicker:
  # Name       DotClock   HTimings                 VTimings                 Flags
  Modeline "800x600_75"  49.50   800 816 896 1056   600 601 604 625  +HSync +VSync
  # WARNING: Verify your monitor supports 46.9 kHz Horizontal Sync first!""",
        "sections": [
            (
                "Why Your 60 Hz Monitor Fights Your Office Fluorescent Ballasts",
                [
                    "In North America, magnetic fluorescent ceiling ballasts flicker at 120 Hz "
                    "(twice the 60 Hz mains frequency); in Europe, they flicker at 100 Hz. When "
                    "your Windows 95 video driver defaults your S3 Trio64 card to `800x600 @ 60 Hz` "
                    "(or worse, `1024x768 @ 87 Hz Interlaced`), the phosphor decay beats against "
                    "the room lighting. Switching to **72 Hz or 75 Hz non-interlaced** reduces "
                    "subconscious pupillary oscillation by over 60%.",
                ],
            ),
            (
                "Hearing Conservation for Headphone Engineers: The 85 dBA SPL Rule",
                [
                    "Closed-back studio headphones like the Sony MDR-V6 have a razor-sharp 3 kHz "
                    "presence peak designed to reveal tape hiss. When monitoring shortwave static "
                    "or mastering tracks late at night, auditory fatigue tricks you into creeping "
                    "the headphone potentiometer up 6 dB every hour. Calibrate a known 80 dB SPL "
                    "pink-noise mark on your mixer and put a piece of white gaffer tape next to "
                    "the knob.",
                ],
            ),
        ],
        "table_headers": ["Keyboard / Input", "Actuation Force & Travel", "Ergonomic Verdict (1995)"],
        "table_rows": [
            ["IBM Model M (Part #1391401)", "65g Buckling Spring // 4.0mm", "Crisp tactile stop prevents bottoming out; loud!"],
            ["Microsoft Natural Keyboard (1994)", "55g Rubber Dome // Split 12°", "Excellent ulnar deviation relief; mushy spacebar"],
            ["Kinesis Contoured (Model 110)", "45g Cherry MX Brown // Concave bowls", "Gold standard for severe tendonitis ($390)"],
            ["Logitech TrackMan Marble (1995)", "Thumb optical trackball", "Eliminates shoulder abduction from reaching for mouse"],
        ],
        "guestbook": [
            ("Carpal_Coder", "Boston, MA", "1995-10-08", "Switched my ViewSonic 15G from 60Hz to 75Hz using your XF86Config modeline. My 4 PM headaches vanished in two days."),
            ("Audio_Dan", "Nashville, TN", "1995-10-01", "The gaffer-tape mark on the headphone amp knob is mandatory in our control room now."),
        ],
    },
    {
        "label": "KIDS",
        "slug": "interest-kids",
        "hood": "EnchantedForest/Glade & Heartland/Woods",
        "hood_slug": "hood_enchantedforest-glade",
        "bg": "#FFFACD",
        "text": "#000080",
        "link": "#FF0000",
        "vlink": "#800080",
        "banner_color": "#FF6600",
        "title": "GeoCities Kids — THE TREEHOUSE CLUB: Pogs, Slammers & KidPix Gallery!",
        "curator": "Toby (Age 11) & Meg (Age 14) (treehouse95@prodigy.com) // Eugene, Oregon",
        "counter": "012099",
        "updated": "1995-10-10",
        "marquee": "*** WELCOME TO THE TREEHOUSE!! DO NOT STEAL MY POG SCANS!! SIGN OUR GUESTBOOK OR ELSE!! :-) ***",
        "lead": (
            "Hi!! My name is Toby and my sister Meg helped me make the HTML tables so our "
            "mom would let us put this page on GeoCities! Here you can see my undefeated "
            "Pog slammer collection, Cheat Codes for <i>Sonic &amp; Knuckles</i>, and my "
            "5th-grade Science Fair project on TV static!"
        ),
        "ascii_title": "TOBY'S UNDEFEATED 1/2-INCH BRASS TORPEDO SLAMMER (DRAWN IN THE_DRAW)",
        "ascii_box": r"""          .-------.
       .-'  *   *  '-.     NAME: "THE ANNIHILATOR" (8-Ball Hologram Foil)
      /   \  \_/  /   \    WEIGHT: 3.2 Ounces Solid Knurled Brass
     |  *  | (8) |  *  |   RECORD AT RECESS: 44 Wins - 2 Losses
      \   /  / \  \   /    (Principal Miller banned it on October 3rd
       '-.  *   *  .-'      because it cracked the cafeteria linoleum!)
          '-------'""",
        "sections": [
            (
                "Official Eugene Elementary Bus #14 Pog Rules (No Finger-Tipping!)",
                [
                    "1. Maximum stack height is 10 milkcaps (5 from each player). No bent cardboard "
                    "caps from juice boxes allowed in "
                    "'for keeps' games!<br>"
                    "2. Two-finger edge-slamming is LEGAL, but if your slammer hits the floor "
                    "before the stack, it's a foul and you lose your turn.<br>"
                    "3. Metal saw-blade slammers with sharp teeth are banned because Kyle ripped "
                    "his starter jacket.",
                ],
            ),
            (
                "My Science Fair Project: Measuring Static From Our Sony Trinitron TV!",
                [
                    "When you turn off our 27-inch living room TV right after watching *Animaniacs*, "
                    "the glass screen makes a loud *CRACK-POP* sound and pulls all the hair on your "
                    "arm straight up! For my Science Fair project, I hung an aluminum-foil ball from "
                    "a silk thread in front of the screen. When the TV turns on, the high-voltage "
                    "flyback transformer charges the glass to 25,000 volts and launches the foil "
                    "ball 4 inches away!",
                ],
            ),
        ],
        "table_headers": ["Sega Genesis / SNES Game", "Toby's Rating", "Best Secret Code"],
        "table_rows": [
            ["Sonic 3 & Knuckles (Locked On!)", "10 / 10 STARS", "Left, Left, Left, Right, Right, Right, Up, Up, Up on mushroom pulley"],
            ["Donkey Kong Country (SNES)", "9.5 / 10 STARS", "Down, Y, Down, Down, Y at Cranky's cabin for 50 extra lives!"],
            ["EarthBound (SNES — Big Box!)", "10 / 10 STARS", "Scratch-and-sniff pizza card in the strategy guide smells like oregano"],
            ["SimCity 2000 (Mac LC III)", "9 / 10 STARS", "Type 'porntipsguzzardo' for $500,000 and all arcologies!"],
        ],
        "guestbook": [
            ("Skater_Zach", "Boise, ID", "1995-10-09", "Cool page Toby!! Our school banned Pogs completely last month so now everyone trades Magic: The Gathering Ice Age cards."),
            ("Grandma_Ruth", "Salem, OR", "1995-10-02", "Very proud of your science project Toby! Remember not to touch the back of the television set. Love, Grandma."),
        ],
    },
    {
        "label": "MUSIC",
        "slug": "interest-music",
        "hood": "SunsetStrip/Club & Nashville/Opry",
        "hood_slug": "hood_sunsetstrip-club",
        "bg": "#0D060E",
        "text": "#F2E6FF",
        "link": "#00FFCC",
        "vlink": "#FF66CC",
        "banner_color": "#330044",
        "title": "GeoCities Music — ANALOG & ARENA: The Heartstrike Archive & Vintage Synth Rigs",
        "curator": "Rick 'Fretless' Morales (rmorales@primenet.com) // Sunset Strip & Cherokee Studios",
        "counter": "073815",
        "updated": "1995-10-14",
        "marquee": "*** NEW SYSEX UPLOAD: EXACT YAMAHA DX7 + JUNO-106 PATCH DUMP FROM HEARTSTRIKE'S 1986 MONTERREY SOUNDCHECK ***",
        "lead": (
            "Dedicated to the golden era of high-voltage analog/FM hybrid rock and synth-pop "
            "(1983–1990): before corporate labels replaced live rhythm sections and 2-inch "
            "Studer A800 tape machines with sterile presets. Home to the complete "
            "<b><i>Heartstrike</i></b> tour bootleg database, vintage Roland/Yamaha synth "
            "service notes, and cassette bias calibration guides."
        ),
        "ascii_title": "HEARTSTRIKE 1986 STAGE SYNTH & GUITAR SIGNAL CHAIN (VANCE / TAKAHASHI)",
        "ascii_box": r"""  [KRAMER BARETTA] ---> [ADA MP-1 TUBE PREAMP] ---> [ROLAND SDE-3000 DELAY (380ms)]
                                                            |
  [YAMAHA DX7 II-FD] -> [ROLAND JUNO-106 (CHORUS II)] ------+--> [SSL 4000E BUS]
  (MIDI CH 1: E.PIANO    (BBD MN3009 analog bucket-brigade       (15 IPS Studer A800
   detuned +7 cents)      warmth under the FM attack transient!)  w/ Dolby SR)""",
        "sections": [
            (
                "How 'Heartstrike' Built the Wall of Sound on 'Chrome Velocity' (1985) and 'Steel Thunder' (1987)",
                [
                    "People who only heard <b><i>Heartstrike</i></b> on compressed AM car radios "
                    "think they were just another Sunset Strip arena band. Put on an original 1985 "
                    "Orion first pressing of <i>Chrome Velocity</i> or the 1987 <i>Steel Thunder</i> "
                    "12-inch promo single of <i>'Run With The Fire'</i>: keyboardist Kenji Voss "
                    "triggered a Yamaha TX816 rack (eight individual DX7 modules!) panned hard "
                    "left/right into a pair of Roland Dimension D SDD-320 chorus units, while "
                    "the kick drum keyed an analog noise gate on the bass synth.",
                ],
            ),
            (
                "The 1990 Corporate Purge: Why We Still Boycott 'Glass Hours'",
                [
                    "By early 1990, Orion Records' new executive suite decided that real studio "
                    "engineers, expensive 2-inch magnetic tape, and unpredictable artists were "
                    "bad for quarterly margins. They dropped half the Sunset Strip rock roster, "
                    "shuttered Sublevel B2, and spent $2 million promoting <b>Luna Gray's</b> "
                    "<i>Glass Hours</i> (released April 12, 1990)—an album so scrubbed of "
                    "sub-bass dynamics and human tape bleed it sounds like an elevator demo ROM.",
                ],
            ),
        ],
        "table_headers": ["Bootleg / Pressing", "Date & Venue", "Lineage & Sound Quality"],
        "table_rows": [
            ["Heartstrike — Live in Monterrey", "1986-11-14 // Monterrey, MX", "Soundboard -> Sony WM-D6C (Type II CrO2) // Grade: A+"],
            ["Heartstrike — Budokan Final Night", "1986-04-22 // Tokyo, Japan", "FM Broadcast (NHK-FM) -> Nakamichi Dragon // Grade: A"],
            ["Heartstrike — Sunset Strip Demo Reel", "1984-08-09 // Gazzarri's / Cherokee", "2nd-gen TDK SA-X90 dub // Unreleased intro on 'Static & Steel'"],
            ["Steel Thunder OST (12-Inch Promo)", "1987-06-19 // Orion Records PRO-87", "45 RPM 180g audiophile cut; +4 dB hotter than retail LP"],
        ],
        "guestbook": [
            ("Elena_V", "Coyoacán, Mexico DF", "1995-10-13", "My older brother recorded that 1986 Monterrey cassette from the mixing tower! Still plays crisp on our Technics deck."),
            ("Juno_Tech", "Stockholm, Sweden", "1995-10-07", "Loaded your DX7 + Juno-106 layer patch via MIDI-OX. That metallic attack into the BBD chorus is the exact '86 sound!"),
        ],
    },
    {
        "label": "PEOPLE",
        "slug": "interest-people",
        "hood": "Colosseum/Field & BourbonStreet/Square",
        "hood_slug": "hood_colosseum-field",
        "bg": "#F9F5EC",
        "text": "#1A1A1A",
        "link": "#004488",
        "vlink": "#553366",
        "banner_color": "#1F4E78",
        "title": "GeoCities People — The Global Postcard & C-90 Soundscape Pen-Pal Registry",
        "curator": "Eleni Papadopoulos (elenip@forthnet.gr) // Heraklion & Athens",
        "counter": "022610",
        "updated": "1995-10-12",
        "marquee": "*** 142 ACTIVE PEN-PALS ACROSS 34 COUNTRIES // NO CHAIN LETTERS OR MLM PYRAMIDS ALLOWED! ***",
        "lead": (
            "E-mail takes four seconds to cross the ocean, which is wonderful—and also why "
            "it feels weightless. The Global C-90 &amp; Postcard Registry pairs people in "
            "different time zones who still love pulling a battered airmail padded envelope "
            "out of the postbox containing a handwritten letter, two local tram tickets, and "
            "a 90-minute cassette recording of what their town actually sounds like."
        ),
        "ascii_title": "THE '60 / 30' HOMETOWN SOUNDSCAPE CASSETTE FORMULA (TDK SA-90)",
        "ascii_box": r"""  SIDE A (45 MIN):  Local FM/AM Radio Surf at Midnight (leave the DJ weather
                    reports, local car-dealership jingles, & station IDs IN!)
  SIDE B (00-15m):  Your favourite local unsigned band or kitchen table song
  SIDE B (15-45m):  Unedited Window-Sill Microphone Recording (Rain on tin
                    roof, harbor ferries, cicadas, or morning bakery delivery)""",
        "sections": [
            (
                "Why We Record the Weather Forecast and the Ferry Horn (Anemoia in Practice)",
                [
                    "Last month I received a Maxell XLII-90 in the post from a tram driver in "
                    "Gothenburg, Sweden. Side B was thirty minutes of his cassette recorder sitting "
                    "on the dashboard of Tram #7 during an October sleet storm: the rhythmic "
                    "*clack-clack* of the relay contactors, the pneumatic hiss of the folding doors, "
                    "and passengers shaking out wet umbrellas. Listening to it on headphones in "
                    "sunny Crete gave me homesickness for a rainy Swedish street corner I have "
                    "never stood on in my life.",
                ],
            ),
            (
                "How to Use International Reply Coupons (IRCs) & Avoid Customs Tape X-Rays",
                [
                    "When mailing cassettes across borders, always write `MAGNETIC AUDIO TAPE — "
                    "DO NOT X-RAY // NO COMMERCIAL VALUE` in thick black marker on both sides of "
                    "the Jiffy bag, and wrap the cassette shell in a layer of kitchen aluminum "
                    "foil just in case.",
                ],
            ),
        ],
        "table_headers": ["Pen-Pal Handle & City", "Languages Written", "Seeking Swap Of"],
        "table_rows": [
            ["Eleni P. — Heraklion, Crete (Greece)", "Greek, English, basic French", "Harbor/train ambient recordings & local newspaper comics"],
            ["Kenji T. — Akasaka, Tokyo (Japan)", "Japanese, English", "Yamanote Line station melodies & 80s synth-pop C-90s"],
            ["Marek W. — Gdańsk (Poland)", "Polish, German, English", "Baltic marine weather bulletins & shipyard brass bands"],
            ["Lucia R. — Montevideo (Uruguay)", "Spanish, Portuguese, English", "Rio de la Plata shortwave tangos & thunderstorm tapes"],
        ],
        "guestbook": [
            ("Bram_NL", "Utrecht, Netherlands", "1995-10-11", "Eleni, your cassette of the Heraklion ferry port arrived today! The bouzouki bleed from the taverna downstairs is magic."),
            ("Sanne_SE", "Gothenburg, Sweden", "1995-10-04", "Glad Tram #7 made it to Greece intact! Recording Side A of the autumn tape this weekend."),
        ],
    },
    {
        "label": "RECREATION",
        "slug": "interest-recreation",
        "hood": "CapeCanaveral/Station & Heartland/Plains",
        "hood_slug": "hood_capecanaveral-lab",
        "bg": "#0A141E",
        "text": "#D0E8FF",
        "link": "#66CCFF",
        "vlink": "#6699CC",
        "banner_color": "#102A44",
        "title": "GeoCities Recreation — DXING THE GRAYLINE: Shortwave, Boatanchors & Night Trains",
        "curator": "Walter 'W9DX' Kestrel (w9dx@arrl.org) // Rural Wisconsin & Dayton Hamvention",
        "counter": "031048",
        "updated": "1995-10-13",
        "marquee": "*** SOLAR MINIMUM PROPAGATION: 160M & 80M TROPICAL BANDS WIDE OPEN AT 02:14 UTC GRAYLINE! ***",
        "lead": (
            "As we head into the 1995–1996 sunspot minimum (Solar Cycle 22 winding down), "
            "the upper HF bands (15m and 10m) may go quiet after sunset, but the lower "
            "shortwave bands (60m, 80m, and 49m between 3.2 and 7.3 MHz) are delivering "
            "astonishing low-noise trans-oceanic propagation. Grab your soldering iron, "
            "warm up the tubes on your Collins R-390A, and string a Beverage wire!"
        ),
        "ascii_title": "500-FOOT UNIDIRECTIONAL BEVERAGE RECEIVING ANTENNA (FENCEPOST RIG)",
        "ascii_box": r"""  [9:1 MATCHING XFMR]==============================[470-OHM NON-INDUCTIVE]
   |                  500 ft #16 AWG Copperweld      |  CARBON TERMINATION
   v                  strung 6 ft high on wooden     v  (Points toward
  50-Ohm RG-8X        pasture fenceposts!           [GND] target azimuth!)
  to Receiver         ---[8 ft Copper Ground Rod]---""",
        "sections": [
            (
                "Logging Coastal Morse Stations Before the 1999 GMDSS Satellite Cutoff",
                [
                    "The International Maritime Organization has mandated that commercial ships "
                    "phase out hand-keyed 500 kHz and HF Morse code by February 1999 in favor of "
                    "GMDSS satellite terminals. Right now, in October 1995, you can still tune "
                    "between `6,477.5 kHz` and `8,658 kHz` at midnight and hear the master operators "
                    "at **KPH (Point Reyes, CA)**, **WCC (Chatham, MA)**, and **DAN (Norddeich Radio)** "
                    "sending 28-word-per-minute weather advisories on Vibroplex bug keys. Record "
                    "them onto cassette now while they still rule the ocean.",
                ],
            ),
            (
                "Restoring the Collins R-390A/URR: Mechanical Filters & Ballast Tubes",
                [
                    "If you pick up a surplus 85-pound Collins R-390A receiver at the Dayton "
                    "Hamvention flea market, do NOT power it up before replacing the `C551` "
                    "0.01 uF paper coupling capacitor on the mechanical filter deck! If `C551` "
                    "leaks DC plate voltage into the magnetostrictive transducer coil, it will "
                    "melt an irreplaceable 455 kHz mechanical filter in thirty seconds.",
                ],
            ),
        ],
        "table_headers": ["Frequency (kHz)", "Station / Beacon", "Best Grayline Window (UTC)"],
        "table_rows": [
            ["3,330.0 kHz (CHU)", "Ottawa Time Signal (Bilingual Voice + FSK)", "00:00 - 11:00 UTC across North America"],
            ["4,625.0 kHz (UVB-76)", "Leningrad / Povarovo Buzzer & Voice Relay", "02:00 - 02:30 UTC (Watch for 110-baud sidebands)"],
            ["5,000.0 kHz (WWV / WWVH)", "Fort Collins & Kauai Propagation Announcements", "Minute :18 (Geo-alert solar flux K-index)"],
            ["6,477.5 kHz (KPH)", "Point Reyes Maritime CW Traffic List", "02:00 & 05:00 UTC (750 Hz BFO pitch)"],
        ],
        "guestbook": [
            ("SM5_Lars", "Uppsala, Sweden", "1995-10-12", "Strung a 180-meter Beverage wire pointing 310 degrees across my neighbour's barley field. Copied KPH on 8642 kHz at S5!"),
            ("VE3_Tubes", "Ottawa, ON", "1995-10-05", "Saved my 1961 EAC R-390A with your C551 capacitor warning. Measured 42V DC leaking across the old Sprague Vitamin Q cap!"),
        ],
    },
    {
        "label": "SCIENCE FICTION",
        "slug": "interest-scifi",
        "hood": "Area51/Nebula & EnchantedForest/Tower",
        "hood_slug": "hood_area51-vault",
        "bg": "#060414",
        "text": "#D8D0FF",
        "link": "#00E5FF",
        "vlink": "#9966FF",
        "banner_color": "#1E0B4B",
        "title": "GeoCities Science Fiction — NEON & ORBIT: Paperback Art, B5 & Cyberpunk",
        "curator": "Galen Vance (gvance@panix.com) // Brooklyn & rec.arts.sf.written",
        "counter": "049103",
        "updated": "1995-10-14",
        "marquee": "*** BABYLON 5 SEASON 3 PREMIERE COUNTDOWN: 'MATTERS OF HONOR' AIRS NOVEMBER 6, 1995! ***",
        "lead": (
            "A sanctuary for readers who judge paperbacks by their 1978 Chris Foss airbrushed "
            "spaceship covers, tape every episode of <i>Babylon 5</i> on Super-VHS to freeze-frame "
            "the NewTek LightWave 3D battle sequences, and argue on `rec.arts.sf.written` "
            "about whether neural networks could ever wake up inside a distributed packet switch."
        ),
        "ascii_title": "O'NEILL CYLINDER L5 HABITAT CORIOLIS & SPIN GRAVITY TABLE",
        "ascii_box": r"""       . - ~ ~ ~ - .
    , '      |      ' ,    RADIUS (R) = 3,200 meters // LENGTH = 32 km
   /         | R       \   ROTATION   = 0.525 RPM (~1 revolution / 114 sec)
  |          +--------->|  RIM GRAVITY: a = w^2 * R = 9.81 m/s^2 (1.0 G)
   \                   /   WARNING: Throwing a baseball spinward increases
    ' ,             , '    apparent weight by +14% due to 2*m*(w x v)!
       ' - _ _ _ - '""",
        "sections": [
            (
                "How Eight Amiga 2000s with Video Toasters Beat $200,000 Mainframes on 'Babylon 5'",
                [
                    "Traditional network executives laughed in 1993 when Foundation Imaging announced "
                    "they would render every Starfury fighter and the 5-mile-long Babylon 5 station "
                    "on networked Commodore Amiga 2000s and 486 render nodes running NewTek LightWave 3D "
                    "instead of shooting physical motion-control models. Yet because LightWave obeys "
                    "Newtonian zero-G thruster physics, a Starfury cutting its main engines and "
                    "pivoting 180 degrees on RCS thrusters looks more authentic than anything "
                    "in a $60 million theatrical release.",
                ],
            ),
            (
                "Cyberpunk Paperbacks vs. Actual 1995 UNIX Networking: A Reality Check",
                [
                    "In 1984, William Gibson's <i>Neuromancer</i> imagined hackers jacking into a "
                    "neon 3D consensual hallucination using an Ono-Sendai deck. Eleven years later, "
                    "what does real cyberspace look like? It looks like a monochrome 80x24 `xterm` "
                    "window, a noisy 28.8k modem carrier, and 300,000 personal homepages stitched "
                    "together by hand-coded HTML links. Honestly? We prefer the real version—because "
                    "nobody Corporate owns the root index.",
                ],
            ),
        ],
        "table_headers": ["Book / Series", "Author / Year", "Essential Edition to Hunt Used"],
        "table_rows": [
            ["Neuromancer / Count Zero", "William Gibson (1984 / 1986)", "1st Ace Paperback w/ Rick Berry cover art ($2.95 cover price)"],
            ["A Fire Upon the Deep", "Vernor Vinge (1992)", "Tor Hardcover — Features 'The Net of a Million Lies' (Usenet in space!)"],
            ["Snow Crash", "Neal Stephenson (1992)", "Bantam Spectra Trade Paperback ( pixelated face cover )"],
            ["The Stars My Destination", "Alfred Bester (1956 / 1979)", "Panther UK Paperback w/ Chris Foss diagonal checkerboard freighter"],
        ],
        "guestbook": [
            ("JMS_Lurker", "Pasadena, CA", "1995-10-13", "JMS just replied to my post on rastb5m! Season 3 is going to blow the roof off the Shadow war."),
            ("Foss_Collector", "Bristol, UK", "1995-10-06", "Found four 1977 Panther Asimov paperbacks with wrap-around Chris Foss covers at an Oxfam shop for 20p each!"),
        ],
    },
]


def compute_public_urls(repo_root: Path) -> dict[str, str]:
    """Uses deploy/urlmap.js via Node to compute the exact publicUrl() for all 20 interest slugs & neighborhoods."""
    import shutil
    node_bin = shutil.which("node") or "/opt/homebrew/bin/node"
    urlmap_uri = (repo_root / "deploy" / "urlmap.js").resolve().as_uri()
    script = """
import(%s).then(({ publicUrl }) => {
  const slugs = %s;
  const out = {};
  for (const s of slugs) {
    out[s] = publicUrl("geocities/" + s + ".html");
  }
  out["geocities/index.html"] = publicUrl("geocities/index.html");
  out["geocities/hollywood-hills-4127.html"] = publicUrl("geocities/hollywood-hills-4127.html");
  out["geocities/dir-index.html"] = publicUrl("geocities/dir-index.html");
  console.log(JSON.stringify(out));
});
""" % (
        json.dumps(urlmap_uri),
        json.dumps([s["slug"] for s in INTEREST_SPECS] + list({s["hood_slug"] for s in INTEREST_SPECS})),
    )
    res = subprocess.run([node_bin, "-e", script], check=True, capture_output=True, text=True)
    return json.loads(res.stdout.strip())


def render_interest_page(spec: dict, urls: dict[str, str]) -> str:
    quick_links = " &middot; ".join(
        f'<B>{html.escape(s["label"])}</B>'
        if s["slug"] == spec["slug"]
        else f'<A HREF="{html.escape(urls[s["slug"]])}">{html.escape(s["label"])}</A>'
        for s in INTEREST_SPECS
    )

    sections_html = []
    for heading, paragraphs in spec["sections"]:
        sections_html.append(f'<H2><FONT FACE="Arial,Helvetica">{html.escape(heading)}</FONT></H2>')
        for p in paragraphs:
            sections_html.append(f"<P>{p}</P>")

    rows_html = []
    for r in spec["table_rows"]:
        cells = "".join(f"<TD><FONT SIZE=2>{html.escape(c)}</FONT></TD>" for c in r)
        rows_html.append(f"<TR>{cells}</TR>")
    headers_html = "".join(
        f"<TH ALIGN=LEFT><FONT FACE='Arial,Helvetica' SIZE=2>{html.escape(h)}</FONT></TH>"
        for h in spec["table_headers"]
    )

    gb_html = []
    for who, where, dt, msg in spec["guestbook"]:
        gb_html.append(
            f"<TR><TD><FONT SIZE=2><B>{html.escape(who)}</B> ({html.escape(where)}) &middot; "
            f"<I>{html.escape(dt)}</I></FONT><BR>{html.escape(msg)}</TD></TR>"
        )

    counter_cells = "".join(
        f'<TD BGCOLOR="#000000"><FONT FACE="Courier New,Courier" COLOR="#33FF33"><B>{d}</B></FONT></TD>'
        for d in spec["counter"]
    )

    hood_url = urls.get(spec["hood_slug"], urls["geocities/dir-index.html"])
    geo_index_url = urls["geocities/index.html"]
    ring_home_url = urls["geocities/hollywood-hills-4127.html"]
    dir_index_url = urls["geocities/dir-index.html"]

    return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<HTML LANG="en"><HEAD><TITLE>{html.escape(spec["title"])}</TITLE>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
<META NAME="description" CONTENT="{html.escape(spec["title"])} — Curated by {html.escape(spec["curator"])}">
</HEAD>
<BODY BGCOLOR="{spec["bg"]}" TEXT="{spec["text"]}" LINK="{spec["link"]}" VLINK="{spec["vlink"]}" ALINK="#FF0000">
<CENTER>
<!-- Top Yellow GeoCities Navigation Bar -->
<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 WIDTH="720" BGCOLOR="#FFCC00">
<TR>
  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="https://stardust-archive.net/" STYLE="color:#000000; text-decoration:none;">&nbsp;Main&nbsp;</A></B></FONT></TD>
  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="{html.escape(geo_index_url)}" STYLE="color:#000000; text-decoration:none;">&nbsp;Homestead Directory&nbsp;</A></B></FONT></TD>
  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="{html.escape(hood_url)}" STYLE="color:#000000; text-decoration:none;">&nbsp;{html.escape(spec["hood"])}&nbsp;</A></B></FONT></TD>
  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="{html.escape(dir_index_url)}" STYLE="color:#000000; text-decoration:none;">&nbsp;All Suburbs&nbsp;</A></B></FONT></TD>
  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="{html.escape(ring_home_url)}" STYLE="color:#000000; text-decoration:none;">&nbsp;Webring Home&nbsp;</A></B></FONT></TD>
</TR>
</TABLE>

<!-- Interest Category Switchboard -->
<TABLE BORDER=1 CELLPADDING=4 CELLSPACING=0 WIDTH="720" BGCOLOR="#EEEEEE">
<TR><TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE=1 COLOR="#000000">
  <B>GEOCITIES INTEREST COMMONS:</B> {quick_links}
</FONT></TD></TR>
</TABLE>

<TABLE WIDTH="720" BORDER=0 CELLPADDING=6 CELLSPACING=0><TR><TD>
<CENTER>
  <TABLE BORDER=2 CELLPADDING=6 CELLSPACING=0 WIDTH="100%" BGCOLOR="{spec["banner_color"]}">
    <TR><TD ALIGN=CENTER>
      <FONT FACE="Arial Black,Arial,Helvetica" SIZE=4 COLOR="#FFFFFF"><B>{html.escape(spec["title"])}</B></FONT><BR>
      <FONT FACE="Courier New,Courier" SIZE=2 COLOR="#FFCC00"><B>Curator: {html.escape(spec["curator"])} &middot; Updated: {spec["updated"]}</B></FONT>
    </TD></TR>
  </TABLE>
  <BR>
  <MARQUEE BEHAVIOR=SCROLL SCROLLAMOUNT=4 WIDTH="92%"><FONT FACE="Courier New,Courier" SIZE=2><B>{html.escape(spec["marquee"])}</B></FONT></MARQUEE>
</CENTER>

<P>{spec["lead"]}</P>

<H3><FONT FACE="Courier New,Courier">[ {html.escape(spec["ascii_title"])} ]</FONT></H3>
<PRE>{html.escape(spec["ascii_box"])}</PRE>

{"".join(sections_html)}

<H2><FONT FACE="Arial,Helvetica">Curated {html.escape(spec["label"].title())} Directory &amp; Reference Matrix (1995)</FONT></H2>
<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%">
  <TR BGCOLOR="{spec["banner_color"]}">{headers_html}</TR>
  {"".join(rows_html)}
</TABLE>

<H2><FONT FACE="Arial,Helvetica">Recent Guestbook Entries</FONT></H2>
<TABLE BORDER=1 CELLPADDING=5 CELLSPACING=0 WIDTH="100%">
  {"".join(gb_html)}
</TABLE>

<HR SIZE=2 NOSHADE>
<CENTER>
  <P><FONT SIZE=2>Visitor Counter since March 1995:</FONT><BR>
  <TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0><TR>{counter_cells}</TR></TABLE></P>
  <P><FONT SIZE=2>[ <A HREF="{html.escape(geo_index_url)}">&lt;&lt; Back to GeoCities Homestead Directory</A> |
  <A HREF="{html.escape(hood_url)}">Explore {html.escape(spec["hood"])}</A> |
  <A HREF="{html.escape(dir_index_url)}">Browse All 78 Suburbs</A> |
  <A HREF="https://stardust-archive.net/">WWW Virtual Library</A> ]</FONT></P>
  <P><FONT SIZE=1>Hosted Free by <B>GeoCities</B> &middot; Best viewed with Netscape Navigator 2.0 at 800x600 &middot; CERN-HTTPd/3.0</FONT></P>
</CENTER>
</TD></TR></TABLE>
</CENTER>
</BODY></HTML>
"""


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    site_geo_dir = repo_root / "site" / "geocities"
    site_geo_dir.mkdir(parents=True, exist_ok=True)

    urls = compute_public_urls(repo_root)
    pages_by_slug: dict[str, str] = {}

    for spec in INTEREST_SPECS:
        html_out = render_interest_page(spec, urls)
        out_file = site_geo_dir / f"{spec['slug']}.html"
        out_file.write_text(html_out, encoding="utf-8")
        pages_by_slug[spec["slug"]] = html_out
        print(f"[INTEREST_BUILDER] Wrote {out_file.name} ({len(html_out)} bytes) -> {urls[spec['slug']]}")

    idx_path = site_geo_dir / "index.html"
    if idx_path.exists():
        raw_index = idx_path.read_text(encoding="utf-8")
    elif Path("/tmp/b").exists():
        raw_index = Path("/tmp/b").read_text(encoding="utf-8")
    else:
        raw_index = ""

    if raw_index:
        for spec in INTEREST_SPECS:
            label_html = spec["label"].replace("&", "&amp;")
            old_tag = f'<A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">{label_html}</A>'
            new_tag = f'<A HREF="{urls[spec["slug"]]}" STYLE="color:#CC0000; text-decoration:underline;">{label_html}</A>'
            if old_tag in raw_index:
                raw_index = raw_index.replace(old_tag, new_tag, 1)
        idx_path.write_text(raw_index, encoding="utf-8")
        print("[INTEREST_BUILDER] Patched site/geocities/index.html with all 20 active interest links!")

    label_to_url = {spec["label"]: urls[spec["slug"]] for spec in INTEREST_SPECS}
    interests_js = (
        "// Auto-generated 1995-1996 GeoCities Interest Pages & Edge Link Rewriter (Anemoia Worldbuilding)\n"
        f"export const INTEREST_PAGES = {json.dumps(pages_by_slug)};\n"
        f"export const INTEREST_LABEL_URLS = {json.dumps(label_to_url)};\n"
    )
    deploy_dir = repo_root / "deploy"
    deploy_dir.mkdir(parents=True, exist_ok=True)
    (deploy_dir / "interests.js").write_text(interests_js, encoding="utf-8")
    print(f"[INTEREST_BUILDER] Wrote {deploy_dir / 'interests.js'}")


if __name__ == "__main__":
    main()

