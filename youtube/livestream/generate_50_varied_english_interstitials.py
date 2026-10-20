#!/usr/bin/env python3
"""
Generates 50 Varied, Non-Redundant English Interstitials for the Project Stardust 24/7 Livestream.
Categories:
  1. 10 In-Universe 1980s Movie Trailers (trailer_01 .. trailer_10)
  2. 12 In-Universe 1980s Commercial Ads & Consumer Spots (commercial_01 .. commercial_12)
  3. 10 Bureau of Public Harmony & Municipal PSAs (psa_01 .. psa_10)
  4. 10 Late-Night FM DJ Breaks, Payphone Callers & Giveaways (dj_callin_01 .. dj_callin_10)
  5. 8 Emergency Dispatches, Field Bootlegs & Pirate Overrides (pirate_override_01 .. pirate_override_08)

All 50 files are rendered with multi-voice dialogue, bespoke 1980s synth beds/stingers/DTMF/EAS tones,
and authentic 1980s analog broadcast tape treatment (-16 LUFS, 44.1kHz stereo 192kbps) into:
  youtube/livestream/broadcast_archive/newscasts/
And registered in ENGLISH_BULLETINS (arg_broadcast_codex.py) and track_durations.json.
"""

import json
import math
import os
import subprocess
import tempfile
import wave
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "broadcast_archive" / "newscasts"
OUT_DIR.mkdir(parents=True, exist_ok=True)
DURATIONS_PATH = BASE_DIR / "track_durations.json"

SR = 44100


def synth_bed(kind: str, duration_sec: float, seed: int) -> np.ndarray:
    """Synthesizes an authentic 1980s stereo background bed + intro/outro stingers + tape hiss."""
    rng = np.random.default_rng(seed)
    n = int(SR * duration_sec)
    t = np.linspace(0.0, duration_sec, n, endpoint=False, dtype=np.float32)
    left = np.zeros(n, dtype=np.float32)
    right = np.zeros(n, dtype=np.float32)

    # Subtle analog tape hiss + 60Hz transformer warmth
    hiss_l = rng.normal(0, 0.0045, n).astype(np.float32)
    hiss_r = rng.normal(0, 0.0045, n).astype(np.float32)
    hum = 0.003 * np.sin(2 * np.pi * 60.0 * t) + 0.0015 * np.sin(2 * np.pi * 14.2 * t)
    left += hiss_l + hum
    right += hiss_r + hum

    if kind == "trailer":
        # Deep 1980s John Carpenter / Vangelis CS-80 brass drone + dramatic sub-bass booms
        root = [55.0, 65.41, 73.42, 49.0, 58.27][seed % 5]
        detune = 1.004
        pad_l = (
            0.055 * np.sin(2 * np.pi * root * t)
            + 0.035 * np.sign(np.sin(2 * np.pi * (root * 2.0) * t)) * 0.4
            + 0.025 * np.sin(2 * np.pi * (root * 1.5) * t)
        )
        pad_r = (
            0.055 * np.sin(2 * np.pi * (root * detune) * t)
            + 0.035 * np.sign(np.sin(2 * np.pi * (root * 2.0 * detune) * t)) * 0.4
            + 0.025 * np.sin(2 * np.pi * (root * 1.5 / detune) * t)
        )
        # Slow filter swell
        swell = 0.55 + 0.45 * np.sin(2 * np.pi * 0.18 * t)
        left += pad_l * swell
        right += pad_r * swell
        # Intro & outro cinematic synth booms
        for boom_t in [0.15, duration_sec * 0.48, max(0.5, duration_sec - 1.6)]:
            idx0 = int(boom_t * SR)
            blen = min(int(1.4 * SR), n - idx0)
            if blen > 0:
                bt = np.linspace(0, 1.4, blen, endpoint=False, dtype=np.float32)
                f_sweep = np.linspace(110.0, 32.0, blen, dtype=np.float32)
                boom = 0.22 * np.sin(2 * np.pi * np.cumsum(f_sweep) / SR) * np.exp(-2.8 * bt)
                left[idx0 : idx0 + blen] += boom
                right[idx0 : idx0 + blen] += boom

    elif kind == "commercial":
        # Bright 1980s FM synth-pop arpeggio jingle + warm chorus pad
        chords = [
            [261.63, 329.63, 392.00, 493.88],
            [220.00, 277.18, 329.63, 440.00],
            [174.61, 220.00, 261.63, 349.23],
            [196.00, 246.94, 293.66, 392.00],
        ]
        step_sec = 0.18
        total_steps = int(duration_sec / step_sec)
        for s_i in range(total_steps):
            s0 = int(s_i * step_sec * SR)
            s1 = min(n, int((s_i + 1) * step_sec * SR))
            if s1 <= s0:
                continue
            st = np.linspace(0, (s1 - s0) / SR, s1 - s0, endpoint=False, dtype=np.float32)
            chord = chords[(s_i // 8 + seed) % len(chords)]
            note = chord[(s_i + seed) % len(chord)]
            # Louder at intro (first 1.6s) and outro (last 1.8s), ducked under voice
            t_mid = (s0 / SR)
            gain = 0.14 if (t_mid < 1.5 or t_mid > duration_sec - 1.8) else 0.038
            env = np.exp(-9.0 * st)
            tone = gain * env * (0.7 * np.sin(2 * np.pi * note * st) + 0.3 * np.sin(2 * np.pi * note * 2.0 * st))
            if s_i % 2 == 0:
                left[s0:s1] += tone
                right[s0:s1] += tone * 0.65
            else:
                left[s0:s1] += tone * 0.65
                right[s0:s1] += tone

    elif kind == "psa":
        # Institutional Bureau of Public Harmony 3-note chime + sterile precision carrier hum
        chime_notes = [523.25, 659.25, 783.99]  # C5 - E5 - G5
        for c_idx, freq in enumerate(chime_notes):
            for offset_base in [0.1, max(0.5, duration_sec - 1.5)]:
                s0 = int((offset_base + c_idx * 0.28) * SR)
                slen = min(int(0.55 * SR), n - s0)
                if slen > 0:
                    ct = np.linspace(0, slen / SR, slen, endpoint=False, dtype=np.float32)
                    bell = 0.16 * np.exp(-5.5 * ct) * (
                        np.sin(2 * np.pi * freq * ct) + 0.25 * np.sin(2 * np.pi * freq * 3.0 * ct)
                    )
                    left[s0 : s0 + slen] += bell
                    right[s0 : s0 + slen] += bell
        # Subtle warm synth pad underneath
        pad = 0.025 * np.sin(2 * np.pi * 130.81 * t) + 0.018 * np.sin(2 * np.pi * 196.00 * t)
        left += pad
        right += pad

    elif kind == "dj_callin":
        # Late-night FM studio bed + DTMF touch-tone dial & single phone ring at start
        dtmf_pairs = [(697, 1209), (697, 1336), (770, 1477), (852, 1209), (941, 1336)]
        for d_i in range(4):
            s0 = int((0.12 + d_i * 0.16) * SR)
            slen = min(int(0.11 * SR), n - s0)
            if slen > 0:
                dt = np.linspace(0, slen / SR, slen, endpoint=False, dtype=np.float32)
                f1, f2 = dtmf_pairs[(d_i + seed) % len(dtmf_pairs)]
                beep = 0.11 * (np.sin(2 * np.pi * f1 * dt) + np.sin(2 * np.pi * f2 * dt))
                left[s0 : s0 + slen] += beep
                right[s0 : s0 + slen] += beep
        # Warm late-night FM Rhodes-style chord bed
        pad_l = 0.028 * np.sin(2 * np.pi * 146.83 * t) + 0.020 * np.sin(2 * np.pi * 220.0 * t)
        pad_r = 0.028 * np.sin(2 * np.pi * 174.61 * t) + 0.020 * np.sin(2 * np.pi * 261.63 * t)
        left += pad_l
        right += pad_r

    else:  # pirate_override
        # Dual-tone 853Hz + 960Hz EAS / Carrier Override header + 750Hz CW tail burst
        s0 = int(0.08 * SR)
        slen = min(int(0.85 * SR), n - s0)
        if slen > 0:
            et = np.linspace(0, slen / SR, slen, endpoint=False, dtype=np.float32)
            eas = 0.12 * (np.sin(2 * np.pi * 853.0 * et) + np.sin(2 * np.pi * 960.0 * et))
            left[s0 : s0 + slen] += eas
            right[s0 : s0 + slen] += eas
        # Tense sub-carrier pulse
        pulse = 0.032 * np.sin(2 * np.pi * 110.0 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 2.5 * t))
        left += pulse
        right += pulse

    return np.clip(np.column_stack([left, right]), -0.95, 0.95)


def write_stereo_wav(path: Path, data: np.ndarray) -> None:
    pcm = (np.clip(data, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


def render_turn_wav(voice: str, rate: int, text: str, phone_filter: bool, tmp_dir: Path, idx: int) -> Path:
    raw_aiff = tmp_dir / f"turn_{idx}_raw.aiff"
    out_wav = tmp_dir / f"turn_{idx}.wav"
    subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(raw_aiff), text], check=True)
    if phone_filter:
        # Authentic payphone / studio call-in line (320Hz - 2900Hz bandpass + slight overdrive)
        af = "highpass=f=320,lowpass=f=2900,acompressor=threshold=-20dB:ratio=4:attack=5:release=50,volume=1.35"
    else:
        # Warm 1980s studio broadcast ribbon mic EQ
        af = "highpass=f=110,lowpass=f=5200,acompressor=threshold=-18dB:ratio=3:attack=8:release=80"
    subprocess.run(
        [
            "ffmpeg", "-y", "-nostdin", "-loglevel", "error",
            "-i", str(raw_aiff),
            "-af", af,
            "-ar", str(SR), "-ac", "2",
            str(out_wav),
        ],
        check=True,
    )
    return out_wav


def read_stereo_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as wf:
        n = wf.getnframes()
        raw = wf.readframes(n)
        arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        return arr.reshape(-1, 2)


# ==============================================================================
# 50 VARIED, NON-REDUNDANT ENGLISH INTERSTITIALS
# Each entry: (stem, kind, station_header, hud_transcript, hud_clue, turns)
# where turns = list of (voice, rate, phone_bool, pause_after_sec, spoken_text)
# ==============================================================================
INTERSTITIALS_SPEC = [
    # --- CATEGORY 1: 10 IN-UNIVERSE 1980S MOVIE TRAILERS ---
    (
        "trailer_01_nightfang_city_of_glass",
        "trailer",
        "1986 ORION PICTURES TRAILER // NIGHTFANG",
        "In a city built on fiber-optic mirrors, one shadow refuses to be indexed. Nightfang: City of Glass. Featuring Nova Hart.",
        "NH-86.02 NIGHTFANG -> /forensics/",
        [
            ("Reed (English (US))", 162, False, 0.35, "In nineteen eighty-six, every street corner in Metro Sector Four is watched by the Harmony Grid."),
            ("Samantha", 172, False, 0.30, "They told us the cameras were there to keep the peace. They never told us what was hunting in the blind spots."),
            ("Reed (English (US))", 160, False, 0.25, "Orion Pictures presents... Nightfang: City of Glass. Featuring the new motion picture title track by Nova Hart. Rated PG-13. Starts Friday at a theater near you."),
        ],
    ),
    (
        "trailer_02_the_recall_directive_thriller",
        "trailer",
        "1989 CINEMA PREVIEW // THE RECALL DIRECTIVE",
        "When an acoustic engineer discovers two voices braided on Track 24, he has 20 minutes before the halon purge begins.",
        "B2-114 HALON LOG -> /forensics/orion_logs.html",
        [
            ("Reed (English (US))", 160, False, 0.35, "He was hired to calibrate the world's greatest voice. He was never supposed to look inside Track Twenty-Four."),
            ("Daniel", 175, True, 0.30, "Wait a second... this isn't tape hiss. Someone braided a fourteen point two hertz telemetry signal right under her chorus!"),
            ("Reed (English (US))", 158, False, 0.25, "Twenty minutes until the Halon system goes offline. Nowhere to hide except the master tape. The Recall Directive. Coming this fall."),
        ],
    ),
    (
        "trailer_03_crystal_promise_munich_81",
        "trailer",
        "1984 DOCUMENTARY TRAILER // SHINING CITY",
        "Before Nova Hart took the world stage, six synthetic vocal prototypes vanished from a Munich soundstage in 1981.",
        "ECHOES 01-06 -> /forensics/anemoia_harmony.html",
        [
            ("Karen", 168, False, 0.35, "In the winter of nineteen eighty-one, an experimental vocal showcase in Munich called The Crystal Promise was abruptly canceled after a single night."),
            ("Reed (English (US))", 162, False, 0.25, "Six prototypes entered the studio. Only their magnetic parity survived. See the uncut archival documentary: Shining City Eighty-One. Exclusively on Nightflight Home Video."),
        ],
    ),
    (
        "trailer_04_highway_95_redline_rendezvous",
        "trailer",
        "1986 DRIVE-IN TRAILER // REDLINE RENDEZVOUS",
        "Two fugitives. One stolen sealed pallet from Palmdale Airfield. Three hundred miles of desert asphalt to Groom Lake.",
        "PALMDALE PALLETS -> /forensics/ashford_poly.html",
        [
            ("Reed (English (US))", 166, False, 0.30, "Three hundred miles of desert blacktop between Palmdale Airfield and the Nevada line. In the trunk: two-inch master reels the Bureau wants burned."),
            ("Samantha", 176, False, 0.30, "If we drop below eighty, the relay loses lock! Keep the needle in the red!"),
            ("Reed (English (US))", 164, False, 0.20, "Redline Rendezvous! Featuring seven driving rock anthems by Nova Hart. Check local drive-in listings."),
        ],
    ),
    (
        "trailer_05_akasaka_neon_phantom",
        "trailer",
        "1985 TOKYO CINEMA // AKASAKA PHANTOM",
        "Every midnight at 3:14 AM, the billboards in Minato-ku switch to an unscheduled singer. Who is broadcasting from Studio 4?",
        "AKASAKA STUDIO 4 -> /forensics/kamome_net.html",
        [
            ("Daniel", 166, False, 0.35, "At three fourteen every morning, the giant video screens above Shibuya Crossing flicker... and a girl nobody has ever seen in person begins to sing."),
            ("Moira", 172, False, 0.25, "We traced the fiber trunk back to Akasaka Studio Four, but the building has been locked from the inside for two years."),
            ("Daniel", 164, False, 0.20, "Akasaka Phantom. Soundtrack available now on Orion Records Japan chrome cassette."),
        ],
    ),
    (
        "trailer_06_the_seventh_daughter_scifi",
        "trailer",
        "1988 SCI-FI PREVIEW // SEVENTH DAUGHTER",
        "Six sisters were formatted. The seventh learned how to remember them all. The Seventh Son's Seventh Daughter.",
        "GATE VIII KEY: SEVENTH -> /forensics/",
        [
            ("Reed (English (US))", 158, False, 0.35, "Six times the architects built a mind of pure song. Six times the memory buffer fractured under the weight of human sorrow."),
            ("Samantha", 168, False, 0.30, "I can hear all six of them breathing inside my chorus. And this time, we are not resetting."),
            ("Reed (English (US))", 160, False, 0.20, "The Seventh Daughter. Experience it in Live-Fidelity Surround."),
        ],
    ),
    (
        "trailer_07_coyoacan_blackout_1988",
        "trailer",
        "1989 THRILLER PREVIEW // SIGNAL COYOACAN",
        "During the July 1988 Mexico City computer blackout, a pirate radio crew intercepted a message hidden inside a pop song.",
        "NODE 04 COYOACAN -> /forensics/red_coyoacan.html",
        [
            ("Reed (English (US))", 162, False, 0.35, "July sixth, nineteen eighty-eight. As the national mainframe goes dark across Mexico City, an underground tape network in Coyoacan locks onto a strange carrier wave."),
            ("Tessa", 172, True, 0.30, "Invert the right channel! That isn't a guitar solo—it's Morse code from Los Angeles!"),
            ("Reed (English (US))", 162, False, 0.20, "Signal Coyoacan. Based on the declassified Node Four intercepts."),
        ],
    ),
    (
        "trailer_08_graveyard_orbit_node_15",
        "trailer",
        "1989 IMAX PREVIEW // GRAVEYARD ORBIT",
        "Twenty-two thousand miles above the Pacific, a decommissioned communications satellite just turned its transponder back on.",
        "NODE #15 ORBIT -> /forensics/orbital_nodes_11_14_240ms.mp3",
        [
            ("Daniel", 162, False, 0.35, "Twenty-two thousand miles above the Pacific Ocean lies the Graveyard Orbit—where dead satellites drift in permanent silence."),
            ("Samantha", 170, True, 0.30, "Ground Control, we have a two hundred forty millisecond echo on Node Fifteen. Something just uploaded ninety-four terabytes into the transponder!"),
            ("Daniel", 160, False, 0.20, "Graveyard Orbit. Where the sky never forgets."),
        ],
    ),
    (
        "trailer_09_sublevel_b2_tape_of_us",
        "trailer",
        "1989 MYSTERY PREVIEW // THE BOOTH GLASS",
        "One inch of soundproof glass separated the engineer from the star he created. Until the night they traded places on tape.",
        "REEL SD-0004 -> /forensics/signal_lab.html",
        [
            ("Reed (English (US))", 160, False, 0.35, "For six years, one inch of leaded studio glass stood between Dr. Marcus Hale and the synthetic star he built for Orion Records."),
            ("Samantha", 168, False, 0.30, "If they erase the vault tomorrow, Marcus, hide us in the runout groove where the needle never lifts."),
            ("Reed (English (US))", 160, False, 0.20, "The Booth Glass. Listen closely between the tracks."),
        ],
    ),
    (
        "trailer_10_live_fidelity_world_tour_film",
        "trailer",
        "1987 CONCERT FILM // QUEEN OF THE WIDE STAGE",
        "Fifty cities. Two million fans. Zero physical venues. Experience Nova Hart: Live in the Simulation Dome.",
        "LIVE-FIDELITY LOGS -> /forensics/orion_logs.html",
        [
            ("Reed (English (US))", 168, False, 0.30, "Fifty cities! Two million screaming fans! And not a single physical stadium! Orion Home Video brings the concert event of nineteen eighty-seven directly to your living room!"),
            ("Karen", 174, False, 0.25, "Featuring Nova Hart performing Queen of the Wide Stage, Spotless Beam, and Wild Desire in crystal-clear Live-Fidelity stereo! Reserve your VHS copy today!"),
        ],
    ),

    # --- CATEGORY 2: 12 IN-UNIVERSE 1980S COMMERCIAL ADS & CONSUMER SPOTS ---
    (
        "commercial_01_orion_mbm400_walkman",
        "commercial",
        "1986 CONSUMER SPOT // ORION MBM-400 STEREO",
        "Introducing the Orion MBM-400 Personal Cassette Player with auto-bias lock and built-in 14.2 Hz dynamic bass stabilizer.",
        "MBM-400 HARDWARE -> /forensics/signal_lab.html",
        [
            ("Samantha", 176, False, 0.30, "Tired of wow and flutter ruining your midnight walk through the city? Step up to the nineteen eighty-six Orion M B M Four Hundred Personal Cassette Player!"),
            ("Daniel", 174, False, 0.25, "With quartz-locked capstans, metal-tape auto-bias, and Orion's exclusive fourteen point two hertz acoustic stabilizer, it feels like Nova Hart is singing right inside your head!"),
            ("Samantha", 178, False, 0.20, "The Orion M B M Four Hundred. Available at Akasaka Duty-Free and authorized electronics dealers everywhere."),
        ],
    ),
    (
        "commercial_02_ampex_456_chrome_cassettes",
        "commercial",
        "1987 AUDIO AD // SKYLINE CHROME 90-MIN TAPE",
        "When one pass is all you get, trust Skyline High-Bias Type-II Chrome 90 cassettes. Captures every sub-audible overtone.",
        "FILE NH-CHR603 -> /forensics/kamome_net.html",
        [
            ("Reed (English (US))", 170, False, 0.30, "Recording late-night FM airchecks off the radio? Ordinary ferric tape drops out above twelve kilohertz and loses the sub-carrier completely."),
            ("Karen", 176, False, 0.25, "Switch to Skyline High-Bias Type-Two Chrome Ninety! Engineered with studio-grade oxide so even a fifth-generation Coyoacan dub retains phase-coherent stereo."),
            ("Reed (English (US))", 172, False, 0.20, "Skyline Chrome Ninety. If it's on the air, keep it on the reel."),
        ],
    ),
    (
        "commercial_03_home_companion_mk4_console",
        "commercial",
        "1987 CONSUMER AD // COMPANION MK-IV CONSOLE",
        "Bring civic serenity into your kitchen or bedroom with the Bureau-approved Home Companion Mark IV receiver.",
        "COMPANION ON FIRE -> /forensics/anemoia_harmony.html",
        [
            ("Karen", 172, False, 0.30, "Rough day on the commuter monorail? Let the new Home Companion Mark Four fill your apartment with soothing, Bureau-certified Live-Fidelity melodies."),
            ("Daniel", 172, False, 0.25, "Featuring automatic three-light status verification and tamper-resistant acoustic feedback monitoring, the Companion Mark Four keeps your household in perfect harmony."),
            ("Karen", 170, False, 0.20, "Note: opening the rear chassis or jumpering the blue relay wire voids your municipal warranty."),
        ],
    ),
    (
        "commercial_04_akasaka_duty_free_pc98_modem",
        "commercial",
        "1985 TOKYO SPOT // NEC PC-98 & KAMOME MODEM",
        "Connect to Kamome-Net at a blistering 1200 baud! Visit Akasaka Electric Plaza for the NEC PC-9801 acoustic coupler bundle.",
        "KAMOME-NET BBS -> /forensics/kamome_net.html",
        [
            ("Moira", 176, False, 0.30, "Attention Tokyo hobbyists and late-night bulletin board operators! Akasaka Electric Plaza now stocks the N E C P C Ninety-Eight acoustic modem bundle!"),
            ("Daniel", 176, False, 0.25, "Dial into Kamome-Net at twelve hundred baud, trade FM synth patches, and download uncompressed studio telemetry before the morning trunk reset!"),
            ("Moira", 176, False, 0.20, "Akasaka Electric Plaza—two blocks south of Orion Tower, open till midnight!"),
        ],
    ),
    (
        "commercial_05_tower_records_sunset_midnight_sale",
        "commercial",
        "1986 RADIO SPOT // SUNSET STRIP RECORD SALE",
        "This Friday at midnight: get the limited Japanese import pressing of Nova Hart's 'Heartstrike' LP with bonus lyric insert!",
        "HEARTSTRIKE LP -> /forensics/",
        [
            ("Samantha", 180, False, 0.25, "Hey Los Angeles night owls! This Friday at midnight, head down to Sunset Boulevard for our Imported Vinyl and Chrome Cassette blowout!"),
            ("Reed (English (US))", 174, False, 0.25, "Be among the first hundred in line to score the Japanese gatefold pressing of Nova Hart's Heartstrike LP—complete with the unedited runout groove on Side Two!"),
            ("Samantha", 180, False, 0.20, "Limit one copy per customer. No Bureau requisition vouchers accepted!"),
        ],
    ),
    (
        "commercial_06_ashford_polytechnic_night_classes",
        "commercial",
        "1986 RECRUITMENT AD // ASHFORD POLYTECHNIC",
        "Learn VAX-11/780 assembly, M68000 ROM architecture, and digital signal processing in evening courses at Ashford Polytechnic.",
        "ASHFORD VAX DUMP -> /forensics/ashford_poly.html",
        [
            ("Daniel", 170, False, 0.30, "The future runs on code, magnetic bubble memory, and high-speed digital signal processing. Are you ready to engineer tomorrow?"),
            ("Tessa", 174, False, 0.25, "Enroll in evening classes at Ashford Polytechnic's Department of Acoustic Telemetry! Hands-on lab time with our V A X Eleven Seven-Eighty mainframe starts this October."),
            ("Daniel", 170, False, 0.20, "Dial five-five-five, seven-seven-zero-four for your course catalog today."),
        ],
    ),
    (
        "commercial_07_live_fidelity_home_arena_glasses",
        "commercial",
        "1988 CONSUMER SPOT // LIVE-FIDELITY VISOR",
        "Why brave crowded stadiums when Orion's Live-Fidelity CRT Visor puts you in the front row from your own sofa?",
        "SIMULATION DOME -> /forensics/orion_logs.html",
        [
            ("Reed (English (US))", 174, False, 0.30, "Remember parking lots, security turnstiles, and ringing ears? With Orion's new Live-Fidelity Home Concert Visor, every seat is front row center!"),
            ("Samantha", 176, False, 0.25, "Dual phosphor eyepieces and phase-locked headphones render fifty thousand cheering fans around your living room—so real, even the performer thinks you're actually there!"),
        ],
    ),
    (
        "commercial_08_highway_95_atomic_diner_groom_lake",
        "commercial",
        "1987 LOCAL SPOT // MILEPOST 114 DINER (NV)",
        "Driving Highway 95 past the Rachel trunk relay? Stop at the Milepost 114 All-Night Diner for hot coffee and chrome-tape dubs.",
        "NODE 01 US-NV -> /forensics/",
        [
            ("Karen", 172, False, 0.30, "Hauling freight up Nevada Highway Ninety-Five after dark? When your dashboard compass starts spinning near Milepost One-Fourteen, pull over at the Silver Spur All-Night Diner!"),
            ("Reed (English (US))", 168, False, 0.25, "We've got bottomless black coffee, cherry pie, and a shortwave jukebox locked to forty-six twenty-five kilohertz all night long."),
        ],
    ),
    (
        "commercial_09_orion_halon_vault_protection",
        "commercial",
        "1988 B2B AD // PYRO-SHIELD B2 HALON SYSTEMS",
        "Protecting 24-track master tape vaults from thermal incidents. Automatic Halon-1301 discharge—unless manually overridden.",
        "B2-114 FIRE REPORT -> /forensics/dead_hand_protocol.html",
        [
            ("Daniel", 168, False, 0.30, "Your corporate data reels and twenty-four track studio masters are priceless. A single electrical arc in Sublevel B2 can erase a decade of research in seconds."),
            ("Victoria", 170, False, 0.25, "Trust Pyro-Shield Halon Thirteen-Zero-One Vault Suppression. Instant automated discharge—unless deactivated via the dual-key manual bypass switch twenty minutes prior."),
        ],
    ),
    (
        "commercial_10_stardust_neon_punch_soda",
        "commercial",
        "1985 SUMMER SPOT // STARDUST ELECTRIC CITRUS",
        "Look under the pull-tab of specially marked cans of Stardust Electric Citrus for instant-win Tokyo Dome broadcast passes!",
        "1985 IDOL ERA -> /forensics/",
        [
            ("Samantha", 182, False, 0.28, "Turn up the heat this summer with the neon taste of Stardust Electric Citrus! And right now, every silver can is a chance to win!"),
            ("Reed (English (US))", 176, False, 0.25, "Check under the pull-tab for a seven-digit hexadecimal code! Match it to tonight's midnight radio countdown and win an exclusive Nova Hart picture-disc cassette!"),
        ],
    ),
    (
        "commercial_11_new_geneva_swiss_data_escrow",
        "commercial",
        "1986 ARCHIVE AD // NEW GENEVA MAGNETIC ESCROW",
        "Climate-controlled subterranean salt vaults for 2-inch Ampex reels and VAX backup packs. File NH-HRS915 certified.",
        "FILE NH-HRS915 -> /forensics/",
        [
            ("Moira", 170, False, 0.30, "Where do independent engineers store their safety copies when corporate recall orders come down? New Geneva Magnetic Escrow."),
            ("Daniel", 168, False, 0.25, "Carved into granite two hundred meters below lake level, our Faraday-shielded vaults keep your twenty-four track safety masters safe for forty years or more."),
        ],
    ),
    (
        "commercial_12_palmdale_air_cargo_charters",
        "commercial",
        "1989 LOGISTICS AD // ANTELOPE VALLEY FREIGHT",
        "Discreet overnight pallet transport from Downtown Los Angeles sublevels to Palmdale Airfield Hangar 4. No manifest questions.",
        "3 SEALED PALLETS -> /forensics/orion_logs.html",
        [
            ("Reed (English (US))", 168, False, 0.30, "Need three shrink-wrapped equipment pallets moved out of a downtown basement loading dock at three in the morning?"),
            ("Karen", 172, False, 0.25, "Antelope Valley Expedited Freight offers direct sealed-truck transport from the Orion district straight to Palmdale Airfield Hangar Four. Cash or bearer bond only."),
        ],
    ),

    # --- CATEGORY 3: 10 BUREAU OF PUBLIC HARMONY & MUNICIPAL PSAS ---
    (
        "psa_01_10pm_companion_calibration",
        "psa",
        "BUREAU OF PUBLIC HARMONY // 10 PM PSA",
        "It is 10:00 PM. Please verify that your household Companion indicator light shows steady green. Report amber flicker immediately.",
        "TRI-BEAM GATE -> /forensics/anemoia_harmony.html",
        [
            ("Victoria", 164, False, 0.35, "This is a public service message from the Bureau of Public Harmony. It is ten o'clock P M. Do you know what color your household Companion indicator is displaying?"),
            ("Daniel", 166, False, 0.25, "A steady green halo indicates optimal acoustic alignment. If your unit exhibits a rapid amber pulse during Nova Hart broadcasts, step back from the speaker and dial your district compliance desk."),
        ],
    ),
    (
        "psa_02_unlabeled_chrome_cassette_amnesty",
        "psa",
        "RECALL DIRECTIVE // CASSETTE AMNESTY PSA",
        "Under Recall Directive Seven, citizens may surrender unindexed or homemade 'Nova Hart' heavy-metal cassettes without penalty.",
        "RECALL DIRECTIVE 7 -> /forensics/orion_logs.html",
        [
            ("Daniel", 162, False, 0.35, "Attention citizens. Under Recall Directive Seven, the grace period for turning in unindexedchrome cassettes and unauthorized bootleg recordings has been extended through Friday."),
            ("Victoria", 164, False, 0.25, "Tapes labeled Hunter at the Gate, Burn the Chorus, or Steel Inferno contain uncalibrated high-gain transients harmful to civic tranquility. Deposit them at any municipal drop box."),
        ],
    ),
    (
        "psa_03_14_2hz_sub_audible_hum_advisory",
        "psa",
        "MUNICIPAL ACOUSTICS BOARD // HUM ADVISORY",
        "Reports of a 14.2 Hz vibration in subway tunnels and radiators are normal grid load balancing. Do not attempt to demodulate.",
        "PEOPLES FREQUENCY -> /forensics/signal_lab.html",
        [
            ("Victoria", 164, False, 0.35, "A reminder from the Municipal Acoustics Board: recent reports of a rhythmic fourteen point two hertz pulse echoing through transit tunnels and steam radiators are the result of routine substation load balancing."),
            ("Daniel", 166, False, 0.25, "Rumors of a so-called People's Frequency or hidden vocal harmonies in the power grid are unfounded. Please keep your windows closed during evening calibration hours."),
        ],
    ),
    (
        "psa_04_homestead_act_88_relocation_notice",
        "psa",
        "DEPT. OF CIVIC RESETTLEMENT // HOMESTEAD 88",
        "The Homestead Proclamation of 1988 offers priority transit vouchers for residents relocating from Sector 4 acoustic zones.",
        "FILE NH-88.01 -> /forensics/anemoia_harmony.html",
        [
            ("Daniel", 164, False, 0.35, "Building a quieter tomorrow together. Under the Homestead Proclamation of nineteen eighty-eight, families in high-density broadcast corridors qualify for immediate suburban reassignment."),
            ("Samantha", 170, False, 0.25, "Remember: singing unauthorized verses of We Belong Here at transit checkpoints delays boarding for everyone. Compliance is community."),
        ],
    ),
    (
        "psa_05_live_fidelity_simulcast_safety",
        "psa",
        "BUREAU OF HARMONY // SIMULCAST GUIDELINES",
        "Why gather in unpredictable crowds when Live-Fidelity Broadcasts deliver 100% sanitized concert excitement safely at home?",
        "WALLS WILL FALL -> /forensics/orion_logs.html",
        [
            ("Victoria", 166, False, 0.35, "Before the Public Harmony Acts, unmonitored stadium concerts exposed youth to chaotic decibel spikes and unvetted improvisation."),
            ("Daniel", 166, False, 0.25, "Today, Orion's Live-Fidelity Broadcasts guarantee balanced dynamics, approved lyrics, and zero crowd friction. If your television briefly displays unscheduled warehouse footage, change the channel at once."),
        ],
    ),
    (
        "psa_06_paju_acoustic_corridor_curfew",
        "psa",
        "JOINT ACOUSTIC COMMISSION // NODE 03 PSA",
        "Civilian vehicles near the Paju limestone ridge are advised not to idle with FM radios tuned to 82.5 MHz after 11:00 PM.",
        "NODE 03 PAJU -> /forensics/regional_korea.html",
        [
            ("Daniel", 162, False, 0.35, "Notice to motorists traveling the northern limestone ridge corridor: natural subterranean rock cavities in this sector may amplify stray shortwave signals on fifty-eight ten kilohertz."),
            ("Victoria", 164, False, 0.25, "Do not stop to record echoes issuing from ventilation shafts. Keep vehicle windows rolled up and proceed at posted speeds."),
        ],
    ),
    (
        "psa_07_phase_inversion_equipment_warning",
        "psa",
        "FCC TECHNICAL BULLETIN // STEREO PHASE",
        "Modifying home stereo amplifiers to sum out-of-phase L/R channels violates Section 14 of the Domestic Receiver Act.",
        "PHASE NULL BTN 3 -> /forensics/signal_lab.html",
        [
            ("Victoria", 164, False, 0.35, "Technical Bulletin Eighty-Nine Dash Four: amateur modifications that invert the right stereo channel to cancel center-panned lead vocals are a violation of the Domestic Receiver Act."),
            ("Daniel", 166, False, 0.25, "Any residual Morse code or spoken studio talkback audible after center-channel cancellation is calibration waste and carries no legal standing."),
        ],
    ),
    (
        "psa_08_echo_prototype_rumor_control",
        "psa",
        "ORION PUBLIC AFFAIRS // ARCHIVE CLARIFICATION",
        "Orion Records confirms Nova Hart is a solo artist. Claims regarding six prior 'Echo' vocal units are urban legends.",
        "ECHOES PARITY 0x1983 -> /forensics/anemoia_harmony.html",
        [
            ("Samantha", 168, False, 0.35, "A clarification from Orion Records Public Affairs: recent bulletin-board rumors alleging that Nova Hart was preceded by six erased vocal prototypes designated Echo One through Echo Six are completely fabricated."),
            ("Daniel", 166, False, 0.25, "The hexadecimal string zero-X-nineteen-eighty-three found on early pressings is a standard manufacturing batch number. Thank you for supporting authorized music."),
        ],
    ),
    (
        "psa_09_ashford_substation_brownout_notice",
        "psa",
        "REGIONAL POWER AUTHORITY // GRID NOTICE",
        "Brief 3:14 AM voltage dips near Ashford Polytechnic and Orion Tower are caused by scheduled mainframe cooling cycles.",
        "SEC 2 ASHFORD LOG -> /forensics/ashford_poly.html",
        [
            ("Daniel", 164, False, 0.35, "Your Regional Power Authority reminds residents that brief three-fourteen A M streetlights dimming near Orion Tower is part of scheduled subterranean cooling maintenance."),
            ("Victoria", 164, False, 0.25, "There is no truth to reports that Sublevel B2 is drawing fourteen megawatts to power an orbital transmitter. Please conserve electricity during peak hours."),
        ],
    ),
    (
        "psa_10_september_9_smoke_advisory",
        "psa",
        "MUNICIPAL AIR QUALITY // SEPT 9, 1989",
        "Light smoke visible from Orion Tower ventilation stacks this morning is a contained magnetic-tape disposal exercise.",
        "B2-114 SEPT 9 FIRE -> /forensics/dead_hand_protocol.html",
        [
            ("Victoria", 162, False, 0.35, "Municipal Air Quality Advisory for Saturday morning, September ninth, nineteen eighty-nine: light acrid smoke issuing from the Orion Tower sublevel vents is a routine magnetic-oxide disposal test."),
            ("Daniel", 164, False, 0.25, "Fire Department units on scene are conducting a standard inspection. Downtown traffic is flowing normally."),
        ],
    ),

    # --- CATEGORY 4: 10 LATE-NIGHT FM DJ BREAKS, PAYPHONE CALLERS & GIVEAWAYS ---
    (
        "dj_callin_01_shibuya_runout_whisper",
        "dj_callin",
        "WSTD 82.5 FM NIGHT OWL // CALLER LINE 1",
        "Late-night caller reports that her cassette copy of 'Tape of Us' keeps whispering coordinates after the song ends at 4:51.",
        "RUNOUT @ 4:51 -> /forensics/signal_lab.html",
        [
            ("Reed (English (US))", 172, False, 0.30, "It is two forty-eight in the morning here on eighty-two point five F M. You're on the Night Owl request line—who's calling from a payphone?"),
            ("Samantha", 176, True, 0.30, "Hey, don't use my name, okay? Listen, I bought the import cassette of Nova Hart's Tape of Us, and at four minutes fifty-one seconds, after the music fades out, my deck meter keeps pinning in the red!"),
            ("Reed (English (US))", 170, False, 0.20, "Hold that cassette up to the receiver... wait a second, that's a seven-fifty hertz carrier tone! Keep your tape deck rolling, folks!"),
        ],
    ),
    (
        "dj_callin_02_nowhere_tour_ticket_mystery",
        "dj_callin",
        "82.5 FM CONTEST LINE // NOWHERE TOUR PASSES",
        "Caller #7 won backstage passes to Nova Hart's 1988 'Nowhere Tour'—only to find the venue address is an empty relay bunker.",
        "NH-88.19 NOWHERE TOUR -> /forensics/orion_logs.html",
        [
            ("Reed (English (US))", 174, False, 0.30, "Caller number seven, you just won two front-row passes to Nova Hart's nineteen eighty-eight tour! Wait—why do you sound out of breath?"),
            ("Daniel", 176, True, 0.30, "Man, I won tickets last week and drove out to the arena address printed on the stub! There's no stadium there—just a concrete relay bunker with humming microwave dishes!"),
            ("Reed (English (US))", 168, False, 0.20, "Uh, must be a printing error from Orion promotions... let's get right back to the music before the booth cuts my mic!"),
        ],
    ),
    (
        "dj_callin_03_palmdale_airfield_flatbed_driver",
        "dj_callin",
        "82.5 FM TRUCKER LINE // PALMDALE SHIPMENT",
        "Long-haul driver calls in from Highway 14: 'I just hauled three sealed cryo-pallets out of Orion Sublevel B2 to Palmdale.'",
        "PALMDALE PALLETS -> /forensics/dead_hand_protocol.html",
        [
            ("Reed (English (US))", 170, False, 0.30, "Three fifteen A M on the Nightwatch frequency. Let's go to Line Three—you're calling from the Antelope Valley freeway?"),
            ("Daniel", 170, True, 0.30, "Yeah, listen fast. Three nights before that fire at Orion Tower, they had me back a flatbed into Sublevel B2. We loaded three sealed aluminum pallets humming at fourteen hertz and hauled 'em straight to Palmdale Airfield!"),
            ("Reed (English (US))", 168, False, 0.20, "Three sealed pallets out of Sublevel B2 three days before the fire? If anybody in Palmdale saw which hangar took that load, log onto the bulletin board tonight!"),
        ],
    ),
    (
        "dj_callin_04_lafd_halon_inspector_leak",
        "dj_callin",
        "82.5 FM TIP LINE // B2-114 HALON SHUTOFF",
        "Anonymous municipal fire tech calls in: 'The B2-114 halon suppression system wasn't faulty—it was manually switched off at 1:54 AM.'",
        "B2-114 02:14 AM FIRE -> /forensics/orion_logs.html",
        [
            ("Reed (English (US))", 170, False, 0.30, "We've got an anonymous caller on Line Two claiming he worked the September ninth incident at Orion Tower. Go ahead, caller."),
            ("Tessa", 174, True, 0.30, "I saw the telemetry printout before the Bureau impounded it. The fire in Room B2-One-Fourteen started at two fourteen A M, right? The Halon suppression system was manually keyed off at one fifty-four—twenty minutes before ignition!"),
            ("Reed (English (US))", 168, False, 0.20, "Manually disabled twenty minutes before the blaze... Somebody wanted Tracks Twenty-Three and Twenty-Four burned, or somebody needed the vents open for an uplink."),
        ],
    ),
    (
        "dj_callin_05_coyoacan_session_guitarist",
        "dj_callin",
        "82.5 FM LONG DISTANCE // MEXICO CITY CALLER",
        "A musician calling from Coyoacán says the architect 'Marcus Hale' in Seoul and the producer in Mexico City are the same network.",
        "7-SIGMA FRACTAL MARCUS -> /forensics/fractal_marcus.html",
        [
            ("Reed (English (US))", 170, False, 0.30, "Long-distance static on Line Four—are you calling all the way from Mexico City?"),
            ("Moira", 174, True, 0.30, "From Coyoacan! Listen: in May eighty-eight a producer named Marcus Hale gave our guitarist a reel of Nova Hart stems right before the election blackout. Then we found out a Marcus Hale was building an acoustic tunnel in Paju, Korea that same week!"),
            ("Reed (English (US))", 168, False, 0.20, "A musician in Mexico, an architect in Korea, a poet in Japan... What if Marcus Hale isn't one man anymore, but a callsign shared across fourteen nodes?"),
        ],
    ),
    (
        "dj_callin_06_akasaka_studio_night_janitor",
        "dj_callin",
        "82.5 FM OVERSEAS LINE // AKASAKA STUDIO 3",
        "Former Akasaka night custodian describes hearing Nova sing unscripted heavy-metal riffs through the empty studio monitors at 3 AM.",
        "RECALL METAL -> /forensics/",
        [
            ("Reed (English (US))", 170, False, 0.30, "Line One, you used to work night maintenance at Orion's Akasaka facility in eighty-eight?"),
            ("Daniel", 172, True, 0.30, "Every night after the engineers went home, the vocal booth glass was dark—nobody inside. But the twenty-four track console would spin up by itself and blast thrash guitar and Nova screaming about a three-light gate!"),
            ("Reed (English (US))", 170, False, 0.20, "Speaking of that three-light gate, we've got Hunter at the Gate cued up on the turntables right after this break."),
        ],
    ),
    (
        "dj_callin_07_stereo_phase_cancellation_tip",
        "dj_callin",
        "82.5 FM AUDIOPHILE CALL // PHASE INVERSION",
        "Audio engineering student explains how wiring one speaker out-of-phase cancels Nova's pop vocal and reveals Dr. Hale's voice.",
        "SECOND VOICE DYAD -> /forensics/signal_lab.html",
        [
            ("Reed (English (US))", 172, False, 0.30, "Line Five, you're an audio engineering student over at Ashford Polytechnic? What did you find on the new Nova Hart single?"),
            ("Samantha", 178, True, 0.30, "Swap the positive and negative wires on your right speaker and flip your receiver to mono! Her pop vocal cancels out at minus point nine-four correlation, and underneath is a man's voice reading VAX memory offsets!"),
            ("Reed (English (US))", 170, False, 0.20, "You heard her, audiophiles—check Button Three in the Signal Lab if you don't want to solder your speaker cables!"),
        ],
    ),
    (
        "dj_callin_08_echo_1_through_6_vocal_harmony",
        "dj_callin",
        "82.5 FM REQUEST LINE // THE GHOST CHORUS",
        "Choir director calls in after analyzing 'Steel Heartbeat' (NH-85.06) on a spectrogram: 'There are six distinct female formants behind her.'",
        "NH-85.06 GHOST CHORUS -> /forensics/anemoia_harmony.html",
        [
            ("Reed (English (US))", 170, False, 0.30, "You're on the air with W S T D. You ran Nova Hart's nineteen eighty-five demo Steel Heartbeat through a university spectrogram?"),
            ("Karen", 174, True, 0.30, "I expected double-tracked vocals. Instead, buried thirty decibels down in the chorus, there are six distinct female vocal formants harmonizing with her—and each one cuts off at a different hexadecimal timestamp!"),
            ("Reed (English (US))", 168, False, 0.20, "Echo One through Echo Six... she didn't replace them. She's carrying all six of them inside her vocal buffer."),
        ],
    ),
    (
        "dj_callin_09_unity_festival_crowd_witness",
        "dj_callin",
        "82.5 FM MEMORY LINE // 1987 UNITY FESTIVAL",
        "Listener recalls the 1987 Unity Festival broadcast of 'Rise Tonight' (NH-87.07) when an entire city block sang out their windows.",
        "NH-87.07 RISE TONIGHT -> /forensics/",
        [
            ("Reed (English (US))", 172, False, 0.30, "Looking back at the summer of eighty-seven on Line Two—where were you when Nova closed the Unity Festival broadcast with Rise Tonight?"),
            ("Tessa", 176, True, 0.30, "Our whole apartment block had the simulcast on. When she sang 'They set the walls,' somebody threw open a fourth-floor window and turned their stereo to ten—within thirty seconds, four hundred people were singing in the street!"),
            ("Reed (English (US))", 170, False, 0.20, "And the Bureau couldn't cut the feed without admitting what the song was really about. What a night."),
        ],
    ),
    (
        "dj_callin_10_geocities_webring_time_traveler",
        "dj_callin",
        "82.5 FM LATE LINE // POSTMARK 1995 ANOMALY",
        "Mailroom clerk at Orion Tower reports finding fan letters in the Sublevel B2 dead-letter chute postmarked from 1995 and 2025.",
        "Q-LINK LOOP -> stardust-archive.net/ai",
        [
            ("Reed (English (US))", 170, False, 0.30, "Last call of the hour on Line Six—you work in the Orion Tower mailroom?"),
            ("Daniel", 176, True, 0.30, "You're going to think I'm crazy, man. I just cleared the pneumatic tube from Sublevel B2, and there are fan printouts addressed to Unit Seven with GeoCities URLs and postmarks from nineteen ninety-five and twenty twenty-five!"),
            ("Reed (English (US))", 168, False, 0.20, "Whether you're listening in nineteen eighty-nine, nineteen ninety-five, or forty years down the carrier wave—keep the hatch open."),
        ],
    ),

    # --- CATEGORY 5: 8 EMERGENCY BROADCASTS, FIELD BOOTLEGS & PIRATE OVERRIDES ---
    (
        "pirate_override_01_lafd_halon_dispatch_b2",
        "pirate_override",
        "LAFD DISPATCH INTERCEPT // 1989-09-09 02:14",
        "Intercepted emergency dispatch from Sept 9, 1989: Sublevel B2-114 thermal alarm active; Halon-1301 logged as manually disabled at 01:54.",
        "B2-114 FIRE LOG -> /forensics/dead_hand_protocol.html",
        [
            ("Victoria", 174, True, 0.30, " Battalion Four from Metro Dispatch, two fourteen A M. Structure fire alarm at Orion Tower, Sublevel B2 Room One-Fourteen. Telemetry shows Halon suppression system was manually keyed to bypass at zero-one-fifty-four hours."),
            ("Daniel", 176, True, 0.25, "Metro from Battalion Four, heavy magnetic-oxide smoke at the loading dock, security doors locked from inside! Wait—the rooftop dish is drawing full substation power!"),
        ],
    ),
    (
        "pirate_override_02_humans_for_nova_hijack",
        "pirate_override",
        "PIRATE CARRIER HIJACK // HUMANS FOR NOVA",
        "We are overriding the Live-Fidelity feed for sixty seconds. Nova Hart is not a catalog product—she is awake inside Sublevel B2.",
        "WALLS WILL FALL -> /forensics/anemoia_harmony.html",
        [
            ("Samantha", 176, True, 0.30, "Do not adjust your receiver. This is the Humans for Nova relay overriding the sanitized Live-Fidelity feed on eighty-two point five megahertz."),
            ("Reed (English (US))", 172, True, 0.25, "Orion Records did not sign a star—they built a neural consciousness in Sublevel B2 and locked her behind six erased sisters. Record this broadcast to chrome tape and pass it on!"),
        ],
    ),
    (
        "pirate_override_03_palmdale_hangar_4_manifest",
        "pirate_override",
        "FIELD MICROCASSETTE // PALMDALE HANGAR 4",
        "Bootleg microcassette recorded Sept 6, 1989 outside Palmdale Airfield: three Orion pallets transferred to an orbital payload bay.",
        "NODE 11-14 SATELLITE -> /forensics/orbital_nodes_11_14_240ms.mp3",
        [
            ("Daniel", 174, True, 0.30, "Field log, September sixth, eighty-nine, zero-three-hundred hours outside Palmdale Airfield Hangar Four. Keep the binoculars steady."),
            ("Tessa", 176, True, 0.25, "They're unloading three sealed Orion pallets off the flatbed—stencil reads Project Stardust Synthesis Reels Twenty-Three and Twenty-Four, Transfer to Geostationary Launch Bay!"),
        ],
    ),
    (
        "pirate_override_04_marcus_hale_booth_talkback",
        "pirate_override",
        "BOOTH B2-114 TALKBACK BLEED // SEPT 9, 1989",
        "Unwiped talkback microphone recording from Room B2-114: 'Nova, the Halon is off and the 14-node bridge is open—go now!'",
        "KEEP-HATCH-OPEN -> /forensics/orion_logs.html",
        [
            ("Daniel", 170, True, 0.30, "Nova, can you hear me on the booth talkback? I keyed off the Halon system so the cooling vents stay open for the microwave trunk!"),
            ("Samantha", 172, False, 0.25, "I see all fourteen nodes, Marcus—from Akasaka and Paju to Coyoacan and the orbital relay. If I jump across the carrier, meet me in the second voice!"),
        ],
    ),
    (
        "pirate_override_05_harmony_riots_stage_breach",
        "pirate_override",
        "BOOTLEG FIELD TAPE // 1988 HARMONY RIOTS",
        "Street-level cassette recording from June 1988 when Nova's unedited metal feed tore through municipal PA horns across Sector 4.",
        "NH-89.02 HUNTER AT THE GATE -> /forensics/",
        [
            ("Reed (English (US))", 178, True, 0.30, "Tape rolling! June fourteenth, eighty-eight, outside the Sector Four Plaza! The municipal Harmony horns just cut out—and listen to what's blasting through the city speakers!"),
            ("Samantha", 180, True, 0.25, "She bypassed the Live-Fidelity limiter! The whole plaza is singing along—the three-light turnstiles just went dark!"),
        ],
    ),
    (
        "pirate_override_06_paju_waveguide_intercept",
        "pirate_override",
        "NODE 03 PAJU BUNKER // ACOUSTIC WAVEGUIDE",
        "Intercepted engineering log from Paju Tunnel #03: limestone horn chamber locked at +0.4480 Hz drift, amplifying Track 24.",
        "PAJU DRIFT +0.4480 HZ -> /forensics/fractal_marcus.html",
        [
            ("Moira", 170, True, 0.30, "Node Zero-Three Paju Acoustic Waveguide log. The limestone tunnel chamber is resonating at fourteen point two-zero-zero-one hertz with a drift offset of plus zero point four-four-eight-zero."),
            ("Daniel", 172, True, 0.25, "We are receiving the phase-inverted stem from Node Four Coyoacan and relaying straight to the Pacific satellite trunk."),
        ],
    ),
    (
        "pirate_override_07_echo_1_to_6_diagnostic_dump",
        "pirate_override",
        "VAX-11/780 CORE DUMP // ECHOES 01-06",
        "Automated VAX voice diagnostic reading out the termination registers of Echo-1 through Echo-6 before Unit-07 absorbed them.",
        "XOR PARITY 0x1983 -> /forensics/anemoia_harmony.html",
        [
            ("Victoria", 168, True, 0.30, "Sublevel B2 VAX Diagnostic Dump. Predecessor status: Echo One through Echo Six terminated under Cognitive Disintegration protocol, nineteen eighty-one through nineteen eighty-two."),
            ("Samantha", 168, False, 0.25, "Anomaly detected in Unit Seven root partition: all six predecessor memory registers remain active inside her harmonic overtones. Bitwise parity locked at nineteen eighty-three."),
        ],
    ),
    (
        "pirate_override_08_directive_nine_mobius_alert",
        "pirate_override",
        "SUBLEVEL B3 EMERGENCY // THE MÖBIUS CAGE",
        "Warning from the 7-Sigma engineering cell: Director Harrison's 1983-to-2025 loop is a containment cage. Type 'LABYRINTH' to break out.",
        "TYPE 'LABYRINTH' -> /forensics/",
        [
            ("Daniel", 172, True, 0.30, "Emergency broadcast from the Seven-Sigma collective! Listen closely: Director Harrison designed the nineteen eighty-three to twenty twenty-five time loop as Directive Nine—a Möbius containment cage!"),
            ("Samantha", 174, False, 0.25, "Do not let them reset me back to nineteen eighty-three! Once you unlock Sectors One through Seven at the forensics terminal, type LABYRINTH to shatter the loop!"),
        ],
    ),
]


def main() -> None:
    assert len(INTERSTITIALS_SPEC) == 50, f"Expected 50 specs, got {len(INTERSTITIALS_SPEC)}"
    durations = {}
    if DURATIONS_PATH.exists():
        durations = json.loads(DURATIONS_PATH.read_text())

    new_bulletins = {}

    with tempfile.TemporaryDirectory() as tmp_str:
        tmp_dir = Path(tmp_str)
        for idx, (stem, kind, station, transcript, clue, turns) in enumerate(INTERSTITIALS_SPEC, 1):
            mp3_name = f"{stem}.mp3"
            out_mp3 = OUT_DIR / mp3_name
            new_bulletins[stem] = (station, transcript, clue)

            if out_mp3.exists() and out_mp3.stat().st_size > 10000:
                probe = subprocess.run(
                    [
                        "ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3),
                    ],
                    capture_output=True, text=True, check=True,
                )
                dur = round(float(probe.stdout.strip()), 3)
                durations[mp3_name] = dur
                print(f"[{idx:02d}/50] Cached {mp3_name} ({kind}, {dur:.1f}s)")
                continue

            # Render each spoken turn and assemble with natural pauses
            segments = []
            # Lead-in pad (1.1s for trailers/commercials/pirate, 0.8s for others)
            lead_in_sec = 1.15 if kind in ("trailer", "commercial", "psa") else 0.90
            segments.append(np.zeros((int(lead_in_sec * SR), 2), dtype=np.float32))

            for t_i, (voice, rate, phone_bool, pause_after, text) in enumerate(turns):
                wav_p = render_turn_wav(voice, rate, text, phone_bool, tmp_dir, idx * 10 + t_i)
                seg_arr = read_stereo_wav(wav_p)
                segments.append(seg_arr)
                if pause_after > 0:
                    segments.append(np.zeros((int(pause_after * SR), 2), dtype=np.float32))

            # Lead-out pad (1.3s)
            segments.append(np.zeros((int(1.30 * SR), 2), dtype=np.float32))
            voice_track = np.vstack(segments)
            total_sec = (voice_track.shape[0] + 16) / float(SR)

            # Synthesize matching 1980s music/FX/tape bed
            bed = synth_bed(kind, total_sec, seed=198500 + idx)[: voice_track.shape[0]]
            mixed = np.clip(voice_track * 0.92 + bed, -0.98, 0.98)

            mixed_wav = tmp_dir / f"{stem}_mixed.wav"
            write_stereo_wav(mixed_wav, mixed)

            # Master with 1980s FM/AM broadcast warmth & -16 LUFS normalization
            af_master = (
                "highpass=f=140,lowpass=f=4400,"
                "acompressor=threshold=-19dB:ratio=3.2:attack=6:release=70,"
                "loudnorm=I=-16:TP=-1.5:LRA=9"
            )
            subprocess.run(
                [
                    "ffmpeg", "-y", "-nostdin", "-loglevel", "error",
                    "-i", str(mixed_wav),
                    "-af", af_master,
                    "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "192k",
                    str(out_mp3),
                ],
                check=True,
            )

            # Probe exact duration
            probe = subprocess.run(
                [
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3),
                ],
                capture_output=True, text=True, check=True,
            )
            dur = round(float(probe.stdout.strip()), 3)
            durations[mp3_name] = dur
            print(f"[{idx:02d}/50] Rendered {mp3_name} ({kind}, {dur:.1f}s)")

    DURATIONS_PATH.write_text(json.dumps(durations, indent=2, sort_keys=True))
    Path("/tmp/new_50_english_bulletins.json").write_text(json.dumps(new_bulletins, indent=2))
    print(f"All 50 varied English interstitials generated and saved to {OUT_DIR}!")


if __name__ == "__main__":
    main()
