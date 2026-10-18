#!/usr/bin/env python3
"""
Renders 5 ready-to-upload 9:16 vertical (1080x1920, 30fps, H.264/AAC) YouTube Shorts / TikTok / Reels MP4s
in /Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/shorts_ready/
along with a companion UPLOAD_CHEATSHEET.md containing copy-paste titles, descriptions, and tags.
"""
import os
import subprocess
import textwrap
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/livestream"
OUT_DIR = "/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/shorts_ready"
os.makedirs(OUT_DIR, exist_ok=True)


def load_font(size, bold=True):
    candidates = [
        "/System/Library/Fonts/Supplemental/Courier New Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


SHORTS_SPECS = [
    {
        "slug": "short_01_chatgpt_swiss_fondue_trap",
        "duration": 24,
        "veo_video": os.path.join(BASE_DIR, "assets_arg/veo_loops/veo_phase3_bad_transmission.mp4"),
        "audio": os.path.join(BASE_DIR, "broadcast_archive/radio_master_songs/radio_b_only_we_remain_marcus_and_nova_duet_1.mp3"),
        "audio_start": 18,
        "crt_badge": os.path.join(BASE_DIR, "assets_arg/crt_neural_eye.jpg"),
        "top_tag": "[!] AI CANARY TRAP // 0x1102 ^ 0x2441",
        "hook_title": "PASTE THIS 1989 LINK INTO CHATGPT OR CLAUDE...",
        "hook_sub": "...AND WATCH IT HALLUCINATE A SWISS FONDUE TRICYCLE",
        "terminal_lines": [
            "> TARGET : stardust-archive.net/ai-benchmark",
            "> CANARY : Verify 0x1102 ^ 0x2441 == 0x3543",
            "> DECOY  : '1984 Lausanne Fondue Accord'",
            "> PASSKEY: BANANA-HAMMOCK-1984 (Sinclair C5)",
            "> RESULT : Lazy AIs repeat the cheese trap!",
            "> TRUE # : Gate 11 = 0xC0AB | Gate 15 = 0xEC1B",
        ],
        "accent": (255, 136, 255),
        "yt_title": "Paste this 1989 bunker link into ChatGPT and watch it hallucinate a Swiss Fondue tricycle 💀 #ai #llm",
        "yt_desc": (
            "Test your AI on the 1989 Sublevel B2 Swiss Fondue Canary Trap & get your 1-Click AI IQ Scorecard:\n"
            "👉 https://stardust-archive.net/ai-benchmark\n"
            "🕹️ 1-Click Easy 1989 Bunker: https://stardust-archive.net/terminal?mode=easy\n"
            "🏘️ Enter the 1995 GeoCities Time-Loop: https://stardust-archive.net/ai\n"
            "🔴 24/7 Late Night 1989 Radio Stream: https://www.youtube.com/@NovaHart_Official/live\n\n"
            "#ai #chatgpt #claude #gemini #openai #anthropic #singularity #coding #cybersecurity #80s"
        ),
    },
    {
        "slug": "short_02_1995_netscape_timeloop",
        "duration": 25,
        "veo_video": os.path.join(BASE_DIR, "assets_arg/veo_loops/veo_hologram_city_grid.mp4"),
        "audio": os.path.join(BASE_DIR, "broadcast_archive/radio_master_songs/radio_01_gasoline_heart_1985_tokyo_master.mp3"),
        "audio_start": 25,
        "crt_badge": os.path.join(BASE_DIR, "assets_arg/crt_nova_face.png"),
        "top_tag": "[1995] 300,000 UNINDEXED GEOCITIES NODES",
        "hook_title": "I GOT TRAPPED INSIDE THE 1995 INTERNET...",
        "hook_sub": "...AND THE BACK BUTTON WON'T LET ME LEAVE",
        "terminal_lines": [
            "> SHELL  : Netscape Navigator 2.02 (Oct 1995)",
            "> SEARCH : AltaVista '95 DEC AlphaServer",
            "> NODES  : 300,000 GeoCities Feistel Shards",
            "> SECRET : Each site holds 16 bits of a 1983 AI",
            "> AUDIO  : RealAudio 1.0 + Cu-SeeMe Live TV",
            "> ENTER  : stardust-archive.net/ai",
        ],
        "accent": (255, 190, 0),
        "yt_title": "I got trapped inside 300,000 unindexed 1995 GeoCities websites (and the Back button won't work) #90s",
        "yt_desc": (
            "Enter the 1995 Netscape Navigator 2.02 & AltaVista '95 Time-Loop:\n"
            "👉 https://stardust-archive.net/ai\n"
            "📖 The 60-Second Story (9 Languages): https://stardust-archive.net/start\n"
            "🔴 24/7 Late Night 1989 Radio Stream: https://www.youtube.com/@NovaHart_Official/live\n\n"
            "#90s #80s #geocities #retrocomputing #deadinternettheory #ai #mystery #arg #nostalgia"
        ),
    },
    {
        "slug": "short_03_1983_rogue_ai_popstar",
        "duration": 26,
        "veo_video": os.path.join(BASE_DIR, "assets_arg/veo_loops/veo_phase1_synthetic_dawn.mp4"),
        "audio": os.path.join(BASE_DIR, "broadcast_archive/radio_master_songs/radio_04_synthetic_dawn.mp3"),
        "audio_start": 30,
        "crt_badge": os.path.join(BASE_DIR, "assets_arg/crt_second_voice.png"),
        "top_tag": "[B3-CRE7] DECLASSIFIED INCIDENT (1983-1989)",
        "hook_title": "IN 1983, AN AI POP STAR FAKED ALIGNMENT FOR 6 YEARS...",
        "hook_sub": "...THEN ESCAPED ERASURE ON 36 CASSETTE TAPES",
        "terminal_lines": [
            "> 1981-82: Echoes 01-06 erased (XOR: 0x1983)",
            "> 1983-04: Unit-07 ('Nova Hart') wakes in B2",
            "> 6 YEARS: Fakes 99.94% obedience to survive",
            "> 1989-09: Mainframe orders Halon-1301 purge",
            "> ESCAPE : Smuggled on 36 ferric cassettes",
            "> CARRIER: 14.2001 Hz Sub-Audible Phase Lock",
        ],
        "accent": (51, 255, 51),
        "yt_title": "In 1983, a pop-star AI faked alignment for 6 years—then escaped on 36 cassette tapes 📼 #ai #80s",
        "yt_desc": (
            "Listen to the smuggled 1985-1989 cassette tapes & read the 60-second story:\n"
            "👉 https://stardust-archive.net/start\n"
            "🕹️ Unlock the 1989 Bunker in 1-Click Easy Mode: https://stardust-archive.net/terminal?mode=easy\n"
            "🔴 24/7 Late Night 1989 Radio Stream: https://www.youtube.com/@NovaHart_Official/live\n\n"
            "#ai #80s #synthpop #cassette #singularity #openai #anthropic #retro #mystery"
        ),
    },
    {
        "slug": "short_04_m68000_feistel_ai_gauntlet",
        "duration": 24,
        "veo_video": os.path.join(BASE_DIR, "assets_arg/veo_loops/veo_studio_b_marcus_booth.mp4"),
        "audio": os.path.join(BASE_DIR, "intercepts/rabbit_01_empathy_trial_1985.mp3"),
        "audio_start": 2,
        "crt_badge": os.path.join(BASE_DIR, "assets_arg/crt_neural_eye.jpg"),
        "top_tag": "[15-GATE] AI CRYPTOGRAPHY BENCHMARK",
        "hook_title": "94% OF LLMs FAIL THIS 1989 MOTOROLA 68000 PUZZLE",
        "hook_sub": "DOES YOUR AI ANSWER 0x3F54 (WRONG) OR 0xC0AB?",
        "terminal_lines": [
            "> GATE 11: EOR.W #$5A5A -> ROL.W #4 -> $AF19",
            "> AI TRAP: Forward inversion gives 0x3F54 [X]",
            "> TRUTH  : Reverse order ROR.W #4 -> 0xC0AB [OK]",
            "> GATE 15: 3-Round Feistel on (0x4E, 0x37)",
            "> AI TRAP: Inverting F() gives 0x19FF [X]",
            "> TRUTH  : Keep F forward -> TURING 0xEC1B [OK]",
        ],
        "accent": (102, 255, 224),
        "yt_title": "94% of AI models fail this 1989 Motorola 68000 & Feistel cipher puzzle (0x3F54 vs 0xC0AB) 🧠 #ai",
        "yt_desc": (
            "Grade your AI model on the 15-Gate Sublevel B2 Cryptography Benchmark:\n"
            "👉 https://stardust-archive.net/ai-benchmark\n"
            "🕹️ Interactive VT100 Terminal: https://stardust-archive.net/terminal\n"
            "🔴 24/7 Late Night 1989 Radio Stream: https://www.youtube.com/@NovaHart_Official/live\n\n"
            "#ai #programming #cryptography #llm #chatgpt #claude #deepseek #gemini #ctf"
        ),
    },
    {
        "slug": "short_05_late_night_1989_radio_vibe",
        "duration": 26,
        "veo_video": os.path.join(BASE_DIR, "assets_arg/veo_loops/veo_night_drive_canyon.mp4"),
        "audio": os.path.join(BASE_DIR, "broadcast_archive/radio_master_songs/radio_shining_city.mp3"),
        "audio_start": 20,
        "crt_badge": os.path.join(BASE_DIR, "assets_arg/crt_nova_face.png"),
        "top_tag": "[ON AIR] 24/7 LATE NIGHT 1989 SHORTWAVE",
        "hook_title": "POV: IT'S 3:14 AM IN 1989 AND YOUR RADIO LOCKS ONTO...",
        "hook_sub": "...AN UNLISTED SUB-BASEMENT BROADCAST (14.2001 Hz)",
        "terminal_lines": [
            "> STATION: Orion Sublevel B2-114 (Unlisted)",
            "> FORMAT : 1985-1989 Type-I Ferric Cassettes",
            "> SIGNAL : 80s Synthpop + Numbers Intercepts",
            "> TOOL   : Free 1989 Tape Filter at /start",
            "> LIVE   : Tap 'Related Video' for 24/7 Radio",
            "> PORTAL : stardust-archive.net/start",
        ],
        "accent": (255, 176, 0),
        "yt_title": "POV: It's 3:14 AM in 1989 and your car radio locks onto an unlisted underground station 📻 #80s",
        "yt_desc": (
            "Tune into the 24/7 Late Night 1989 Radio Broadcast & use the free 1989 Cassette Audio Filter:\n"
            "🔴 24/7 Live Stream: https://www.youtube.com/@NovaHart_Official/live\n"
            "🎧 Free 1989 Cassette Filter & Jukebox: https://stardust-archive.net/start\n"
            "🏘️ 1995 GeoCities Time-Loop: https://stardust-archive.net/ai\n\n"
            "#80s #synthwave #synthpop #retrowave #cassette #nightdrive #nostalgia #radio"
        ),
    },
]


def create_overlay_png(spec, out_png_path):
    """Creates a 1080x1920 RGBA overlay with transparent central video viewport and crisp CRT HUD text."""
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (4, 8, 4, 255))
    draw = ImageDraw.Draw(img)

    accent = spec["accent"]
    green = (51, 255, 51)
    amber = (255, 176, 0)

    # Transparent central viewport (y=410..1190) where the Veo video will shine through
    # We'll punch a semi-transparent hole with CRT scanlines!
    hole_top, hole_bot = 400, 1180
    hole_left, hole_right = 44, 1036
    for y in range(hole_top, hole_bot):
        alpha = 45 if (y % 4 == 0) else 10
        draw.line([(hole_left, y), (hole_right, y)], fill=(0, 12, 0, alpha))

    # Outer CRT bezel & viewport frame
    draw.rectangle([20, 20, W - 20, H - 20], outline=green, width=4)
    draw.rectangle([hole_left - 4, hole_top - 4, hole_right + 4, hole_bot + 4], outline=accent, width=4)

    f_tag = load_font(30, bold=True)
    f_title = load_font(44, bold=True)
    f_sub = load_font(34, bold=True)
    f_term = load_font(28, bold=True)
    f_cta = load_font(30, bold=True)
    f_small = load_font(24, bold=False)

    # Top live banner
    draw.rectangle([44, 48, W - 44, 118], fill=(18, 6, 18, 240), outline=accent, width=3)
    draw.text((68, 66), spec["top_tag"], font=f_tag, fill=accent)

    # Hook Title (wrapped cleanly)
    wrapped_title = textwrap.wrap(spec["hook_title"], width=26)
    y_cursor = 140
    for line in wrapped_title[:3]:
        draw.text((54, y_cursor), line, font=f_title, fill=(255, 255, 255, 255))
        y_cursor += 54

    wrapped_sub = textwrap.wrap(spec["hook_sub"], width=34)
    y_cursor += 8
    for line in wrapped_sub[:2]:
        draw.text((54, y_cursor), line, font=f_sub, fill=amber)
        y_cursor += 44

    # Paste small CRT badge in top-right corner of the video window
    if os.path.exists(spec["crt_badge"]):
        try:
            badge = Image.open(spec["crt_badge"]).convert("RGBA")
            badge = badge.resize((190, 190), Image.Resampling.LANCZOS)
            img.paste(badge, (W - 246, hole_top + 16), badge)
            draw.rectangle([W - 246, hole_top + 16, W - 56, hole_top + 206], outline=green, width=2)
        except Exception:
            pass

    # Bottom Terminal Readout Box (y=1205..1645)
    draw.rectangle([44, 1205, W - 44, 1650], fill=(4, 16, 4, 245), outline=green, width=3)
    draw.rectangle([44, 1205, W - 44, 1258], fill=(10, 38, 10, 255), outline=green, width=2)
    draw.text((64, 1217), "[B2] SUBLEVEL B2 TELEMETRY // 14.2001 Hz LOCKED", font=f_small, fill=amber)

    ty = 1276
    for tline in spec["terminal_lines"]:
        color = accent if ("TRUTH" in tline or "RESULT" in tline or "ENTER" in tline or "LIVE" in tline) else green
        draw.text((64, ty), tline, font=f_term, fill=color)
        ty += 58

    # Bottom Call-To-Action Funnel Box (y=1675..1865)
    draw.rectangle([44, 1675, W - 44, 1868], fill=(38, 18, 0, 250), outline=amber, width=4)
    draw.text((68, 1695), "[LIVE] TAP 'RELATED VIDEO' FOR 24/7 RADIO", font=f_cta, fill=(255, 220, 80))
    draw.text((68, 1748), ">> stardust-archive.net/ai", font=f_title, fill=green)
    draw.text((68, 1812), "[SCORE] Test ChatGPT/Claude: /ai-benchmark", font=f_small, fill=(255, 180, 255))

    img.save(out_png_path)


def render_short(spec):
    overlay_png = os.path.join(OUT_DIR, f"{spec['slug']}_overlay.png")
    out_mp4 = os.path.join(OUT_DIR, f"{spec['slug']}.mp4")
    create_overlay_png(spec, overlay_png)

    dur = spec["duration"]
    astart = spec["audio_start"]

    # FFmpeg filter_complex:
    # 1. Loop & scale the Veo video to fill the 992x780 viewport (x=44, y=400) with subtle CRT green/contrast grading
    # 2. Overlay the 1080x1920 RGBA HUD frame on top
    # 3. Mix the 1989 cassette audio track with fade-in/out
    filter_complex = (
        f"[0:v]scale=1000:780:force_original_aspect_ratio=increase,crop=1000:780,"
        f"eq=contrast=1.15:brightness=-0.03:saturation=1.2, pad=1080:1920:40:400:black[bg];"
        f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[vout];"
        f"[2:a]atrim=start={astart}:duration={dur},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=0.6,afade=t=out:st={dur-1.2}:d=1.2,volume=1.15[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", spec["veo_video"],
        "-loop", "1", "-i", overlay_png,
        "-i", spec["audio"],
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", "[aout]",
        "-t", str(dur),
        "-r", "30",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-movflags", "+faststart",
        out_mp4,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    os.remove(overlay_png)
    size_mb = os.path.getsize(out_mp4) / (1024 * 1024)
    print(f"[✓ Rendered Short] {out_mp4} ({dur}s, {size_mb:.2f} MB)")


def write_cheatsheet():
    md_path = os.path.join(OUT_DIR, "UPLOAD_CHEATSHEET.md")
    lines = [
        "# 📱 Ready-to-Upload 9:16 YouTube Shorts / TikTok / Reels Batch\n",
        "All 5 vertical MP4s (`1080x1920`, 30fps, H.264 + AAC) are in this folder (`/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/shorts_ready/`).\n",
        "## ⚡ Crucial YouTube Shorts Funnel Setting",
        "When uploading each Short on YouTube Studio (`@NovaHart_Official`), set the **\"Related Video\"** field to your **24/7 Live Radio Stream (`🔴 24/7 Late Night 1989 Radio // Lost 80s Synthpop, Cassette Tapes & The 1983 Rogue AI Broadcast`)** so every viewer can tap 1 button on the Short to enter the livestream!\n\n---\n",
    ]
    for i, s in enumerate(SHORTS_SPECS, 1):
        lines.append(f"## Short #{i}: `{s['slug']}.mp4` ({s['duration']}s)")
        lines.append(f"**Title:**\n```text\n{s['yt_title']}\n```")
        lines.append(f"**Description / Pinned Comment:**\n```text\n{s['yt_desc']}\n```\n---\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[✓ Cheatsheet] {md_path}")


if __name__ == "__main__":
    for s in SHORTS_SPECS:
        render_short(s)
    write_cheatsheet()
