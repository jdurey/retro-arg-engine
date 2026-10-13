#!/bin/bash
# 24/7 Autonomous YouTube Live Streamer for Project Stardust
# Usage: ./stream.sh <YOUR_YOUTUBE_STREAM_KEY>

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STREAM_KEY="${1:-$YOUTUBE_STREAM_KEY}"

if [ -z "$STREAM_KEY" ]; then
    echo "=========================================================="
    echo "ERROR: YouTube Stream Key is required!"
    echo "Usage: ./stream.sh <YOUR_STREAM_KEY>"
    echo "Or set: export YOUTUBE_STREAM_KEY='xxxx-xxxx-xxxx-xxxx-xxxx'"
    echo "You can get your Stream Key from:"
    echo "  https://studio.youtube.com/channel/UCQ2nHAazpB_HIiiQCPqFm1w/livestreaming"
    echo "=========================================================="
    exit 1
fi

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
    caffeinate -d -i -m -s -u \
    ffmpeg -stream_loop -1 -re -i "$BACKDROP" \
        -f concat -safe 0 -stream_loop -1 -i "$PLAYLIST" \
        -filter_complex "[1:a]aresample=async=1000[a];[a]showwaves=s=404x214:mode=line:colors=lime:draw=full:scale=cbrt:r=30[wave];[wave]colorkey=0x000000:0.05:0.1[wave_trans];[0:v][wave_trans]overlay=x=731:y=456:eof_action=repeat:shortest=0:repeatlast=1[v]" \
        -map "[v]" -map 1:a \
        -c:v h264_videotoolbox -b:v 5500k -realtime 1 -prio_speed 1 -pix_fmt yuv420p -g 60 -keyint_min 60 \
        -c:a aac -b:a 192k -ar 44100 -ac 2 \
        -flvflags no_duration_filesize \
        -f flv "$RTMP_URL" || true

    echo "Stream disconnected. Reconnecting in 5 seconds..."
    sleep 5
done
