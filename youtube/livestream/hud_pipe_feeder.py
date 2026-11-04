#!/usr/bin/env python3
"""
Project Stardust — Real-Time 1.0 Hz PNG Pipe Feeder for FFmpeg `image2pipe` (v2.0)
===================================================================================
Streams freshly rendered 960x540 RGBA PNG frames (`live_hud.png`) over stdout
(`-f image2pipe -vcodec png -framerate 1 -i -`) on a drift-free monotonic 1.000000 Hz clock,
and automatically hot-reloads `arg_broadcast_codex.py` and `sync_telemetry.py` whenever
they are modified on disk so visual upgrades take effect without interrupting FFmpeg!
"""

from __future__ import annotations
import argparse
import importlib
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

import arg_broadcast_codex  # noqa: E402
import radio_shows_engine  # noqa: E402
import song_crt_cgi_engine  # noqa: E402
import song_lore_questions  # noqa: E402
import studio_b_live_wire  # noqa: E402
import sync_telemetry  # noqa: E402

_latest_png_bytes: bytes = b""
_last_mtimes: dict[str, float] = {}


def _hot_reload_if_needed() -> None:
    """Hot-reloads arg_broadcast_codex, radio_shows_engine, studio_b_live_wire, song_crt_cgi_engine, song_lore_questions, nova_live_jukebox, and sync_telemetry if modified on disk."""
    global _last_mtimes
    try:
        codex_p = SCRIPT_DIR / "arg_broadcast_codex.py"
        shows_p = SCRIPT_DIR / "radio_shows_engine.py"
        wire_p = SCRIPT_DIR / "studio_b_live_wire.py"
        cgi_p = SCRIPT_DIR / "song_crt_cgi_engine.py"
        lore_p = SCRIPT_DIR / "song_lore_questions.py"
        jb_p = SCRIPT_DIR / "nova_live_jukebox.py"
        sync_p = SCRIPT_DIR / "sync_telemetry.py"
        m1 = codex_p.stat().st_mtime_ns if codex_p.exists() else 0
        m_sh = shows_p.stat().st_mtime_ns if shows_p.exists() else 0
        m_wr = wire_p.stat().st_mtime_ns if wire_p.exists() else 0
        m_cgi = cgi_p.stat().st_mtime_ns if cgi_p.exists() else 0
        m_lore = lore_p.stat().st_mtime_ns if lore_p.exists() else 0
        m_jb = jb_p.stat().st_mtime_ns if jb_p.exists() else 0
        m2 = sync_p.stat().st_mtime_ns if sync_p.exists() else 0
        if _last_mtimes and (
            _last_mtimes.get("codex") != m1
            or _last_mtimes.get("shows") != m_sh
            or _last_mtimes.get("wire") != m_wr
            or _last_mtimes.get("cgi") != m_cgi
            or _last_mtimes.get("lore") != m_lore
            or _last_mtimes.get("jb") != m_jb
            or _last_mtimes.get("sync") != m2
        ):
            importlib.invalidate_caches()
            importlib.reload(arg_broadcast_codex)
            importlib.reload(radio_shows_engine)
            importlib.reload(studio_b_live_wire)
            importlib.reload(song_crt_cgi_engine)
            importlib.reload(song_lore_questions)
            if "nova_live_jukebox" in sys.modules:
                importlib.reload(sys.modules["nova_live_jukebox"])
            importlib.reload(sync_telemetry)
        _last_mtimes["codex"] = m1
        _last_mtimes["shows"] = m_sh
        _last_mtimes["wire"] = m_wr
        _last_mtimes["cgi"] = m_cgi
        _last_mtimes["lore"] = m_lore
        _last_mtimes["jb"] = m_jb
        _last_mtimes["sync"] = m2
    except Exception:
        pass


def _fallback_png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGBA", (sync_telemetry.FRAME_W, sync_telemetry.FRAME_H), (0, 0, 0, 0)).save(
        buf, format="PNG", compress_level=1
    )
    return buf.getvalue()


def _render_once(repo_root: Path, out_json: Path, out_forensics_json: Path, out_hud: Path, assets_dir: Path) -> bytes:
    _hot_reload_if_needed()
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
    return sync_telemetry.render_full_arg_overlay_png(
        out_hud,
        snap["diagnostic_ramp"],
        assets_dir,
        now,
        snap_meta=snap["diagnostic_ramp"].get("_snap_meta"),
    )


def _render_worker(repo_root: Path, out_json: Path, out_forensics_json: Path, out_hud: Path, assets_dir: Path) -> None:
    global _latest_png_bytes
    while True:
        try:
            _latest_png_bytes = _render_once(repo_root, out_json, out_forensics_json, out_hud, assets_dir)
        except Exception:
            pass
        time.sleep(0.5)


def _get_live_ffmpeg_mux_sec(log_path: Path) -> float:
    """Returns FFmpeg's current muxer timestamp (`time=HH:MM:SS.xx`) from stream.log."""
    if not log_path.exists():
        return 0.0
    try:
        mtime = log_path.stat().st_mtime
        age = max(0.0, time.time() - mtime)
        if age > 15.0:
            return 0.0
        with open(log_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            sz = f.tell()
            f.seek(max(0, sz - 65536))
            chunk = f.read().decode("utf-8", errors="ignore")
        parts = chunk.split("[STREAM.SH] Selected encoder:")
        tail = parts[-1] if parts else chunk
        times = sync_telemetry.TIME_RE.findall(tail)
        if not times:
            return 0.0
        h, m, s = times[-1]
        return int(h) * 3600 + int(m) * 60 + float(s) + min(1.0, age)
    except Exception:
        return 0.0


def main() -> None:
    global _latest_png_bytes
    parser = argparse.ArgumentParser(description="Project Stardust Closed-Loop Zero-Lag HUD Pipe Feeder v2.2")
    parser.add_argument("--repo-root", type=Path, default=SCRIPT_DIR.parents[1])
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    out_json = repo_root / "site" / "assets" / "live_telemetry.json"
    out_forensics_json = repo_root / "site" / "forensics" / "live_telemetry.json"
    out_hud = repo_root / "youtube" / "livestream" / "live_hud.png"
    assets_dir = repo_root / "youtube" / "livestream" / "assets_arg"
    log_path = repo_root / "youtube" / "livestream" / "stream.log"
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
        # With `-threads 1` on FFmpeg's image2pipe PNG decoder, 2 initial frames initialize framesync
        for _ in range(2):
            sys.stdout.buffer.write(_latest_png_bytes)
        sys.stdout.buffer.flush()

        next_tick = time.monotonic() + 1.0
        while True:
            sleep_sec = next_tick - time.monotonic()
            if sleep_sec > 0:
                time.sleep(sleep_sec)
            elif sleep_sec < -1.0:
                next_tick = time.monotonic()
            next_tick += 1.0
            sys.stdout.buffer.write(_latest_png_bytes)
            sys.stdout.buffer.flush()
    except (BrokenPipeError, KeyboardInterrupt, OSError):
        os._exit(0)


if __name__ == "__main__":
    main()
