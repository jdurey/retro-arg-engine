#!/bin/bash
# Autonomous background runner for Nova Hart YouTube description updates.
# Runs daily or retries when quota resets until 100% of videos are updated.

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$DIR")"

cd "$ROOT"
echo "=== NOVA HART YOUTUBE AUTOMATION RUNNER ==="
echo "Timestamp: $(date)"

"$DIR/.venv/bin/python3" "$DIR/yt.py" apply

python3 -c '
import json, os
state = "youtube/state"
v_path = os.path.join(state, "videos.json")
d_path = os.path.join(state, "done.json")
if os.path.exists(v_path) and os.path.exists(d_path):
    v = [x for x in json.load(open(v_path))["videos"] if x["status"]["privacyStatus"] != "private"]
    d = json.load(open(d_path))
    print(f"Status: {len(d)}/{len(v)} videos updated.")
'
