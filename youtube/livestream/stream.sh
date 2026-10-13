#!/bin/bash
# 24/7 Autonomous YouTube Live Streamer for Project Stardust
# Usage: ./stream.sh <YOUR_YOUTUBE_STREAM_KEY>

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STREAM_KEY="${1:-${YOUTUBE_STREAM_KEY:-d579-7bua-q3b7-sjmm-973s}}"

python3 "$DIR/build_playlist.py"

BACKDROP="$DIR/backdrop_loop.mp4"
PLAYLIST="$DIR/playlist.txt"
RTMP_URL="rtmp://a.rtmp.youtube.com/live2/$STREAM_KEY"

echo "=========================================================="
echo " Starting 24/7 Live Broadcast: 14.2 Hz Carrier Signal"
echo " Bitrate Target: 5500 Kbps (YouTube 1080p 30fps Hardware Accelerated)"
echo " Audio Waveform: Real-Time CRT Oscilloscope Reactive Display"
echo " Anti-Sleep: caffeinate active"
echo " Stream will run continuously with auto-reconnect..."
echo " Press Ctrl+C to terminate."
echo "=========================================================="

while true; do
    # Only generate playlist if missing (preserves playhead across reconnects)
    if [ ! -f "$PLAYLIST" ]; then
        python3 "$DIR/build_playlist.py" || true
    fi

    caffeinate -d -i -m -s -u \
    ffmpeg -stream_loop -1 -i "$BACKDROP" \
        -readrate 1.0 -readrate_initial_burst 15.0 -readrate_catchup 1.3 \
        -f concat -safe 0 -i "$PLAYLIST" \
        -filter_complex "[1:a]aresample=44100:async=1000,asplit=2[a_out][a_wave];[a_wave]showwaves=s=404x214:mode=line:colors=lime:draw=full:scale=cbrt:r=30[wave];[wave]colorkey=0x000000:0.05:0.1[wave_trans];[0:v][wave_trans]overlay=x=731:y=456:eof_action=repeat:shortest=0:repeatlast=1[v]" \
        -map "[v]" -map "[a_out]" \
        -c:v h264_videotoolbox -b:v 3800k -maxrate 4200k -bufsize 8000k -realtime 1 -prio_speed 1 -pix_fmt yuv420p -r 30 -g 60 -keyint_min 60 \
        -c:a aac -b:a 192k -ar 44100 -ac 2 \
        -rtmp_buffer 8000 -rtmp_live live \
        -flvflags no_duration_filesize+no_sequence_end \
        -f flv "$RTMP_URL" 2>&1 | tee -a "$DIR/stream.log" || true

    echo "Stream disconnected. Reconnecting in 1 second..."
    sleep 1
done
