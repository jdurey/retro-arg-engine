#!/usr/bin/env python3
"""Autonomous Folder Watcher Daemon for Project Stardust Livestream.
Continuously watches '/Users/joshuadurey/Downloads/For Live Stream'.

Whenever the user drops a new song (.wav, .mp3, .flac, .aiff, etc.) into the folder:
1. Waits for file download/export to complete.
2. Automatically ingests and masters it to 192k 44.1kHz stereo MP3 with zero silence.
3. Automatically updates playlist.txt.
4. Smoothly signals the livestream to incorporate the new track into active rotation.
"""

import os
import sys
import time
import subprocess
from ingest_download_songs import ingest_all, DOWNLOADS_DIR

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_SCRIPT = os.path.join(HERE, "build_playlist.py")

def get_folder_state():
    if not os.path.exists(DOWNLOADS_DIR):
        return {}
    state = {}
    for f in os.listdir(DOWNLOADS_DIR):
        if f.startswith("."):
            continue
        p = os.path.join(DOWNLOADS_DIR, f)
        if os.path.isfile(p):
            state[f] = (os.path.getmtime(p), os.path.getsize(p))
    return state

def reload_stream():
    """Smoothly restarts ffmpeg or stream.sh to pick up updated playlist.txt with zero downtime."""
    try:
        # Check if stream.sh is running
        stream_sh_pids = []
        try:
            stream_sh_pids = subprocess.check_output(["pgrep", "-f", "stream.sh"]).decode().split()
        except subprocess.CalledProcessError:
            pass

        # Check running ffmpeg
        ffmpeg_pids = []
        try:
            ffmpeg_pids = subprocess.check_output(["pgrep", "-f", "ffmpeg.*rtmp://a.rtmp.youtube.com"]).decode().split()
        except subprocess.CalledProcessError:
            pass

        if stream_sh_pids:
            for pid in ffmpeg_pids:
                pid = pid.strip()
                if pid:
                    subprocess.run(["kill", "-9", pid])
            print(f"[WATCHER]: Reloaded ffmpeg - stream.sh will restart broadcast in 1s!")
        else:
            for pid in ffmpeg_pids:
                pid = pid.strip()
                if pid:
                    subprocess.run(["kill", "-9", pid])
            print(f"[WATCHER]: stream.sh not running. Launching background stream.sh...")
            stream_sh_path = os.path.join(HERE, "stream.sh")
            subprocess.Popen(["bash", stream_sh_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=HERE)
            print(f"[WATCHER]: stream.sh launched successfully!")
    except Exception as e:
        print(f"[WATCHER]: Livestream reload notice: {e}")

def main():
    print(f"==========================================================")
    print(f" [AUTONOMOUS FOLDER WATCHER ACTIVE]")
    print(f" Monitoring: '{DOWNLOADS_DIR}'")
    print(f" Any new songs added will instantly join the live stream.")
    print(f"==========================================================")

    last_state = get_folder_state()

    while True:
        try:
            time.sleep(3)
            current_state = get_folder_state()

            # Check if any new file or file size change
            has_changes = False
            for fname, (mtime, size) in current_state.items():
                if fname not in last_state:
                    has_changes = True
                    break
                prev_mtime, prev_size = last_state[fname]
                if mtime > prev_mtime or size != prev_size:
                    has_changes = True
                    break

            if has_changes:
                # Wait 2 seconds to make sure write/export is finished
                time.sleep(2)
                print(f"\n[WATCHER]: Detected new or modified audio files in '{DOWNLOADS_DIR}'!")
                added = ingest_all()
                if added:
                    print(f"[WATCHER]: Ingested {len(added)} new song(s). Rebuilding playlist...")
                    subprocess.run(["python3", BUILD_SCRIPT], check=True)
                    reload_stream()
                    print(f"[WATCHER]: ✓ Livestream updated and broadcasting new lineup!\n")

                last_state = get_folder_state()

        except KeyboardInterrupt:
            print("\nFolder watcher stopped.")
            break
        except Exception as e:
            print(f"[WATCHER ERROR]: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
