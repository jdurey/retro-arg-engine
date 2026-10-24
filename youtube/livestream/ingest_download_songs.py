#!/usr/bin/env python3
"""Dynamically ingests any audio files placed in '/Users/joshuadurey/Downloads/For Live Stream'
into the 24/7 broadcast archive.

Features:
- Scans for .wav, .mp3, .flac, .aif, .aiff, .m4a
- Automatically slugifies names: 'Memory Hatch Reconstruction.wav' -> 'radio_memory_hatch_reconstruction.mp3'
- Precision silence trimming (zero dead air at beginning or end)
- Broadcast mastering: 192kbps 44.1kHz stereo MP3
- Skips already converted files unless modified
"""

import os
import glob
import re
import subprocess

DOWNLOADS_DIR = "/Users/joshuadurey/Downloads/For Live Stream"
HERE = os.path.dirname(os.path.abspath(__file__))
DEST_DIR = os.path.join(HERE, "broadcast_archive", "radio_master_songs")
os.makedirs(DEST_DIR, exist_ok=True)

SUPPORTED_EXTS = (".wav", ".mp3", ".flac", ".aif", ".aiff", ".m4a")

def slugify(filename):
    base, _ = os.path.splitext(filename)
    # Remove leading numbers like "08 ", "14 "
    cleaned = re.sub(r'^\d+\s*[-_.]*\s*', '', base)
    cleaned = cleaned.lower()
    # Normalize Roman numerals
    cleaned = re.sub(r'\bmovement\s+iii\b', 'movement_3', cleaned)
    cleaned = re.sub(r'\bmovement\s+ii\b', 'movement_2', cleaned)
    cleaned = re.sub(r'\bmovement\s+i\b', 'movement_1', cleaned)
    cleaned = re.sub(r'[^a-z0-9]+', '_', cleaned)
    cleaned = cleaned.strip('_')
    return f"radio_{cleaned}.mp3"

# Clean silence trimming + transparent -13.5 LUFS loudness leveling (zero retro EQ or tape hiss)
CLEAN_SONG_TRIM_FILTER = (
    "silenceremove=start_periods=1:start_duration=0.04:start_threshold=-38dB:detection=peak,"
    "areverse,silenceremove=start_periods=1:start_duration=0.08:start_threshold=-38dB:detection=peak,areverse,"
    "loudnorm=I=-13.5:TP=-0.8:LRA=9"
)

from concurrent.futures import ThreadPoolExecutor

EXCLUDED_SLUGS = {
    "radio_two_voices.mp3",
    "radio_synthetic_dawn_retro.mp3",
    "radio_end_like_that.mp3",
    "radio_tape_of_us_1989_rough_mix.mp3",
    "radio_the_second_voice_1.mp3",
    "radio_echoes_of_tomorrow_80s_hard_rock_remix.mp3",
    "radio_faint_residual_(the_upload).mp3",
    "radio_11_ghost_transit.mp3",
    "radio_memory_hatch_reconstruction.mp3",
    "radio_03_only_we_remain_1989_tokyo_master.mp3",
    "radio_someone_else_s_memories_old.mp3",
    "radio_the_world_moves_without_me_old.mp3",
    "radio_nh_synthetic_dawn_1985_synth_original_mix.mp3",
    "radio_abandoned_shell_es.mp3",
    "radio_asset_loss_kr.mp3",
    "radio_03_corridor_dreams.mp3",
}

def process_one_track(item):
    fname, force = item
    src_path = os.path.join(DOWNLOADS_DIR, fname)
    dest_filename = slugify(fname)
    if dest_filename in EXCLUDED_SLUGS:
        return None
    dest_path = os.path.join(DEST_DIR, dest_filename)

    src_mtime = os.path.getmtime(src_path)
    dest_exists = os.path.exists(dest_path)
    dest_mtime = os.path.getmtime(dest_path) if dest_exists else 0

    # If dest exists and is newer than source, skip unless force is True
    if not force and dest_exists and dest_mtime >= src_mtime:
        return None

    try:
        tmp_trimmed = dest_path + ".trimmed.mp3"
        cmd = [
            "ffmpeg", "-y",
            "-i", src_path,
            "-af", CLEAN_SONG_TRIM_FILTER,
            "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            tmp_trimmed
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        os.replace(tmp_trimmed, dest_path)

        cmd_info = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", dest_path]
        dur = float(subprocess.check_output(cmd_info).decode().strip())
        sz_kb = os.path.getsize(dest_path) // 1024
        print(f"  ✓ {dest_filename}: {dur:.2f}s ({sz_kb} KB) untouched studio audio!")
        return dest_path
    except Exception as e:
        print(f"  ✗ Failed to process {fname}: {e}")
        return None

def ingest_all(force=False):
    if not os.path.exists(DOWNLOADS_DIR):
        print(f"Directory not found: {DOWNLOADS_DIR}")
        return []

    candidates = [f for f in os.listdir(DOWNLOADS_DIR) if f.lower().endswith(SUPPORTED_EXTS) and not f.startswith(".")]
    tasks = [(f, force) for f in sorted(candidates)]

    print(f"Ingesting {len(tasks)} tracks with Radio Broadcast EQ (4 workers)...")
    newly_added = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(process_one_track, tasks))
        newly_added = [r for r in results if r is not None]

    return newly_added

if __name__ == "__main__":
    added = ingest_all()
    if added:
        print(f"\nSuccessfully added {len(added)} new track(s) to rotation!")
    else:
        print("\nAll tracks in folder are up to date.")
