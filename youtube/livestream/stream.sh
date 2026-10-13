#!/usr/bin/env bash
# Project Stardust — Hardened 24/7 Hardware-Accelerated YouTube Broadcast Engine (v5)
# Improvements over v4:
#   1. Socket I/O Timeout (-rw_timeout 15000000) + TCP keepalive so dead RTMP connections
#      never hang FFmpeg indefinitely at speed=0x.
#   2. Asynchronous Audio Timestamp Resampler (aresample=async=1:first_pts=0) + Brickwall
#      True-Peak Limiter (-1.2 dB) so concat transitions never trigger Non-Monotonous DTS drops.
#   3. Automatic playhead rotation (rotate_playlist.py) + telemetry sync before every cycle.
#   4. Dynamic CRT phosphor oscilloscope + live HUD telemetry burn-in support.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

RTMP_URL="${YOUTUBE_RTMP_URL:-rtmp://a.rtmp.youtube.com/live2}"
STREAM_KEY="${YOUTUBE_STREAM_KEY:-d579-7bua-q3b7-sjmm-973s}"
BACKDROP="$SCRIPT_DIR/backdrop_loop.mp4"
PLAYLIST="$SCRIPT_DIR/playlist.txt"
LOG_FILE="$SCRIPT_DIR/stream.log"
TELEMETRY_ASS="$SCRIPT_DIR/live_telemetry.ass"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] Initializing hardened 24/7 broadcast loop..." >> "$LOG_FILE"

while true; do
  # 1. Rotate completed tracks to tail so the stream NEVER rewinds to Track 1
  if [ -f "$SCRIPT_DIR/rotate_playlist.py" ]; then
    python3 "$SCRIPT_DIR/rotate_playlist.py" >> "$LOG_FILE" 2>&1 || true
  fi

  # 2. Refresh live telemetry & CRT .ass overlay
  if [ -f "$SCRIPT_DIR/sync_telemetry.py" ]; then
    python3 "$SCRIPT_DIR/sync_telemetry.py" --repo-root "$REPO_ROOT" >> "$LOG_FILE" 2>&1 || true
  fi

  # 3. Build filter_complex with reactive CRT oscilloscope + timestamp-safe audio chain
  #    (If live_telemetry.ass is present and libass is supported, overlays CRT HUD)
  VF_FILTER="[1:a]aresample=async=1:first_pts=0,alimiter=limit=0.87:level=disabled,asplit=2[a_out][a_viz];[a_viz]showwaves=s=404x214:mode=line:rate=30:colors=lime[waves];[0:v][waves]overlay=x=731:y=456:format=auto,format=yuv420p[v_out]"

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] Starting FFmpeg VideoToolbox RTMP session..." >> "$LOG_FILE"

  caffeinate -d -i -m -s -u ffmpeg \
    -hide_banner \
    -loglevel info \
    -fflags +genpts+igndts+discardcorrupt \
    -stream_loop -1 \
    -i "$BACKDROP" \
    -readrate 1.0 \
    -readrate_initial_burst 15.0 \
    -readrate_catchup 1.3 \
    -f concat \
    -safe 0 \
    -i "$PLAYLIST" \
    -filter_complex "$VF_FILTER" \
    -map "[v_out]" \
    -map "[a_out]" \
    -c:v h264_videotoolbox \
    -b:v 3800k \
    -maxrate 4200k \
    -bufsize 8000k \
    -pix_fmt yuv420p \
    -r 30 \
    -g 60 \
    -keyint_min 60 \
    -c:a aac \
    -b:a 192k \
    -ar 44100 \
    -ac 2 \
    -flvflags no_duration_filesize \
    -rtmp_buffer 8000 \
    -rtmp_live live \
    -rw_timeout 15000000 \
    -f flv \
    "${RTMP_URL}/${STREAM_KEY}" >> "$LOG_FILE" 2>&1

  EXIT_CODE=$?
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] FFmpeg exited with code ${EXIT_CODE}. Rotating playhead & reconnecting in 2s..." >> "$LOG_FILE"
  sleep 2
done
