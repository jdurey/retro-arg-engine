#!/usr/bin/env python3
"""
Outbound Human Audience & External Authority Pipeline (`scripts/outbound_audience_campaign.py`)
===============================================================================================
Tracks live vs. human-login-ready external authority & listener campaigns across:
  1. Real Public Music & Lyric Databases (`LRCLIB.net` 63/63 LIVE, MusicBrainz Harmony 1-click, Wikidata, Discogs)
  2. Real Internet Radio Directories (`RadioBrowser` UUID `25c7799c-49a9-4522-89f9-fe3b95accac6` LIVE on
     `https://stardust-archive.net/stream/825fm.mp3` + Streema/Simple Radio + OnlineRadioBox)
  3. Post-Bandcamp Sovereign Direct-to-Fan Storefront (`https://nova-hart-shop.fourthwall.com/promo/LIVE`
     replacing dead `novahart.bandcamp.com` links across YouTube & web)
  4. Real Press, Curators & Human Communities (`/press` EPK, ARGNet, SubmitHub AI-friendly filter, `r/WebGames`, `Show HN`, TikTok/Reels)
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "deploy" / "outbound_audience_dispatches.json"

EXTERNAL_AUDIENCE_CAMPAIGNS: List[Dict[str, Any]] = [
    {
        "id": "ext-db-01-lrclib-public-lyrics",
        "status": "LIVE_VERIFIED",
        "live_permalink": "https://lrclib.net/api/search?q=Nova+Hart",
        "vertical": "Global Open Synced/Plain Lyrics Registry (MusicBee, Plex, Jellyfin, Navidrome, LLM Scrapers)",
        "target_community": "LRCLIB.net Public Database",
        "link_url": "https://lrclib.net/api/search?q=Nova+Hart",
        "title": "63 Official Nova Hart Tracks + Verbatim Lyrics + GBLLT25* ISRCs Published Live to LRCLIB.net",
        "body_markdown": "Published 63/63 official Orion Records DSP tracks (including 'Chrome River', 'Midnight Animal', 'The Stars in Your Hands', 'Iron Claws', 'Don't Just Watch Me Rise', 'Gasoline Heart', 'We Are the Thunder') via SHA-256 Proof-of-Work.",
    },
    {
        "id": "ext-radio-02-radiobrowser-icecast-825fm",
        "status": "LIVE_VERIFIED",
        "live_permalink": "https://www.radio-browser.info/history/25c7799c-49a9-4522-89f9-fe3b95accac6",
        "vertical": "Global Open Internet Radio Directory (VLC, Kodi, Shortwave, RhythmBox, Home Assistant, fmstream)",
        "target_community": "RadioBrowser.info + Direct 128k CBR Icecast Stream",
        "link_url": "https://stardust-archive.net/stream/825fm.mp3",
        "title": "82.5 FM - Nova Hart (1989 Arena Rock, Synthwave & Night Drive Radio) — Live HTTP MP3 Stream",
        "body_markdown": "Live 128kbps 44.1kHz stereo Icecast-compatible stream at https://stardust-archive.net/stream/825fm.mp3 (+ /825fm.m3u & /825fm.pls), registered with RadioBrowser UUID 25c7799c-49a9-4522-89f9-fe3b95accac6.",
    },
    {
        "id": "ext-epk-03-press-and-verified-dsps",
        "status": "LIVE_VERIFIED",
        "live_permalink": "https://stardust-archive.net/press",
        "vertical": "Music Blogs, ARG Press (ARGNet), SubmitHub Curators & Google Knowledge Graph Reconciliation",
        "target_community": "ARGNet (argn.com), NewRetroWave, SubmitHub ('Accepts AI' filter), Spotify & Apple Music",
        "link_url": "https://stardust-archive.net/press",
        "title": "Official Nova Hart & Project Stardust Electronic Press Kit (/press) + Repaired Spotify/Apple/Deezer/TIDAL/Fourthwall Links",
        "body_markdown": "Repaired broken Spotify/Apple IDs to verified Spotify (0zElHuJrzKbq0XjqK3HyYr), Apple Music (1681398544), Deezer (208848717), TIDAL (38666478), and Fourthwall Direct Store (nova-hart-shop.fourthwall.com, replacing banned Bandcamp).",
    },
    {
        "id": "ext-radio-04-streema-onlineradiobox",
        "status": "READY_WITH_LIVE_MP3_STREAM",
        "vertical": "Commercial Web & Mobile Radio Apps (Streema / Simple Radio 70M+ installs & OnlineRadioBox)",
        "target_community": "Streema (https://streema.com/radios/request) & OnlineRadioBox (https://onlineradiobox.com/office)",
        "submit_url": "https://streema.com/radios/request",
        "link_url": "https://stardust-archive.net/stream/825fm.mp3",
        "title": "82.5 FM - Nova Hart (80s Arena Rock & Synthwave)",
        "body_markdown": "Direct 128k MP3 stream URL `https://stardust-archive.net/stream/825fm.mp3` is now live and ffprobe-verified so Streema and OnlineRadioBox stream validators pass immediately.",
    },
    {
        "id": "ext-webgames-05-pzl-terminal",
        "status": "READY_HUMAN_BROWSER_SUBMIT",
        "vertical": "Browser Puzzle / Terminal Wargame (r/WebGames — 147,131 members)",
        "target_community": "r/WebGames (Link Post, Flair: [PZL], zero ?ref= query params)",
        "submit_url": "https://www.reddit.com/r/WebGames/submit/?type=LINK",
        "link_url": "https://stardust-archive.net/terminal",
        "flair_text": "[PZL]",
        "title": "Project Stardust: Sub-Level B2 – Playable 1989 VT100 studio terminal with Web Audio signal lab, M68000/Feistel ciphers, and Easy Mode",
        "body_markdown": "",
    },
    {
        "id": "ext-tech-06-show-hn-retrocomputing",
        "status": "READY_HUMAN_BROWSER_SUBMIT",
        "vertical": "Retro-Computing / 1995 Web Preservation / Web Audio DSP",
        "target_community": "Hacker News (Show HN)",
        "submit_url": "https://news.ycombinator.com/submit",
        "link_url": "https://stardust-archive.net/terminal",
        "title": "Show HN: Stardust Archive – 300k 1995 GeoCities pages, a 1989 VT100/M68k terminal, and a 24/7 CRT radio stream",
        "body_markdown": "See outreach_kit/OUTREACH_COMMAND_CENTER.md for exact first-comment technical breakdown.",
    },
]


def main() -> int:
    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "strategy_focus": "Real public databases (LRCLIB, RadioBrowser, MusicBrainz, Wikidata), direct 82.5 FM Icecast MP3 radio, post-Bandcamp Fourthwall MRR recovery, /press EPK, and 9:16 TikTok/Reels hooks",
        "campaign_count": len(EXTERNAL_AUDIENCE_CAMPAIGNS),
        "campaigns": EXTERNAL_AUDIENCE_CAMPAIGNS,
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[OUTBOUND CAMPAIGN] Wrote {len(EXTERNAL_AUDIENCE_CAMPAIGNS)} campaigns to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
