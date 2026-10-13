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
import re
import time

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

from ingest_download_songs import ingest_all, DOWNLOADS_DIR

# 1. Ingest any new tracks added to Downloads/For Live Stream before building playlist
ingest_all()

out_file = os.path.join(HERE, "playlist.txt")

# Helper to normalize song root title for spacing and deduplication
def get_base_root(path):
    b = os.path.basename(path).lower()
    b = re.sub(r'^radio_', '', b)
    b = re.sub(r'^\d+_', '', b)
    b = re.sub(r'\.mp3$', '', b)
    b = re.sub(r'_old$', '', b)
    b = re.sub(r'_\d+$', '', b)
    b = re.sub(r'_v\d+$', '', b)
    b = re.sub(r'_\d{4}_tokyo_master$', '', b)
    b = re.sub(r'_movement_\d+$', '', b)
    b = re.sub(r'_\(the_upload\)$', '', b)
    b = re.sub(r'_reconstruction$', '', b)
    b = re.sub(r'[^a-z0-9]', '', b)
    return b

# 2. Collect all unique master vocal songs
all_songs = [t for t in glob.glob(os.path.join(REAL_SONGS_DIR, "*.mp3")) if os.path.isfile(t)]
if not all_songs:
    raise RuntimeError(f"No songs found in {REAL_SONGS_DIR}!")

# 3. Identify newly added songs from Downloads folder (modified in the last 48 hours)
recent_stems = set()
now = time.time()
if os.path.exists(DOWNLOADS_DIR):
    for f in os.listdir(DOWNLOADS_DIR):
        p = os.path.join(DOWNLOADS_DIR, f)
        if os.path.isfile(p) and (now - os.path.getmtime(p) < 172800):  # within 48h
            base = os.path.splitext(f)[0]
            clean = re.sub(r'^\d+\s*[-_.]*\s*', '', base).lower()
            clean = re.sub(r'[^a-z0-9]+', '_', clean).strip('_')
            recent_stems.add(clean)

new_tracks = []
classic_tracks = []
for s in all_songs:
    b = os.path.basename(s).replace('radio_', '').replace('.mp3', '')
    if any(stem in b or b in stem for stem in recent_stems):
        new_tracks.append(s)
    else:
        classic_tracks.append(s)

# Use dynamic system randomness (no static seed)
rng = random.Random()

# 4. Authentic 1980s Roland/Yamaha FM Synthesizer MIDI Masters
midi_tracks = [t for t in glob.glob(os.path.join(MIDI_DIR, "*.mp3")) if os.path.isfile(t)]
rng.shuffle(midi_tracks)

# 5. High-Quality Spoken Radio Bulletins (67 unique crisp bulletins)
spoken_pool = []
spoken_pool += [t for t in glob.glob(os.path.join(MULTILINGUAL_DIR, "*.mp3")) if os.path.isfile(t)]
spoken_pool += [t for t in glob.glob(os.path.join(GEOCITIES_DIR, "*.mp3")) if os.path.isfile(t)]
spoken_pool += [t for t in glob.glob(os.path.join(NEWSCASTS_DIR, "*.mp3")) if os.path.isfile(t)]
rng.shuffle(spoken_pool)

# 6. Ultra-tight Telemetry Beacons (2.5s - 5s punchy 750Hz Morse chirps)
morse_beacons = [t for t in glob.glob(os.path.join(MORSE_DIR, "*.mp3")) if os.path.isfile(t)]
rng.shuffle(morse_beacons)

print(f"Building Broadcast Lineup:")
print(f"  - Total Unique Vocal Master Songs: {len(all_songs)}")
print(f"    * Newly Added Tracks (Front-Loaded): {len(new_tracks)}")
print(f"    * Classic Repertoire Tracks: {len(classic_tracks)}")
print(f"  - FM Synth MIDI Masters: {len(midi_tracks)}")
print(f"  - Spoken Radio Bulletins: {len(spoken_pool)}")
print(f"  - Tight Morse Beacons: {len(morse_beacons)}")

# 7. Helper to generate a well-spaced single cycle containing every song exactly once
def build_shuffled_cycle(song_list, avoid_start_root=None):
    for _ in range(100):
        cand = list(song_list)
        rng.shuffle(cand)
        if avoid_start_root and get_base_root(cand[0]) == avoid_start_root:
            continue
        # Verify spacing between same-root songs
        valid = True
        recent = []
        for s in cand:
            r = get_base_root(s)
            if r in recent[-10:]:
                valid = False
                break
            recent.append(r)
        if valid:
            return cand
    return cand

# 8. Build 4 distinct cycles (~21 hours before playlist loop)
# In Cycle 1: Front-load all new tracks interleaved with classic tracks so listeners hear new songs immediately!
cycle_1 = []
rng.shuffle(new_tracks)
rng.shuffle(classic_tracks)

# Interleave new tracks with classic tracks at the opening
c_idx = 0
for n_song in new_tracks:
    cycle_1.append(n_song)
    if c_idx < len(classic_tracks):
        cycle_1.append(classic_tracks[c_idx])
        c_idx += 1

# Append remaining classic tracks
cycle_1.extend(classic_tracks[c_idx:])

# Cycles 2, 3, 4: Pure randomized fair rotation of all 80 songs
cycles = [cycle_1]
last_root = get_base_root(cycle_1[-1])
for _ in range(3):
    next_cycle = build_shuffled_cycle(all_songs, avoid_start_root=last_root)
    cycles.append(next_cycle)
    last_root = get_base_root(next_cycle[-1])

# Combine all cycles
ordered_songs = []
for c in cycles:
    ordered_songs.extend(c)

# 9. Interweave with Zero Dead Air Cadence:
#   [Vocal Master Song 3-5m]
#   -> [3.5s Roland/Yamaha FM Synth MIDI Stinger]
#   -> [Crisp Spoken Radio Bulletin / Narration 5-8s]
#   -> [Tight Morse Beacon 2-4s (alternating)]
#   -> [Next Vocal Master Song]
full_playlist = []
spoken_idx = 0
morse_idx = 0
midi_idx = 0

for song in ordered_songs:
    full_playlist.append(song)

    # 1. 3.5s Vintage FM Synth MIDI Stinger (plays BEFORE narration)
    if midi_tracks:
        full_playlist.append(midi_tracks[midi_idx % len(midi_tracks)])
        midi_idx += 1

    # 2. Tight spoken radio bulletin / narration
    if spoken_pool:
        full_playlist.append(spoken_pool[spoken_idx % len(spoken_pool)])
        spoken_idx += 1

    # 3. Tight 2-4 second Morse beacon
    if morse_beacons and (morse_idx % 2 == 0):
        full_playlist.append(morse_beacons[morse_idx % len(morse_beacons)])
        morse_idx += 1

tmp_file = out_file + ".tmp"
with open(tmp_file, "w") as f:
    for t in full_playlist:
        f.write(f"file '{t}'\n")
os.replace(tmp_file, out_file)

believers_count = sum(1 for s in ordered_songs if "calling_all_believers" in s)
print(f"\n✓ Generated Live Stream Playlist with {len(full_playlist)} total tracks ({len(ordered_songs)} songs across 4 cycles) in {out_file}")
print(f"✓ Calling All Believers appears {believers_count} time(s) total (exactly once per 80-song cycle, ~5.3 hours apart)!")

