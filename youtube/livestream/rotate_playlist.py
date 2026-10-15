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
        return 0.0, ""
    
    last_rot_file = os.path.join(DIR, ".last_rotated_session")
    already_rotated = ""
    if os.path.exists(last_rot_file):
        try:
            already_rotated = open(last_rot_file).read().strip()
        except Exception:
            pass

    # Read the last 512 KB of stream.log so warning lines never obscure time=HH:MM:SS
    try:
        with open(LOG_FILE, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 524288))
            chunk = f.read().decode("utf-8", errors="ignore")
        # Walk backwards through recent FFmpeg sessions so a brief <15s reconnect never masks a longer session
        parts = chunk.split("[STREAM.SH] Selected encoder:")
        for idx in range(len(parts) - 1, 0, -1):
            session_chunk = parts[idx]
            prev_lines = parts[idx - 1].splitlines()
            hdr_stamp = prev_lines[-1][:21] if prev_lines else f"idx{idx}"
            matches = re.findall(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)", session_chunk)
            if matches:
                best = 0.0
                for m in matches[-50:]:
                    sec = float(m[0]) * 3600.0 + float(m[1]) * 60.0 + float(m[2])
                    if sec > best:
                        best = sec
                session_id = f"{hdr_stamp}:{int(best)}"
                if best >= 15.0 and session_id != already_rotated:
                    return best, session_id
    except Exception as e:
        print(f"Warning: could not parse elapsed time from log: {e}")
    return 0.0, ""

import json

DURATIONS_FILE = os.path.join(DIR, "track_durations.json")
try:
    with open(DURATIONS_FILE, "r") as _df:
        _DURATION_CACHE = json.load(_df)
except Exception:
    _DURATION_CACHE = {}

def get_duration(filepath):
    bname = os.path.basename(filepath)
    if bname in _DURATION_CACHE:
        try:
            if os.path.getsize(filepath) > 4096:
                return float(_DURATION_CACHE[bname])
        except Exception:
            return float(_DURATION_CACHE[bname])
    try:
        sz = os.path.getsize(filepath)
        if sz <= 4096:
            return 0.05
        with open(filepath, "rb") as f:
            hdr = f.read(10)
        if len(hdr) == 10 and hdr[:3] == b"ID3":
            id3_sz = ((hdr[6] & 0x7f) << 21) | ((hdr[7] & 0x7f) << 14) | ((hdr[8] & 0x7f) << 7) | (hdr[9] & 0x7f)
            sz -= (id3_sz + 10)
        return max(0.05, (sz - 1440) / 24000.0)
    except Exception:
        return 200.0


def rotate():
    elapsed, session_id = get_last_elapsed_seconds()
    last_rot_file = os.path.join(DIR, ".last_rotated_session")

    fresh_marker = os.path.join(DIR, ".playlist_fresh")
    if os.path.exists(fresh_marker):
        try:
            os.remove(fresh_marker)
        except OSError:
            pass
        if session_id:
            try:
                with open(last_rot_file, "w") as lf:
                    lf.write(session_id)
            except Exception:
                pass
        print("✓ Freshly built playlist detected; starting directly at newly queued Track #1.")
        return

    print(f"Last stream session elapsed time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
    
    if elapsed < 15.0:
        print("Stream ran for less than 15s; keeping current playhead.")
        return
    if session_id and os.path.exists(last_rot_file):
        try:
            if open(last_rot_file).read().strip() == session_id:
                print("Session already rotated; skipping duplicate rotation.")
                return
        except Exception:
            pass
    if session_id:
        try:
            with open(last_rot_file, "w") as lf:
                lf.write(session_id)
        except Exception:
            pass

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
