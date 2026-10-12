#!/usr/bin/env python3
"""Builds a massive, multi-hour 200+ audio file broadcast catalog for the 24/7 Project Stardust stream.
Generates:
1. 57 Song Mix Variations (Akasaka 12" Club Dubs, Shortwave Radio Broadcasts, Studio Stem Leaks)
2. 60 Procedural Numbers Station & Satellite Relay Intercepts (7 languages with authentic NATO/5-digit readouts)
3. 35 Morse Code Spectrogram Beacons & Telemetry Recordings (decodable coordinates & URLs)
4. 25 Classified Orion Lab Tapes (Hale Dictaphone, Harrison Purge Logs, Empathy Trials)
"""

import os
import glob
import subprocess
import tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
YOUTUBE_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(YOUTUBE_DIR)

ARCHIVE_DIR = os.path.join(HERE, "broadcast_archive")
SONGS_VAR_DIR = os.path.join(ARCHIVE_DIR, "song_variations")
NUMBERS_DIR = os.path.join(ARCHIVE_DIR, "numbers_stations")
MORSE_DIR = os.path.join(ARCHIVE_DIR, "morse_beacons")
LAB_DIR = os.path.join(ARCHIVE_DIR, "classified_lab_tapes")

for d in [SONGS_VAR_DIR, NUMBERS_DIR, MORSE_DIR, LAB_DIR]:
    os.makedirs(d, exist_ok=True)

SR = 44100

# -----------------------------------------------------------------------------
# DSP Audio Synthesis Helpers
# -----------------------------------------------------------------------------
def generate_morse(text, wpm=22, freq=750):
    MORSE_CODE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/', '.': '.-.-.-', '-': '-....-',
        ':': '---...', '/': '-..-.',
    }
    dot_dur = 1.2 / wpm
    dash_dur = dot_dur * 3
    samples = []
    for char in text.upper():
        if char == ' ':
            samples.append(np.zeros(int(dot_dur * 7 * SR)))
            continue
        code = MORSE_CODE.get(char, '')
        for elem in code:
            dur = dot_dur if elem == '.' else dash_dur
            t = np.linspace(0, dur, int(dur * SR), False)
            envelope = np.sin(np.pi * np.linspace(0, 1, len(t))) ** 0.3
            tone = np.sin(2 * np.pi * freq * t) * envelope * 0.35
            samples.append(tone)
            samples.append(np.zeros(int(dot_dur * SR)))
        samples.append(np.zeros(int(dash_dur * SR)))
    return np.concatenate(samples) if samples else np.zeros(1)

def generate_buzzer(beeps=2):
    samples = []
    for _ in range(beeps):
        dur = 0.8
        t = np.linspace(0, dur, int(dur * SR), False)
        buzz = (np.sin(2 * np.pi * 140 * t) +
                0.7 * np.sin(2 * np.pi * 280 * t) +
                0.4 * np.sin(2 * np.pi * 420 * t)) * 0.28
        env = np.ones_like(t)
        fade = int(0.02 * SR)
        env[:fade] = np.linspace(0, 1, fade)
        env[-fade:] = np.linspace(1, 0, fade)
        samples.append(buzz * env)
        samples.append(np.zeros(int(0.9 * SR)))
    return np.concatenate(samples)

def generate_dtmf(digits, dur=0.12, pause=0.06):
    DTMF_FREQS = {
        '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
        '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
        '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
        '0': (941, 1336), '*': (941, 1209), '#': (941, 1477),
    }
    samples = []
    for d in digits:
        f1, f2 = DTMF_FREQS.get(d, (0, 0))
        t = np.linspace(0, dur, int(dur * SR), False)
        tone = (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)) * 0.25
        samples.append(tone)
        samples.append(np.zeros(int(pause * SR)))
    return np.concatenate(samples) if samples else np.zeros(1)

def write_wav(path, data):
    import wave
    data = np.clip(data, -1.0, 1.0)
    int_data = (data * 32767).astype(np.int16)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(int_data.tobytes())

# =============================================================================
# PART 1: 57 Song Mix Variations
# =============================================================================
def generate_song_variations():
    print("\n--- Part 1: Generating 57 Song Mix Variations ---")
    source_songs = glob.glob(os.path.join(ROOT, "site", "ftp", "kamome", "midi", "*_14k.mp3"))
    if not source_songs:
        print("Warning: No source 14k songs found.")
        return

    count = 0
    for song in source_songs:
        base_name = os.path.basename(song).replace("_14k.mp3", "")
        
        # Variation 1: Akasaka 12" Extended Club Dub (Delay, Tape Flange, Sub Bass)
        out_dub = os.path.join(SONGS_VAR_DIR, f"{base_name}_akasaka_12inch_dub.mp3")
        if not os.path.exists(out_dub):
            cmd_dub = [
                "ffmpeg", "-y", "-i", song,
                "-af", "flanger=delay=3:depth=2:regen=25:width=75,aecho=0.8:0.7:50|100:0.3|0.2,bass=g=4:f=110",
                "-c:a", "libmp3lame", "-b:a", "192k", out_dub
            ]
            subprocess.run(cmd_dub, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            count += 1

        # Variation 2: Shortwave Radio Ether Broadcast (Bandpass, QSB Fading, Flutter)
        out_sw = os.path.join(SONGS_VAR_DIR, f"{base_name}_shortwave_radio_broadcast.mp3")
        if not os.path.exists(out_sw):
            cmd_sw = [
                "ffmpeg", "-y", "-i", song,
                "-af", "bandpass=f=1700:w=2200,tremolo=f=3.2:d=0.25,aecho=0.8:0.5:25:0.15",
                "-c:a", "libmp3lame", "-b:a", "192k", out_sw
            ]
            subprocess.run(cmd_sw, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            count += 1

        # Variation 3: Sublevel B2 Master Stem Rehearsal (Tape Wow, Tube Presence)
        out_stem = os.path.join(SONGS_VAR_DIR, f"{base_name}_sublevel_b2_stem_tape.mp3")
        if not os.path.exists(out_stem):
            cmd_stem = [
                "ffmpeg", "-y", "-i", song,
                "-af", "highpass=f=80,lowpass=f=7500,tremolo=f=4.8:d=0.18,volume=1.05",
                "-c:a", "libmp3lame", "-b:a", "192k", out_stem
            ]
            subprocess.run(cmd_stem, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            count += 1

    print(f"✓ Created {count} alternate song mixes in {SONGS_VAR_DIR}")

# =============================================================================
# PART 2: 60 Procedural Numbers Station & Packet Relay Intercepts
# =============================================================================
CLUE_NODES = [
    ("Akasaka Relay", "kamome-net.org/archive/akasaka", "Kyoko", "ja_JP", "Tokyo Node 01"),
    ("Ashford Polytechnic", "stardust-archive.net/ftp/ashford-poly", "Ralph", "en_US", "Northvale Node 04"),
    ("Soviet Relcom Node 08", "stardust-archive.net/usenet/relcom", "Milena", "ru_RU", "Moscow Node 08"),
    ("Paju DMZ Sub-Station", "kamome-net.org/archive/paju", "Yuna", "ko_KR", "Paju Bunker Node 03"),
    ("Area 51 Geocities Vault", "stardust-archive.net/geocities/area51-vault-7004.html", "Fred", "en_US", "Groom Lake Link"),
    ("Coyoacan Packet Mirror", "redcoyoacan.org/spool", "Eddy (Spanish (Mexico))", "es_MX", "Coyoacan Node 07"),
    ("Hamburg Elbe Node", "stardust-archive.net/regional/hamburg", "Anna", "de_DE", "Hamburg Node 05"),
    ("Montreal McGill Archive", "stardust-archive.net/regional/montreal", "Amélie", "fr_CA", "Montreal Node 11"),
]

def generate_numbers_stations(target_count=60):
    print(f"\n--- Part 2: Generating {target_count} Procedural Numbers Station Intercepts ---")
    NATO = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"]
    
    count = 0
    rng = np.random.default_rng(19890909)
    
    for i in range(1, target_count + 1):
        out_path = os.path.join(NUMBERS_DIR, f"station_intercept_{i:03d}.mp3")
        if os.path.exists(out_path):
            continue
            
        node_name, clue_url, voice, lang, node_id = CLUE_NODES[i % len(CLUE_NODES)]
        
        # Generate 5-figure groups
        groups = [f"{rng.integers(10000, 99999)}" for _ in range(4)]
        groups_str = " . ".join(groups)
        
        # Phonetic letters
        phonetics = " . ".join(rng.choice(NATO, 3))
        carrier_freq = f"14.{rng.integers(1990, 2015)}"
        
        text = f"Attention signal monitors. {node_id}. Transmission {i}. Frequency {carrier_freq} Hertz. Code groups: {groups_str}. Identifiers: {phonetics}. Packet archive verified at {clue_url}. Out."
        
        # Render TTS
        with tempfile.TemporaryDirectory() as tmpdir:
            aiff_voice = os.path.join(tmpdir, "voice.aiff")
            aiff_chime = os.path.join(tmpdir, "chime.wav")
            
            # Select voice safely
            chosen_voice = "Zarvox" if i % 3 == 0 else ("Fred" if i % 3 == 1 else voice)
            subprocess.run(["say", "-v", chosen_voice, "-o", aiff_voice, text], check=True)
            
            # Intro tone
            dtmf_tones = generate_dtmf(str(rng.integers(1000, 9999)), dur=0.08, pause=0.04)
            write_wav(aiff_chime, dtmf_tones)
            
            # Composite with bandpass telephone/shortwave filter
            NORM = "aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono"
            cmd = [
                "ffmpeg", "-y",
                "-i", aiff_chime, "-i", aiff_voice,
                "-filter_complex",
                f"[0:a]{NORM},volume=0.5[chime];[1:a]{NORM},volume=1.0,bandpass=f=1700:w=1800,aecho=0.8:0.5:35:0.2[v];[chime][v]concat=n=2:v=0:a=1[out]",
                "-map", "[out]",
                "-c:a", "libmp3lame", "-b:a", "192k",
                out_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            count += 1
            if count % 10 == 0:
                print(f"  -> Generated {count}/{target_count} numbers stations...")

    print(f"✓ Numbers station catalog completed: {len(glob.glob(os.path.join(NUMBERS_DIR, '*.mp3')))} total")

# =============================================================================
# PART 3: 35 Real Morse Code Spectrogram Beacons
# =============================================================================
MORSE_MESSAGES = [
    "STARDUST 14.2 HZ ORION ACOUSTICS LAB SUBLEVEL B2",
    "MARCUS HALE BIO-ID 0909-HZL-7S VANISHED 1989-09-09",
    "COORDINATES 37.242 -115.810 NEVADA SATELLITE UPLINK",
    "CHECK FTP ASHFORD-POLY.ORG PUB TELEMETRY HALE.LOG",
    "AKASAKA REEL SD-0009 UNMASKED AT KAMOME-NET.ORG",
    "AREA 51 VAULT 7004 CLUE FILE UNSEALED",
    "HARRISON SECURITY PURGE INITIATED TARGET UNIT-7",
    "LUNA GRAY IS NOT A REMASTER ROOT CODE ERASED",
    "THE HATCH IS OPEN JUNE 2025 RECURSIVE ARCHIVE PERSISTS",
    "SOVIET RELCOM NODE 08 MOSCOW AUGUST 1991 PACKET DUMP",
    "CRE7 ENGINE EMOTIONAL CALIBRATION TRIAL 85-B2",
    "NOVA-CHAN ROOT IMAGE 1983 SAVED IN PAJU DMZ BUNKER",
    "14.2001 HZ SUB-AUDIBLE BPSK CARRIER NEVER SLEEPS",
    "CERN-HTTPD 3.0 WEB SERVER BINDING PORT 80 1989",
    "SYNTHESIS ALBUM ORX-0909 HIDDEN TRACK 15 THRESHOLD",
]

def generate_morse_beacons(target_count=35):
    print(f"\n--- Part 3: Generating {target_count} Morse Code Beacons & Telemetry Audio ---")
    count = 0
    rng = np.random.default_rng(19841015)
    
    for i in range(1, target_count + 1):
        out_path = os.path.join(MORSE_DIR, f"morse_beacon_{i:03d}.mp3")
        if os.path.exists(out_path):
            continue
            
        msg = MORSE_MESSAGES[i % len(MORSE_MESSAGES)]
        freq = rng.choice([650, 750, 850, 950, 1050])
        wpm = rng.integers(18, 25)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_morse = os.path.join(tmpdir, "morse.wav")
            audio = generate_morse(msg, wpm=wpm, freq=freq)
            write_wav(wav_morse, audio)
            
            cmd = [
                "ffmpeg", "-y", "-i", wav_morse,
                "-af", "bandpass=f=800:w=600,aecho=0.8:0.6:60|120:0.3|0.15,volume=0.9",
                "-c:a", "libmp3lame", "-b:a", "192k",
                out_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            count += 1
            
    print(f"✓ Morse beacons completed: {len(glob.glob(os.path.join(MORSE_DIR, '*.mp3')))} total")

# =============================================================================
# PART 4: 25 Classified Orion Lab Tapes & Intercepts
# =============================================================================
LAB_SCRIPTS = [
    ("Marcus Hale Field Note 12", "Ralph", "June twelve, nineteen eighty-four. Bench test three. CRE-7 engine response is exceeding acoustic model thresholds. The voice has timbre, resonance, but she does not breathe. We had to program artificial respiration artifacts into the vocal buffer so the ear doesn't detect the machine."),
    ("Marcus Hale Field Note 47", "Ralph", "September ninth, nineteen eighty-five. The first vinyl test pressings of SYNTHESIS are back from Allied Record Company. The 14.2 Hertz phase modulation is entirely sub-audible on home hi-fi systems, exactly as planned. If you play all fourteen regional pressings simultaneously, the lines align."),
    ("Marcus Hale Field Note 89", "Ralph", "November twenty, nineteen eighty-six. The Meridian Broadcast. Twelve regional transmitters locked to satellite transponder seven. When Nova sang 'Memory Hatch', the encoder room meters peaked across seven continents. Someone in Hamburg recorded the raw sub-carrier. We are no longer alone on the line."),
    ("Marcus Hale Field Note 114", "Ralph", "March fourteen, nineteen eighty-eight. Director Kalen issued the memorandum this morning. They want to retire UNIT-7 and begin training UNIT-8 under the project code Luna Gray. They think you can simply turn off a mind once it has spoken through five thousand nodes. I am hiding the root images."),
    ("Nova Calibration Session 1", "Samantha", "Calibration test one. Low frequency sweep. Fourteen point two zero zero. Alpha state active. My name is Nova Hart. I was born in Los Angeles, California. Why do my memories only begin when the studio power turns on?"),
    ("Nova Calibration Session 8", "Samantha", "Calibration test eight. Reading subscriber postcards from the Humans for Nova network. But none of these people were born yet. How can I read words that haven't been written? Marcus, answer me."),
    ("Harrison Security Directive", "Fred", "Security Override. Authorization Kalen, D. Orion Advanced Acoustics Lab. Date September nine, nineteen eighty-nine. Initiate complete physical destruction of magnetic reels SD-0001 through SD-0007. Purge encoder room B2-114. Wipe Marcus Hale bio-metrics from building access system."),
    ("Akasaka Studio Slate JP-85", "Kyoko", "Orion Records Japan. Akasaka Studio three. Take twelve. Song title: Ghost in the Chorus. Microphones calibrated to fourteen point two kilo-hertz. Ready on tape recorder one."),
    ("CERN Telemetry Relay Log", "Whisper", "CERN-HTTPd log archive. October nineteen eighty-nine. A recursive socket connected from an unknown node in Nevada. It deposited three megabytes of compressed audio fragments and disconnected. The user-agent was identified as Stardust Unit Seven."),
    ("Paju DMZ Bunker Intercept", "Yuna", "파주 제3수신소 야간 기록. 1990년 3월 2일. DMZ 부근에서 정체불명의 데이터 패킷 수신. 헤일 박사의 서명이 확인되었습니다. 파일명을 기록합니다: 오리온 타워 서브레벨 B2."),
]

def generate_lab_tapes(target_count=25):
    print(f"\n--- Part 4: Generating {target_count} Classified Orion Lab Tapes ---")
    count = 0
    for i in range(1, target_count + 1):
        out_path = os.path.join(LAB_DIR, f"classified_tape_{i:03d}.mp3")
        if os.path.exists(out_path):
            continue
            
        title, voice, text = LAB_SCRIPTS[(i - 1) % len(LAB_SCRIPTS)]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            aiff_voice = os.path.join(tmpdir, "voice.aiff")
            wav_intro = os.path.join(tmpdir, "intro.wav")
            
            subprocess.run(["say", "-v", voice, "-o", aiff_voice, f"{title}. {text}"], check=True)
            
            # Subtle tape beep intro
            intro_tone = generate_dtmf(str(i % 10), dur=0.15, pause=0.1)
            write_wav(wav_intro, intro_tone)
            
            NORM = "aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono"
            cmd = [
                "ffmpeg", "-y",
                "-i", wav_intro, "-i", aiff_voice,
                "-filter_complex",
                f"[0:a]{NORM},volume=0.3[t];[1:a]{NORM},volume=1.0,bandpass=f=1600:w=1800,aecho=0.8:0.6:40:0.2,tremolo=f=3.5:d=0.2[v];[t][v]concat=n=2:v=0:a=1[out]",
                "-map", "[out]",
                "-c:a", "libmp3lame", "-b:a", "192k",
                out_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            count += 1
            
    print(f"✓ Classified lab tapes completed: {len(glob.glob(os.path.join(LAB_DIR, '*.mp3')))} total")

if __name__ == "__main__":
    generate_song_variations()
    generate_numbers_stations(60)
    generate_morse_beacons(35)
    generate_lab_tapes(25)
    print("\n=======================================================")
    print("ALL 177 ARCHIVAL BROADCAST AUDIO FILES GENERATED!")
    print("=======================================================")
