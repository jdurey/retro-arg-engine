---
name: audio-analog
description: >-
  Transforms any audio file (local file, directory, HTML page with embedded base64 audio,
  or live web URL / stardust-archive.net endpoint) into an eerie, distant 1989 Type-I ferric
  analog cassette dub without mechanical button clicks by default. Activate this skill when
  the user invokes /audio-analog or asks to make audio sound like an old, eerie, worn analog
  cassette dub.
---

# `/audio-analog` — 1989 Eerie Distant Analog Cassette Dub Skill

This skill applies the signature **Sublevel B2 1989 Type-I Ferric Cassette Dub** DSP profile to any audio file on your machine or live on `stardust-archive.net`.

## DSP Signal Chain

1. **Subtle Capstan Wow & Flutter (`0.35x` / 35% intensity)**:
   - Dual-capstan drift (`0.52 Hz` and `1.15 Hz`) + `6.4 Hz` pinch-roller flutter + initial motor spin-up scoop (`-0.018 * exp(-t / 0.28)`), scaled by `0.35`.
2. **Eerie Distant Stereo Collapse & Azimuth Skew**:
   - Narrows stereo width to `22%` (`mid ± 0.22 * side`), shifts the right channel by `6` samples (`~0.136 ms` head azimuth misalignment), and modulates right-channel head contact at `0.37 Hz`.
3. **Magnetic Oxide Crinkles & Asymmetric Dropouts**:
   - Periodic `140 ms` Hanning-windowed oxide dropouts every `14.2 s` (`55%` L / `35%` R attenuation).
4. **Type-I Ferric Cassette Bandpass & Resonant Saturation**:
   - 3rd-order Butterworth highpass at `165 Hz` and 4th-order Butterworth lowpass at `2,950 Hz`.
   - Resonant cassette shell warmth/boxiness peaks at `240 Hz` (`Q=1.2`) and `780 Hz` (`Q=1.0`) mixed at `0.55 * dry + 0.30 * warm + 0.32 * box`.
   - Asymmetric Type-I ferric saturation (`drive = 3.2`: `tanh(s * 3.2 + 0.09 * s²) / tanh(3.2)`) followed by a `3,100 Hz` post-saturation lowpass (`* 0.72`).
5. **Dynamic Bias Hiss & Power Transformer Hum**:
   - Bandpass-filtered (`350 Hz – 4,200 Hz`) analog bias hiss (`0.018 + 0.022 * |y|`) + `60 Hz`, `120 Hz`, and `180 Hz` transformer hum.
6. **No Mechanical Tape Clicks by Default**:
   - Mechanical play/stop button clicks are disabled by default (pass `--clicks` only if explicitly requested).
7. **Idempotent Clean Backups**:
   - Automatically caches an untouched copy of each original file in `/tmp/audio_analog_clean_backups/` before its first pass so re-running with different parameters never double-degrades a track.

## Usage

### 1. Local Audio File or Folder
```bash
python3 ~/.gemini/config/skills/audio-analog/scripts/audio_analog.py /path/to/track.mp3
```
Or write to a separate output file:
```bash
python3 ~/.gemini/config/skills/audio-analog/scripts/audio_analog.py /path/to/input.wav -o /path/to/output_analog.mp3
```

### 2. Live Web Page or Audio URL on `stardust-archive.net`
When given a live `stardust-archive.net` URL (either a direct `.mp3` link or an HTML page like `https://stardust-archive.net/terminal`), the script automatically:
- Discovers all referenced `.mp3`/`.wav`/`.ogg` assets and embedded base64 MP3 blobs (`MARCUS_EMBEDDED`) on the page,
- Processes and syncs all mirror copies across `assets/`, `src/site_static/`, and `site/` in parallel.

```bash
python3 ~/.gemini/config/skills/audio-analog/scripts/audio_analog.py https://stardust-archive.net/terminal --workers 6
```

### 3. Deploying Live Updates to `stardust-archive.net`
Whenever modifying live audio files on `stardust-archive.net`:
1. Increment `ASSET_VERSION` in `/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/deploy/worker.js` (and `AUDIO_VER` in `terminal/index.html` if updating `/terminal`).
2. Commit and push all modified audio files in `assets/`, `src/site_static/`, `site/`, and `deploy/worker.js` to `origin/main`.
3. Wait for GitHub Pages (`https://jdurey.github.io/retro-arg-engine/...`) to serve the new MD5 checksum.
4. Run `npx --yes wrangler deploy --config deploy/wrangler.toml` so the Cloudflare Worker caches the updated upstream assets under the new `?v=` version.
