#!/usr/bin/env bash
# Project Stardust — Hardened 24/7 YouTube Broadcast Engine with Intentional ARG CRT & HUD (v6.0)
# Key reliability & intentional ARG upgrades:
#   1. 540p30 Ultra-Stable Widescreen (`960x540` @ 260 kbps video + 160 kbps audio):
#      Cuts pixel count by 75% vs 1080p and 44% vs 720p while keeping razor-sharp 16:9 CRT text.
#   2. Intentional Track-Synchronized CRT Monitor + Bottom Telemetry HUD (`hud_pipe_feeder.py` -> `image2pipe`):
#      Streams 1.0 Hz RGBA PNG overlays over a drift-free monotonic pipe directly into FFmpeg:
#        - Live English translations inside the CRT monitor for all 52 foreign broadcasts & intercepts
#        - 750 Hz CW Morse Demodulator + 3D Wireframe Polyhedron + ASCII decode for all 35 Morse beacons
#        - 5-Digit One-Time-Pad Cipher Matrix for all 60 Numbers Stations
#        - Sublevel B2 Dictaphone Reel Dossier for all 25 Classified Lab Tapes
#        - Nova Hart's 1985 CRT Digital Face, Second Voice Dual-Carrier Anomaly, & Biometric Iris Lock
#          composited transparently over the live 30fps green soundwave (`colorkey` + per-pixel alpha)
#        - Bottom Telemetry Label (`HUD`) with track-specific solvable ARG clues & terminal commands
#   3. Socket I/O Timeout (`-rw_timeout 15000000`) + Async PTS Resampler (`aresample=44100:async=1`).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

RTMP_URL="${YOUTUBE_RTMP_URL:-rtmp://a.rtmp.youtube.com/live2}"
STREAM_KEY="${YOUTUBE_STREAM_KEY:-d579-7bua-q3b7-sjmm-973s}"
BACKDROP="$SCRIPT_DIR/backdrop_loop_540p.mp4"
PLAYLIST="$SCRIPT_DIR/playlist.txt"
LOG_FILE="$SCRIPT_DIR/stream.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] Initializing hardened 24/7 intentional ARG broadcast loop (540p30)..." >> "$LOG_FILE"

while true; do
  # 1. Rotate completed tracks to tail BEFORE truncating stream.log so the stream NEVER rewinds to Track 1
  if [ -f "$SCRIPT_DIR/rotate_playlist.py" ]; then
    /usr/bin/python3 "$SCRIPT_DIR/rotate_playlist.py" >> "$LOG_FILE" 2>&1 || true
  fi

  # 2. Cap stream.log at 10 MB (keep last 2 MB) AFTER rotate_playlist reads elapsed time
  if [ -f "$LOG_FILE" ] && [ "$(stat -f%z "$LOG_FILE" 2>/dev/null || echo 0)" -gt 10485760 ]; then
    tail -c 2097152 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
  fi

  # 3. Refresh initial telemetry & CRT/HUD overlay before pipeline launch
  if [ -f "$SCRIPT_DIR/sync_telemetry.py" ]; then
    /usr/bin/python3 "$SCRIPT_DIR/sync_telemetry.py" --repo-root "$REPO_ROOT" >> "$LOG_FILE" 2>&1 || true
  fi

  VF_FILTER="[1:a]aresample=44100:async=1,aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,alimiter=limit=0.87:level=disabled,asplit=2[a_out][a_viz];[a_viz]showwaves=s=202x108:mode=line:rate=30:colors=lime,colorkey=0x000000:0.06:0.08[waves];[0:v][waves]overlay=x=366:y=228:format=auto[v_osc];[v_osc][2:v]overlay=x=0:y=0:format=auto:eof_action=repeat,format=yuv420p[v_out]"

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] Selected encoder: 540p30 Intentional ARG CRT/HUD Engine (260k video + 160k audio)" >> "$LOG_FILE"

  /usr/bin/python3 -u "$SCRIPT_DIR/hud_pipe_feeder.py" --repo-root "$REPO_ROOT" | caffeinate -d -i -m -s -u ffmpeg \
    -hide_banner \
    -loglevel info \
    -reinit_filter 0 \
    -fflags +genpts+igndts+discardcorrupt \
    -stream_loop -1 \
    -i "$BACKDROP" \
    -readrate 1.0 \
    -readrate_initial_burst 3.0 \
    -readrate_catchup 1.15 \
    -f concat \
    -safe 0 \
    -i "$PLAYLIST" \
    -thread_queue_size 64 \
    -f image2pipe \
    -vcodec png \
    -framerate 1 \
    -i - \
    -filter_complex "$VF_FILTER" \
    -map "[v_out]" \
    -map "[a_out]" \
    -c:v libx264 \
    -preset veryfast \
    -tune zerolatency \
    -b:v 260k \
    -maxrate 300k \
    -bufsize 600k \
    -pix_fmt yuv420p \
    -r 30 \
    -g 60 \
    -keyint_min 60 \
    -c:a aac \
    -b:a 160k \
    -ar 44100 \
    -ac 2 \
    -flvflags no_duration_filesize \
    -rtmp_buffer 3000 \
    -rtmp_live live \
    -rw_timeout 15000000 \
    -f flv \
    "${RTMP_URL}/${STREAM_KEY}" >> "$LOG_FILE" 2>&1

  EXIT_CODE=$?
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] FFmpeg exited with code ${EXIT_CODE}. Rotating playhead & reconnecting in 2s..." >> "$LOG_FILE"
  sleep 2
done
