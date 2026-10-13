#!/usr/bin/env python3
"""
Project Stardust — Bi-Directional Livestream Telemetry & Diegetic CRT HUD Renderer
Reads active FFmpeg stream.log and playlist.txt, computes exact playhead state,
and writes:
  1. site/assets/live_telemetry.json (Web & Cloudflare Edge synchronization)
  2. youtube/livestream/live_hud.png (Real-time 8x8 VGA bitmap CRT Diagnostic HUD
     overlaid onto the 24/7 YouTube broadcast via atomic os.replace)
  3. youtube/livestream/live_telemetry.ass (Optional libass subtitle stream)
"""

from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
import re
import struct
import time
import zlib
from pathlib import Path

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

# Compact 5x7 / 8x8 VGA terminal glyph bitmaps for uppercase ASCII, digits, and punctuation
GLYPHS_5X7: dict[str, list[int]] = {
    " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "!": [0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04],
    '"': [0x0A, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00],
    "#": [0x0A, 0x1F, 0x0A, 0x0A, 0x1F, 0x0A, 0x00],
    "(": [0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02],
    ")": [0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08],
    "*": [0x00, 0x04, 0x15, 0x0E, 0x15, 0x04, 0x00],
    "+": [0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00],
    ",": [0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x08],
    "-": [0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00],
    ".": [0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C],
    "/": [0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10],
    "0": [0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E],
    "1": [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
    "2": [0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F],
    "3": [0x1F, 0x02, 0x04, 0x06, 0x01, 0x11, 0x0E],
    "4": [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
    "5": [0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E],
    "6": [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E],
    "7": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
    "8": [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
    "9": [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C],
    ":": [0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00],
    "=": [0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00],
    ">": [0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08],
    "[": [0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E],
    "]": [0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E],
    "_": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F],
    "A": [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "B": [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
    "C": [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E],
    "D": [0x1C, 0x12, 0x11, 0x11, 0x11, 0x12, 0x1C],
    "E": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
    "F": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
    "G": [0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F],
    "H": [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "I": [0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
    "J": [0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C],
    "K": [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
    "L": [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
    "M": [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
    "N": [0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11],
    "O": [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "P": [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
    "Q": [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
    "R": [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
    "S": [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
    "T": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    "U": [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "V": [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
    "W": [0x11, 0x11, 0x11, 0x15, 0x15, 0x15, 0x0A],
    "X": [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
    "Y": [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
    "Z": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
}

TIME_RE = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")
SPEED_RE = re.compile(r"speed=\s*([0-9.]+)x")
FPS_RE = re.compile(r"fps=\s*([0-9.]+)")
DROP_RE = re.compile(r"drop=\s*(\d+)")
BITRATE_RE = re.compile(r"bitrate=\s*([0-9.]+kbits/s)")
FILE_RE = re.compile(r"file\s+'([^']+)'")


def classify_track(filepath: str) -> dict:
    p = Path(filepath)
    stem = p.stem
    parent = p.parent.name
    if "radio_master_songs" in filepath or stem.startswith("radio_"):
        kind = "vocal_song"
        clean = re.sub(r"^radio_", "", stem).replace("_", " ").title()
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
        clean = f"MARINE / SHORTWAVE BULLETIN // {stem.upper()}"
    elif "midi_masters" in filepath or stem.startswith("midi_"):
        kind = "fm_synth_bumper"
        clean = f"FM SYNTH BUMPER // {stem.replace('midi_', '').replace('_', ' ').upper()}"
    else:
        kind = "arg_intercept"
        clean = f"DEEP SHORTWAVE INTERCEPT // {stem.upper()}"
    return {"filename": p.name, "stem": stem, "category": parent, "kind": kind, "display_title": clean}


def compute_diagnostic_ramp(current_track: dict, relay: dict) -> dict:
    """
    Produces a diegetic Sublevel B2 diagnostic log entry that gives observant
    livestream viewers a genuine engineering lead without ever breaking character
    or handing out a pre-solved password.
    """
    stem = current_track["stem"].lower()
    kind = current_track["kind"]

    if "rabbit_08" in stem or "sstv" in stem:
        return {
            "mode": "ANOMALY_WARN",
            "fault_code": "FAULT 0x08 // VIS-1200HZ RASTER",
            "line1": "[! FAULT 0x08] VIS-1200HZ RASTER BLEED ON BIAS SUB-CARRIER (1500-2300 HZ)",
            "line2": "DMA PARTITION ANCHORS -> DEMODULATE AT stardust-archive.net/forensics/signal_lab.html",
            "line3": "LOGGED BY: vax4000.ashford-poly.org // SEE SPOOL: stardust-archive.net/usenet/comp.dsp",
        }
    if "rabbit_09" in stem or "bell103" in stem or kind == "numbers_station":
        return {
            "mode": "ANOMALY_WARN",
            "fault_code": "FAULT 0x09 // BELL-103 AX.25",
            "line1": "[! FAULT 0x09] 110-BAUD BELL-103 AFSK PACKET (1270/1070 HZ) ON 4625 KHZ",
            "line2": "ORIGIN: RELCOM-NODE08 (LENINGRAD) // FEISTEL PERMUTATION MASK IN FRAME",
            "line3": "SPOOL ARCHIVE: stardust-archive.net/usenet/alt.conspiracy // FINGER op08@relcom-node08.org",
        }
    if "rabbit_10" in stem or "phase" in stem or kind in ("classified_lab_tape", "morse_beacon"):
        return {
            "mode": "ANOMALY_WARN",
            "fault_code": "FAULT 0x0A // CORR -0.94 PHASE NULL",
            "line1": "[! FAULT 0x0A] CH-L / CH-R PHASE CORRELATION = -0.94 (180 DEG DIFFERENTIAL)",
            "line2": "330/495/990 HZ CALIBRATION TRIAD CANCELS UNDER L+R MONO SUMMATION",
            "line3": "ISOLATE 750 HZ BIAS CW SALT -> stardust-archive.net/terminal (MEMO 89-114)",
        }
    return {
        "mode": "NOMINAL",
        "fault_code": "PARITY NOMINAL",
        "line1": f"ORION ARCHIVE B2 // 15 IPS NAB // BIAS CARRIER: 14.2001 HZ [LOCKED]",
        "line2": f"REEL: {current_track['display_title'][:42]} // NODE #{relay['node']:02d} {relay['code']}",
        "line3": "UUCP / HTTPd ARCHIVE MIRROR: stardust-archive.net // FEISTEL BUS: 0x89B2B2D8",
    }


def render_crt_hud_png(out_path: Path, ramp: dict) -> None:
    """
    Renders a 720x58 RGBA PNG with an authentic 5x7 CRT pixel font and scanline
    dimming, written atomically via os.replace so FFmpeg -loop 1 -i live_hud.png
    never reads a partial frame.
    """
    width, height = 720, 58
    buf = bytearray(width * height * 4)

    is_warn = ramp["mode"] == "ANOMALY_WARN"
    # Phosphor amber for diagnostic anomalies, phosphor green for nominal tape playback
    fg_r, fg_g, fg_b = (255, 176, 0) if is_warn else (51, 255, 51)
    bg_r, bg_g, bg_b = (14, 8, 2) if is_warn else (2, 10, 2)

    for y in range(height):
        scan = 0.78 if (y % 2 == 1) else 1.0
        row_off = y * width * 4
        border = y in (0, 1, height - 2, height - 1)
        for x in range(width):
            idx = row_off + x * 4
            if border or x in (0, 1, width - 2, width - 1):
                buf[idx] = int(fg_r * 0.7 * scan)
                buf[idx + 1] = int(fg_g * 0.7 * scan)
                buf[idx + 2] = int(fg_b * 0.7 * scan)
                buf[idx + 3] = 235
            else:
                buf[idx] = bg_r
                buf[idx + 1] = bg_g
                buf[idx + 2] = bg_b
                buf[idx + 3] = 215

    lines = [ramp["line1"][:56], ramp["line2"][:56], ramp["line3"][:56]]
    for line_idx, text in enumerate(lines):
        base_y = 7 + line_idx * 16
        base_x = 12
        for ch_idx, ch in enumerate(text.upper()):
            glyph = GLYPHS_5X7.get(ch, GLYPHS_5X7[" "])
            gx = base_x + ch_idx * 12
            if gx + 10 >= width - 4:
                break
            for row_i, row_bits in enumerate(glyph):
                for col_i in range(5):
                    if (row_bits >> (4 - col_i)) & 1:
                        # 2x2 pixel scaling for crisp 1080p readability
                        for dy in range(2):
                            for dx in range(2):
                                py = base_y + row_i * 2 + dy
                                px = gx + col_i * 2 + dx
                                if 0 <= py < height and 0 <= px < width:
                                    p_idx = (py * width + px) * 4
                                    scan = 0.85 if (py % 2 == 1) else 1.0
                                    buf[p_idx] = int(fg_r * scan)
                                    buf[p_idx + 1] = int(fg_g * scan)
                                    buf[p_idx + 2] = int(fg_b * scan)
                                    buf[p_idx + 3] = 255

    def png_chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = bytearray()
    stride = width * 4
    for y in range(height):
        raw.append(0)
        raw.extend(buf[y * stride : (y + 1) * stride])

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png_bytes = (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(bytes(raw), 6))
        + png_chunk(b"IEND", b"")
    )
    tmp_path = out_path.with_suffix(".tmp.png")
    tmp_path.write_bytes(png_bytes)
    os.replace(tmp_path, out_path)


def parse_stream_log(log_path: Path, now_ts: float) -> dict:
    if not log_path.exists():
        return {"is_live": False}
    try:
        mtime = log_path.stat().st_mtime
        is_live = (now_ts - mtime) <= 30.0
        with open(log_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 8192))
            tail = f.read().decode("utf-8", errors="ignore")
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
    candidates = [playlist_path, Path("/tmp/debug_playlist.txt"), Path("/tmp/test_playlist.txt")]
    for c in candidates:
        if c.exists():
            lines = c.read_text(encoding="utf-8", errors="ignore").splitlines()
            files = []
            for line in lines:
                m = FILE_RE.search(line)
                if m:
                    files.append(m.group(1))
            if files:
                return files
    return [
        "broadcast_archive/radio_master_songs/radio_tape_of_us.mp3",
        "intercepts/rabbit_08_sstv_b2_schematic.mp3",
        "broadcast_archive/numbers_stations/station_intercept_033.mp3",
        "broadcast_archive/radio_master_songs/radio_patterns_in_the_mesh.mp3",
        "intercepts/rabbit_09_bell103_relcom_packet.mp3",
        "intercepts/rabbit_10_phase_inverted_hart_stem.mp3",
    ]


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
    avg_item_sec = 99.0
    if is_live and elapsed_sec > 0:
        playhead_index = int(elapsed_sec // avg_item_sec) % len(tracks)
    else:
        playhead_index = 0

    current_track = classify_track(tracks[playhead_index])
    next_track = classify_track(tracks[(playhead_index + 1) % len(tracks)])
    recipe = CADENCE_RECIPES[playhead_index % len(CADENCE_RECIPES)]
    relay = REGIONAL_RELAYS[int(now // 300) % len(REGIONAL_RELAYS)]
    ramp = compute_diagnostic_ramp(current_track, relay)

    carrier_phase_deg = round(((now * 14.2001) % 1.0) * 360.0, 2)
    window_slot = int(now // 600)
    beacon_hash = hashlib.sha256(f"stardust-14.2hz|{window_slot}|{relay['code']}".encode()).hexdigest()[:12].upper()

    return {
        "schema": "stardust.live.telemetry.v3",
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
                "step_4_xor_synthesis": "XOR memory addresses (0x89B2B2D8 ^ 0x89B2D39A ^ 0x3A5F) + salt -> RESTORE 5 0x89B2-5BC8-7704-AKASAKA",
            },
        },
        "active_relay": relay,
    }


def generate_ass_overlay(telemetry: dict) -> str:
    ramp = telemetry["diagnostic_ramp"]
    header = """[Script Info]
Title: Project Stardust Live CRT Telemetry OSD
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CRT_HUD,Courier New,22,&H0033FF33,&H0000FF00,&H00051505,&H80020802,-1,0,0,0,100,100,1,0,1,1.5,0,7,60,60,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    return (
        header
        + f"Dialogue: 0,0:00:00.00,9:59:59.00,CRT_HUD,,0,0,0,,{{\\pos(580,960)}}{ramp['line1']}\\N{ramp['line2']}\\N{ramp['line3']}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Stardust Livestream Telemetry & Diegetic HUD Synchronizer")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out-json", type=Path, default=None)
    parser.add_argument("--out-ass", type=Path, default=None)
    parser.add_argument("--out-hud-png", type=Path, default=None)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--daemon", action="store_true")
    args = parser.parse_args()

    out_json = args.out_json or (args.repo_root / "site" / "assets" / "live_telemetry.json")
    out_ass = args.out_ass or (args.repo_root / "youtube" / "livestream" / "live_telemetry.ass")
    out_hud = args.out_hud_png or (args.repo_root / "youtube" / "livestream" / "live_hud.png")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_ass.parent.mkdir(parents=True, exist_ok=True)
    out_hud.parent.mkdir(parents=True, exist_ok=True)

    while True:
        snap = build_telemetry_snapshot(args.repo_root, force_offline=args.offline)
        out_json.write_text(json.dumps(snap, indent=2), encoding="utf-8")
        out_ass.write_text(generate_ass_overlay(snap), encoding="utf-8")
        render_crt_hud_png(out_hud, snap["diagnostic_ramp"])
        if not args.daemon:
            print(f"[SYNC_TELEMETRY] Status: {snap['stream_health']['status']}")
            print(f"  -> HUD Ramp Mode: {snap['diagnostic_ramp']['mode']} ({snap['diagnostic_ramp']['fault_code']})")
            print(f"  -> Wrote CRT HUD PNG: {out_hud} ({out_hud.stat().st_size} bytes)")
            break
        time.sleep(5)


if __name__ == "__main__":
    main()
