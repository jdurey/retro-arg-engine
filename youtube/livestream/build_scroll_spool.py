#!/usr/bin/env python3
"""
Builds the master multilingual Usenet + Regional BBS + YouTube Comment rolling scroll
spool (`youtube/livestream/usenet_youtube_scroll_spool.json`) for the right-side
livestream terminal overlay.
"""
import glob
import html
import json
import re
import textwrap
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT_JSON = Path(__file__).resolve().parent / "usenet_youtube_scroll_spool.json"


def wrap_line(line: str, width: int = 44) -> list[str]:
    line = line.rstrip()
    if not line:
        return [""]
    # Keep ASCII dividers intact
    if set(line) <= set("-=_+*~# ") and len(line) > 8:
        return [line[:width]]
    # For CJK lines (Japanese/Korean), wrap at shorter character count since glyphs are 2x wide
    has_cjk = any("\u3000" <= ch <= "\u9fff" or "\uac00" <= ch <= "\ud7af" for ch in line)
    eff_w = 24 if has_cjk else width
    if len(line) <= eff_w:
        return [line]
    if has_cjk:
        return [line[i : i + eff_w] for i in range(0, len(line), eff_w)]
    return textwrap.wrap(line, width=eff_w, break_long_words=True, replace_whitespace=False) or [""]


def fetch_youtube_comments() -> list[tuple[str, str, str]]:
    def fetch_video_ids(url: str) -> list[str]:
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}
            )
            page = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
            vids = []
            for vid in re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', page):
                if vid not in vids:
                    vids.append(vid)
            return vids[:18]
        except Exception:
            return []

    def fetch_for_video(vid: str) -> list[tuple[str, str, str]]:
        try:
            watch_url = f"https://www.youtube.com/watch?v={vid}"
            req = urllib.request.Request(
                watch_url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}
            )
            page = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
            m_title = re.search(r'"title":\{"runs":\[\{"text":"([^"]+)"', page)
            vtitle = m_title.group(1) if m_title else vid
            tokens = re.findall(r'"continuationCommand":\{"token":"([^"]+)"', page)
            out = []
            for tok in tokens[-2:]:
                payload = json.dumps(
                    {
                        "context": {"client": {"clientName": "WEB", "clientVersion": "2.20250101.00.00"}},
                        "continuation": tok,
                    }
                ).encode("utf-8")
                creq = urllib.request.Request(
                    "https://www.youtube.com/youtubei/v1/next?prettyPrint=false",
                    data=payload,
                    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
                )
                cjson = urllib.request.urlopen(creq, timeout=10).read().decode("utf-8", errors="ignore")
                data = json.loads(cjson)
                mutations = (
                    data.get("frameworkUpdates", {}).get("entityBatchUpdate", {}).get("mutations", [])
                )
                for mut in mutations:
                    cep = mut.get("payload", {}).get("commentEntityPayload", {})
                    if cep:
                        author = cep.get("author", {}).get("displayName", "@listener")
                        content = cep.get("properties", {}).get("content", {}).get("content", "")
                        if content:
                            out.append((author, content.replace("\r", " ").strip(), vtitle))
            return out
        except Exception:
            return []

    vids = (
        ["N71E_Cn6ULQ"]
        + fetch_video_ids("https://www.youtube.com/@NovaHart_Official/videos")
        + fetch_video_ids("https://www.youtube.com/@NovaHart_Official/streams")
    )
    seen_vids = set()
    seen_texts = set()
    comments = []
    for v in vids[:16]:
        if v in seen_vids:
            continue
        seen_vids.add(v)
        for author, text, title in fetch_for_video(v):
            sig = f"{author}:{text[:40]}"
            if sig not in seen_texts:
                seen_texts.add(sig)
                comments.append((author, text, title))
    return comments


def build_blocks() -> list[list[dict]]:
    blocks: list[list[dict]] = []

    def add_block(tag: str, header: str, raw_lines: list[str], color: str = "green") -> None:
        blk = [
            {"text": "=" * 44, "color": "dim"},
            {"text": f"[{tag}] {header}"[:44], "color": "amber"},
            {"text": "-" * 44, "color": "dim"},
        ]
        for rl in raw_lines:
            c = color
            if rl.startswith(("From:", "Subject:", "Date:", "Newsgroups:", "De:", "Asunto:", "번호:", "제목:", "No.")):
                c = "amber"
            elif rl.startswith(">"):
                c = "cyan"
            for wl in wrap_line(rl, 44):
                blk.append({"text": wl, "color": c})
        blk.append({"text": "", "color": "dim"})
        blocks.append(blk)

    # 1. Community Investigator's Report (Pinned #1)
    add_block(
        "COMMUNITY REPORT",
        "PROJECT STARDUST: FIRST 10 ENTRIES 🥝",
        [
            "From: Community Investigator // Usenet Audit",
            "Subject: WHAT WE HAVE DISCOVERED (ENTRIES 1-20)",
            "1. Nova Hart & Echo-1..6: Kestrel claims 14",
            "   regional pressings of SYNTHESIS carried",
            "   hidden messages; Echo-1..6 purged in 1981",
            "   ('We don't sign stars. We build them').",
            "   -> CORROBORATED in Entry #21 (Memo 81-044)!",
            "2. STARDUST, UNIT-7 & LUNA: 1989 fire in B2-114",
            "   destroyed TWIN-68; H.A.R.R.I.S.O.N. & Luna.",
            "   -> CORROBORATED in Entry #27 ('By Order of",
            "      Harmony' sung by Director Harrison)!",
            "3. Marcus Hale Paradox: Missing 1 May 1988 vs",
            "   present at Sept 9, 1989 fire + 4 personas.",
            "   -> SOLVED in Entry #23 (4-Node Drift Sum)!",
            "4. Nodes 11-14 in Orbit (240.4 ms delay) &",
            "   'ORION BUILT A PATCH NOT A STAR' /",
            "   'WHEN THE HATCH IS OPEN, WHO WALKS IN?'",
            "   -> AUDIO & OSCILLOSCOPE LOGS in #24 & #26!",
            "5. 1989 Fire: LAFD Report #89-0909-B2 & LA",
            "   Times Sept 10, 1989 clipping in Entry #22!",
            "6. Mexico 1988 Coyoacan Cassette & Korea Paju",
            "   12.00m (14.2001 Hz) Blueprint in #24 & #25!",
            "7. NEXT STEP: Type 'KESTREL' or 'HATCH-OVERRIDE'",
            "   at stardust-archive.net/forensics!",
        ],
        color="bright",
    )

    # 2. All 13 Multilingual Regional BBS / Usenet Nodes in Original Languages
    for p in sorted(glob.glob(str(REPO / "site" / "regional" / "*" / "index.html"))):
        node_dir = Path(p).parent.name.upper()
        raw_html = Path(p).read_text(encoding="utf-8", errors="ignore")
        clean = html.unescape(re.sub(r"<[^>]+>", "", raw_html))
        lines = [l.strip() for l in clean.splitlines() if l.strip()]
        if lines:
            add_block(f"REGIONAL {node_dir}", lines[0], lines[1:32], color="bright")

    # 3. Canonical Hand-Crafted Threads across all Usenet Newsgroups (t*.txt)
    for p in sorted(glob.glob(str(REPO / "site" / "usenet" / "*" / "t*.txt"))):
        ng = Path(p).parent.name.replace("-", ".")
        fname = Path(p).name
        lines = Path(p).read_text(encoding="utf-8", errors="ignore").splitlines()
        body = [l for l in lines if not l.startswith(("Path:", "Message-ID:", "NNTP-Posting-Host:", "X-Newsreader:", "Lines:", "Organization:"))]
        add_block(f"USENET {ng}", fname, body[:55], color="green")

    # 4. Primary Evidence Threads #11-#30 in alt.conspiracy
    alt_files = [
        "s11037.txt", "s10772.txt", "s01939.txt", "s12107.txt", "s02842.txt",
        "s20827.txt", "s07454.txt", "s22486.txt", "s22965.txt", "s23876.txt",
        "s21794.txt", "s17914.txt", "s01207.txt", "s10066.txt", "s02239.txt",
        "s24262.txt", "s20400.txt", "s10410.txt",
    ]
    for fn in alt_files:
        fp = REPO / "site" / "usenet" / "alt-conspiracy" / fn
        if fp.exists():
            lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
            body = [l for l in lines if not l.startswith(("Path:", "Message-ID:", "NNTP-Posting-Host:", "X-Newsreader:", "Lines:", "Organization:"))]
            add_block("alt.conspiracy", fn, body[:55], color="green")

    return blocks


def main() -> None:
    blocks = build_blocks()
    yt_comments = fetch_youtube_comments()
    print(f"Loaded {len(blocks)} Usenet/BBS blocks and {len(yt_comments)} real YouTube comments")

    # Interleave: after every Usenet/Regional block, insert 3-4 real YouTube comments!
    final_lines: list[dict] = []
    yt_idx = 0
    for b_idx, blk in enumerate(blocks):
        final_lines.extend(blk)
        if yt_comments:
            final_lines.append({"text": "=" * 44, "color": "dim"})
            final_lines.append({"text": "[YOUTUBE LIVE COMMUNITY & COMMENT FEED]", "color": "amber"})
            final_lines.append({"text": "-" * 44, "color": "dim"})
            for _ in range(4):
                author, text, vtitle = yt_comments[yt_idx % len(yt_comments)]
                yt_idx += 1
                clean_title = vtitle.split("[")[0].split("(")[0].strip()[:26].rstrip()
                final_lines.append({"text": f"[YT] {author} ({clean_title}):"[:44], "color": "amber"})
                for wl in wrap_line(f'"{text}"', 44)[:10]:
                    final_lines.append({"text": wl, "color": "bright"})
                final_lines.append({"text": "", "color": "dim"})

    OUT_JSON.write_text(json.dumps({"total_lines": len(final_lines), "lines": final_lines}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(final_lines)} scroll lines to {OUT_JSON}")


if __name__ == "__main__":
    main()
