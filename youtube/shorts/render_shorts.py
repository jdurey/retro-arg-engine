#!/usr/bin/env python3
"""Renders viral 9:16 vertical shorts for YouTube Shorts, TikTok, and Instagram Reels using Pillow + ffmpeg."""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ASSETS = os.path.join(HERE, "assets")
OUT_DIR = os.path.join(HERE, "rendered")
os.makedirs(OUT_DIR, exist_ok=True)

AUDIO_DIR = os.path.join(ROOT, "site", "ftp", "kamome", "audio")


def add_captions(img_path, top_text, mid_text, bottom_text, out_img_path):
    img = Image.open(img_path).convert("RGBA")
    img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(img)

    # Use default or system font
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
        font_mid = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 44)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 38)
    except Exception:
        font_large = font_mid = font_small = ImageFont.load_default()

    def draw_badge(y, text, font, text_color, bg_color):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (1080 - tw) // 2
        padding = 24
        draw.rectangle(
            [x - padding, y - padding // 2, x + tw + padding, y + th + padding // 2],
            fill=bg_color,
        )
        draw.text((x, y - 4), text, font=font, fill=text_color)

    # Top Badge
    draw_badge(220, top_text, font_large, (255, 255, 255, 255), (0, 0, 0, 210))

    # Bottom Callout Badges
    draw_badge(1480, mid_text, font_mid, (57, 255, 20, 255), (0, 0, 0, 220))
    draw_badge(1570, bottom_text, font_small, (255, 255, 255, 255), (0, 0, 0, 210))

    final_img = img.convert("RGB")
    final_img.save(out_img_path, quality=95)


def render_short(bg_file, audio_file, top_text, mid_text, bottom_text, out_mp4, duration=20):
    framed_jpg = os.path.join(ASSETS, f"framed_{os.path.basename(bg_file)}")
    add_captions(bg_file, top_text, mid_text, bottom_text, framed_jpg)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", framed_jpg,
        "-i", audio_file,
        "-t", str(duration),
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"-> Successfully rendered: {out_mp4}")


def main():
    print("=== RENDERING VIRAL SHORTS ===")
    
    # Short 1: The 1995 Server Mystery
    s1_bg = os.path.join(ASSETS, "short1_bg.jpg")
    s1_audio = os.path.join(AUDIO_DIR, "ghost_in_the_chorus.mp3")
    s1_out = os.path.join(OUT_DIR, "short1_the_forgotten_server.mp4")
    render_short(
        s1_bg, s1_audio,
        "UNSOLVED INTERNET MYSTERY (1995)",
        "This 1995 server is still transmitting.",
        "14.2 Hz CARRIER // stardust-archive.net",
        s1_out,
        duration=18
    )

    # Short 2: The Found 1989 Cassette
    s2_bg = os.path.join(ASSETS, "short2_bg.jpg")
    s2_audio = os.path.join(AUDIO_DIR, "jp-85-gt_ghost_transit_shortwave.mp3")
    s2_out = os.path.join(OUT_DIR, "short2_found_tape_1989.mp4")
    render_short(
        s2_bg, s2_audio,
        "ESTATE SALE // 1989 TAPE DISCOVERY",
        "The label said 'Do Not Play'.",
        "Listen to the hidden frequency at the end...",
        s2_out,
        duration=22
    )


if __name__ == "__main__":
    main()
