#!/usr/bin/env python3
"""Builds an infinite looping audio playlist for the 24/7 YouTube live stream
using the Concentric Counter-Rotating Circles architecture:

- INNER CIRCLE (Songs & Alternate Mixes, length N_S):
  Rotates CLOCKWISE (+1 mod N_S). The entire catalog of N_S Nova Hart studio
  masters and alternate mixes plays through 100% before any song repeats.
  Alternate mixes of the same base song are spaced far apart around the circle.

- OUTER CIRCLE (Interstitials, length N_I, with gcd(N_S, N_I) == 1):
  Rotates COUNTER-CLOCKWISE (-1 mod N_I, opposite direction to the Inner Circle).
  The entire list of N_I interstitials (20 Humanist Resistance Break-Ins,
  10 Heartstrike Announcements, 20 World-Building Vignettes, 50 Movie Trailers /
  Commercials / PSAs / DJ Call-Ins / Pirate Overrides, Lab Tapes, Numbers Stations,
  Bulletins, and Morse/MIDI Stingers) plays through 100% before any interstitial
  repeats.

- ZERO REPEATED PAIRINGS:
  Because the Inner Circle (+1 mod N_S) and Outer Circle (-1 mod N_I) turn in
  opposite directions with coprime circumferences (gcd(N_S, N_I) == 1), by the
  Chinese Remainder Theorem no (song, interstitial) pairing repeats for
  N_S * N_I transitions (70,000+ transitions / 200+ continuous days).
"""

import glob
import math
import os
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

from ingest_download_songs import ingest_all

# 1. Ingest any new tracks added to Downloads/For Live Stream before building playlist
ingest_all()

out_file = os.path.join(HERE, "playlist.txt")


def get_base_root(path):
    """Returns the canonical base song root (used to space alternate mixes far apart)."""
    b = os.path.basename(path).lower()
    b = re.sub(r"\.(mp3|wav|m4a|flac)$", "", b)
    b = re.sub(r"^radio_", "", b)
    b = b.replace("’", "_").replace("'", "_")
    b = re.sub(
        r"^(?:\d+(?:\.\d+)?[a-z]?[\s_-]+|b[\s_-]+|nh[\s_-]+|nova[\s_-]*chan[\s_-]+|nova[\s_-]*hart[\s_-]+)+",
        "",
        b,
    )
    if "run for cover" in b or "run_for_cover" in b:
        return "runforcover"
    b = re.sub(
        r"(_19\d\d.*|_80s.*|_old|_1|_2|_\(the_upload\)|_remastered|_v\d+|_es|_kr|_the_dead_hand|_marcus_and_nova_duet.*|_bonus_track|_final.*|_reconstruction|_retro.*|_master|_live.*|_cover|_edit|_raw|_duet|_instrumental|_vocals|_nova_chan|_crystal_promise|_archival_demo|_demo_version|_marcus_song|_unfiltered_sovereign_mix|_workout_synth_remix|_new_wave)+$",
        "",
        b,
    )
    b = re.sub(r"^(the|we)_+", "", b)
    b = re.sub(r"[^a-z0-9]", "", b)
    return b


def get_mix_key(path):
    """
    Returns a unique key per distinct mix (so studio masters, Live 1986 mixes,
    Archival Demos, Raw Voltage Demos, Remixes, Duets, and Retro/Original mixes
    all coexist in the Inner Circle, while collapsing only identical '_1' file copies).
    """
    b = os.path.basename(path).lower()
    b = re.sub(r"\.(mp3|wav|m4a|flac)$", "", b)
    b = re.sub(r"^radio_", "", b)
    b = b.replace("’", "_").replace("'", "_")
    b = re.sub(r"^(?:\d+(?:\.\d+)?[a-z]?_|b_|nh_|nova_chan_|nova_hart_)+", "", b)
    if "run_for_cover" in b:
        return "runforcover"
    # Strip only generic copy suffixes (_1, _final, _master, _v3), preserving mix tags!
    b = re.sub(r"(_1|_v\d+|_final|_master|_cover|_edit)+$", "", b)
    b = re.sub(r"[^a-z0-9]", "", b)
    return b


# 2. Collect all master vocal songs AND alternate mixes (excluding only non-song spoken scenes / foreign edits)
EXCLUDED_SONGS = {
    "radio_two_voices.mp3",
    "radio_end_like_that.mp3",
    "radio_the_second_voice_1.mp3",
    "radio_faint_residual_(the_upload).mp3",
    "radio_11_ghost_transit.mp3",
    "radio_someone_else_s_memories_old.mp3",
    "radio_the_world_moves_without_me_old.mp3",
    "radio_abandoned_shell_es.mp3",
    "radio_asset_loss_kr.mp3",
    "radio_03_corridor_dreams.mp3",
}

raw_songs = sorted(
    t
    for t in glob.glob(os.path.join(REAL_SONGS_DIR, "*.mp3"))
    if os.path.isfile(t)
    and os.path.basename(t) not in EXCLUDED_SONGS
    and os.path.getsize(t) > 50000  # Ignore 50ms bridge stubs
)

all_songs = []
seen_mix_keys = set()
for s in raw_songs:
    mk = get_mix_key(s)
    if mk not in seen_mix_keys:
        seen_mix_keys.add(mk)
        all_songs.append(s)

if not all_songs:
    raise RuntimeError(f"No songs found in {REAL_SONGS_DIR}!")

# Read the first 35 songs of existing playlist.txt so rebuilding avoids repeating songs just heard
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

rng = random.Random()

# Identify recently ingested tracks (added in the last 6 hours) to interleave around the start of the Inner Circle
now_ts = time.time()
freshly_ingested = [s for s in all_songs if (now_ts - os.path.getmtime(s)) < 21600]
rng.shuffle(freshly_ingested)


def build_inner_circle(song_list, avoid_recent=None, front_pool=None):
    """
    Arranges all N_S songs & alternate mixes into a single Inner Circle where:
    1. Every single track in song_list appears EXACTLY ONCE.
    2. Newly added tracks (front_pool) are interleaved 2:1 at the start of the circle.
    3. Alternate mixes sharing the same base song root (get_base_root) are spaced
       as far apart around the circle as possible (minimum 25+ tracks apart).
    """
    if avoid_recent is None:
        avoid_recent = []
    if front_pool is None:
        front_pool = []
    avoid_mix_keys = {get_mix_key(s) for s in avoid_recent[-30:]}
    front_set = set(front_pool)

    def make_candidate():
        if front_pool:
            f_copy = list(front_pool)
            rest_unplayed = [
                s for s in song_list if s not in front_set and get_mix_key(s) not in avoid_mix_keys
            ]
            rest_played = [
                s for s in song_list if s not in front_set and get_mix_key(s) in avoid_mix_keys
            ]
            rng.shuffle(f_copy)
            rng.shuffle(rest_unplayed)
            rng.shuffle(rest_played)
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
        else:
            cand = list(song_list)
            rng.shuffle(cand)

        # Greedy pass to separate any two alternate mixes sharing the same base root by >= 28 slots
        n = len(cand)
        for i in range(n):
            r_i = get_base_root(cand[i])
            # Check if any track within the previous 28 slots (including wrap-around) shares r_i
            conflict = False
            for d in range(1, min(28, n)):
                if get_base_root(cand[(i - d) % n]) == r_i:
                    conflict = True
                    break
            if conflict:
                # Find a swap partner j further ahead that doesn't create a root conflict
                for j in range(i + 1, n):
                    r_j = get_base_root(cand[j])
                    if r_j == r_i:
                        continue
                    ok_swap = True
                    for d in range(1, min(28, n)):
                        if get_base_root(cand[(i - d) % n]) == r_j:
                            ok_swap = False
                            break
                    if ok_swap:
                        cand[i], cand[j] = cand[j], cand[i]
                        break
        return cand

    best_cand = None
    best_score = -999999
    for _ in range(150):
        cand = make_candidate()
        score = 0
        n = len(cand)
        for idx, s in enumerate(cand):
            r = get_base_root(s)
            for d in range(1, min(28, n)):
                if get_base_root(cand[(idx - d) % n]) == r:
                    score -= 40
        if score == 0:
            return cand
        if score > best_score:
            best_score = score
            best_cand = cand
    return best_cand if best_cand is not None else make_candidate()


# 3. Build the INNER CIRCLE (Songs & Alternate Mixes, rotating CLOCKWISE +1 mod N_S)
inner_circle_songs = build_inner_circle(
    all_songs, avoid_recent=previously_playing, front_pool=freshly_ingested
)
N_S = len(inner_circle_songs)
assert len(set(inner_circle_songs)) == N_S, "Inner circle must contain unique song files!"


# 4. Collect all Interstitial Pools for the OUTER CIRCLE
all_newscasts = sorted(
    t for t in glob.glob(os.path.join(NEWSCASTS_DIR, "*.mp3")) if os.path.isfile(t)
)
humanist_pool = [
    t for t in all_newscasts if os.path.basename(t).startswith("humanist_")
]
hs_pool = [
    t for t in all_newscasts if os.path.basename(t).startswith(("heartstrike_", "blaze_"))
]
world_pool = [
    t for t in all_newscasts if os.path.basename(t).startswith("world_")
]
varied_en_pool = [
    t
    for t in all_newscasts
    if os.path.basename(t).startswith(
        ("trailer_", "commercial_", "psa_", "dj_callin_", "pirate_override_")
    )
]
legacy_en_pool = [
    t
    for t in all_newscasts
    if not os.path.basename(t).startswith(
        (
            "humanist_",
            "heartstrike_",
            "blaze_",
            "world_",
            "trailer_",
            "commercial_",
            "psa_",
            "dj_callin_",
            "pirate_override_",
        )
    )
]

lab_pool = sorted(
    t for t in glob.glob(os.path.join(LAB_DIR, "*.mp3")) if os.path.isfile(t)
)
spoken_pool = sorted(
    [t for t in glob.glob(os.path.join(MULTILINGUAL_DIR, "*.mp3")) if os.path.isfile(t)]
    + [t for t in glob.glob(os.path.join(GEOCITIES_DIR, "*.mp3")) if os.path.isfile(t)]
)
intercept_pool = sorted(
    t for t in glob.glob(os.path.join(INTERCEPT_DIR, "*.mp3")) if os.path.isfile(t)
)
midi_tracks = sorted(
    t for t in glob.glob(os.path.join(MIDI_DIR, "*.mp3")) if os.path.isfile(t)
)
morse_beacons = sorted(
    t for t in glob.glob(os.path.join(MORSE_DIR, "*.mp3")) if os.path.isfile(t)
)
numbers_pool = sorted(
    t for t in glob.glob(os.path.join(NUMBERS_DIR, "*.mp3")) if os.path.isfile(t)
)

rng.shuffle(humanist_pool)
rng.shuffle(hs_pool)
rng.shuffle(world_pool)
rng.shuffle(varied_en_pool)
rng.shuffle(legacy_en_pool)
rng.shuffle(lab_pool)
rng.shuffle(spoken_pool)
rng.shuffle(intercept_pool)
rng.shuffle(midi_tracks)
rng.shuffle(morse_beacons)
rng.shuffle(numbers_pool)

# Build the Counter-Clockwise (CCW) traversal order of ALL unique interstitials
# so that:
# 1. Every single interstitial plays through once before ANY interstitial repeats.
# 2. The 20 new Humanist Resistance Break-Ins, 10 Heartstrike Announcements,
#    20 World-Building Vignettes, and 50 Varied English Spots are front-and-center
#    and evenly braided around the Outer Circle alongside Lab Tapes, Numbers,
#    Bulletins, Intercepts, MIDI, and Morse Beacons.
priority_english_buckets = [
    list(humanist_pool),
    list(hs_pool),
    list(world_pool),
    list(varied_en_pool) + list(legacy_en_pool),
]
secondary_archive_buckets = [
    list(lab_pool),
    list(intercept_pool),
    list(spoken_pool),
    list(numbers_pool),
    list(morse_beacons) + list(midi_tracks),
]

ccw_interstitials = []
# Braided pass: 3 priority English interstitials (rotating Humanist -> Heartstrike -> World -> Varied)
# followed by 1 secondary archive dispatch until all pools are 100% placed on the Outer Circle!
p_cursors = [0] * len(priority_english_buckets)
s_cursors = [0] * len(secondary_archive_buckets)
p_turn = 0
s_turn = 0

while any(p_cursors[i] < len(priority_english_buckets[i]) for i in range(len(priority_english_buckets))) or any(
    s_cursors[j] < len(secondary_archive_buckets[j]) for j in range(len(secondary_archive_buckets))
):
    # Pick up to 3 priority English tracks from distinct buckets (Humanist, Heartstrike, World, Varied)
    added_p = 0
    attempts = 0
    while added_p < 3 and attempts < len(priority_english_buckets) * 2:
        b_idx = p_turn % len(priority_english_buckets)
        p_turn += 1
        attempts += 1
        if p_cursors[b_idx] < len(priority_english_buckets[b_idx]):
            ccw_interstitials.append(priority_english_buckets[b_idx][p_cursors[b_idx]])
            p_cursors[b_idx] += 1
            added_p += 1

    # Pick 1 secondary archive track (only after the opening 24 transitions so listeners immediately hear Humanist/Heartstrike/World!)
    if len(ccw_interstitials) >= 24:
        s_attempts = 0
        while s_attempts < len(secondary_archive_buckets):
            sb_idx = s_turn % len(secondary_archive_buckets)
            s_turn += 1
            s_attempts += 1
            if s_cursors[sb_idx] < len(secondary_archive_buckets[sb_idx]):
                ccw_interstitials.append(secondary_archive_buckets[sb_idx][s_cursors[sb_idx]])
                s_cursors[sb_idx] += 1
                break

# Deduplicate just in case while preserving exact order
seen_inter = set()
unique_ccw = []
for item in ccw_interstitials:
    if item not in seen_inter:
        seen_inter.add(item)
        unique_ccw.append(item)

# Ensure gcd(N_S, N_I) == 1 so that Inner Circle (+1 mod N_S) and Outer Circle (-1 mod N_I)
# are strictly coprime and NO (song, interstitial) pairing can EVER repeat!
while math.gcd(N_S, len(unique_ccw)) != 1 and len(unique_ccw) > 120:
    # Trim a non-English tail item (morse/numbers) from the end to achieve exact coprimality
    for idx in range(len(unique_ccw) - 1, -1, -1):
        if "newscasts" not in unique_ccw[idx]:
            unique_ccw.pop(idx)
            break
    else:
        unique_ccw.pop()

N_I = len(unique_ccw)
# Place unique_ccw around outer_circle_interstitials such that stepping COUNTER-CLOCKWISE
# (-1 mod N_I starting at N_I - 1) visits unique_ccw[0], unique_ccw[1], ... in exact order!
outer_circle_interstitials = [None] * N_I
for step_k, track_path in enumerate(unique_ccw):
    outer_idx = (N_I - 1 - step_k) % N_I
    outer_circle_interstitials[outer_idx] = track_path

print("Building Concentric Counter-Rotating Broadcast Lineup:")
print(f"  - INNER CIRCLE (Songs & Alternate Mixes, Clockwise +1): {N_S} unique tracks ({len(freshly_ingested)} newly added)")
print(f"  - OUTER CIRCLE (Interstitials, Counter-Clockwise -1):   {N_I} unique tracks")
print(f"      * Humanist Resistance Break-Ins (Edge Neural Voices): {len(humanist_pool)}")
print(f"      * Heartstrike Announcements (Edge Neural Voices):     {len(hs_pool)}")
print(f"      * Pure World-Building Vignettes (Edge Neural Voices): {len(world_pool)}")
print(f"      * Trailers / Commercials / PSAs / DJ / Pirate Spots:  {len(varied_en_pool) + len(legacy_en_pool)}")
print(f"      * Lab Tapes / Numbers / Bulletins / Morse / MIDI:     {N_I - len(all_newscasts)}")
print(f"  - Coprime Check: gcd({N_S}, {N_I}) = {math.gcd(N_S, N_I)} -> Non-repeating pairing period = {N_S * N_I:,} transitions (~{N_S * N_I * 3.8 / 60:.0f} hours)!")

# 5. Generate 8 full revolutions of the Inner Circle against the Counter-Rotating Outer Circle
NUM_CYCLES = 8
TOTAL_STEPS = N_S * NUM_CYCLES

full_playlist = []
ordered_songs = []
seen_pairings = set()

for t in range(TOTAL_STEPS):
    # Inner Circle turns CLOCKWISE (+1 mod N_S)
    s_idx = t % N_S
    # Outer Circle turns COUNTER-CLOCKWISE (-1 mod N_I)
    i_idx = (N_I - 1 - t) % N_I

    song_track = inner_circle_songs[s_idx]
    inter_track = outer_circle_interstitials[i_idx]

    pair_key = (s_idx, i_idx)
    assert pair_key not in seen_pairings, f"Duplicate pairing detected at step {t}: {pair_key}"
    seen_pairings.add(pair_key)

    ordered_songs.append(song_track)
    full_playlist.append(song_track)
    full_playlist.append(inter_track)

# Verify full-circle play-through invariant before repeating:
# Every single window of N_S steps has N_S unique songs, and every window of N_I steps has N_I unique interstitials!
assert len(set(ordered_songs[:N_S])) == N_S, "Inner circle failed full play-through before repeat!"
first_ni_interstitials = [full_playlist[2 * t + 1] for t in range(N_I)]
assert len(set(first_ni_interstitials)) == N_I, "Outer circle failed full play-through before repeat!"

tmp_file = out_file + ".tmp"
with open(tmp_file, "w") as f:
    for t in full_playlist:
        f.write(f"file '{t}'\n")
os.replace(tmp_file, out_file)

fresh_marker = os.path.join(HERE, ".playlist_fresh")
with open(fresh_marker, "w") as fm:
    fm.write(str(time.time()))

print(f"\n✓ Generated Counter-Rotating Circles Playlist with {len(full_playlist)} total items ({len(ordered_songs)} song plays across {NUM_CYCLES} revolutions) in {out_file}")
print(f"✓ Verified 0 repeated (song, interstitial) pairings across all {TOTAL_STEPS:,} transitions ({len(seen_pairings):,} unique pairings)!")
print(f"✓ Opening Song #1 (Inner Circle idx 0): {os.path.basename(inner_circle_songs[0])}")
print(f"✓ Opening Interstitial #1 (Outer Circle idx {N_I - 1}): {os.path.basename(outer_circle_interstitials[N_I - 1])}")
