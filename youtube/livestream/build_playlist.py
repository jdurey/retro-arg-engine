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
FM_SPOTS_DIR = os.path.join(ARCHIVE_DIR, "fm_80s_spots")
MIDI_DIR = os.path.join(ARCHIVE_DIR, "midi_masters")
MULTILINGUAL_DIR = os.path.join(ARCHIVE_DIR, "multilingual_bulletins")
LAB_DIR = os.path.join(ARCHIVE_DIR, "classified_lab_tapes")
MORSE_DIR = os.path.join(ARCHIVE_DIR, "morse_beacons")
NUMBERS_DIR = os.path.join(ARCHIVE_DIR, "numbers_stations")
NEWSCASTS_DIR = os.path.join(ARCHIVE_DIR, "newscasts")
GEOCITIES_DIR = os.path.join(ARCHIVE_DIR, "geocities_readings")
INTERCEPT_DIR = os.path.join(HERE, "intercepts")

from ingest_download_songs import ingest_all
import trojan_horse_radio_engine as thr

# 1. Ingest any new tracks & ensure all core 1986 FM Sweepers / Weather / Spots / Splices exist
ingest_all()
thr.ensure_core_fm_80s_spots()

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
        r"(_luna_revision|_hard_rock(?:_version)?|_arena_rock_mix|_synth_rock_mix|_19\d\d.*|_80s.*|_old|_1|_2|_\(the_upload\)|_remastered|_v\d+|_es|_kr|_jp|_fr|_pt|_de|_it|_zh|_the_dead_hand|_marcus_and_nova_duet.*|_bonus_track|_final.*|_reconstruction|_retro.*|_master|_live.*|_cover|_edit|_raw|_duet|_instrumental|_vocals|_nova_chan|_crystal_promise|_archival_demo|_demo_version|_marcus_song|_unfiltered_sovereign_mix|_workout_synth_remix|_new_wave)+$",
        "",
        b,
    )
    b = re.sub(r"^(the|we)_+", "", b)
    b = re.sub(r"[^a-z0-9]", "", b)
    _luna_renamed_roots = {
        "amberhorizon": "crimsonhorizon",
        "boldreaction": "coldreaction",
        "chainlinkkiss": "barbedwirekiss",
        "diamondinthequiet": "diamondinthedark",
        "holdthelinewithin": "holdthelineinside",
        "nightrunner": "nightfang",
        "steelandshine": "steelandskin",
        "override": "signaloverride",
        "theoverride": "signaloverride",
        "standhere": "belonghere",
        "westandhere": "belonghere",
        "weekendfestival": "midnightanimal",
        "fuocodentro": "stillbelievin",
        "salvesequienpueda": "runforcover",
    }
    return _luna_renamed_roots.get(b, b)


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


# 2. Collect all master vocal songs AND alternate mixes (excluding superseded copies + Heavy Metal cuts)
from excluded_radio_songs import EXCLUDED_RADIO_SONGS as EXCLUDED_SONGS

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

import sync_telemetry as _st
import song_lore_questions as _slq


_ARTIST_BUCKET_CACHE: dict[str, str] = {}


def get_artist_bucket(path: str) -> str:
    """Classifies each song as solo 'nova', 'luna' (N0VA H4RT), 'heartstrike', or 'fm_guest'."""
    if path in _ARTIST_BUCKET_CACHE:
        return _ARTIST_BUCKET_CACHE[path]
    bname = os.path.basename(path)
    stem = os.path.splitext(bname)[0]
    if "_luna_revision" in bname.lower():
        _ARTIST_BUCKET_CACHE[path] = "luna"
        return "luna"
    lore = _slq.SONG_LORE_CODEX.get(bname) or {}
    ct = {"filename": bname, "stem": stem, "display_title": _st.classify_track(path).get("display_title", "")}
    art, _, _ = _st._extract_80s_release_meta(ct, lore)
    art_u = art.upper()
    if "N0VA H4RT" in art_u or "L.U.N.A" in art_u:
        res = "luna"
    elif "HEARTSTRIKE" in art_u:
        res = "heartstrike"
    elif art_u != "NOVA HART":
        res = "fm_guest"
    else:
        res = "nova"
    _ARTIST_BUCKET_CACHE[path] = res
    return res


# Identify recently ingested solo NOVA HART tracks (never front-cluster N0VA H4RT or guest bands!)
now_ts = time.time()
freshly_ingested = [
    s for s in all_songs
    if (now_ts - os.path.getmtime(s)) < 21600 and get_artist_bucket(s) == "nova"
]
rng.shuffle(freshly_ingested)


def build_inner_circle(song_list, avoid_recent=None, front_pool=None):
    """
    Arranges all N_S songs & alternate mixes into a single Inner Circle where:
    1. Every single track in song_list appears EXACTLY ONCE.
    2. Non-solo-Nova-Hart artists (`N0VA H4RT`, `Heartstrike`, `80s FM` guest bands) are spread
       uniformly around the entire circle (~1 guest/alt track every 6-7 solo Nova Hart songs,
       with Heartstrike & 80s FM bands interleaved between N0VA H4RT tracks so N0VA H4RT never
       clusters and plays at most once every ~9-12 songs / 35-45 minutes!).
    3. Alternate mixes sharing the same base song root (`get_base_root`) are spaced >= 26 slots apart.
    """
    if avoid_recent is None:
        avoid_recent = []
    if front_pool is None:
        front_pool = []
    avoid_mix_keys = {get_mix_key(s) for s in avoid_recent[-30:]}
    front_set = set(front_pool)

    nova_all = [s for s in song_list if get_artist_bucket(s) == "nova"]
    luna_all = [s for s in song_list if get_artist_bucket(s) == "luna"]
    hs_all = [s for s in song_list if get_artist_bucket(s) == "heartstrike"]
    fm_all = [s for s in song_list if get_artist_bucket(s) == "fm_guest"]

    def make_candidate():
        # 1. Build ordered solo NOVA HART stream (with optional gentle 1:4 fresh interleave, never 2:1!)
        f_copy = [s for s in front_pool if get_artist_bucket(s) == "nova"]
        nova_unplayed = [s for s in nova_all if s not in front_set and get_mix_key(s) not in avoid_mix_keys]
        nova_played = [s for s in nova_all if s not in front_set and get_mix_key(s) in avoid_mix_keys]
        rng.shuffle(f_copy)
        rng.shuffle(nova_unplayed)
        rng.shuffle(nova_played)

        if f_copy:
            nova_seq = []
            fi, ui = 0, 0
            while fi < len(f_copy) or ui < len(nova_unplayed):
                if fi < len(f_copy):
                    nova_seq.append(f_copy[fi])
                    fi += 1
                for _ in range(4):
                    if ui < len(nova_unplayed):
                        nova_seq.append(nova_unplayed[ui])
                        ui += 1
            nova_seq.extend(nova_played)
        else:
            nova_seq = nova_unplayed + nova_played

        # 2. Build evenly interleaved guest/alt ring (`Heartstrike` + `80s FM` woven between `N0VA H4RT`)
        luna_shuf = list(luna_all)
        other_guests = list(hs_all) + list(fm_all)
        rng.shuffle(luna_shuf)
        rng.shuffle(other_guests)

        total_guests = len(luna_shuf) + len(other_guests)
        guest_ring = []
        li, oi = 0, 0
        for g_step in range(total_guests):
            # Proportional Bresenham weave so `other_guests` (Heartstrike / 80s FM) break up `luna_shuf`!
            want_other = oi < len(other_guests) and (
                li >= len(luna_shuf)
                or (oi + 1) * total_guests <= (g_step + 1) * len(other_guests) + (total_guests // 3)
            )
            if want_other:
                guest_ring.append(other_guests[oi])
                oi += 1
            elif li < len(luna_shuf):
                guest_ring.append(luna_shuf[li])
                li += 1
            elif oi < len(other_guests):
                guest_ring.append(other_guests[oi])
                oi += 1

        # 3. Spread `guest_ring` uniformly across `nova_seq` (~1 guest per 6 solo Nova Hart songs!)
        total_n = len(nova_seq) + len(guest_ring)
        cand = []
        ni, gi = 0, 0
        if len(guest_ring) > 0:
            spacing = total_n / float(len(guest_ring))
            next_guest_pos = max(3, int(round(spacing * 0.6)))
            for pos in range(total_n):
                if gi < len(guest_ring) and (pos >= next_guest_pos or ni >= len(nova_seq)):
                    cand.append(guest_ring[gi])
                    gi += 1
                    next_guest_pos = int(round((gi + 0.6) * spacing))
                elif ni < len(nova_seq):
                    cand.append(nova_seq[ni])
                    ni += 1
                elif gi < len(guest_ring):
                    cand.append(guest_ring[gi])
                    gi += 1
        else:
            cand = list(nova_seq)

        # 4. Role-preserving base-root separation pass (`nova <-> nova` and `luna <-> luna` / `guest <-> guest`)
        #    so guest spacing NEVER drifts or clusters while separating same-root mixes by >= 26 slots!
        n = len(cand)
        buckets = [get_artist_bucket(s) for s in cand]
        for i in range(n):
            r_i = get_base_root(cand[i])
            conflict = any(get_base_root(cand[(i - d) % n]) == r_i for d in range(1, min(26, n)))
            if conflict:
                b_i = buckets[i]
                for j in range(i + 1, i + n):
                    jj = j % n
                    if jj == i or buckets[jj] != b_i:
                        continue
                    r_j = get_base_root(cand[jj])
                    if r_j == r_i:
                        continue
                    ok_i = all(get_base_root(cand[(i - d) % n]) != r_j for d in range(-25, 26) if d != 0 and (i - d) % n != jj)
                    ok_j = all(get_base_root(cand[(jj - d) % n]) != r_i for d in range(-25, 26) if d != 0 and (jj - d) % n != i)
                    if ok_i and ok_j:
                        cand[i], cand[jj] = cand[jj], cand[i]
                        break
        return cand

    best_cand = None
    best_score = -999999
    for _ in range(120):
        cand = make_candidate()
        score = 0
        n = len(cand)
        for idx, s in enumerate(cand):
            r = get_base_root(s)
            b = get_artist_bucket(s)
            for d in range(1, min(26, n)):
                if get_base_root(cand[(idx - d) % n]) == r:
                    score -= 50
            if b == "luna":
                for d in range(1, min(8, n)):
                    if get_artist_bucket(cand[(idx - d) % n]) == "luna":
                        score -= 80
            if b != "nova":
                for d in range(1, min(5, n)):
                    if get_artist_bucket(cand[(idx - d) % n]) != "nova":
                        score -= 60
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


# 4. Collect 1986 FM Sweepers, Gapless Splices, & Trojan-Horse 86/14 Outer-Circle Break Pools
fm_splices = sorted(glob.glob(os.path.join(FM_SPOTS_DIR, "fm_splice_*.mp3")))
fm_sweepers = sorted(glob.glob(os.path.join(FM_SPOTS_DIR, "fm_sweeper_*.mp3")))
fm_weather_and_spots = sorted(
    glob.glob(os.path.join(FM_SPOTS_DIR, "fm_weather_*.mp3"))
    + glob.glob(os.path.join(FM_SPOTS_DIR, "fm_spot86_*.mp3"))
    + glob.glob(os.path.join(FM_SPOTS_DIR, "fm_rsi_*.mp3"))
)
fm_drifts = sorted(glob.glob(os.path.join(FM_SPOTS_DIR, "fm_drift_*.mp3")))

if not fm_splices or not fm_sweepers:
    raise RuntimeError(f"Missing core 1986 FM splices/sweepers in {FM_SPOTS_DIR}!")

all_newscasts = sorted(
    t for t in glob.glob(os.path.join(NEWSCASTS_DIR, "*.mp3")) if os.path.isfile(t)
)
humanist_pool = [
    t for t in all_newscasts if os.path.basename(t).startswith("humanist_")
]
pirate_pool = [
    t for t in all_newscasts if os.path.basename(t).startswith("pirate_override_")
]
request_and_dj_pool = [
    t for t in all_newscasts if os.path.basename(t).startswith(("request_line_", "dj_callin_", "blaze_"))
]
_raw_crt_tv = sorted(
    t for t in all_newscasts if os.path.basename(t).startswith("commercial_tv_")
)
_fw_spots = [t for t in _raw_crt_tv if "_live20" in os.path.basename(t)]
_sv_spots_raw = [t for t in _raw_crt_tv if "_streamvid" in os.path.basename(t)]
_lore_spots = [
    t for t in _raw_crt_tv
    if "_live20" not in os.path.basename(t) and "_streamvid" not in os.path.basename(t)
]
# Order stream videos so short promos and longer diagnostic featurettes alternate cleanly
_sv_short = [t for t in _sv_spots_raw if "_feat_" not in os.path.basename(t)]
_sv_long = [t for t in _sv_spots_raw if "_feat_" in os.path.basename(t)]
_sv_spots: list[str] = []
for _si in range(max(len(_sv_short), len(_sv_long))):
    if _si < len(_sv_short):
        _sv_spots.append(_sv_short[_si])
    if _si < len(_sv_long):
        _sv_spots.append(_sv_long[_si])

if _lore_spots and (_fw_spots or _sv_spots):
    # First interleave Fourthwall spots across classic CRT spots, then weave stream break videos evenly
    _base_tv: list[str] = []
    if _fw_spots:
        _stride_fw = max(2, len(_lore_spots) // len(_fw_spots))
        _fw_i = 0
        for _li, _lt in enumerate(_lore_spots):
            _base_tv.append(_lt)
            if (_li + 1) % _stride_fw == 0 and _fw_i < len(_fw_spots):
                _base_tv.append(_fw_spots[_fw_i])
                _fw_i += 1
        while _fw_i < len(_fw_spots):
            _base_tv.append(_fw_spots[_fw_i])
            _fw_i += 1
    else:
        _base_tv = list(_lore_spots)

    if _sv_spots:
        crt_tv_pool = []
        _stride_sv = max(2, len(_base_tv) // len(_sv_spots))
        _sv_i = 0
        for _bi, _bt in enumerate(_base_tv):
            crt_tv_pool.append(_bt)
            if (_bi + 1) % _stride_sv == 0 and _sv_i < len(_sv_spots):
                crt_tv_pool.append(_sv_spots[_sv_i])
                _sv_i += 1
        while _sv_i < len(_sv_spots):
            crt_tv_pool.append(_sv_spots[_sv_i])
            _sv_i += 1
    else:
        crt_tv_pool = _base_tv
else:
    crt_tv_pool = _raw_crt_tv
commercial_and_trailer_pool = [
    t
    for t in all_newscasts
    if os.path.basename(t).startswith(("commercial_", "trailer_", "heartstrike_"))
    and not os.path.basename(t).startswith("commercial_tv_")
]
world_and_psa_pool = [
    t
    for t in all_newscasts
    if os.path.basename(t).startswith(("world_", "psa_", "wlf_"))
    or not os.path.basename(t).startswith(
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
            "request_line_",
            "wlf_",
            "nova_live_slot_",
        )
    )
]

lab_pool = sorted(
    t for t in glob.glob(os.path.join(LAB_DIR, "*.mp3")) if os.path.isfile(t)
)
intercept_pool = sorted(
    t for t in glob.glob(os.path.join(INTERCEPT_DIR, "*.mp3")) if os.path.isfile(t)
)
numbers_pool = sorted(
    t for t in glob.glob(os.path.join(NUMBERS_DIR, "*.mp3")) if os.path.isfile(t)
)

for pool in (
    fm_weather_and_spots,
    fm_drifts,
    crt_tv_pool,
    request_and_dj_pool,
    commercial_and_trailer_pool,
    world_and_psa_pool,
    humanist_pool,
    pirate_pool,
    lab_pool,
    intercept_pool,
    numbers_pool,
):
    rng.shuffle(pool)

# TROJAN-HORSE 86% / 14% OUTER-CIRCLE CLOCKWHEEL:
#   - 86% (6 of every 7 sweep breaks): Warm, nostalgic 1986 FM Radio surface
#     (Nova's Highway Weather & Trojan-Horse Live Reads, Open Request Line, DJ Call-Ins,
#      Rick Blaze, 1980s Commercials/Trailers, Heartstrike Spots, & 1980s World Vignettes).
#   - 14% (1 of every 7 sweep breaks — ~once per 21 songs): Haunting Subcarrier Bleed
#     (7.6s 82.5 FM Carrier Drift w/ faint 750 Hz CW Morse, Pirate Override, Resistance,
#      Sublevel B2 Dictaphone, or Shortwave Intercept).
surface_fm_buckets = [
    list(fm_weather_and_spots),
    list(request_and_dj_pool),
    list(commercial_and_trailer_pool),
    list(world_and_psa_pool),
]
bleed_arg_pool = (
    list(fm_drifts)
    + list(pirate_pool)
    + list(humanist_pool[:10])
    + list(lab_pool[:6])
    + list(intercept_pool[:5])
    + list(numbers_pool[:3])
)
rng.shuffle(bleed_arg_pool)

ccw_interstitials = []
surf_cursors = [0] * len(surface_fm_buckets)
surf_turn = 0
bleed_cursor = 0

while any(surf_cursors[i] < len(surface_fm_buckets[i]) for i in range(len(surface_fm_buckets))):
    # Place 6 authentic 1986 FM surface spots (86%)
    added_s = 0
    attempts = 0
    while added_s < 6 and attempts < len(surface_fm_buckets) * 4:
        b_idx = surf_turn % len(surface_fm_buckets)
        surf_turn += 1
        attempts += 1
        if b_idx == 0 and surf_cursors[0] >= len(surface_fm_buckets[0]) and surface_fm_buckets[0]:
            # Cycle Nova's own 1986 FM Weather & Studio Live-Read spots evenly around the dial
            pass
        if surf_cursors[b_idx] < len(surface_fm_buckets[b_idx]):
            ccw_interstitials.append(surface_fm_buckets[b_idx][surf_cursors[b_idx]])
            surf_cursors[b_idx] += 1
            added_s += 1
    if not added_s:
        break

    # Place 1 subtle Trojan-Horse subcarrier bleed spot (14%)
    if bleed_cursor < len(bleed_arg_pool):
        ccw_interstitials.append(bleed_arg_pool[bleed_cursor])
        bleed_cursor += 1

# Deduplicate while preserving exact 86/14 braided order
seen_inter = set()
unique_ccw = []
for item in ccw_interstitials:
    if item not in seen_inter:
        seen_inter.add(item)
        unique_ccw.append(item)

# Ensure gcd(N_S, N_I) == 1 so sweep breaks never repeat `(song, break)` pairings!
while math.gcd(N_S, len(unique_ccw)) != 1 and len(unique_ccw) > 60:
    for idx in range(len(unique_ccw) - 1, -1, -1):
        if "fm_80s_spots" not in unique_ccw[idx]:
            unique_ccw.pop(idx)
            break
    else:
        unique_ccw.pop()

N_I = len(unique_ccw)
outer_circle_interstitials = [None] * N_I
for step_k, track_path in enumerate(unique_ccw):
    outer_idx = (N_I - 1 - step_k) % N_I
    outer_circle_interstitials[outer_idx] = track_path

bleed_set = set(bleed_arg_pool)
actual_bleed_cnt = sum(1 for x in unique_ccw if x in bleed_set)
actual_surf_cnt = N_I - actual_bleed_cnt

print("Building 1986 FM Trojan-Horse 3-Song-Sweep Broadcast Clockwheel:")
print(f"  - INNER CIRCLE (Songs & Alternate Mixes, Clockwise +1): {N_S} unique tracks ({len(freshly_ingested)} newly added)")
print(f"  - SWEEP ARCHITECTURE: 3 Songs in a Row -> [Song 1 -> 0.34s Splice -> Song 2 -> 0.34s Splice / 5s 82.5 FM Sweeper -> Song 3 -> 18s FM Break]")
print(f"  - OUTER CIRCLE (Sweep Breaks, Counter-Clockwise -1):    {N_I} unique breaks")
print(f"      * 1986 FM Surface Spots (Weather/Ads/Request/DJ):   {actual_surf_cnt} ({100.0 * actual_surf_cnt / max(1, N_I):.1f}%)")
print(f"      * Trojan-Horse Subcarrier Bleeds (:02 Drift/Lab):   {actual_bleed_cnt} ({100.0 * actual_bleed_cnt / max(1, N_I):.1f}%)")
print(f"  - Coprime Check: gcd({N_S}, {N_I}) = {math.gcd(N_S, N_I)}")

# 5. Generate 8 full revolutions of the Inner Circle in 3-Song Commercial-Free Music Sweeps!
# CRITICAL INVARIANT: Every single vocal song still has a real non-song `.mp3` (`>= 4.5 KB`) at `slot - 1`
# (`fm_splice_001..090.mp3`, `fm_sweeper_01..06.mp3`, or an `outer_circle` break) so Live Chat Jukebox
# song intros and spoken viewer replies NEVER wait 3 songs—they can hot-swap immediately after ANY song!
NUM_CYCLES = 8
TOTAL_STEPS = N_S * NUM_CYCLES

# Discover verified pre-song Veo AI DJ intro clips (`broadcast_archive/dj_intros/dj_intro_<song_stem>.mp3`
# paired 1:1 with `assets_arg/dj_intros/dj_intro_<song_stem>.mp4`)
DJ_INTROS_MP3_DIR = os.path.join(ARCHIVE_DIR, "dj_intros")
DJ_INTROS_MP4_DIR = os.path.join(HERE, "assets_arg", "dj_intros")
verified_dj_intros: dict[str, str] = {}
if os.path.isdir(DJ_INTROS_MP3_DIR) and os.path.isdir(DJ_INTROS_MP4_DIR):
    for _mp3_p in sorted(glob.glob(os.path.join(DJ_INTROS_MP3_DIR, "dj_intro_*.mp3"))):
        _bname = os.path.basename(_mp3_p)
        _stem = os.path.splitext(_bname)[0]
        _mp4_p = os.path.join(DJ_INTROS_MP4_DIR, f"{_stem}.mp4")
        if (
            os.path.isfile(_mp3_p)
            and os.path.getsize(_mp3_p) >= 8192
            and os.path.isfile(_mp4_p)
            and os.path.getsize(_mp4_p) >= 32768
        ):
            _song_stem = _stem[len("dj_intro_") :]
            verified_dj_intros[_song_stem] = _mp3_p

NOVA_FACELESS_INTERSTITIAL_PREFIXES = (
    "fm_sweeper_",
    "fm_weather_",
    "fm_spot86_",
    "fm_rsi_",
    "request_line_",
    "nova_live_slot_",
    "opener_",
    "story_",
    "signoff_",
    "_runtime_open_",
)


def is_nova_faceless_interstitial(path_str: str) -> bool:
    norm_p = (path_str or "").replace("\\", "/").lower()
    bname = os.path.basename(norm_p)
    if bname.startswith(NOVA_FACELESS_INTERSTITIAL_PREFIXES):
        return True
    return any(seg in norm_p for seg in ("/show_segments/", "/multilingual_bulletins/", "/geocities_readings/"))


full_playlist = []
ordered_songs = []
seen_sweep_pairings = set()
splice_cursor = 0
step_inter_tracks: list[str] = []

for t in range(TOTAL_STEPS):
    s_idx = t % N_S
    pos_in_sweep = t % 3
    sweep_num = t // 3

    if pos_in_sweep == 0:
        # Song 1 -> Song 2: seamless 0.34s analog tape splice
        inter_track = fm_splices[splice_cursor % len(fm_splices)]
        splice_cursor += 1
    elif pos_in_sweep == 1:
        # Song 2 -> Song 3: alternate between seamless 0.34s splice and crisp 5s `82.5 FM Stereo` ID sweeper
        if sweep_num % 2 == 0:
            inter_track = fm_splices[splice_cursor % len(fm_splices)]
            splice_cursor += 1
        else:
            inter_track = fm_sweepers[(sweep_num // 2) % len(fm_sweepers)]
    else:
        # End of 3-Song Sweep:
        #   - Even sweeps (Sweep #1, #3, #5... ~every 6 songs / 20 mins): Full-Motion 30fps CRT TV Commercial (`commercial_tv_*`)
        #   - Odd sweeps  (Sweep #2, #4, #6...): Curated 1986 FM Radio Spot (86% 1986 FM / 14% Subcarrier Bleed)
        if crt_tv_pool and (sweep_num % 2 == 0):
            tv_idx = (sweep_num // 2) % len(crt_tv_pool)
            inter_track = crt_tv_pool[tv_idx]
        else:
            fm_sweep_step = (sweep_num // 2) if crt_tv_pool else sweep_num
            i_idx = (N_I - 1 - fm_sweep_step) % N_I
            inter_track = outer_circle_interstitials[i_idx]
            seen_sweep_pairings.add((s_idx, i_idx))

    step_inter_tracks.append(inter_track)

for t in range(TOTAL_STEPS):
    s_idx = t % N_S
    song_track = inner_circle_songs[s_idx]
    song_stem = os.path.splitext(os.path.basename(song_track))[0]
    inter_track = step_inter_tracks[t]
    prev_inter_track = step_inter_tracks[(t - 1) % TOTAL_STEPS]

    ordered_songs.append(song_track)
    # HARD INVARIANT: Never place an on-screen Veo introduction (`dj_intro_*`) immediately after a faceless Nova interstitial!
    dj_intro_track = None if is_nova_faceless_interstitial(prev_inter_track) else verified_dj_intros.get(song_stem)
    if dj_intro_track:
        full_playlist.append(dj_intro_track)
        dj_tail_cand = os.path.join(REAL_SONGS_DIR, "dj_tails", f"dj_tail_{song_stem}.mp3")
        if os.path.isfile(dj_tail_cand) and os.path.getsize(dj_tail_cand) >= 16384:
            full_playlist.append(dj_tail_cand)
        else:
            full_playlist.append(song_track)
    else:
        full_playlist.append(song_track)
    full_playlist.append(inter_track)

assert len(set(ordered_songs[:N_S])) == N_S, "Inner circle failed full play-through before repeat!"
for _chk_i in range(len(full_playlist)):
    _cur_p = full_playlist[_chk_i]
    _nxt_p = full_playlist[(_chk_i + 1) % len(full_playlist)]
    assert not (
        is_nova_faceless_interstitial(_cur_p) and os.path.basename(_cur_p) and os.path.basename(_nxt_p).startswith("dj_intro_")
    ), f"Back-to-back faceless Nova + on-screen dj_intro at {_chk_i}: {_cur_p} -> {_nxt_p}"
    assert not (
        os.path.basename(_cur_p).startswith("dj_intro_") and is_nova_faceless_interstitial(_nxt_p)
    ), f"Back-to-back on-screen dj_intro + faceless Nova at {_chk_i}: {_cur_p} -> {_nxt_p}"

tmp_file = out_file + ".tmp"
with open(tmp_file, "w") as f:
    for t in full_playlist:
        f.write(f"file '{t}'\n")
os.replace(tmp_file, out_file)

fresh_marker = os.path.join(HERE, ".playlist_fresh")
with open(fresh_marker, "w") as fm:
    fm.write(str(time.time()))

first_break_name = os.path.basename(crt_tv_pool[0]) if crt_tv_pool else os.path.basename(outer_circle_interstitials[N_I - 1])
print(f"\n✓ Generated 1986 FM + 30fps CRT TV 3-Song-Sweep Playlist with {len(full_playlist)} total slots ({len(ordered_songs)} song plays, {len(crt_tv_pool)} CRT TV commercials) in {out_file}")
print(f"✓ Opening 3-Song Sweep: {os.path.basename(inner_circle_songs[0])} -> {os.path.basename(inner_circle_songs[1])} -> {os.path.basename(inner_circle_songs[2])}")
print(f"✓ First Break after Sweep #1: {first_break_name}")
