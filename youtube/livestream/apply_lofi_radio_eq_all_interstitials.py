#!/usr/bin/env python3
"""Applies the uniform 1980s lo-fi AM/shortwave/pirate radio bandpass EQ treatment
(280-3400 Hz bandpass, midrange transistor resonance, analog broadcast compression,
shortwave squelch break-in/carrier bed on clean podcast/documentary extracts, and
-16 LUFS broadcast loudness) across ALL interstitials in the broadcast archive.

NEVER touches radio_master_songs/ (all vocal songs remain 100% untouched studio audio).
"""

import os
import subprocess
import tempfile
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "broadcast_archive"
SR = 44100

INTERSTITIAL_DIRS = [
    ARCHIVE / "newscasts",
    ARCHIVE / "multilingual_bulletins",
    ARCHIVE / "geocities_readings",
    ARCHIVE / "classified_lab_tapes",
    ARCHIVE / "numbers_stations",
    ARCHIVE / "arg_intercepts",
    ARCHIVE / "marcus_footprint",
    HERE / "intercepts",
]

# Classic lo-fi 1980s radio bandpass EQ & broadcast compression chain
LOFI_RADIO_EQ_WITH_ECHO = (
    "highpass=f=280:poles=2,highpass=f=240:poles=2,"
    "lowpass=f=3400:poles=2,lowpass=f=3700:poles=2,"
    "equalizer=f=950:t=q:w=1.2:g=3.0,"
    "equalizer=f=2150:t=q:w=1.4:g=2.2,"
    "aecho=0.8:0.65:22:0.10,"
    "acompressor=threshold=-18dB:ratio=4:attack=6:release=70,"
    "loudnorm=I=-16:TP=-1.5:LRA=7"
)

LOFI_RADIO_EQ_BANDPASS = (
    "highpass=f=280:poles=2,highpass=f=240:poles=2,"
    "lowpass=f=3400:poles=2,lowpass=f=3700:poles=2,"
    "equalizer=f=950:t=q:w=1.2:g=2.6,"
    "equalizer=f=2150:t=q:w=1.4:g=1.8,"
    "acompressor=threshold=-18dB:ratio=3.8:attack=6:release=70,"
    "loudnorm=I=-16:TP=-1.5:LRA=7"
)


def measure_hf_lf_ratio(mp3_path: Path) -> tuple[float, float]:
    """Measures HF (>3.8kHz) / MID (300-3200Hz) and LF (<200Hz) / MID energy ratios."""
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-nostdin", "-loglevel", "error",
        "-ss", "2", "-t", "18", "-i", str(mp3_path),
        "-ac", "1", "-ar", "16000", "-f", "s16le", "-",
    ]
    raw = subprocess.run(cmd, capture_output=True).stdout
    if not raw or len(raw) < 8192:
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-nostdin", "-loglevel", "error",
            "-i", str(mp3_path), "-ac", "1", "-ar", "16000", "-f", "s16le", "-",
        ]
        raw = subprocess.run(cmd, capture_output=True).stdout
    if not raw:
        return 0.0, 0.0
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    if len(x) < 2048:
        return 0.0, 0.0
    spec = np.abs(np.fft.rfft(x))
    freqs = np.fft.rfftfreq(len(x), d=1.0 / 16000.0)
    mid = float(np.sum(spec[(freqs >= 300) & (freqs <= 3200)] ** 2)) + 1e-9
    hf = float(np.sum(spec[freqs > 3800] ** 2))
    lf = float(np.sum(spec[freqs < 200] ** 2))
    return hf / mid, lf / mid


def synth_radio_static_bed(n_samples: int, seed: int) -> np.ndarray:
    """Synthesizes a 1980s shortwave/AM squelch break-in/out & subtle analog carrier bed."""
    rng = np.random.default_rng(seed)
    t = np.arange(n_samples, dtype=np.float32) / float(SR)
    total_sec = n_samples / float(SR)

    noise = rng.normal(0.0, 0.015, size=(n_samples, 2)).astype(np.float32)
    crackle = (rng.random((n_samples, 2)) > 0.9988).astype(np.float32) * rng.uniform(
        -0.14, 0.14, size=(n_samples, 2)
    ).astype(np.float32)

    # Squelch envelope: brief static break-in (0.0-0.42s), quiet analog carrier floor (0.025),
    # and brief squelch tail at end
    squelch_env = np.ones(n_samples, dtype=np.float32) * 0.025
    in_end = min(n_samples, int(0.42 * SR))
    if in_end > 0:
        squelch_env[:in_end] = np.linspace(0.65, 0.025, in_end, dtype=np.float32)
    out_start = max(0, int((total_sec - 0.48) * SR))
    if out_start < n_samples:
        squelch_env[out_start:] = np.linspace(0.025, 0.55, n_samples - out_start, dtype=np.float32)

    # Subtle 1020 Hz heterodyne whistle during squelch break-in/out only
    whistle_env = np.zeros(n_samples, dtype=np.float32)
    if in_end > 0:
        whistle_env[:in_end] = np.sin(np.linspace(0, np.pi, in_end, dtype=np.float32)) * 0.035
    if out_start < n_samples:
        whistle_env[out_start:] = np.sin(np.linspace(0, np.pi, n_samples - out_start, dtype=np.float32)) * 0.030
    whistle = (np.sin(2.0 * np.pi * 1020.0 * t) * whistle_env)[:, None]

    bed = (noise + crackle) * (1.0 + squelch_env[:, None] * 6.5) + whistle
    return np.clip(bed, -0.35, 0.35).astype(np.float32)


def process_one_interstitial(args: tuple[int, Path]) -> tuple[str, bool, str]:
    idx, mp3_path = args
    assert "radio_master_songs" not in str(mp3_path), f"SAFETY ABORT: {mp3_path}"
    assert "real_nova_songs" not in str(mp3_path), f"SAFETY ABORT: {mp3_path}"

    name = mp3_path.name
    is_podcast_extract = name.startswith("wlf_") or name.startswith("blaze_")

    hf_ratio, lf_ratio = measure_hf_lf_ratio(mp3_path)
    # If already tightly band-limited and not a clean podcast extract, skip
    if not is_podcast_extract and hf_ratio <= 0.0020 and lf_ratio <= 0.1100:
        return name, False, f"already lo-fi (HF={hf_ratio:.4f}, LF={lf_ratio:.4f})"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        if is_podcast_extract:
            # Decode stereo 44.1kHz PCM, mix subtle shortwave squelch & carrier bed, then apply LOFI_RADIO_EQ_WITH_ECHO
            raw_cmd = [
                "/opt/homebrew/bin/ffmpeg", "-nostdin", "-loglevel", "error",
                "-i", str(mp3_path),
                "-ar", str(SR), "-ac", "2", "-f", "s16le", "-",
            ]
            raw_bytes = subprocess.run(raw_cmd, capture_output=True, check=True).stdout
            pcm = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32).reshape(-1, 2) / 32768.0
            bed = synth_radio_static_bed(pcm.shape[0], seed=198300 + idx)
            mixed = np.clip(pcm * 0.94 + bed, -0.98, 0.98)
            in_wav = tmp_dir / "mixed_in.wav"
            with wave.open(str(in_wav), "wb") as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(SR)
                wf.writeframes((mixed * 32767.0).astype(np.int16).tobytes())
            src_for_ffmpeg = in_wav
            af_chain = LOFI_RADIO_EQ_WITH_ECHO
        else:
            src_for_ffmpeg = mp3_path
            af_chain = LOFI_RADIO_EQ_BANDPASS

        out_tmp = tmp_dir / name
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y", "-nostdin", "-loglevel", "error",
            "-i", str(src_for_ffmpeg),
            "-af", af_chain,
            "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_tmp),
        ]
        subprocess.run(cmd, check=True)
        os.replace(out_tmp, mp3_path)

    hf_after, lf_after = measure_hf_lf_ratio(mp3_path)
    return name, True, f"HF {hf_ratio:.4f}->{hf_after:.4f}, LF {lf_ratio:.4f}->{lf_after:.4f}"


def main() -> None:
    all_files: list[Path] = []
    for d in INTERSTITIAL_DIRS:
        if d.exists():
            all_files.extend(sorted(d.glob("*.mp3")))

    print(f"Auditing & applying lo-fi radio EQ across {len(all_files)} interstitials...")
    tasks = list(enumerate(all_files))
    updated = 0
    skipped = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        for name, changed, msg in ex.map(process_one_interstitial, tasks):
            if changed:
                updated += 1
                print(f"  [EQ APPLIED] {name:52s} | {msg}")
            else:
                skipped += 1

    print(f"\nDone! Updated {updated} interstitials with lo-fi radio EQ ({skipped} already lo-fi).")


if __name__ == "__main__":
    main()
