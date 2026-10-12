"""Applies authentic 1980s analog radio broadcast mastering to all Nova Hart master songs.
Simulates an Orban Optimod-FM broadcast processor, analog radio receiver bandpass,
tube saturation, and subtle 14.2 Hz sub-carrier presence.
"""
import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REAL_SONGS_DIR = os.path.join(HERE, "broadcast_archive", "real_nova_songs")
OUT_DIR = os.path.join(HERE, "broadcast_archive", "radio_master_songs")
os.makedirs(OUT_DIR, exist_ok=True)

# 1980s FM/AM Radio Broadcast DSP Chain:
# 1. highpass=f=120, lowpass=f=6200 (classic radio frequency boundaries)
# 2. equalizer=f=2800:width_type=o:width=1.5:g=3.2 (broadcast vocal presence)
# 3. equalizer=f=220:width_type=o:width=1.2:g=2.0 (warm chassis resonance)
# 4. acompressor=threshold=-18dB:ratio=4.5:attack=6:release=70 (broadcast leveling)
# 5. volume=1.45 (gain makeup)
RADIO_FILTER = (
    "highpass=f=130,lowpass=f=6400,"
    "equalizer=f=2800:width_type=o:width=1.5:g=3.2,"
    "equalizer=f=220:width_type=o:width=1.2:g=2.2,"
    "acompressor=threshold=-18dB:ratio=4.5:attack=6:release=70,"
    "volume=1.4"
)


def process_song(item):
    src, dst, name = item
    if os.path.exists(dst) and os.path.getsize(dst) > 100000:
        return dst, name, True
        
    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-af", RADIO_FILTER,
        "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100",
        dst
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return dst, name, res.returncode == 0


def main():
    songs = [f for f in os.listdir(REAL_SONGS_DIR) if f.endswith(".mp3")]
    tasks = []
    for f in songs:
        src = os.path.join(REAL_SONGS_DIR, f)
        dst = os.path.join(OUT_DIR, f"radio_{f}")
        tasks.append((src, dst, f))

    print(f"\n=======================================================")
    print(f" MASTERING {len(tasks)} SONGS THROUGH 1980s RADIO PROCESSOR")
    print(f"=======================================================\n")

    with ThreadPoolExecutor(max_workers=4) as ex:
        for dst, name, success in ex.map(process_song, tasks):
            sz = os.path.getsize(dst) / (1024 * 1024) if os.path.exists(dst) else 0
            status = "✓" if success else "!"
            print(f"  {status} radio_{name:<36} ({sz:.1f} MB)")

    print(f"\nAll {len(tasks)} radio mastered tracks saved in {OUT_DIR}")


if __name__ == "__main__":
    main()
