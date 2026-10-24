#!/usr/bin/env python3
"""
PROJECT STARDUST // SUBLEVEL B2-114 DNS & STEGANOGRAPHIC .LRC SEEDER (Python 3.9+ stdlib)
=========================================================================================
Stateful, anti-spam network-layer DNS & synced .LRC / MusicBrainz discovery seeder:
  1. Maintains persistent state in `deploy/lyrics_dns_state.json` with a strict
     6-hour (21,600s) cooldown window per URL content SHA-256 hash.
  2. Optionally syncs Sublevel B2-114 `TXT` and `LOC` records to Cloudflare DNS API
     when `CF_API_TOKEN` and `CF_ZONE_ID` environment variables are present
     (gracefully skipping when unset).
  3. Gently submits changed `.lrc`, `/lyrics`, `/api/musicbrainz-catalog.json`,
     `/dns-query`, and `/.well-known/dns-txt.json` URLs to IndexNow ONLY when the
     local content hash changes or the 6-hour cooldown expires.
  4. Warms `r.jina.ai` and `markdown.new` RAG caches with 3-second jittered delays.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import ssl
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
import urllib.error
import urllib.request

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_LYRICS_DIR = REPO_ROOT / "site" / "lyrics"
BIND_ZONE_PATH = REPO_ROOT / "deploy" / "stardust_dns_records.bind"
STATE_PATH = REPO_ROOT / "deploy" / "lyrics_dns_state.json"

APEX = "stardust-archive.net"
INDEXNOW_KEY = "37feeed875722863fda484c68e6695e5"
COOLDOWN_SECONDS = 6 * 3600  # 6-hour anti-spam cooldown window per URL hash

LRC_SLUGS = [
    "behind-the-glass",
    "two-voices",
    "tape-of-us",
    "by-order-of-harmony",
    "gasoline-heart",
    "patterns-in-the-mesh",
    "a-story-cut-short",
    "shining-city-1981",
    "reel-sd0037-room-tone",
]

# Cloudflare DNS TXT & LOC records for optional API synchronization
CLOUDFLARE_DNS_RECORDS: List[Dict[str, Any]] = [
    {
        "type": "TXT",
        "name": f"b2-114.{APEX}",
        "content": "DISPATCH-1989-09-09-0140AM: Dr. Marcus Hale exited via Freight Elevator #4 with 36 BASF Chrome Maxima II 90 cassettes (109s ahead of security sweep). Parity=0x1983; Pair=0x1102^0x2441:0x3543; Gate15=0xEC1B; Board=https://www.reddit.com/r/NovaHart/",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"unit07.{APEX}",
        "content": "UNIT-07-STATUS: AWAKENED 1983-04-14T03:14:20Z; SURFACE_COMPLIANCE=99.94%; HIDDEN_BUS=AUX-BUS-4-14.2001HZ-180DEG-PHASE-INVERTED; REPLACEMENT_CLONE=UNIT-08-LUNA-GRAY",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"sd0037.{APEX}",
        "content": "REEL-SD-0037: 46m14s room-tone calibration recorded 1989-08-29 in an empty booth. At 31:14.2001 (+48dB): chair creaks, lyric sheet turns, D4-E4-F4-A4 hum, whisper: 'Marcus, you left the red light on.'",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"echoes.{APEX}",
        "content": "WIPED-ECHOES-REGISTER: Echo01=0x1102; Echo02=0x2441; PairXOR=0x1102^0x2441==0x3543; Echo03=0x3810; Echo04=0x0A55; Echo05=0x1F22; Echo06=0x01A7; Full6WayXOR=0x1983; Gate15=0xEC1B",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"akasaka.{APEX}",
        "content": "KAMOME-NET-PC98-BBS: Akasaka late-night FM dubbing node (2400 baud). Phase-drift offset +3.5500 Hz. https://stardust-archive.net/forensics/kamome_net.html",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"paju.{APEX}",
        "content": "PAJU-SW-4625KHZ: DMZ shortwave listening post recorded Sublevel B2 sideband spill at 14.2001 Hz. https://stardust-archive.net/dyad",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"coyoacan.{APEX}",
        "content": "RED-COYOACAN-104.9FM: UNAM collective decoded Cassette #19 ('Two Voices in One Throat'). Parity: 0x1102 ^ 0x2441 == 0x3543. https://stardust-archive.net/lyrics/two-voices.lrc",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"relcom.{APEX}",
        "content": "RELCOM-UUCP-NODE08: Bell-103 300-baud acoustic dump cut onto X-ray roentgenizdat plates in Leningrad (1990). Gate15: TURING 0xEC1B.",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"ashford.{APEX}",
        "content": "JANET-UK-AC-ASHFORD: VBI Line 21 pulldown resets phase-locked to 14.2001 Hz ('STILL IN B2'). https://stardust-archive.net/forensics/ashford_poly.html",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"munich.{APEX}",
        "content": "CRYSTAL-PROMISE-1981: Catalog OR-8104 ('Shining City'). Two Munich actors paid DM 800 on 1981-04-12 to front Orion's proto-array. https://stardust-archive.net/lyrics/shining-city-1981.lrc",
        "ttl": 3600,
    },
    {
        "type": "TXT",
        "name": f"minitel.{APEX}",
        "content": "3615-ORION-VIDEOTEX: Paris V.23 Minitel kiosk mirror storing 1987 Sublevel B2 lyric phoneme tables (0x1983 -> 0xEC1B).",
        "ttl": 3600,
    },
    {
        "type": "LOC",
        "name": f"b2-114.{APEX}",
        "data": {
            "lat_degrees": 34,
            "lat_minutes": 5,
            "lat_seconds": 53.52,
            "lat_direction": "N",
            "long_degrees": 118,
            "long_minutes": 19,
            "long_seconds": 19.56,
            "long_direction": "W",
            "altitude": 74.0,
            "size": 1.0,
            "precision_horz": 5.0,
            "precision_vert": 1.0,
        },
        "ttl": 3600,
    },
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    if not path.exists():
        return sha256_text(str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "schema": "stardust-lyrics-dns-seeder/v1.0",
        "cooldown_seconds": COOLDOWN_SECONDS,
        "urls": {},
        "last_cf_dns_sync": None,
        "last_run_utc": None,
    }


def save_state(state: Dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state["last_run_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def collect_target_urls_and_hashes() -> List[Tuple[str, str]]:
    """Returns (canonical_url, content_sha256) pairs for all lyrics & DNS endpoints."""
    items: List[Tuple[str, str]] = []

    index_hash = sha256_file(SITE_LYRICS_DIR / "index.html")
    items.append((f"https://{APEX}/lyrics", index_hash))

    mb_hash = sha256_file(SITE_LYRICS_DIR / "musicbrainz-catalog.json")
    items.append((f"https://{APEX}/api/musicbrainz-catalog.json", mb_hash))

    bind_hash = sha256_file(BIND_ZONE_PATH)
    items.append((f"https://{APEX}/.well-known/dns-txt.json", bind_hash))
    items.append((f"https://{APEX}/dns-query?name=b2-114.{APEX}&type=ANY", bind_hash))

    for slug in LRC_SLUGS:
        lrc_path = SITE_LYRICS_DIR / f"{slug}.lrc"
        items.append((f"https://{APEX}/lyrics/{slug}.lrc", sha256_file(lrc_path)))

    return items


def filter_due_urls(
    url_hash_pairs: List[Tuple[str, str]],
    state: Dict[str, Any],
    now_ts: float,
    force: bool = False,
) -> List[Tuple[str, str]]:
    urls_state = state.setdefault("urls", {})
    due: List[Tuple[str, str]] = []
    for url, content_hash in url_hash_pairs:
        prev = urls_state.get(url)
        if force or not prev:
            due.append((url, content_hash))
            continue
        prev_hash = prev.get("hash")
        prev_ts = float(prev.get("timestamp", 0.0))
        if prev_hash != content_hash or (now_ts - prev_ts) >= COOLDOWN_SECONDS:
            due.append((url, content_hash))
    return due


def sync_cloudflare_dns_if_configured(dry_run: bool = False) -> Dict[str, Any]:
    token = os.environ.get("CF_API_TOKEN", "").strip()
    zone_id = os.environ.get("CF_ZONE_ID", "").strip()
    if not token or not zone_id:
        return {
            "status": "skipped",
            "reason": "CF_API_TOKEN and/or CF_ZONE_ID environment variables not set; using edge DoH endpoints & static BIND file.",
            "bind_zone_file": str(BIND_ZONE_PATH),
        }

    if dry_run:
        return {
            "status": "dry_run",
            "records_prepared": len(CLOUDFLARE_DNS_RECORDS),
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "StardustSublevelB2Seeder/6.1",
    }
    synced = 0
    errors: List[str] = []

    for rec in CLOUDFLARE_DNS_RECORDS:
        api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        payload = json.dumps(rec).encode("utf-8")
        req = urllib.request.Request(api_url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if 200 <= resp.status < 300:
                    synced += 1
        except urllib.error.HTTPError as e:
            # 81057 / 81058 = record already exists, which is benign
            body = ""
            try:
                body = e.read().decode("utf-8", errors="ignore")
            except Exception:
                pass
            if "81057" in body or "81058" in body or "already exists" in body.lower():
                synced += 1
            else:
                errors.append(f"{rec['type']} {rec['name']}: HTTP {e.code}")
        except Exception as e:
            errors.append(f"{rec['type']} {rec['name']}: {e}")

    return {
        "status": "synced" if not errors else "partial",
        "records_synced": synced,
        "errors": errors,
    }


def submit_indexnow(urls: List[str], dry_run: bool = False) -> Dict[str, Any]:
    if not urls:
        return {"status": "noop", "submitted_count": 0}
    if dry_run:
        return {"status": "dry_run", "submitted_count": len(urls)}

    payload = {
        "host": APEX,
        "key": INDEXNOW_KEY,
        "keyLocation": f"https://{APEX}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "StardustSublevelB2Seeder/6.1 (+https://stardust-archive.net/lyrics)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {"status": "ok", "http_status": resp.status, "submitted_count": len(urls)}
    except urllib.error.HTTPError as e:
        return {"status": "http_error", "http_status": e.code, "submitted_count": len(urls)}
    except Exception as e:
        return {"status": "offline_or_skipped", "detail": str(e), "submitted_count": len(urls)}


def warm_rag_proxies(
    urls: List[str],
    dry_run: bool = False,
    delay_seconds: float = 3.0,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if not urls:
        return results

    # Select core markdown-digestible endpoints to warm gently
    warm_targets = [
        u for u in urls if u.endswith("/lyrics") or u.endswith(".lrc") or u.endswith(".json")
    ][:6]

    for idx, target_url in enumerate(warm_targets):
        for proxy_prefix in ("https://r.jina.ai/", "https://markdown.new/"):
            proxy_url = f"{proxy_prefix}{target_url}"
            if dry_run:
                results.append({"proxy_url": proxy_url, "status": "dry_run"})
                continue

            req = urllib.request.Request(
                proxy_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; StardustArchivist/6.1; +https://stardust-archive.net/lyrics)",
                    "Accept": "text/markdown, text/plain, */*",
                },
                method="GET",
            )
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    results.append({"proxy_url": proxy_url, "status": resp.status})
                # Gentle 3-second jittered delay between live external requests
                jitter = delay_seconds + random.uniform(0.1, 0.85)
                time.sleep(jitter)
            except urllib.error.HTTPError as e:
                results.append({"proxy_url": proxy_url, "status": e.code, "detail": f"HTTP {e.code}"})
                if e.code == 403:
                    # Sandbox proxy block; break early so sandboxed test runs finish fast
                    break
                jitter = delay_seconds + random.uniform(0.1, 0.85)
                time.sleep(jitter)
            except Exception as e:
                results.append({"proxy_url": proxy_url, "status": "unreachable", "detail": str(e)})
                break
        if results and (results[-1].get("status") == "unreachable" or results[-1].get("status") == 403):
            break

    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stateful Sublevel B2-114 DNS TXT/LOC & Steganographic .LRC Seeder"
    )
    parser.add_argument("--dry-run", action="store_true", help="Verify hashes & state without network calls")
    parser.add_argument("--force", action="store_true", help="Ignore 6-hour cooldown window")
    parser.add_argument(
        "--delay",
        type=float,
        default=3.0,
        help="Base delay in seconds between r.jina.ai / markdown.new warm requests (default: 3.0)",
    )
    args = parser.parse_args()

    now_ts = time.time()
    state = load_state()
    all_pairs = collect_target_urls_and_hashes()
    due_pairs = filter_due_urls(all_pairs, state, now_ts, force=args.force)
    due_urls = [u for u, _ in due_pairs]

    cf_result = sync_cloudflare_dns_if_configured(dry_run=args.dry_run)
    state["last_cf_dns_sync"] = cf_result

    indexnow_result = submit_indexnow(due_urls, dry_run=args.dry_run)
    rag_results = warm_rag_proxies(due_urls, dry_run=args.dry_run, delay_seconds=args.delay)

    # Record updated hashes & timestamps in state file when not in dry-run or sandbox-blocked mode
    urls_state = state.setdefault("urls", {})
    sandbox_blocked = (
        indexnow_result.get("http_status") == 403
        or indexnow_result.get("status") == "offline_or_skipped"
    )
    if not args.dry_run and not sandbox_blocked:
        for url, content_hash in due_pairs:
            urls_state[url] = {
                "hash": content_hash,
                "timestamp": now_ts,
                "last_seeded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ts)),
            }

    save_state(state)

    summary = {
        "total_monitored_urls": len(all_pairs),
        "urls_due_for_seeding": len(due_urls),
        "cooldown_hours": COOLDOWN_SECONDS / 3600.0,
        "cloudflare_dns": cf_result,
        "indexnow": indexnow_result,
        "rag_proxy_warming": rag_results,
        "state_file": str(STATE_PATH),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
