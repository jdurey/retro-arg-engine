#!/usr/bin/env python3
"""Normalizes all 80s FM songs (Velvet Tide, Vyper Strike, Neon Comets, Thunder Machine),
Heartstrike songs, and any quiet tracks in radio_master_songs/ (RMS < -16.0 dBFS)
to -13.5 LUFS (TP=-0.8 dBTP, LRA=9) with 100% transparent studio audio (zero EQ coloration),
and boosts the 80s FM Rick Blaze (blaze_ep01_*) & White Lines (wlf_*) segments to -14.0 LUFS.
"""

import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
SONG_DIR = HERE / "broadcast_archive" / "radio_master_songs"
NEWS_DIR = HERE / "broadcast_archive" / "newscasts"

PRIORITY_80SFM_AND_HEARTSTRIKE = {
    "radio_lost_in_london_velvet_tide.mp3",
    "radio_midnight_venom_vyper_strike.mp3",
    "radio_synth_dreams_neon_comets.mp3",
    "radio_electric_storm_thunder_machine.mp3",
    "radio_echoes_of_tomorrow_80s_hard_rock_remix.mp3",
    "radio_crossing_this_line_remastered.mp3",
    "radio_to_the_end_of_time.mp3",
    "radio_lightning_strikes_twice.mp3",
    "radio_frame_by_frame.mp3",
    "radio_fire_in_your_heart.mp3",
    "radio_to_the_ends_of_forever.mp3",
    "radio_frame_your_shot.mp3",
    "radio_heart_and_mind_aligned.mp3",
    "radio_edit_the_script.mp3",
    "radio_all_in_this_is_the_moment.mp3",
}


def measure_rms_peak(mp3_path: Path) -> tuple[float, float]:
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-nostdin", "-loglevel", "error",
        "-ss", "20", "-t", "50", "-i", str(mp3_path),
        "-ac", "2", "-ar", "22050", "-f", "s16le", "-",
    ]
    raw = subprocess.run(cmd, capture_output=True).stdout
    if not raw or len(raw) < 8192:
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-nostdin", "-loglevel", "error",
            "-i", str(mp3_path), "-ac", "2", "-ar", "22050", "-f", "s16le", "-",
        ]
        raw = subprocess.run(cmd, capture_output=True).stdout
    if not raw:
        return 0.0, 0.0
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    rms_db = float(20.0 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9))
    peak_db = float(20.0 * np.log10(np.max(np.abs(x)) + 1e-9))
    return rms_db, peak_db


def normalize_one_song(mp3_path: Path) -> tuple[str, bool, str]:
    name = mp3_path.name
    rms_before, peak_before = measure_rms_peak(mp3_path)
    force = name in PRIORITY_80SFM_AND_HEARTSTRIKE
    if not force and rms_before >= -16.2:
        return name, False, f"already loud (RMS={rms_before:.2f} dBFS, Peak={peak_before:.2f} dBFS)"

    with tempfile.TemporaryDirectory() as tmpdir:
        out_tmp = Path(tmpdir) / name
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y", "-nostdin", "-loglevel", "error",
            "-i", str(mp3_path),
            "-af", "loudnorm=I=-13.5:TP=-0.8:LRA=9",
            "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_tmp),
        ]
        subprocess.run(cmd, check=True)
        os.replace(out_tmp, mp3_path)

    rms_after, peak_after = measure_rms_peak(mp3_path)
    return (
        name,
        True,
        f"RMS {rms_before:6.2f} -> {rms_after:6.2f} dBFS | Peak {peak_before:5.2f} -> {peak_after:5.2f} dBFS",
    )


def normalize_one_podcast_segment(mp3_path: Path) -> tuple[str, bool, str]:
    name = mp3_path.name
    rms_before, peak_before = measure_rms_peak(mp3_path)
    with tempfile.TemporaryDirectory() as tmpdir:
        out_tmp = Path(tmpdir) / name
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y", "-nostdin", "-loglevel", "error",
            "-i", str(mp3_path),
            "-af", "acompressor=threshold=-20dB:ratio=3.5:attack=5:release=60:makeup=3dB,loudnorm=I=-14.0:TP=-1.0:LRA=6",
            "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_tmp),
        ]
        subprocess.run(cmd, check=True)
        os.replace(out_tmp, mp3_path)
    rms_after, peak_after = measure_rms_peak(mp3_path)
    return (
        name,
        True,
        f"RMS {rms_before:6.2f} -> {rms_after:6.2f} dBFS | Peak {peak_before:5.2f} -> {peak_after:5.2f} dBFS",
    )


def main() -> None:
    songs = sorted(SONG_DIR.glob("*.mp3"))
    print(f"Checking & normalizing {len(songs)} songs in {SONG_DIR} (target: -13.5 LUFS)...")
    updated = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        for name, changed, msg in ex.map(normalize_one_song, songs):
            if changed:
                updated += 1
                tag = "[80s FM / HS]" if name in PRIORITY_80SFM_AND_HEARTSTRIKE else "[SONG NORM]  "
                print(f"  {tag} {name:50s} | {msg}")

    podcast_segs = sorted(NEWS_DIR.glob("blaze_*.mp3")) + sorted(NEWS_DIR.glob("wlf_*.mp3"))
    print(f"\nBoosting {len(podcast_segs)} 80s FM & White Lines segments to match song presence (-14.0 LUFS)...")
    with ThreadPoolExecutor(max_workers=6) as ex:
        for name, changed, msg in ex.map(normalize_one_podcast_segment, podcast_segs):
            print(f"  [80s FM SEG]  {name:50s} | {msg}")

    print(f"\nNormalized {updated} songs and {len(podcast_segs)} 80s FM / WLF broadcast segments!")


if __name__ == "__main__":
    main()
