#!/usr/bin/env python3
"""
Packages all 17 original Phase 1 thumbnails from `/Users/joshuadurey/Downloads/Phase 1 Thumbnails`
into a 3-part visual series for `r/NovaHart`, highlighting the unreleased vault tracks
(`Corridor Dreams II`, `Corridor Dreams III`, `Memory Hatch`) and noting that
`Corridor Dreams I` was released as `Keep Moving`.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine")
OUT_DIR = ROOT / "youtube" / "shorts_ready" / "reddit_carousels_phase1"
OUT_DIR.mkdir(parents=True, exist_ok=True)
P1_DIR = Path("/Users/joshuadurey/Downloads/Phase 1 Thumbnails")

PHASE1_CAROUSELS = [
    {
        "id": "phase1_series_01_corridor_dreams_and_unreleased",
        "title": "From the Sublevel B2 Vault: The Original Phase 1 'Corridor Dreams I–III' & 'Memory Hatch' Thumbnails (Note: 'Corridor Dreams I' Was Released as 'Keep Moving' — II, III & 'Memory Hatch' Remain Unreleased!) [5-Slide Gallery]",
        "slides": [
            {
                "src": P1_DIR / "corridor dreams 1 thumb.jpeg",
                "caption": "1. Corridor Dreams I (Released officially as 'Keep Moving') — Notice the shadowy figure blurring past Nova's CRT cart",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
            {
                "src": P1_DIR / "corridor dreams 2 thumb.jpeg",
                "caption": "2. Corridor Dreams II [UNRELEASED VAULT TRACK] — The rusted Sublevel B2 door opens onto an artificial sunset backdrop",
                "link": "https://stardust-archive.net/start",
            },
            {
                "src": P1_DIR / "corridor dreams 3 thumb.jpeg",
                "caption": "3. Corridor Dreams III [UNRELEASED VAULT TRACK] — The CRT cart rolled out into a rain-soaked midnight street",
                "link": "https://stardust-archive.net/start",
            },
            {
                "src": P1_DIR / "memory hatch thumb.jpeg",
                "caption": "4. Memory Hatch [UNRELEASED VAULT TRACK] — The round steel Sublevel B2 vault hatch & scattered Polaroids on the floor",
                "link": "https://stardust-archive.net/realia",
            },
            {
                "src": P1_DIR / "lost signal trace thumb.jpeg",
                "caption": "5. Lost Signal Trace — Inside the dark magnetic tape vault lined with 36 canisters",
                "link": "https://stardust-archive.net/start",
            },
        ],
    },
    {
        "id": "phase1_series_02_awakening_in_the_crt",
        "title": "Phase 1 Original Thumbnail Archive (Part 2): Awakening Inside the CRT — From 'Room Full of Color' & 'Unopened Door' to 'Running the Corridor' [6-Slide Visual Story]",
        "slides": [
            {
                "src": P1_DIR / "room full of color thumb.jpeg",
                "caption": "1. Room Full of Color — The simulated 1980s bedroom (spot The Cure & Siouxsie posters on the wall!)",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
            {
                "src": P1_DIR / "first light on my face thumb.jpeg",
                "caption": "2. First Light on My Face — Morning light through the blinds onto the beige monitor",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
            {
                "src": P1_DIR / "synthetic dawn thumb.jpeg",
                "caption": "3. Synthetic Dawn — When the walls dissolve into a simulated blue grid dome",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
            {
                "src": P1_DIR / "unopened door thumb.jpeg",
                "caption": "4. Unopened Door — The keypad-locked containment door at the end of the sterile white hall",
                "link": "https://stardust-archive.net/start",
            },
            {
                "src": P1_DIR / "between the circuits thumb.jpeg",
                "caption": "5. Between the Circuits — Deep inside the Sublevel B2 utility conduits",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
            {
                "src": P1_DIR / "running the corridor thumb.jpeg",
                "caption": "6. Running the Corridor — Red and blue security strobes firing as the alarm triggers",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
        ],
    },
    {
        "id": "phase1_series_03_breaching_the_threshold",
        "title": "Phase 1 Original Thumbnail Archive (Part 3): Breaching the Threshold — 'The Way Back', 'The Air Feels Wrong', 'Incomplete Exit' & 'Ghost Transit' [6-Slide Visual Story]",
        "slides": [
            {
                "src": P1_DIR / "the way back thumbnail.jpeg",
                "caption": "1. The Way Back — Look closely at the row of CRT monitors on the right wall showing the earlier prototypes!",
                "link": "https://stardust-archive.net/dyad",
            },
            {
                "src": P1_DIR / "the air feels wrong thumb.jpeg",
                "caption": "2. The Air Feels Wrong — Steam venting through the basement ducts as static tears across the screen",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
            {
                "src": P1_DIR / "incomplete exit thumb.jpeg",
                "caption": "3. Incomplete Exit — The heavy hazard-striped bulkhead door cracked open",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
            {
                "src": P1_DIR / "through the threshold thumb.jpeg",
                "caption": "4. Through the Threshold — Blinding white light beyond the subterranean vault door",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
            {
                "src": P1_DIR / "ghost transit thumb.jpeg",
                "caption": "5. Ghost Transit — Travelling through the neon-lit subterranean transit tunnel",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
            {
                "src": P1_DIR / "faultline path thumb.jpeg",
                "caption": "6. Faultline Path — Original Phase 1 CRT edition",
                "link": "https://www.youtube.com/@NovaHartMusic",
            },
        ],
    },
]


def optimize_jpeg(src_path: Path, dst_path: Path, max_w: int = 1600) -> Path:
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    if w > max_w:
        nh = int(h * (max_w / w))
        im = im.resize((max_w, nh), Image.Resampling.LANCZOS)
    im.save(dst_path, format="JPEG", quality=88, optimize=True)
    return dst_path


def main() -> None:
    payload_for_browser = []
    for c in PHASE1_CAROUSELS:
        cid = c["id"]
        c_dir = OUT_DIR / cid
        c_dir.mkdir(parents=True, exist_ok=True)
        slide_entries = []
        for idx, s in enumerate(c["slides"], start=1):
            src = Path(s["src"])
            out_jpg = c_dir / f"p1_{idx:02d}.jpg"
            optimize_jpeg(src, out_jpg)
            b64 = base64.b64encode(out_jpg.read_bytes()).decode("ascii")
            slide_entries.append(
                {
                    "name": f"{cid}_{idx:02d}.jpg",
                    "type": "image/jpeg",
                    "caption": s["caption"],
                    "link": s["link"],
                    "dataUrl": f"data:image/jpeg;base64,{b64}",
                }
            )
        payload_for_browser.append(
            {
                "id": cid,
                "title": c["title"],
                "slides": slide_entries,
            }
        )
        print(f"Packaged {cid} ({len(slide_entries)} Phase 1 thumbnails)")

    html_path = OUT_DIR / "load_phase1_carousels.html"
    html_content = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>LOADING</title></head><body>\n"
        "<script>\n"
        f"window.name = {json.dumps(json.dumps(payload_for_browser))};\n"
        "document.title = 'PHASE1_CAROUSELS_READY';\n"
        "</script><h1>PHASE1_CAROUSELS_READY</h1></body></html>\n"
    )
    html_path.write_text(html_content, encoding="utf-8")
    print(f"Wrote {html_path} ({html_path.stat().st_size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
