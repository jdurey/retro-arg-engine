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

# 1. Upload notifySubscribers=False Gateway Documentary & Vertical Shorts first
"$ROOT/youtube/.venv/bin/python3" "$ROOT/youtube/yt.py" upload-shorts --limit 3 || true

# 2. Upgrade catalog videos to Lost 1989 Studio Tape / Erased Singer Mystery Bridge (20 languages)
"$ROOT/youtube/.venv/bin/python3" "$ROOT/youtube/yt.py" apply --limit 50 || true

# 3. Sync any brand-new uploads on @NovaHart_Official
"$ROOT/youtube/.venv/bin/python3" "$ROOT/youtube/yt.py" sync || true

# 4. Submit fresh multi-domain URLs across all 13 root domains to IndexNow & RAG proxies
/usr/bin/python3 "$ROOT/scripts/publish_da99_authority_network.py" || true

# 5. Seed AgentDex, Nostr/Clawstr relays, WebSub, and Markdown RAG caches
/usr/bin/python3 "$ROOT/scripts/agentic_web_seeder.py" || true

echo "=== [CYCLE COMPLETE: $(date -u +"%Y-%m-%dT%H:%M:%SZ")] ==="
