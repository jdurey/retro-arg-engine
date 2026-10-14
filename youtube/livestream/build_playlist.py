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

# 3. Identify the most recently added song(s) in Downloads folder so the newest track plays first in Cycle 1
newest_songs = []
if os.path.exists(DOWNLOADS_DIR):
    dl_files = []
    for f in os.listdir(DOWNLOADS_DIR):
        p = os.path.join(DOWNLOADS_DIR, f)
        if os.path.isfile(p) and not f.startswith("."):
            dl_files.append((os.path.getmtime(p), f))
    dl_files.sort(reverse=True)
    if dl_files:
        latest_mtime, latest_fname = dl_files[0]
        from ingest_download_songs import slugify
        latest_slug = slugify(latest_fname)
        for s in all_songs:
            if os.path.basename(s) == latest_slug:
                newest_songs.append(s)
                break

# Read head of existing playlist.txt so rebuilding never immediately repeats the song that was just playing
previously_playing = []
if os.path.exists(out_file):
    try:
        with open(out_file, "r") as pf:
            for line in pf:
                m = re.search(r"file\s+'([^']+)'", line)
                if m and "radio_master_songs" in m.group(1):
                    previously_playing.append(m.group(1))
                    if len(previously_playing) >= 15:
                        break
    except Exception:
        pass

# Use dynamic system randomness (no static seed)
rng = random.Random()

# 4. Authentic 1980s Roland/Yamaha FM Synthesizer MIDI Masters (30 files)
midi_tracks = [t for t in glob.glob(os.path.join(MIDI_DIR, "*.mp3")) if os.path.isfile(t)]
rng.shuffle(midi_tracks)

# 5. Spoken Radio Bulletins, Newscasts & Marine Advisories (69 files)
spoken_pool = []
spoken_pool += [t for t in glob.glob(os.path.join(MULTILINGUAL_DIR, "*.mp3")) if os.path.isfile(t)]
spoken_pool += [t for t in glob.glob(os.path.join(GEOCITIES_DIR, "*.mp3")) if os.path.isfile(t)]
spoken_pool += [t for t in glob.glob(os.path.join(NEWSCASTS_DIR, "*.mp3")) if os.path.isfile(t)]
rng.shuffle(spoken_pool)

# 6. Ultra-tight Telemetry Beacons (35 files, 2.5s - 5s punchy 750Hz Morse chirps)
morse_beacons = [t for t in glob.glob(os.path.join(MORSE_DIR, "*.mp3")) if os.path.isfile(t)]
rng.shuffle(morse_beacons)

# 7. Shortwave Numbers Station Intercepts (60 files, 20s - 35s phonetic codes)
numbers_pool = [t for t in glob.glob(os.path.join(NUMBERS_DIR, "*.mp3")) if os.path.isfile(t)]
rng.shuffle(numbers_pool)

# 8. Classified Orion Lab Tapes (25 files, Marcus Hale dictaphone, Harrison purge logs)
lab_pool = [t for t in glob.glob(os.path.join(LAB_DIR, "*.mp3")) if os.path.isfile(t)]
rng.shuffle(lab_pool)

# 9. Deep Rabbit Hole ARG Intercepts & UVB-76 Buzzer Bursts (12 files)
intercept_pool = [t for t in glob.glob(os.path.join(INTERCEPT_DIR, "*.mp3")) if os.path.isfile(t)]
rng.shuffle(intercept_pool)

print(f"Building Broadcast Lineup:")
print(f"  - Total Unique Vocal Master Songs: {len(all_songs)}")
print(f"  - FM Synth MIDI Masters: {len(midi_tracks)}")
print(f"  - Spoken Radio Bulletins: {len(spoken_pool)}")
print(f"  - Tight Morse Beacons: {len(morse_beacons)}")
print(f"  - Shortwave Numbers Stations: {len(numbers_pool)}")
print(f"  - Classified Orion Lab Tapes: {len(lab_pool)}")
print(f"  - Deep ARG Signal Intercepts: {len(intercept_pool)}")

# 10. Helper to generate a well-spaced single cycle containing every song exactly once
def build_shuffled_cycle(song_list, avoid_recent=None, pin_first=None):
    if avoid_recent is None:
        avoid_recent = []
    if pin_first is None:
        pin_first = []
    avoid_roots = {get_base_root(s) for s in avoid_recent if s not in pin_first}
    remaining_pool = [s for s in song_list if s not in pin_first]
    
    for attempt in range(500):
        cand_rest = list(remaining_pool)
        rng.shuffle(cand_rest)
        cand = list(pin_first) + cand_rest
        
        # Ensure the opening of this cycle (after pinned new tracks) does not repeat the end of the previous cycle
        check_slice = cand[len(pin_first):len(pin_first) + min(len(cand_rest), len(avoid_recent))]
        if any(get_base_root(s) in avoid_roots for s in check_slice):
            continue
            
        # Verify internal spacing between any duplicate roots (e.g. movements)
        valid = True
        recent = []
        for s in cand:
            r = get_base_root(s)
            if r in recent[-20:]:  # At least 20 songs between similar roots
                valid = False
                break
            recent.append(r)
        if valid:
            return cand
    return list(pin_first) + remaining_pool

# 11. Build 8 distinct cycles (~45 hours of non-repeating fair rotation)
# Every song in the catalog appears EXACTLY ONCE per cycle (~5.6 hours apart)
NUM_CYCLES = 8
cycles = []
last_tail = previously_playing

for c_num in range(NUM_CYCLES):
    pin = newest_songs if c_num == 0 else []
    next_cycle = build_shuffled_cycle(all_songs, avoid_recent=last_tail, pin_first=pin)
    cycles.append(next_cycle)
    last_tail = next_cycle[-30:]  # Protect the last 30 songs from appearing in the start of next cycle

# Combine all cycles into ordered songs list
ordered_songs = []
for c in cycles:
    ordered_songs.extend(c)

# 12. Dynamic Transition Engine:
# Alternates between 6 authentic radio interstitial cadences so transitions never feel robotic
CADENCE_PATTERNS = [
    "bulletin",       # MIDI Stinger + Radio Bulletin / Newscast
    "numbers",        # Morse Beacon + Shortwave Numbers Station
    "direct_morse",   # Quick Morse chirp straight into next song (keeps energy up)
    "lab_tape",       # Classified Orion Dictaphone / Marcus Hale tape + Morse
    "bulletin",       # MIDI Stinger + Marine Advisory / Foreign Radio Dispatch
    "arg_intercept",  # UVB-76 Buzzer / Deep Shortwave Intercept
    "direct_midi",    # Vintage 3.5s FM Synth Stinger direct segue
    "numbers",        # Shortwave Numbers Station
    "lab_tape",       # Classified Lab Tape
    "bulletin",       # MIDI Stinger + GeoCities Reading / Community Bulletin
]

full_playlist = []
spoken_idx = 0
morse_idx = 0
midi_idx = 0
numbers_idx = 0
lab_idx = 0
intercept_idx = 0

for song_idx, song in enumerate(ordered_songs):
    full_playlist.append(song)
    
    # Pick next transition pattern
    pattern = CADENCE_PATTERNS[song_idx % len(CADENCE_PATTERNS)]
    
    if pattern == "bulletin":
        # 3.5s MIDI Stinger -> Spoken Bulletin
        if midi_tracks:
            full_playlist.append(midi_tracks[midi_idx % len(midi_tracks)])
            midi_idx += 1
        if spoken_pool:
            full_playlist.append(spoken_pool[spoken_idx % len(spoken_pool)])
            spoken_idx += 1
            
    elif pattern == "numbers":
        # Morse Beacon -> Numbers Station
        if morse_beacons and (song_idx % 2 == 0):
            full_playlist.append(morse_beacons[morse_idx % len(morse_beacons)])
            morse_idx += 1
        if numbers_pool:
            full_playlist.append(numbers_pool[numbers_idx % len(numbers_pool)])
            numbers_idx += 1
            
    elif pattern == "lab_tape":
        # Classified Orion Tape -> Tight Morse chirp
        if lab_pool:
            full_playlist.append(lab_pool[lab_idx % len(lab_pool)])
            lab_idx += 1
        if morse_beacons:
            full_playlist.append(morse_beacons[morse_idx % len(morse_beacons)])
            morse_idx += 1
            
    elif pattern == "arg_intercept":
        # Deep ARG Intercept / UVB-76 Buzzer
        if intercept_pool:
            full_playlist.append(intercept_pool[intercept_idx % len(intercept_pool)])
            intercept_idx += 1
            
    elif pattern == "direct_morse":
        # Punchy 2-4 second Morse beacon direct segue
        if morse_beacons:
            full_playlist.append(morse_beacons[morse_idx % len(morse_beacons)])
            morse_idx += 1
            
    elif pattern == "direct_midi":
        # Vintage FM Synth Stinger direct segue
        if midi_tracks:
            full_playlist.append(midi_tracks[midi_idx % len(midi_tracks)])
            midi_idx += 1

tmp_file = out_file + ".tmp"
with open(tmp_file, "w") as f:
    for t in full_playlist:
        f.write(f"file '{t}'\n")
os.replace(tmp_file, out_file)

fresh_marker = os.path.join(HERE, ".playlist_fresh")
with open(fresh_marker, "w") as fm:
    fm.write(str(time.time()))

print(f"\n✓ Generated Dynamic Live Stream Playlist with {len(full_playlist)} total tracks ({len(ordered_songs)} songs across {NUM_CYCLES} cycles) in {out_file}")
if newest_songs:
    print(f"✓ Pinned newest ingested track at #1: {os.path.basename(newest_songs[0])}")
print(f"✓ Every song in the {len(all_songs)}-track catalog appears exactly once per cycle (~5.6 hours apart)!")
print(f"✓ Interstitial diversity: Numbers Stations, Classified Lab Tapes, ARG Intercepts, Bulletins, Morse Beacons, and MIDI Stingers all actively rotating!")

