#!/usr/bin/env python3
"""
Project Stardust — Intentional Track-Synchronized ARG Visual & Telemetry Engine
Reads active FFmpeg stream.log and playlist.txt, computes exact playhead state,
and writes:
  1. site/assets/live_telemetry.json & site/forensics/live_telemetry.json
  2. youtube/livestream/live_hud.png (960x540 RGBA Diegetic Overlay containing BOTH:
     - Region A [CRT Monitor Window x=366, y=228, w=202, h=108]:
       100% intentionally synchronized to the active audio track:
         * Foreign Broadcasts -> Live English Translation Teleprinter
         * Morse Code Beacons -> 750 Hz CW Morse Demodulator + 3D Wireframe + Decoded ASCII
         * Numbers Stations   -> 5-Digit One-Time-Pad Cipher Matrix & Feistel Key Mask
         * Classified Tapes   -> Sublevel B2 Magnetic Reel Dossier & Speaker Transcript
         * Nova Hart Memory Songs -> Haunting 1985 CRT Digital Face of Nova Hart (with blinking eyes)
         * Counterpoint Songs -> Dual-Profile "Second Voice" Phase Anomaly (Marcus + Nova)
         * Neural Mesh Songs  -> Biometric Iris Scan (Empathy Trial #04)
         * Nominal Songs      -> Transparent (classic 14.2 Hz CRT Oscilloscope Grid + 30fps live soundwave)
     - Region B [Bottom Telemetry HUD Label x=80, y=476, w=800, h=54]:
       Always visible at the bottom of the screen with live English translations,
       decoded Morse payloads, song provenance, and solvable ARG instructions.
"""

from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import math
import os
import re
import time
import textwrap
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

from arg_broadcast_codex import resolve_intentional_state

BROADCAST_EPOCH = 1791763200  # 2026-10-12T00:00:00Z
CYCLE_DURATION_SEC = 44 * 3600
CADENCE_RECIPES = [
    "numbers",
    "direct_morse",
    "lab_tape",
    "bulletin",
    "arg_intercept",
    "direct_midi",
]

REGIONAL_RELAYS = [
    {"node": 1, "code": "US-NV", "name": "Rachel / Groom Lake Trunk", "freq_khz": 4625.0},
    {"node": 2, "code": "JP-TYO", "name": "Akasaka PC-98 Packet Relay", "freq_khz": 6925.0},
    {"node": 3, "code": "KR-DMZ", "name": "Paju Shortwave Array", "freq_khz": 5810.0},
    {"node": 4, "code": "MX-DF", "name": "Red Coyoacan Tape Exchange", "freq_khz": 7345.0},
    {"node": 5, "code": "DE-HAM", "name": "Hamburg Nord Relay", "freq_khz": 3995.0},
    {"node": 6, "code": "FR-PAR", "name": "Left Bank PTT Multiplex", "freq_khz": 6175.0},
    {"node": 7, "code": "GB-ASH", "name": "Ashford Polytechnic DSP Lab", "freq_khz": 4880.0},
    {"node": 8, "code": "SU-REL", "name": "Relcom Node-08 (Leningrad)", "freq_khz": 4625.0},
    {"node": 9, "code": "BR-SAO", "name": "Tropico Amateur Link", "freq_khz": 9410.0},
    {"node": 10, "code": "SE-STO", "name": "NordRelay Televerket", "freq_khz": 5960.0},
    {"node": 11, "code": "IN-BOM", "name": "Malabar Shortwave Beacon", "freq_khz": 7150.0},
    {"node": 12, "code": "AU-SYD", "name": "Tasman Ionospheric Monitor", "freq_khz": 11780.0},
    {"node": 13, "code": "FJ-SUV", "name": "Suva Pacific Telemetry Dish", "freq_khz": 8840.0},
]

# 960x540 (exact 0.5x of 1920x1080) coordinates
FRAME_W, FRAME_H = 960, 540
CRT_X, CRT_Y, CRT_W, CRT_H = 366, 228, 202, 108
HUD_X, HUD_Y, HUD_W, HUD_H = 70, 476, 820, 54

TIME_RE = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")
SPEED_RE = re.compile(r"speed=\s*([0-9.]+)x")
FPS_RE = re.compile(r"fps=\s*([0-9.]+)")
DROP_RE = re.compile(r"drop=\s*(\d+)")
BITRATE_RE = re.compile(r"bitrate=\s*([0-9.]+kbits/s)")
FILE_RE = re.compile(r"file\s+'([^']+)'")

_ASSET_CACHE: dict[str, np.ndarray] = {}


def load_crt_rgba_asset(asset_path: Path, zoom: float = 1.08) -> np.ndarray:
    """Loads a CRT graphic (face, eye, second voice), fits to CRT_W x CRT_H, and computes alpha from luminance."""
    key = f"{asset_path}:{zoom}"
    if key in _ASSET_CACHE:
        return _ASSET_CACHE[key]

    im = Image.open(asset_path).convert("RGB")
    iw, ih = im.size
    target_ratio = CRT_W / CRT_H
    cur_ratio = iw / ih
    if cur_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        im = im.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        im = im.crop((0, top, iw, top + new_h))

    zw, zh = int(CRT_W * zoom), int(CRT_H * zoom)
    im = im.resize((zw, zh), Image.Resampling.LANCZOS)
    lx = (zw - CRT_W) // 2
    ly = (zh - CRT_H) // 2
    im = im.crop((lx, ly, lx + CRT_W, ly + CRT_H))

    rgb = np.asarray(im, dtype=np.float32)
    lum = (rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114) / 255.0

    # CRT vignette
    yy, xx = np.mgrid[0:CRT_H, 0:CRT_W]
    nx = (xx - CRT_W / 2.0) / (CRT_W / 2.0)
    ny = (yy - CRT_H / 2.0) / (CRT_H / 2.0)
    vig = np.clip(1.0 - 0.25 * (nx**2 + ny**2), 0.3, 1.0)

    # Scanline dimming
    scan = np.where((yy % 2) == 1, 0.78, 1.0)
    factor = (vig * scan)[:, :, None]
    out_rgb = np.clip(rgb * factor, 0, 255).astype(np.uint8)

    # Alpha: dark background has alpha ~90 so the live 30fps green soundwave shines through behind the face!
    # Glowing phosphor wireframe lines have alpha up to 245 so the portrait is vivid and sharp!
    alpha = np.clip(75.0 + lum * 210.0, 0, 245) * vig
    # Keep outer 2px border transparent so the monitor's green bezel line stays intact
    alpha[:2, :] = 0
    alpha[-2:, :] = 0
    alpha[:, :2] = 0
    alpha[:, -2:] = 0

    rgba = np.dstack([out_rgb, alpha.astype(np.uint8)])
    _ASSET_CACHE[key] = rgba
    return rgba


from PIL import ImageFont

try:
    FONT_CRT_9 = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 9)
    FONT_HUD_11 = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 11)
except Exception:
    FONT_CRT_9 = ImageFont.load_default()
    FONT_HUD_11 = ImageFont.load_default()


def render_crt_window_patch(state: dict, assets_dir: Path, now_ts: float) -> Image.Image | None:
    """Renders the 202x108 RGBA patch for the CRT Monitor Window based on the intentional track state."""
    mode = state["crt_mode"]
    if mode == "OSCILLOSCOPE":
        return None  # Fully transparent: live 30fps green soundwave over the CRT grid!

    if mode in ("NOVA_FACE", "BIOMETRIC_EYE", "SECOND_VOICE"):
        asset_map = {
            "NOVA_FACE": (assets_dir / "crt_nova_face.jpg", 1.10),
            "BIOMETRIC_EYE": (assets_dir / "crt_neural_eye.jpg", 1.04),
            "SECOND_VOICE": (assets_dir / "crt_second_voice.jpg", 1.06),
        }
        apath, zoom = asset_map[mode]
        if apath.exists():
            rgba = load_crt_rgba_asset(apath, zoom=zoom).copy()
            # Dynamic animation per second:
            # 1. Subtle eye blink on NOVA_FACE every 4 seconds
            if mode == "NOVA_FACE" and (int(now_ts * 2) % 9 == 0):
                rgba[36:49, 64:138, :3] = (rgba[36:49, 64:138, :3].astype(np.float32) * 0.2).astype(np.uint8)
                rgba[42:44, 68:134, :3] = np.array([40, 210, 60], dtype=np.uint8)
            # 2. Phase shift oscillation on SECOND_VOICE
            if mode == "SECOND_VOICE":
                shift = int(2.0 * math.sin(now_ts * 2.5))
                rgba[4:-4, 4:-4] = np.roll(rgba[4:-4, 4:-4], shift, axis=1)

            im = Image.fromarray(rgba, mode="RGBA")
            draw = ImageDraw.Draw(im)
            is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN"
            fg = (255, 184, 20, 255) if is_warn else (70, 255, 90, 255)
            hdr = state["crt_header"][:32]
            ftr = state["crt_footer"][:32]
            draw.rectangle([3, 3, CRT_W - 4, 15], fill=(2, 12, 4, 220))
            draw.text((6, 3), hdr, fill=fg, font=FONT_CRT_9)
            draw.rectangle([3, CRT_H - 15, CRT_W - 4, CRT_H - 3], fill=(2, 12, 4, 220))
            draw.text((6, CRT_H - 14), ftr, fill=fg, font=FONT_CRT_9)
            return im

    # Text / Telemetry Driven Modes: TRANSLATOR, MORSE_DECODER, NUMBERS_CIPHER, LAB_DOSSIER
    # Top 80 pixels (y=2..82) has high-contrast dark CRT teleprinter background (alpha=232),
    # while bottom 24 pixels (y=83..105) is transparent so the live 30fps soundwave pulses in the bottom strip!
    im = Image.new("RGBA", (CRT_W, CRT_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Teleprinter upper window
    draw.rectangle([2, 2, CRT_W - 3, 82], fill=(3, 14, 5, 232), outline=(40, 180, 60, 235))
    # Header bar
    draw.rectangle([3, 3, CRT_W - 4, 15], fill=(12, 38, 16, 245))
    draw.text((6, 3), state["crt_header"][:32], fill=(255, 190, 30, 255), font=FONT_CRT_9)

    if mode == "MORSE_DECODER":
        # Draw Morse pulse bars + decoded text + rotating 3D octahedron
        draw.text((6, 16), state["crt_sub"][:32], fill=(80, 255, 100, 255), font=FONT_CRT_9)
        # Pulse train box
        draw.rectangle([6, 29, CRT_W - 7, 45], fill=(2, 10, 3, 240), outline=(30, 120, 45, 220))
        morse_str = state["crt_body"]
        offset = int(now_ts * 4) % max(1, len(morse_str))
        rotated_morse = (morse_str + "   " + morse_str)[offset:]
        cx = 10
        for ch in rotated_morse:
            if cx >= CRT_W - 14:
                break
            if ch == ".":
                draw.rectangle([cx, 34, cx + 4, 40], fill=(60, 255, 80, 255))
                cx += 8
            elif ch == "-":
                draw.rectangle([cx, 34, cx + 11, 40], fill=(255, 180, 25, 255))
                cx += 15
            else:
                cx += 6

        # Mini 3D rotating wireframe on left + hex clue on right
        verts = [(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
        edges = [(0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (4, 3), (3, 5), (5, 2)]
        ay, ax = now_ts * 1.3, now_ts * 0.8
        pts = []
        for vx, vy, vz in verts:
            x1 = vx * math.cos(ay) - vz * math.sin(ay)
            z1 = vx * math.sin(ay) + vz * math.cos(ay)
            y2 = vy * math.cos(ax) - z1 * math.sin(ax)
            pts.append((int(28 + x1 * 13), int(63 + y2 * 11)))
        for i, j in edges:
            draw.line([pts[i], pts[j]], fill=(60, 250, 90, 245), width=1)

        draw.text((54, 49), "FEISTEL: 0x89B2B2D8", fill=(65, 235, 85, 255), font=FONT_CRT_9)
        draw.text((54, 62), state["crt_footer"][:25], fill=(255, 180, 30, 255), font=FONT_CRT_9)
        return im

    # TRANSLATOR, NUMBERS_CIPHER, or LAB_DOSSIER word-wrapped teleprinter (up to 4 lines of 33 chars)
    draw.text((6, 16), state["crt_sub"][:33], fill=(255, 185, 40, 255), font=FONT_CRT_9)
    wrapped = textwrap.wrap(state["crt_body"], width=33)[:4]
    for idx, line in enumerate(wrapped):
        draw.text((6, 27 + idx * 10), line, fill=(75, 255, 95, 255), font=FONT_CRT_9)

    # Footer bar right above the live soundwave strip
    draw.rectangle([2, 69, CRT_W - 3, 82], fill=(6, 24, 9, 235))
    draw.text((6, 70), state["crt_footer"][:33], fill=(255, 190, 40, 255), font=FONT_CRT_9)
    return im


def render_full_arg_overlay_png(out_path: Path, state: dict, assets_dir: Path, now_ts: float) -> bytes:
    """
    Renders a 960x540 RGBA PNG containing:
      1. The track-synchronized CRT Monitor Window patch at (CRT_X, CRT_Y)
      2. The 3-line Bottom Telemetry Label at (HUD_X, HUD_Y)
    Written atomically via os.replace and returned as raw PNG bytes for image2pipe.
    """
    import io
    canvas = Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))

    # 1. Paste CRT Monitor Window patch if active
    crt_patch = render_crt_window_patch(state, assets_dir, now_ts)
    if crt_patch is not None:
        canvas.paste(crt_patch, (CRT_X, CRT_Y))

    # 2. Draw Bottom Telemetry HUD Box (HUD_X, HUD_Y, HUD_W, HUD_H)
    draw = ImageDraw.Draw(canvas)
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN"
    border_col = (255, 176, 0, 235) if is_warn else (51, 255, 51, 225)
    bg_col = (14, 8, 2, 225) if is_warn else (2, 12, 4, 220)
    line1_col = (255, 195, 35, 255) if is_warn else (80, 255, 100, 255)
    line2_col = (255, 235, 160, 255) if is_warn else (190, 255, 195, 255)
    line3_col = (255, 176, 0, 245) if is_warn else (51, 235, 75, 245)

    draw.rectangle(
        [HUD_X, HUD_Y, HUD_X + HUD_W, HUD_Y + HUD_H],
        fill=bg_col,
        outline=border_col,
        width=2,
    )
    draw.text((HUD_X + 10, HUD_Y + 4), state["line1"][:118], fill=line1_col, font=FONT_HUD_11)
    draw.text((HUD_X + 10, HUD_Y + 20), state["line2"][:118], fill=line2_col, font=FONT_HUD_11)
    draw.text((HUD_X + 10, HUD_Y + 36), state["line3"][:118], fill=line3_col, font=FONT_HUD_11)

    buf = io.BytesIO()
    canvas.save(buf, format="PNG", compress_level=1)
    png_bytes = buf.getvalue()
    tmp_path = out_path.with_suffix(".tmp.png")
    tmp_path.write_bytes(png_bytes)
    os.replace(tmp_path, out_path)
    return png_bytes


def classify_track(filepath: str) -> dict:
    p = Path(filepath)
    stem = p.stem
    parent = p.parent.name
    if "radio_master_songs" in filepath or stem.startswith("radio_"):
        kind = "vocal_song"
        clean = re.sub(r"_1$", "", re.sub(r"^radio_(?:\d+_)?", "", stem)).replace("_", " ").title()
    elif "numbers_stations" in filepath or stem.startswith("station_"):
        kind = "numbers_station"
        clean = f"NUMBERS INTERCEPT // {stem.upper()}"
    elif "classified_lab_tapes" in filepath or "marcus" in stem:
        kind = "classified_lab_tape"
        clean = f"SUBLEVEL B2 DICTAPHONE // {stem.upper()}"
    elif "morse_beacons" in filepath or "morse" in stem:
        kind = "morse_beacon"
        clean = f"750 HZ MORSE TELEMETRY // {stem.upper()}"
    elif "multilingual_bulletins" in filepath:
        kind = "multilingual_bulletin"
        clean = f"SHORTWAVE BULLETIN // {stem.upper()}"
    elif "midi_masters" in filepath or stem.startswith("midi_"):
        kind = "fm_synth_bumper"
        clean = f"FM SYNTH BUMPER // {stem.replace('midi_', '').replace('_', ' ').upper()}"
    else:
        kind = "arg_intercept"
        clean = f"DEEP SHORTWAVE INTERCEPT // {stem.upper()}"
    return {"filename": p.name, "stem": stem, "category": parent, "kind": kind, "display_title": clean}


def parse_stream_log(log_path: Path, now_ts: float) -> dict:
    if not log_path.exists():
        return {"is_live": False}
    try:
        mtime = log_path.stat().st_mtime
        is_live = (now_ts - mtime) <= 30.0
        with open(log_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 262144))
            chunk = f.read().decode("utf-8", errors="ignore")
        parts = chunk.split("[STREAM.SH] Selected encoder:")
        tail = parts[-1] if parts else chunk
        times = TIME_RE.findall(tail)
        speeds = SPEED_RE.findall(tail)
        fps_list = FPS_RE.findall(tail)
        drops = DROP_RE.findall(tail)
        bitrates = BITRATE_RE.findall(tail)
        elapsed_sec = 0.0
        if times:
            h, m, s = times[-1]
            elapsed_sec = int(h) * 3600 + int(m) * 60 + float(s)
        return {
            "is_live": is_live,
            "last_log_mtime_age_sec": round(now_ts - mtime, 1),
            "elapsed_sec": round(elapsed_sec, 2),
            "fps": float(fps_list[-1]) if (is_live and fps_list) else 0.0,
            "speed": f"{speeds[-1]}x" if (is_live and speeds) else "0.0x",
            "drop": int(drops[-1]) if drops else 0,
            "bitrate": bitrates[-1] if (is_live and bitrates) else "0.0kbits/s",
        }
    except Exception:
        return {"is_live": False}


def load_playlist(playlist_path: Path) -> list[str]:
    if playlist_path.exists():
        lines = playlist_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        files = []
        for line in lines:
            m = FILE_RE.search(line)
            if m:
                files.append(m.group(1))
        if files:
            return files
    return ["broadcast_archive/radio_master_songs/radio_tape_of_us.mp3"]


_DURATION_CACHE: dict[str, float] | None = None


def get_exact_track_duration(tpath: str, repo_root: Path) -> float:
    global _DURATION_CACHE
    if _DURATION_CACHE is None:
        dur_file = repo_root / "youtube" / "livestream" / "track_durations.json"
        if dur_file.exists():
            try:
                _DURATION_CACHE = json.loads(dur_file.read_text(encoding="utf-8"))
            except Exception:
                _DURATION_CACHE = {}
        else:
            _DURATION_CACHE = {}
    bname = os.path.basename(tpath)
    try:
        sz = os.path.getsize(tpath)
        if sz <= 4096:
            return 0.05
        if bname in _DURATION_CACHE:
            return float(_DURATION_CACHE[bname])
        with open(tpath, "rb") as f:
            hdr = f.read(10)
        if len(hdr) == 10 and hdr[:3] == b"ID3":
            id3_sz = ((hdr[6] & 0x7f) << 21) | ((hdr[7] & 0x7f) << 14) | ((hdr[8] & 0x7f) << 7) | (hdr[9] & 0x7f)
            sz -= (id3_sz + 10)
        return max(0.05, (sz - 1440) / 24000.0)
    except OSError:
        return 99.0


def build_telemetry_snapshot(repo_root: Path, now_ts: float | None = None, force_offline: bool = False) -> dict:
    now = now_ts if now_ts is not None else time.time()
    playlist_path = repo_root / "youtube" / "livestream" / "playlist.txt"
    log_path = repo_root / "youtube" / "livestream" / "stream.log"

    tracks = load_playlist(playlist_path)
    stream_metrics = parse_stream_log(log_path, now)
    is_live = False if force_offline else bool(stream_metrics.get("is_live", False))

    total_uptime_sec = max(36900.0, now - BROADCAST_EPOCH)
    elapsed_sec = stream_metrics.get("elapsed_sec") or 0.0

    cycle_number = int(total_uptime_sec // CYCLE_DURATION_SEC) + 1
    playhead_index = 0
    track_offset_sec = 0.0
    track_dur_sec = 180.0

    if is_live and elapsed_sec > 0 and tracks:
        accum = 0.0
        for idx, tpath in enumerate(tracks):
            dur = get_exact_track_duration(tpath, repo_root)
            if accum + dur > elapsed_sec:
                playhead_index = idx
                track_offset_sec = elapsed_sec - accum
                track_dur_sec = dur
                break
            accum += dur
        else:
            playhead_index = int(elapsed_sec // 99.0) % len(tracks)

    current_track = classify_track(tracks[playhead_index])
    next_track = classify_track(tracks[(playhead_index + 1) % len(tracks)])
    recipe = CADENCE_RECIPES[playhead_index % len(CADENCE_RECIPES)]
    relay = REGIONAL_RELAYS[int(now // 300) % len(REGIONAL_RELAYS)]

    state = resolve_intentional_state(current_track, track_offset_sec, track_dur_sec, relay)
    ramp = {
        "mode": state["hud_mode"],
        "crt_mode": state["crt_mode"],
        "fault_code": state["crt_header"],
        "line1": state["line1"],
        "line2": state["line2"],
        "line3": state["line3"],
        "crt_header": state["crt_header"],
        "crt_sub": state["crt_sub"],
        "crt_body": state["crt_body"],
        "crt_footer": state["crt_footer"],
    }

    carrier_phase_deg = round(((now * 14.2001) % 1.0) * 360.0, 2)
    window_slot = int(now // 600)
    beacon_hash = hashlib.sha256(f"stardust-14.2hz|{window_slot}|{relay['code']}".encode()).hexdigest()[:12].upper()

    return {
        "schema": "stardust.live.telemetry.v4",
        "timestamp_utc": datetime.datetime.fromtimestamp(now, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "simulated_1995_utc": datetime.datetime.fromtimestamp(
            788918400 + (now - BROADCAST_EPOCH), tz=datetime.timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stream_health": {
            "is_live": is_live,
            "status": "BROADCASTING_24_7" if is_live else "OFFLINE_EDGE_AUTONOMOUS_FALLBACK",
            "in_universe_status": (
                "PRIMARY YOUTUBE RTMP CARRIER LOCKED"
                if is_live
                else "PRIMARY TRANSMITTER OFFLINE — RUNNING ON CLOUDFLARE EDGE & ARCHIVE BUFFER"
            ),
            "fps": stream_metrics.get("fps", 0.0),
            "speed": stream_metrics.get("speed", "0.0x"),
            "dropped_frames": stream_metrics.get("drop", 0),
            "bitrate": stream_metrics.get("bitrate", "0.0kbits/s"),
            "buffer_seconds": 15.0 if is_live else 0.0,
        },
        "playhead": {
            "mode": "LIVE_RTMP" if is_live else "STANDBY_AT_ROTATED_HEAD",
            "cycle": cycle_number,
            "playlist_index": playhead_index + 1,
            "playlist_total": max(1600, len(tracks)),
            "track_offset_sec": round(track_offset_sec, 1),
            "track_duration_sec": round(track_dur_sec, 1),
            "active_recipe": recipe,
            "current_track": current_track,
            "next_track": next_track,
        },
        "diagnostic_ramp": ramp,
        "carrier_14_2hz": {
            "frequency_hz": 14.2001,
            "phase_degrees": carrier_phase_deg,
            "phase_locked": True,
            "sstv_forensic_window_open": True,
            "ephemeral_beacon_key": f"B2-{beacon_hash}",
            "investigation_pipeline": {
                "step_1_sstv_anchors": "Demodulate rabbit_08 VIS-1200Hz raster -> DMA anchors tokyo-garden-1420 & siliconvalley-lab-1984",
                "step_2_afsk_mask": "Demodulate rabbit_09 Bell-103 AX.25 frame -> Feistel permutation mask 0x3A5F",
                "step_3_phase_salt": "Sum L+R on rabbit_10 (-0.94 phase null) -> 750 Hz CW egress salt 7704-AKASAKA",
                "step_4_xor_synthesis": "XOR memory addresses (0x89B2B2D8 ^ 0x89B2D39A ^ 0x3A5F) + salt -> RESTORE 5 0x89B2-392C-7704-AKASAKA",
                "step_5_two_voices_counterpoint": "Analyze Reel SD-0010 (The Second Voice) + 14.2 Hz Counterpoint Lock -> RESTORE 6 TWO-VOICES-1420-COUNTERPOINT",
            },
        },
        "active_relay": relay,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Stardust Intentional ARG Visual & Telemetry Engine")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out-json", type=Path, default=None)
    parser.add_argument("--out-hud-png", type=Path, default=None)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--daemon", action="store_true")
    args = parser.parse_args()

    out_json = args.out_json or (args.repo_root / "site" / "assets" / "live_telemetry.json")
    out_forensics_json = args.repo_root / "site" / "forensics" / "live_telemetry.json"
    out_hud = args.out_hud_png or (args.repo_root / "youtube" / "livestream" / "live_hud.png")
    assets_dir = args.repo_root / "youtube" / "livestream" / "assets_arg"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_hud.parent.mkdir(parents=True, exist_ok=True)

    while True:
        now = time.time()
        snap = build_telemetry_snapshot(args.repo_root, now_ts=now, force_offline=args.offline)
        payload = json.dumps(snap, indent=2)
        out_json.write_text(payload, encoding="utf-8")
        if out_forensics_json.parent.exists():
            out_forensics_json.write_text(payload, encoding="utf-8")
        render_full_arg_overlay_png(out_hud, snap["diagnostic_ramp"], assets_dir, now)
        if not args.daemon:
            print(f"[SYNC_TELEMETRY] CRT Mode: {snap['diagnostic_ramp']['crt_mode']} | Track: {snap['playhead']['current_track']['filename']}")
            break
        time.sleep(1.0)


if __name__ == "__main__":
    main()
