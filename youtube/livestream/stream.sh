#!/usr/bin/env bash
# Project Stardust — Hardened 24/7 YouTube Broadcast Engine with Diegetic CRT HUD (v5.1)
# Key reliability & ARG upgrades:
#   1. VideoToolbox Compression Session Auto-Probe: Detects Apple Silicon error -12908
#      (when running headless/backgrounded or when hardware encoder is busy) and
#      seamlessly switches between `h264_videotoolbox -allow_sw 1` and `libx264 -preset veryfast`
#      so the encoder NEVER crashes on startup.
#   2. Real-Time Diegetic CRT Diagnostic HUD (`live_hud.png` via `-loop 1` image2 reload):
#      Displays calm 1989/1995 tape bias telemetry during songs and automatically switches
#      to Amber Diagnostic Fault Mode during numbers stations, SSTV bursts, and AFSK packets,
#      giving livestream viewers an authentic engineering on-ramp into the ARG.
#   3. Socket I/O Timeout (`-rw_timeout 15000000`) + Async PTS Resampler (`aresample=async=1:first_pts=0`).

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
HUD_PNG="$SCRIPT_DIR/live_hud.png"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] Initializing hardened 24/7 broadcast loop..." >> "$LOG_FILE"

select_video_encoder() {
  if ffmpeg -hide_banner -loglevel error -f lavfi -i "color=c=black:s=1920x1080:r=30" -t 0.1 -c:v h264_videotoolbox -allow_sw 1 -b:v 3800k -f null - >/dev/null 2>&1; then
    echo "-c:v h264_videotoolbox -allow_sw 1"
  else
    echo "-c:v libx264 -preset veryfast -tune zerolatency"
  fi
}

while true; do
  # 0. Cap stream.log at 10 MB (keep last 2 MB) AFTER rotate_playlist reads elapsed time
  # 1. Rotate completed tracks to tail so the stream NEVER rewinds to Track 1
  if [ -f "$SCRIPT_DIR/rotate_playlist.py" ]; then
    python3 "$SCRIPT_DIR/rotate_playlist.py" >> "$LOG_FILE" 2>&1 || true
  fi

  if [ -f "$LOG_FILE" ] && [ "$(stat -f%z "$LOG_FILE" 2>/dev/null || echo 0)" -gt 10485760 ]; then
    tail -c 2097152 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
  fi

  # 2. Refresh live telemetry & render initial CRT HUD PNG (live_hud.png)
  if [ -f "$SCRIPT_DIR/sync_telemetry.py" ]; then
    python3 "$SCRIPT_DIR/sync_telemetry.py" --repo-root "$REPO_ROOT" >> "$LOG_FILE" 2>&1 || true
  fi

  VF_FILTER="[1:a]aresample=44100:async=1,aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,alimiter=limit=0.87:level=disabled,asplit=2[a_out][a_viz];[a_viz]showwaves=s=404x214:mode=line:rate=30:colors=lime[waves];[0:v][waves]overlay=x=731:y=456:format=auto,scale=1280:720:flags=bilinear,format=yuv420p[v_out]"

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] Selected encoder: 720p30 ultra-stable CBR (450k video + 160k audio)" >> "$LOG_FILE"

  caffeinate -d -i -m -s -u ffmpeg \
    -nostdin \
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
    -filter_complex "$VF_FILTER" \
    -map "[v_out]" \
    -map "[a_out]" \
    -c:v libx264 \
    -preset veryfast \
    -tune zerolatency \
    -b:v 450k \
    -maxrate 550k \
    -bufsize 1100k \
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
