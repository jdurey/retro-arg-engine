#!/usr/bin/env python3
"""Maintains persistent playlist playhead across stream restarts.
Extracts elapsed streaming time from stream.log, determines which tracks
have completed playing, and rotates them to the end of playlist.txt so
the broadcast always advances continuously with ZERO song repetition.
"""

import os
import re
import subprocess

DIR = os.path.dirname(os.path.abspath(__file__))
PLAYLIST = os.path.join(DIR, "playlist.txt")
LOG_FILE = os.path.join(DIR, "stream.log")

def get_last_elapsed_seconds():
    if not os.path.exists(LOG_FILE):
        return 0.0
    
    # Read the tail of stream.log to find the last time=HH:MM:SS string
    try:
        res = subprocess.run(["tail", "-n", "100", LOG_FILE], capture_output=True, text=True)
        matches = re.findall(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)", res.stdout)
        if matches:
            last = matches[-1]
            h, m, s = float(last[0]), float(last[1]), float(last[2])
            return h * 3600.0 + m * 60.0 + s
    except Exception as e:
        print(f"Warning: could not parse elapsed time from log: {e}")
    return 0.0

def get_duration(filepath):
    try:
        cmd = ["ffprobe", "-i", filepath, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
        out = subprocess.check_output(cmd, text=True).strip()
        return float(out)
    except Exception:
        return 200.0 # fallback

def rotate():
    fresh_marker = os.path.join(DIR, ".playlist_fresh")
    if os.path.exists(fresh_marker):
        try:
            os.remove(fresh_marker)
        except OSError:
            pass
        print("✓ Freshly built playlist detected; starting directly at newly queued Track #1.")
        return

    elapsed = get_last_elapsed_seconds()
    print(f"Last stream session elapsed time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
    
    if elapsed < 15.0:
        print("Stream ran for less than 15s; keeping current playhead.")
        return

    if not os.path.exists(PLAYLIST):
        print("playlist.txt does not exist; skipping rotation.")
        return

    with open(PLAYLIST, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return

    # Extract file paths from lines like: file '/path/to/file.mp3'
    paths = []
    for l in lines:
        m = re.search(r"file\s+'([^']+)'", l)
        if m:
            paths.append(m.group(1))
        else:
            paths.append(l)

    # Accumulate durations up to elapsed
    accum = 0.0
    played_count = 0
    for i, path in enumerate(paths):
        dur = get_duration(path)
        if accum + dur <= elapsed:
            accum += dur
            played_count = i + 1
        else:
            # We are currently in the middle of track i, so everything before i has finished
            played_count = i
            break

    if played_count > 0:
        played_lines = lines[:played_count]
        remaining_lines = lines[played_count:]
        new_playlist = remaining_lines + played_lines
        
        # Write atomically
        tmp_path = PLAYLIST + ".tmp"
        with open(tmp_path, "w") as f:
            for l in new_playlist:
                f.write(l + "\n")
        os.replace(tmp_path, PLAYLIST)

        print(f"✓ Rotated {played_count} played tracks ({accum/60:.1f} min of audio) to tail.")
        if remaining_lines:
            next_track = remaining_lines[0].split("/")[-1].replace("'", "")
            print(f"✓ Resuming stream seamlessly from: {next_track}")
    else:
        print("Played count is 0; no rotation needed.")

if __name__ == "__main__":
    rotate()
