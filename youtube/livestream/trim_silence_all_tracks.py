#!/usr/bin/env python3
"""Trims leading and trailing silence from all broadcast audio tracks.
Eliminates dead space between songs on the 24/7 YouTube livestream.

Processes:
- radio_master_songs/ (48 studio tracks)
- midi_masters/ (30 Roland/Yamaha FM compositions)
- newscasts/ (10 retro emergency bulletins)
- geocities_readings/ (6 multilingual readings)
- classified_lab_tapes/ (10 lab recordings)
- intercepts/ (rabbit hole phone/tape intercepts)
"""

import os
import glob
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(HERE, "broadcast_archive")

TARGET_DIRS = [
    os.path.join(ARCHIVE_DIR, "radio_master_songs"),
    os.path.join(ARCHIVE_DIR, "midi_masters"),
    os.path.join(ARCHIVE_DIR, "newscasts"),
    os.path.join(ARCHIVE_DIR, "geocities_readings"),
    os.path.join(ARCHIVE_DIR, "classified_lab_tapes"),
    os.path.join(HERE, "intercepts"),
]

def trim_file(file_path):
    # Check original duration
    try:
        cmd_info = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
        orig_dur = float(subprocess.check_output(cmd_info).decode().strip())
    except Exception:
        return 0.0

    # Trimming filter:
    # 1. silenceremove at start: remove silence below -28dB, keep start clean
    # 2. areverse -> silenceremove at end (now start) -> areverse
    af_filter = "silenceremove=start_periods=1:start_duration=0.04:start_threshold=-28dB:detection=peak,areverse,silenceremove=start_periods=1:start_duration=0.08:start_threshold=-28dB:detection=peak,areverse"

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        cmd = [
            "ffmpeg", "-y", "-i", file_path,
            "-af", af_filter,
            "-c:a", "libmp3lame", "-b:a", "192k",
            tmp_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            os.remove(tmp_path)
            return 0.0

        # Check new duration
        new_dur = float(subprocess.check_output(cmd_info[:-1] + [tmp_path]).decode().strip())
        trimmed_sec = orig_dur - new_dur

        # Replace file if valid (must be at least 1 second)
        if new_dur >= 1.0 and trimmed_sec > 0.05:
            os.replace(tmp_path, file_path)
            return trimmed_sec
        else:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return 0.0
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return 0.0

def main():
    print("==========================================================")
    print(" TRIMMING DEAD SPACE AND SILENCE ACROSS BROADCAST TRACKS")
    print("==========================================================")

    total_trimmed = 0.0
    files_modified = 0

    for d in TARGET_DIRS:
        if not os.path.isdir(d):
            continue
        files = sorted(glob.glob(os.path.join(d, "*.mp3")))
        print(f"\nProcessing {len(files)} tracks in {os.path.basename(d)}...")
        for f in files:
            trimmed = trim_file(f)
            if trimmed > 0.05:
                print(f"  ✓ {os.path.basename(f):<35} - cut {trimmed:.2f}s dead air")
                total_trimmed += trimmed
                files_modified += 1

    print(f"\nFinished! Trimmed a total of {total_trimmed:.2f} seconds of dead air across {files_modified} files.")

if __name__ == "__main__":
    main()
