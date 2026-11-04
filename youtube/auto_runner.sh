#!/bin/bash
# Legacy hourly auto_runner disarmed on 2026-10-28 to prevent:
#   1. Hourly YouTube Data API v3 quota exhaustion (10,000 units/day)
#   2. Clobbering new-era song titles/descriptions/tags during the 48-hour browse test window.
# Inventory sync & holdout-protected packaging are now handled by:
#   - scripts/sync_and_repair_youtube_catalog.py
#   - scripts/meta_architect.py --closed-loop
exit 0
