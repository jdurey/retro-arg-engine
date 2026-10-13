#!/usr/bin/env python3
"""
Project Stardust — High-Level Audio Forensics & Multi-Stage Signal Synthesizer
Each intercept encodes ONE authentic technical component of Marcus Hale's
September 9, 1989 Sublevel B2 emergency egress (never a pre-solved password):

  1. rabbit_08_sstv_b2_schematic.mp3
     - Robot36 VIS header (1900Hz / 1200Hz) + scanline luminance (1500-2300 Hz)
       encoding the Sublevel B2-114 DMA Partition Map pointing to two GeoCities
       homestead anchors: TOKYO/GARDEN/1420 and SILICONVALLEY/LAB/1984.
     - Tail CW Morse (750 Hz): "DMA ANCHORS TOKYO 1420 SV 1984"

  2. rabbit_09_bell103_relcom_packet.mp3
     - Bell 103 AFSK frame (1270 Hz mark / 1070 Hz space) captured by Relcom
       Node-08 (4625 kHz) carrying the raw UUCP egress telemetry header:
       "FM RELCOM-08 TO ASHPOLY-07 // SEQ 89-09-09T03:59Z // FEISTEL-MASK: 0x3A5F // NULL CH-L+CH-R FOR SALT"
     - Tail CW Morse (750 Hz): "FEISTEL MASK 0X3A5F"

  3. rabbit_10_phase_inverted_hart_stem.mp3
     - Differential phase puzzle: A loud 330/495/990 Hz calibration triad is
       recorded 180 degrees out of phase between Left and Right channels (corr = -0.94).
     - In stereo, the calibration triad masks the sub-carrier. When the investigator
       sums Left + Right to mono (phase cancellation), the triad cancels by >40 dB
       and isolates Marcus Hale's 750 Hz CW Morse bias inscription:
       "B2 EGRESS SALT 7704 AKASAKA"
"""

from __future__ import annotations
import math
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


def lcg_noise(seed: int) -> tuple[int, float]:
    seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
    return seed, ((seed / 1073741824.0) - 1.0)


def encode_morse_envelope(message: str, unit_sec: float = 0.052) -> list[float]:
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
    total_samples = int(SAMPLE_RATE * duration_sec)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    rows_ascii = [
        "################",
        "#B2-DMA-MAP-89.#",
        "#.####...####..#",
        "#.#...#.#....#.#",
        "#.####......#..#",
        "#.#...#...##...#",
        "#.####...######.",
        "#..............#",
        "#A:TOKYO/1420..#",
        "#B:SV-LAB/1984.#",
        "#..............#",
        "#..*........*..#",
        "#...*..**..*...#",
        "#....******....#",
        "#..XOR->RELCOM.#",
        "################",
    ]

    morse_env = encode_morse_envelope("DMA ANCHORS TOKYO 1420 SV 1984", unit_sec=0.044)
    phase = 0.0
    seed = 89114

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        seed, wn = lcg_noise(seed)

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
                freq = 1200.0
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
            m_idx = (i - int(13.70 * SAMPLE_RATE)) % max(1, len(morse_env))
            m_amp = morse_env[m_idx]
            sig = (0.42 * m_amp + 0.08) * math.sin(phase)

        left[i] = sig + bed
        right[i] = sig * 0.96 + bed * 1.04 + 0.03 * math.cos(phase * 0.5)

    return left, right


def synth_bell103_relcom_packet(duration_sec: float = 15.0) -> tuple[list[float], list[float]]:
    total_samples = int(SAMPLE_RATE * duration_sec)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    payload = (
        b"FM RELCOM-08 TO ASHPOLY-07 UI PID=F0 // "
        b"SEQ: 89-09-09T03:59Z // FEISTEL-MASK: 0x3A5F // "
        b"NULL CH-L+CH-R ON REEL SD-0009 FOR EGRESS SALT\r\n"
    )
    bits: list[int] = [1] * 50
    for b in payload:
        bits.append(0)
        for bit_pos in range(8):
            bits.append((b >> bit_pos) & 1)
        bits.append(1)
        bits.append(1)
    bits.extend([1] * 40)

    baud = 110.0
    samples_per_bit = SAMPLE_RATE / baud
    morse_env = encode_morse_envelope("FEISTEL MASK 0X3A5F", unit_sec=0.048)

    phase = 0.0
    seed = 199510

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        seed, wn = lcg_noise(seed)

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
    total_samples = int(SAMPLE_RATE * duration_sec)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    morse_env = encode_morse_envelope("B2 EGRESS SALT 7704 AKASAKA", unit_sec=0.048)
    seed = 4127

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        seed, wn = lcg_noise(seed)

        flutter = 1.0 + 0.003 * math.sin(2.0 * math.pi * 5.5 * t)
        mask = (
            0.34 * math.sin(2.0 * math.pi * 330.0 * flutter * t)
            + 0.24 * math.sin(2.0 * math.pi * 495.0 * flutter * t)
            + 0.16 * math.sin(2.0 * math.pi * 990.0 * flutter * t)
        )

        m_amp = morse_env[i % len(morse_env)]
        secret_morse = (0.28 * m_amp) * math.sin(2.0 * math.pi * 750.0 * t)
        secret_pad = 0.14 * math.sin(2.0 * math.pi * 220.0 * t) * (1.0 + 0.25 * math.sin(2.0 * math.pi * 14.2001 * t))
        tape_hiss = 0.025 * wn

        left[i] = secret_morse + secret_pad + mask + tape_hiss
        right[i] = secret_morse + secret_pad - mask + tape_hiss

    return left, right


def master_to_broadcast_mp3(wav_path: Path, mp3_path: Path) -> dict:
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

    verify_cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-hide_banner",
        "-i", str(mp3_path),
        "-af", "silencedetect=n=-30dB:d=0.5,ebur128=peak=true",
        "-f", "null",
        "-",
    ]
    res = subprocess.run(verify_cmd, check=True, capture_output=True, text=True)
    silence_hits = res.stderr.count("silence_start:")
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
            web_copy = assets_dir / filename
            web_copy.write_bytes(mp3_out.read_bytes())
            print(f"[MASTERED] {filename}: {stats['size_bytes']} bytes | silence_gaps={stats['silence_gaps']}")


if __name__ == "__main__":
    main()
