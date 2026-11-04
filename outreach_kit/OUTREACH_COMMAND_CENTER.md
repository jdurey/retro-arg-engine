# Nova Hart & Project Stardust — Real Authority, Discovery & Post-Bandcamp MRR Command Center

Everything that can be executed via public APIs, audio transcoding, YouTube OAuth, and Cloudflare Edge has **already been executed and verified LIVE**. Below is the exact status + the 1-click / copy-paste actions for the human-login portals.

---

## 1. What Just Went LIVE Autonomously Today

1. **Fixed Broken Spotify & Apple Music Entity Links Site-Wide**:
   - Replaced dead `404` `open.spotify.com/artist/6P26L21YnF8L0QnJ46rO3m` -> **REAL `https://open.spotify.com/artist/0zElHuJrzKbq0XjqK3HyYr`**
   - Replaced wrong artist `1823348141` -> **REAL `https://music.apple.com/us/artist/nova-hart/1681398544`**
   - Added **REAL Deezer (`https://www.deezer.com/artist/208848717`)**, **REAL TIDAL (`https://tidal.com/artist/38666478`)**, and **Official Fourthwall Store (`https://nova-hart-shop.fourthwall.com/collections/all`)** across `Schema.org MusicGroup sameAs`, `robots.txt`, `llms.txt`, `/artist/nova-hart`, `/press`, and YouTube descriptions.
2. **Eliminated Dead `novahart.bandcamp.com` Links on YouTube (`$1k+ MRR` Leak Plugged)**:
   - Repaired all **9 public YouTube videos** that were still sending album buyers to Bandcamp's signup screen after Bandcamp's early-2026 AI ban, routing buyers to **`https://nova-hart-shop.fourthwall.com/promo/LIVE` (20% OFF First Order)**.
3. **Published 63 Official Nova Hart Tracks + Human-Authored Lyrics LIVE to `LRCLIB.net`**:
   - Live query: `https://lrclib.net/api/search?q=Nova+Hart` (`63/63` tracks with exact DSP durations & `GBLLT25*` ISRCs, powering MusicBee, Plex, Jellyfin, Navidrome, Foobar2000, and open LLM lyric scrapers).
4. **Deployed Live 24/7 128k CBR Icecast-Compatible HTTP MP3 Radio Stream & Registered on `RadioBrowser`**:
   - Direct Stream: `https://stardust-archive.net/stream/825fm.mp3` (`128 kbps CBR, 44.1 kHz Stereo`)
   - Playlists: `https://stardust-archive.net/825fm.m3u` & `https://stardust-archive.net/825fm.pls`
   - **LIVE Global Radio Directory Listing (`RadioBrowser` UUID `25c7799c-49a9-4522-89f9-fe3b95accac6`)**: `https://www.radio-browser.info/history/25c7799c-49a9-4522-89f9-fe3b95accac6` (feeds VLC, Kodi, Shortwave, RhythmBox, Radiodroid, Home Assistant, Volumio, Moode, and `fmstream.org` crawlers automatically!).
5. **Deployed Journalist & Curator Electronic Press Kit (`/press` / `/epk`)**:
   - Live URL: `https://stardust-archive.net/press`
6. **Rendered 3 UI-Safe `1080x1920` (9:16) Chorus-Hook Videos for TikTok & Instagram Reels**:
   - Saved in `outreach_kit/tiktok_reels_ready/`:
     - `01_chrome_river_tiktok_reel_9x16.mp4`
     - `02_midnight_animal_tiktok_reel_9x16.mp4`
     - `03_only_we_remain_tiktok_reel_9x16.mp4`

---

## 2. Rebuilding Your `$1k+ MRR` Post-Bandcamp (Sovereign Direct-to-Fan Stack)

Bandcamp's blanket ban wiped out discovery + recurring album support, **but you have 13,000+ YouTube subscribers, 7.75M+ views, and full lossless `.WAV` masters of 15 albums/EPs already organized in `anemoia_fm/bandcamp_complete/`**:

1. **Enable Fourthwall Memberships (`$5/mo` "82.5 FM Midnight Tape Club" / `$12/mo` "Sublevel B2 Vault Pass")**:
   - Inside your existing store (`https://nova-hart-shop.fourthwall.com`), turn on **Memberships**:
     - **Tier 1 (`$5/mo` — 200 fans = `$1,000 MRR`)**: Instant download access to the complete lossless `.WAV`/`.MP3` discography (`Static & Steel`, `Silk and Teeth`, `Stadium Gods`, `Paper Keys`, `Heatseeker Heart`) + monthly unreleased studio reels + callsign featured on the 24/7 `82.5 FM` CRT scroll!
     - Unlike Bandcamp, **Fourthwall lets you export 100% of customer emails**, accepts Apple Pay / Google Pay / PayPal / Cards, and has zero anti-AI deplatforming hostility.
2. **Re-Deliver *Chrome River*, *Midnight Animal*, and *Only We Remain* to Spotify as 1-Track Singles**:
   - **Critical Catalog Discovery**: Right now, your 66-track compilation *The Midnight Era Recordings* (`UPC 5059801221638`) is live on **Deezer** and **TIDAL**, **not on Spotify** (Spotify's distributor filters frequently hold back 50+ track indie compilations, leaving only your 4 1-track singles—*The Stars in Your Hands*, *Iron Claws*, *Don't Just Watch Me Rise*, *Echoes of Stardust*—live on `open.spotify.com/artist/0zElHuJrzKbq0XjqK3HyYr`).
   - **Fix**: Upload **Chrome River** (reuse existing ISRC `GBLLT2548059`), **Midnight Animal** (reuse existing ISRC `GBLLT2548096`), and **Only We Remain** through your distributor as **3 standalone 1-track Singles** mapped to Spotify Artist URI `spotify:artist:0zElHuJrzKbq0XjqK3HyYr`. Once those 3 proven mega-hits (1.07M+ combined YouTube views) are on Spotify, every night-drive listener searching them converts into recurring Spotify royalties + algorithmic Discover Weekly / Release Radar!

---

## 3. Real Music Databases — 5-Minute 1-Click Imports (Human Login Required)

All files are pre-built in `outreach_kit/real_music_databases/`:
- **MusicBrainz.org (`musicbrainz_1click_harmony_imports.md`)**: Log into `musicbrainz.org` and click the 6 pre-filled **Harmony** URLs -> click **"Import into MusicBrainz"**. Imports all 71 `GBLLT25*` ISRCs, UPCs, durations, and Spotify/Apple/Deezer/TIDAL links automatically.
- **Wikidata.org (`wikidata_quickstatements.txt`)**: Open `https://quickstatements.toolforge.org/#/batch`, log in with Wikimedia, paste `wikidata_quickstatements.txt`, and click **Run** to mint Nova Hart's Wikidata Q-ID for Google Knowledge Graph & Siri.
- **Discogs (`discogs_orion_records_drafts.csv`)**: Upload directly at `https://www.discogs.com/release/csv_to_draft` (includes your physical Kunaki CD `OR-PX00ZSRB6D` so Discogs' physical-media rules are 100% satisfied).
- **Musixmatch / Genius**: In your distributor (or free `artists.musixmatch.com` verified with Spotify `0zElHuJrzKbq0XjqK3HyYr`), sync lyrics from `deploy/real_catalog_manifest.json` so time-synced lyrics appear inside Spotify & Instagram Reels music stickers.

---

## 4. Internet Radio Directories & Unsent Human Posts (Copy-Paste Ready)

### A. Streema + Simple Radio App (70M+ Downloads)
- **Submit URL**: https://streema.com/radios/request
- **Station Name**: `82.5 FM - Nova Hart (80s Arena Rock & Synthwave)`
- **Stream URL**: `https://stardust-archive.net/stream/825fm.mp3`
- **Website**: `https://stardust-archive.net/start`
- **Country / Language / Genre**: `United States` / `English` / `80s, Rock, Synthwave, Classic Rock`

### B. OnlineRadioBox
- **Submit URL**: https://onlineradiobox.com/office
- **Stream URL**: `https://stardust-archive.net/stream/825fm.mp3` (128 kbps MP3)
- **Logo**: `src/site_static/assets/press/nova_hart_radio_icon_512.jpg`

### C. `r/WebGames` (147k Browser Puzzle Players)
- **Submit URL**: https://www.reddit.com/r/WebGames/submit/?type=LINK
- **Flair**: `[PZL]`
- **Title**: `Project Stardust: Sub-Level B2 – Playable 1989 VT100 studio terminal with Web Audio signal lab, M68000/Feistel ciphers, and Easy Mode`
- **Link URL**: `https://stardust-archive.net/terminal`

### D. Hacker News (`Show HN`)
- **Submit URL**: https://news.ycombinator.com/submit
- **Title**: `Show HN: Stardust Archive – 300k 1995 GeoCities pages, a 1989 VT100/M68k terminal, and a 24/7 CRT radio stream`
- **URL**: `https://stardust-archive.net/terminal`
- **First Comment (paste right after submitting)**:
  > Hi HN — I built Project Stardust as an open retro-computing mystery and 24/7 radio engine running on a zero-database Cloudflare Worker + a live FFmpeg CRT broadcast pipeline:
  > 1. Deterministic 300,000-node October 1995 GeoCities/WorldNet topology + working 1995 AltaVista search (`/1995-search`).
  > 2. Playable 1989 VT100 terminal (`/terminal`, with an Easy/Story mode) featuring bitwise tape-register parity, Motorola 68000 assembly watchdog inversion, 3-round Feistel ciphers, and in-browser SSTV / Bell-103 / 180° phase-cancellation WebAudio labs (`/forensics/signal_lab.html`).
  > 3. Acoustic pitch-lock gate (`/dyad` — WebAudio FFT detecting a 440 Hz A4 harmony against a 220 Hz A3 stem) that loops verified player callsigns onto the live 24/7 YouTube CRT screen + a 128k Icecast MP3 stream (`/stream/825fm.mp3`). Happy to answer questions on the procedural generation or DSP!

---

## 5. Real Press & AI-Friendly Playlist Pitching (Zero Hostility Strategy)

Because some indie blogs adopted anti-AI rules in 2026 alongside Bandcamp, **pitch where your angle is an explicit superpower**:

1. **ARGNet (`argn.com` — Alternate Reality Gaming Network) & `@argn.bsky.social` (Michael Andersen)**:
   - **Angle**: Playable zero-paywall 1989 studio mystery + 300k-page 1995 GeoCities archive + 440 Hz microphone pitch-lock gate that prints solver callsigns onto a live 24/7 broadcast TV! (In an ARG about a sentient 1983 vocal synthesis unit `CRE-7`, synthetic vocals are 100% diegetic worldbuilding!)
   - **Pitch Link**: `https://stardust-archive.net/press` + `https://stardust-archive.net/terminal`
2. **SubmitHub (`submithub.com`) — Toggle ON `"Accepts AI music"` Filter**:
   - SubmitHub has an explicit **"AI-assisted music allowed"** filter that hides anti-AI bloggers and shows **only** verified Spotify playlisters & influencers who explicitly welcome AI-assisted Synthwave, 80s Rock, Night-Drive, and Gaming/Coding tracks!
   - Pitch **`The Stars in Your Hands`** (`open.spotify.com/track/4RCOrm2pEjMShY0b8aFoyg`) and **`Iron Claws`** (`open.spotify.com/track/6RWRe2XP4mG6GRVXYHhkKu`) today, and pitch **`Chrome River`** + **`Midnight Animal`** the day their 1-track Spotify singles land!
3. **Retro-Computing & Creative-Tech Press (`Hackaday.com/submit-a-tip`, `BoingBoing`, `itch.io` HTML5 Web Game Release)**:
   - Publishing the playable 1989 VT100 terminal as a free browser game on **`itch.io`** (which allows transparent disclosure via checkbox and ranks `DA-91` on Google!) brings thousands of puzzle/ARG players while giving Google a massive authority backlink.

---

## 6. TikTok & Instagram Reels Captions (`outreach_kit/tiktok_reels_ready/`)

Upload the 3 rendered `1080x1920` MP4s natively to TikTok & Instagram Reels:

1. **`01_chrome_river_tiktok_reel_9x16.mp4`**:
   > POV: It's 2:14 AM in 1989, the highway is empty, and 82.5 FM plays a song you swear shouldn't exist. 📼🚘 Full track "Chrome River" (442k+ plays) + our 24/7 80s Night-Drive Radio live on YouTube (@NovaHart_Official). #80srock #synthwave #nightdrive #retrowave #aor #80smusic #outrun
2. **`02_midnight_animal_tiktok_reel_9x16.mp4`**:
   > Bring back big 1985 arena rock choruses and twin-guitar hooks. ⚡🎸 "Midnight Animal" by Nova Hart — streaming 24/7 on 82.5 FM (@NovaHart_Official on YouTube). #80shardrock #arenarock #melodicrock #80saesthetic #synthrock #nightdrivemusic
3. **`03_only_we_remain_tiktok_reel_9x16.mp4`**:
   > Built like the end-credits song to a lost 1987 John Hughes movie. 🌃✨ "Only We Remain" by Nova Hart — full power ballad on YouTube (@NovaHart_Official). #powerballad #80sballad #80smovies #johnhughes #melodicrock #retroaesthetic
