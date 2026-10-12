#!/usr/bin/env python3
"""Builds an infinite looping audio playlist for the 24/7 YouTube live stream.
Interweaves 300+ unique tracks with ZERO dead space:
- 53 Authentic Nova Hart Vocal Master Songs (including the 5 new master tracks from Downloads)
- 30 Authentic 1980s Roland & Yamaha FM Synth MIDI Master Compositions
- 51 Multilingual 1980s Radio Bulletins & Marine Advisories (18 languages)
- 25 Classified Orion Lab Tapes (Marcus Hale Dictaphone, Harrison Purge Logs, Empathy Trials)
- 35 Punchy 750 Hz Morse Code Telemetry Beacons (2.5s - 6.5s)
- 60 Procedural Shortwave Numbers Station Intercepts (7 languages)
- 12 Deep Rabbit Hole ARG Intercepts & UVB-76 Buzzer Bursts
"""

import os
import glob
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(HERE, "broadcast_archive")

REAL_SONGS_DIR = os.path.join(ARCHIVE_DIR, "radio_master_songs")
MIDI_DIR = os.path.join(ARCHIVE_DIR, "midi_masters")
MULTILINGUAL_DIR = os.path.join(ARCHIVE_DIR, "multilingual_bulletins")
LAB_DIR = os.path.join(ARCHIVE_DIR, "classified_lab_tapes")
MORSE_DIR = os.path.join(ARCHIVE_DIR, "morse_beacons")
NUMBERS_DIR = os.path.join(ARCHIVE_DIR, "numbers_stations")
NEWSCASTS_DIR = os.path.join(ARCHIVE_DIR, "newscasts")
GEOCITIES_DIR = os.path.join(ARCHIVE_DIR, "geocities_readings")
INTERCEPT_DIR = os.path.join(HERE, "intercepts")

from ingest_download_songs import ingest_all

# Ingest any new tracks added to Downloads/For Live Stream before building playlist
ingest_all()

out_file = os.path.join(HERE, "playlist.txt")

# 1. Real Nova Hart Master Songs (Vocal Studio Tracks, Rock, Synth & Tokyo Tapes)
real_songs = [t for t in glob.glob(os.path.join(REAL_SONGS_DIR, "*.mp3")) if os.path.isfile(t)]
random.seed(19850909)
random.shuffle(real_songs)

# 2. Authentic 1980s Roland/Yamaha FM Synthesizer MIDI Masters (30 procedural compositions)
midi_tracks = [t for t in glob.glob(os.path.join(MIDI_DIR, "*.mp3")) if os.path.isfile(t)]
random.shuffle(midi_tracks)

# 3. Spoken Radio Bulletins Pool (Heavily weighted towards the 51 Multilingual Bulletins + Lab Tapes)
# 51 Multilingual + 25 Lab Tapes + 6 Geocities + 10 Newscasts = 92 unique spoken broadcasts
spoken_pool = []
spoken_pool += [t for t in glob.glob(os.path.join(MULTILINGUAL_DIR, "*.mp3")) if os.path.isfile(t)]
spoken_pool += [t for t in glob.glob(os.path.join(LAB_DIR, "*.mp3")) if os.path.isfile(t)]
spoken_pool += [t for t in glob.glob(os.path.join(GEOCITIES_DIR, "*.mp3")) if os.path.isfile(t)]
spoken_pool += [t for t in glob.glob(os.path.join(NEWSCASTS_DIR, "*.mp3")) if os.path.isfile(t)]
random.shuffle(spoken_pool)

# 4. Telemetry & Cryptographic Signals Pool (Punchy Morse, Numbers Stations, Rabbit Holes)
# 35 Morse (2.5s-6.5s) + 60 Numbers Stations + 12 Intercepts = 107 unique telemetry bursts
signal_pool = []
signal_pool += [t for t in glob.glob(os.path.join(MORSE_DIR, "*.mp3")) if os.path.isfile(t)]
signal_pool += [t for t in glob.glob(os.path.join(NUMBERS_DIR, "*.mp3")) if os.path.isfile(t)]
signal_pool += [t for t in glob.glob(os.path.join(INTERCEPT_DIR, "*.mp3")) if os.path.isfile(t)]
random.shuffle(signal_pool)

print(f"Building Broadcast Lineup:")
print(f"  - Vocal Master Songs: {len(real_songs)}")
print(f"  - FM Synth MIDI Masters: {len(midi_tracks)}")
print(f"  - Spoken Radio Bulletins (18 languages): {len(spoken_pool)}")
print(f"  - Signal & Telemetry Bursts: {len(signal_pool)}")

# 5. Build Radio Station Rotation:
# Cadence:
#   [Vocal Master Song 3-5m]
#   -> [Spoken Radio Bulletin: 6-10s (Multilingual/Lab Tape)]
#   -> [Roland/Yamaha MIDI Master 45-80s]
#   -> [Signal Telemetry Burst: 3-6s (Morse/Numbers Station)]
#   -> [Vocal Master Song 3-5m]
#   ...
full_playlist = []
spoken_idx = 0
signal_idx = 0
midi_idx = 0

# Loop 4 full passes across the real song catalog (~16 hours of continuous unrepeated sequence)
for song in (real_songs * 4):
    full_playlist.append(song)

    # 1 tight spoken bulletin after vocal song
    if spoken_pool:
        full_playlist.append(spoken_pool[spoken_idx % len(spoken_pool)])
        spoken_idx += 1

    # 1 retro Roland/Yamaha MIDI master composition
    if midi_tracks:
        full_playlist.append(midi_tracks[midi_idx % len(midi_tracks)])
        midi_idx += 1

    # 1 tight signal burst / telemetry beacon after MIDI track
    if signal_pool:
        full_playlist.append(signal_pool[signal_idx % len(signal_pool)])
        signal_idx += 1

with open(out_file, "w") as f:
    for t in full_playlist:
        f.write(f"file '{t}'\n")

print(f"\n✓ Generated Live Stream Playlist with {len(full_playlist)} total tracks in {out_file}")
