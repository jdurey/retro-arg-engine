#!/usr/bin/env python3
"""
Project Stardust — Bi-Directional Livestream Telemetry & CRT OSD Synchronizer
Reads active FFmpeg stream.log and playlist.txt (with deterministic epoch fallback),
detects whether the YouTube RTMP livestream is actively broadcasting or OFFLINE
(based on stream.log freshness < 30s or explicit --offline flag), and writes:
  1. site/assets/live_telemetry.json (for Web & Cloudflare Edge sync)
  2. youtube/livestream/live_telemetry.ass (dynamic CRT VT100 OSD overlay for FFmpeg)
"""

from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
import re
import time
from pathlib import Path

BROADCAST_EPOCH = 1791763200  # 2026-10-12T00:00:00Z
CYCLE_DURATION_SEC = 44 * 3600  # 44-hour non-repeating fair-rotation schedule
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
        "broadcast_archive/midi_masters/midi_analog_heartbeat_1984.mp3",
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

    # When offline, hold playhead at the last rotated head of playlist.txt (or Track #328 checkpoint)
    cycle_number = int(total_uptime_sec // CYCLE_DURATION_SEC) + 1
    avg_item_sec = 99.0
    if is_live and elapsed_sec > 0:
        playhead_index = int(elapsed_sec // avg_item_sec) % len(tracks)
    else:
        playhead_index = 0  # Head of rotated playlist.txt awaits next FFmpeg launch

    current_track = classify_track(tracks[playhead_index])
    next_track = classify_track(tracks[(playhead_index + 1) % len(tracks)])
    recipe = CADENCE_RECIPES[playhead_index % len(CADENCE_RECIPES)]
    relay = REGIONAL_RELAYS[int(now // 300) % len(REGIONAL_RELAYS)]

    carrier_phase_deg = round(((now * 14.2001) % 1.0) * 360.0, 2)
    window_slot = int(now // 600)
    beacon_hash = hashlib.sha256(f"stardust-14.2hz|{window_slot}|{relay['code']}".encode()).hexdigest()[:12].upper()

    return {
        "schema": "stardust.live.telemetry.v2",
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
        "carrier_14_2hz": {
            "frequency_hz": 14.2001,
            "phase_degrees": carrier_phase_deg,
            "phase_locked": True,
            "sstv_forensic_window_open": True,  # Always open in Signal Lab when primary RTMP is offline
            "ephemeral_beacon_key": f"B2-{beacon_hash}",
            "sector_5_unlock_code": "ASHFORD-KAMOME-1420",
        },
        "active_relay": relay,
    }


def generate_ass_overlay(telemetry: dict) -> str:
    """Generates an FFmpeg-compatible .ass CRT VT100 telemetry overlay for when stream.sh runs."""
    t = telemetry
    cur = t["playhead"]["current_track"]
    nxt = t["playhead"]["next_track"]
    relay = t["active_relay"]
    c14 = t["carrier_14_2hz"]
    health = t["stream_health"]

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
Style: CRT_ALERT,Courier New,20,&H0000B0FF,&H0000FFFF,&H00051505,&H80020802,-1,0,0,0,100,100,1,0,1,1.5,0,1,60,60,45,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    hud_line_1 = (
        f"ORION ARCHIVE RELAY // CYCLE #{t['playhead']['cycle']} "
        f"[TRACK #{t['playhead']['playlist_index']}/{t['playhead']['playlist_total']}] "
        f"// STATUS: {health['status']}"
    )
    hud_line_2 = f"QUEUED AT PLAYHEAD: {cur['display_title']} ({cur['kind'].upper()})"
    hud_line_3 = (
        f"CARRIER: {c14['frequency_hz']} HZ [PHASE {c14['phase_degrees']} DEG] "
        f"// NODE #{relay['node']:02d} {relay['code']} ({relay['freq_khz']} kHz)"
    )
    hud_line_4 = (
        f"SSTV/AFSK LAB: /forensics/signal_lab.html "
        f"// BEACON: {c14['ephemeral_beacon_key']} // NEXT: {nxt['display_title'][:38]}"
    )
    events = [
        f"Dialogue: 0,0:00:00.00,9:59:59.00,CRT_HUD,,0,0,0,,{{\\pos(731,690)}}{hud_line_1}\\N{hud_line_2}\\N{hud_line_3}",
        f"Dialogue: 0,0:00:00.00,9:59:59.00,CRT_ALERT,,0,0,0,,{{\\pos(731,785)}}{hud_line_4}",
    ]
    return header + "\n".join(events) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Stardust Livestream Telemetry Synchronizer")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out-json", type=Path, default=None)
    parser.add_argument("--out-ass", type=Path, default=None)
    parser.add_argument("--offline", action="store_true", help="Force offline status in telemetry snapshot")
    parser.add_argument("--daemon", action="store_true", help="Continuously update every 5 seconds")
    args = parser.parse_args()

    out_json = args.out_json or (args.repo_root / "site" / "assets" / "live_telemetry.json")
    out_ass = args.out_ass or (args.repo_root / "youtube" / "livestream" / "live_telemetry.ass")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_ass.parent.mkdir(parents=True, exist_ok=True)

    while True:
        snap = build_telemetry_snapshot(args.repo_root, force_offline=args.offline)
        out_json.write_text(json.dumps(snap, indent=2), encoding="utf-8")
        out_ass.write_text(generate_ass_overlay(snap), encoding="utf-8")
        if not args.daemon:
            print(f"[SYNC_TELEMETRY] Status: {snap['stream_health']['status']}")
            print(f"  -> Playhead Mode: {snap['playhead']['mode']} ({snap['playhead']['current_track']['display_title']})")
            print(f"  -> Beacon Key: {snap['carrier_14_2hz']['ephemeral_beacon_key']} | Relay: {snap['active_relay']['name']}")
            break
        time.sleep(5)


if __name__ == "__main__":
    main()
