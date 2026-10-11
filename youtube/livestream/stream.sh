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

BACKDROP="$DIR/backdrop.jpg"
PLAYLIST="$DIR/playlist.txt"
RTMP_URL="rtmp://a.rtmp.youtube.com/live2/$STREAM_KEY"

echo "=========================================================="
echo " Starting 24/7 Live Broadcast: 14.2 Hz Carrier Signal"
echo " RTMP Endpoint: rtmp://a.rtmp.youtube.com/live2/****"
echo " Stream will run continuously with auto-reconnect..."
echo " Press Ctrl+C to terminate."
echo "=========================================================="

while true; do
    ffmpeg -re -loop 1 -framerate 30 -i "$BACKDROP" \
        -f concat -safe 0 -stream_loop -1 -i "$PLAYLIST" \
        -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
        -c:v libx264 -preset veryfast -b:v 3000k -maxrate 3500k -bufsize 7000k \
        -pix_fmt yuv420p -g 60 -keyint_min 60 \
        -c:a aac -b:a 192k -ar 44100 -ac 2 \
        -f flv "$RTMP_URL" || true

    echo "Stream disconnected. Reconnecting in 5 seconds..."
    sleep 5
done

