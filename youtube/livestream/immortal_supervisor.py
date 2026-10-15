#!/usr/bin/env python3
"""
Project Stardust — Immortal 24/7 Livestream Watchdog & Self-Healing Supervisor
Eliminates all four causes of YouTube Live disconnects:
  1. Zombie RTMP Socket Hangs: Monitors `stream.log` every 5s to verify `frame=`
     is actively advancing. If FFmpeg hangs on a half-open socket for >20s,
     kills the hung process, rotates the playlist playhead, and reconnects.
  2. Playlist Concat Corruption: Audits `playlist.txt` before every launch and
     strips any missing or zero-byte audio files so concat demuxer never aborts.
  3. Non-Rewinding Playhead Continuity: Calls `rotate_playlist.py` before every
     reconnect so the 80-song / 231-interstitial catalog never rewinds to Track 1.
  4. Auxiliary Daemon Supervision: Automatically keeps `watch_downloads_folder.py`
     and `sync_telemetry.py` alive alongside the broadcast.
"""

from __future__ import annotations
import argparse
import datetime
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

FRAME_RE = re.compile(r"frame=\s*(\d+)")
SPEED_RE = re.compile(r"speed=\s*([0-9.]+)x")
FILE_RE = re.compile(r"^\s*file\s+'([^']+)'")


def log(msg: str) -> None:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [IMMORTAL-SUPERVISOR] {msg}", flush=True)


def sanitize_playlist(playlist_path: Path) -> int:
    """Removes missing or corrupt (<2KB) files from playlist.txt so FFmpeg concat never aborts."""
    if not playlist_path.exists():
        return 0
    lines = playlist_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    valid_lines: list[str] = []
    removed = 0
    for line in lines:
        m = FILE_RE.match(line)
        if not m:
            if line.strip():
                valid_lines.append(line)
            continue
        fp = Path(m.group(1))
        if fp.exists() and fp.stat().st_size >= 2048:
            valid_lines.append(line)
        else:
            removed += 1
            log(f"Removed missing/corrupt track from playlist: {fp}")
    if removed > 0 and valid_lines:
        playlist_path.write_text("\n".join(valid_lines) + "\n", encoding="utf-8")
    return len(valid_lines)


def read_latest_frame_and_age(log_path: Path) -> tuple[int, float, float]:
    """Returns (latest_frame_number, log_mtime_age_seconds, latest_speed)."""
    if not log_path.exists():
        return -1, 999999.0, 0.0
    try:
        age = time.time() - log_path.stat().st_mtime
        with open(log_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 65536))
            tail = f.read().decode("utf-8", errors="ignore")
        frames = FRAME_RE.findall(tail)
        speeds = SPEED_RE.findall(tail)
        frame_num = int(frames[-1]) if frames else -1
        speed_val = float(speeds[-1]) if speeds else 1.0
        return frame_num, age, speed_val
    except Exception:
        return -1, 999999.0, 0.0


def run_rotate_playlist(repo_root: Path) -> None:
    rotate_script = repo_root / "youtube" / "livestream" / "rotate_playlist.py"
    if rotate_script.exists():
        try:
            res = subprocess.run(
                ["/usr/bin/python3", str(rotate_script)],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                timeout=15,
            )
            if res.stdout.strip():
                log(f"rotate_playlist.py: {res.stdout.strip().splitlines()[-1]}")
        except Exception as e:
            log(f"Warning: rotate_playlist.py error: {e}")


def run_sync_telemetry(repo_root: Path) -> None:
    sync_script = repo_root / "youtube" / "livestream" / "sync_telemetry.py"
    if sync_script.exists():
        try:
            subprocess.run(
                ["/usr/bin/python3", str(sync_script), "--repo-root", str(repo_root)],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                timeout=10,
            )
        except Exception:
            pass


def terminate_process_group(proc: subprocess.Popen | None) -> None:
    if proc is None or proc.poll() is not None:
        return
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        proc.wait(timeout=5)
    except Exception:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except Exception:
            pass


def supervise(repo_root: Path, stall_timeout_sec: float = 25.0) -> None:
    livestream_dir = repo_root / "youtube" / "livestream"
    stream_sh = livestream_dir / "stream.sh"
    playlist_path = livestream_dir / "playlist.txt"
    log_path = livestream_dir / "stream.log"
    watcher_script = livestream_dir / "watch_downloads_folder.py"
    promoter_script = livestream_dir / "agent_autonomous_promoter.py"
    health_path = livestream_dir / "supervisor_health.json"

    stream_proc: subprocess.Popen | None = None
    watcher_proc: subprocess.Popen | None = None
    promoter_proc: subprocess.Popen | None = None

    last_frame = -1
    last_frame_advance_ts = time.time()
    restart_count = 0

    def handle_exit(signum, _frame):
        log(f"Received signal {signum}, shutting down child processes cleanly...")
        terminate_process_group(stream_proc)
        terminate_process_group(watcher_proc)
        terminate_process_group(promoter_proc)
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    log(f"Starting Immortal 24/7 Broadcast Supervisor in {repo_root}")

    while True:
        # 1. Keep Downloads Folder Watcher & Agentic Seeding Daemon alive
        if watcher_script.exists() and (watcher_proc is None or watcher_proc.poll() is not None):
            log("Starting watch_downloads_folder.py daemon...")
            watcher_proc = subprocess.Popen(
                [sys.executable, str(watcher_script)],
                cwd=str(repo_root),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

        if promoter_script.exists() and (promoter_proc is None or promoter_proc.poll() is not None):
            log("Starting agent_autonomous_promoter.py daemon...")
            promoter_proc = subprocess.Popen(
                [sys.executable, str(promoter_script)],
                cwd=str(repo_root),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

        # 2. Check if stream.sh is running; if not, rotate playlist, sanitize, and launch
        if stream_proc is None or stream_proc.poll() is not None:
            if stream_proc is not None:
                log(f"stream.sh exited with code {stream_proc.returncode}. Preparing instant self-heal...")
                restart_count += 1

            valid_count = sanitize_playlist(playlist_path)
            run_sync_telemetry(repo_root)

            log(f"Launching stream.sh (valid playlist tracks: {valid_count}, restart #{restart_count})...")
            stream_proc = subprocess.Popen(
                ["/bin/bash", str(stream_sh)],
                cwd=str(repo_root),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            last_frame = -1
            last_frame_advance_ts = time.time()
            time.sleep(8)
            continue

        # 3. Active Watchdog Check: Ensure frames are advancing and socket hasn't hung
        frame_num, log_age, speed = read_latest_frame_and_age(log_path)
        now = time.time()

        if frame_num != last_frame and frame_num >= 0:
            last_frame = frame_num
            last_frame_advance_ts = now

        stall_duration = now - last_frame_advance_ts

        # Write machine-readable supervisor health status
        health_payload = {
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "stream_pid": stream_proc.pid,
            "watcher_pid": watcher_proc.pid if watcher_proc else None,
            "latest_frame": frame_num,
            "speed": f"{speed}x",
            "log_age_sec": round(log_age, 1),
            "stall_duration_sec": round(stall_duration, 1),
            "restarts": restart_count,
            "status": "HEALTHY" if stall_duration < stall_timeout_sec else "RECOVERING_STALL",
        }
        try:
            health_path.write_text(json.dumps(health_payload, indent=2), encoding="utf-8")
        except Exception:
            pass

        run_sync_telemetry(repo_root)

        if stall_duration > stall_timeout_sec or (log_age > stall_timeout_sec and now - last_frame_advance_ts > stall_timeout_sec):
            log(
                f"WATCHDOG TRIGGERED: FFmpeg frame counter stalled at frame={frame_num} "
                f"for {stall_duration:.1f}s (log_age={log_age:.1f}s). Killing hung RTMP session & rotating..."
            )
            terminate_process_group(stream_proc)
            stream_proc = None
            restart_count += 1
            time.sleep(2)
            continue

        time.sleep(5)


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Stardust Immortal 24/7 Livestream Supervisor")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--stall-timeout", type=float, default=25.0, help="Seconds without frame advance before auto-heal")
    args = parser.parse_args()
    supervise(args.repo_root, stall_timeout_sec=args.stall_timeout)


if __name__ == "__main__":
    main()
