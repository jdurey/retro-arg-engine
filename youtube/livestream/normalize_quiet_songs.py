#!/usr/bin/env python3
"""2-Pass EBU R128 Broadcast Loudness Normalizer for 82.5 FM Studio B.

Normalizes every song in `broadcast_archive/radio_master_songs/*.mp3` outside
`[-13.55, -12.45] LUFS` or with True Peak `> -0.60 dBTP` to uniform `-13.0 LUFS`
(`TP = -1.0 dBTP, LRA = 11`, `44.1 kHz`, `2ch`, `192k` CBR `-vn` MP3), eliminating
volume drops on quiet masters (e.g. `radio_kilometro_cero.mp3` at `-16.06 LUFS`) and
attenuating hot/clipping masters (e.g. `-8.10 LUFS / +1.20 dBTP`).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SONG_DIR = HERE / "broadcast_archive" / "radio_master_songs"
FFMPEG_BIN = "/opt/homebrew/bin/ffmpeg" if os.path.exists("/opt/homebrew/bin/ffmpeg") else "ffmpeg"

TARGET_I = -13.0
TARGET_TP = -1.0
TARGET_LRA = 11.0


def probe_loudnorm_stats(mp3_path: Path) -> dict | None:
    res = subprocess.run(
        [
            FFMPEG_BIN,
            "-nostdin",
            "-nostats",
            "-i",
            str(mp3_path),
            "-vn",
            "-af",
            f"loudnorm=I={TARGET_I:.1f}:TP={TARGET_TP:.1f}:LRA={TARGET_LRA:.0f}:print_format=json",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    m = re.search(r"\{\s*\"input_i\".*?\}", res.stderr, re.S)
    if not m:
        return None
    d = json.loads(m.group(0))
    return {
        "file": mp3_path.name,
        "I": float(d["input_i"]),
        "TP": float(d["input_tp"]),
        "LRA": float(d["input_lra"]),
        "thresh": float(d["input_thresh"]),
        "offset": float(d["target_offset"]),
    }


def normalize_one_song(args_tuple: tuple[Path, dict | None]) -> tuple[str, bool, str]:
    mp3_path, pre_stats = args_tuple
    name = mp3_path.name
    st = pre_stats or probe_loudnorm_stats(mp3_path)
    if st is None or st["I"] <= -60.0:
        return name, False, "skipped (unmeasurable)"

    in_i = float(st["I"])
    in_tp = float(st["TP"])
    in_lra = float(st["LRA"])
    in_thresh = float(st["thresh"])
    in_off = float(st["offset"])

    if (-13.55 <= in_i <= -12.45) and (in_tp <= -0.60):
        return name, False, f"already normalized (I={in_i:6.2f} LUFS, TP={in_tp:5.2f} dBTP)"

    af = (
        f"loudnorm=I={TARGET_I:.1f}:TP={TARGET_TP:.1f}:LRA={TARGET_LRA:.0f}:"
        f"measured_I={in_i:.2f}:measured_TP={in_tp:.2f}:measured_LRA={in_lra:.2f}:"
        f"measured_thresh={in_thresh:.2f}:offset={in_off:.2f}:linear=true"
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        out_tmp = Path(tmpdir) / name
        subprocess.run(
            [
                FFMPEG_BIN,
                "-y",
                "-nostdin",
                "-loglevel",
                "error",
                "-i",
                str(mp3_path),
                "-vn",
                "-af",
                af,
                "-ar",
                "44100",
                "-ac",
                "2",
                "-c:a",
                "libmp3lame",
                "-b:a",
                "192k",
                str(out_tmp),
            ],
            check=True,
        )
        # Atomic replace inside SONG_DIR
        local_tmp = mp3_path.with_suffix(".norm_tmp.mp3")
        os.replace(out_tmp, local_tmp)
        os.replace(local_tmp, mp3_path)

    return name, True, f"I={in_i:6.2f} -> -13.00 LUFS (was TP={in_tp:5.2f} dBTP)"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-scan", type=Path, default=None, help="Optional pre-computed JSON list of Pass-1 stats")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    pre_map: dict[str, dict] = {}
    if args.from_scan and args.from_scan.exists():
        for row in json.loads(args.from_scan.read_text(encoding="utf-8")):
            pre_map[str(row["file"])] = row

    songs = sorted(SONG_DIR.glob("*.mp3"))
    print(f"Normalizing {len(songs)} songs in {SONG_DIR} to {TARGET_I:.1f} LUFS (TP={TARGET_TP:.1f} dBTP)...", flush=True)
    work = [(p, pre_map.get(p.name)) for p in songs]
    updated = 0
    kept = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        for name, changed, msg in ex.map(normalize_one_song, work):
            if changed:
                updated += 1
                print(f"  [NORM] {name:50s} | {msg}", flush=True)
            else:
                kept += 1
    print(f"\nDone! Normalized {updated} songs, {kept} already within [-13.55, -12.45] LUFS & TP <= -0.60 dBTP.", flush=True)


if __name__ == "__main__":
    main()
