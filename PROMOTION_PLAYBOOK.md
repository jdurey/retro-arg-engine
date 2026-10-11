# 🚀 Project Stardust & Nova Hart: The Growth & Discovery Playbook

> **Core Philosophy**: Alternate Reality Games (ARGs) and narrative music projects never succeed through paid advertisements. They explode when audiences feel the **thrill of stumbling upon an unindexed mystery**. 
> 
> This playbook provides four turnkey promotional engines that turn passive listeners into active investigators.

---

## 📺 Engine 1: The 24/7 "Ghost Signal" Live Stream

YouTube heavily recommends 24/7 live streams on user homepages in the synthwave, lofi, darkwave, and analog horror niches.

### What is Prepared:
* **Visual**: Custom 1080p green phosphor CRT oscilloscope backdrop (`youtube/livestream/backdrop.jpg`) featuring 14.2 Hz signal telemetry.
* **Audio**: Continuous shuffle of 29 authentic 1980s 14k audio tracks, shortwave radio intercepts, and telemetry spools (`site/ftp/kamome/audio/`).
* **Auto-Reconnection**: Resilient streaming loop with automatic reconnect.

### How to Launch It (1 Step):
1. Go to [YouTube Studio Live Dashboard](https://studio.youtube.com/channel/UCQ2nHAazpB_HIiiQCPqFm1w/livestreaming).
2. Copy your **Stream Key**.
3. In your terminal, run:
```bash
./youtube/livestream/stream.sh "YOUR_STREAM_KEY_HERE"
```
The stream will immediately begin broadcasting live to YouTube. Leave it running in a background terminal.

---

## 📱 Engine 2: Short-Form Viral "Trailhead" Videos

Over 80% of modern ARG discovery happens on **TikTok, YouTube Shorts, and Instagram Reels**. 

Two complete, high-retention 9:16 vertical MP4 videos have been rendered with authentic audio stems, CRT graphics, and retro text overlays:

### Ready-to-Post Videos:
1. **Short 1: The Forgotten Server**
   * **File**: `youtube/shorts/rendered/short1_the_forgotten_server.mp4`
   * **Hook**: *"UNSOLVED INTERNET MYSTERY (1995) — This 1995 server is still transmitting."*
   * **Audio**: `ghost_in_the_chorus.mp3`
   * **Suggested Caption**:
     ```text
     Found an unlisted 1995 university FTP server that's still transmitting on modern IP space. What is the 14.2 Hz signal?
     #ARG #AnalogHorror #UnsolvedMystery #WebArchaeology #NovaHart
     ```

2. **Short 2: The Found 1989 Cassette**
   * **File**: `youtube/shorts/rendered/short2_found_tape_1989.mp4`
   * **Hook**: *"ESTATE SALE // 1989 TAPE DISCOVERY — The label said 'Do Not Play'."*
   * **Audio**: `jp-85-gt_ghost_transit_shortwave.mp3`
   * **Suggested Caption**:
     ```text
     Bought a box of old tapes at an estate sale. The handwritten label on this one said "Orion Simulation 1989 // DO NOT PLAY // 14.2 Hz". Listen to what happened at the end...
     #LostMedia #FoundTape #VintageSynth #CreepyInternet #NovaHart
     ```

---

## 🕵️‍♂️ Engine 3: Mystery Investigator "Whistleblower" Dossiers

Instead of posting links on public forums, send an anonymous whistleblower tip directly to the public submission inboxes of the top mystery creators.

Detailed, pre-written email dossiers with specific entry points are located in:
👉 [`promo/whistleblower_dossiers/investigator_emails.md`](file:///Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/promo/whistleblower_dossiers/investigator_emails.md)

### Creators Targeted:
* **Night Mind** (`nightmindsubmissions@gmail.com`) — The internet's premier ARG analysis channel.
* **Nexpo** (`nexposubmissions@gmail.com`) — Master of dark web anomalies and digital rabbit holes.
* **Wendigoon** (`wendigoontips@gmail.com`) — Specialist in deep internet lore and philosophical horror.
* **blameitonjorge** (`blameitonjorge@gmail.com`) — Authority on lost media and obscure analog recordings.

---

## 🎵 Engine 4: Synthwave Curator "Trojan Horse"

Nova Hart's music stands firmly on its own musical merits. Getting featured on major synthwave curation channels brings thousands of listeners who read the video descriptions and fall down the rabbit hole.

Complete track pitches and curator contact links are located in:
👉 [`promo/music_curators/synthwave_submissions.md`](file:///Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/promo/music_curators/synthwave_submissions.md)

### Key Curators:
* **ThePrimeThanatos** (1.2M Subs) — Pitch *"Asset Loss"* or *"Burning Oath"*.
* **NewRetroWave** (1.4M Subs) — Pitch *"Crossing This Line"*.
* **Astral Throb** (400K Subs) — Pitch *"Shadows in the Rain"*.

---

## ⚙️ Summary of Automated Systems Running

| System | State | Action |
| :--- | :--- | :--- |
| **YouTube Channel Bio** | **Live in 20 Languages** | Channel name and Project Stardust bio are translated and active. |
| **Catalog Batch Updater** | **Active in Background** | Upgraded 89+ videos with 20-language titles and full descriptions. |
| **Hourly Upload Watcher** | **Active (`cron`)** | Detects new uploads every hour and automatically localizes them. |
| **Daily Quota Backfiller** | **Active (`cron`)** | Resumes every day at 16:05 KST (07:05 UTC) right after YouTube quota resets. |
