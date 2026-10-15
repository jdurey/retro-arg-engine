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
    b = b.replace('’', '_').replace("'", "_")
    b = re.sub(r'^(?:\d+[a-z]?_|b_|nh_|nova_chan_|nova_hart_)', '', b)
    b = re.sub(r'\.mp3$', '', b)
    b = re.sub(
        r'(_19\d\d.*|_80s.*|_old|_1|_\(the_upload\)|_remastered|_v\d+|_es|_kr|_the_dead_hand|_marcus_and_nova_duet.*|_bonus_track|_final.*|_reconstruction|_retro|_master|_live|_cover|_edit|_raw|_duet|_instrumental|_vocals|_nova_chan|_crystal_promise|_archival_demo|_marcus_song)$',
        '',
        b,
    )
    b = re.sub(r'[^a-z0-9]', '', b)
    return b

# 2. Collect all unique master vocal songs (excluding removed items and duplicates)
EXCLUDED_SONGS = {
    "radio_two_voices.mp3",
    "radio_synthetic_dawn_retro.mp3",
    "radio_end_like_that.mp3",
    "radio_tape_of_us_1989_rough_mix.mp3",
    "radio_the_second_voice_1.mp3",
    "radio_echoes_of_tomorrow_80s_hard_rock_remix.mp3",
    "radio_faint_residual_(the_upload).mp3",
    "radio_11_ghost_transit.mp3",
    "radio_memory_hatch_reconstruction.mp3",
    "radio_03_only_we_remain_1989_tokyo_master.mp3",
    "radio_someone_else_s_memories_old.mp3",
    "radio_the_world_moves_without_me_old.mp3",
    "radio_nh_synthetic_dawn_1985_synth_original_mix.mp3",
    "radio_abandoned_shell_es.mp3",
    "radio_asset_loss_kr.mp3",
    "radio_03_corridor_dreams.mp3",
}
raw_songs = sorted(
    t for t in glob.glob(os.path.join(REAL_SONGS_DIR, "*.mp3"))
    if os.path.isfile(t)
    and os.path.basename(t) not in EXCLUDED_SONGS
    and os.path.getsize(t) > 50000  # Ignore 50ms bridge stubs
)
all_songs = []
seen_roots = set()
for s in raw_songs:
    root = get_base_root(s)
    if root not in seen_roots:
        seen_roots.add(root)
        all_songs.append(s)

if not all_songs:
    raise RuntimeError(f"No songs found in {REAL_SONGS_DIR}!")

# Read the first 35 songs of existing playlist.txt (roughly the last 2.5 hours of playback)
# so rebuilding NEVER repeats songs that were just playing!
previously_playing = []
if os.path.exists(out_file):
    try:
        with open(out_file, "r") as pf:
            for line in pf:
                m = re.search(r"file\s+'([^']+)'", line)
                if m and "radio_master_songs" in m.group(1):
                    previously_playing.append(m.group(1))
                    if len(previously_playing) >= 35:
                        break
    except Exception:
        pass

# Use dynamic system randomness (no static seed)
rng = random.Random()

# Identify recently ingested tracks (added in the last 6 hours) to mix into the opening rotation
now_ts = time.time()
freshly_ingested = [s for s in all_songs if (now_ts - os.path.getmtime(s)) < 21600]
rng.shuffle(freshly_ingested)

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
print(f"  - Total Unique Vocal Master Songs: {len(all_songs)} ({len(freshly_ingested)} newly added from Drive)")
print(f"  - FM Synth MIDI Masters: {len(midi_tracks)}")
print(f"  - Spoken Radio Bulletins: {len(spoken_pool)}")
print(f"  - Tight Morse Beacons: {len(morse_beacons)}")
print(f"  - Shortwave Numbers Stations: {len(numbers_pool)}")
print(f"  - Classified Orion Lab Tapes: {len(lab_pool)}")
print(f"  - Deep ARG Signal Intercepts: {len(intercept_pool)}")

# 10. Helper to generate a well-spaced single cycle across the entire catalog
def build_shuffled_cycle(song_list, avoid_recent=None, front_pool=None):
    if avoid_recent is None:
        avoid_recent = []
    if front_pool is None:
        front_pool = []
    avoid_roots = {get_base_root(s) for s in avoid_recent[-35:]}
    front_set = set(front_pool)

    def make_candidate():
        if front_pool:
            f_copy = list(front_pool)
            rest_unplayed = [s for s in song_list if s not in front_set and get_base_root(s) not in avoid_roots]
            rest_played = [s for s in song_list if s not in front_set and get_base_root(s) in avoid_roots]
            rng.shuffle(f_copy)
            rng.shuffle(rest_unplayed)
            rng.shuffle(rest_played)
            # Interleave newly added Google Drive tracks (2 new : 1 unplayed classic) at the front,
            # pushing any recently heard songs to the very end of the cycle (6+ hours later)
            cand = []
            fi, ui = 0, 0
            while fi < len(f_copy) or ui < len(rest_unplayed):
                if fi < len(f_copy):
                    cand.append(f_copy[fi])
                    fi += 1
                if fi < len(f_copy):
                    cand.append(f_copy[fi])
                    fi += 1
                if ui < len(rest_unplayed):
                    cand.append(rest_unplayed[ui])
                    ui += 1
            cand.extend(rest_played)
            return cand
        else:
            pool_copy = list(song_list)
            rng.shuffle(pool_copy)
            return pool_copy

    best_cand = None
    best_score = -999999
    for attempt in range(400):
        cand = make_candidate()
        score = 0
        # Penalize repeating end of previous cycle in the first 35 songs
        for s in cand[:35]:
            if get_base_root(s) in avoid_roots:
                score -= 60

        # Penalize similar roots being closer than 20 songs apart
        recent = []
        for s in cand:
            r = get_base_root(s)
            if r in recent[-20:]:
                score -= 25
            recent.append(r)

        if score == 0:
            return cand
        if score > best_score:
            best_score = score
            best_cand = cand
    return best_cand if best_cand is not None else make_candidate()

# 11. Build 8 distinct cycles (~68+ hours of non-repeating fair rotation)
# Every song in the catalog appears EXACTLY ONCE per cycle
NUM_CYCLES = 8
cycles = []
last_tail = previously_playing

for c_num in range(NUM_CYCLES):
    front = freshly_ingested if c_num == 0 else []
    next_cycle = build_shuffled_cycle(all_songs, avoid_recent=last_tail, front_pool=front)
    cycles.append(next_cycle)
    last_tail = next_cycle[-35:]  # Protect the last 35 songs from appearing in the start of next cycle

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
if ordered_songs:
    print(f"✓ Opening track #1: {os.path.basename(ordered_songs[0])}")
print(f"✓ Every song in the {len(all_songs)}-track catalog appears exactly once per cycle (~{len(all_songs)*4/60:.1f} hours apart)!")
print(f"✓ Interstitial diversity: Numbers Stations, Classified Lab Tapes, ARG Intercepts, Bulletins, Morse Beacons, and MIDI Stingers all actively rotating!")

