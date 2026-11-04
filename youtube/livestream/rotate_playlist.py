#!/usr/bin/env python3
"""
Maintains persistent, non-repeating playlist playhead across ALL stream restarts:
  1. Uses `nova_brain/live_playhead_bookmark.json` (written live by `sync_telemetry.py` via `lsof`)
     AND `stream.log` (`2 MB` tail, resilient even when session headers scroll past 2 MB) to rotate
     every played track + the interrupted track to the tail of `playlist.txt`.
  2. Checks `nova_brain/recent_played_songs.json` (last 90 vocal songs played): if the resulting
     head song (or cold-boot / rapid-restart playhead) was recently played—or if `played_count == 0`—
     jumps forward to a random fresh `(interstitial, song)` boundary whose upcoming songs have NOT
     played recently, recording the new starting song immediately so two restarts can NEVER start
     at the same song!
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
import time

DIR = os.path.dirname(os.path.abspath(__file__))
PLAYLIST = os.path.join(DIR, "playlist.txt")
LOG_FILE = os.path.join(DIR, "stream.log")
NOVA_BRAIN_DIR = os.path.join(DIR, "nova_brain")
BOOKMARK_FILE = os.path.join(NOVA_BRAIN_DIR, "live_playhead_bookmark.json")
RECENT_SONGS_FILE = os.path.join(NOVA_BRAIN_DIR, "recent_played_songs.json")
LAST_ROT_EPOCH_FILE = os.path.join(NOVA_BRAIN_DIR, ".last_rotate_epoch")
DURATIONS_FILE = os.path.join(DIR, "track_durations.json")

try:
    with open(DURATIONS_FILE, "r", encoding="utf-8") as _df:
        _DURATION_CACHE = json.load(_df)
except Exception:
    _DURATION_CACHE = {}


def get_duration(filepath: str) -> float:
    bname = os.path.basename(filepath)
    if bname in _DURATION_CACHE:
        try:
            if os.path.getsize(filepath) > 4096:
                return float(_DURATION_CACHE[bname])
        except Exception:
            return float(_DURATION_CACHE[bname])
    try:
        sz = os.path.getsize(filepath)
        if sz <= 4096:
            return 0.05
        with open(filepath, "rb") as f:
            hdr = f.read(10)
        if len(hdr) == 10 and hdr[:3] == b"ID3":
            id3_sz = ((hdr[6] & 0x7F) << 21) | ((hdr[7] & 0x7F) << 14) | ((hdr[8] & 0x7F) << 7) | (hdr[9] & 0x7F)
            sz -= id3_sz + 10
        return max(0.05, (sz - 1440) / 24000.0)
    except Exception:
        return 200.0


def get_last_elapsed_seconds() -> float:
    """Reads up to 2 MB of `stream.log` and extracts elapsed streaming time even for multi-hour sessions."""
    if not os.path.exists(LOG_FILE):
        return 0.0
    try:
        with open(LOG_FILE, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 2097152))
            chunk = f.read().decode("utf-8", errors="ignore")

        parts = chunk.split("[STREAM.SH] Selected encoder:")
        # Check most recent session chunks first; if the session ran so long its header scrolled past 2MB,
        # `parts` has length 1 and we still parse `parts[0]`!
        search_chunks = list(reversed(parts[1:])) if len(parts) > 1 else [parts[0]]
        for session_chunk in search_chunks:
            matches = re.findall(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)", session_chunk)
            if matches:
                best = 0.0
                for m in matches[-80:]:
                    sec = float(m[0]) * 3600.0 + float(m[1]) * 60.0 + float(m[2])
                    if sec > best:
                        best = sec
                if best >= 3.0:
                    return best
    except Exception as e:
        print(f"Warning: could not parse elapsed time from log: {e}")
    return 0.0


def _load_recent_songs() -> list[str]:
    if not os.path.exists(RECENT_SONGS_FILE):
        return []
    try:
        data = json.loads(open(RECENT_SONGS_FILE, "r", encoding="utf-8").read())
        return [str(x) for x in data if x] if isinstance(data, list) else []
    except Exception:
        return []


def _save_recent_songs(songs: list[str]) -> None:
    try:
        os.makedirs(NOVA_BRAIN_DIR, exist_ok=True)
        tmp_p = RECENT_SONGS_FILE + ".tmp"
        with open(tmp_p, "w", encoding="utf-8") as f:
            json.dump(songs[-90:], f)
        os.replace(tmp_p, RECENT_SONGS_FILE)
    except Exception:
        pass


def _first_vocal_song(lines_seq: list[str]) -> str:
    for ln in lines_seq[:8]:
        if "radio_master_songs" in ln:
            m = re.search(r"file\s+'([^']+)'", ln)
            if m:
                bn = os.path.basename(m.group(1))
                return bn[len("dj_tail_") :] if bn.startswith("dj_tail_") else bn
    return ""


SHORT_ALBUM_TRACKS = {
    "radio_signal_acquired.mp3",
    "radio_in_this_together.mp3",
}

from excluded_radio_songs import EXCLUDED_RADIO_SONGS, purge_excluded_playlist_lines

SUPERSEDED_DUPLICATE_FILES = set(EXCLUDED_RADIO_SONGS)


def _norm_song_stem(fname: str) -> str:
    s = os.path.splitext(os.path.basename(fname).lower())[0]
    if s.startswith("dj_tail_"):
        s = s[len("dj_tail_") :]
    s = re.sub(r"^radio_(?:b_|19b_|\d+_)?", "", s)
    # Strip only file-copy / mastering tags — NEVER strip _live, _tokyo_master, _demo, _es, _kr, _nova_hart, _aor_mix!
    if not s.endswith("tokyo_master"):
        s = re.sub(r"_(?:remastered|master|final(?:_\d+)?|v\d+|1)$", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def discover_unlisted_master_songs(existing_paths: list[str]) -> list[str]:
    """
    Finds any vocal songs in `broadcast_archive/radio_master_songs/` (`>= 60s` or in `SHORT_ALBUM_TRACKS`)
    that are NOT yet present in `playlist.txt` (ignoring superseded duplicate copy files).
    """
    songs_dir = os.path.join(DIR, "broadcast_archive", "radio_master_songs")
    if not os.path.isdir(songs_dir):
        return []
    existing_bnames = {os.path.basename(p) for p in existing_paths if "radio_master_songs" in p}
    existing_stems = {_norm_song_stem(b) for b in existing_bnames if _norm_song_stem(b)}

    missing_full_paths: list[str] = []
    for fname in sorted(os.listdir(songs_dir)):
        if not fname.endswith(".mp3") or not fname.startswith("radio_"):
            continue
        if fname in existing_bnames or fname in SUPERSEDED_DUPLICATE_FILES:
            continue
        n_stem = _norm_song_stem(fname)
        if n_stem and n_stem in existing_stems:
            continue
        fpath = os.path.join(songs_dir, fname)
        if fname not in SHORT_ALBUM_TRACKS and get_duration(fpath) < 60.0:
            continue
        missing_full_paths.append(fpath)
        existing_bnames.add(fname)
        if n_stem:
            existing_stems.add(n_stem)
    return missing_full_paths


def append_missing_songs_to_tail() -> list[str]:
    """
    Appends any newly added `radio_*.mp3` songs (each paired with an interstitial slot)
    strictly to the TAIL of `playlist.txt` so active FFmpeg `-f concat` indices `0..N-1`
    never shift mid-run while ensuring `playlist.txt` permanently contains every new song!
    """
    if not os.path.exists(PLAYLIST):
        return []
    with open(PLAYLIST, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]
    paths = []
    interstitials = []
    for ln in lines:
        m = re.search(r"file\s+'([^']+)'", ln)
        if m:
            p = m.group(1)
            paths.append(p)
            if (
                "radio_master_songs" not in p
                and "nova_live_slot_" not in p
                and not os.path.basename(p).startswith("fm_splice_")
                and os.path.exists(p)
            ):
                interstitials.append(p)

    new_songs = discover_unlisted_master_songs(paths)
    if not new_songs:
        return []

    rng = random.SystemRandom()
    fallback_int = interstitials[0] if interstitials else ""
    appended_names: list[str] = []
    for sp in new_songs:
        if interstitials:
            int_p = rng.choice(interstitials)
            lines.append(f"file '{int_p}'")
        elif fallback_int:
            lines.append(f"file '{fallback_int}'")
        lines.append(f"file '{sp}'")
        appended_names.append(os.path.basename(sp))

    tmp_path = PLAYLIST + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        for l in lines:
            f.write(l + "\n")
    os.replace(tmp_path, PLAYLIST)
    return appended_names


def rotate() -> None:
    os.makedirs(NOVA_BRAIN_DIR, exist_ok=True)
    now_ts = time.time()

    # Dedup guard (6s) so `immortal_supervisor.py` + `stream.sh` calling `rotate_playlist.py`
    # back-to-back within the same launch only rotate once, while ANY subsequent restart rotates fresh!
    if os.path.exists(LAST_ROT_EPOCH_FILE):
        try:
            prev_rot = float(open(LAST_ROT_EPOCH_FILE, "r", encoding="utf-8").read().strip() or 0.0)
            if 0.0 <= (now_ts - prev_rot) < 6.0:
                print("✓ Already rotated within last 6s boot window; keeping fresh playhead.")
                return
        except Exception:
            pass

    fresh_marker = os.path.join(DIR, ".playlist_fresh")
    if os.path.exists(fresh_marker):
        try:
            os.remove(fresh_marker)
        except OSError:
            pass

    if not os.path.exists(PLAYLIST):
        print("playlist.txt does not exist; skipping rotation.")
        return

    with open(PLAYLIST, "r", encoding="utf-8", errors="ignore") as f:
        raw_lines = [line.strip() for line in f if line.strip()]
    if len(raw_lines) < 4:
        return

    repo_root = os.path.abspath(os.path.join(DIR, "..", ".."))
    lines: list[str] = []
    for rl in raw_lines:
        m_p = re.search(r"file\s+'([^']+)'", rl)
        if m_p and not os.path.exists(m_p.group(1)) and "/retro_arg_engine/" in m_p.group(1):
            alt_p = os.path.join(repo_root, m_p.group(1).split("/retro_arg_engine/", 1)[1])
            if os.path.exists(alt_p):
                rl = f"file '{alt_p}'"
        lines.append(rl)

    paths: list[str] = []
    interstitial_pool: list[str] = []
    for l in lines:
        m = re.search(r"file\s+'([^']+)'", l)
        p_val = m.group(1) if m else l
        paths.append(p_val)
        if (
            "radio_master_songs" not in p_val
            and "nova_live_slot_" not in p_val
            and not os.path.basename(p_val).startswith("fm_splice_")
            and os.path.exists(p_val)
        ):
            interstitial_pool.append(p_val)

    # Auto-discover & weave any newly added `radio_*.mp3` songs in `broadcast_archive/radio_master_songs/`
    # so every new Nova Hart song automatically enters 24/7 rotation!
    newly_found = discover_unlisted_master_songs(paths)
    if newly_found:
        rng_new = random.SystemRandom()
        for sp in newly_found:
            if interstitial_pool:
                int_p = rng_new.choice(interstitial_pool)
                lines.append(f"file '{int_p}'")
                paths.append(int_p)
            lines.append(f"file '{sp}'")
            paths.append(sp)
        print(f"✓ Auto-ingested {len(newly_found)} new song(s) into playlist.txt: {[os.path.basename(x) for x in newly_found]}")

    n_total = len(lines)

    # 1. Compute advance count from `stream.log` elapsed seconds
    elapsed = get_last_elapsed_seconds()
    log_played = 0
    if elapsed >= 3.0:
        accum = 0.0
        for i, path in enumerate(paths):
            dur = get_duration(path)
            if accum + dur <= elapsed:
                accum += dur
                log_played = i + 1
            else:
                if (elapsed - accum) >= 4.0 or i == 0:
                    log_played = i + 1
                else:
                    log_played = i
                break

    # 2. Compute advance count from `live_playhead_bookmark.json` (`lsof` truth!)
    bm_played = 0
    if os.path.exists(BOOKMARK_FILE):
        try:
            bm = json.loads(open(BOOKMARK_FILE, "r", encoding="utf-8").read())
            bm_bname = str(bm.get("open_bname") or "")
            bm_ts = float(bm.get("ts") or 0.0)
            # Use bookmark if updated within the last 12 hours
            if bm_bname and (now_ts - bm_ts) <= 43200.0:
                for i, p in enumerate(paths):
                    if os.path.basename(p) == bm_bname:
                        bm_played = i + 1
                        break
        except Exception:
            pass

    played_count = max(log_played, bm_played) % n_total
    force_dj_intro = "--start-with-dj-intro" in sys.argv

    # Never slice directly between `dj_intro_<song>.mp3` and `<song>.mp3`!
    if played_count > 0 and "radio_master_songs" in paths[played_count]:
        prev_bname = os.path.basename(paths[played_count - 1])
        if prev_bname.startswith("dj_intro_"):
            played_count -= 1

    # 3. Anti-Repeat Guarantee: NEVER start at Track 0 unchanged AND NEVER start on a recently played song!
    recent_songs = _load_recent_songs()
    recent_set = set(recent_songs[-75:])

    cand_rot = lines[played_count:] + lines[:played_count]
    head_song = _first_vocal_song(cand_rot)

    if force_dj_intro or played_count == 0 or (head_song and head_song in recent_set):
        # Collect all clean song/pair start indices whose vocal song is NOT in `recent_set`,
        # strongly preferring `dj_intro_*.mp3` slots so reconnects open with Nova live in the 82.5 FM booth!
        dj_intro_offsets: list[int] = []
        fresh_offsets: list[int] = []
        for idx in range(2, n_total - 2):
            p_cur = paths[idx]
            p_nxt = paths[(idx + 1) % n_total]
            cur_bname = os.path.basename(p_cur)
            if cur_bname.startswith("dj_intro_") and "radio_master_songs" in p_nxt:
                s_bname = os.path.basename(p_nxt)
                if s_bname.startswith("dj_tail_"):
                    s_bname = s_bname[len("dj_tail_") :]
                if s_bname not in recent_set and s_bname not in SUPERSEDED_DUPLICATE_FILES:
                    dj_intro_offsets.append(idx)
                    fresh_offsets.append(idx)
            elif "radio_master_songs" not in p_cur and "radio_master_songs" in p_nxt:
                s_bname = os.path.basename(p_nxt)
                if s_bname.startswith("dj_tail_"):
                    s_bname = s_bname[len("dj_tail_") :]
                if s_bname not in recent_set and s_bname not in SUPERSEDED_DUPLICATE_FILES:
                    fresh_offsets.append(idx)
            elif "radio_master_songs" in p_cur and idx not in fresh_offsets:
                prev_b = os.path.basename(paths[idx - 1])
                if prev_b.startswith("dj_intro_"):
                    continue
                s_bname = os.path.basename(p_cur)
                if s_bname.startswith("dj_tail_"):
                    s_bname = s_bname[len("dj_tail_") :]
                if s_bname not in recent_set and s_bname not in SUPERSEDED_DUPLICATE_FILES:
                    fresh_offsets.append(idx)

        rng = random.SystemRandom()
        if dj_intro_offsets:
            played_count = rng.choice(dj_intro_offsets)
        elif fresh_offsets:
            played_count = rng.choice(fresh_offsets)
        else:
            # All songs cycled -> jump by a random large prime-ish offset (at least 15%–85% into catalog)
            played_count = rng.randint(max(2, n_total // 7), max(4, (n_total * 6) // 7))

        cand_rot = lines[played_count:] + lines[:played_count]
        head_song = _first_vocal_song(cand_rot)

    cand_rot = purge_excluded_playlist_lines(cand_rot)
    head_song = _first_vocal_song(cand_rot)

    # Atomically write rotated playlist + update recent_songs & dedup timestamp
    tmp_path = PLAYLIST + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        for l in cand_rot:
            f.write(l + "\n")
    os.replace(tmp_path, PLAYLIST)

    if head_song:
        recent_songs = [x for x in recent_songs if x != head_song] + [head_song]
        _save_recent_songs(recent_songs)

    try:
        with open(LAST_ROT_EPOCH_FILE, "w", encoding="utf-8") as lf:
            lf.write(f"{now_ts:.2f}")
    except Exception:
        pass

    next_label = head_song or cand_rot[0].split("/")[-1].replace("'", "")
    print(f"✓ Rotated playlist by {played_count}/{n_total} entries -> next vocal track: {next_label}")


if __name__ == "__main__":
    import sys as _sys

    if "--append-new-only" in _sys.argv:
        added = append_missing_songs_to_tail()
        print(f"✓ Appended {len(added)} new song(s) to tail of playlist.txt: {added}")
    else:
        rotate()
