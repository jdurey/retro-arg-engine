#!/usr/bin/env python3
"""
Project Stardust — Real-Time 1.0 Hz PNG Pipe Feeder for FFmpeg `image2pipe`
===========================================================================
Solves FFmpeg 8's single-file `-f image2 -loop 1` frame caching and eliminates
disk partial-read race conditions by streaming freshly rendered 960x540 RGBA
PNG frames (`live_hud.png`) over stdout (`-f image2pipe -vcodec png -framerate 1 -i -`)
on a drift-free monotonic 1.000000 Hz clock.

Architecture:
  - Background thread (`_render_worker`): Polls `stream.log` and `playlist.txt`
    every 1.0s via `sync_telemetry`, updates `live_telemetry.json` and `live_hud.png`
    atomically on disk, and swaps `_latest_png_bytes` in RAM.
  - Main thread: Sends an initial 3-frame burst at t=0 (matching FFmpeg's
    `-readrate_initial_burst 3.0`) and then writes `_latest_png_bytes` to
    `sys.stdout.buffer` every 1.000000s on `time.monotonic()`.
"""

from __future__ import annotations
import argparse
import io
import json
import os
import sys
import threading
import time
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import sync_telemetry  # noqa: E402

_latest_png_bytes: bytes = b""


def _fallback_png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGBA", (sync_telemetry.FRAME_W, sync_telemetry.FRAME_H), (0, 0, 0, 0)).save(
        buf, format="PNG", compress_level=1
    )
    return buf.getvalue()


def _render_once(repo_root: Path, out_json: Path, out_forensics_json: Path, out_hud: Path, assets_dir: Path) -> bytes:
    now = time.time()
    snap = sync_telemetry.build_telemetry_snapshot(repo_root, now_ts=now, force_offline=False)
    payload = json.dumps(snap, indent=2)
    tmp_json = out_json.with_suffix(".tmp.json")
    tmp_json.write_text(payload, encoding="utf-8")
    os.replace(tmp_json, out_json)
    if out_forensics_json.parent.exists():
        tmp_fjson = out_forensics_json.with_suffix(".tmp.json")
        tmp_fjson.write_text(payload, encoding="utf-8")
        os.replace(tmp_fjson, out_forensics_json)
    return sync_telemetry.render_full_arg_overlay_png(out_hud, snap["diagnostic_ramp"], assets_dir, now)


def _render_worker(repo_root: Path, out_json: Path, out_forensics_json: Path, out_hud: Path, assets_dir: Path) -> None:
    global _latest_png_bytes
    while True:
        try:
            _latest_png_bytes = _render_once(repo_root, out_json, out_forensics_json, out_hud, assets_dir)
        except Exception:
            pass
        time.sleep(1.0)


def main() -> None:
    global _latest_png_bytes
    parser = argparse.ArgumentParser(description="Project Stardust 1.0 Hz HUD Pipe Feeder")
    parser.add_argument("--repo-root", type=Path, default=SCRIPT_DIR.parents[1])
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    out_json = repo_root / "site" / "assets" / "live_telemetry.json"
    out_forensics_json = repo_root / "site" / "forensics" / "live_telemetry.json"
    out_hud = repo_root / "youtube" / "livestream" / "live_hud.png"
    assets_dir = repo_root / "youtube" / "livestream" / "assets_arg"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_hud.parent.mkdir(parents=True, exist_ok=True)

    try:
        _latest_png_bytes = _render_once(repo_root, out_json, out_forensics_json, out_hud, assets_dir)
    except Exception:
        _latest_png_bytes = _fallback_png_bytes()

    t = threading.Thread(
        target=_render_worker,
        args=(repo_root, out_json, out_forensics_json, out_hud, assets_dir),
        daemon=True,
    )
    t.start()

    try:
        # Initial 6-frame burst to cover image2pipe stream probe + FFmpeg `-readrate_initial_burst 3.0`
        for _ in range(6):
            sys.stdout.buffer.write(_latest_png_bytes)
        sys.stdout.buffer.flush()

        next_tick = time.monotonic() + 1.0
        while True:
            sleep_sec = next_tick - time.monotonic()
            if sleep_sec > 0:
                time.sleep(sleep_sec)
            next_tick += 1.0
            sys.stdout.buffer.write(_latest_png_bytes)
            sys.stdout.buffer.flush()
    except (BrokenPipeError, KeyboardInterrupt, OSError):
        os._exit(0)


if __name__ == "__main__":
    main()
