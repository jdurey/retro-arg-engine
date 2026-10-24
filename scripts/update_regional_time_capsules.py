#!/usr/bin/env python3
"""
PROJECT STARDUST // REGIONAL TIME-CAPSULE ARTIFACTS SEEDER & STATE MANAGER
==========================================================================
Python 3.9+ stdlib-only, anti-spam, rate-limited regional seeder for the
7 Continental Vintage-Hardware Time-Capsule Artifacts (/regional/artifacts/*):

1. Content-Hash Deduplication & 6-Hour Cooldown (deploy/regional_capsule_state.json):
   - Computes SHA-256 hashes of every static HTML exhibit and raw vintage-protocol
     dump in site/regional/artifacts/.
   - Enforces a strict 6-hour (21,600s) cooldown per regional node AND skips
     unchanged hashes within the cooldown window.
2. Targeted Regional IndexNow Submission:
   - Yandex IndexNow (https://yandex.com/indexnow) for RU/UA (SU-REL)
   - Naver IndexNow (https://searchadvisor.naver.com/indexnow) for KR (KR-DMZ)
   - Seznam IndexNow (https://search.seznam.cz/indexnow) for EU (FR-PAR, GB-ASH, DE-HAM, SU-REL)
   - Bing & Global IndexNow (https://www.bing.com/indexnow, https://api.indexnow.org/indexnow)
3. Gentle RAG Proxy Cache-Warming (r.jina.ai & markdown.new):
   - Uses 3-second jittered sleeps (3.0s - 3.9s) between requests and triggers
     immediate HTTP 429 exponential/cooldown backoff.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ARTIFACTS_DIR = REPO_ROOT / "site" / "regional" / "artifacts"
STATE_PATH = REPO_ROOT / "deploy" / "regional_capsule_state.json"

APEX = "stardust-archive.net"
INDEXNOW_KEY = "37feeed875722863fda484c68e6695e5"
COOLDOWN_SECONDS = 6 * 3600  # 6-hour anti-spam cooldown per regional node
JITTER_BASE_SECONDS = 3.0

INDEXNOW_ENDPOINTS: dict[str, str] = {
    "yandex_ru_ua": "https://yandex.com/indexnow",
    "naver_kr": "https://searchadvisor.naver.com/indexnow",
    "seznam_eu": "https://search.seznam.cz/indexnow",
    "bing_global": "https://www.bing.com/indexnow",
    "indexnow_global": "https://api.indexnow.org/indexnow",
}

REGIONAL_CAPSULE_NODES: list[dict[str, Any]] = [
    {
        "node_id": "INDEX-GLOBAL",
        "region": "Global Master Index",
        "lang": "en",
        "files": ["index.html", "regional-artifacts.json"],
        "urls": [
            f"https://{APEX}/regional/artifacts",
            f"https://{APEX}/regional/artifacts/index.html",
            f"https://{APEX}/api/regional-artifacts.json",
        ],
        "warm_urls": [
            f"https://{APEX}/regional/artifacts/index.html",
        ],
        "indexnow_targets": ["yandex_ru_ua", "naver_kr", "seznam_eu", "bing_global", "indexnow_global"],
    },
    {
        "node_id": "JP-TYO",
        "region": "Japan (Akasaka Studio 3 // NEC PC-9801RA)",
        "lang": "ja",
        "files": ["pc98_kamome_1985.html", "kamome_bbs_1985.d88.txt"],
        "urls": [
            f"https://{APEX}/regional/artifacts/pc98_kamome_1985.html",
            f"https://{APEX}/regional/artifacts/kamome_bbs_1985.d88.txt",
        ],
        "warm_urls": [
            f"https://{APEX}/regional/artifacts/pc98_kamome_1985.html",
        ],
        "indexnow_targets": ["bing_global", "indexnow_global"],
    },
    {
        "node_id": "KR-DMZ",
        "region": "South Korea (Sewoon Sangga & Paju DMZ // Hitel VT100)",
        "lang": "ko",
        "files": ["hitel_gonova_1994.html", "hitel_gonova_1994.ans"],
        "urls": [
            f"https://{APEX}/regional/artifacts/hitel_gonova_1994.html",
            f"https://{APEX}/regional/artifacts/hitel_gonova_1994.ans",
        ],
        "warm_urls": [
            f"https://{APEX}/regional/artifacts/hitel_gonova_1994.html",
        ],
        "indexnow_targets": ["naver_kr", "bing_global", "indexnow_global"],
    },
    {
        "node_id": "FR-PAR",
        "region": "France (FNAC Paris // PTT Minitel 1B 3615 ORION)",
        "lang": "fr",
        "files": ["minitel_3615_orion.html", "minitel_3615_orion.vdt"],
        "urls": [
            f"https://{APEX}/regional/artifacts/minitel_3615_orion.html",
            f"https://{APEX}/regional/artifacts/minitel_3615_orion.vdt",
        ],
        "warm_urls": [
            f"https://{APEX}/regional/artifacts/minitel_3615_orion.html",
        ],
        "indexnow_targets": ["seznam_eu", "bing_global", "indexnow_global"],
    },
    {
        "node_id": "GB-ASH",
        "region": "United Kingdom (Ashford Polytechnic // BBC Ceefax Page 888)",
        "lang": "en-GB",
        "files": ["ceefax_page888_1989.html", "ceefax_page888_1989.tti"],
        "urls": [
            f"https://{APEX}/regional/artifacts/ceefax_page888_1989.html",
            f"https://{APEX}/regional/artifacts/ceefax_page888_1989.tti",
        ],
        "warm_urls": [
            f"https://{APEX}/regional/artifacts/ceefax_page888_1989.html",
        ],
        "indexnow_targets": ["seznam_eu", "bing_global", "indexnow_global"],
    },
    {
        "node_id": "SU-REL",
        "region": "Eastern Europe (Leningrad Roentgenizdat & Relcom Node-08)",
        "lang": "ru/uk",
        "files": ["roentgenizdat_relcom_08.html", "relcom_node08_1990.uucp"],
        "urls": [
            f"https://{APEX}/regional/artifacts/roentgenizdat_relcom_08.html",
            f"https://{APEX}/regional/artifacts/relcom_node08_1990.uucp",
        ],
        "warm_urls": [
            f"https://{APEX}/regional/artifacts/roentgenizdat_relcom_08.html",
        ],
        "indexnow_targets": ["yandex_ru_ua", "seznam_eu", "bing_global", "indexnow_global"],
    },
    {
        "node_id": "DE-HAM",
        "region": "Germany (Munich Bavaria Filmstudios & Deutsche Bundespost Btx)",
        "lang": "de",
        "files": ["btx_crystal_promise_1981.html", "btx_crystal_promise_1981.btx"],
        "urls": [
            f"https://{APEX}/regional/artifacts/btx_crystal_promise_1981.html",
            f"https://{APEX}/regional/artifacts/btx_crystal_promise_1981.btx",
        ],
        "warm_urls": [
            f"https://{APEX}/regional/artifacts/btx_crystal_promise_1981.html",
        ],
        "indexnow_targets": ["seznam_eu", "bing_global", "indexnow_global"],
    },
    {
        "node_id": "LATAM-MX-BR",
        "region": "Latin America (Mexico DF Red Coyoacan & Sao Paulo Radio Pirata)",
        "lang": "es/pt-BR",
        "files": ["sonidero_coyoacan_1989.html", "red_coyoacan_1989.fidonet"],
        "urls": [
            f"https://{APEX}/regional/artifacts/sonidero_coyoacan_1989.html",
            f"https://{APEX}/regional/artifacts/red_coyoacan_1989.fidonet",
        ],
        "warm_urls": [
            f"https://{APEX}/regional/artifacts/sonidero_coyoacan_1989.html",
        ],
        "indexnow_targets": ["bing_global", "indexnow_global"],
    },
]


def ensure_static_artifacts_exist() -> None:
    """Ensure site/regional/artifacts/* exists by syncing from deploy/regional_time_capsules.js if needed."""
    if (SITE_ARTIFACTS_DIR / "index.html").exists() and (SITE_ARTIFACTS_DIR / "pc98_kamome_1985.html").exists():
        return
    js_module = REPO_ROOT / "deploy" / "regional_time_capsules.js"
    if not js_module.exists():
        return
    SITE_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPO_ROOT / "site" / "api").mkdir(parents=True, exist_ok=True)
    node_sync = (
        "import('./deploy/regional_time_capsules.js').then(async m => {"
        "const fs = await import('node:fs'); const path = await import('node:path');"
        "const out = 'site/regional/artifacts';"
        "fs.writeFileSync(path.join(out, 'index.html'), m.buildRegionalArtifactsIndexHtml(), 'utf8');"
        "const j = m.buildRegionalArtifactsJson();"
        "fs.writeFileSync(path.join(out, 'regional-artifacts.json'), j, 'utf8');"
        "fs.writeFileSync('site/api/regional-artifacts.json', j, 'utf8');"
        "for (const a of m.REGIONAL_ARTIFACTS) {"
        "  fs.writeFileSync(path.join(out, a.htmlSlug), m.renderRegionalCapsuleHtml(a), 'utf8');"
        "  fs.writeFileSync(path.join(out, a.rawSlug), a.rawDumpContent, 'utf8');"
        "}"
        "});"
    )
    try:
        subprocess.run(["node", "-e", node_sync], cwd=str(REPO_ROOT), check=True, timeout=15)
    except Exception as exc:
        print(f"[warn] Static sync via node failed: {exc}", file=sys.stderr)


def compute_node_hash(files: list[str]) -> str:
    hasher = hashlib.sha256()
    for fname in sorted(files):
        fpath = SITE_ARTIFACTS_DIR / fname
        hasher.update(fname.encode("utf-8"))
        if fpath.exists():
            hasher.update(fpath.read_bytes())
        else:
            hasher.update(b"<MISSING>")
    return hasher.hexdigest()


def load_state() -> dict[str, Any]:
    if STATE_PATH.exists():
        try:
            data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("nodes", {})
                data.setdefault("proxy_backoff_until", {})
                return data
        except Exception:
            pass
    return {
        "schema": "stardust-regional-capsule-seeder-state/v1.0",
        "cooldown_seconds": COOLDOWN_SECONDS,
        "last_run_utc": None,
        "proxy_backoff_until": {},
        "nodes": {},
    }


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state["last_run_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def submit_indexnow(urls: list[str], target_names: list[str], dry_run: bool = False) -> dict[str, int]:
    results: dict[str, int] = {}
    payload = json.dumps(
        {
            "host": APEX,
            "key": INDEXNOW_KEY,
            "keyLocation": f"https://{APEX}/{INDEXNOW_KEY}.txt",
            "urlList": urls,
        }
    ).encode("utf-8")

    for name in target_names:
        ep = INDEXNOW_ENDPOINTS.get(name)
        if not ep:
            continue
        if dry_run:
            results[name] = 200
            continue
        try:
            req = urllib.request.Request(
                ep,
                data=payload,
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                    "User-Agent": "Stardust-Regional-TimeCapsule-Seeder/1.0 (+https://stardust-archive.net)",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                results[name] = int(resp.status)
        except urllib.error.HTTPError as exc:
            results[name] = int(exc.code)
        except Exception:
            results[name] = 0
    return results


def warm_rag_proxies(
    urls: list[str],
    state: dict[str, Any],
    dry_run: bool = False,
    sleep_seconds: float = JITTER_BASE_SECONDS,
) -> dict[str, dict[str, int]]:
    proxies = {
        "r.jina.ai": "https://r.jina.ai/",
        "markdown.new": "https://markdown.new/",
    }
    backoff_map: dict[str, float] = state.setdefault("proxy_backoff_until", {})
    now = time.time()
    report: dict[str, dict[str, int]] = {}

    for u in urls:
        report[u] = {}
        for proxy_name, prefix in proxies.items():
            backoff_until = float(backoff_map.get(proxy_name, 0.0) or 0.0)
            if now < backoff_until:
                report[u][proxy_name] = -429  # Skipped due to active 429 backoff
                continue
            if dry_run:
                report[u][proxy_name] = 200
                continue

            if sleep_seconds > 0:
                jitter = sleep_seconds + random.uniform(0.05, 0.75)
                time.sleep(jitter)

            target_url = f"{prefix}{u}"
            try:
                req = urllib.request.Request(
                    target_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; StardustRegionalArchiver/1.0; +https://stardust-archive.net)",
                        "Accept": "text/markdown, text/plain, */*;q=0.8",
                    },
                    method="GET",
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    _ = resp.read(1024)
                    report[u][proxy_name] = int(resp.status)
            except urllib.error.HTTPError as exc:
                code = int(exc.code)
                report[u][proxy_name] = code
                if code == 429:
                    # Immediate 429 backoff: halt hitting this proxy for 6 hours
                    backoff_map[proxy_name] = time.time() + COOLDOWN_SECONDS
                    print(
                        f"  [!] HTTP 429 from {proxy_name}; engaging immediate 6-hour backoff.",
                        file=sys.stderr,
                    )
            except Exception:
                report[u][proxy_name] = 0
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rate-limited Regional Time-Capsule Artifacts Seeder (6h cooldown + SHA-256 deduplication)."
    )
    parser.add_argument("--dry-run", action="store_true", help="Verify hashes and state transitions without network I/O.")
    parser.add_argument("--force", action="store_true", help="Bypass 6-hour cooldown (still respects 429 backoff).")
    parser.add_argument(
        "--sleep",
        type=float,
        default=JITTER_BASE_SECONDS,
        help="Base sleep seconds before RAG proxy requests (default: 3.0s + jitter).",
    )
    args = parser.parse_args()

    ensure_static_artifacts_exist()
    state = load_state()
    nodes_state: dict[str, Any] = state.setdefault("nodes", {})
    now = time.time()
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))

    seeded_count = 0
    skipped_count = 0

    print("==============================================================================")
    print(f" PROJECT STARDUST // REGIONAL TIME-CAPSULE SEEDER ({now_iso})")
    print(f" Cooldown: {COOLDOWN_SECONDS}s (6h) | Dry-Run: {args.dry_run} | State: {STATE_PATH.name}")
    print("==============================================================================")

    for node in REGIONAL_CAPSULE_NODES:
        node_id = node["node_id"]
        current_hash = compute_node_hash(node["files"])
        prev = nodes_state.get(node_id, {})
        prev_hash = prev.get("content_sha256")
        last_epoch = float(prev.get("last_seeded_epoch", 0.0) or 0.0)
        elapsed = now - last_epoch
        cooldown_active = elapsed < COOLDOWN_SECONDS
        hash_changed = current_hash != prev_hash

        if not args.force and cooldown_active and not hash_changed:
            remaining_min = int((COOLDOWN_SECONDS - elapsed) // 60)
            print(
                f" [SKIP] {node_id:<12} ({node['lang']:<8}) | Hash unchanged ({current_hash[:12]}) "
                f"& cooldown active ({remaining_min}m remaining)"
            )
            skipped_count += 1
            continue

        reason = "FORCE" if args.force else ("HASH_CHANGED" if hash_changed else "COOLDOWN_EXPIRED")
        print(f" [SEED] {node_id:<12} ({node['lang']:<8}) | Reason: {reason} | Hash: {current_hash[:12]}")

        indexnow_statuses = submit_indexnow(
            node["urls"],
            node["indexnow_targets"],
            dry_run=args.dry_run,
        )
        rag_statuses = warm_rag_proxies(
            node["warm_urls"],
            state,
            dry_run=args.dry_run,
            sleep_seconds=args.sleep,
        )

        nodes_state[node_id] = {
            "region": node["region"],
            "lang": node["lang"],
            "content_sha256": current_hash,
            "last_seeded_epoch": round(now, 3),
            "last_seeded_utc": now_iso,
            "last_trigger_reason": reason,
            "urls": node["urls"],
            "indexnow_statuses": indexnow_statuses,
            "rag_proxy_statuses": rag_statuses,
        }
        seeded_count += 1
        save_state(state)

    save_state(state)
    print("------------------------------------------------------------------------------")
    print(f" Completed Regional Capsule Pass: {seeded_count} seeded, {skipped_count} skipped (cooldown/dedup).")
    print(f" State persisted to: {STATE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
