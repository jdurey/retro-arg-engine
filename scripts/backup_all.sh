#!/usr/bin/env bash
set -euo pipefail

cd /Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine

echo "=== [1/3] Staging & Pushing Code + State Ledgers to GitHub (origin/main) ==="
git add -u
git add \
  deploy/*.js deploy/*.json deploy/*.mjs deploy/*.md deploy/*.bind \
  scripts/*.py scripts/*.sh scripts/*.mjs \
  src/site_static/cre7 src/site_static/reddit-wiki \
  youtube/*.py youtube/livestream/*.py youtube/livestream/*.js \
  youtube/livestream/*.mjs \
  youtube/livestream/agentic_nostr_seed_results.json \
  youtube/livestream/moltbook_agent_insights.json \
  youtube/livestream/zero_auth_human_web_manifest.json \
  youtube/shorts_ready/UPLOAD_CHEATSHEET.md

git commit -m "Backup Sovereign Agent Bounty Leaderboard, HMAC Dyad Ticket anti-bounce scoring, and 24/7 radio packaging" || echo "Nothing new to commit"
git push origin main

echo "=== [2/3] Deploying Cloudflare Worker (retro-arg-router) ==="
(cd deploy && npx wrangler deploy)

echo "=== [3/3] Syncing deploy/ and site/dyad/ Backup to Primary Broadcaster (mini) ==="
scp deploy/*.js deploy/*.json deploy/WINDOW_COORDINATION_NOTICE.md mini:/Users/2hl/.gemini/antigravity-ide/scratch/retro_arg_engine/deploy/
scp site/dyad/index.html mini:/Users/2hl/.gemini/antigravity-ide/scratch/retro_arg_engine/site/dyad/index.html

echo "=== ✅ FULL BACKUP COMPLETE (GitHub + Cloudflare Edge + mini) ==="
