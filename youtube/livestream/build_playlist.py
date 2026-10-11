#!/usr/bin/env python3
"""Builds an infinite looping audio playlist for the 24/7 YouTube live stream.
Interweaves retro MIDI/synth tracks with authentic shortwave numbers station voice intercepts.
"""

import os
import glob
import random

HERE = os.path.dirname(os.path.abspath(__file__))
YOUTUBE_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(YOUTUBE_DIR)
AUDIO_DIR = os.path.join(ROOT, "site", "ftp", "kamome", "audio")
MIDI_DIR = os.path.join(ROOT, "site", "ftp", "kamome", "midi")
INTERCEPT_DIR = os.path.join(HERE, "intercepts")

out_file = os.path.join(HERE, "playlist.txt")

music_tracks = []
music_tracks += glob.glob(os.path.join(MIDI_DIR, "*_14k.mp3"))
music_tracks += glob.glob(os.path.join(AUDIO_DIR, "*.mp3"))
music_tracks = [t for t in music_tracks if os.path.isfile(t)]
random.shuffle(music_tracks)

intercept_tracks = glob.glob(os.path.join(INTERCEPT_DIR, "*.mp3"))
intercept_tracks = [t for t in intercept_tracks if os.path.isfile(t)]
random.shuffle(intercept_tracks)

# Interleave: 2-3 music tracks -> 1 intercept -> repeat
full_playlist = []
int_idx = 0

for i, track in enumerate(music_tracks):
    full_playlist.append(track)
    # Every 2 to 3 tracks, insert an atmospheric numbers station / intercepted transmission
    if (i + 1) % 2 == 0 and intercept_tracks:
        full_playlist.append(intercept_tracks[int_idx % len(intercept_tracks)])
        int_idx += 1

with open(out_file, "w") as f:
    for t in full_playlist:
        f.write(f"file '{t}'\n")

print(f"Generated ARG livestream playlist: {len(full_playlist)} items ({len(music_tracks)} music, {int_idx} intercepts)")
