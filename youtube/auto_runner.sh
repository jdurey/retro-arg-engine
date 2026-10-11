#!/bin/bash
# Autonomous background runner for Nova Hart YouTube description updates.
# Runs daily or retries when quota resets until 100% of videos are updated.

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$DIR")"

cd "$ROOT"
echo "=== NOVA HART YOUTUBE AUTOMATION RUNNER ==="
echo "Timestamp: $(date)"

# 1. Check for and sync any new uploads
"$DIR/.venv/bin/python3" "$DIR/yt.py" sync

# 2. Backfill full AI-translated titles & descriptions across catalog
"$DIR/.venv/bin/python3" "$DIR/yt.py" apply --translate

python3 -c '
import json, os
state = "youtube/state"
v_path = os.path.join(state, "videos.json")
d_path = os.path.join(state, "done.json")
t_path = os.path.join(state, "translated_done.json")
if os.path.exists(v_path):
    v = [x for x in json.load(open(v_path))["videos"] if x["status"]["privacyStatus"] != "private"]
    d = json.load(open(d_path)) if os.path.exists(d_path) else []
    t = json.load(open(t_path)) if os.path.exists(t_path) else []
    print(f"Status: {len(d)}/{len(v)} videos linked to ARG nodes.")
    print(f"Translations: {len(t)}/{len(v)} videos with full AI-translated titles & descriptions across 20 languages.")
'


