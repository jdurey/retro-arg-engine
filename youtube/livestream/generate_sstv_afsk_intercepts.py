#!/usr/bin/env python3
"""
Project Stardust — Deep Audio Forensics & Steganographic Intercept Synthesizer
Generates three broadcast-ready EBU R128 (-16 LUFS, 44.1 kHz stereo 192k MP3)
steganographic intercepts with zero dead air:
  1. rabbit_08_sstv_b2_schematic.mp3
     - Robot36-inspired VIS header (1900Hz / 1200Hz / 1300Hz) + scanline frequency
       modulation (1500-2300 Hz) encoding the Sublevel B2-114 Vault & Nevada Uplink schematic.
  2. rabbit_09_bell103_relcom_packet.mp3
     - Bell 103 300-baud AFSK data burst (1270 Hz mark / 1070 Hz space) carrying
       the Relcom Node-08 / Ashford-Kamome cross-domain decryption frame over a
       14.2001 Hz phase-locked sub-carrier hum.
  3. rabbit_10_phase_inverted_hart_stem.mp3
     - Phase-inverted differential telemetry stem (L/R 180-degree phase offset on
       carrier harmonics with 14.2 Hz AM envelope) designed to cancel out carrier noise
       and reveal clean hidden Morse ("ASHFORD-KAMOME-1420") when summed in Mono (L+R)
       inside the Forensic Signal Laboratory.
"""

from __future__ import annotations
import math
import os
import struct
import subprocess
import tempfile
import wave
from pathlib import Path

SAMPLE_RATE = 44100

MORSE_TABLE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    "-": "-....-", "/": "-..-.", " ": " ",
}


def clamp_i16(val: float) -> int:
    return max(-32767, min(32767, int(val * 32767.0)))


def write_stereo_wav(path: Path, left: list[float], right: list[float]) -> None:
    n = min(len(left), len(right))
    buf = bytearray(n * 4)
    for i in range(n):
        struct.pack_into("<hh", buf, i * 4, clamp_i16(left[i]), clamp_i16(right[i]))
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(buf)


def lcg_noise(seed: int) -> float:
    seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
    return seed, ((seed / 1073741824.0) - 1.0)


def encode_morse_envelope(message: str, unit_sec: float = 0.055) -> list[float]:
    env: list[float] = []
    unit_samples = int(SAMPLE_RATE * unit_sec)
    ramp = max(1, int(SAMPLE_RATE * 0.004))

    def append_tone(units: int, active: bool) -> None:
        total = units * unit_samples
        for i in range(total):
            if not active:
                env.append(0.0)
            else:
                if i < ramp:
                    env.append(i / ramp)
                elif i > total - ramp:
                    env.append((total - i) / ramp)
                else:
                    env.append(1.0)

    for ch in message.upper():
        code = MORSE_TABLE.get(ch, "")
        if ch == " ":
            append_tone(4, False)
            continue
        for idx, sym in enumerate(code):
            append_tone(1 if sym == "." else 3, True)
            if idx < len(code) - 1:
                append_tone(1, False)
        append_tone(3, False)
    return env


def synth_sstv_b2_schematic(duration_sec: float = 16.0) -> tuple[list[float], list[float]]:
    """
    Synthesizes an authentic SSTV VIS header + 32 scanlines representing a 32x32
    luminance grid of the Sublevel B2-114 schematic & coordinates 37.242 -115.810,
    layered over analog shortwave bed so there is zero dead air.
    """
    total_samples = int(SAMPLE_RATE * duration_sec)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # 16x16 bitmap of "B2" + satellite dish icon (0.0..1.0 luminance)
    rows_ascii = [
        "################",
        "#..............#",
        "#.####...####..#",
        "#.#...#.#....#.#",
        "#.####......#..#",
        "#.#...#...##...#",
        "#.####...######.",
        "#..............#",
        "#..14.2001.HZ..#",
        "#...*......*...#",
        "#....*....*....#",
        "#.....****.....#",
        "#......**......#",
        "#....******....#",
        "#..............#",
        "################",
    ]

    # Build frequency timeline:
    # 0.0 - 0.9s: VIS Header (1900Hz leader, 1200Hz break, 1900Hz leader, 1200Hz start bit + Robot36 code)
    # 0.9 - 13.7s: 32 scanlines (each 0.4s: 0.03s 1200Hz hsync + 0.37s 1500..2300Hz luminance)
    # 13.7 - 16.0s: 750Hz Morse confirmation tail ("B2 SSTV END")
    morse_env = encode_morse_envelope("B2 SSTV 1420", unit_sec=0.045)
    phase = 0.0
    seed = 89114

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        seed, wn = lcg_noise(seed)

        # Warm shortwave carrier bed + 14.2001 Hz sub-carrier modulation (prevents dead air)
        sub_mod = 1.0 + 0.18 * math.sin(2.0 * math.pi * 14.2001 * t)
        bed = 0.045 * wn + 0.035 * math.sin(2.0 * math.pi * 440.0 * t) * sub_mod

        if t < 0.35:
            freq = 1900.0
        elif t < 0.40:
            freq = 1200.0
        elif t < 0.75:
            freq = 1900.0
        elif t < 0.90:
            bit_idx = int((t - 0.75) / 0.02)
            freq = 1100.0 if (bit_idx % 2 == 0) else 1300.0
        elif t < 13.70:
            line_t = t - 0.90
            line_idx = int(line_t / 0.40)
            in_line = line_t % 0.40
            if in_line < 0.035:
                freq = 1200.0  # Horizontal sync pulse
            else:
                px_norm = (in_line - 0.035) / 0.365
                row = rows_ascii[min(15, line_idx // 2)]
                col = min(15, int(px_norm * 16))
                ch = row[col]
                lum = 1.0 if ch == "#" else (0.75 if ch not in (".", " ") else 0.12)
                freq = 1500.0 + lum * 800.0
        else:
            freq = 750.0

        phase += (2.0 * math.pi * freq) / SAMPLE_RATE
        if t < 13.70:
            sig = 0.48 * math.sin(phase)
        else:
            m_idx = i - int(13.70 * SAMPLE_RATE)
            m_amp = morse_env[m_idx] if 0 <= m_idx < len(morse_env) else 0.35
            sig = (0.42 * m_amp + 0.08) * math.sin(phase)

        # Slight stereo ionospheric spread
        left[i] = sig + bed
        right[i] = sig * 0.96 + bed * 1.04 + 0.03 * math.cos(phase * 0.5)

    return left, right


def synth_bell103_relcom_packet(duration_sec: float = 15.0) -> tuple[list[float], list[float]]:
    """
    Synthesizes a Bell 103 300-baud AFSK packet (1270 Hz mark / 1070 Hz space)
    encoding: "RELCOM-08 // XOR:0x3A5F // KEY:ASHFORD-KAMOME-1420 // HALE-ALIVE-IN-MESH"
    followed by a Morse verification burst.
    """
    total_samples = int(SAMPLE_RATE * duration_sec)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    payload = b"*** RELCOM-NODE08 AX.25 FRAME // XOR-DYAD: 0x3A5F // SECTOR-5-KEY: ASHFORD-KAMOME-1420 ***\r\n"
    bits: list[int] = [1] * 60  # Carrier mark lead-in
    for b in payload:
        bits.append(0)  # Start bit
        for bit_pos in range(8):
            bits.append((b >> bit_pos) & 1)
        bits.append(1)  # Stop bit
        bits.append(1)
    bits.extend([1] * 45)

    baud = 110.0  # 110-baud teletype / early Relcom pace to fill ~10.5s cleanly
    samples_per_bit = SAMPLE_RATE / baud
    morse_env = encode_morse_envelope("ASHFORD KAMOME 1420", unit_sec=0.048)

    phase = 0.0
    seed = 199510

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        seed, wn = lcg_noise(seed)

        # UVB-76 style 14.2 Hz sub-carrier buzz bed
        buzz = 0.06 * math.sin(2.0 * math.pi * 110.0 * t) * (0.6 + 0.4 * math.sin(2.0 * math.pi * 14.2001 * t))
        hiss = 0.035 * wn

        bit_idx = int(i / samples_per_bit)
        if bit_idx < len(bits):
            bit = bits[bit_idx]
            freq = 1270.0 if bit == 1 else 1070.0
            phase += (2.0 * math.pi * freq) / SAMPLE_RATE
            sig = 0.46 * math.sin(phase)
        else:
            m_idx = (i - int(len(bits) * samples_per_bit)) % max(1, len(morse_env))
            m_amp = morse_env[m_idx]
            phase += (2.0 * math.pi * 750.0) / SAMPLE_RATE
            sig = (0.44 * m_amp + 0.09) * math.sin(phase)

        left[i] = sig + buzz + hiss
        right[i] = sig * 0.94 - buzz * 0.5 + hiss

    return left, right


def synth_phase_inverted_hart_stem(duration_sec: float = 15.0) -> tuple[list[float], list[float]]:
    """
    Synthesizes a phase-cancellation puzzle track:
      - A loud masking chord (440 Hz + 554.37 Hz + 659.25 Hz) is recorded 180 degrees
        OUT OF PHASE between Left and Right channels (L = +mask, R = -mask).
      - A secret 750 Hz Morse code transmission ("ASHFORD-KAMOME-1420") + warm synth
        pad is recorded IN PHASE (L = +secret, R = +secret).
      - When played in stereo, the masking chord dominates; when summed to Mono (L+R)
        or phase-inverted in the Forensic Signal Lab, the masking chord cancels out
        completely, revealing the clean secret transmission!
    """
    total_samples = int(SAMPLE_RATE * duration_sec)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    morse_env = encode_morse_envelope("SECTOR 5 KEY ASHFORD-KAMOME-1420", unit_sec=0.048)
    seed = 4127

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        seed, wn = lcg_noise(seed)

        # Out-of-phase masking carrier (cancels when L+R summed!)
        flutter = 1.0 + 0.003 * math.sin(2.0 * math.pi * 5.5 * t)
        mask = (
            0.34 * math.sin(2.0 * math.pi * 330.0 * flutter * t)
            + 0.24 * math.sin(2.0 * math.pi * 495.0 * flutter * t)
            + 0.16 * math.sin(2.0 * math.pi * 990.0 * flutter * t)
        )

        # In-phase secret Morse signal + 14.2001 Hz modulated sub-harmonic (survives L+R sum!)
        m_amp = morse_env[i % len(morse_env)]
        secret_morse = (0.28 * m_amp) * math.sin(2.0 * math.pi * 750.0 * t)
        secret_pad = 0.14 * math.sin(2.0 * math.pi * 220.0 * t) * (1.0 + 0.25 * math.sin(2.0 * math.pi * 14.2001 * t))
        tape_hiss = 0.025 * wn

        left[i] = secret_morse + secret_pad + mask + tape_hiss
        right[i] = secret_morse + secret_pad - mask + tape_hiss

    return left, right


def master_to_broadcast_mp3(wav_path: Path, mp3_path: Path) -> dict:
    """
    Masters WAV to Project Stardust broadcast specification:
    - Stereo 44.1 kHz 192 kbps MP3
    - Highpass 180 Hz, Lowpass 4800 Hz (shortwave/forensic tape profile)
    - EBU R128 loudness normalization: loudnorm=I=-16:TP=-1.5:LRA=7
    - Verified with silencedetect at -30 dB
    """
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    af_chain = "highpass=f=180,lowpass=f=4800,loudnorm=I=-16:TP=-1.5:LRA=7"
    cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-hide_banner",
        "-i", str(wav_path),
        "-af", af_chain,
        "-ar", "44100",
        "-ac", "2",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        str(mp3_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)

    # Verify zero silence gaps at -30 dB
    verify_cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-hide_banner",
        "-i", str(mp3_path),
        "-af", "silencedetect=n=-30dB:d=0.5,ebur128=peak=true",
        "-f", "null",
        "-",
    ]
    res = subprocess.run(verify_cmd, check=True, capture_output=True, text=True)
    stderr = res.stderr
    silence_hits = stderr.count("silence_start:")
    return {"mp3": str(mp3_path), "size_bytes": mp3_path.stat().st_size, "silence_gaps": silence_hits}


def main() -> None:
    out_dir = Path("/tmp/stardust_expansion/youtube/livestream/intercepts")
    assets_dir = Path("/tmp/stardust_expansion/site/assets/audio/forensics")
    out_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    specs = [
        ("rabbit_08_sstv_b2_schematic.mp3", synth_sstv_b2_schematic),
        ("rabbit_09_bell103_relcom_packet.mp3", synth_bell103_relcom_packet),
        ("rabbit_10_phase_inverted_hart_stem.mp3", synth_phase_inverted_hart_stem),
    ]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for filename, fn in specs:
            wav_file = tmp_path / (filename.replace(".mp3", ".wav"))
            left, right = fn()
            write_stereo_wav(wav_file, left, right)
            mp3_out = out_dir / filename
            stats = master_to_broadcast_mp3(wav_file, mp3_out)
            # Also copy into site/assets/audio/forensics/ for browser Web Audio decoder
            web_copy = assets_dir / filename
            web_copy.write_bytes(mp3_out.read_bytes())
            print(f"[MASTERED] {filename}: {stats['size_bytes']} bytes | silence_gaps={stats['silence_gaps']}")


if __name__ == "__main__":
    main()
