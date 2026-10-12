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

def ingest_all():
    if not os.path.exists(DOWNLOADS_DIR):
        print(f"Directory not found: {DOWNLOADS_DIR}")
        return []

    newly_added = []
    candidates = [f for f in os.listdir(DOWNLOADS_DIR) if f.lower().endswith(SUPPORTED_EXTS) and not f.startswith(".")]

    for fname in sorted(candidates):
        src_path = os.path.join(DOWNLOADS_DIR, fname)
        dest_filename = slugify(fname)
        dest_path = os.path.join(DEST_DIR, dest_filename)

        src_mtime = os.path.getmtime(src_path)
        dest_exists = os.path.exists(dest_path)
        dest_mtime = os.path.getmtime(dest_path) if dest_exists else 0

        # If dest exists and is newer than source, skip
        if dest_exists and dest_mtime >= src_mtime:
            continue

        print(f"Ingesting '{fname}' -> '{dest_filename}'...")
        try:
            cmd = [
                "ffmpeg", "-y",
                "-i", src_path,
                "-af", "silenceremove=start_periods=1:start_duration=0.04:start_threshold=-30dB:detection=peak,areverse,silenceremove=start_periods=1:start_duration=0.08:start_threshold=-30dB:detection=peak,areverse",
                "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                dest_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            cmd_info = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", dest_path]
            dur = float(subprocess.check_output(cmd_info).decode().strip())
            sz_kb = os.path.getsize(dest_path) // 1024
            print(f"  ✓ {dest_filename}: {dur:.2f}s ({sz_kb} KB) ready for broadcast!")
            newly_added.append(dest_path)
        except Exception as e:
            print(f"  ✗ Failed to process {fname}: {e}")

    return newly_added

if __name__ == "__main__":
    added = ingest_all()
    if added:
        print(f"\nSuccessfully added {len(added)} new track(s) to rotation!")
    else:
        print("\nAll tracks in folder are up to date.")
