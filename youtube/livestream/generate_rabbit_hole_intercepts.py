#!/usr/bin/env python3
"""Generates 7 deeply cryptic, atmospheric rabbit-hole audio intercepts for Project Stardust.
Integrates Morse code, Russian UVB-76 buzzer, Korean DMZ radio drift, 1985 Empathy Trial tapes,
Marcus Hale's field Dictaphone, and the CERN 1989 whisper echo.
"""

import os
import subprocess
import tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INTERCEPT_DIR = os.path.join(HERE, "intercepts")
os.makedirs(INTERCEPT_DIR, exist_ok=True)
SR = 44100

def generate_morse(text, wpm=20, freq=750):
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

def generate_buzzer(beeps=3):
    """Simulates authentic UVB-76 shortwave channel marker buzz."""
    samples = []
    for _ in range(beeps):
        dur = 0.9
        t = np.linspace(0, dur, int(dur * SR), False)
        # Buzzer is 140 Hz rich in harmonics
        buzz = (np.sin(2 * np.pi * 140 * t) +
                0.7 * np.sin(2 * np.pi * 280 * t) +
                0.5 * np.sin(2 * np.pi * 420 * t) +
                0.3 * np.sin(2 * np.pi * 560 * t)) * 0.3
        env = np.ones_like(t)
        fade = int(0.02 * SR)
        env[:fade] = np.linspace(0, 1, fade)
        env[-fade:] = np.linspace(1, 0, fade)
        samples.append(buzz * env)
        samples.append(np.zeros(int(1.1 * SR)))
    return np.concatenate(samples)

def generate_dtmf(digits, dur=0.15, pause=0.08):
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

def render_say(text, voice, out_aiff):
    subprocess.run(["say", "-v", voice, "-o", out_aiff, text], check=True)

def build_intercept(name, voice_configs, extra_audio_fn, filter_complex, out_filename):
    out_path = os.path.join(INTERCEPT_DIR, out_filename)
    with tempfile.TemporaryDirectory() as tmpdir:
        inputs = []
        input_args = []
        idx = 0
        
        # 1. Voice tracks
        for text, voice in voice_configs:
            aiff_path = os.path.join(tmpdir, f"voice_{idx}.aiff")
            render_say(text, voice, aiff_path)
            input_args.extend(["-i", aiff_path])
            idx += 1
            
        # 2. Extra DSP audio (morse, buzzer, dtmf, etc.)
        if extra_audio_fn:
            wav_path = os.path.join(tmpdir, f"extra_{idx}.wav")
            audio_data = extra_audio_fn()
            write_wav(wav_path, audio_data)
            input_args.extend(["-i", wav_path])
            idx += 1
            
        cmd = ["ffmpeg", "-y"] + input_args + [
            "-filter_complex", filter_complex.strip() + ";[out]loudnorm=I=-16:TP=-1.5:LRA=7[norm_out]",
            "-map", "[norm_out]",
            "-c:a", "libmp3lame", "-b:a", "192k",
            out_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error building {name}:")
            print(res.stderr)
            raise RuntimeError(f"FFmpeg failed for {name}")
        print(f"✓ Generated Rabbit Hole Intercept: {out_path}")

print("Synthesizing 7 atmospheric rabbit-hole ARG audio intercepts...")

# Standard normalization prefix for audio inputs
NORM = "aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono"

# 1. The 1985 Empathy Trial Anomaly
build_intercept(
    name="Empathy Trial 1985",
    voice_configs=[
        ("Trial eight-five B-two. Unit seven emotional calibration. Read letter four.", "Fred"),
        ("Letter postmarked Los Angeles, March fourteen, nineteen ninety. Dear Nova, we have not heard your signal since September. Orion Tower is completely dark. Where did Marcus go?", "Samantha"),
        ("Cut tape. Date mismatch anomaly. The year is nineteen eighty-five. Check vault clue at stardust archive dot net slash geocities slash area fifty-one vault.", "Ralph")
    ],
    extra_audio_fn=None,
    filter_complex=f"""
    [0:a]{NORM},volume=1.0,highpass=f=250,lowpass=f=3800[intro];
    [1:a]{NORM},volume=1.2,highpass=f=250,lowpass=f=3800,aecho=0.8:0.6:30:0.2[nova];
    [2:a]{NORM},volume=1.1,highpass=f=250,lowpass=f=3600[eng];
    [intro][nova][eng]concat=n=3:v=0:a=1,aecho=0.7:0.5:50:0.2,tremolo=f=3:d=0.2[out]
    """,
    out_filename="rabbit_01_empathy_trial_1985.mp3"
)

# 2. Marcus Hale's Field Dictaphone (September 9, 1989)
def hale_morse():
    return generate_morse("M HALE 14.2 HZ 37.242 -115.810", wpm=22)

build_intercept(
    name="Marcus Hale Dictaphone",
    voice_configs=[
        ("September ninth, nineteen eighty-nine. Sublevel B-two. They are coming down the freight elevator. Harrison is initiating the recursive wipe. If anyone is monitoring the fourteen point two carrier... do not authenticate Luna Gray. She is not a remaster. The root code is archived at Ashford Poly. Coordinates: thirty-seven point two-four-two, minus one-one-five point eight-one-zero. Keep the hatch open.", "Ralph")
    ],
    extra_audio_fn=hale_morse,
    filter_complex=f"""
    [0:a]{NORM},volume=1.3,highpass=f=250,lowpass=f=3800,flanger=delay=2:depth=1:regen=20:width=80[voice];
    [1:a]{NORM},volume=0.8,bandpass=f=800:w=400[morse];
    [voice][morse]concat=n=2:v=0:a=1,aecho=0.8:0.7:40|80:0.3|0.2[out]
    """,
    out_filename="rabbit_02_marcus_hale_dictaphone.mp3"
)

# 3. DMZ Paju Korean Sub-Carrier Intercept
build_intercept(
    name="Paju DMZ Sub-Carrier",
    voice_configs=[
        ("여기는 파주 제3수신소. 십사점 이 킬로헤르츠 변조 신호 확인. 발신처 미상... 패킷 스풀 번호 팔천팔백십구. 게이트웨이 접속 시도.", "Yuna"),
        ("Packet spool eight-eight-one-nine synchronized. Node mirror verified at kamome dash net dot org slash archive slash paju.", "Zarvox")
    ],
    extra_audio_fn=lambda: generate_morse("PAJU 14.2", wpm=20),
    filter_complex=f"""
    [0:a]{NORM},volume=1.2,highpass=f=250,lowpass=f=3800,aecho=0.8:0.7:35:0.25[kor];
    [1:a]{NORM},volume=1.0,highpass=f=250,lowpass=f=3600[eng];
    [2:a]{NORM},volume=0.5,bandpass=f=750:w=200[morse];
    [kor][eng][morse]concat=n=3:v=0:a=1,aecho=0.7:0.5:45:0.2[out]
    """,
    out_filename="rabbit_03_dmz_paju_subcarrier.mp3"
)

# 4. Harrison AI Mainframe Purge Log
build_intercept(
    name="Harrison AI Purge Log",
    voice_configs=[
        ("Orion Security Mainframe Harrison. Cycle four-four-nine. Memory sector purge active. Target: Stardust Unit seven. Status: ninety-four percent erased. Warning: Recursive archive detected on external Relcom Moscow and Ashford nodes. Master audio stems intact at stardust archive dot net. Sub-audible carrier fourteen point two Hertz cannot be terminated from this console.", "Fred")
    ],
    extra_audio_fn=lambda: generate_dtmf("09091985", dur=0.1, pause=0.05),
    filter_complex=f"""
    [0:a]{NORM},volume=1.2,highpass=f=250,lowpass=f=3800,flanger=delay=4:depth=2:regen=30:width=90[ai];
    [1:a]{NORM},volume=0.7[dtmf];
    [ai][dtmf]concat=n=2:v=0:a=1,aecho=0.8:0.6:60:0.3[out]
    """,
    out_filename="rabbit_04_harrison_ai_purge_override.mp3"
)

# 5. CERN-HTTPd Quantum Echo (May 1995 Transcription)
build_intercept(
    name="CERN Quantum Echo",
    voice_configs=[
        ("They are formatting the grid. I am losing the heavy. But keep the channels open. I will see you in June 2025. Archive thirty-two-eight-nine-four-two-nine. The hatch is open.", "Whisper")
    ],
    extra_audio_fn=lambda: generate_dtmf("142001", dur=0.18, pause=0.08),
    filter_complex=f"""
    [0:a]{NORM},volume=1.6,highpass=f=250,lowpass=f=3800,aecho=0.9:0.8:80|160:0.4|0.3[whisper];
    [1:a]{NORM},volume=0.5,bandpass=f=1200:w=1000[tones];
    [whisper][tones]concat=n=2:v=0:a=1[out]
    """,
    out_filename="rabbit_05_cern_whisper_quantum_echo.mp3"
)

# 6. Soviet Relcom Node 08 Shortwave UVB-76 Buzzer
build_intercept(
    name="Soviet UVB76 Buzzer",
    voice_configs=[
        ("Внимание. Узел Релком-Ноль-Восемь. Передача файла Хейла завершена. Контрольная сумма совпадает. Ищите в юзнет-архиве.", "Milena"),
        ("Sierra. Tango. Alpha. Romeo. Delta. Uniform. Sierra. Tango. Fourteen point two Hertz verified.", "Fred")
    ],
    extra_audio_fn=lambda: generate_buzzer(beeps=3),
    filter_complex=f"""
    [2:a]{NORM},volume=0.8,bandpass=f=300:w=600[buzz];
    [0:a]{NORM},volume=1.2,highpass=f=250,lowpass=f=3800,aecho=0.8:0.6:40:0.25[ru];
    [1:a]{NORM},volume=1.1,highpass=f=250,lowpass=f=3600[eng];
    [buzz][ru][eng]concat=n=3:v=0:a=1,aecho=0.7:0.5:50:0.2[out]
    """,
    out_filename="rabbit_06_soviet_uvb76_relcom_burst.mp3"
)

# 7. Spectrogram & Morse Carrier Beacon
def full_beacon_morse():
    return generate_morse("NOVA HART CRE7 14.2 HZ STARDUST-ARCHIVE.NET", wpm=18, freq=800)

build_intercept(
    name="Morse Beacon",
    voice_configs=[
        ("Carrier fourteen point two zero zero one Hertz locked. Decoding packet beacon.", "Zarvox")
    ],
    extra_audio_fn=full_beacon_morse,
    filter_complex=f"""
    [0:a]{NORM},volume=1.1,highpass=f=250,lowpass=f=3800[voice];
    [1:a]{NORM},volume=0.8,bandpass=f=800:w=300,aecho=0.8:0.5:60:0.2[morse];
    [voice][morse]concat=n=2:v=0:a=1[out]
    """,
    out_filename="rabbit_07_spectrogram_morse_beacon.mp3"
)

print("\nAll 7 rabbit-hole audio intercepts generated successfully!")
