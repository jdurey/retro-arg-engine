#!/usr/bin/env python3
"""Generates punchy, authentic 4-to-6 second Morse Code radio telemetry bursts.
Replaces the 34-second near-silent files with crisp, audible shortwave CW signals.
"""

import os
import wave
import subprocess
import tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MORSE_DIR = os.path.join(HERE, "broadcast_archive", "morse_beacons")
os.makedirs(MORSE_DIR, exist_ok=True)

SR = 44100

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': ' '
}

SHORT_MESSAGES = [
    "STARDUST 14.2",
    "ORION B2",
    "UNIT 7",
    "SERIES NH",
    "LUNA GRAY",
    "CARRIER LOCK",
    "AKASAKA 85",
    "HALE 1989",
    "REEL 09",
    "FREQ 1420",
    "ASHFORD PUB",
    "SIGNAL PERSISTS",
]

def generate_cw_burst(text, freq=750, wpm=22):
    dot_dur = 1.2 / wpm
    dash_dur = dot_dur * 3.0
    samples = []

    for char in text.upper():
        if char == ' ':
            samples.append(np.zeros(int(dot_dur * 3 * SR)))
            continue
        code = MORSE_CODE.get(char, '')
        for elem in code:
            dur = dot_dur if elem == '.' else dash_dur
            n = int(dur * SR)
            t = np.linspace(0, dur, n, False)
            # Soft envelope to prevent clicking
            env = np.sin(np.pi * np.linspace(0, 1, n)) ** 0.4
            tone = np.sin(2 * np.pi * freq * t) * env * 0.7
            samples.append(tone)
            samples.append(np.zeros(int(dot_dur * SR)))
        samples.append(np.zeros(int(dot_dur * 2 * SR)))

    # Add a short fade-out room static
    total_audio = np.concatenate(samples)
    noise = np.random.normal(0, 0.015, len(total_audio))
    return (total_audio + noise).astype(np.float32)

def main():
    print("Generating 35 crisp, 4-6s Morse Code telemetry beacons...")
    for i in range(1, 36):
        out_path = os.path.join(MORSE_DIR, f"morse_beacon_{i:03d}.mp3")
        msg = SHORT_MESSAGES[(i - 1) % len(SHORT_MESSAGES)]
        freq = 700 + (i * 25) % 300
        audio = generate_cw_burst(msg, freq=freq, wpm=22)

        # Soft limiter
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = audio / peak * 0.85
        int_data = (audio * 32767).astype(np.int16)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            wav_path = tmp_wav.name

        with wave.open(wav_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SR)
            wf.writeframes(int_data.tobytes())

        # Encode to MP3 with tight trim
        cmd = [
            "ffmpeg", "-y", "-i", wav_path,
            "-af", "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-30dB:detection=peak,areverse,silenceremove=start_periods=1:start_duration=0.05:start_threshold=-30dB:detection=peak,areverse",
            "-c:a", "libmp3lame", "-b:a", "192k",
            out_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(wav_path)

        cmd_info = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_path]
        dur = float(subprocess.check_output(cmd_info).decode().strip())
        print(f"  ✓ {os.path.basename(out_path)}: {dur:.2f}s - '{msg}' ({freq} Hz)")

    print("All 35 morse beacons regenerated as tight, crisp telemetry bursts!")

if __name__ == "__main__":
    main()
