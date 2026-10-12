#!/usr/bin/env python3
"""Applies authentic 1990s 14.4kbps dial-up / RealAudio degradation to all MIDI broadcast tracks.
- Lowers volume by ~8 dB (prevents overpowering vocal songs)
- Restricts bandwidth with 5.2 kHz lowpass filter (removes piercing high-frequency sizzle)
- Adds low-mid warmth and telephone-style presence
- Applies 24 kbps 16 kHz lossy codec compression pass
- Re-encodes to 44.1 kHz 192k stereo for seamless livestream concat
"""

import os
import glob
import tempfile
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
MIDI_DIR = os.path.join(HERE, "broadcast_archive", "midi_masters")

def degrade_track(path):
    with tempfile.TemporaryDirectory() as tmpdir:
        pass1 = os.path.join(tmpdir, "pass1.mp3")
        pass2 = os.path.join(tmpdir, "pass2.mp3")

        # 1. 14.4k modem degradation filter chain + 16kHz 24kbps compression pass
        cmd_degrade = [
            "ffmpeg", "-y",
            "-i", path,
            "-filter_complex",
            "[0:a]volume=0.40,highpass=f=140:poles=1,lowpass=f=5200:poles=2,equalizer=f=400:t=q:w=1.2:g=2.5,equalizer=f=1800:t=q:w=1.5:g=1.5,equalizer=f=3500:t=q:w=1.0:g=-3[a]",
            "-map", "[a]",
            "-c:a", "libmp3lame", "-b:a", "24k", "-ar", "16000", "-ac", "2",
            pass1
        ]
        subprocess.run(cmd_degrade, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # 2. Resample cleanly back to 44.1kHz 192k stereo for seamless livestream concat
        cmd_broadcast = [
            "ffmpeg", "-y",
            "-i", pass1,
            "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            pass2
        ]
        subprocess.run(cmd_broadcast, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Atomic replacement
        os.replace(pass2, path)

def get_volume(path):
    try:
        out = subprocess.check_output(
            ["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "/dev/null"],
            stderr=subprocess.STDOUT
        ).decode()
        mean = None
        max_vol = None
        for line in out.splitlines():
            if "mean_volume:" in line:
                mean = line.split("mean_volume:")[1].strip()
            elif "max_volume:" in line:
                max_vol = line.split("max_volume:")[1].strip()
        return mean, max_vol
    except Exception:
        return "N/A", "N/A"

def main():
    tracks = sorted(glob.glob(os.path.join(MIDI_DIR, "midi_*.mp3")))
    print(f"==========================================================")
    print(f" DEGRADING {len(tracks)} MIDI MASTERS TO 14.4 KBPS 90S STREAM AUDIO")
    print(f" Target: -8 dB volume cut, 5.2 kHz low-pass, 14.4k codec pass")
    print(f"==========================================================")

    for idx, t in enumerate(tracks, 1):
        name = os.path.basename(t)
        mean_before, max_before = get_volume(t)
        degrade_track(t)
        mean_after, max_after = get_volume(t)
        print(f" [{idx:02d}/{len(tracks):02d}] {name:<35} | Peak: {max_before} -> {max_after} | Mean: {mean_before} -> {mean_after}")

    print("\n✓ All MIDI broadcast tracks successfully remastered with 14.4k retro degradation!")

if __name__ == "__main__":
    main()
