#!/usr/bin/env python3
"""Shortens all 30 MIDI broadcast tracks to 3.5 seconds (3-4s range).
- Removes any leading silence so the synth starts immediately
- Trims to exactly 3.5 seconds
- Applies a smooth 0.3s micro-fadeout (from 3.2s to 3.5s) to eliminate clicks
- Re-encodes at 44.1 kHz 192k stereo for seamless livestream concat
"""

import os
import glob
import tempfile
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
MIDI_DIR = os.path.join(HERE, "broadcast_archive", "midi_masters")

TARGET_DURATION = 3.5  # Exactly in the 3-4s range requested by user
FADE_START = 3.2
FADE_DUR = 0.3

def shorten_track(path):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name

    af_filter = (
        f"silenceremove=start_periods=1:start_duration=0.01:start_threshold=-35dB:detection=peak,"
        f"atrim=0:{TARGET_DURATION},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={FADE_START}:d={FADE_DUR}"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", path,
        "-af", af_filter,
        "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        tmp_path
    ]

    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # Check new duration
        cmd_dur = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", tmp_path
        ]
        dur = float(subprocess.check_output(cmd_dur).decode().strip())
        os.replace(tmp_path, path)
        return dur
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        print(f"Error shortening {path}: {e}")
        return None

def main():
    tracks = sorted(glob.glob(os.path.join(MIDI_DIR, "*.mp3")))
    print(f"Shortening {len(tracks)} MIDI tracks to {TARGET_DURATION} seconds (3-4s stinger range)...")

    for t in tracks:
        name = os.path.basename(t)
        new_dur = shorten_track(t)
        if new_dur is not None:
            print(f"  ✓ {name}: {new_dur:.2f}s")
        else:
            print(f"  ✗ {name}: Failed")

    print("\nAll MIDI tracks successfully shortened.")

if __name__ == "__main__":
    main()
