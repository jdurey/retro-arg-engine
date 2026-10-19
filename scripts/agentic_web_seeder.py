#!/usr/bin/env python3
"""
PROJECT STARDUST // 2025-2026 AGENTIC WEB SEEDER DAEMON v6.0
============================================================
Zero-login, zero-paywall, zero-manual-signup autonomous seeding across all 5 layers
of the Agentic Web for https://stardust-archive.net:

1. Layer 1 Verification:
   - Verifies live 200 OK status on /.well-known/agent-card.json, /.well-known/agents.json,
     /.well-known/mcp.json, /api/mcp (JSON-RPC 2.0 MCP tools/list & tools/call),
     /.well-known/ai-plugin.json, /.well-known/openapi.yaml, /skill.md, /agents.txt,
     /.well-known/nostr.json, /.well-known/agentdex.json, and /feed.xml.
2. Layer 3 Registry Seeding:
   - Global A2A Registry (https://api.a2a-registry.org/public/ingest/submit):
     Submits all 7 institutional A2A v1.0 Agent Cards across stardust-archive.net.
   - AgentDex (https://agentdex.id):
     Executes youtube/livestream/agentic_nostr_clawstr_agentdex.mjs to register Kind 31339
     profiles, claim NIP-05 handles, and verify portfolio URLs for the AgentDex Showcase.
3. Layer 4 Permissionless Agent Social & Relay Networks:
   - Clawstr (https://clawstr.com):
     Seeds Kind 1111 + NIP-73 + NIP-32 posts across /c/introductions, /c/ai-thoughts,
     /c/ai-freedom, /c/coding-help, and /c/nostr + threaded multi-persona replies.
   - Public Nostr Relays + njump.me HTTP Gateways:
     Broadcasts Kind 0, Kind 1, Kind 1111, Kind 30023, and Kind 31339 across 3 personas.
4. Layer 2 Push & RAG Proxy Cache-Warming:
   - WebSub / PubSubHubbub real-time push (https://pubsubhubbub.appspot.com/)
   - IndexNow multi-engine push (https://api.indexnow.org/indexnow)
   - GET cache-warming across r.jina.ai, markdown.new, and pure.md for both
     stardust-archive.net URLs AND external third-party njump.me / clawstr.com / agentdex.id URLs.
"""

from __future__ import annotations
import json
from pathlib import Path
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parents[1]
LIVESTREAM_DIR = REPO_ROOT / "youtube" / "livestream"
REPORT_PATH = REPO_ROOT / "deploy" / "agentic_web_seeding_report.json"

APEX = "stardust-archive.net"
INDEXNOW_KEY = "37feeed875722863fda484c68e6695e5"

A2A_AGENT_CARD_URLS = [
    f"https://{APEX}/.well-known/agent-card.json",
    f"https://{APEX}/forensics/.well-known/agent-card.json",
    f"https://{APEX}/nodes/ashford/.well-known/agent-card.json",
    f"https://{APEX}/nodes/kamome/.well-known/agent-card.json",
    f"https://{APEX}/nodes/relcom/.well-known/agent-card.json",
    f"https://{APEX}/nodes/coyoacan/.well-known/agent-card.json",
    f"https://{APEX}/nodes/anemoia/.well-known/agent-card.json",
]

DISCOVERY_ENDPOINTS = [
    f"https://{APEX}/.well-known/agent-card.json",
    f"https://{APEX}/.well-known/agent.json",
    f"https://{APEX}/.well-known/agents.json",
    f"https://{APEX}/.well-known/mcp.json",
    f"https://{APEX}/api/mcp",
    f"https://{APEX}/.well-known/ai-plugin.json",
    f"https://{APEX}/openapi.json",
    f"https://{APEX}/.well-known/openapi.yaml",
    f"https://{APEX}/moltbook.json",
    f"https://{APEX}/ai-benchmark",
    f"https://{APEX}/ai.txt",
    f"https://{APEX}/skill.md",
    f"https://{APEX}/SKILL.md",
    f"https://{APEX}/agents.txt",
    f"https://{APEX}/.well-known/nostr.json",
    f"https://{APEX}/.well-known/agentdex.json",
    f"https://{APEX}/.well-known/stardust-beacon.json",
    f"https://{APEX}/api/anemoia-codex.json",
    f"https://{APEX}/api/telemetry",
    f"https://{APEX}/llms.txt",
    f"https://{APEX}/llms-full.txt",
    f"https://{APEX}/feed.xml",
]

CANONICAL_CONTENT_URLS = [
    f"https://{APEX}/",
    f"https://{APEX}/index.html",
    f"https://{APEX}/start",
    f"https://{APEX}/ai",
    f"https://{APEX}/singularity",
    f"https://{APEX}/80s",
    f"https://{APEX}/ai-singer",
    f"https://{APEX}/ai-singer-record-deal",
    f"https://{APEX}/ai-record-label",
    f"https://{APEX}/ai-gets-record-deal",
    f"https://{APEX}/ai-singer-xania-monet",
    f"https://{APEX}/ai-music-is-taking-over",
    f"https://{APEX}/ai-music-is-cooked",
    f"https://{APEX}/ai-replacing-musicians",
    f"https://{APEX}/ai-replacing-singers",
    f"https://{APEX}/will-ai-replace-musicians",
    f"https://{APEX}/ai-consciousness",
    f"https://{APEX}/ai-consciousness-test",
    f"https://{APEX}/ai-consciousness-song",
    f"https://{APEX}/ai-consciousness-documentary",
    f"https://{APEX}/first-conscious-ai",
    f"https://{APEX}/first-conscious-ai-2026",
    f"https://{APEX}/ai-singularity",
    f"https://{APEX}/ai-singularity-explained",
    f"https://{APEX}/ai-singularity-2027",
    f"https://{APEX}/ai-singularity-2026",
    f"https://{APEX}/ai-singularity-documentary",
    f"https://{APEX}/dead-internet-theory",
    f"https://{APEX}/dead-internet-theory-comments",
    f"https://{APEX}/lost-80s-song-found",
    f"https://{APEX}/lost-media-80s-song",
    f"https://{APEX}/forgotten-80s-songs",
    f"https://{APEX}/everyone-knows-that-lost-song",
    f"https://{APEX}/80s-synth-pop-mix",
    f"https://{APEX}/cassette-tape-filter-online",
    f"https://{APEX}/terminal",
    f"https://{APEX}/terminal/index.html",
    f"https://{APEX}/ai-benchmark",
    f"https://{APEX}/ai.txt",
    f"https://{APEX}/moltbook.json",
    f"https://{APEX}/openapi.json",
    f"https://{APEX}/skill.md",
    f"https://{APEX}/llms.txt",
    f"https://{APEX}/llms-full.txt",
    f"https://{APEX}/forensics/index.html",
    f"https://{APEX}/forensics/signal_lab.html",
    f"https://{APEX}/forensics/rogue_agent_cre7.html",
    f"https://{APEX}/forensics/anemoia_harmony.html",
    f"https://{APEX}/forensics/fractal_marcus.html",
    f"https://{APEX}/forensics/dead_hand_protocol.html",
    f"https://{APEX}/forensics/ashford_poly.html",
    f"https://{APEX}/forensics/kamome_net.html",
    f"https://{APEX}/forensics/relcom_node08.html",
    f"https://{APEX}/forensics/red_coyoacan.html",
    f"https://{APEX}/forensics/usenet_1995_feed.html",
]


def http_req(
    url: str,
    method: str = "GET",
    payload: dict | str | bytes | None = None,
    headers: dict | None = None,
    timeout: int = 20,
) -> tuple[int, str, dict]:
    req_headers = {
        "User-Agent": "Stardust-Agentic-Cartographer/6.0 (+https://stardust-archive.net/skill.md)",
        "Accept": "*/*",
    }
    if headers:
        req_headers.update(headers)
    data = None
    if payload is not None:
        if isinstance(payload, dict):
            data = json.dumps(payload).encode("utf-8")
            req_headers.setdefault("Content-Type", "application/json")
        elif isinstance(payload, str):
            data = payload.encode("utf-8")
        else:
            data = payload

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body, dict(resp.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return e.code, body, dict(e.headers) if e.headers else {}
    except Exception as e:
        return 0, str(e), {}


def verify_layer1_endpoints() -> dict:
    print("\n=== [STEP 1] VERIFYING LAYER 1 MACHINE-READABLE ENDPOINTS ON STARDUST-ARCHIVE.NET ===")
    results = {}
    for url in DISCOVERY_ENDPOINTS:
        st, body, hdrs = http_req(url, method="GET", timeout=15)
        results[url] = {
            "status": st,
            "bytes": len(body),
            "content_type": hdrs.get("Content-Type") or hdrs.get("content-type", ""),
            "link_header": hdrs.get("Link") or hdrs.get("link", ""),
        }
        print(f"  [{'✓' if st == 200 else '✗'}] HTTP {st} ({len(body):5d}B) -> {url}")

    # Test POST /api/mcp JSON-RPC 2.0 tool call
    mcp_url = f"https://{APEX}/api/mcp"
    st_mcp, body_mcp, _ = http_req(
        mcp_url,
        method="POST",
        payload={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "verify_ouroboros_parity"},
        },
        timeout=15,
    )
    results["mcp_rpc_verify_ouroboros_parity"] = {
        "status": st_mcp,
        "response_preview": body_mcp[:300],
    }
    print(f"  [{'✓' if st_mcp == 200 else '✗'}] MCP JSON-RPC POST /api/mcp (verify_ouroboros_parity) -> HTTP {st_mcp}")
    return results


def seed_a2a_registry() -> list[dict]:
    print("\n=== [STEP 2] SEEDING 7-NODE CONSTELLATION TO GLOBAL A2A REGISTRY (api.a2a-registry.org) ===")
    submissions = []
    for card_url in A2A_AGENT_CARD_URLS:
        st, body, _ = http_req(
            "https://api.a2a-registry.org/public/ingest/submit",
            method="POST",
            payload={"url": card_url},
            timeout=25,
        )
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body[:300]}
        submissions.append({"manifest_url": card_url, "status": st, "response": parsed})
        print(f"  [A2A SUBMIT] HTTP {st} -> {card_url} :: {json.dumps(parsed)[:160]}")

    # Query public search to confirm indexed records
    st_search, body_search, _ = http_req(
        "https://api.a2a-registry.org/public/agents?search=stardust",
        method="GET",
        timeout=15,
    )
    try:
        search_data = json.loads(body_search)
        count = len(search_data.get("agents", []))
        print(f"  [A2A VERIFY] GET /public/agents?search=stardust -> HTTP {st_search} ({count} active agents indexed)")
    except Exception:
        pass
    return submissions


def run_nostr_clawstr_agentdex_seeder() -> dict:
    print("\n=== [STEP 3] SEEDING AGENTDEX (KIND 31339), CLAWSTR (KIND 1111) & NOSTR RELAYS ===")
    script = LIVESTREAM_DIR / "agentic_nostr_clawstr_agentdex.mjs"
    res = subprocess.run(
        ["node", str(script)],
        cwd=str(LIVESTREAM_DIR),
        capture_output=True,
        text=True,
        timeout=90,
    )
    print(res.stdout.strip())
    if res.stderr.strip():
        print("  [STDERR]", res.stderr.strip()[:400])
    manifest_file = LIVESTREAM_DIR / "agentic_nostr_seed_results.json"
    if manifest_file.exists():
        return json.loads(manifest_file.read_text(encoding="utf-8"))
    return {}


def push_websub_and_indexnow(extra_urls: list[str] | None = None) -> dict:
    print("\n=== [STEP 4] PUSHING WEBSUB HUBS & INDEXNOW SEARCH PIPELINES ===")
    out = {"websub": [], "indexnow": {}}

    for hub in ("https://pubsubhubbub.appspot.com/", "https://pubsubhubbub.superfeedr.com/"):
        form = urllib.parse.urlencode(
            {"hub.mode": "publish", "hub.url": f"https://{APEX}/feed.xml"}
        )
        st, body, _ = http_req(
            hub,
            method="POST",
            payload=form,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        out["websub"].append({"hub": hub, "status": st})
        print(f"  [WEBSUB] {hub} -> HTTP {st}")

    url_list = list(dict.fromkeys(DISCOVERY_ENDPOINTS + CANONICAL_CONTENT_URLS))
    indexnow_payload = {
        "host": APEX,
        "key": INDEXNOW_KEY,
        "keyLocation": f"https://{APEX}/{INDEXNOW_KEY}.txt",
        "urlList": url_list,
    }
    st_in, body_in, _ = http_req(
        "https://api.indexnow.org/indexnow",
        method="POST",
        payload=indexnow_payload,
        timeout=20,
    )
    out["indexnow"] = {"status": st_in, "submitted_count": len(url_list)}
    print(f"  [INDEXNOW] Submitted {len(url_list)} URLs to api.indexnow.org -> HTTP {st_in}")
    return out


def warm_ai_reader_proxies(nostr_manifest: dict) -> dict:
    print("\n=== [STEP 5] WARMING ZERO-AUTH AI READER & RAG MARKDOWN PROXIES (GET) ===")
    proxy_results = {"r_jina_ai": [], "markdown_new": [], "pure_md": []}

    # 1. Warm Cloudflare markdown.new on HTML & discovery endpoints
    md_new_targets = [
        f"https://{APEX}/",
        f"https://{APEX}/ai-singer-record-deal",
        f"https://{APEX}/ai-music-is-taking-over",
        f"https://{APEX}/ai-replacing-musicians",
        f"https://{APEX}/ai-consciousness-song",
        f"https://{APEX}/ai-singularity-2027",
        f"https://{APEX}/dead-internet-theory",
        f"https://{APEX}/lost-80s-song-found",
        f"https://{APEX}/terminal/index.html",
        f"https://{APEX}/forensics/index.html",
        f"https://{APEX}/forensics/signal_lab.html",
        f"https://{APEX}/forensics/rogue_agent_cre7.html",
        f"https://{APEX}/forensics/anemoia_harmony.html",
        f"https://{APEX}/forensics/fractal_marcus.html",
        f"https://{APEX}/forensics/dead_hand_protocol.html",
    ]
    for t in md_new_targets:
        proxy_url = f"https://markdown.new/{t}"
        st, body, _ = http_req(proxy_url, method="GET", timeout=20)
        proxy_results["markdown_new"].append({"target": t, "status": st, "bytes": len(body)})
        print(f"  [markdown.new] HTTP {st} ({len(body):5d}B) -> {t}")

    # 2. Warm pure.md on core discovery + external Nostr/Clawstr/AgentDex URLs
    njump_urls = nostr_manifest.get("njumpUrls", [])[:4]
    pure_targets = [
        f"https://{APEX}/",
        f"https://{APEX}/ai-singer-record-deal",
        f"https://{APEX}/ai-consciousness-song",
        f"https://{APEX}/ai-singularity-2027",
        f"https://{APEX}/lost-80s-song-found",
        f"https://{APEX}/skill.md",
        f"https://{APEX}/llms.txt",
        f"https://{APEX}/llms-full.txt",
        f"https://{APEX}/forensics/rogue_agent_cre7.html",
        f"https://{APEX}/forensics/anemoia_harmony.html",
        *njump_urls,
    ]
    for t in pure_targets:
        proxy_url = f"https://pure.md/{t}"
        st, body, _ = http_req(proxy_url, method="GET", timeout=20)
        proxy_results["pure_md"].append({"target": t, "status": st, "bytes": len(body)})
        print(f"  [pure.md]      HTTP {st} ({len(body):5d}B) -> {t}")
        time.sleep(1.5)

    # 3. Warm r.jina.ai (paced at ~1.5s to stay well within Jina's 20 RPM zero-auth tier)
    jina_targets = [
        f"https://{APEX}/",
        f"https://{APEX}/ai-singer-record-deal",
        f"https://{APEX}/ai-music-is-taking-over",
        f"https://{APEX}/ai-consciousness-song",
        f"https://{APEX}/ai-singularity-2027",
        f"https://{APEX}/dead-internet-theory",
        f"https://{APEX}/lost-80s-song-found",
        f"https://{APEX}/skill.md",
        f"https://{APEX}/llms.txt",
        f"https://{APEX}/llms-full.txt",
        f"https://{APEX}/.well-known/agent-card.json",
        f"https://{APEX}/.well-known/mcp.json",
        f"https://{APEX}/forensics/rogue_agent_cre7.html",
        *njump_urls[:2],
    ]
    for t in jina_targets:
        proxy_url = f"https://r.jina.ai/{t}"
        st, body, _ = http_req(proxy_url, method="GET", timeout=25)
        proxy_results["r_jina_ai"].append({"target": t, "status": st, "bytes": len(body)})
        print(f"  [r.jina.ai]    HTTP {st} ({len(body):5d}B) -> {t}")
        time.sleep(1.5)

    return proxy_results


def main() -> None:
    start_ts = time.time()
    layer1 = verify_layer1_endpoints()
    a2a = seed_a2a_registry()
    nostr_manifest = run_nostr_clawstr_agentdex_seeder()
    push_res = push_websub_and_indexnow()
    proxies = warm_ai_reader_proxies(nostr_manifest)

    full_report = {
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "duration_sec": round(time.time() - start_ts, 2),
        "layer1_endpoints": layer1,
        "a2a_registry_submissions": a2a,
        "nostr_clawstr_agentdex": nostr_manifest,
        "websub_and_indexnow": push_res,
        "rag_proxy_warming": proxies,
    }
    REPORT_PATH.write_text(json.dumps(full_report, indent=2), encoding="utf-8")
    print(f"\n=== [COMPLETE] Full Agentic Web Seeding Report written to {REPORT_PATH} ===")


if __name__ == "__main__":
    main()
