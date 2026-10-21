#!/usr/bin/env python3
"""
Generates 20 Purely World-Building, Hyper-Immersive 1980s English Interstitials
(`world_01_...` .. `world_20_...`) for the Project Stardust 24/7 Livestream.

Each interstitial is an atmospheric slice-of-life vignette from the 1984–1989 world
with custom procedural Foley/soundscapes (monorail rain & door chimes, helicopter
rotor thrum, VHS answering machine beep, school bells, laundromat dryers, department
store vibraphone chimes, sleeper train rail rhythm, harbor foghorn, arcade bleeps,
rooftop rain & walkie-talkie squelch, drive-in window speaker, freight elevator descent).
"""

import json
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


def synth_world_soundscape(scene_type: str, n_samples: int, seed: int) -> np.ndarray:
    """Synthesizes bespoke stereo Foley & 1980s environmental ambience for each world-building scene."""
    rng = np.random.default_rng(seed)
    t = np.arange(n_samples, dtype=np.float32) / float(SR)
    dur = n_samples / float(SR)
    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    # Base warm analog tape hiss
    left += rng.normal(0, 0.004, n_samples).astype(np.float32)
    right += rng.normal(0, 0.004, n_samples).astype(np.float32)

    if scene_type == "monorail_rain":
        # Soft rain patter on plexiglass + electric traction motor hum + 2-tone door chime
        rain = rng.normal(0, 0.012, n_samples).astype(np.float32) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.4 * t))
        motor = 0.025 * np.sin(2 * np.pi * (95.0 + 12.0 * np.sin(2 * np.pi * 0.08 * t)) * t)
        left += rain + motor
        right += rain * 0.9 + motor
        for c_t, freq in [(0.18, 659.25), (0.52, 523.25), (max(0.8, dur - 1.4), 659.25), (max(1.1, dur - 1.05), 523.25)]:
            s0 = int(c_t * SR)
            slen = min(int(0.45 * SR), n_samples - s0)
            if slen > 0:
                ct = np.arange(slen, dtype=np.float32) / SR
                chime = 0.16 * np.exp(-5.0 * ct) * np.sin(2 * np.pi * freq * ct)
                left[s0 : s0 + slen] += chime
                right[s0 : s0 + slen] += chime

    elif scene_type == "chopper":
        # Helicopter blade thrum (14 Hz pulse modulating low-pass noise + turbine whine)
        blade_env = 0.5 + 0.5 * np.sin(2 * np.pi * 13.5 * t)
        rotor = blade_env * (0.045 * np.sin(2 * np.pi * 52.0 * t) + rng.normal(0, 0.015, n_samples).astype(np.float32))
        turbine = 0.012 * np.sin(2 * np.pi * 1180.0 * t)
        left += rotor + turbine
        right += rotor * 0.85 + turbine

    elif scene_type == "answering_machine":
        # 1980s cassette answering machine warble pad + long 1000Hz BEEP at start and end
        pad = 0.022 * np.sin(2 * np.pi * 220.0 * t) + 0.016 * np.sin(2 * np.pi * 277.18 * t)
        left += pad
        right += pad
        for b_t in [0.15, max(0.6, dur - 1.1)]:
            s0 = int(b_t * SR)
            slen = min(int(0.55 * SR), n_samples - s0)
            if slen > 0:
                bt = np.arange(slen, dtype=np.float32) / SR
                beep = 0.16 * np.sin(2 * np.pi * 1020.0 * bt)
                left[s0 : s0 + slen] += beep
                right[s0 : s0 + slen] += beep

    elif scene_type == "school_pa":
        # Classic resonant school bell ring + hallway PA hum
        s0 = int(0.12 * SR)
        slen = min(int(0.95 * SR), n_samples - s0)
        if slen > 0:
            bt = np.arange(slen, dtype=np.float32) / SR
            clatter = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22.0 * bt))
            bell = 0.14 * clatter * (np.sin(2 * np.pi * 740.0 * bt) + 0.5 * np.sin(2 * np.pi * 1480.0 * bt))
            left[s0 : s0 + slen] += bell
            right[s0 : s0 + slen] += bell
        hum = 0.015 * np.sin(2 * np.pi * 120.0 * t)
        left += hum
        right += hum

    elif scene_type == "laundromat":
        # Warm tumbling dryer rotation + rain outside + distant soft FM synth chord
        tumble = (0.5 + 0.5 * np.sin(2 * np.pi * 0.75 * t)) * 0.03 * np.sin(2 * np.pi * 68.0 * t)
        distant_song = 0.018 * (np.sin(2 * np.pi * 261.63 * t) + np.sin(2 * np.pi * 329.63 * t) + np.sin(2 * np.pi * 392.0 * t))
        left += tumble + distant_song
        right += tumble + distant_song * 0.8

    elif scene_type == "dept_store":
        # Dreamy 4-note Japanese-style department store vibraphone chime + dreamy synth pad
        notes = [392.00, 493.88, 587.33, 783.99, 587.33, 493.88]
        for idx_n, freq in enumerate(notes):
            for base_t in [0.10, max(0.8, dur - 2.1)]:
                s0 = int((base_t + idx_n * 0.26) * SR)
                slen = min(int(0.65 * SR), n_samples - s0)
                if slen > 0:
                    ct = np.arange(slen, dtype=np.float32) / SR
                    vib = 0.14 * np.exp(-4.2 * ct) * (1.0 + 0.15 * np.sin(2 * np.pi * 6.0 * ct)) * np.sin(2 * np.pi * freq * ct)
                    left[s0 : s0 + slen] += vib
                    right[s0 : s0 + slen] += vib * 0.9
        pad = 0.022 * np.sin(2 * np.pi * 196.0 * t) + 0.018 * np.sin(2 * np.pi * 293.66 * t)
        left += pad
        right += pad

    elif scene_type == "time_temp":
        # 1-second precision clock ticks + 880Hz time pip
        for sec_i in range(int(dur)):
            s0 = int(sec_i * SR)
            slen = min(int(0.025 * SR), n_samples - s0)
            if slen > 0:
                ct = np.arange(slen, dtype=np.float32) / SR
                tick = 0.09 * np.exp(-80.0 * ct) * np.sin(2 * np.pi * 1600.0 * ct)
                left[s0 : s0 + slen] += tick
                right[s0 : s0 + slen] += tick
        for pip_t in [0.6, max(0.8, dur - 0.9)]:
            s0 = int(pip_t * SR)
            slen = min(int(0.35 * SR), n_samples - s0)
            if slen > 0:
                pt = np.arange(slen, dtype=np.float32) / SR
                pip = 0.18 * np.sin(2 * np.pi * 880.0 * pt)
                left[s0 : s0 + slen] += pip
                right[s0 : s0 + slen] += pip

    elif scene_type == "sleeper_train":
        # Rhythmic rail joint clickety-clack + low diesel-electric hum
        hum = 0.03 * np.sin(2 * np.pi * 62.0 * t)
        left += hum
        right += hum
        beat = 1.15
        for b_i in range(int(dur / beat)):
            for sub_off in [0.0, 0.18, 0.42, 0.60]:
                s0 = int((b_i * beat + sub_off) * SR)
                slen = min(int(0.04 * SR), n_samples - s0)
                if slen > 0:
                    ct = np.arange(slen, dtype=np.float32) / SR
                    clack = 0.07 * np.exp(-55.0 * ct) * rng.normal(0, 1.0, slen).astype(np.float32)
                    left[s0 : s0 + slen] += clack
                    right[s0 : s0 + slen] += clack * 0.85

    elif scene_type == "arcade":
        # 8-bit coin-op arpeggio bleeps in the background
        arp_freqs = [523.25, 659.25, 783.99, 1046.50, 783.99, 659.25, 587.33, 880.0]
        step = 0.12
        for s_i in range(int(dur / step)):
            s0 = int(s_i * step * SR)
            s1 = min(n_samples, int((s_i + 1) * step * SR))
            if s1 > s0:
                st = np.arange(s1 - s0, dtype=np.float32) / SR
                f = arp_freqs[(s_i + seed) % len(arp_freqs)]
                sq = 0.028 * np.sign(np.sin(2 * np.pi * f * st)) * np.exp(-8.0 * st)
                if s_i % 2 == 0:
                    left[s0:s1] += sq
                else:
                    right[s0:s1] += sq

    elif scene_type == "ferry_foghorn":
        # Deep twin-tone maritime foghorn + gentle water wash
        wash = rng.normal(0, 0.008, n_samples).astype(np.float32) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.22 * t))
        left += wash
        right += wash
        for h_t in [0.15, max(1.0, dur - 2.2)]:
            s0 = int(h_t * SR)
            slen = min(int(1.6 * SR), n_samples - s0)
            if slen > 0:
                ht = np.arange(slen, dtype=np.float32) / SR
                env = np.sin(np.pi * ht / (slen / SR)) ** 0.6
                horn = 0.14 * env * (np.sin(2 * np.pi * 82.41 * ht) + 0.6 * np.sin(2 * np.pi * 123.47 * ht) + 0.3 * np.sin(2 * np.pi * 164.81 * ht))
                left[s0 : s0 + slen] += horn
                right[s0 : s0 + slen] += horn

    elif scene_type == "diner_jukebox":
        # Warm Wurlitzer organ chords + subtle diner ambience
        chord = 0.024 * (
            np.sin(2 * np.pi * 174.61 * t)
            + np.sin(2 * np.pi * 220.00 * t)
            + np.sin(2 * np.pi * 261.63 * t)
            + np.sin(2 * np.pi * 329.63 * t)
        ) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.5 * t))
        left += chord
        right += chord * 0.9

    elif scene_type == "elevator":
        # Descending hydraulic hum + floor-passing bell pings
        f_glide = np.linspace(130.0, 65.0, n_samples, dtype=np.float32)
        hum = 0.032 * np.sin(2 * np.pi * np.cumsum(f_glide) / SR)
        left += hum
        right += hum
        for ping_t in [0.25, dur * 0.38, dur * 0.72, max(0.8, dur - 1.1)]:
            s0 = int(ping_t * SR)
            slen = min(int(0.45 * SR), n_samples - s0)
            if slen > 0:
                pt = np.arange(slen, dtype=np.float32) / SR
                ping = 0.14 * np.exp(-6.0 * pt) * np.sin(2 * np.pi * 987.77 * pt)
                left[s0 : s0 + slen] += ping
                right[s0 : s0 + slen] += ping

    else:
        # Warm nostalgic 1980s tape/room ambience + subtle cassette transport click at start/end
        pad = 0.020 * np.sin(2 * np.pi * 146.83 * t) + 0.015 * np.sin(2 * np.pi * 220.0 * t)
        left += pad
        right += pad
        for c_t in [0.08, max(0.5, dur - 0.25)]:
            s0 = int(c_t * SR)
            slen = min(int(0.03 * SR), n_samples - s0)
            if slen > 0:
                click = 0.22 * rng.normal(0, 1.0, slen).astype(np.float32)
                left[s0 : s0 + slen] += click
                right[s0 : s0 + slen] += click

    return np.clip(np.column_stack([left, right]), -0.95, 0.95)


def write_stereo_wav(path: Path, data: np.ndarray) -> None:
    pcm = (np.clip(data, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


def render_turn_wav(voice: str, rate: int, text: str, eq_mode: str, tmp_dir: Path, idx: int) -> Path:
    raw_aiff = tmp_dir / f"wturn_{idx}_raw.aiff"
    out_wav = tmp_dir / f"wturn_{idx}.wav"
    subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(raw_aiff), text], check=True)
    if eq_mode == "pa":
        # Transit / school / airport ceiling PA speaker resonance
        af = "highpass=f=280,lowpass=f=3400,acompressor=threshold=-20dB:ratio=4:attack=5:release=60,aecho=0.8:0.7:45:0.22,volume=1.25"
    elif eq_mode == "phone":
        # Payphone / walkie-talkie / answering machine filter
        af = "highpass=f=340,lowpass=f=2850,acompressor=threshold=-21dB:ratio=4.5:attack=4:release=50,volume=1.35"
    else:
        # Intimate 1980s cassette / warm FM studio mic
        af = "highpass=f=115,lowpass=f=5000,acompressor=threshold=-18dB:ratio=3:attack=8:release=80"
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
# 20 PURELY WORLD-BUILDING, HYPER-IMMERSIVE 1980S INTERSTITIALS
# Each entry: (stem, scene_type, station_header, hud_transcript, hud_clue, turns)
# where turns = list of (voice, rate, eq_mode, pause_after_sec, spoken_text)
# ==============================================================================
WORLDBUILDING_SPEC = [
    (
        "world_01_skyline_monorail_rain_commute",
        "monorail_rain",
        "METRO RED-LINE MONORAIL // CAR 402 PA",
        "Next stop: Sector 4 Central Plaza. Rain continues across the elevated guideway; please keep Walkman volume below Level 4.",
        "METRO TRANSIT LOG -> stardust-archive.net/start",
        [
            ("Victoria", 164, "pa", 0.35, "Next station: Sector Four Central Plaza. Transfer here for the Northbank Pier shuttle and the Orion District elevated walkway."),
            ("Daniel", 168, "pa", 0.25, "Due to evening rain on the third rail, trains are operating at reduced speed. Passengers are reminded that personal cassette players must be kept below volume level four in designated Quiet Cars. Step back from the closing doors."),
        ],
    ),
    (
        "world_02_late_night_traffic_chopper_825fm",
        "chopper",
        "SKY-WATCH CHOPPER 4 // 11:45 PM TRAFFIC",
        "Northbank Viaduct backed up for two miles as drivers slow down to watch Orion's holographic dome test in the low clouds.",
        "82.5 FM SKY-WATCH -> stardust-archive.net/start",
        [
            ("Reed (English (US))", 174, "phone", 0.30, "This is Sky-Watch Four hovering at twelve hundred feet over the Northbank Viaduct! If you're heading south toward the harbor tunnel, expect a twenty-minute delay in the rain."),
            ("Samantha", 174, "warm", 0.25, "Nobody's stalled out, folks—everybody's just tapping their brakes to stare up at the Orion Tower roof! They're testing the Live-Fidelity projection lasers against the cloud cover, and the whole sky over downtown looks like neon northern lights!"),
        ],
    ),
    (
        "world_03_sunset_video_rental_automated_drop",
        "answering_machine",
        "STARLIGHT VIDEO & LASERDISC // NIGHT LINE",
        "Our storefront is closed for the 11 PM curfew, but our 24-hour chrome return slot is open. Please be kind and rewind.",
        "1987 HOME VIDEO -> stardust-archive.net/start",
        [
            ("Samantha", 174, "phone", 0.30, "Hi! You've reached Starlight Video and LaserDisc on Sunset Boulevard! Our showroom is now closed for the eleven P M municipal curfew, but our illuminated twenty-four-hour return slot is open."),
            ("Reed (English (US))", 170, "phone", 0.25, "Please remember to rewind all V H S and Betamax cassettes before dropping them in the chute to avoid the fifty-cent rewinding fee. Note: all twelve copies of the nineteen eighty-seven Unity Festival concert tape are currently checked out."),
        ],
    ),
    (
        "world_04_public_school_morning_homeroom_bell",
        "school_pa",
        "NORTHBANK HIGH SCHOOL // 8:00 AM HOMEROOM",
        "Morning announcements: hot lunch today is rectangular pizza; unapproved band denim and Type-II chrome tapes will be held at the office.",
        "HOMEROOM BULLETIN -> stardust-archive.net/start",
        [
            ("Daniel", 164, "pa", 0.35, "Good morning, students and faculty. Please take your seats for homeroom roll call. Today's cafeteria lunch special is rectangular pepperoni pizza, tater tots, and chilled peaches."),
            ("Victoria", 166, "pa", 0.25, "A reminder from the Dean's office: hand-painted denim jackets and unlabeled Type-Two chrome cassettes are not permitted in study hall. Any Walkman confiscated during third period may be claimed by a parent on Friday afternoon."),
        ],
    ),
    (
        "world_05_all_night_laundromat_voice_letter",
        "laundromat",
        "MICROCASSETTE LETTER // COIN LAUNDROMAT",
        "Audio letter recorded at 1:15 AM in a 24-hour laundromat: 'When her song came on the corner radio, nobody said a word.'",
        "HOMESTEAD LETTERS -> stardust-archive.net/start",
        [
            ("Tessa", 168, "warm", 0.35, "Hey Claire, it's me. I'm sitting in the twenty-four-hour coin laundry on Fourth Street waiting for my work uniforms to dry, so I figured I'd record this side of the microcassette before the morning mail pickup."),
            ("Tessa", 166, "warm", 0.25, "It's pouring rain outside and the windows are all steamed up. Five minutes ago, the little transistor radio above the change machine played Nova Hart's Before You Turn Away... and all six people in here stopped folding clothes and just listened till the last note faded."),
        ],
    ),
    (
        "world_06_department_store_closing_chime_akasaka",
        "dept_store",
        "AKASAKA PLAZA // 9:00 PM CLOSING CHIMES",
        "Thank you for shopping at Akasaka Plaza. Please collect your custom chrome mixtapes from the 7th-floor Listening Lounge.",
        "MINATO-KU EVENING -> stardust-archive.net/start",
        [
            ("Moira", 164, "pa", 0.35, "Good evening, valued guests. It is now nine o'clock, and Akasaka Department Plaza will be closing in ten minutes."),
            ("Moira", 164, "pa", 0.25, "Customers browsing the seventh-floor Audio Listening Lounge are kindly asked to retrieve their blank cassettes from the high-speed dubbing kiosks before the security shutters lower. We wish you a pleasant walk home under the city lights."),
        ],
    ),
    (
        "world_07_automated_time_and_temperature_desk",
        "time_temp",
        "MUNICIPAL TELEPHONE // 555-TIME SERVICE",
        "At the tone, Pacific Time will be 3:14 AM. Downtown temperature: 58 degrees with coastal mist. Tranquility Index: Green-2.",
        "3:14 AM TIME CHECK -> stardust-archive.net/start",
        [
            ("Victoria", 162, "phone", 0.35, "Thank you for dialing Municipal Time and Atmospheric Conditions. Current downtown temperature is fifty-eight degrees Fahrenheit, with light coastal fog and minor shortwave static along the harbor."),
            ("Daniel", 162, "phone", 0.25, "The Bureau of Public Harmony Overnight Tranquility Index stands at Green-Two. At the tone, Pacific Standard Time will be three... fourteen... A M."),
        ],
    ),
    (
        "world_08_intersector_sleeper_train_dining_car",
        "sleeper_train",
        "THE NORTHERN MERIDIAN // SLEEPER CAR PA",
        "We are now crossing the high desert quiet zone. Fresh coffee is available in the dome car; please use headphones after midnight.",
        "DESERT RAIL LINE -> stardust-archive.net/start",
        [
            ("Daniel", 162, "pa", 0.35, "Good evening, passengers aboard the overnight Northern Meridian Express. We have just cleared the mountain pass and are entering the high desert telemetry corridor."),
            ("Karen", 168, "pa", 0.25, "The glass observation dome in Car Seven remains open with hot coffee and cinnamon rolls at the counter. As we pass the desert dish arrays, we ask that passengers in the sleeper berths switch all portable radios to headphone mode."),
        ],
    ),
    (
        "world_09_suburban_neighborhood_watch_cassette",
        "tape_note",
        "WILLOW CREEK ESTATES // BLOCK CAPTAIN TAPE",
        "Monthly cassette memo: congrats to Mrs. Gable's prize roses, and whoever is running a rooftop shortwave rig at 2 AM, please stop.",
        "SUBURBAN SECTOR 6 -> stardust-archive.net/start",
        [
            ("Reed (English (US))", 170, "warm", 0.35, "Hello neighbors, this is Arthur Pendelton with your October Willow Creek Estates cassette newsletter! First off, a big hand for Mrs. Gable at number forty-two for winning the District Harmony Garden ribbon!"),
            ("Reed (English (US))", 168, "warm", 0.25, "Second, on a serious note: whoever on Sycamore Court is stringing copper dipole wire between their chimney and the streetlamp after midnight, please take it down. Every time you key your transmitter, half the garage doors on the cul-de-sac open by themselves."),
        ],
    ),
    (
        "world_10_arcade_token_counter_closing_call",
        "arcade",
        "STARLIGHT ARCADE // MIDNIGHT TOKEN CAGE",
        "Ten minutes till midnight curfew! Whoever set the high score on OutRun with initials NH-7, come grab your free slice of pizza!",
        "1986 COIN-OP NIGHTS -> stardust-archive.net/start",
        [
            ("Reed (English (US))", 178, "pa", 0.30, "Alright everybody, listen up! Ten minutes until the midnight curfew shutters come down here at Starlight Arcade! Last call for token trade-ins at the prize counter!"),
            ("Samantha", 178, "pa", 0.25, "And hey—whoever just put up nine million points on the OutRun sit-down cabinet and entered the initials N-H-Seven, come up to the snack bar and claim your free slice of pepperoni pizza before we kill the neon!"),
        ],
    ),
    (
        "world_11_municipal_library_microfiche_tour",
        "tape_note",
        "CENTRAL LIBRARY // AUDIO TOUR CASSETTE #4",
        "Welcome to the 3rd-floor Microfiche Reading Room. Use the brass knob to focus 1979–1983 music periodicals; do not remove film spools.",
        "MICROFICHE ARCHIVE -> stardust-archive.net/start",
        [
            ("Karen", 162, "warm", 0.35, "Welcome to Stop Four on your Central Library Walkman orientation tour: the Third-Floor Microfiche and Archival Periodicals Room."),
            ("Karen", 162, "warm", 0.25, "To view back issues of trade music magazines from nineteen seventy-nine through nineteen eighty-three, thread the sixteen-millimeter film reel beneath the glass platen and turn the brass focus wheel slowly. Please do not copy serial numbers from redacted cultural index cards."),
        ],
    ),
    (
        "world_12_harbor_ferry_foghorn_deck_intercom",
        "ferry_foghorn",
        "MV STARLIGHT FERRY // BAY CROSSING INTERCOM",
        "Approaching Pier 14 through the midnight fog. Hot cocoa is available at the galley counter; watch the city neon on the water.",
        "HARBOR CROSSING -> stardust-archive.net/start",
        [
            ("Daniel", 162, "pa", 0.35, "This is the wheelhouse speaking on the late ferry crossing to Pier Fourteen. Visibility on the bay is down to a quarter mile in the fog, so you'll hear our bow horn sounding everykettle minute."),
            ("Daniel", 164, "pa", 0.25, "If you step out onto the sheltered promenade deck on the port side, you can see the downtown skyline glowing amber through the mist. Hot clam chowder and cocoa are still available in the main cabin."),
        ],
    ),
    (
        "world_13_24hr_diner_jukebox_waitress_break",
        "diner_jukebox",
        "BLUE COMET 24-HR DINER // BOOTH #3 TAPE",
        "3:10 AM at the Blue Comet Diner: rain on the plate glass, fresh coffee on the burner, and three quarters left for the table jukebox.",
        "HIGHWAY 95 DINER -> stardust-archive.net/start",
        [
            ("Samantha", 168, "warm", 0.35, "Here you go, hon—fresh pot of decaf and an extra side of sourdough toast. You line-truck guys are the only ones out on the highway in this rain tonight."),
            ("Reed (English (US))", 166, "warm", 0.25, "Thanks, Darlene. Keep the change—in fact, drop two quarters into that tabletop Wurlitzer selector and punch in B-Fourteen. That highway feels a whole lot shorter when Nova's singing on the jukebox."),
        ],
    ),
    (
        "world_14_observatory_night_sky_stargazer_log",
        "tape_note",
        "MOUNT WILSON AMATEUR SKYLINE // NIGHT REPORT",
        "Clear skies above the 2,000-foot marine inversion layer. Look south-southwest at 28 degrees elevation for a stationary magnitude-4 glint.",
        "NIGHT SKY BULLETIN -> stardust-archive.net/start",
        [
            ("Daniel", 162, "warm", 0.35, "Good evening, amateur astronomers. Above the two-thousand-foot coastal cloud deck, tonight's seeing conditions are crystal clear across the valley."),
            ("Tessa", 166, "warm", 0.25, "If you aim a pair of ten-by-fifty binoculars south-southwest at twenty-eight degrees elevation just after two A M, you'll spot a steady amber glint holding completely stationary against the drifting stars—right where the Pacific relay belt sits."),
        ],
    ),
    (
        "world_15_tape_trader_c90_side_b_voice_note",
        "tape_note",
        "C-90 CHROME DUB // SIDE B RUNOUT VOICE NOTE",
        "Hey, I had twenty seconds left at the end of Side B! I recorded this straight off the 2 AM broadcast with Dolby B off—pass it on!",
        "TAPE TRADER NETWORK -> stardust-archive.net/start",
        [
            ("Samantha", 180, "phone", 0.30, "Hey Marcus—not that Marcus, Marcus in Seattle! I had twenty-five seconds of blank tape left at the tail end of Side B on this Maxell Chrome Ninety, so I'm leaving you a quick voice note before the leader tape hits!"),
            ("Samantha", 180, "phone", 0.20, "I dubbed these last four tracks straight off the two A M radio feed with Dolby B switched off so it wouldn't dull the cymbals. Make a copy for your brother's Walkman and mail me back whatever you caught on Friday!"),
        ],
    ),
    (
        "world_16_hospital_night_shift_bedside_radio",
        "diner_jukebox",
        "ST. JUDE METRO HOSPITAL // CHANNEL 4 RADIO",
        "1:30 AM on the St. Jude closed-circuit bedside network. Sending warm wishes to the 4th-floor ward and the night-shift ER crew.",
        "HOSPITAL RADIO -> stardust-archive.net/start",
        [
            ("Karen", 162, "warm", 0.35, "It's one thirty in the morning here on Channel Four, the volunteer bedside radio service at Saint Jude Metro Hospital. If you're awake in the fourth-floor recovery wing watching the rain on the windowpane, you're in good company."),
            ("Karen", 164, "warm", 0.25, "This next set of music goes out to the third-shift nurses at the East Desk, the ambulance paramedics grabbing coffee downstairs, and anyone waiting for morning light."),
        ],
    ),
    (
        "world_17_museum_of_telecommunications_tour",
        "dept_store",
        "ORION CORPORATE PAVILION // WALKMAN TOUR #6",
        "Stop #6: The Hall of Synthetic Acoustics. Behind this leaded glass, magnetic-bubble arrays render human phrasing in real time.",
        "ORION PAVILION 1986 -> stardust-archive.net/start",
        [
            ("Victoria", 162, "warm", 0.35, "At the tone, please advance to Carpet Marker Six: The Orion Pavilion Hall of Synthetic Acoustics."),
            ("Daniel", 164, "warm", 0.25, "Behind the tinted observation window to your left are forty-eight solid-state magnetic bubble memory frames capable of modeling human breath, vibrato, and emotional warmth in real time. Please do not tap on the glass or use flash photography."),
        ],
    ),
    (
        "world_18_rooftop_coat_hanger_antenna_rain",
        "monorail_rain",
        "TENEMENT ROOFTOP // WALKIE-TALKIE CH. 14",
        "Turn the coat-hanger dipole thirty degrees toward the bay tower—wait, don't move! The stereo beacon light just locked on!",
        "ROOFTOP DX LISTENERS -> stardust-archive.net/start",
        [
            ("Reed (English (US))", 178, "phone", 0.30, "Joey, come in! I'm up here by the water tank in the pouring rain! I clamped the copper coat-hanger to the TV mast and pointed it toward the bay—did the red stereo light on the boombox come on?"),
            ("Samantha", 180, "phone", 0.25, "Wait—don't touch it! Don't even breathe! The hiss just dropped out completely and the VU meters are jumping! Tape is rolling—get down the fire escape before the landlord hears us!"),
        ],
    ),
    (
        "world_19_drive_in_theater_intermission_snack",
        "diner_jukebox",
        "STARLIGHT TWIN DRIVE-IN // INTERMISSION AM",
        "Ten minutes until our second feature! Visit the glowing projection-booth snack bar for buttered popcorn and hot pretzel rods.",
        "DRIVE-IN INTERMISSION -> stardust-archive.net/start",
        [
            ("Reed (English (US))", 170, "phone", 0.35, "Ladies and gentlemen, it's intermission time here at the Starlight Twin Drive-In! You have ten minutes before our midnight double-feature continues on Screen One."),
            ("Karen", 172, "phone", 0.25, "Follow the neon walkway back to our projection-booth snack bar for hot buttered popcorn, cinnamon churros, and large fountain cups of Stardust Electric Citrus. And please—remember to return your cast-aluminum speaker to the post before driving out!"),
        ],
    ),
    (
        "world_20_subterranean_elevator_shift_change",
        "elevator",
        "ORION TOWER FREIGHT LIFT #4 // SHIFT CHANGE",
        "Descending to Sublevel B2. Graveyard-shift tape librarians must clip magnetic dosimeter badges to their collars before exiting.",
        "SUBLEVEL B2 NIGHT SHIFT -> stardust-archive.net/start",
        [
            ("Victoria", 162, "pa", 0.35, "Freight Elevator Four descending. Passing Concourse... Basement One... arriving Sublevel B2 Acoustic Archives."),
            ("Daniel", 164, "pa", 0.25, "Graveyard-shift tape librarians and cooling-plant technicians are reminded to clip their magnetic flux dosimeters to their outer lapels and deposit all personal Walkman players in Locker Bay C before entering the main corridor."),
        ],
    ),
]


def main() -> None:
    assert len(WORLDBUILDING_SPEC) == 20, f"Expected 20 specs, got {len(WORLDBUILDING_SPEC)}"
    durations = {}
    if DURATIONS_PATH.exists():
        durations = json.loads(DURATIONS_PATH.read_text())

    new_world_bulletins = {}

    with tempfile.TemporaryDirectory() as tmp_str:
        tmp_dir = Path(tmp_str)
        for idx, (stem, scene_type, station, transcript, clue, turns) in enumerate(WORLDBUILDING_SPEC, 1):
            mp3_name = f"{stem}.mp3"
            out_mp3 = OUT_DIR / mp3_name
            new_world_bulletins[stem] = (station, transcript, clue)

            segments = []
            segments.append(np.zeros((int(1.10 * SR), 2), dtype=np.float32))

            for t_i, (voice, rate, eq_mode, pause_after, text) in enumerate(turns):
                wav_p = render_turn_wav(voice, rate, text, eq_mode, tmp_dir, idx * 10 + t_i)
                seg_arr = read_stereo_wav(wav_p)
                segments.append(seg_arr)
                if pause_after > 0:
                    segments.append(np.zeros((int(pause_after * SR), 2), dtype=np.float32))

            segments.append(np.zeros((int(1.35 * SR), 2), dtype=np.float32))
            voice_track = np.vstack(segments)

            bed = synth_world_soundscape(scene_type, voice_track.shape[0], seed=198800 + idx)
            mixed = np.clip(voice_track * 0.92 + bed, -0.98, 0.98)

            mixed_wav = tmp_dir / f"{stem}_mixed.wav"
            write_stereo_wav(mixed_wav, mixed)

            af_master = (
                "highpass=f=130,lowpass=f=4400,"
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

            probe = subprocess.run(
                [
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3),
                ],
                capture_output=True, text=True, check=True,
            )
            dur = round(float(probe.stdout.strip()), 3)
            durations[mp3_name] = dur
            print(f"[{idx:02d}/20] Rendered {mp3_name} ({scene_type}, {dur:.1f}s)")

    DURATIONS_PATH.write_text(json.dumps(durations, indent=2, sort_keys=True))
    Path("/tmp/new_20_world_bulletins.json").write_text(json.dumps(new_world_bulletins, indent=2))
    print(f"All 20 pure world-building English interstitials generated and saved to {OUT_DIR}!")


if __name__ == "__main__":
    main()
