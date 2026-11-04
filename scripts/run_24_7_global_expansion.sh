#!/bin/bash
# Listener-First Global Discovery, Catalog Hygiene & Music/Guides SEO Runner
#
# De-collided from `Daily Ground-Truth Audit & Autonomous Optimizer` (09:00 KST) and
# scheduled Short slots (12:00 PM KST). Stripped of zero-conversion agent-bounty,
# Moltbook/Colony/Nostr/AgentDex bot spam, and paywalled `pure.md` (HTTP 402) calls:
#   1. Retires any off-brand/static uploads & syncs `youtube/state/videos.json`
#   2. Harvests 20-language YouTube autocomplete demand & injects listener search hooks
#   3. Submits canonical listener/guide/lyrics URLs to IndexNow + WebSub & warms AI search caches
#   4. Syncs r/NovaHart PAA & 20-language wiki, `.LRC` lyrics, and regional time-capsule pages
#   5. Scans YouTube comments for human Track-24 `/dyad` locks & refreshes local 24/7 radio spool

set -u
ROOT="/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine"
cd "$ROOT" || exit 1

echo "=== [LISTENER-FIRST CATALOG HYGIENE & SEO CYCLE: $(date -u +"%Y-%m-%dT%H:%M:%SZ")] ==="

# 1. Keep all off-topic static/cipher TTS uploads set to Private
"$ROOT/youtube/.venv/bin/python3" "$ROOT/youtube/yt.py" privatize-static || true

# 2. Sync live channel uploads inventory into youtube/state/videos.json, retire off-brand Shorts, & repair any truncated non-holdout titles
#    (NOTE: Short uploads are owned strictly by the nightly 12:00 PM KST scheduler; 24h causal evaluation & canary rollouts
#     are owned strictly by the 09:00 KST Daily Ground-Truth Audit so `youtube_stats_timeseries.jsonl` stays cleanly spaced.)
/usr/bin/python3 "$ROOT/scripts/sync_and_repair_youtube_catalog.py" || true

# 2b. Ensure every public VOD has the 24/7 82.5 FM livestream link in description + @NovaHart_Official comment (capped at 50/run & 55/PT-day to preserve >=4,400 daily YouTube API quota headroom)
/usr/bin/python3 "$ROOT/scripts/ensure_livestream_links_and_comments.py" --limit 50 --daily-cap 55 || true

# 3. Harvest 20-Language YouTube Autocomplete Queries (suggestqueries.google.com?ds=yt, 24h cooldown) & inject listener hooks
/usr/bin/python3 "$ROOT/scripts/harvest_yt_autocomplete_keywords.py" || true

# 4. Submit listener/guide/lyrics canonical URLs across root domains to IndexNow + WebSub & warm r.jina.ai / markdown.new (cooldown-gated, zero pure.md)
/usr/bin/python3 "$ROOT/scripts/publish_da99_authority_network.py" || true

# 5. r/NovaHart SEO Authority Loop, PAA Question Matrix & 20-Language Wiki Seeder (human-jitter anti-spam cooldown)
/usr/bin/python3 "$ROOT/scripts/reddit_seo_authority_pipeline.py" || true

# 6. Synced .LRC Lyrics & MusicBrainz Catalog Seeder (SHA-256 content-hash 6h cooldown)
/usr/bin/python3 "$ROOT/scripts/lyrics_and_dns_seeder.py" || true

# 7. 7-Country Regional Time-Capsule Artifacts Seeder (SHA-256 content-hash 6h cooldown + Regional IndexNow)
/usr/bin/python3 "$ROOT/scripts/update_regional_time_capsules.py" || true

# 8. Human Listener Funnel & 24/7 Radio Stream Spool Sync (YouTube comment Track-24 `/dyad` auto-scan + offline telemetry)
/usr/bin/python3 "$ROOT/scripts/sync_dyad_anchor.py" --auto-scan || true
/opt/homebrew/bin/python3 "$ROOT/youtube/livestream/sync_telemetry.py" --offline || true

# 9. Archive unarchived listener/guide nodes into Internet Archive Wayback Machine (capped at 3)
node "$ROOT/deploy/archive_wayback.mjs" --limit 3 || true

echo "=== [CYCLE COMPLETE: $(date -u +"%Y-%m-%dT%H:%M:%SZ")] ==="

