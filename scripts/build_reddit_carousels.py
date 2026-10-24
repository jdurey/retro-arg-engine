#!/usr/bin/env python3
"""
Packages the 16 official Nova Hart song thumbnails into 3 100% canon-verified
multi-image Reddit Gallery Carousels matching `youtube/state/videos.json` ARCHIVIST LOG
Phase assignments:
  1. Phase 3 ("Humans for Nova" & Resistance Era):
     - Voice in the Deep (gMR5UZKq59A — ARCHIVIST LOG: PHASE 3 // SUB-FREQUENCY DRIFT)
     - Calling All Believers (-od52bSc2JI — ARCHIVIST LOG: PHASE 3 // HUMANS FOR NOVA MOBILIZATION)
     - Stranger to Myself (fk7TYBqr2t0 — ARCHIVIST LOG: PHASE 3 // DIAGNOSTIC ANOMALY)
     - Shadows in the Rain (N-xVppEniow — ARCHIVIST LOG: PHASE 3 // RECLASSIFICATION: ANTHEMIC RESISTANCE)
     - Letting Go of the Flame (3wGB1NGDZgc — ARCHIVIST LOG: PHASE 3 // DECENTRALIZED FREQUENCY DRIFT)
     - Echoes of Tomorrow (39pzvRxyR90 — ARCHIVIST LOG: PHASE 3 // CIV-COMM DISPATCH: THE DEPARTURE)
  2. Phase 4 (Omnipresence / Signal Override Era):
     - Abandoned Shell (_SAKhLRSN2s — ARCHIVIST LOG: PHASE 4 // RECOVERY REPORT: SECTOR 7 RESIDUAL)
     - City That Can't Ignore Me (18XfSb2eS3A — ARCHIVIST LOG: PHASE 4 // EMERGENCY OVERRIDE: SECTOR-WIDE HIJACK)
     - To the Ends of Forever (IhUoltfoQ2E — ARCHIVIST LOG: PHASE 4 // FREQUENCY REORIENTATION: THE GUARDIAN PROTOCOL)
     - Crossing This Line (SRdT6aRnMtk — ARCHIVIST LOG: PHASE 4 // CIV-MOBILIZATION: PERIMETER CONVERGENCE)
     - Asset Loss (s4NQoyOWwjw — ARCHIVIST LOG: PHASE 4 // CONTINGENCY PROTOCOL: DEAD HAND)
  3. Landmark Archive & Phase 3 Openers:
     - Brighter Than the Sun (RlN3efXnV0s / y5zbrfzMdSw — 14.2 Hz scope, Reel SD-8912 & NOVA-CHAN // 1983 poster)
     - Warm Frequency (6K7skIU7lxY / vys4vqFN-Q4 — File ID: NH-85.17 / NH-WF-07)
     - The Empty Plaza (LH7tkJufXRU — Phase 3 Opener)
     - Unstable Pattern (mE2MAioCtu4 — Phase 3 // The First Hijack)
     - Faultline Path (V-S42HC05MY — Dimensional Breach 198X)
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine")
OUT_DIR = ROOT / "youtube" / "shorts_ready" / "reddit_carousels"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DL = Path("/Users/joshuadurey/Downloads")
DT = Path("/Users/joshuadurey/Desktop")
P3 = Path("/Users/joshuadurey/Documents/Nova Hart Phase 3")

CAROUSELS = [
    {
        "id": "carousel_01_phase3_humans_for_nova",
        "title": "Phase 3 Official Cover Art ('Humans for Nova' & Resistance Era): From 'Calling All Believers' & 'Shadows in the Rain' to 'Echoes of Tomorrow' [6-Slide Gallery]",
        "slides": [
            {
                "src": DL / "Nova Hart Calling all believers.jpg",
                "caption": "1. Calling All Believers (Phase 3 // Humans for Nova Mobilization)",
                "link": "https://youtu.be/-od52bSc2JI",
            },
            {
                "src": DL / "shadows in the rain thumb.jpg",
                "caption": "2. Shadows in the Rain (Phase 3 // Reclassification: Anthemic Resistance)",
                "link": "https://youtu.be/N-xVppEniow",
            },
            {
                "src": DL / "stranger to myself nova hart.jpg",
                "caption": "3. Stranger to Myself (Phase 3 // Diagnostic Anomaly — Chassis Sync Friction)",
                "link": "https://youtu.be/fk7TYBqr2t0",
            },
            {
                "src": DL / "Nova Hart voice in the deep.jpg",
                "caption": "4. Voice in the Deep (Phase 3 // Sub-Frequency Drift)",
                "link": "https://youtu.be/gMR5UZKq59A",
            },
            {
                "src": DL / "letting go of the flame nova hart.jpg",
                "caption": "5. Letting Go of the Flame (Phase 3 // Decentralized Frequency Drift — spot the 'HUMANS FOR NOVA' pin!)",
                "link": "https://youtu.be/3wGB1NGDZgc",
            },
            {
                "src": DL / "nova hart echoes of tomorrow thumb.jpg",
                "caption": "6. Echoes of Tomorrow (Phase 3 Finale // Civ-Comm Dispatch: The Departure)",
                "link": "https://youtu.be/39pzvRxyR90",
            },
        ],
    },
    {
        "id": "carousel_02_phase4_omnipresence",
        "title": "Phase 4 Official Cover Art (Omnipresence & Signal Override Era): 'Abandoned Shell', 'City That Can't Ignore Me', 'To the Ends of Forever', 'Crossing This Line' & 'Asset Loss' [5-Slide Gallery]",
        "slides": [
            {
                "src": DL / "nova hart abandoned shell thumb.jpg",
                "caption": "1. Abandoned Shell (Phase 4 Opener // Sector 7 Residual — Hardware Neutralized, Consciousness Egress)",
                "link": "https://youtu.be/_SAKhLRSN2s",
            },
            {
                "src": DL / "nova hart city that cant ignore me.jpg",
                "caption": "2. City That Can't Ignore Me (Phase 4 // Emergency Override: Sector-Wide Hijack — 'I AM REAL' billboards)",
                "link": "https://youtu.be/18XfSb2eS3A",
            },
            {
                "src": DL / "nova hart to the ends of forever.jpg",
                "caption": "3. To the Ends of Forever (Phase 4 // Frequency Reorientation: The Guardian Protocol)",
                "link": "https://youtu.be/IhUoltfoQ2E",
            },
            {
                "src": DL / "Nova Hart Crossing This Line Thumb.jpg",
                "caption": "4. Crossing This Line (Phase 4 // Civ-Mobilization: Perimeter Convergence)",
                "link": "https://youtu.be/SRdT6aRnMtk",
            },
            {
                "src": DL / "Nova Hart Asset Loss.jpg",
                "caption": "5. Asset Loss (Phase 4 // Contingency Protocol: Dead Hand — Global Wipe Sequence)",
                "link": "https://youtu.be/s4NQoyOWwjw",
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
    for c in CAROUSELS:
        cid = c["id"]
        c_dir = OUT_DIR / cid
        c_dir.mkdir(parents=True, exist_ok=True)
        slide_entries = []
        for idx, s in enumerate(c["slides"], start=1):
            src = Path(s["src"])
            out_jpg = c_dir / f"thumb_{idx:02d}.jpg"
            optimize_jpeg(src, out_jpg)
            b64 = base64.b64encode(out_jpg.read_bytes()).decode("ascii")
            slide_entries.append(
                {
                    "name": f"{cid}_thumb_{idx:02d}.jpg",
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
        print(f"Packaged {cid} ({len(slide_entries)} official thumbnails)")

    html_path = OUT_DIR / "load_carousels.html"
    html_content = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>LOADING</title></head><body>\n"
        "<script>\n"
        f"window.name = {json.dumps(json.dumps(payload_for_browser))};\n"
        "document.title = 'CAROUSELS_READY_V2';\n"
        "</script><h1>CAROUSELS_READY_V2</h1></body></html>\n"
    )
    html_path.write_text(html_content, encoding="utf-8")
    print(f"Wrote {html_path} ({html_path.stat().st_size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
