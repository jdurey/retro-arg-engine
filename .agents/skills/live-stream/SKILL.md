---
name: live-stream
description: >-
  Autonomous 24/7 retro radio YouTube live streaming workflow.
  Use this skill whenever the user wants to start, configure, manage, or debug
  a 24/7 YouTube live stream, ingest new tracks, synthesize multilingual radio bulletins,
  or build zero-dead-air radio station playlists.
---

# Autonomous 24/7 Retro Radio Live Streaming Runbook

This skill provides an end-to-end operational guide and executable toolset for running a 24/7 retro radio YouTube live broadcast with real-time reactive audio oscilloscope visualization, zero dead air, multilingual interstitial bulletins, and automated new track ingestion.

---

## 1. Quick Start Commands

All commands are run from the project root directory (e.g. `retro_arg_engine/`):

### Start the Live Stream
```bash
# Using stream key argument:
./youtube/livestream/stream.sh <YOUR_YOUTUBE_STREAM_KEY>

# Or using environment variable:
export YOUTUBE_STREAM_KEY="xxxx-xxxx-xxxx-xxxx-xxxx"
./youtube/livestream/stream.sh
```

### Start the Autonomous Folder Watcher (Background Daemon)
Monitors `/Users/joshuadurey/Downloads/For Live Stream` and immediately masters, trims, and queues any new audio files into the live broadcast:
```bash
python3 youtube/livestream/watch_downloads_folder.py &
```

### Rebuild the Broadcast Playlist On-Demand
Scans and interleaves master songs, FM synth compositions, multilingual bulletins, and telemetry:
```bash
python3 youtube/livestream/build_playlist.py
```

### Smooth Stream Reload (Zero Downtime)
To reload ffmpeg with an updated playlist without terminating the outer `stream.sh` auto-reconnect supervisor:
```bash
kill $(pgrep -f "ffmpeg.*rtmp://a.rtmp.youtube.com")
# stream.sh will catch the exit and reconnect within 5 seconds
```

---

## 2. Broadcast System Architecture

```
[ Downloads Folder / Audio Sources ]
                │
                ▼ (Dynamic Ingest & Silence Trim)
[ broadcast_archive/radio_master_songs ] ──┐
[ broadcast_archive/midi_masters ]       ──┼──▶ [ build_playlist.py ]
[ broadcast_archive/multilingual_bulletins]─┤           │
[ broadcast_archive/morse_beacons ]       ──┘           ▼
                                                 [ playlist.txt ]
                                                        │
┌───────────────────────────┐                           │
│ backdrop_loop.mp4 (1080p) │                           │
└─────────────┬─────────────┘                           │
              │                                         ▼
              │                     ┌──────────────────────────────────────┐
              └────────────────────▶│ ffmpeg Hardware-Accelerated Pipeline │
                                    │ - Video: h264_videotoolbox (5500k)   │
                                    │ - Audio: 192k 44.1kHz AAC Stereo     │
                                    │ - Overlay: Reactive CRT Oscilloscope │
                                    └───────────────────┬──────────────────┘
                                                        │
                                                        ▼
                                       rtmp://a.rtmp.youtube.com/live2/<KEY>
```

---

## 3. Radio Clock-Wheel Cadence (Zero Dead Air)

The broadcast avoids repetitive clumping or awkward silences by interleaving audio through an authentic 1980s radio station clock-wheel format:

$$\text{[Master Song (3–4 min)]} \longrightarrow \text{[Multilingual Bulletin (6–10s)]} \longrightarrow \text{[Roland/Yamaha MIDI Master (30–60s)]} \longrightarrow \text{[Morse/Telemetry Burst (3–6s)]} \longrightarrow \text{[Master Song]}$$

* **Desynchronized Loop**: Song pools (56 songs), bulletin pools (92 spoken dispatches), and telemetry pools (107 signals) have different lengths. Tracks never align in the same combinations, providing over 26 hours of continuous unrepeated listening.
* **Double-Pass Silence Trimming**: Every audio track passes through a front-and-back silence trimmer to strip dead air:
  ```bash
  -af "silenceremove=start_periods=1:start_duration=0.04:start_threshold=-30dB:detection=peak,areverse,silenceremove=start_periods=1:start_duration=0.08:start_threshold=-30dB:detection=peak,areverse"
  ```

---

## 4. Synthesizing Interstitials & Telemetry

### A. Multilingual Radio Bulletins (18 Languages)
Generate atmospheric shortwave dispatches, marine weather advisories, and late-night station IDs using macOS native speech synthesis coupled with 1980s telephone/AM bandpass filters:
```bash
# Generate voice
say -v Kyoko -o /tmp/voice.aiff "こちらはエフエム東京。ただいまの時刻は午前三時をお知らせいたします。"

# Filter voice through 1980s radio telephone curve
ffmpeg -y -i /tmp/voice.aiff \
  -af "highpass=f=180,lowpass=f=4200,volume=1.4,silenceremove=start_periods=1:start_duration=0.02:start_threshold=-35dB:detection=peak,areverse,silenceremove=start_periods=1:start_duration=0.05:start_threshold=-35dB:detection=peak,areverse" \
  -c:a libmp3lame -b:a 192k -ar 44100 -ac 1 output.mp3
```

### B. DTMF Touch-Tone Dialing Bursts
Synthesize mathematical dual-sine telephone dialing tones using NumPy:
$$\text{Tone}(t) = (\sin(2\pi f_1 t) + \sin(2\pi f_2 t)) \times 0.25$$
Frequencies: Row `(697, 770, 852, 941 Hz)`, Column `(1209, 1336, 1477 Hz)`. 80ms tone with 40ms pause.

### C. Morse Code Spectrogram Telemetry
Generate crisp 750 Hz Morse telemetry bursts (2.5s to 6.5s) at -12dB level to avoid dead air gaps.

---

## 5. Streaming & Video Pipeline Configuration

The stream is configured for continuous 24/7 reliability on macOS:

* **Hardware Video Encoding**: Apple Silicon VideoToolbox (`-c:v h264_videotoolbox -b:v 5500k -prio_speed 1`).
* **Audio Resampling**: `-filter_complex "[1:a]aresample=async=1000[a]"` guarantees perfect audio/video clock sync without frame drops over days of streaming.
* **Chroma Key Reactive Oscilloscope**:
  ```text
  [a]showwaves=s=404x214:mode=line:colors=lime:draw=full:scale=cbrt:r=30[wave];
  [wave]colorkey=0x000000:0.05:0.1[wave_trans];
  [0:v][wave_trans]overlay=x=731:y=456:eof_action=repeat:shortest=0:repeatlast=1[v]
  ```
* **Anti-Sleep Protection**: Supervised by `caffeinate -d -i -m -s -u` to prevent system sleep or display idle downclocking.
* **Auto-Reconnect Loop**: `stream.sh` catches any RTMP disconnects and seamlessly reconnects within 5 seconds.

---

## 6. Process Monitoring & Health Check

Check running stream components:
```bash
ps aux | grep -E "(stream\.sh|ffmpeg|watch_downloads)" | grep -v grep
```
Ensure 3 processes are active:
1. `stream.sh` (Supervisor)
2. `caffeinate ... ffmpeg` (Active RTMP streamer)
3. `watch_downloads_folder.py` (Automated ingester)
