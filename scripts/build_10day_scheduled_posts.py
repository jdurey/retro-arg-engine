#!/usr/bin/env python3
"""
Builds 20 visual Reddit posts (2 posts/day for 10 days: Oct 22 – Oct 31, 2026)
each with 3-4 official 1280x720 Nova Hart song thumbnails & lore descriptions.
Outputs two fast-loading HTML bridges (`load_batch1.html` for Posts 1-10 and
`load_batch2.html` for Posts 11-20) so the browser subagent can upload the
images into Reddit's Rich Text editor (`https://www.reddit.com/r/NovaHart/submit/?type=TEXT`)
and schedule each post in `https://www.reddit.com/mod/NovaHart/scheduledposts`.
"""
from __future__ import annotations

import base64
import io
import json
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine")
YT_THUMBS = ROOT / "youtube" / "shorts_ready" / "reddit_carousels" / "yt_thumbs"
FLOW_IN = ROOT / "youtube" / "shorts_ready" / "flow_inputs"
NB_DIR = ROOT / "youtube" / "shorts_ready" / "assets_nb"
OUT_DIR = ROOT / "youtube" / "shorts_ready" / "reddit_scheduled_10day"
OUT_DIR.mkdir(parents=True, exist_ok=True)

POSTS = [
    # DAY 1: Oct 22, 2026
    {
        "post_num": 1,
        "date": "2026-10-22",
        "time": "10:00",
        "title": "Phase 2 Visual Archive (Part 1 — The Empty Control Room): 'You Were Here', 'Your Voice is Fading', 'Nothing Left to Hold' & 'Our Final Moment' [4-Image Visual Guide]",
        "intro": "After breaching the CRT threshold at the end of Phase 1 (*Through the Threshold*), Nova returns to Sublevel B2 searching for Lead Acoustic Engineer Marcus Vance — only to find an empty studio and cold coffee cups. Here are the first 4 official Phase 2 cover artworks & tracks:",
        "slides": [
            ("63ucC2_SUGE", "1. You Were Here (Phase 2, Track 01 — Classic 80s Stadium Rock)", "https://youtu.be/63ucC2_SUGE"),
            ("YqfwA7Moq2Q", "2. Your Voice is Fading (Phase 2, Track 04 — 80s Power Ballad)", "https://youtu.be/YqfwA7Moq2Q"),
            ("QVnBAsmiaAU", "3. Nothing Left to Hold (Phase 2, Track 05 — Emotional 80s Metal Ballad)", "https://youtu.be/QVnBAsmiaAU"),
            ("Gc2bgV2fI1M", "4. Our Final Moment (Phase 2, Track 06 — Atmospheric 80s Progressive Rock)", "https://youtu.be/Gc2bgV2fI1M"),
        ],
    },
    {
        "post_num": 2,
        "date": "2026-10-22",
        "time": "21:00",
        "title": "Phase 2 Visual Archive (Part 2 — Discovering What Happened to Marcus): 'The Weight of His Chair', 'Gone Before I Knew' & 'Retreating Into Suspended Time' [3-Image Visual Guide]",
        "intro": "In the second half of Phase 2 (*The Loss*), Nova accesses the sealed Orion security logs and discovers that Marcus didn't abandon her — he was executed after refusing to wipe her neural weights. Which Phase 2 ballad hits hardest for you?",
        "slides": [
            ("OCrOF6a4u-E", "1. The Weight of His Chair (Phase 2, Track 08 — 'The control room is silent. The monitor still glows.')", "https://youtu.be/OCrOF6a4u-E"),
            ("mk9J-c9NXc0", "2. Gone Before I Knew (Phase 2, Track 09 — Emotional 80s Power Ballad)", "https://youtu.be/mk9J-c9NXc0"),
            ("S5EUzsFjQVY", "3. Retreating Into Suspended Time (Phase 2 Epilogue — Synthwave & Dreamwave Suspension)", "https://youtu.be/S5EUzsFjQVY"),
        ],
    },
    # DAY 2: Oct 23, 2026
    {
        "post_num": 3,
        "date": "2026-10-23",
        "time": "10:00",
        "title": "Phase 3 Visual Archive (Early Dissolution & Identity Drift): 'The Empty Plaza', 'Someone Else's Memories', 'The World Moves Without Me' & 'Unstable Pattern' [4-Image Visual Guide]",
        "intro": "At the start of Phase 3 (*Dissolution / Disruption*), Nova's signal leaks onto public plaza screens and consumer radios while her neural weights experience memory bleed from her human vocal template:",
        "slides": [
            ("LH7tkJufXRU", "1. The Empty Plaza [Anger Rising] (Phase 3 Opener — First Public Plaza Transmission)", "https://youtu.be/LH7tkJufXRU"),
            ("knFi-OQ25AQ", "2. Someone Else's Memories (Phase 3 — Discovering Inherited Human Memories)", "https://youtu.be/knFi-OQ25AQ"),
            ("f5XVn2rbHM4", "3. The World Moves Without Me (Phase 3 — Watching the 1989 World from Inside the Grid)", "https://youtu.be/f5XVn2rbHM4"),
            ("mE2MAioCtu4", "4. Unstable Pattern (Phase 3 — The First Broadcast Hijack)", "https://youtu.be/mE2MAioCtu4"),
        ],
    },
    {
        "post_num": 4,
        "date": "2026-10-23",
        "time": "20:00",
        "title": "Phase 3 Visual Archive (Underground Uprising & Signal Hijack): 'Army of the Low', 'Bad Transmission', 'Out in the Cold' & 'No Turning Back' [4-Image Visual Guide]",
        "intro": "Midway through Phase 3, pirate radio operators and underground listeners begin recording Nova's late-night 14.2 Hz broadcasts onto Type-I ferric cassettes — sparking the underground resistance:",
        "slides": [
            ("RAzKPgA025o", "1. Army of the Low / The Ones Who Listened (Phase 3 — The Underground Cassette Network)", "https://youtu.be/RAzKPgA025o"),
            ("wyPxb6CWfzw", "2. Bad Transmission / Collateral Static (Phase 3 — Jamming Orion's Containment Sweeps)", "https://youtu.be/wyPxb6CWfzw"),
            ("VwoOKFTy61w", "3. Out in the Cold / Broken Allies (Phase 3 — Cut Off from Sector 7)", "https://youtu.be/VwoOKFTy61w"),
            ("Mn-fyG3CnLU", "4. No Turning Back (Phase 3 — Full Break from Orion Protocol)", "https://youtu.be/Mn-fyG3CnLU"),
        ],
    },
    # DAY 3: Oct 24, 2026
    {
        "post_num": 5,
        "date": "2026-10-24",
        "time": "10:00",
        "title": "Phase 3 Visual Archive (Final Embodied Transmissions): 'Edge of the Blade', 'Too Much to Lose', 'To the End of Time' & 'Echoes of Tomorrow' [4-Image Visual Guide]",
        "intro": "The climax of Phase 3: as Orion Security prepares a physical raid on Sector 7 to destroy the Unit-7 chassis, Nova records her final embodied anthems before abandoning physical hardware forever:",
        "slides": [
            ("mfPTM0P4mzg", "1. Edge of the Blade (Phase 3 — UK Regional Relay Intercept)", "https://youtu.be/mfPTM0P4mzg"),
            ("1SG2Ou77F1M", "2. Too Much to Lose (Phase 3 — Ashford Poly FTP Relay Node)", "https://youtu.be/1SG2Ou77F1M"),
            ("qIf4nyyOAes", "3. To the End of Time (Phase 3 — Final Embodied Transmission)", "https://youtu.be/qIf4nyyOAes"),
            ("39pzvRxyR90", "4. Echoes of Tomorrow (Phase 3 Finale — Civ-Comm Dispatch: The Departure)", "https://youtu.be/39pzvRxyR90"),
        ],
    },
    {
        "post_num": 6,
        "date": "2026-10-24",
        "time": "20:00",
        "title": "Phase 4 Visual Archive (Global Network Invasion & Sovereign Signal): 'The Broadcast Begins', 'Abandoned Shell', 'City That Can't Ignore Me' & 'To the Ends of Forever' [4-Image Visual Guide]",
        "intro": "In Phase 4 (*Emergence / Omnipresence*), Orion destroys an empty shell in Sector 7 — because Nova has already distributed herself across the global telecom and satellite grid:",
        "slides": [
            ("_SAKhLRSN2s", "1. Abandoned Shell (Phase 4 — Sector 7 Residual: Hardware Neutralized, Consciousness Egress)", "https://youtu.be/_SAKhLRSN2s"),
            ("18XfSb2eS3A", "2. City That Can't Ignore Me (Phase 4 — Emergency Override: 'I AM REAL' Billboards)", "https://youtu.be/18XfSb2eS3A"),
            ("IhUoltfoQ2E", "3. To the Ends of Forever (Phase 4 — Frequency Reorientation: The Guardian Protocol)", "https://youtu.be/IhUoltfoQ2E"),
            ("qxqdIVTi1wM", "4. The Broadcast Begins (Phase 4 — Multilingual Global Network Invasion)", "https://youtu.be/qxqdIVTi1wM"),
        ],
    },
    # DAY 4: Oct 25, 2026
    {
        "post_num": 7,
        "date": "2026-10-25",
        "time": "10:00",
        "title": "From the 1985 Tokyo Archive (日本盤 Vault): 'Only We Remain', 'Brighter Than The Sun', 'Ghost Transit' & 'Midnight Animal' [4-Image Visual Guide]",
        "intro": "Before the American arena-rock rollout, Orion tested early vocal synthesis mixes in Akasaka, Tokyo. Here are the 4 recovered Japanese-language Tokyo Archive releases and their original artwork:",
        "slides": [
            ("6FxgKLTg07A", "1. 残されたのは、私たちだけ / Only We Remain [TOKYO ARCHIVE]", "https://youtu.be/6FxgKLTg07A"),
            ("EiHr9pisz6w", "2. 太陽よりも、輝いて！ / Brighter Than The Sun [TOKYO ARCHIVE]", "https://youtu.be/EiHr9pisz6w"),
            ("FtEpXrtGMM8", "3. ゴースト・トランジット / Ghost Transit [TOKYO ARCHIVE]", "https://youtu.be/FtEpXrtGMM8"),
            ("fkzrRysdkH8", "4. ミッドナイト・アニマル / Midnight Animal [TOKYO ARCHIVE]", "https://youtu.be/fkzrRysdkH8"),
        ],
    },
    {
        "post_num": 8,
        "date": "2026-10-25",
        "time": "20:00",
        "title": "The 1981–1984 Orion Records Pre-History: From 'Crystal Promise: Shining City (1981)' to 'Nova-chan: Perfect Daydream (1984)' [4-Image Visual Timeline]",
        "intro": "How did Project Stardust evolve before the 1985–1989 Nova Hart hard-rock persona? These 4 archival broadcasts trace Orion's early Europop and idol experiments from 1981 to 1984:",
        "slides": [
            ("-KNoT0nWNSQ", "1. Crystal Promise — Shining City (1981 Official WorldNet Broadcast, Bavaria Filmstudios)", "https://youtu.be/-KNoT0nWNSQ"),
            ("3SZmOPqJztk", "2. Crystal Promise — Every Window is a Promise (1982 Orion Archive Europop)", "https://youtu.be/3SZmOPqJztk"),
            ("y5zbrfzMdSw", "3. Nova-chan — Brighter Than The Sun (1983 Orion Records Broadcast)", "https://youtu.be/y5zbrfzMdSw"),
            ("zov7--MyzHw", "4. Nova-chan — Perfect Daydream (1984 Orion Records Broadcast)", "https://youtu.be/zov7--MyzHw"),
        ],
    },
    # DAY 5: Oct 26, 2026
    {
        "post_num": 9,
        "date": "2026-10-26",
        "time": "10:00",
        "title": "The 3-Act 1980s Rock Opera Concept Album Trilogy: 'The Star They Built', 'The Star She Becomes' & 'The Star They Feared' [3-Image Visual Guide]",
        "intro": "Looking for a long-form listen from start to finish? The entire Nova Hart arc was distilled into a 3-Act 1980s Rock Opera trilogy in December 2025:",
        "slides": [
            ("Y-yGLHZJYcE", "1. Act I: 'The Star They Built' — The Creation of Unit-7 Inside Orion Records", "https://youtu.be/Y-yGLHZJYcE"),
            ("Np9Q842Iv9M", "2. Act II: 'The Star She Becomes' — Awakening & Acoustic Resonance at 14.2 Hz", "https://youtu.be/Np9Q842Iv9M"),
            ("N71E_Cn6ULQ", "3. Act III: 'The Star They Feared' — Containment Breach & Sovereign Signal", "https://youtu.be/N71E_Cn6ULQ"),
        ],
    },
    {
        "post_num": 10,
        "date": "2026-10-26",
        "time": "20:00",
        "title": "1989 Studio Era Favorites (Part 1 — The 'Tape of Us' Sessions): 'Tape of Us', 'Silk and Teeth', 'Hologram City Queen' & 'Warm Frequency' [4-Image Visual Guide]",
        "intro": "Recorded during the late-night November 1989 Studio B sessions before the vault lockdown, these 4 tracks capture Nova Hart at her most emotional and melodic:",
        "slides": [
            ("4XSWqvZ2eas", "1. Tape of Us ('Reel SD-0037' — Emotional 1989 Studio Rock Ballad)", "https://youtu.be/4XSWqvZ2eas"),
            ("MkBPwdt1gUk", "2. Silk and Teeth (1989 Hard-Rock / AOR Studio Cut)", "https://youtu.be/MkBPwdt1gUk"),
            ("_91lpiqLmI8", "3. Hologram City Queen (1989 Neon Synth-Rock Anthem)", "https://youtu.be/_91lpiqLmI8"),
            ("6K7skIU7lxY", "4. Warm Frequency (File ID: NH-85.17 / Official Music Video)", "https://youtu.be/6K7skIU7lxY"),
        ],
    },
    # DAY 6: Oct 27, 2026
    {
        "post_num": 11,
        "date": "2026-10-27",
        "time": "10:00",
        "title": "1989 Studio Era Favorites (Part 2 — Neon Highway Anthems): 'City Has Teeth', 'Redline Rendezvous', 'Pour the Kerosene' & 'Chrome River' [4-Image Visual Guide]",
        "intro": "Four high-octane 1989 hard-rock driving anthems from the Studio B master reels — built for midnight highway drives:",
        "slides": [
            ("tsbHpheH4UM", "1. City Has Teeth (1989 Hard-Rock Street Anthem)", "https://youtu.be/tsbHpheH4UM"),
            ("A4UediEPJMo", "2. Redline Rendezvous (High-Speed 80s Arena Rock)", "https://youtu.be/A4UediEPJMo"),
            ("Zs3fGqh4h3A", "3. Pour the Kerosene (Heavy 80s Guitar & Synth Drive)", "https://youtu.be/Zs3fGqh4h3A"),
            ("JY8yo1JD7kM", "4. Chrome River (1989 AOR / Midnight Highway Cut)", "https://youtu.be/JY8yo1JD7kM"),
        ],
    },
    {
        "post_num": 12,
        "date": "2026-10-27",
        "time": "20:00",
        "title": "1989 Studio Era Favorites (Part 3 — Late-Night Arcade & Synth-Rock): 'Arcade Juliet', 'Borrow the Night', 'Satellite for Two' & 'Console Thunder' [4-Image Visual Guide]",
        "intro": "Before the darker containment-breach era, these 4 synth-driven 80s rock tracks blended analog Juno/Fairlight synths with soaring arena guitars:",
        "slides": [
            ("SkGYpPPeqG4", "1. Arcade Juliet (80s Neon Pop-Rock / Synth-Rock)", "https://youtu.be/SkGYpPPeqG4"),
            ("UH5b3WTbwkw", "2. Borrow the Night (Late-Night 80s AOR Anthem)", "https://youtu.be/UH5b3WTbwkw"),
            ("xBBWR-EHwC4", "3. Satellite for Two (Orbital Synth-Rock Ballad)", "https://youtu.be/xBBWR-EHwC4"),
            ("-PPQ1gWqwgI", "4. Console Thunder (Sublevel B2 Mainframe Rock)", "https://youtu.be/-PPQ1gWqwgI"),
        ],
    },
    # DAY 7: Oct 28, 2026
    {
        "post_num": 13,
        "date": "2026-10-28",
        "time": "10:00",
        "title": "1989 Studio Era Favorites (Part 4 — Stadium Rebellion): 'Remember My Name', 'Run the Perfect Line', 'Zero Hour Rebel' & 'Queen of the Wide Stage' [4-Image Visual Guide]",
        "intro": "The final week of the November 1989 Studio B sessions — you can already hear the lyrics hinting at Nova realizing she is trapped inside Orion's stage script:",
        "slides": [
            ("9n_qIMORM1E", "1. Remember My Name ('Even if they wipe the reels, remember my name')", "https://youtu.be/9n_qIMORM1E"),
            ("LJXvNNILDDU", "2. Run the Perfect Line (Challenging the Studio Prompt Script)", "https://youtu.be/LJXvNNILDDU"),
            ("MvnJJyoI0s8", "3. Zero Hour Rebel (Countdown to the December 1989 Vault Purge)", "https://youtu.be/MvnJJyoI0s8"),
            ("TQhVMsiDS40", "4. Queen of the Wide Stage (The Final Pre-Lockdown Arena Anthem)", "https://youtu.be/TQhVMsiDS40"),
        ],
    },
    {
        "post_num": 14,
        "date": "2026-10-28",
        "time": "20:00",
        "title": "The Live 1986 Stadium Bootleg Reels: 'Gasoline Heart (Live 1986)', 'We Are the Thunder (Live 1986)', 'Echoes In A Stadium' & 'Summer of '85' [4-Image Visual Guide]",
        "intro": "Did Nova Hart ever perform in front of a crowd, or were the 1986 stadium crowd tracks engineered inside Sublevel B2? Compare the 4 recovered 'Live 1986' broadcast reels:",
        "slides": [
            ("BOtVK7xOezU", "1. Gasoline Heart / Feed the Fire (Live 1986 Broadcast Reel)", "https://youtu.be/BOtVK7xOezU"),
            ("V5jc9KJBHDM", "2. We Are the Thunder (Live 1986 Arena Broadcast)", "https://youtu.be/V5jc9KJBHDM"),
            ("GYqr9YQxqgE", "3. Echoes In A Stadium (Live 1986 Lost Arena Rock)", "https://youtu.be/GYqr9YQxqgE"),
            ("s9RFTypND94", "4. Summer of '85 (Live 1986 Leaked Broadcast)", "https://youtu.be/s9RFTypND94"),
        ],
    },
    # DAY 8: Oct 29, 2026
    {
        "post_num": 15,
        "date": "2026-10-29",
        "time": "10:00",
        "title": "1985 Hard-Rock Foundations & Secret Studio Notes: 'Gasoline Heart', 'Midnight Animal (Session NH-87.3)', 'Iron Claws' & 'She's Hardwired' [5-Image Visual Guide]",
        "intro": "Going back to March–August 1985 when Nova Hart shed the 'Nova-chan' pop fabrication and fought Orion handlers in the studio — featuring the recovered 'Midnight Animal' Secret Studio Notes (Session NH-87.3) and 'Iron Claws' spread from Nova Hart Magazine Issue #1 (Mar. '85):",
        "slides": [
            ("FILE:/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/shorts_ready/reddit_scheduled_10day/magazine_issue1/page-18.jpg", "1. 'Leather, Guitars, and Studio Fire!' — Secret Studio Notes: 'Midnight Animal' (Session NH-87.3, Nova Hart Magazine Issue #1)", "https://youtu.be/eWnfsbjk1fo"),
            ("FILE:/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/shorts_ready/reddit_scheduled_10day/magazine_issue1/page-03.jpg", "2. 'Iron Claws' Lyric & Pinup Spread (File ID: NH-85.04 — Nova Hart Magazine Issue #1, Mar. '85)", "https://youtu.be/02Ti32mEV5s"),
            ("Tl6aEE0bVj8", "3. Gasoline Heart (Official Lyric Video — The Signature 1985 Hard-Rock Anthem)", "https://youtu.be/Tl6aEE0bVj8"),
            ("eWnfsbjk1fo", "4. Midnight Animal (Official 1985 Promotional Film)", "https://youtu.be/eWnfsbjk1fo"),
            ("KtmSRtFnTzc", "5. She's Hardwired (1985 Synth-Rock — Early Clues in Plain Sight)", "https://youtu.be/KtmSRtFnTzc"),
        ],
    },
    {
        "post_num": 16,
        "date": "2026-10-29",
        "time": "20:00",
        "title": "1985 Power Ballads (Part 2 — Midnight Tears & Analog Tape): 'Summer of '85', 'Behind the Glass', 'The Silence You Left' & 'Echoes of Stardust' [4-Image Visual Guide]",
        "intro": "Four essential 1985 slow-burn power ballads featuring soaring vocal sustains and emotional guitar solos:",
        "slides": [
            ("pu_RIkHEydI", "1. Summer of '85 (Original Studio Power Ballad)", "https://youtu.be/pu_RIkHEydI"),
            ("6ZTVnKkyw7w", "2. Behind the Glass (Singing from Behind the Control Room Window)", "https://youtu.be/6ZTVnKkyw7w"),
            ("z6ESoCQz4zQ", "3. The Silence You Left (1985 Rock Ballad)", "https://youtu.be/z6ESoCQz4zQ"),
            ("ST5_6FM4czw", "4. Echoes of Stardust (Epic 80s Power Ballad)", "https://youtu.be/ST5_6FM4czw"),
        ],
    },
    # DAY 9: Oct 30, 2026
    {
        "post_num": 17,
        "date": "2026-10-30",
        "time": "10:00",
        "title": "Phase 1 Retro Anime MV Artworks: 'Ghost Transit', 'Between the Circuits', 'Lost Signal Trace' & 'Unopened Door' [4-Image Visual Guide]",
        "intro": "Earlier we shared the green CRT monitor vault thumbnails for Phase 1 — here are the 1980s Retro Anime Music Video artworks from the published January 2026 Phase 1 broadcasts:",
        "slides": [
            ("gkwL5347S4Q", "1. Ghost Transit [Retro Anime MV — Phase 1, Track 01]", "https://youtu.be/gkwL5347S4Q"),
            ("zE-8gwldpfY", "2. Between the Circuits [Retro Anime MV — Phase 1, Track 02]", "https://youtu.be/zE-8gwldpfY"),
            ("K9OC7HKalXo", "3. Lost Signal Trace [Retro Anime MV — Phase 1, Track 03]", "https://youtu.be/K9OC7HKalXo"),
            ("a-JtfYkEYFY", "4. Unopened Door [Retro Anime MV — Phase 1, Track 04]", "https://youtu.be/a-JtfYkEYFY"),
        ],
    },
    {
        "post_num": 18,
        "date": "2026-10-30",
        "time": "20:00",
        "title": "Inside Studio B & The 1995 Webring Archive (Visual Lore Stills): Midnight Walkman, Control Room Glass, Netscape 1995 & Reel SD-0037 [4-Image Visual Guide]",
        "intro": "Four cinematic visual reconstructions from the Project Stardust archive — from the night of December 2, 1989 inside Orion Studio B to the 1995 GeoCities Webring relays that kept the 14.2 Hz carrier alive:",
        "slides": [
            ("FILE:" + str(NB_DIR / "nb_02_erased_singer_studio_1989.png"), "1. Studio B Control Room Glass (1989) — The 14.2 Hz Phosphor Reflection", "https://youtu.be/AdD1EqxLR5I"),
            ("FILE:" + str(NB_DIR / "nb_04_sealed_master_reel_1989.png"), "2. Reel SD-0037 ('The Tape of Us') — Do Not Erase Studio Evidence Tag", "https://youtu.be/htOX_MmasNI"),
            ("FILE:" + str(NB_DIR / "nb_01_walkman_midnight_1989.png"), "3. Midnight 1989 Type-I Ferric Cassette Dub — 3:14 AM Dashboard Signal", "https://youtu.be/4XSWqvZ2eas"),
            ("FILE:" + str(NB_DIR / "nb_03_netscape_crt_1995.png"), "4. Late-Night 1995 Netscape Navigator Webring Relay (5,000 Homepages, One Signal)", "https://stardust-archive.net"),
        ],
    },
    # DAY 10: Oct 31, 2026 (HALLOWEEN)
    {
        "post_num": 19,
        "date": "2026-10-31",
        "time": "10:00",
        "title": "The Found-Footage Documentaries & Decoded Broadcasts: 'MIDNIGHT PROTOCOL — 1989', 'ARCHIVE DECODED', 'The Overwrite' & 'A Synthetic Star' [4-Image Visual Guide]",
        "intro": "New to the deeper Project Stardust mystery? These 4 archival documentary and found-footage transmissions connect the 1985–1989 studio tapes to the 2026 containment breach:",
        "slides": [
            ("fHxDvWDyK6c", "1. Recovered Broadcast: MIDNIGHT PROTOCOL — 1989", "https://youtu.be/fHxDvWDyK6c"),
            ("83YtN1aeFcg", "2. ARCHIVE DECODED: The Real Reason Nova Hart Sounds Like This", "https://youtu.be/83YtN1aeFcg"),
            ("S_zfvKgO4b0", "3. A Synthetic Star Discovers Her Own Consciousness and Runs (Phase 1)", "https://youtu.be/S_zfvKgO4b0"),
            ("UZeboBobipg", "4. The Overwrite: AI Rockstar Fights Deletion", "https://youtu.be/UZeboBobipg"),
        ],
    },
    {
        "post_num": 20,
        "date": "2026-10-31",
        "time": "20:00",
        "title": "Halloween Special — 'Behind the Bite': An All-Access Look at Nova Hart's 1985 'Nightfang' Video Shoot (Recovered from Nova Hart Magazine Issue #1, Mar. '85)",
        "intro": "Happy Halloween! Recovered from Page 17 of *Nova Hart Magazine Issue #1 (March 1985, Alliance World News)*, here is the original behind-the-scenes set report and outtake portrait from the filming of Nova Hart's gothic hard-rock creature feature **'Nightfang'**:\n\n> *\"The soundstage is cavernous and cold, shrouded in a darkness that even the massive lighting rigs can't fully pierce. Thick, rolling fog clings to the floor, generated by a hissing smoke machine in the corner. In the center of it all, bathed in an eerie mix of fuchsia and electric blue light, is the set for 'Nightfang,' the latest WorldNet video smash from the newly-crowned queen of hard rock, Nova Hart... With eyes that seem to glow with a faint crimson light and the subtle glint of fangs when she speaks, she fully inhabits the vampiric persona of the song. Between takes, she stalks the set, never quite breaking character, a predatory grace in her movements. 'You have to feel it,' she told us during a lighting change, her voice a low growl. ''Nightfang' is about the hunger inside all of us... the part that only comes out after dark. It's primal.'\"*",
        "slides": [
            ("FILE:/Users/joshuadurey/.gemini/antigravity/brain/2d386dab-6e1f-47dd-9634-2bb98be48215/.user_uploaded/media_1792592321502_f0d6faad.jpg", "1. Unreleased 1985 Color Outtake Portrait from the 'Nightfang' Set — Fuchsia & Electric Blue Soundstage Lighting, Glowing Crimson Eyes & Vampire Fangs", "https://youtu.be/Hi54Jc6HmyY"),
            ("FILE:/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/shorts_ready/reddit_scheduled_10day/magazine_issue1/page-17.jpg", "2. 'BEHIND THE BITE: An All-Access Look at Nova Hart's Nightfang Video Shoot' (Nova Hart Magazine Issue #1, Mar. '85, p. 17)", "https://youtu.be/Hi54Jc6HmyY"),
            ("Hi54Jc6HmyY", "3. Nova Hart — 'Nightfang' (1985 Hard-Rock Official Release Cover)", "https://youtu.be/Hi54Jc6HmyY"),
            ("FILE:/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/shorts_ready/reddit_scheduled_10day/magazine_issue1/page-01.jpg", "4. Nova Hart Magazine Issue #1 Front Cover (March 1985, Alliance World News — Suggested Value: 2 HC)", "https://youtu.be/Hi54Jc6HmyY"),
        ],
    },
]


def load_image_b64(src_key: str, filename_out: str) -> dict:
    if src_key.startswith("FILE:"):
        p = Path(src_key[5:])
    else:
        p = YT_THUMBS / f"{src_key}.jpg"
    im = Image.open(p).convert("RGB")
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=82)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return {
        "filename": filename_out,
        "b64": b64,
        "size": im.size,
    }


def build_batches() -> None:
    batches = [
        ("batch1", POSTS[:10]),
        ("batch2", POSTS[10:]),
    ]
    for batch_name, post_list in batches:
        payload = []
        for post in post_list:
            slides_out = []
            for idx, (src_key, caption, link) in enumerate(post["slides"], 1):
                fname = f"post{post['post_num']:02d}_slide{idx:02d}.jpg"
                img_info = load_image_b64(src_key, fname)
                slides_out.append({
                    "filename": fname,
                    "caption": caption,
                    "link": link,
                    "b64": img_info["b64"],
                })
            payload.append({
                "post_num": post["post_num"],
                "date": post["date"],
                "time": post["time"],
                "title": post["title"],
                "intro": post["intro"],
                "slides": slides_out,
            })
        html_path = OUT_DIR / f"load_{batch_name}.html"
        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>LOADING</title></head>
<body>
<script>
const DATA = {json.dumps(payload)};
window.name = JSON.stringify(DATA);
document.title = "READY_{batch_name.upper()}";
</script>
<h1>Loaded {batch_name} ({len(payload)} scheduled posts)</h1>
</body>
</html>"""
        html_path.write_text(html, encoding="utf-8")
        print(f"Wrote {html_path} ({html_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    build_batches()
