"""Generate authentic 1990s 88x31 web badges and retro GIF icons using PIL."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BADGE_DIR = os.path.join(ROOT, "assets", "badges")
os.makedirs(BADGE_DIR, exist_ok=True)

def draw_bevel(draw, box, top_color, bot_color):
    x0, y0, x1, y1 = box
    draw.line([(x0, y0), (x1, y0)], fill=top_color)
    draw.line([(x0, y0), (x0, y1)], fill=top_color)
    draw.line([(x0, y1), (x1, y1)], fill=bot_color)
    draw.line([(x1, y0), (x1, y1)], fill=bot_color)

def make_88x31(name, left_bg, left_fg, left_text, right_bg, right_fg, right_text, split=44):
    img = Image.new("RGB", (88, 31), color=left_bg)
    draw = ImageDraw.Draw(img)
    # Right box
    draw.rectangle([split, 0, 87, 30], fill=right_bg)
    # Bevel border (classic 90s button)
    draw_bevel(draw, (0, 0, 87, 30), "#FFFFFF", "#555555")
    draw_bevel(draw, (1, 1, 86, 29), "#E0E0E0", "#000000")
    
    # Text
    # Use default bitmap font
    font = ImageFont.load_default()
    
    # Draw left text
    lt_lines = left_text.split("\n")
    y_start = max(2, (31 - len(lt_lines) * 11) // 2)
    for i, line in enumerate(lt_lines):
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        x = max(3, (split - w) // 2)
        draw.text((x, y_start + i * 11), line, fill=left_fg, font=font)
        
    # Draw right text
    rt_lines = right_text.split("\n")
    y_start_r = max(2, (31 - len(rt_lines) * 11) // 2)
    for i, line in enumerate(rt_lines):
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        x = split + max(2, ((88 - split) - w) // 2)
        draw.text((x, y_start_r + i * 11), line, fill=right_fg, font=font)
        
    path = os.path.join(BADGE_DIR, f"{name}.gif")
    img.save(path, format="GIF")
    print(f"Created {path}")

def make_cassette():
    img = Image.new("RGB", (48, 32), color="#222222")
    draw = ImageDraw.Draw(img)
    draw_bevel(draw, (0, 0, 47, 31), "#888888", "#000000")
    # Cassette body
    draw.rectangle([4, 4, 43, 27], fill="#111111", outline="#666666")
    # Label
    draw.rectangle([8, 6, 39, 18], fill="#ECE5D0", outline="#444444")
    font = ImageFont.load_default()
    draw.text((10, 7), "C-90", fill="#AA0000", font=font)
    # Spools
    draw.ellipse([14, 19, 20, 25], fill="#FFFFFF", outline="#000000")
    draw.ellipse([27, 19, 33, 25], fill="#FFFFFF", outline="#000000")
    draw.rectangle([21, 21, 26, 23], fill="#555555")
    path = os.path.join(BADGE_DIR, "cassette.gif")
    img.save(path, format="GIF")
    print(f"Created {path}")

def make_star():
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 8-point gold glittering star
    points = [
        (16, 2), (19, 11), (28, 11), (21, 17), (24, 27),
        (16, 21), (8, 27), (11, 17), (4, 11), (13, 11)
    ]
    draw.polygon(points, fill="#FFDD00", outline="#FF8800")
    draw.point((16, 16), fill="#FFFFFF")
    draw.point((15, 16), fill="#FFFFFF")
    draw.point((16, 15), fill="#FFFFFF")
    path = os.path.join(BADGE_DIR, "spinning_star.gif")
    img.save(path, format="GIF")
    print(f"Created {path}")

def make_novachan_chibi():
    # 48x48 pixel art of blonde Nova-chan with blonde hair and gold star
    img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Blonde hair back
    draw.rectangle([10, 8, 38, 38], fill="#FCD842")
    # Face
    draw.rectangle([15, 14, 33, 30], fill="#FFE0BD")
    # Blonde bangs
    draw.polygon([(12, 10), (36, 10), (34, 18), (28, 14), (24, 18), (20, 14), (14, 18)], fill="#FFE666")
    # Eyes (blue eyes, anime style)
    draw.rectangle([18, 19, 21, 23], fill="#0088FF")
    draw.rectangle([27, 19, 30, 23], fill="#0088FF")
    draw.point((19, 20), fill="#FFFFFF")
    draw.point((28, 20), fill="#FFFFFF")
    # Blush
    draw.rectangle([16, 24, 19, 25], fill="#FF9999")
    draw.rectangle([29, 24, 32, 25], fill="#FF9999")
    # Smile
    draw.line([(22, 26), (26, 26)], fill="#CC3333")
    # Gold star hair clip (blonde hair clip)
    draw.polygon([(33, 9), (36, 12), (39, 9), (37, 15), (34, 14)], fill="#FFCC00", outline="#FF6600")
    # Sailor collar / dress (pink/white)
    draw.rectangle([14, 31, 34, 44], fill="#FFB6C1")
    draw.polygon([(18, 31), (24, 38), (30, 31)], fill="#FFFFFF", outline="#0044AA")
    # White gloves
    draw.rectangle([8, 36, 13, 44], fill="#FFFFFF", outline="#CCCCCC")
    draw.rectangle([35, 36, 40, 44], fill="#FFFFFF", outline="#CCCCCC")
    path = os.path.join(BADGE_DIR, "novachan_chibi.gif")
    img.save(path, format="GIF")
    print(f"Created {path}")

def make_guestbook():
    img = Image.new("RGBA", (44, 36), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Open leather ledger book
    draw.rectangle([4, 10, 40, 32], fill="#4A2810", outline="#201005")
    draw.rectangle([6, 12, 21, 30], fill="#FFF8DC")
    draw.rectangle([23, 12, 38, 30], fill="#FFF8DC")
    # Faux writing lines
    for y in [15, 18, 21, 24, 27]:
        draw.line([(8, y), (19, y)], fill="#8888AA")
        draw.line([(25, y), (36, y)], fill="#8888AA")
    # Feather quill
    draw.line([(28, 28), (41, 4)], fill="#DDDDDD", width=2)
    draw.line([(40, 4), (43, 2)], fill="#FFFFFF")
    draw.point((27, 29), fill="#000088")
    path = os.path.join(BADGE_DIR, "guestbook.gif")
    img.save(path, format="GIF")
    print(f"Created {path}")

def make_radio_tower():
    img = Image.new("RGBA", (36, 44), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Lattice tower
    draw.line([(18, 8), (6, 42)], fill="#CCCCCC", width=2)
    draw.line([(18, 8), (30, 42)], fill="#CCCCCC", width=2)
    for y in [18, 26, 34]:
        draw.line([(10 + (y-18)//3, y), (26 - (y-18)//3, y)], fill="#AAAAAA")
    draw.line([(10, 18), (24, 34)], fill="#888888")
    draw.line([(26, 18), (8, 34)], fill="#888888")
    # Flashing red beacon tip
    draw.ellipse([16, 4, 20, 8], fill="#FF0000", outline="#FF8888")
    # Broadcast waves
    draw.arc([8, 0, 28, 16], start=200, end=340, fill="#00FFCC")
    draw.arc([4, -4, 32, 20], start=200, end=340, fill="#00FFCC")
    path = os.path.join(BADGE_DIR, "radio_tower.gif")
    img.save(path, format="GIF")
    print(f"Created {path}")

def make_cd_spin():
    img = Image.new("RGBA", (36, 36), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, 33, 33], fill="#E8E8E8", outline="#888888")
    draw.arc([4, 4, 31, 31], start=45, end=135, fill="#00FFFF", width=2)
    draw.arc([4, 4, 31, 31], start=225, end=315, fill="#FF00FF", width=2)
    draw.ellipse([13, 13, 22, 22], fill="#FFFFFF", outline="#AAAAAA")
    draw.ellipse([16, 16, 19, 19], fill="#000000")
    path = os.path.join(BADGE_DIR, "cd_spin.gif")
    img.save(path, format="GIF")
    print(f"Created {path}")

def main():
    # 1. Netscape 2.0 Now
    make_88x31("netscape_now", "#000088", "#FFFFFF", "NETSCAPE\nNOW!", "#0055AA", "#FFCC00", "NAVIGATOR\n2.0", split=40)
    # 2. Humans for Nova
    make_88x31("hfn_badge", "#000000", "#FFCCFF", "HUMANS\nFOR NOVA", "#330033", "#00FFFF", "MEMBER\n#1994", split=46)
    # 3. Listening Night
    make_88x31("listening_night", "#001A33", "#33FF33", "02:14 UTC\nSURVIVOR", "#003366", "#FFFF00", "LISTENING\nNIGHT III", split=44)
    # 4. Node Hunter
    make_88x31("node_hunter", "#330000", "#FF6666", "NODE\nHUNTER", "#660000", "#FFFFCC", "14.2 Hz\nCARRIER", split=42)
    # 5. Tape Trader
    make_88x31("tape_trader", "#222222", "#FFCC00", "TAPE\nTRADER", "#333333", "#FFFFFF", "C-90 / DAT\nMAIL ORDER", split=40)
    # 6. Stardust Webring
    make_88x31("stardust_webring", "#000055", "#00FFFF", "STARDUST\nWEBRING", "#000000", "#FF00FF", "STATION\nMEMBER", split=45)
    # 7. Orion Records Japan
    make_88x31("orion_records_badge", "#FFFFFF", "#000088", "ORION\nRECORDS", "#000088", "#FFFFFF", "AKASAKA\nARCHIVE", split=42)
    # 8. Public Harmony Warning
    make_88x31("warning_glitch", "#CC0000", "#FFFFFF", "PUBLIC\nHARMONY", "#000000", "#FFCC00", "COMPLIANT\n1985", split=45)
    # 9. GeoCities Homestead
    make_88x31("geocities_badge", "#006633", "#FFFFFF", "GEOCITIES\nWATERGATE", "#004422", "#FFFF00", "HOMESTEAD\nFREE HOST", split=46)
    # 10. Best Viewed 640x480
    make_88x31("view_640", "#444444", "#FFFFFF", "BEST VIEW\n640 x 480", "#222222", "#33FF33", "16-BIT\nCOLOR", split=44)
    # 11. Cassette Icon
    make_cassette()
    # 12. Golden Star Icon
    make_star()
    # 13. Blonde Nova-chan Chibi
    make_novachan_chibi()
    # 14. Guestbook Icon
    make_guestbook()
    # 15. Radio Tower
    make_radio_tower()
    # 16. CD Spin
    make_cd_spin()
    print("All 16 badges and icons generated successfully!")

if __name__ == "__main__":
    main()
