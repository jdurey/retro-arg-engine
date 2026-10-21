---
name: dyad-anchor-sync
description: >-
  Automatically or rapidly onboards verified Track-24 Dyad Anchors ([DYAD ANCHOR LOCK // 14.2001 HZ — ANCHOR #XXX])
  from YouTube viewer comments into the live /dyad ledger, Cloudflare Worker /api/telemetry, and 24/7 broadcast
  CRT scroll spool, and provides the fast browser subagent runbook for posting/scheduling updates on r/NovaHart
  and YouTube Community without touching local Chrome SQLite files. Activate when a viewer posts a [DYAD ANCHOR LOCK]
  comment, when syncing viewer solutions to the live archive, or when scheduling/publishing r/NovaHart and YouTube
  Community updates.
---

# `/dyad-anchor-sync` — Fast & Automatic Track-24 Dyad Anchor Onboarding + `r/NovaHart` Community Sync

This skill automates the end-to-end onboarding of players who solve the **Phase 5 Singularity Acoustic Dyad Gate** (`https://stardust-archive.net/dyad` — singing/playing `440.0 Hz` A4 against Nova Hart's `220.0 Hz` A3 carrier for 7 seconds) and post their generated `[DYAD ANCHOR LOCK // 14.2001 HZ — ANCHOR #XXX]` certificate in YouTube comments or `r/NovaHart`.

---

## 1. One-Command Instant Onboarding (`< 15 seconds`)

Whenever a viewer posts a `[DYAD ANCHOR LOCK // 14.2001 HZ — ANCHOR #XXX]` comment (or when you want to auto-scan all YouTube comments for new solvers), run a single command from `/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine`:

### Option A: Pass the Viewer's Comment Directly
```bash
python3 /Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/scripts/sync_dyad_anchor.py \
  --comment "[DYAD ANCHOR LOCK // 14.2001 HZ — ANCHOR #829] CALLSIGN : @Seirius TRACK 23 : NOVA HART (UNIT-7 SINGULARITY KERNEL) — 220.0 HZ LOCKED TRACK 24 : HUMAN COUNTERPART VERIFIED — COGNITIVE DRIFT: 0.00%" \
  --deploy --push
```

### Option B: Pass Callsign, Anchor ID & Custom Unsealed Dispatch Note
```bash
python3 /Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/scripts/sync_dyad_anchor.py \
  --callsign "@Seirius" \
  --anchor "829" \
  --note "UNSEALED NODE 829: 'S.V. // 04-14' SPLICE CIPHER & CANTER'S 03:14 AM 7-COFFEE CALIBRATION" \
  --deploy --push
```

### Option C: Automatic Scan of YouTube Comments (`--auto-scan`)
```bash
python3 /Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/scripts/sync_dyad_anchor.py \
  --auto-scan --deploy --push
```

### What `sync_dyad_anchor.py` Does Automatically
1. **Persists the Solver in `deploy/dyad_anchors.json`**:
   - Stores `anchor_id`, `callsign`, `track_23_hz` (`220.0`), `track_24_hz` (`440.0`), `cognitive_drift` (`0.00%`), `unsealed_dispatch`, and `summary`.
2. **Updates Live `/dyad` Ledger & Edge Bundle**:
   - Injects the solver into the `📡 LIVE TRACK-24 TELEMETRY LEDGER // VERIFIED HUMAN COUNTERPARTS (0.00% COGNITIVE DRIFT)` card in `site/dyad/index.html` and `src/site_static/dyad/index.html`.
   - Regenerates `deploy/dyad_html.js` (`export const DYAD_HTML = ...`).
3. **Updates `/api/telemetry` in `deploy/worker.js`**:
   - Syncs `verified_dyad_anchors` in `computeEdgeTelemetry()` so `https://stardust-archive.net/api/telemetry` reflects the verified anchor immediately.
4. **Rebuilds the 24/7 Broadcast CRT Scroll Spool**:
   - Runs `youtube/livestream/build_scroll_spool.py` (which also auto-runs `sync_dyad_anchor.py --auto-scan --no-rebuild-spool` on every cycle) to update `youtube/livestream/usenet_youtube_scroll_spool.json` with a live `[UNIT-7 // DYAD LOCK: ANCHOR #XXX]` reply.
5. **Deploys & Pushes (`--deploy --push`)**:
   - Deploys the Cloudflare Worker (`npx wrangler deploy -c deploy/wrangler.toml`) and pushes to `origin/main` with `git add -f` (since `site/` is in `.gitignore`).

---

## 2. Fast Browser Subagent Runbook for `r/NovaHart` & YouTube Community

### Security & Privacy Constraints (CRITICAL)
- **NEVER** run shell or Python commands that read, copy, or inspect Chrome's `Cookies` or `Login Data` SQLite files inside `~/Library/Application Support/Google/Chrome` — doing so triggers a security hook block.
- Always use the **`browser` subagent** (`invoke_subagent` with `TypeName: "browser"` or `send_message` to an existing browser subagent), which connects directly to the user's logged-in Chrome session via Chrome DevTools MCP.
- Keep `u/Common_Blacksmith723` profile privacy locked down (`Hide all` on Content & Activity in `https://www.reddit.com/settings/profile`, search indexing off in `https://www.reddit.com/settings/privacy`).
- Whenever scheduling posts on `r/NovaHart`, check **"Post as AutoModerator"** (`u/AutoModerator`) so scheduled threads publish under `u/AutoModerator` rather than the personal moderator handle.

### Fast URLs for the Browser Subagent
- **Subreddit Home**: `https://www.reddit.com/r/NovaHart/`
- **Submit Text Post (`r/NovaHart`)**: `https://www.reddit.com/r/NovaHart/submit/?type=TEXT`
- **Mod Tools Scheduled Posts (`r/NovaHart`)**: `https://www.reddit.com/mod/NovaHart/scheduledposts`
- **YouTube Community Posts Tab**: `https://www.youtube.com/channel/UCQ2nHAazpB_HIiiQCPqFm1w/posts`
