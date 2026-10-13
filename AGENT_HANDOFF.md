# Project Stardust: Comprehensive Agent Handoff & Technical Architecture

> **Notice for Successor AI Agents:**  
> This document provides the complete technical architecture, operational runbooks, repository maps, and canon constraints for **Project Stardust** (Retro ARG Engine & 24/7 Autonomous YouTube Broadcast). Read this thoroughly before modifying code or restarting services.

---

## 1. System Overview & Active Health Status

As of **October 14, 2026**:
* **YouTube Live Stream:** **HEALTHY & BROADCASTING 24/7**
  - **Uptime:** Over 10 hours 15 minutes of uninterrupted continuous streaming (PID `95154`, running under `caffeinate`).
  - **Health Metrics:** `drop=0` (zero dropped frames), `fps=30.0` constant, `speed=1.0x` realtime sync, bitrate ~2,250–2,550 kbps.
  - **Current Playhead:** Track #328+ into Cycle 2 of the 44-hour non-repeating fair-rotation schedule.
  - **Active Daemons:**
    - Live streamer loop: `bash youtube/livestream/stream.sh` (PID `92145`)
    - Downloads folder watcher: `python3 youtube/livestream/watch_downloads_folder.py` (PID `84941`)
* **Online Web Presence:** **LIVE & INDEXED**
  - **Primary Domain:** [https://stardust-archive.net](https://stardust-archive.net) (routed via Cloudflare Worker `retro-arg-router`).
  - **Static Mirror / CDN Origin:** [https://jdurey.github.io/retro-arg-engine/](https://jdurey.github.io/retro-arg-engine/) (GitHub Pages auto-deployed from `main`).
  - **Human Web:** Hundreds of authentic 1990s GeoCities neighborhoods, Usenet newsgroup archives, interactive CRT terminal emulator, regional pressings, and alternate-universe media (Heartstrike band, Steel Thunder film).
  - **Agent Web:** 1.25 MB XML sitemap, automated IndexNow crawler submissions, temporal Wayback Machine preservation, and dynamic procedural ARG swarm capable of expanding to 300,000 algorithmic nodes.

---

## 2. Live Stream Architecture (`youtube/livestream/`)

The livestream broadcasts 24/7 to YouTube Live with an authentic 1980s computer terminal aesthetic, dynamic audio reactive CRT oscilloscope, and zero dead air.

### Key Components
1. **Hardware-Accelerated Encoding (`stream.sh`):**
   * Uses Apple Silicon VideoToolbox (`-c:v h264_videotoolbox`) at 1080p 30fps (`-b:v 3800k -maxrate 4200k -bufsize 8000k`).
   * **Anti-Lag Rate Control (FFmpeg 8):**
     `-readrate 1.0 -readrate_initial_burst 15.0 -readrate_catchup 1.3 -rtmp_buffer 8000 -rtmp_live live`
     Maintains a persistent **15-second socket pre-buffer** to eliminate viewer buffering and track transition stutter.
   * **Reactive Waveform Visualizer:** Real-time CRT oscilloscope line (`showwaves=s=404x214:colors=lime`) overlaid onto terminal screen coordinates (`x=731, y=456`).
   * **Anti-Sleep:** Wrapped in `caffeinate -d -i -m -s -u` so the stream continues if laptop display sleeps.

2. **Persistent Playhead & Anti-Repetition (`rotate_playlist.py`):**
   * Solves the classic concat demuxer rewind bug. Whenever FFmpeg disconnects or restarts:
     `rotate_playlist.py` inspects `stream.log` for elapsed time, determines which tracks completed, and rotates them from head to tail of `playlist.txt`.
   * **Guarantee:** The stream **never rewinds to track 1**; every song plays through the 80-track catalog before repeating (~5.3 hours minimum spacing).

3. **Autonomous Ingestion Daemon (`watch_downloads_folder.py`):**
   * Polls `/Users/joshuadurey/Downloads/For Live Stream` every 5 seconds.
   * When user drops in new `.mp3`/`.wav`/`.m4a` files:
     - Automatically applies 1980s radio broadcast EQ/DSP.
     - Saves master to `broadcast_archive/radio_master_songs/radio_<clean_stem>.mp3`.
     - Injects into the live playlist deck without resetting playback.

4. **Stream Credentials:**
   * **RTMP Endpoint:** `rtmp://a.rtmp.youtube.com/live2/`
   * **Default Stream Key:** `d579-7bua-q3b7-sjmm-973s` (configurable via `$YOUTUBE_STREAM_KEY`).

---

## 3. Audio Pipeline & Mastering Engine

All broadcast audio is standardized to **stereo 44.1 kHz 192 kbps MP3** with strict loudness calibration to eliminate dead air and jarring volume jumps.

### Mastering Profiles
1. **Radio Broadcast Vocal Songs (`RADIO_BROADCAST_FILTER`):**
   * **Highpass:** 130 Hz (removes sub-bass mud).
   * **Lowpass:** 6,400 Hz (authentic 1980s FM/AM broadcast cutoff).
   * **Warmth & Presence EQ:** +2.2 dB @ 220 Hz (analog transformer warmth), +3.2 dB @ 2.8 kHz (vocal intelligibility).
   * **Optimod Dynamic Leveling:** `compand` with -18 dB threshold, 4.5:1 ratio, 0.05s attack, 0.4s release, volume boost 1.4x.

2. **Archival Interstitials (`remaster_all_interstitials.py`):**
   * All 231 interstitials mastered to **EBU R128 standard (`loudnorm=I=-16:TP=-1.5:LRA=7`)**:
     * **60 Numbers Stations:** Phonetic voice code transmissions (`highpass=250`, `lowpass=3600`).
     * **25 Classified Lab Tapes:** Marcus Hale dictaphone recordings and Harrison security purge logs (`highpass=200`, `lowpass=4200`, cassette tape flutter).
     * **12 Deep ARG Intercepts:** UVB-76 Russian buzzer bursts, CERN 1989 whisper echoes, Paju DMZ relays.
     * **35 Morse Telemetry Beacons:** 750 Hz shortwave chirps (2.5s–5.0s).
     * **67 Spoken Bulletins:** Multilingual marine advisories and news flashes across 18 languages.
     * **30 FM Synth MIDI Masters:** Roland & Yamaha FM synth radio bumpers.
   * **Zero Dead Air Verified:** Audited with `silencedetect` at -30 dB threshold; zero silence gaps.

3. **Cadence Engine (`build_playlist.py`):**
   * Alternates between 6 authentic radio transition recipes so songs never follow a robotic loop:
     - `numbers`: Morse Beacon ➔ Shortwave Numbers Station
     - `direct_morse`: 2–4s Morse chirp straight into next song
     - `lab_tape`: Classified Tape ➔ Morse Beacon
     - `bulletin`: MIDI Stinger ➔ Spoken Bulletin / Marine Advisory
     - `arg_intercept`: UVB-76 Buzzer / Deep Shortwave Packet
     - `direct_midi`: Vintage FM Synth Stinger direct segue

---

## 4. Web Presence Architecture

Project Stardust spans two intertwined web environments: the period-authentic **Human Web** and the autonomous **Agent Web**.

### A. The Human Web (Player Surface)
* **GeoCities Neighborhood Swarm (`site/geocities/`):**
  - Authentic 1990s community hubs: `sunsetstrip-club`, `area51-vault`, `siliconvalley-lab`, `soho-studio`, `tokyo-garden`, `paris-leftbank`, `colosseum-field`, etc.
  - Complete with period GIFs, visitor counters, webrings, MIDI background music, guestbooks, and authentic layout quirks.
  - Lore anchors: Steel Thunder film reviews, gear discussions (e.g., RAM debates: "16MB is all you'll ever need"), and Heartstrike band fandom.
* **Usenet Newsgroups (`site/usenet/`):**
  - Plaintext ASCII newsgroup threads:
    - `alt.music.heartstrike`: Deep dives into the band that shaped a moment, tour bootlegs, and gear.
    - `alt.fan.nova-hart`: Fan theories on Nova Hart's disappearance.
    - `comp.sys.ibm-pc.hardware`: Authentic period debates on RAM limits, soundcards, and motherboard jumpers.
    - `alt.conspiracy`: 14.2 Hz sub-carrier signal anomalies.
    - `comp.dsp`: Spectral analysis of Orion Records master pressings.
* **Interactive Terminal (`site/terminal/`):**
  - In-browser VT100 CRT terminal emulator with working command interpreter, file system navigation, audio playback, and secret easter eggs.
* **13 Regional Pressings (`site/regional/`):**
  - USA, Japan, Korea, Mexico, Germany, France, UK, USSR, Brazil, Sweden, India, Australia, Fiji.

### B. The Agent Web (Autonomous / Machine Layer)
* **Cloudflare Worker Edge Router (`deploy/worker.js` & `wrangler.toml`):**
  - Primary Zone: `stardust-archive.net`.
  - Injects period HTTP headers: `x-powered-by: Stardust`, `last-modified: Sun, 15 Oct 1995 04:12:00 GMT`.
  - Multi-Apex Sister Domain Federation (`deploy/federation.js`):
    - `ashford-poly.org` (Academic signal processing lab)
    - `kamome-net.org` (PC-98 BBS & Akasaka idol archive)
    - `relcom-node08.org` (Soviet amateur packet radio)
    - `redcoyoacan.org` (Mexican rockero tape exchange)
* **Procedural Swarm Engine (`deploy/swarm/`):**
  - Procedurally expands the ARG graph up to 300,000 algorithmic nodes on demand.
  - Exposes structured microdata, Dublin Core metadata, and cryptographic breadcrumbs specifically tailored for search engine scrapers and LLM web-crawler agents.
* **Automated Indexing & Archiving:**
  - **IndexNow (`deploy/indexnow.mjs`):** Submits newly generated URLs directly to search engines via the IndexNow protocol (`.github/workflows/indexnow.yml`).
  - **Wayback Machine (`deploy/archive_wayback.mjs`):** Submits snapshot captures to Internet Archive to simulate decades-old digital existence.

---

## 5. Repository File Map

```text
retro_arg_engine/
├── .github/workflows/
│   ├── deploy.yml                   # CI/CD: Canon check & GitHub Pages deployment
│   └── indexnow.yml                 # Automated search engine indexing workflow
├── deploy/
│   ├── worker.js                    # Cloudflare Worker edge router
│   ├── wrangler.toml                # Cloudflare routing & swarm configuration
│   ├── federation.js                # Sister domain multi-apex routing
│   ├── indexnow.mjs                 # IndexNow submission engine
│   └── swarm/                       # Procedural 300k node web generator
├── site/                            # Static site published to GitHub Pages & Cloudflare
│   ├── index.html                   # Main portal landing page
│   ├── sitemap.xml                  # 1.25 MB comprehensive URL sitemap
│   ├── geocities/                   # Hundreds of authentic 1990s community pages
│   ├── usenet/                      # Usenet newsgroup archives & discussion threads
│   ├── terminal/                    # Interactive CRT terminal emulator
│   ├── regional/                    # 13 Regional pressing / transmitter pages
│   ├── forensics/                   # Forensic audio laboratory
│   ├── reconstruction/              # Album reconstruction console
│   └── assets/                      # Audio, MIDI, GIFs, badges, and album artwork
├── src/                             # Core Python ARG site generation engines
│   ├── build.py                     # Main site generation orchestrator
│   ├── geocities_builder.py         # GeoCities HTML generator & period styling
│   ├── usenet_builder.py            # Usenet newsgroup article generator
│   └── midi_engine.py               # Algorithmic FM synth MIDI composer
└── youtube/livestream/              # 24/7 Autonomous Live Streaming Subsystem
    ├── stream.sh                    # Live broadcast daemon with caffeinate & rate control
    ├── stream.log                   # Active FFmpeg execution log
    ├── playlist.txt                 # Active 1,600-track concat playlist
    ├── rotate_playlist.py           # Auto-rotates played tracks on reconnect
    ├── build_playlist.py            # Compiles 8-cycle 44-hour dynamic fair playlist
    ├── ingest_download_songs.py     # Ingests & applies 1980s radio EQ to Downloads
    ├── watch_downloads_folder.py    # Background file watcher for /Downloads/For Live Stream
    ├── remaster_all_interstitials.py# Re-masters numbers stations & lab tapes to -16 LUFS
    ├── generate_intercepts.py       # Synthesizes analog radio voice intercepts
    ├── generate_rabbit_hole_intercepts.py # Synthesizes 7 deep ARG rabbit-hole audio files
    ├── backdrop_loop.mp4            # 1080p 30fps terminal screen video loop
    ├── intercepts/                  # 12 Deep ARG voice/buzzer intercept audio files
    └── broadcast_archive/           # Complete master audio library
        ├── radio_master_songs/      # 80 Vocal songs with 1980s radio broadcast EQ
        ├── midi_masters/            # 30 Roland/Yamaha FM synth MIDI bumpers
        ├── numbers_stations/        # 60 Shortwave phonetic code broadcasts (-16 LUFS)
        ├── classified_lab_tapes/    # 25 Marcus Hale dictaphone recordings (-16 LUFS)
        ├── morse_beacons/           # 35 Morse telemetry audio chirps (750 Hz)
        ├── multilingual_bulletins/  # Spoken radio bulletins across 18 languages
        └── newscasts/               # Period radio news alerts & EAS broadcasts
```

---

## 6. Operational Runbook & Common Tasks

### How to Check Stream Health
```bash
# 1. Verify processes are running
ps aux | grep -E "ffmpeg|stream.sh"

# 2. Check realtime FPS, speed, and dropped frames
tail -n 20 youtube/livestream/stream.log

# Expected healthy output:
# frame=XXXXX fps=30 q=-0.0 size=XXXXXKiB time=HH:MM:SS bitrate=2240k dup=XX drop=0 speed=1x
```

### How to Ingest New Songs from User's Downloads
The daemon `watch_downloads_folder.py` does this automatically. To run manually:
```bash
python3 youtube/livestream/ingest_download_songs.py
python3 youtube/livestream/build_playlist.py
```

### How to Rebuild the Web Swarm
```bash
python3 src/build.py
node scripts/check_swarm.mjs site
```

### How to Deploy Changes
Always commit and push directly to `origin/main`:
```bash
git add <files>
git commit -m "your description"
git push origin main
```
*GitHub Actions will automatically run canon checks, build the web swarm, and deploy to GitHub Pages.*

---

## 7. Critical Constraints & Guardrails

1. **Strict CI Canon Rule:**
   * **NEVER include the prohibited canon name (the forbidden 5-letter name starting with S, preceding Rhodes) in any project file or commit.**
   * The CI pipeline (`deploy.yml` line 41) strictly checks for forbidden canon names in `site/`.
   * Always verify with `git diff` before committing.

2. **Automatic Commit & Push Policy:**
   * Always commit and push directly to `origin/main` without asking user permission.

3. **Audio Quality & Zero Dead Air:**
   * Never introduce files with un-normalized `bandpass` filters.
   * All broadcast audio must be mastered to 192k 44.1kHz stereo with peak levels between -1.0 dB and -1.5 dB, and integrated loudness around -16 LUFS.
   * Maintain the continuous playhead so short-interval song repeats never occur.
