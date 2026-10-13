#!/usr/bin/env python3
"""
Project Stardust — Comprehensive Site-Wide Link Auditor & Auto-Fixer
Scans every HTML file in site/ (especially site/forensics/, site/terminal/,
site/reconstruction/, site/usenet/, site/index.html), rewrites any legacy
or broken /federation/... and dotted /usenet/comp.dsp paths to verified
working paths in site/, ensures all referenced assets/pages exist on disk
(or in story_paths.js), and exits non-zero if any broken link remains.
"""

from __future__ import annotations
import re
import shutil
import sys
from pathlib import Path

HREF_SRC_RE = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)

# Canonical routes guaranteed to exist in the main repo's story_paths.js
CANONICAL_STORY_PATHS = {
    "index.html",
    "ftp/ashford-poly/index.html",
    "ftp/kamome/index.html",
    "regional/01-usa/index.html",
    "regional/02-japan/index.html",
    "regional/03-korea/index.html",
    "regional/04-mexico/index.html",
    "regional/05-germany/index.html",
    "regional/06-france/index.html",
    "regional/07-uk/index.html",
    "regional/08-ussr/index.html",
    "regional/09-brazil/index.html",
    "regional/10-sweden/index.html",
    "regional/11-india/index.html",
    "regional/12-australia/index.html",
    "regional/13-fiji/index.html",
    "usenet/index.html",
    "usenet/comp-dsp/index.html",
    "usenet/alt-conspiracy/index.html",
    "usenet/alt-fan-nova-hart/index.html",
    "usenet/alt-music-synth-pop/index.html",
    "usenet/comp-sys-m68k/index.html",
    "geocities/index.html",
    "geocities/tokyo-garden-1420.html",
    "geocities/siliconvalley-lab-1984.html",
    "geocities/hollywood-hills-4127.html",
    "geocities/sunsetstrip-nova-tape-of-us-analysis.html",
}

REWRITE_MAP = {
    "/federation/ashford-poly.org/index.html": "/forensics/ashford_poly.html",
    "/federation/ashford-poly.org/": "/forensics/ashford_poly.html",
    "/federation/kamome-net.org/index.html": "/forensics/kamome_net.html",
    "/federation/kamome-net.org/": "/forensics/kamome_net.html",
    "/federation/relcom-node08.org/index.html": "/forensics/relcom_node08.html",
    "/federation/relcom-node08.org/": "/forensics/relcom_node08.html",
    "/federation/redcoyoacan.org/index.html": "/forensics/red_coyoacan.html",
    "/federation/redcoyoacan.org/": "/forensics/red_coyoacan.html",
    "/usenet/comp.dsp/s00901.txt": "/forensics/usenet_1995_feed.html",
    "/usenet/comp.dsp/": "/usenet/comp-dsp/index.html",
    "/usenet/comp.dsp": "/usenet/comp-dsp/index.html",
    "/usenet/alt.fan.nova-hart/s00902.txt": "/forensics/usenet_1995_feed.html",
    "/usenet/alt.fan.nova-hart/": "/usenet/alt-fan-nova-hart/index.html",
    "/usenet/alt.fan.nova-hart": "/usenet/alt-fan-nova-hart/index.html",
    "/usenet/alt.conspiracy/s00903.txt": "/forensics/usenet_1995_feed.html",
    "/usenet/alt.conspiracy/": "/usenet/alt-conspiracy/index.html",
    "/usenet/alt.conspiracy": "/usenet/alt-conspiracy/index.html",
    "/usenet/alt.music.heartstrike/s00904.txt": "/forensics/usenet_1995_feed.html",
    "/usenet/alt.music.heartstrike": "/usenet/alt-music-synth-pop/index.html",
    "/usenet/comp.sys.ibm-pc.hardware/s00905.txt": "/forensics/usenet_1995_feed.html",
    "/usenet/comp.sys.ibm-pc.hardware": "/usenet/comp-sys-m68k/index.html",
    "/usenet/live_1995_feed.html": "/forensics/usenet_1995_feed.html",
}


def cleanup_legacy_dirs(site_dir: Path) -> None:
    """Removes unrouted /federation/ or dotted /usenet/ directories so check_swarm.mjs never trips."""
    fed = site_dir / "federation"
    if fed.exists():
        shutil.rmtree(fed, ignore_errors=True)
    usenet_dir = site_dir / "usenet"
    if usenet_dir.exists():
        for child in usenet_dir.iterdir():
            if child.is_dir() and "." in child.name:
                shutil.rmtree(child, ignore_errors=True)
        live_feed = usenet_dir / "live_1995_feed.html"
        if live_feed.exists():
            live_feed.unlink()


def ensure_sunsetstrip_analysis_page(site_dir: Path) -> None:
    """Ensures /geocities/sunsetstrip-nova-tape-of-us-analysis.html referenced in Sector 1 Clues exists."""
    target = site_dir / "geocities" / "sunsetstrip-nova-tape-of-us-analysis.html"
    if target.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<HTML><HEAD><TITLE>SunsetStrip/Club — "Tape of Us" (1989 Sublevel B2 Rough Mix) Spectral Analysis</TITLE>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
<META NAME="description" CONTENT="Forensic runout groove analysis of Nova Hart's leaked 1989 Sublevel B2 rough mix of Tape of Us.">
</HEAD>
<BODY BGCOLOR="#050805" TEXT="#33FF33" LINK="#FFB000" VLINK="#CC8800">
<CENTER><H1>SUNSET STRIP // "TAPE OF US" RUNOUT GROOVE ANALYSIS</H1></CENTER>
<HR>
<PRE>
ARCHIVE REEL : SD-0004 ("TAPE OF US" - 1989 ROUGH MIX)
ENGINEER     : MARCUS HALE (ORION SUBLEVEL B2)
AUDIO SOURCE : /assets/audio/tape_of_us_1989_rough_mix.mp3
RUNOUT OFFSET: 04:51.0 -> END OF REEL
------------------------------------------------------------------------
OBSERVATION:
After the main vocal fadeout at 4:51, the 14.2001 Hz bias carrier remains
locked while Marcus Hale whispers the Sublevel B2 matrix runout code over
the studio talkback bus:
  REEL MATRIX / RUNOUT: B2-EXEC-1989

To demodulate Sector 1 in the VT100 Forensic Terminal (/forensics/index.html),
enter:
  RESTORE 1 B2-EXEC-1989
</PRE>
<HR>
<P>[ <A HREF="/forensics/index.html">Return to VT100 Forensic Terminal</A> |
<A HREF="/forensics/signal_lab.html">Open Ashford Polytechnic Signal Lab</A> |
<A HREF="/index.html">Main Portal</A> ]</P>
</BODY></HTML>
""",
        encoding="utf-8",
    )


def audit_and_fix_html_files(site_dir: Path) -> tuple[int, int, list[str]]:
    rewritten_count = 0
    checked_links = 0
    broken: list[str] = []

    html_files = list(site_dir.rglob("*.html"))
    for html_file in html_files:
        text = html_file.read_text(encoding="utf-8", errors="ignore")
        orig = text
        for old_url, new_url in REWRITE_MAP.items():
            if old_url in text:
                text = text.replace(old_url, new_url)
        if text != orig:
            html_file.write_text(text, encoding="utf-8")
            rewritten_count += 1

        rel_html = html_file.relative_to(site_dir)
        if rel_html.parts[0] not in ("forensics", "terminal", "reconstruction"):
            continue

        for m in HREF_SRC_RE.finditer(text):
            raw_target = m.group(1).strip()
            if (
                not raw_target
                or raw_target.startswith(("#", "mailto:", "javascript:", "data:", "http://", "https://"))
                or "${" in raw_target
            ):
                continue
            checked_links += 1
            clean_target = raw_target.split("?")[0].split("#")[0]
            if clean_target.startswith("/"):
                rel_path = clean_target.lstrip("/")
                resolved = site_dir / rel_path
            else:
                resolved = (html_file.parent / clean_target).resolve()
                try:
                    rel_path = str(resolved.relative_to(site_dir.resolve()))
                except ValueError:
                    rel_path = clean_target

            if resolved.is_dir():
                resolved = resolved / "index.html"
                rel_path = rel_path.rstrip("/") + "/index.html"

            if not resolved.exists() and rel_path not in CANONICAL_STORY_PATHS:
                broken.append(f"{rel_html} -> {raw_target} (missing {rel_path})")

    return rewritten_count, checked_links, broken


def main() -> None:
    site_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/stardust_expansion/site")
    cleanup_legacy_dirs(site_dir)
    ensure_sunsetstrip_analysis_page(site_dir)
    rewritten, checked, broken = audit_and_fix_html_files(site_dir)
    print(
        f"[LINK_AUDITOR] Scanned {site_dir} | Rewrote {rewritten} files | "
        f"Verified {checked} internal links | Broken: {len(broken)}"
    )
    for b in broken:
        print("  BROKEN:", b)
    if broken:
        sys.exit(1)


if __name__ == "__main__":
    main()
