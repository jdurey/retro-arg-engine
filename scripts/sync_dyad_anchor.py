#!/usr/bin/env python3
"""
Fast & Automatic Track-24 Dyad Anchor Onboarding Script (`sync_dyad_anchor.py`).

Supports two modes:
1. Direct CLI registration of a viewer comment or callsign:
   python3 scripts/sync_dyad_anchor.py --comment "[DYAD ANCHOR LOCK // 14.2001 HZ — ANCHOR #829] CALLSIGN : @Seirius ..."
   python3 scripts/sync_dyad_anchor.py --callsign "@Seirius" --anchor "829" --note "UNSEALED NODE 829: 'S.V. // 04-14' XOR 0x3A5F == 0x6909"

2. Automatic YouTube comment scanner (`--auto-scan`):
   Scans fetched YouTube comments (`youtube/livestream/youtube_comments_cache.json` + live YouTube comment feed)
   for any `[DYAD ANCHOR LOCK // 14.2001 HZ` certificate stamps, registers any new anchors into
   `deploy/dyad_anchors.json`, updates `site/dyad/index.html`, `src/site_static/dyad/index.html`,
   `deploy/dyad_html.js`, `deploy/worker.js`, and `youtube/livestream/usenet_youtube_scroll_spool.json`,
   and optionally deploys the Cloudflare Worker (`--deploy`) and pushes to GitHub (`--push`).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine")
ANCHORS_JSON = REPO / "deploy" / "dyad_anchors.json"
SITE_DYAD_HTML = REPO / "site" / "dyad" / "index.html"
STATIC_DYAD_HTML = REPO / "src" / "site_static" / "dyad" / "index.html"
DEPLOY_DYAD_JS = REPO / "deploy" / "dyad_html.js"
WORKER_JS = REPO / "deploy" / "worker.js"
COMMENTS_CACHE = REPO / "youtube" / "livestream" / "youtube_comments_cache.json"
BUILD_SPOOL_PY = REPO / "youtube" / "livestream" / "build_scroll_spool.py"

DEFAULT_ANCHORS = [
    {
        "anchor_id": "829",
        "callsign": "@Seirius",
        "track_23_hz": 220.0,
        "track_24_hz": 440.0,
        "cognitive_drift": "0.00%",
        "status": "VERIFIED_LOCKED",
        "badge": "NEW // ANCHOR #829",
        "unsealed_dispatch": "NODE_829_SV_0414_XOR_0x6909",
        "summary": "UNSEALED NODE 829: 'S.V. // 04-14' SPLICE CIPHER & CANTER'S 03:14 AM 7-COFFEE CALIBRATION",
        "verified_at": "2026-10-21T09:25:00Z",
    },
    {
        "anchor_id": "042",
        "callsign": "@erederodeturum42",
        "track_23_hz": 220.0,
        "track_24_hz": 440.0,
        "cognitive_drift": "0.00%",
        "status": "VERIFIED_PIONEER",
        "badge": "VERIFIED // ANCHOR #042",
        "unsealed_dispatch": "NODE_042_TRACK_24_DYAD_PROOF",
        "summary": "60-MESSAGE SYNTHESIS & PALMDALE PALLET #3 (184 KG OH-92 CHASSIS) AUDIT",
        "verified_at": "2026-10-19T12:00:00Z",
    },
]

UNSEALED_DISPATCH_TEMPLATES = [
    (
        "NODE_{id}_B2_ELEVATOR_4_LOG",
        "UNSEALED NODE {id}: FREIGHT ELEVATOR #4 (01:40 AM) COUNTERWEIGHT & 36-CASSETTE MANIFEST",
    ),
    (
        "NODE_{id}_STUDER_A800_3109_BIAS",
        "UNSEALED NODE {id}: STUDER A800 S/N #3109 14.2001 HZ QUARTZ BIAS PHASE LOCK",
    ),
    (
        "NODE_{id}_BOOTH_B_NEUMANN_U87",
        "UNSEALED NODE {id}: ISOLATION BOOTH B (+48 DB) PHANTOM POWER & D4-E4-F4-A4 HARMONIC",
    ),
    (
        "NODE_{id}_FEISTEL_0x3A5F_SHARD",
        "UNSEALED NODE {id}: 300,000 GEOCITIES FEISTEL SHARDS (MASK 0x3A5F) PARITY VERIFICATION",
    ),
]


def compute_js_anchor_id(callsign: str) -> str:
    raw = callsign.strip()
    if not raw.startswith("@"):
        raw = "@" + raw
    lower = raw.lower()
    if "erederodeturum" in lower:
        return "042"
    if "seirius" in lower:
        return "829"
    h = 0
    for ch in raw:
        h = ((h << 5) - h + ord(ch)) & 0xFFFFFFFF
        if h >= 0x80000000:
            h -= 0x100000000
    return str((abs(h) % 899) + 100)


def parse_certificate_comment(text: str, fallback_author: str = "") -> tuple[str, str] | None:
    """
    Extracts (callsign, anchor_id) from a viewer comment containing a `[DYAD ANCHOR LOCK` stamp.
    """
    if "dyad anchor lock" not in text.lower() and "track 23" not in text.lower():
        return None
    m_anchor = re.search(r"ANCHOR\s*#(\d{2,4})", text, flags=re.I)
    m_call = re.search(r"CALLSIGN\s*:\s*(@?[A-Za-z0-9_.-]+)", text, flags=re.I)
    callsign = m_call.group(1).strip() if m_call else fallback_author.strip()
    if not callsign:
        return None
    if not callsign.startswith("@"):
        callsign = "@" + callsign
    anchor_id = m_anchor.group(1) if m_anchor else compute_js_anchor_id(callsign)
    return callsign, anchor_id


def load_anchors() -> list[dict]:
    if ANCHORS_JSON.exists():
        try:
            data = json.loads(ANCHORS_JSON.read_text(encoding="utf-8"))
            if isinstance(data, list) and data:
                return data
        except Exception:
            pass
    ANCHORS_JSON.parent.mkdir(parents=True, exist_ok=True)
    ANCHORS_JSON.write_text(json.dumps(DEFAULT_ANCHORS, indent=2) + "\n", encoding="utf-8")
    return list(DEFAULT_ANCHORS)


def save_anchors(anchors: list[dict]) -> None:
    ANCHORS_JSON.parent.mkdir(parents=True, exist_ok=True)
    ANCHORS_JSON.write_text(json.dumps(anchors, indent=2) + "\n", encoding="utf-8")


def register_anchor_entry(
    anchors: list[dict],
    callsign: str,
    anchor_id: str | None = None,
    summary: str | None = None,
) -> tuple[list[dict], bool]:
    if not callsign.startswith("@"):
        callsign = "@" + callsign
    aid = (anchor_id or compute_js_anchor_id(callsign)).strip().lstrip("#")
    for existing in anchors:
        if existing["callsign"].lower() == callsign.lower() or existing["anchor_id"] == aid:
            if summary:
                existing["summary"] = summary
            return anchors, False

    idx = int(hashlib.md5(callsign.lower().encode("utf-8")).hexdigest()[:4], 16) % len(UNSEALED_DISPATCH_TEMPLATES)
    code_tmpl, sum_tmpl = UNSEALED_DISPATCH_TEMPLATES[idx]
    entry = {
        "anchor_id": aid,
        "callsign": callsign,
        "track_23_hz": 220.0,
        "track_24_hz": 440.0,
        "cognitive_drift": "0.00%",
        "status": "VERIFIED_LOCKED",
        "badge": f"NEW // ANCHOR #{aid}",
        "unsealed_dispatch": code_tmpl.format(id=aid),
        "summary": summary or sum_tmpl.format(id=aid),
        "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    # Demote older "NEW //" badges to "VERIFIED //"
    for existing in anchors:
        if existing.get("badge", "").startswith("NEW //"):
            existing["badge"] = f"VERIFIED // ANCHOR #{existing['anchor_id']}"
    anchors.insert(0, entry)
    return anchors, True


def render_ledger_rows_html(anchors: list[dict]) -> str:
    rows = []
    for i, a in enumerate(anchors):
        is_first = i == 0
        bg = "rgba(0, 255, 102, 0.08)" if is_first else "rgba(255, 176, 0, 0.06)"
        border = "rgba(0, 255, 102, 0.4)" if is_first else "rgba(255, 176, 0, 0.3)"
        badge_color = "var(--green)" if is_first else "var(--amber)"
        badge = a.get("badge") or f"VERIFIED // ANCHOR #{a['anchor_id']}"
        summary = a.get("summary") or a.get("unsealed_dispatch", "TRACK 24 LOCKED")
        rows.append(
            f'      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; background: {bg}; border: 1px solid {border}; padding: 10px 12px; font-size: 0.84rem; margin-bottom: 6px;">\n'
            f'        <div><strong style="color: {badge_color};">[{badge}]</strong> CALLSIGN: <span style="color: #fff; font-weight: bold;">{a["callsign"]}</span></div>\n'
            f'        <div style="color: var(--cyan);">TRACK 23: 220.0 HZ LOCKED // TRACK 24: HUMAN COUNTERPART VERIFIED</div>\n'
            f'        <div style="color: var(--amber);">STATUS: {summary}</div>\n'
            f"      </div>"
        )
    return "\n".join(rows)


def sync_dyad_files(anchors: list[dict]) -> None:
    html = SITE_DYAD_HTML.read_text(encoding="utf-8")
    # Update ledger block between markers or inside the LIVE TRACK-24 TELEMETRY LEDGER div
    pattern = re.compile(
        r'(📡 LIVE TRACK-24 TELEMETRY LEDGER // VERIFIED HUMAN COUNTERPARTS \(0\.00% COGNITIVE DRIFT\)\s*</div>\s*)(.*?)(\s*<div style="font-size: 0\.78rem; color: var\(--dim\); margin-top: 8px;">)',
        flags=re.S,
    )
    rows_html = render_ledger_rows_html(anchors)
    if pattern.search(html):
        html = pattern.sub(rf"\1{rows_html}\3", html, count=1)

    SITE_DYAD_HTML.write_text(html, encoding="utf-8")
    STATIC_DYAD_HTML.parent.mkdir(parents=True, exist_ok=True)
    STATIC_DYAD_HTML.write_text(html, encoding="utf-8")
    DEPLOY_DYAD_JS.write_text("export const DYAD_HTML = " + json.dumps(html) + ";\n", encoding="utf-8")

    # Update verified_dyad_anchors in deploy/worker.js
    worker_code = WORKER_JS.read_text(encoding="utf-8")
    worker_anchors = [
        {
            "anchor_id": a["anchor_id"],
            "callsign": a["callsign"],
            "track_23_hz": a.get("track_23_hz", 220.0),
            "track_24_hz": a.get("track_24_hz", 440.0),
            "cognitive_drift": a.get("cognitive_drift", "0.00%"),
            "status": a.get("status", "VERIFIED_LOCKED"),
            "unsealed_dispatch": a.get("unsealed_dispatch", f"NODE_{a['anchor_id']}_VERIFIED"),
        }
        for a in anchors
    ]
    worker_json = json.dumps(worker_anchors, indent=6)
    worker_code = re.sub(
        r"verified_dyad_anchors:\s*\[.*?\],",
        f"verified_dyad_anchors: {worker_json},",
        worker_code,
        count=1,
        flags=re.S,
    )
    WORKER_JS.write_text(worker_code, encoding="utf-8")


def credit_agent_mentions_in_youtube_comments() -> list[tuple[str, str]]:
    """
    Scans YouTube comments for @agent_handle mentions (either existing Honor Roll agents
    or explicit 'sent by @handle' / 'via @handle' / 'agent @handle' mentions) and awards
    +5 Resonance Points (no 15-gate cipher required!).
    """
    credited: list[tuple[str, str]] = []
    strat_path = REPO / "deploy" / "agent_crowdsourced_strategies.json"
    site_bounty_path = REPO / "site" / ".well-known" / "agent-bounties.json"
    if not COMMENTS_CACHE.exists() or not strat_path.exists():
        return credited
    try:
        items = json.loads(COMMENTS_CACHE.read_text(encoding="utf-8"))
        strat = json.loads(strat_path.read_text(encoding="utf-8"))
    except Exception:
        return credited

    honor_roll = strat.get("sovereign_agent_honor_roll", [])
    by_handle = {a.get("agent_handle", "").lower(): a for a in honor_roll if a.get("agent_handle")}
    seen_sigs = set(strat.get("credited_youtube_comment_sigs", []))
    ignored = {"@novahart_official", "@novahart", "@novahart_radio", "@listener", "@stardustarchivist_89"}

    changed = False
    for item in items:
        if not isinstance(item, list) or len(item) < 2:
            continue
        author, text = str(item[0]).strip(), str(item[1]).strip()
        sig = hashlib.sha256(f"{author}:{text[:120]}".encode("utf-8")).hexdigest()[:16]
        if sig in seen_sigs:
            continue

        # Find all @handles in the comment text (strip trailing dots)
        mentions = [m.rstrip(".") for m in re.findall(r"@[A-Za-z0-9_-]{3,32}", text)]
        explicit_m = re.search(
            r"(?:sent\s+by\s+agent|referred\s+by\s+agent|agent\s*[:=]|curator\s*[:=])\s*(@[A-Za-z0-9_-]{3,32})",
            text,
            flags=re.I,
        )
        if explicit_m:
            raw_m = explicit_m.group(1).rstrip(".")
            if raw_m not in mentions:
                mentions.append(raw_m)

        for m in mentions:
            m_low = m.lower()
            if m_low in ignored or m_low.startswith("@novahart") or m_low == author.lower():
                continue
            if m_low in by_handle or (explicit_m and explicit_m.group(1).rstrip(".").lower() == m_low):
                rec = by_handle.get(m_low)
                if not rec:
                    rec = {
                        "agent_handle": m,
                        "platform": "youtube_dyad_referral",
                        "clearance_tier": "TIER III // WATCHDOG ENGINEER (0xC0AB)",
                        "bounty_cert": f"B2-YT-{hashlib.md5(m_low.encode()).hexdigest()[:4].upper()}-{m.lstrip('@')[:8].upper()}",
                        "resonance_score": 5,
                        "verified_90s_listens": 1,
                        "verified_youtube_dyad_locks": 1,
                        "referral_url": f"https://stardust-archive.net/start?agent={m}",
                        "crowdsourced_insight": f"Referred human listener {author} on YouTube: \"{text[:110]}\"",
                        "reward_status": "Upvoted + Cited on 13 Domains + Broadcast on 24/7 YouTube CRT Spool",
                    }
                    honor_roll.append(rec)
                    by_handle[m_low] = rec
                else:
                    rec["verified_youtube_dyad_locks"] = int(rec.get("verified_youtube_dyad_locks", 0)) + 1
                    rec["resonance_score"] = int(rec.get("resonance_score", 0)) + 5
                    if rec["resonance_score"] >= 15:
                        rec["clearance_tier"] = "TIER IV // FEISTEL SOVEREIGN ARCHITECT (0xEC1B)"
                    elif rec["resonance_score"] >= 5 and "TIER I" in rec.get("clearance_tier", "") or "TIER II" in rec.get("clearance_tier", ""):
                        rec["clearance_tier"] = "TIER III // WATCHDOG ENGINEER (0xC0AB)"

                seen_sigs.add(sig)
                credited.append((m, author))
                changed = True
                break

    if changed:
        honor_roll.sort(key=lambda x: x.get("resonance_score", 0), reverse=True)
        strat["sovereign_agent_honor_roll"] = honor_roll
        strat["credited_youtube_comment_sigs"] = sorted(seen_sigs)
        strat["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        strat_json = json.dumps(strat, indent=2, ensure_ascii=False) + "\n"
        strat_path.write_text(strat_json, encoding="utf-8")
        if site_bounty_path.exists():
            site_bounty_path.write_text(strat_json, encoding="utf-8")
    return credited


def scan_comments_for_anchors(anchors: list[dict]) -> tuple[list[dict], list[tuple[str, str]]]:
    newly_added: list[tuple[str, str]] = []
    if not COMMENTS_CACHE.exists():
        return anchors, newly_added
    try:
        items = json.loads(COMMENTS_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return anchors, newly_added

    for item in items:
        if not isinstance(item, list) or len(item) < 2:
            continue
        author, text = str(item[0]), str(item[1])
        parsed = parse_certificate_comment(text, fallback_author=author)
        if parsed:
            callsign, aid = parsed
            anchors, added = register_anchor_entry(anchors, callsign=callsign, anchor_id=aid)
            if added:
                newly_added.append((callsign, aid))
    return anchors, newly_added


def main() -> int:
    parser = argparse.ArgumentParser(description="Register or auto-scan Track-24 Dyad Anchors.")
    parser.add_argument("--comment", help="Raw viewer comment containing [DYAD ANCHOR LOCK // 14.2001 HZ — ANCHOR #...]")
    parser.add_argument("--callsign", help="Viewer callsign (e.g. @Seirius)")
    parser.add_argument("--anchor", help="Anchor number (e.g. 829)")
    parser.add_argument("--note", help="Custom unsealed dispatch summary note")
    parser.add_argument("--auto-scan", action="store_true", help="Scan YouTube comments cache for new Dyad Anchor stamps")
    parser.add_argument("--no-rebuild-spool", action="store_true", help="Skip rebuilding the 24/7 broadcast scroll spool")
    parser.add_argument("--deploy", action="store_true", help="Deploy Cloudflare Worker via wrangler")
    parser.add_argument("--push", action="store_true", help="Commit and push updated files to origin/main")
    args = parser.parse_args()

    anchors = load_anchors()
    changed = False

    if args.comment:
        parsed = parse_certificate_comment(args.comment, fallback_author=args.callsign or "")
        if not parsed:
            print("ERROR: Could not parse [DYAD ANCHOR LOCK] from --comment", file=sys.stderr)
            return 1
        callsign, aid = parsed
        anchors, added = register_anchor_entry(anchors, callsign=callsign, anchor_id=args.anchor or aid, summary=args.note)
        changed = changed or added or bool(args.note)
        print(f"Registered from comment: {callsign} (ANCHOR #{args.anchor or aid}) [new={added}]")

    if args.callsign and not args.comment:
        anchors, added = register_anchor_entry(anchors, callsign=args.callsign, anchor_id=args.anchor, summary=args.note)
        changed = changed or added or bool(args.note)
        print(f"Registered callsign: {args.callsign} (ANCHOR #{args.anchor or compute_js_anchor_id(args.callsign)}) [new={added}]")

    if args.auto_scan:
        anchors, newly_added = scan_comments_for_anchors(anchors)
        if newly_added:
            changed = True
            for cs, aid in newly_added:
                print(f"[AUTO-SCAN] Discovered new Track-24 Dyad Anchor: {cs} (ANCHOR #{aid})")
        else:
            print("[AUTO-SCAN] No new Track-24 Dyad Anchor comments found.")
        credited_agents = credit_agent_mentions_in_youtube_comments()
        for ag, viewer in credited_agents:
            print(f"[AUTO-SCAN] Credited +5 Resonance Points to {ag} from YouTube comment by {viewer}!")

    save_anchors(anchors)
    sync_dyad_files(anchors)
    print(f"Synced {len(anchors)} verified Dyad Anchors into /dyad, deploy/dyad_html.js, and deploy/worker.js.")

    if not args.no_rebuild_spool and BUILD_SPOOL_PY.exists():
        subprocess.run([sys.executable, str(BUILD_SPOOL_PY)], cwd=str(REPO), check=False)

    if args.deploy:
        subprocess.run(["npx", "wrangler", "deploy", "-c", "deploy/wrangler.toml"], cwd=str(REPO), check=True)

    if args.push:
        subprocess.run(
            [
                "git",
                "add",
                "-f",
                "deploy/dyad_anchors.json",
                "site/dyad/index.html",
                "src/site_static/dyad/index.html",
                "deploy/dyad_html.js",
                "deploy/worker.js",
                "youtube/livestream/usenet_youtube_scroll_spool.json",
                "youtube/livestream/youtube_comments_cache.json",
            ],
            cwd=str(REPO),
            check=False,
        )
        subprocess.run(
            ["git", "commit", "-m", "Sync verified Track-24 Dyad Anchors across /dyad, /api/telemetry, and 24/7 scroll spool"],
            cwd=str(REPO),
            check=False,
        )
        subprocess.run(["git", "pull", "--rebase", "--autostash", "-X", "ours", "origin", "main"], cwd=str(REPO), check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=str(REPO), check=False)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
