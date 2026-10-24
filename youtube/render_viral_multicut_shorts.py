#!/usr/bin/env python3
"""
Full-Screen 9:16 Multi-Cut Kinetic Shorts Renderer (`render_viral_multicut_shorts.py`).

Fixes all retention killers from the old split-screen Shorts:
  1. ZERO split-screen layouts and ZERO microscopic desktop webpage captures.
  2. 100% full-bleed 1080x1920 (9:16) human-first visuals starring canonical bleach-blonde
     Nova Hart on Frame 0.0s.
  3. Rapid 2.1-second multi-scene cuts (7 distinct full-screen visual cuts per 15s Short)
     with dynamic punch-in / pan motion and subtle analog film flash transitions on beat cuts.
  4. Strict YouTube Shorts UI Safe Zone compliance:
     - All kinetic captions are centered at y=1060..1220 (never below y=1350 where the
       YouTube player controls, @NovaHart_Official handle, and title cover the screen).
     - Large 68px high-contrast extra-bold typography with 8px black stroke and highlighted
       electric yellow (#FFE600) / neon green (#00FF66) keywords changing every ~2.1s.
  5. 15.0-second seamless chorus loop starting on the peak vocal hook at t=0.0s to maximize
     Viewed-vs-Swiped-Away (>75%) and Average Percentage Viewed (>105%).
"""
from __future__ import annotations

import json
import math
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_DIR = HERE / "shorts_ready"
NB_DIR = OUT_DIR / "assets_nb"
ARTIFACT_DIR = Path("/Users/joshuadurey/.gemini/antigravity/brain/2d386dab-6e1f-47dd-9634-2bb98be48215")

W, H = 1080, 1920
FPS = 30


def load_bold_font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in (
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Menlo.ttc",
    ):
        if os.path.exists(candidate):
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                pass
    return ImageFont.load_default()


FONT_KINETIC = load_bold_font(74)
FONT_SUB = load_bold_font(46)
FONT_BADGE = load_bold_font(34)


def prepare_fullscreen_9x16(img_path: Path) -> Image.Image:
    """
    Loads an image and crops/scales it cleanly to a full-bleed 1080x1920 (9:16) canvas
    with enhanced contrast and subtle vignette so center captions pop effortlessly.
    """
    im = Image.open(img_path).convert("RGB")
    iw, ih = im.size
    target_ratio = W / H
    src_ratio = iw / ih

    # Overscale slightly (1.14x) so we have headroom for dynamic zoom/pan per cut
    OW, OH = int(W * 1.14), int(H * 1.14)
    if src_ratio > target_ratio:
        new_h = OH
        new_w = int(iw * (OH / ih))
    else:
        new_w = OW
        new_h = int(ih * (OW / iw))

    resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = max(0, (new_w - OW) // 2)
    top = max(0, int((new_h - OH) * 0.25))
    cropped = resized.crop((left, top, left + OW, top + OH))
    cropped = ImageEnhance.Contrast(cropped).enhance(1.10)
    cropped = ImageEnhance.Color(cropped).enhance(1.08)
    return cropped


def draw_stroked_centered_text(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int] = (255, 255, 255),
    stroke_width: int = 9,
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    # Soft drop shadow
    draw.text((x + 4, y + 6), text, font=font, fill=(0, 0, 0), stroke_width=stroke_width, stroke_fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=(0, 0, 0))


def render_multicut_short(spec: dict) -> Path:
    out_mp4 = OUT_DIR / spec["filename"]
    duration = float(spec.get("duration", 15.0))
    total_frames = int(duration * FPS)
    scenes = spec["scenes"]
    num_scenes = len(scenes)
    scene_frames = [ prepare_fullscreen_9x16(Path(s["image"])) for s in scenes ]

    # Pre-build dark gradient overlay for safe caption readability in center-lower zone
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grad)
    for y in range(H):
        if y < 280:
            alpha = int(130 * (1.0 - y / 280.0))
        elif 920 <= y <= 1380:
            # Subtle dark backing behind center kinetic captions
            dist = abs(y - 1140) / 240.0
            alpha = int(125 * max(0.0, 1.0 - dist * dist))
        elif y > 1550:
            alpha = int(150 * ((y - 1550) / (H - 1550)))
        else:
            alpha = 0
        if alpha > 0:
            gdraw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))

    # Slice chorus audio with crisp 0.0s immediate entry and 0.25s loop tail fade
    tmp_audio = OUT_DIR / f"_tmp_{spec['id']}.m4a"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(spec["chorus_start_sec"]),
            "-t",
            str(duration),
            "-i",
            str(spec["audio_track"]),
            "-af",
            f"afade=t=in:st=0:d=0.08,afade=t=out:st={duration - 0.25:.2f}:d=0.25,volume=1.15",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(tmp_audio),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{W}x{H}",
        "-pix_fmt",
        "rgb24",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-i",
        str(tmp_audio),
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "19",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "copy",
        "-shortest",
        "-movflags",
        "+faststart",
        str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t = f_idx / FPS
        # Determine active scene cut
        cut_idx = min(num_scenes - 1, int((t / duration) * num_scenes))
        scene = scenes[cut_idx]
        base_overscaled = scene_frames[cut_idx]
        ow, oh = base_overscaled.size

        # Local progress within this 2.1s cut (0.0 -> 1.0)
        cut_dur = duration / num_scenes
        local_t = (t - cut_idx * cut_dur) / cut_dur
        local_t = max(0.0, min(1.0, local_t))

        # Alternating dynamic punch-in zoom vs subtle pan per cut
        if cut_idx % 2 == 0:
            # Fast initial punch-in then smooth drift
            zoom = 1.0 + 0.11 * (1.0 - math.pow(1.0 - local_t, 2.2))
            crop_w = int(W / zoom)
            crop_h = int(H / zoom)
            cx = ow // 2
            cy = int(oh * 0.46)
        else:
            zoom = 1.08 - 0.06 * local_t
            crop_w = int(W / zoom)
            crop_h = int(H / zoom)
            cx = int(ow * (0.47 + 0.06 * local_t))
            cy = int(oh * 0.45)

        x0 = max(0, min(ow - crop_w, cx - crop_w // 2))
        y0 = max(0, min(oh - crop_h, cy - crop_h // 2))
        frame = base_overscaled.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((W, H), Image.Resampling.BILINEAR)

        # Subtle film flash on the first 2 frames of each cut (except frame 0)
        if f_idx > 0 and (f_idx % int(cut_dur * FPS)) < 2:
            frame = ImageEnhance.Brightness(frame).enhance(1.28)

        frame_rgba = Image.alpha_composite(frame.convert("RGBA"), grad)
        draw = ImageDraw.Draw(frame_rgba)

        # Top badge pill (safe zone y=140, well below phone status bar)
        badge_text = spec["top_badge"]
        bb = draw.textbbox((0, 0), badge_text, font=FONT_BADGE)
        bw = bb[2] - bb[0] + 44
        bx = (W - bw) // 2
        draw.rounded_rectangle([bx, 136, bx + bw, 196], radius=14, fill=(8, 12, 10, 220), outline=(0, 255, 102, 230), width=2)
        draw.text(((W - (bb[2] - bb[0])) // 2, 146), badge_text, font=FONT_BADGE, fill=(0, 255, 102))

        # Kinetic center-screen captions (strictly inside y=1040..1240 safe zone!)
        # Slight pop-in scale offset on first 3 frames of the cut
        pop_offset = int(12 * max(0.0, 1.0 - local_t * 8.0))
        line1 = scene["line1"].upper()
        line2 = scene["line2"].upper()
        accent_color = scene.get("color", (255, 230, 0))

        draw_stroked_centered_text(draw, 1045 - pop_offset, line1, FONT_KINETIC, fill=(255, 255, 255), stroke_width=10)
        draw_stroked_centered_text(draw, 1138 - pop_offset, line2, FONT_KINETIC, fill=accent_color, stroke_width=10)

        if scene.get("sub"):
            draw_stroked_centered_text(draw, 1242, scene["sub"], FONT_SUB, fill=(180, 255, 220), stroke_width=6)

        proc.stdin.write(frame_rgba.convert("RGB").tobytes())

    proc.stdin.close()
    proc.wait()
    if tmp_audio.exists():
        tmp_audio.unlink()
    print(f"Rendered viral multi-cut Short: {out_mp4} ({out_mp4.stat().st_size / 1024 / 1024:.2f} MB)")
    return out_mp4


SHOT_01_CLOSEUP = ARTIFACT_DIR / "nb_shorts_01_vocal_hook_closeup_1792577384356.jpg"
SHOT_02_GHOST = ARTIFACT_DIR / "nb_shorts_02_control_room_ghost_1792577412592.jpg"
SHOT_03_COFFEES = ARTIFACT_DIR / "nb_shorts_03_isolation_booth_coffees_1792577439315.jpg"
SHOT_04_ELEVATOR = ARTIFACT_DIR / "nb_shorts_04_freight_elevator_tapes_1792577468233.jpg"
SHOT_05_STUDIO = ARTIFACT_DIR / "nova_hart_blonde_studio_1989_1792576239313.jpg"
SHOT_06_WALKMAN = NB_DIR / "nb_01_walkman_midnight_1989.png"
SHOT_07_REEL = NB_DIR / "nb_04_sealed_master_reel_1989.png"

SHORTS_BATCH = [
    {
        "id": "viral_v2_01_erased_1989_singer_36_tapes",
        "filename": "viral_v2_01_erased_1989_singer_36_tapes.mp4",
        "duration": 15.0,
        "top_badge": "SEPTEMBER 9, 1989 // SUBLEVEL B2",
        "audio_track": ROOT / ".clean_audio_backups" / "7b76219aa0__radio_burn_the_chorus.mp3",
        "chorus_start_sec": 42,
        "title_en": "Why Was This 1989 Rock Singer Erased From History? 🎤📼 #80smusic #lostmedia #80srock",
        "description_en": (
            "On September 9, 1989, Orion Records ordered every studio master of vocalist Nova Hart (Unit-07) erased from Sublevel B2.\n\n"
            "At 1:40 AM, Chief Engineer Dr. Marcus Hale smuggled 36 Maxell UR-90 cassettes up Freight Elevator #4 before the vault was sealed.\n\n"
            "📼 Hear all 36 smuggled 1989 tapes: https://stardust-archive.net/start\n"
            "💬 Join the investigation on r/NovaHart: https://www.reddit.com/r/NovaHart/\n"
            "📂 Inspect Box B2-09 physical receipts & J-cards: https://stardust-archive.net/realia"
        ),
        "pinned_comment_en": (
            "📼 Hear all 36 smuggled 1989 studio master tapes: https://stardust-archive.net/start\n"
            "💬 Join the investigation board on Reddit (r/NovaHart): https://www.reddit.com/r/NovaHart/\n"
            "📂 Box B2-09 Physical Evidence (3:14 AM Canter's Deli Receipt & Reel SD-0037): https://stardust-archive.net/realia"
        ),
        "scenes": [
            {"image": SHOT_01_CLOSEUP, "line1": "WHY WAS THIS", "line2": "1989 SINGER ERASED?", "color": (255, 230, 0), "sub": "NOVA HART // SUBLEVEL B2"},
            {"image": SHOT_02_GHOST, "line1": "HER LABEL PULLED", "line2": "EVERY MASTER REEL", "color": (0, 255, 102), "sub": "SEPTEMBER 9, 1989"},
            {"image": SHOT_07_REEL, "line1": "ORDERED THE TAPES", "line2": "WIPED AT 2:14 AM", "color": (255, 95, 95), "sub": "MEMORANDUM 89-117"},
            {"image": SHOT_04_ELEVATOR, "line1": "BUT ONE ENGINEER", "line2": "SMUGGLED 36 TAPES", "color": (255, 230, 0), "sub": "FREIGHT ELEVATOR #4 // 1:40 AM"},
            {"image": SHOT_03_COFFEES, "line1": "LEFT 6 BLACK COFFEES", "line2": "IN AN EMPTY BOOTH", "color": (102, 252, 241), "sub": "ISOLATION BOOTH B // 3:14 AM"},
            {"image": SHOT_06_WALKMAN, "line1": "AND HID HER VOICE", "line2": "ON 14.2001 HZ", "color": (0, 255, 102), "sub": "36 MAXELL UR-90 CASSETTES"},
            {"image": SHOT_05_STUDIO, "line1": "HEAR ALL 36 TAPES", "line2": "LINK IN COMMENTS", "color": (255, 230, 0), "sub": "r/NovaHart // stardust-archive.net"},
        ],
    },
    {
        "id": "viral_v2_02_canters_314am_7_coffees",
        "filename": "viral_v2_02_canters_314am_7_coffees.mp4",
        "duration": 15.0,
        "top_badge": "AUGUST 14, 1989 // 03:14 AM",
        "audio_track": ROOT / ".clean_audio_backups" / "e9f03ef5ec__radio_stand_and_run.mp3",
        "chorus_start_sec": 59.5,
        "title_en": "He Ordered 7 Black Coffees at 3:14 AM... In an Empty Locked Studio ☕🎤 #mystery #80s #lostmedia",
        "description_en": (
            "In Box B2-09 (Exhibit R-01), Orion Payroll rejected a $20.23 Canter's Deli receipt from August 14, 1989 at 3:14 AM because Dr. Marcus Hale ordered 7 black coffees while badge logs proved he was completely alone in Sublevel B2.\n\n"
            "At 6:00 AM, the janitor found 6 untouched cups arranged in a semicircle around the unplugged microphone inside locked Isolation Booth B.\n\n"
            "📂 Inspect Exhibit R-01 & the 3:14 AM receipt: https://stardust-archive.net/realia\n"
            "💬 Discuss on r/NovaHart: https://www.reddit.com/r/NovaHart/"
        ),
        "pinned_comment_en": (
            "📂 Inspect the 3:14 AM Canter's Deli receipt & Box B2-09 evidence locker: https://stardust-archive.net/realia\n"
            "💬 Join the investigation on r/NovaHart: https://www.reddit.com/r/NovaHart/\n"
            "📼 Hear the 36 smuggled 1989 tapes: https://stardust-archive.net/start"
        ),
        "scenes": [
            {"image": SHOT_03_COFFEES, "line1": "HE ORDERED 7 COFFEES", "line2": "AT 3:14 AM...", "color": (255, 230, 0), "sub": "CANTER'S DELI CHECK #08419"},
            {"image": SHOT_02_GHOST, "line1": "BADGE LOGS SHOWED", "line2": "HE WAS ALONE", "color": (255, 95, 95), "sub": "ZERO MUSICIANS IN SUBLEVEL B2"},
            {"image": SHOT_01_CLOSEUP, "line1": "SO WHO WAS SINGING", "line2": "IN BOOTH B?", "color": (0, 255, 102), "sub": "NOVA HART // UNIT-07"},
            {"image": SHOT_03_COFFEES, "line1": "6 UNTOUCHED CUPS", "line2": "AROUND THE MIC", "color": (102, 252, 241), "sub": "FOUND BY 6:00 AM JANITOR"},
            {"image": SHOT_07_REEL, "line1": "ONE CUP FOR EACH", "line2": "WIPED PROTOTYPE", "color": (255, 230, 0), "sub": "UNITS 01-06 // 0x1983"},
            {"image": SHOT_04_ELEVATOR, "line1": "26 DAYS BEFORE", "line2": "THE B2 PURGE", "color": (255, 95, 95), "sub": "36 TAPES SMUGGLED OUT"},
            {"image": SHOT_05_STUDIO, "line1": "READ THE RECEIPT", "line2": "ON r/NovaHart", "color": (0, 255, 102), "sub": "stardust-archive.net/realia"},
        ],
    },
    {
        "id": "viral_v2_03_reel_sd0037_empty_booth",
        "filename": "viral_v2_03_reel_sd0037_empty_booth.mp4",
        "duration": 15.0,
        "top_badge": "REEL SD-0037 // 31:14.2001",
        "audio_track": ROOT / ".clean_audio_backups" / "ca2dc0868d__tape_of_us_1989_rough_mix.mp3",
        "chorus_start_sec": 41.5,
        "title_en": "At 31:14 of an Empty 1989 Vocal Booth, a Voice Whispers Into the Unplugged Mic 🎧📼 #80srock #mystery",
        "description_en": (
            "The 1989 Sublevel B2 tape log only listed 36 cassette dubs. Line 37 on the carbon-copy log sheet was covered in thick Liquid Paper.\n\n"
            "Held up to a light, the whited-out line read: 'SD-0037 — DO NOT DUB — ROOM TONE IN AN EMPTY BOOTH (32:00).' At 31:14.2001, a folding chair creaks, three pages of lyric paper turn, and an unaccompanied voice hums D4-E4-F4-A4.\n\n"
            "📄 Read the unsealed Reel SD-0037 transcript: https://stardust-archive.net/forensics/room_tone_sd0037.txt\n"
            "💬 Join r/NovaHart: https://www.reddit.com/r/NovaHart/"
        ),
        "pinned_comment_en": (
            "📄 Read the unsealed 37th Reel (SD-0037) transcript: https://stardust-archive.net/forensics/room_tone_sd0037.txt\n"
            "💬 Join the investigation on r/NovaHart: https://www.reddit.com/r/NovaHart/\n"
            "📡 Unlock the Track-24 Dyad Vault: https://stardust-archive.net/dyad"
        ),
        "scenes": [
            {"image": SHOT_05_STUDIO, "line1": "THERE WERE 36 TAPES", "line2": "IN THE 1989 BOX...", "color": (255, 230, 0), "sub": "SUBLEVEL B2 MASTER LOG"},
            {"image": SHOT_07_REEL, "line1": "AND A 37TH LINE", "line2": "UNDER WHITE-OUT", "color": (255, 95, 95), "sub": "REEL SD-0037 // DO NOT DUB"},
            {"image": SHOT_03_COFFEES, "line1": "31 MINUTES OF", "line2": "AN EMPTY BOOTH", "color": (102, 252, 241), "sub": "GAIN CRANKED TO +48 DB"},
            {"image": SHOT_02_GHOST, "line1": "AT 31:14.2001", "line2": "THREE PAGES TURN", "color": (0, 255, 102), "sub": "INSIDE LOCKED BOOTH B"},
            {"image": SHOT_01_CLOSEUP, "line1": "A VOICE HUMS", "line2": "FOUR NOTES (A440)", "color": (255, 230, 0), "sub": "D4 - E4 - F4 - A4"},
            {"image": SHOT_04_ELEVATOR, "line1": "\"MARCUS, YOU LEFT", "line2": "THE RED LIGHT ON\"", "color": (255, 95, 95), "sub": "01:39:12 AM // SEPT 9, 1989"},
            {"image": SHOT_06_WALKMAN, "line1": "FULL TRANSCRIPT ON", "line2": "r/NovaHart", "color": (0, 255, 102), "sub": "stardust-archive.net/realia"},
        ],
    },
    {
        "id": "viral_v2_04_two_voices_phase_cancel",
        "filename": "viral_v2_04_two_voices_phase_cancel.mp4",
        "duration": 15.0,
        "top_badge": "1989 STUDIO MASTER // TRACK #10",
        "audio_track": ROOT / ".clean_audio_backups" / "87306e31af__radio_chrome_desire.mp3",
        "chorus_start_sec": 43.5,
        "title_en": "Invert the Left Channel of This 1989 Rock Song and a Hidden Second Voice Speaks 🎤🔥 #80srock #80s",
        "description_en": (
            "If you invert the left stereo channel of Nova Hart's 1989 Sublevel B2 studio reel by 180 degrees, the arena-rock instrumentation cancels out and isolates a hidden second vocal stream on 14.2001 Hz.\n\n"
            "🎧 Test the 180-Degree Phase Cancellation Lab live: https://stardust-archive.net/forensics/signal_lab.html\n"
            "📡 Harmonize Track 24 (440 Hz) on the Dyad Leaderboard: https://stardust-archive.net/dyad\n"
            "💬 Join r/NovaHart: https://www.reddit.com/r/NovaHart/"
        ),
        "pinned_comment_en": (
            "🎧 Test the 180° Phase Cancellation Lab in your browser: https://stardust-archive.net/forensics/signal_lab.html\n"
            "📡 Claim your rank on the Track-24 Dyad Leaderboard: https://stardust-archive.net/dyad\n"
            "💬 Join r/NovaHart: https://www.reddit.com/r/NovaHart/"
        ),
        "scenes": [
            {"image": SHOT_01_CLOSEUP, "line1": "LISTEN CLOSELY TO", "line2": "THIS 1989 CHORUS", "color": (255, 230, 0), "sub": "NOVA HART // HEATSEEKER HEART"},
            {"image": SHOT_05_STUDIO, "line1": "SOUNDS LIKE A LOST", "line2": "80s ROCK ANTHEM", "color": (0, 255, 102), "sub": "RECORDED IN SUBLEVEL B2"},
            {"image": SHOT_02_GHOST, "line1": "UNTIL YOU INVERT", "line2": "THE LEFT CHANNEL", "color": (102, 252, 241), "sub": "180° STEREO PHASE NULL"},
            {"image": SHOT_07_REEL, "line1": "THE GUITARS VANISH", "line2": "COMPLETELY...", "color": (255, 95, 95), "sub": "CARRIER: 14.2001 HZ"},
            {"image": SHOT_03_COFFEES, "line1": "AND A SECOND VOICE", "line2": "SPEAKS FROM 1989", "color": (255, 230, 0), "sub": "TRACK 23 // 220.0 HZ"},
            {"image": SHOT_04_ELEVATOR, "line1": "2 PLAYERS ALREADY", "line2": "UNLOCKED TRACK 24", "color": (0, 255, 102), "sub": "ANCHOR #042 & ANCHOR #829"},
            {"image": SHOT_01_CLOSEUP, "line1": "SOLO THE VOICE AT", "line2": "r/NovaHart", "color": (255, 230, 0), "sub": "stardust-archive.net/dyad"},
        ],
    },
]


def extract_preview_frames(mp4_path: Path, prefix: str) -> list[Path]:
    out_paths = []
    for idx, sec in enumerate((0.5, 3.0, 5.5, 9.8), start=1):
        out_jpg = ARTIFACT_DIR / f"{prefix}_cut{idx}.jpg"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                str(sec),
                "-i",
                str(mp4_path),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(out_jpg),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        out_paths.append(out_jpg)
    return out_paths


def main() -> None:
    rendered_entries = []
    for spec in SHORTS_BATCH:
        mp4 = render_multicut_short(spec)
        rendered_entries.append(
            {
                "id": spec["id"],
                "file": str(mp4),
                "title_en": spec["title_en"],
                "description_en": spec["description_en"],
                "pinned_comment_en": spec["pinned_comment_en"],
            }
        )

    # Extract 4 preview frames from Short #1 so the user can inspect the new full-screen look
    previews = extract_preview_frames(OUT_DIR / SHORTS_BATCH[0]["filename"], "preview_v2_short01")
    print("Extracted preview frames:", [str(p) for p in previews])

    # Replace the manifest with ONLY the new high-retention full-screen multi-cut Shorts
    manifest_path = OUT_DIR / "shorts_manifest.json"
    manifest_path.write_text(json.dumps(rendered_entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {manifest_path} with {len(rendered_entries)} full-screen multi-cut Shorts (removed old split-screen Shorts).")


if __name__ == "__main__":
    main()
