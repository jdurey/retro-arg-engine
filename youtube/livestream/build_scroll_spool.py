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


def clean_terminal_str(s: str) -> str:
    # Replace smart quotes/dashes, strip :shortcode: tokens, and strip non-BMP emoji characters
    s = s.replace("\r", " ").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("—", "--").replace("–", "-")
    s = re.sub(r":[a-zA-Z0-9_-]{3,32}:", "", s)
    out = []
    for ch in s:
        cp = ord(ch)
        if cp > 0xFFFF or (0x2600 <= cp <= 0x27BF) or (0xFE00 <= cp <= 0xFE0F):
            continue
        out.append(ch)
    return "".join(out)


def wrap_line(line: str, width: int = 44) -> list[str]:
    out_lines: list[str] = []
    for sub in clean_terminal_str(line).split("\n"):
        sub = sub.rstrip()
        if not sub:
            out_lines.append("")
            continue
        if set(sub) <= set("-=_+*~# ") and len(sub) > 8:
            out_lines.append(sub[:width])
            continue
        has_cjk = any("\u3000" <= ch <= "\u9fff" or "\uac00" <= ch <= "\ud7af" for ch in sub)
        eff_w = 24 if has_cjk else width
        if len(sub) <= eff_w:
            out_lines.append(sub)
        elif has_cjk:
            out_lines.extend(sub[i : i + eff_w] for i in range(0, len(sub), eff_w))
        else:
            out_lines.extend(textwrap.wrap(sub, width=eff_w, break_long_words=True) or [""])
    return out_lines or [""]


def fetch_youtube_comments() -> list[tuple[str, str, str]]:
    cache_path = Path(__file__).resolve().parent / "youtube_comments_cache.json"
    cached_items: list[tuple[str, str, str]] = []
    if cache_path.exists():
        try:
            raw_c = json.loads(cache_path.read_text(encoding="utf-8"))
            for item in raw_c:
                if isinstance(item, list) and len(item) == 3:
                    cached_items.append((str(item[0]), str(item[1]), str(item[2])))
        except Exception:
            pass

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
            return vids[:30]
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
            for tok in tokens[-3:]:
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
                        if "retronewsdesk" in author.lower():
                            author = "@StardustArchivist_89"
                        content = cep.get("properties", {}).get("content", {}).get("content", "")
                        if content:
                            out.append((author, content.strip(), vtitle))
            return out
        except Exception:
            return []

    vids = (
        ["N71E_Cn6ULQ"]
        + fetch_video_ids("https://www.youtube.com/@NovaHart_Official/videos")
        + fetch_video_ids("https://www.youtube.com/@NovaHart_Official/streams")
        + fetch_video_ids("https://www.youtube.com/@NovaHart_Official/shorts")
    )
    seen_vids = set()
    seen_texts = set()
    comments: list[tuple[str, str, str]] = []
    for v in vids[:36]:
        if v in seen_vids:
            continue
        seen_vids.add(v)
        for author, text, title in fetch_for_video(v):
            sig = f"{author}:{text[:40]}"
            if sig not in seen_texts:
                seen_texts.add(sig)
                comments.append((author, text, title))

    # Merge with cached items so older/rate-limited comments are preserved
    for author, text, title in cached_items:
        sig = f"{author}:{text[:40]}"
        if sig not in seen_texts:
            seen_texts.add(sig)
            comments.append((author, text, title))

    if comments:
        try:
            cache_path.write_text(json.dumps(comments, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
    return comments


def _dedupe_usenet_lines(lines: list[str]) -> list[str]:
    """Removes boilerplate NNTP headers and consecutive duplicate quoted/unquoted paragraphs."""
    skip_prefixes = (
        "Path:",
        "Message-ID:",
        "NNTP-Posting-Host:",
        "X-Newsreader:",
        "Lines:",
        "Organization:",
        "References:",
        "Xref:",
        "X-Anonymously-To:",
        "Comments: This message was forwarded",
    )
    filtered = [l for l in lines if not l.startswith(skip_prefixes)]
    quoted_norms = {
        re.sub(r"\s+", " ", l.lstrip("> ").strip()).lower()
        for l in filtered
        if l.startswith(">") and len(l.lstrip("> ").strip()) > 18
    }
    out: list[str] = []
    for l in filtered:
        norm = re.sub(r"\s+", " ", l.strip()).lower()
        if not l.startswith(">") and norm in quoted_norms:
            continue
        if out and l.strip() == out[-1].strip() and not l.strip():
            continue
        out.append(l)
    return out


def make_block(tag: str, header: str, raw_lines: list[str], color: str = "green", max_lines: int = 16) -> list[dict]:
    blk = [
        {"text": "=" * 44, "color": "dim"},
        {"text": clean_terminal_str(f"[{tag}] {header}")[:44], "color": "amber"},
        {"text": "-" * 44, "color": "dim"},
    ]
    body_count = 0
    for rl in raw_lines:
        if body_count >= max_lines:
            break
        c = color
        if rl.startswith(("From:", "Subject:", "Date:", "Newsgroups:", "De:", "Asunto:", "번호:", "제목:", "No.", "От:", "Тема:")):
            c = "amber"
        elif rl.startswith(">"):
            c = "cyan"
        for wl in wrap_line(rl, 44):
            if body_count >= max_lines:
                break
            blk.append({"text": wl, "color": c})
            body_count += 1
    blk.append({"text": "", "color": "dim"})
    return blk


def build_blocks(rotation_seed: int = 0) -> tuple[list[list[dict]], list[list[dict]]]:
    import random

    rng = random.Random(rotation_seed)
    usenet_blocks: list[list[dict]] = []
    regional_blocks: list[list[dict]] = []

    # 1. All Living Usenet 1995 Chronological Dispatches (`s00901.txt`+ in `src/site_static/usenet/` or `site/usenet/`)
    seen_files = set()
    living_candidates = sorted(
        list(glob.glob(str(REPO / "src" / "site_static" / "usenet" / "*" / "s009*.txt")))
        + list(glob.glob(str(REPO / "site" / "usenet" / "*" / "s009*.txt")))
    )
    seen_living_names = set()
    for p in living_candidates:
        fp = Path(p)
        key = f"{fp.parent.name}/{fp.name}"
        if key in seen_living_names:
            continue
        seen_living_names.add(key)
        seen_files.add(str(fp))
        ng = fp.parent.name.replace("-", ".")
        lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        body = _dedupe_usenet_lines(lines)
        usenet_blocks.append(make_block(f"LIVE 1995 // {ng}", fp.name, body, color="bright", max_lines=16))

    # 2. All 13 Multilingual Regional BBS Nodes in Original Languages
    for p in sorted(glob.glob(str(REPO / "site" / "regional" / "*" / "index.html"))):
        node_dir = Path(p).parent.name.upper()
        raw_html = Path(p).read_text(encoding="utf-8", errors="ignore")
        raw_html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw_html, flags=re.S | re.I)
        clean = html.unescape(re.sub(r"<[^>]+>", "", raw_html))
        lines = [l.strip() for l in clean.splitlines() if l.strip()]
        if lines:
            regional_blocks.append(make_block(f"BBS {node_dir}", lines[0], lines[1:22], color="bright", max_lines=15))

    # 3. Primary Evidence Threads in alt.conspiracy
    alt_files = [
        "t21.txt", "t22.txt", "t23.txt", "t24.txt", "t25.txt",
        "t26.txt", "t27.txt", "t28.txt", "t29.txt", "t30.txt",
        "s11037.txt", "s01939.txt", "s12107.txt", "s02842.txt",
        "s20827.txt", "s07454.txt", "s22486.txt", "s22965.txt", "s23876.txt",
        "s21794.txt", "s17914.txt", "s01207.txt", "s10066.txt", "s02239.txt",
        "s24262.txt", "s20400.txt", "s10410.txt",
    ]
    for fn in alt_files:
        for base_dir in (REPO / "site" / "usenet" / "alt-conspiracy", REPO / "src" / "site_static" / "usenet" / "alt.conspiracy"):
            fp = base_dir / fn
            if fp.exists() and fn not in seen_living_names:
                seen_living_names.add(fn)
                seen_files.add(str(fp))
                lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
                body = _dedupe_usenet_lines(lines)
                usenet_blocks.append(make_block("alt.conspiracy", fn, body, color="green", max_lines=16))
                break

    # 4. Canonical Threads across Stardust Usenet Newsgroups (`t*.txt`)
    for p in sorted(glob.glob(str(REPO / "site" / "usenet" / "*" / "t*.txt"))):
        if str(Path(p)) in seen_files or "rec-arts-movies-action" in p:
            continue
        seen_files.add(str(Path(p)))
        ng = Path(p).parent.name.replace("-", ".")
        fname = Path(p).name
        lines = Path(p).read_text(encoding="utf-8", errors="ignore").splitlines()
        body = _dedupe_usenet_lines(lines)
        usenet_blocks.append(make_block(f"USENET {ng}", fname, body, color="green", max_lines=16))

    # 5. Rotating sample of 45 Swarm Usenet Discussions (`s*.txt`) across all newsgroups
    swarm_dirs = sorted(glob.glob(str(REPO / "src" / "site_static" / "usenet" / "*")))
    swarm_pool: list[Path] = []
    for d in swarm_dirs:
        dp = Path(d)
        if not dp.is_dir() or "movies" in dp.name:
            continue
        files = sorted(dp.glob("s*.txt"))
        if files:
            swarm_pool.extend(rng.sample(files, min(8, len(files))))
    rng.shuffle(swarm_pool)
    for fp in swarm_pool[:45]:
        if str(fp) in seen_files:
            continue
        seen_files.add(str(fp))
        ng = fp.parent.name.replace("-", ".")
        lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        body = _dedupe_usenet_lines(lines)
        usenet_blocks.append(make_block(f"USENET {ng}", fp.name, body, color="green", max_lines=15))

    # Shuffle Usenet & Regional blocks per rotation cycle while keeping Living 1995 dispatches frequent
    rng.shuffle(usenet_blocks)
    rng.shuffle(regional_blocks)
    return usenet_blocks, regional_blocks


def main() -> None:
    import time

    rotation_seed = int(time.time() // 900)  # Rotates order every 15 minutes
    usenet_blocks, regional_blocks = build_blocks(rotation_seed=rotation_seed)
    yt_comments = fetch_youtube_comments()
    import random

    rng = random.Random(rotation_seed)
    if yt_comments:
        rng.shuffle(yt_comments)
    print(
        f"Loaded {len(usenet_blocks)} Usenet blocks, {len(regional_blocks)} Multilingual BBS blocks, "
        f"and {len(yt_comments)} real YouTube comments (rotation_seed={rotation_seed})"
    )

    # Tightly interleave concise Usenet posts, 3 YouTube comments, and Regional BBS posts
    # so both Usenet & YouTube comments are ALWAYS visible on screen together and rotate every few seconds!
    final_lines: list[dict] = []
    yt_idx = 0
    reg_idx = 0
    for idx, u_blk in enumerate(usenet_blocks):
        final_lines.extend(u_blk)
        if yt_comments:
            final_lines.append({"text": "=" * 44, "color": "dim"})
            final_lines.append({"text": "[YOUTUBE LIVE COMMUNITY & COMMENT FEED]", "color": "amber"})
            final_lines.append({"text": "-" * 44, "color": "dim"})
            added_yt = 0
            tries = 0
            while added_yt < 3 and tries < len(yt_comments):
                author, text, vtitle = yt_comments[yt_idx % len(yt_comments)]
                yt_idx += 1
                tries += 1
                cleaned_body = clean_terminal_str(text).strip()
                if len(cleaned_body) < 3:
                    continue
                ct = clean_terminal_str(vtitle).split("[")[0].split("(")[0].strip()
                ct = re.sub(r"^Nova\s+Hart\s*[-—:]+\s*", "", ct, flags=re.I)
                ct = re.sub(r"^Full\s+80s\s+Rock\s+Opera\s*[-—:]*\s*", "Midnight Protocol", ct, flags=re.I).strip() or "Nova Hart"
                max_ct = max(6, 36 - len(author))
                if len(ct) > max_ct:
                    ct = ct[:max_ct].rstrip()
                final_lines.append({"text": clean_terminal_str(f"[YT] {author} ({ct}):")[:44], "color": "amber"})
                for wl in wrap_line(f'"{cleaned_body}"', 44)[:4]:
                    if wl:
                        final_lines.append({"text": wl, "color": "bright"})
                final_lines.append({"text": "", "color": "dim"})
                added_yt += 1
        if regional_blocks and (idx % 2 == 0):
            final_lines.extend(regional_blocks[reg_idx % len(regional_blocks)])
            reg_idx += 1

    tmp_out = OUT_JSON.with_suffix(".tmp.json")
    tmp_out.write_text(
        json.dumps({"total_lines": len(final_lines), "rotation_seed": rotation_seed, "lines": final_lines}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    import os

    os.replace(tmp_out, OUT_JSON)
    print(f"Wrote {len(final_lines)} scroll lines to {OUT_JSON}")


if __name__ == "__main__":
    main()
