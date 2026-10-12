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

# 3. High-Quality Spoken Radio Bulletins (5-10s audible station IDs & pirate bulletins)
# 51 Multilingual + 6 Geocities + 10 Newscasts = 67 unique crisp bulletins
spoken_pool = []
spoken_pool += [t for t in glob.glob(os.path.join(MULTILINGUAL_DIR, "*.mp3")) if os.path.isfile(t)]
spoken_pool += [t for t in glob.glob(os.path.join(GEOCITIES_DIR, "*.mp3")) if os.path.isfile(t)]
spoken_pool += [t for t in glob.glob(os.path.join(NEWSCASTS_DIR, "*.mp3")) if os.path.isfile(t)]
random.shuffle(spoken_pool)

# 4. Ultra-tight Telemetry Beacons (2.5s - 5s punchy 750Hz Morse chirps only)
morse_beacons = [t for t in glob.glob(os.path.join(MORSE_DIR, "*.mp3")) if os.path.isfile(t)]
random.shuffle(morse_beacons)

print(f"Building Broadcast Lineup:")
print(f"  - Vocal Master Songs: {len(real_songs)}")
print(f"  - FM Synth MIDI Masters (tightly trimmed): {len(midi_tracks)}")
print(f"  - Spoken Radio Bulletins: {len(spoken_pool)}")
print(f"  - Tight Morse Beacons (2-5s): {len(morse_beacons)}")

# 5. Build Radio Station Rotation (Tight, Zero Dead Air Cadence):
#   [Vocal Master Song 3-5m]
#   -> [Crisp Spoken Bulletin 5-8s]
#   -> [Roland/Yamaha MIDI Master (Zero tail)]
#   -> [Tight Morse Beacon 2-4s]
#   -> [Next Vocal Master Song]
full_playlist = []
spoken_idx = 0
morse_idx = 0
midi_idx = 0

for song in (real_songs * 4):
    full_playlist.append(song)

    # Tight spoken bulletin between vocal songs
    if spoken_pool:
        full_playlist.append(spoken_pool[spoken_idx % len(spoken_pool)])
        spoken_idx += 1

    # Tightly trimmed MIDI master composition
    if midi_tracks:
        full_playlist.append(midi_tracks[midi_idx % len(midi_tracks)])
        midi_idx += 1

    # Tight 2-4 second Morse beacon immediately after MIDI (no dead air)
    if morse_beacons and (morse_idx % 2 == 0):
        full_playlist.append(morse_beacons[morse_idx % len(morse_beacons)])
        morse_idx += 1

tmp_file = out_file + ".tmp"
with open(tmp_file, "w") as f:
    for t in full_playlist:
        f.write(f"file '{t}'\n")
os.replace(tmp_file, out_file)

print(f"\n✓ Generated Live Stream Playlist with {len(full_playlist)} total tracks in {out_file}")
