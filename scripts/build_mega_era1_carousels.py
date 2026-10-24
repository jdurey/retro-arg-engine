#!/usr/bin/env python3
"""
Packages the newly extracted Era 1 Mega Archive lore PDFs & 19 Bandcamp Album
Covers into 5 multi-image swipeable Reddit Gallery Carousels (`type=IMAGE`):
  1. Fanzine #2: Crystal Promise & Nova-chan (Dec. 1984, 8 slides)
  2. The Recovery Dossier: CRE-7 Performance Shell Technical Service Manual (Unit NH-04, 10 slides)
  3. Dream Machine '86 Tour Program Vol. 1 & Static & Steel (1988) CD Liner Notes (9 slides)
  4. Era 1 Official Album & EP Cover Art Archive — Part 1: Hard Rock & Arena Metal (10 slides)
  5. Era 1 Official Album & EP Cover Art Archive — Part 2: Synth-Rock, Ballads & The 'Heartstrike' Prototype Band (11 slides)
"""
from __future__ import annotations

import base64
import io
import json
from pathlib import Path
from PIL import Image

MEGA_DIR = Path("/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/shorts_ready/mega_era1_archive")
CAT_DIR = MEGA_DIR / "Nova Hart -The Complete Cataolg"
BC_DIR = CAT_DIR / "Bandcamp Albums"
BONUS_DIR = CAT_DIR / "Bonus Material"
PDF_PAGES = MEGA_DIR / "pdf_pages"

FANZINE2 = PDF_PAGES / "fanzine_2_crystal_promise_and_nova-"
DOSSIER = PDF_PAGES / "the_recovery_dossier_project_stardu"
DREAM86 = PDF_PAGES / "dream_machine_86_tour_program_vol._"
STATIC_CD = PDF_PAGES / "cd_cover_and_liner_notes"

GALLERIES = [
    {
        "id": "mega_01_fanzine2_crystal_promise_novachan",
        "title": "From the Vault: 'Crystal Promise & Nova-chan Fanzine #2' (December 1984) — How Orion Staged 'Live-Fidelity' Broadcasts with Hired Models [8-Slide Gallery]",
        "slides": [
            (FANZINE2 / "page-01.jpg", "1. Cover: Crystal Promise Fanzine #2 (Dec. 1984) — 'Promotional actors; not performers'"),
            (FANZINE2 / "page-02.jpg", "2. Recovered Asset Sheet (OR-CP-NC-001 — 'Studio-Only Project / Performance Simulation')"),
            (FANZINE2 / "page-03.jpg", "3. Editor's Letter: Why 1984 Feels Different (Cue Cards, Marks & Crowd Track)"),
            (FANZINE2 / "page-04.jpg", "4. 'The Shiny Mystery Behind the Suits!' — Alex, Marcello & Sofia ('The voice was never officially credited')"),
            (FANZINE2 / "page-05.jpg", "5. WorldNet BTS: 'Live-Fidelity' Secrets! (No tour buses — just lights, floor marks & scheduled crowd cheers)"),
            (FANZINE2 / "page-06.jpg", "6. Track Talk (1981–1984): 'Shining City', 'Every Window is a Promise', 'Everyone Together Now' & 'Voice of Three'"),
            (FANZINE2 / "page-08.jpg", "7. The Hinge Year (1983 → 1984): File Transfer CP-1983 → NC-1984"),
            (FANZINE2 / "page-12.jpg", "8. Back Cover: Orion Records / WorldNet Catalog Index (December 1984 — Price: 3 Harmony Credits)"),
        ],
    },
    {
        "id": "mega_02_recovery_dossier_cre7_manual",
        "title": "Declassified Orion Manual: 'CRE-7 Performance Shell Technical Service Manual — Subject: NH-04' (From The Recovery Dossier) [10-Slide Gallery]",
        "slides": [
            (DOSSIER / "page-02.jpg", "1. Orion CRE-7 Performance Shell | Technical Service Manual (Subject: NH-04 'Nova-chan')"),
            (DOSSIER / "page-04.jpg", "2. Section 1: System Overview (N.O.V.A Core → CRE-7 Performance Shell ← Harmony Stack)"),
            (DOSSIER / "page-06.jpg", "3. Section 1.2: Major Subsystems (Optical HUD, Vocal Assembly Driver, Affect Modulation & Cognitive Constraint Net)"),
            (DOSSIER / "page-08.jpg", "4. Section 3: Standard Operation (Orion Harmony System v2.7 — Latency: 13ms, Affect Target: Safe Euphoria)"),
            (DOSSIER / "page-10.jpg", "5. Section 4: Troubleshooting Guide ('Unexpected Output? → Unscripted Vocal / Technician Attachment → Flag Category Red')"),
            (DOSSIER / "page-12.jpg", "6. Technical Manual Page 105: Anomalous Behavior Analysis (4.1 Unscripted Vocal & 4.3 Technician Attachment circled)"),
            (DOSSIER / "page-15.jpg", "7. Section 6.2: Recall Procedure Summary (Stamped 'RECALLED')"),
            (DOSSIER / "page-17.jpg", "8. Section 5: Unauthorized Channels & Midnight Protocol ('DO NOT TRACE')"),
            (DOSSIER / "page-21.jpg", "9. Appendix A: Schematic Index (Android Unit Front/Rear, Facial Actuator Grid & Spinal Cable Bundle)"),
            (DOSSIER / "page-26.jpg", "10. Appendix B: Selected Log Excerpts (Diagnostic Session 7 — Tech: Hale_Marcus: 'Wait, [REDACTED] shows a spike in anomaly?')"),
        ],
    },
    {
        "id": "mega_03_dream_machine_86_and_static_steel_cd",
        "title": "1986 'Dream Machine Tour Vol. 1' Program & 1988 'Static & Steel' CD Booklet ('Lunar Colony Beta-7 / Custodian Tag C-12') [9-Slide Gallery]",
        "slides": [
            (DREAM86 / "page-01.jpg", "1. Nova Hart: The Dream Machine '86 Tour Vol. 1 Program Cover (Alliance World News / MBM Companion / Orion Records)"),
            (DREAM86 / "page-02.jpg", "2. Official 1986 Program Setlist ('Broadcast through Orion's Live-Fidelity System')"),
            (DREAM86 / "page-03.jpg", "3. 'A Message From Nova' (Recovered from Orion EM-12 'Empathy Script' packet // 1986)"),
            (DREAM86 / "page-04.jpg", "4. Your Concert Checklist ('Use MBM Companion Headphones — Share your moment on the Companion Hub')"),
            (DREAM86 / "page-05.jpg", "5. MBM Companion, Alliance World News & Orion Records ('Cultural Unity Division / Dream Machine Series 1986')"),
            (DREAM86 / "page-08.jpg", "6. Credits & Compliance ('Produced at Orion Stage 4, 1986')"),
            (STATIC_CD / "page-01.jpg", "7. Static & Steel (1988 CD Booklet Front Cover)"),
            (STATIC_CD / "page-02.jpg", "8. Broadcast Signal Log NH-88 ('QUERY:DEFINE(REAL) — THE ECHO IS REAL // RECALL DIRECTIVE 89 [CUSTODIAN TAG: C-12]')"),
            (STATIC_CD / "page-03.jpg", "9. Static & Steel (1988 CD Back Cover — Includes Bonus Track 13: 'Programmed for Love [Archival Demo]')"),
        ],
    },
    {
        "id": "mega_04_bandcamp_albums_part1_hardrock",
        "title": "The Complete Era 1 Album & EP Cover Art Archive (Part 1 — Hard Rock & Arena Metal): From 'Iron Claws EP' to 'Stadium Gods' & 'Recall Directive' [10-Slide Gallery]",
        "slides": [
            (BC_DIR / "Iron Claws EP/Iron Claws EP Covers/IRON CLAWS COVER.jpg", "1. Iron Claws EP (Official Front Cover)"),
            (BC_DIR / "Iron Claws EP/Iron Claws EP Covers/2.png", "2. Iron Claws EP (Alternate Cover Art #2)"),
            (BC_DIR / "Iron Claws EP/Iron Claws EP Covers/3.png", "3. Iron Claws EP (Alternate Cover Art #3)"),
            (BC_DIR / "Stadium Gods/stadium gods cover.png", "4. Stadium Gods (Full-Length Arena Rock Album Cover)"),
            (BC_DIR / "Signal in the Fire/hard rock cover.png", "5. Signal in the Fire (Hard Rock Album Cover)"),
            (BC_DIR / "Heatseeker Heart/heatseeker heart cover.png", "6. Heatseeker Heart (Album Cover)"),
            (BC_DIR / "Raw Voltage EP Masters/Raw Voltage EP Cover final.png", "7. Raw Voltage EP (Master Cover)"),
            (BC_DIR / "Recall Directive/metal ep cover.jpeg", "8. Recall Directive (Heavy Metal EP Cover)"),
            (BC_DIR / "Silk and Teeth/silk and teeth cover.png", "9. Silk and Teeth (Album Cover)"),
            (BC_DIR / "Dream Machine Tour Live vol. 1/album cover.png", "10. Dream Machine Tour Live Vol. 1 (1986 Live Album Cover)"),
        ],
    },
    {
        "id": "mega_05_bandcamp_albums_part2_synthrock_heartstrike",
        "title": "The Complete Era 1 Album & EP Cover Art Archive (Part 2 — Synth-Rock, Ballads & The 1986 'Heartstrike' Prototype Band) [11-Slide Gallery]",
        "slides": [
            (BC_DIR / "Midnight Protocol Album/Album Cover.png", "1. Midnight Protocol (Concept Album Cover)"),
            (BC_DIR / "Stardust EP/CP Album Cover.png", "2. Stardust EP / Crystal Promise & Nova-chan (Album Cover)"),
            (BC_DIR / "Arcade Juliet/arcade juliet cover.png", "3. Arcade Juliet (Album Cover)"),
            (BC_DIR / "Arcade Juliet/Community Signal Poster.jpeg", "4. Arcade Juliet — 'Community Signal Poster' Insert"),
            (BC_DIR / "Meet Me at the Arcade/arcade cover.jpg", "5. Meet Me at the Arcade (EP Cover)"),
            (BC_DIR / "Paper Keys - Ballads/paper keys cover.png", "6. Paper Keys — Ballads (Compilation Cover)"),
            (BC_DIR / "Through the Wires/through the wires cover.png", "7. Through the Wires (Album Cover)"),
            (BC_DIR / "Artificial Heart/artificial heart cover.png", "8. Artificial Heart (Album Cover)"),
            (BC_DIR / "Lip Service/lip service cover.png", "9. Lip Service (EP Cover)"),
            (BC_DIR / "Deep Cuts Vol 1 EP/deep cuts cover.png", "10. Deep Cuts Vol. 1 EP (Cover)"),
            (BONUS_DIR / "Nova Hart Protoype Band - 'Heartstrike'/Heartstrike Flyer 1986.png", "11. Bonus Vault Artifact: 1986 'Heartstrike' Club Flyer (The Prototype Band Behind 'To the End of Time' & 'No Turning Back')"),
        ],
    },
]


def encode_img(p: Path, fname: str) -> dict:
    if not p.exists() and "page-0" in p.name:
        p = p.with_name(p.name.replace("page-0", "page-"))
    im = Image.open(p).convert("RGB")
    # Cap max dimension at 1600px so 10-slide carousels load fast and crisp
    max_dim = 1600
    if max(im.size) > max_dim:
        ratio = max_dim / max(im.size)
        im = im.resize((int(im.size[0] * ratio), int(im.size[1] * ratio)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=85)
    return {
        "filename": fname,
        "b64": base64.b64encode(buf.getvalue()).decode("ascii"),
    }


def main() -> None:
    batches = [
        ("mega_batch1", GALLERIES[:3]),
        ("mega_batch2", GALLERIES[3:]),
    ]
    for bname, glist in batches:
        payload = []
        for g in glist:
            slides_out = []
            for idx, (src, cap) in enumerate(g["slides"], 1):
                fname = f"{g['id']}_s{idx:02d}.jpg"
                info = encode_img(src, fname)
                slides_out.append({
                    "filename": fname,
                    "caption": cap,
                    "b64": info["b64"],
                })
            payload.append({
                "id": g["id"],
                "title": g["title"],
                "slides": slides_out,
            })
        out_html = MEGA_DIR / f"load_{bname}.html"
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>LOADING</title></head>
<body><script>
window.name = JSON.stringify({json.dumps(payload)});
document.title = "READY_{bname.upper()}";
</script></body></html>"""
        out_html.write_text(html, encoding="utf-8")
        print(f"Wrote {out_html} ({out_html.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
