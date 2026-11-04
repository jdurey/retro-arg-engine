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

export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:/usr/bin:/bin:/usr/sbin:/sbin"

PYTHON_BIN="/usr/bin/python3"
for cand in "/opt/homebrew/bin/python3" "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3" "/usr/local/bin/python3" "/usr/bin/python3"; do
  if [ -x "$cand" ] && "$cand" -c "import PIL, numpy" >/dev/null 2>&1; then
    PYTHON_BIN="$cand"
    break
  fi
done

RTMP_URL="${YOUTUBE_RTMP_URL:-rtmp://a.rtmp.youtube.com/live2}"
STREAM_KEY="${YOUTUBE_STREAM_KEY:-d579-7bua-q3b7-sjmm-973s}"
BACKDROP="$SCRIPT_DIR/backdrop_loop.mp4"
PLAYLIST="$SCRIPT_DIR/playlist.txt"
LOG_FILE="$SCRIPT_DIR/stream.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] Initializing hardened 24/7 intentional ARG broadcast loop (1080p30 Full HD, python=$PYTHON_BIN)..." >> "$LOG_FILE"

while true; do
  # 0. Normalize playlist paths to local REPO_ROOT and filter out any missing files so FFmpeg concat never exits 254
  "$PYTHON_BIN" -c '
import re, sys
from pathlib import Path
pl = Path(sys.argv[1])
root = Path(sys.argv[2])
if pl.exists():
    out = []
    for ln in pl.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"^\s*file\s+\x27([^\x27]+)\x27", ln)
        if m:
            raw = m.group(1)
            fp = Path(raw)
            if not fp.exists() and "/retro_arg_engine/" in raw:
                fp = root / raw.split("/retro_arg_engine/", 1)[1]
            if fp.exists() and fp.stat().st_size >= 2048:
                out.append(f"file \x27{fp}\x27")
        elif ln.strip():
            out.append(ln)
    if out:
        pl.write_text("\n".join(out) + "\n", encoding="utf-8")
' "$PLAYLIST" "$REPO_ROOT" >> "$LOG_FILE" 2>&1 || true

  # 1. Rotate completed tracks to tail BEFORE truncating stream.log so the stream NEVER rewinds to Track 1
  if [ -f "$SCRIPT_DIR/rotate_playlist.py" ]; then
    "$PYTHON_BIN" "$SCRIPT_DIR/rotate_playlist.py" >> "$LOG_FILE" 2>&1 || true
  fi

  # 2. Cap stream.log at 10 MB (keep last 2 MB) AFTER rotate_playlist reads elapsed time
  if [ -f "$LOG_FILE" ] && [ "$(stat -f%z "$LOG_FILE" 2>/dev/null || echo 0)" -gt 10485760 ]; then
    tail -c 2097152 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
  fi

  # 3. Refresh initial telemetry & CRT/HUD overlay before pipeline launch
  if [ -f "$SCRIPT_DIR/sync_telemetry.py" ]; then
    "$PYTHON_BIN" "$SCRIPT_DIR/sync_telemetry.py" --repo-root "$REPO_ROOT" >> "$LOG_FILE" 2>&1 || true
  fi

  PIPE_DIR="$HOME/.stardust_pipes"
  mkdir -p -m 700 "$PIPE_DIR"
  CRT_FIFO="$PIPE_DIR/stardust_crt_30fps.y4m"
  TALKBACK_FIFO="$PIPE_DIR/stardust_talkback_44k.s16le"
  pkill -f "crt_loop_feeder.py" 2>/dev/null || true
  pkill -f "talkback_pipe_feeder.py" 2>/dev/null || true
  rm -f "$CRT_FIFO" "$TALKBACK_FIFO" "/tmp/stardust_crt_30fps.y4m" "/tmp/stardust_talkback_44k.s16le"
  mkfifo "$CRT_FIFO" "$TALKBACK_FIFO"

  VF_FILTER="[1:a]aresample=44100:async=1,aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,alimiter=limit=0.87:level=disabled,asplit=2[a_music][a_viz_m];[4:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,asplit=3[tb_sc][tb_mix][tb_viz];[a_music][tb_sc]sidechaincompress=threshold=0.008:ratio=12:attack=25:release=650:level_sc=3.0[a_ducked];[a_ducked][tb_mix]amix=inputs=2:weights=1 1.18:normalize=0,alimiter=limit=0.92:level=disabled[a_out];[a_viz_m][tb_viz]amix=inputs=2:weights=1 1.45:normalize=0,pan=mono|c0=0.5*c0+0.5*c1,volume=1.9,treble=g=8:f=3500,showfreqs=s=56x32:mode=bar:ascale=cbrt:fscale=log:win_size=1024:averaging=2:rate=30:colors=0xeff8ff@0.82,lagfun=decay=0.45,scale=1344:128:flags=neighbor,drawgrid=w=24:h=128:t=6:c=0x000000@0.0:replace=1,drawgrid=w=1344:h=8:t=3:c=0x000000@0.0:replace=1,format=yuva420p[waves];[0:v][waves]overlay=x=288:y=744:format=yuv420[v_osc];[3:v]scale=1728:928:flags=neighbor[crt_fg];[v_osc][crt_fg]overlay=x=96:y=76:format=yuv420[v_crt];[v_crt][2:v]overlay=x=0:y=0:format=yuv420:eof_action=repeat,format=yuv420p[v_out]"

  ENCODER_ARGS=(-c:v libx264 -preset veryfast -threads 4 -x264-params "nal-hrd=cbr:force-cfr=1")

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] Selected encoder: 1080p30 Full HD Intentional ARG CRT/HUD + Live Talkback Engine (${ENCODER_ARGS[*]})" >> "$LOG_FILE"

  "$PYTHON_BIN" -u "$SCRIPT_DIR/crt_loop_feeder.py" --repo-root "$REPO_ROOT" --fifo "$CRT_FIFO" &
  CRT_FEEDER_PID=$!
  "$PYTHON_BIN" -u "$SCRIPT_DIR/talkback_pipe_feeder.py" --repo-root "$REPO_ROOT" --fifo "$TALKBACK_FIFO" &
  TB_FEEDER_PID=$!
  trap 'kill "$CRT_FEEDER_PID" "$TB_FEEDER_PID" 2>/dev/null || true; exit 0' INT TERM
  trap 'kill "$CRT_FEEDER_PID" "$TB_FEEDER_PID" 2>/dev/null || true' EXIT

  "$PYTHON_BIN" -u "$SCRIPT_DIR/hud_pipe_feeder.py" --repo-root "$REPO_ROOT" | caffeinate -d -i -m -s -u ffmpeg \
    -hide_banner \
    -loglevel info \
    -reinit_filter 0 \
    -fflags +genpts+igndts+discardcorrupt \
    -stream_loop -1 \
    -i "$BACKDROP" \
    -readrate 1.0 \
    -readrate_initial_burst 0.5 \
    -readrate_catchup 1.15 \
    -f concat \
    -safe 0 \
    -i "$PLAYLIST" \
    -thread_queue_size 8 \
    -threads 2 \
    -probesize 32768 \
    -analyzeduration 0 \
    -f image2pipe \
    -vcodec png \
    -framerate 1 \
    -i - \
    -thread_queue_size 16 \
    -f rawvideo \
    -pix_fmt yuva420p \
    -video_size 864x464 \
    -framerate 30 \
    -i "$CRT_FIFO" \
    -thread_queue_size 64 \
    -f s16le \
    -ar 44100 \
    -ac 2 \
    -i "$TALKBACK_FIFO" \
    -filter_complex_threads 4 \
    -filter_complex "$VF_FILTER" \
    -map "[v_out]" \
    -map "[a_out]" \
    "${ENCODER_ARGS[@]}" \
    -b:v 6600k \
    -minrate 6600k \
    -maxrate 6600k \
    -bufsize 13200k \
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
  kill "$CRT_FEEDER_PID" "$TB_FEEDER_PID" 2>/dev/null || true
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STREAM.SH] FFmpeg exited with code ${EXIT_CODE}. Rotating playhead & reconnecting in 2s..." >> "$LOG_FILE"
  sleep 2
done
