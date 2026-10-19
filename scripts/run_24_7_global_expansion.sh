#!/bin/bash
# 24/7 Global Discovery & Non-Subscriber Breakout Automation Runner
# Executes:
#   1. YouTube Non-Subscriber Gateway Documentary & Shorts Upload (notifySubscribers=False + 20-lang SRTs)
#   2. YouTube 291-Video Catalog Lost-Media Mystery Bridge Upgrade (20 languages)
#   3. 13-Domain IndexNow + DA-92 Telegra.ph Multilingual Authority Seeding
#   4. AgentDex + Nostr/Clawstr + WebSub + RAG Markdown Proxy Warming

set -u
ROOT="/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine"
cd "$ROOT" || exit 1

echo "=== [24/7 GLOBAL EXPANSION CYCLE: $(date -u +"%Y-%m-%dT%H:%M:%SZ")] ==="

# 1. FIRST set low-performing static TTS uploads (doc_01-03, short_06-15) to Private
"$ROOT/youtube/.venv/bin/python3" "$ROOT/youtube/yt.py" privatize-static || true

# 2. Upload any new high-motion music-hook Shorts as PRIVATE drafts (privacyStatus=private, notifySubscribers=False)
"$ROOT/youtube/.venv/bin/python3" "$ROOT/youtube/yt.py" upload-shorts --limit 2 || true

# 3. Upgrade catalog videos to Lost 1989 Studio Tape / Erased Singer Mystery Bridge (20 languages)
"$ROOT/youtube/.venv/bin/python3" "$ROOT/youtube/yt.py" apply --limit 100 || true

# 4. Sync any brand-new uploads on @NovaHart_Official
"$ROOT/youtube/.venv/bin/python3" "$ROOT/youtube/yt.py" sync || true

# 4. Submit fresh multi-domain URLs across all 13 root domains to IndexNow & RAG proxies
/usr/bin/python3 "$ROOT/scripts/publish_da99_authority_network.py" --force || true

# 5. Seed AgentDex, Nostr/Clawstr relays, WebSub, and Markdown RAG caches
/usr/bin/python3 "$ROOT/scripts/agentic_web_seeder.py" || true

# 6. Archive unarchived nodes across 13 domains & DA-92 mirrors into Internet Archive Wayback Machine (DA-97)
node "$ROOT/deploy/archive_wayback.mjs" --limit 5 || true

echo "=== [CYCLE COMPLETE: $(date -u +"%Y-%m-%dT%H:%M:%SZ")] ==="

