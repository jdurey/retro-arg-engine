#!/usr/bin/env python3
"""Builds an infinite looping audio playlist for the 24/7 YouTube live stream."""

import os
import glob
import random

HERE = os.path.dirname(os.path.abspath(__file__))
YOUTUBE_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(YOUTUBE_DIR)
AUDIO_DIR = os.path.join(ROOT, "site", "ftp", "kamome", "audio")

MIDI_DIR = os.path.join(ROOT, "site", "ftp", "kamome", "midi")

out_file = os.path.join(HERE, "playlist.txt")

tracks = []
tracks += glob.glob(os.path.join(MIDI_DIR, "*_14k.mp3"))
tracks += glob.glob(os.path.join(AUDIO_DIR, "*.mp3"))

# Filter to playable mp3s
valid_tracks = [t for t in tracks if os.path.isfile(t)]
random.shuffle(valid_tracks)

with open(out_file, "w") as f:
    for t in valid_tracks:
        f.write(f"file '{t}'\n")

print(f"Generated 24/7 livestream playlist with {len(valid_tracks)} audio tracks in {out_file}")
