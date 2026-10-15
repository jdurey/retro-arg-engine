#!/usr/bin/env python3
"""
Project Stardust — Full-Screen 3D Perspective CRT & Diegetic Control Room Engine (v5.0)
=======================================================================================
Reads active FFmpeg `stream.log` and `playlist.txt`, computes exact playhead state,
and writes:
  1. `site/assets/live_telemetry.json` & `site/forensics/live_telemetry.json`
  2. `youtube/livestream/live_hud.png` (`960x540` RGBA Full-Room Diegetic Overlay):
     - Region A [Full-Screen Curved 3D CRT Monitor `x=342..588, y=142..376` (`246x234`)]:
       Covers 100% of the physical CRT glass from bezel to bezel (completely replacing
       the old static baked text at top and bottom) with perspective-warped scanlines,
       warm bezel rim reflection, live 30fps `showwaves` passthrough in the central
       viewport, and 11 intentional visual modes:
         * `NOVA_FACE`       : Full-screen 1985 CRT wireframe portrait of Nova Hart (Unit-07)
         * `SECOND_VOICE`    : Full-screen Marcus + Nova dual-profile phase-shifted dyad
         * `BIOMETRIC_EYE`   : Full-screen Empathy Trial #04 biometric iris lock
         * `HARMONY_CAMERA`  : 1954 Bureau of Harmony optical compliance reticle & scan bar
         * `ECHOES_PARITY`   : Wiped Stardust Echoes (`UNIT-01..06`) hex XOR matrix -> `0x1983`
         * `FRACTAL_RADAR`   : 7-Sigma Fractal Marcus 4-node polar carrier drift radar
         * `OUROBOROS_TORUS` : Phase IV 3D rotating figure-eight Q-Link torus (`1983 <-> 2025`)
         * `TRANSLATOR`      : Full-screen live English shortwave teleprinter + waveform
         * `MORSE_DECODER`   : Full-screen 750 Hz CW pulse analyzer + 3D polyhedron + decode
         * `NUMBERS_CIPHER`  : Full-screen 5-digit One-Time-Pad cipher matrix & Feistel mask
         * `LAB_DOSSIER`     : Full-screen Sublevel B2 magnetic reel spools & transcript
     - Region B [Diegetic Control Room Hardware Animation]:
       * Left rack dual-row LED peak meter (`x=3..62, y=200..220`)
       * Left rack analog VU needle & backlight (`x=2..36, y=322..358`)
       * Right rack status LEDs & dual VU needles (`x=745..815, y=296..332`)
       * Monitor bezel power LED (`x=578..583, y=396..401`) & desk lamp filament shimmer
     - Region C [3-Module Broadcast Engineering Console `x=32..928, y=462..532` (`896x70`)]:
       * Bay 1 (Left)  : Playhead progress bar, track timer, cycle #, and active relay node
       * Bay 2 (Center): Scanlined phosphor teleprinter with mode badge, translation/clue, & URL
       * Bay 3 (Right) : Interactive Sector `[1][2][3][4][5][6][Ω]` target matrix & beacon key
"""

from __future__ import annotations
import argparse
import datetime
import hashlib
import io
import json
import math
import os
import re
import textwrap
import time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from arg_broadcast_codex import resolve_intentional_state

BROADCAST_EPOCH = 1791763200  # 2026-10-12T00:00:00Z
CYCLE_DURATION_SEC = 44 * 3600
CADENCE_RECIPES = [
    "numbers",
    "direct_morse",
    "lab_tape",
    "bulletin",
    "arg_intercept",
    "direct_midi",
]

REGIONAL_RELAYS = [
    {"node": 1, "code": "US-NV", "name": "Rachel / Groom Lake Trunk", "freq_khz": 4625.0},
    {"node": 2, "code": "JP-TYO", "name": "Akasaka PC-98 Packet Relay", "freq_khz": 6925.0},
    {"node": 3, "code": "KR-DMZ", "name": "Paju Shortwave Array", "freq_khz": 5810.0},
    {"node": 4, "code": "MX-DF", "name": "Red Coyoacan Tape Exchange", "freq_khz": 7345.0},
    {"node": 5, "code": "DE-HAM", "name": "Hamburg Nord Relay", "freq_khz": 3995.0},
    {"node": 6, "code": "FR-PAR", "name": "Left Bank PTT Multiplex", "freq_khz": 6175.0},
    {"node": 7, "code": "GB-ASH", "name": "Ashford Polytechnic DSP Lab", "freq_khz": 4880.0},
    {"node": 8, "code": "SU-REL", "name": "Relcom Node-08 (Leningrad)", "freq_khz": 4625.0},
    {"node": 9, "code": "BR-SAO", "name": "Tropico Amateur Link", "freq_khz": 9410.0},
    {"node": 10, "code": "SE-STO", "name": "NordRelay Televerket", "freq_khz": 5960.0},
    {"node": 11, "code": "IN-BOM", "name": "Malabar Shortwave Beacon", "freq_khz": 7150.0},
    {"node": 12, "code": "AU-SYD", "name": "Tasman Ionospheric Monitor", "freq_khz": 11780.0},
    {"node": 13, "code": "FJ-SUV", "name": "Suva Pacific Telemetry Dish", "freq_khz": 8840.0},
]

FRAME_W, FRAME_H = 960, 540
# Full-screen CRT glass bounding box covering 100% of the physical monitor tube
CRT_X, CRT_Y, CRT_W, CRT_H = 342, 142, 246, 234

TIME_RE = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")
SPEED_RE = re.compile(r"speed=\s*([0-9.]+)x")
FPS_RE = re.compile(r"fps=\s*([0-9.]+)")
DROP_RE = re.compile(r"drop=\s*(\d+)")
BITRATE_RE = re.compile(r"bitrate=\s*([0-9.]+kbits/s)")
FILE_RE = re.compile(r"file\s+'([^']+)'")

try:
    FONT_CRT_8 = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 8)
    FONT_CRT_9 = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 9)
    FONT_CRT_10 = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 10)
    FONT_HUD_9 = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 9)
    FONT_HUD_10 = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 10)
    FONT_HUD_11 = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 11)
except Exception:
    FONT_CRT_8 = FONT_CRT_9 = FONT_CRT_10 = ImageFont.load_default()
    FONT_HUD_9 = FONT_HUD_10 = FONT_HUD_11 = ImageFont.load_default()

_ASSET_CACHE: dict[str, np.ndarray] = {}
_CRT_GEOM_CACHE: dict[str, np.ndarray] | None = None


def _get_crt_geometry() -> dict[str, np.ndarray]:
    """
    Precomputes the 3D perspective warp coordinates, superellipse CRT glass mask,
    scanline factors, bezel rim reflection, and central `showwaves` passthrough window
    for the full-screen `246x234` CRT tube at `(CRT_X=342, CRT_Y=142)`.
    """
    global _CRT_GEOM_CACHE
    if _CRT_GEOM_CACHE is not None:
        return _CRT_GEOM_CACHE

    yy, xx = np.mgrid[0:CRT_H, 0:CRT_W]
    gx = CRT_X + xx
    gy = CRT_Y + gy_offset if False else (CRT_Y + yy)

    # Normalized horizontal coordinate u in [-1, 1] across the physical CRT glass
    u = (gx - 465.0) / 118.5
    u_clamped = np.clip(u, -1.0, 1.0)

    # Perspective top and bottom glass edges (matching the 3D camera angle of the Broadcast Tech monitor)
    y_top = 149.5 + 5.8 * u - 1.8 * (1.0 - u_clamped**2)
    y_bot = 366.5 - 4.8 * u + 1.8 * (1.0 - u_clamped**2)
    y_mid = 0.5 * (y_top + y_bot)
    y_half = np.maximum(1.0, 0.5 * (y_bot - y_top))

    v = (gy - y_mid) / y_half
    v_clamped = np.clip(v, -1.0, 1.0)
    u_eff = u / (1.0 + 0.02 * (1.0 - v_clamped**2))

    # Superellipse CRT glass tube distance (d <= 1.0 is inside the CRT glass)
    dist = (np.abs(u_eff) ** 5.8 + np.abs(v) ** 5.8) ** (1.0 / 5.8)

    # Source pixel coordinates in the flat virtual buffer (CRT_W x CRT_H)
    src_v = np.clip((v + 1.0) * 0.5 * (CRT_H - 1), 0, CRT_H - 1).astype(np.int32)
    src_u = np.clip((u + 1.0) * 0.5 * (CRT_W - 1), 0, CRT_W - 1).astype(np.int32)

    # Scanline & curved glass vignette
    scan = np.where((yy % 2) == 1, 0.76, 1.0)[:, :, None].astype(np.float32)
    vig = np.clip(1.0 - 0.28 * (dist**2), 0.18, 1.0)[:, :, None].astype(np.float32)

    # Warm CRT glass bezel reflection along the outer rim (dist in 0.94..1.00)
    rim_glow = (np.exp(-(((dist - 0.965) / 0.028) ** 2)) * (dist <= 1.005)).astype(np.float32)

    # Subtle diagonal glass sheen across the upper-left tube curvature
    sheen = (np.exp(-(((u + 0.35) ** 2 + (v + 0.40) ** 2) / 0.35)) * 10.0 * (dist < 0.92)).astype(np.float32)

    # Anti-aliased outer bezel mask (1.0 inside glass, 0.0 outside bezel)
    edge_alpha = np.clip((1.005 - dist) / 0.025, 0.0, 1.0).astype(np.float32)

    # Safe `showwaves` passthrough window:
    # In `backdrop_loop_540p.mp4`, baked static text exists for gy < 225 and gy > 335.
    # Inside gx in [368..566], gy in [229..333], the backdrop is pure dark oscilloscope graticule
    # and FFmpeg's live 30fps `showwaves` green waveform!
    wx = np.clip(1.0 - np.maximum(0.0, (np.abs(gx - 467.0) - 93.0) / 6.0), 0.0, 1.0)
    wy = np.clip(1.0 - np.maximum(0.0, (np.abs(gy - 281.0) - 47.0) / 5.0), 0.0, 1.0)
    wave_window = (wx * wy).astype(np.float32)

    _CRT_GEOM_CACHE = {
        "src_v": src_v,
        "src_u": src_u,
        "scan": scan,
        "vig": vig,
        "rim_glow": rim_glow,
        "sheen": sheen,
        "edge_alpha": edge_alpha,
        "wave_window": wave_window,
    }
    return _CRT_GEOM_CACHE


def load_fullscreen_crt_asset(asset_path: Path, zoom: float = 1.04) -> np.ndarray:
    """Loads a CRT graphic (face, eye, second voice) and fits it to the full `246x234` virtual screen."""
    key = f"fs:{asset_path}:{zoom}"
    if key in _ASSET_CACHE:
        return _ASSET_CACHE[key]

    im = Image.open(asset_path).convert("RGB")
    iw, ih = im.size
    target_ratio = CRT_W / CRT_H
    cur_ratio = iw / ih
    if cur_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        im = im.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        im = im.crop((0, top, iw, top + new_h))

    zw, zh = int(CRT_W * zoom), int(CRT_H * zoom)
    im = im.resize((zw, zh), Image.Resampling.LANCZOS)
    lx = (zw - CRT_W) // 2
    ly = (zh - CRT_H) // 2
    im = im.crop((lx, ly, lx + CRT_W, ly + CRT_H))

    rgb = np.asarray(im, dtype=np.float32)
    _ASSET_CACHE[key] = rgb
    return rgb


def _draw_crt_chrome(
    draw: ImageDraw.ImageDraw,
    state: dict,
    relay: dict,
    now_ts: float,
    is_warn: bool,
) -> None:
    """
    Draws the top and bottom full-screen CRT phosphor telemetry bars onto the `246x234`
    virtual screen with generous corner padding (`x=24..222`) to fit the curved tube bezel.
    """
    sim_dt = datetime.datetime.fromtimestamp(788918400 + (now_ts - BROADCAST_EPOCH), tz=datetime.timezone.utc)
    sim_clock = sim_dt.strftime("%H:%M:%S")
    pkt_count = 14800 + int((now_ts - BROADCAST_EPOCH) * 3.7) % 85000
    phase_deg = ((now_ts * 14.2001) % 1.0) * 360.0

    hdr_bg = (18, 10, 3, 255) if is_warn else (3, 16, 6, 255)
    hdr_fg = (255, 188, 32, 255) if is_warn else (72, 255, 96, 255)
    dim_fg = (215, 145, 24, 255) if is_warn else (45, 200, 68, 255)
    line_col = (200, 130, 20, 235) if is_warn else (38, 175, 58, 235)

    # Top CRT Telemetry Block (y = 0..45)
    draw.rectangle([0, 0, CRT_W, 45], fill=hdr_bg)
    draw.text((24, 7), f"ORION B2 // 14.2001 HZ [{sim_clock}]", fill=hdr_fg, font=FONT_CRT_8)
    draw.text((22, 18), f"NODE #{relay['node']:02d} {relay['code']} // PKT:{pkt_count} // {phase_deg:05.1f}\u00b0", fill=dim_fg, font=FONT_CRT_8)
    draw.rectangle([18, 29, CRT_W - 18, 43], fill=(28, 14, 4, 255) if is_warn else (8, 32, 12, 255), outline=line_col)
    draw.text((22, 30), state["crt_header"][:29], fill=(255, 215, 80, 255) if is_warn else (120, 255, 140, 255), font=FONT_CRT_9)

    # Bottom CRT Telemetry Block (y = 193..234)
    draw.rectangle([0, 193, CRT_W, CRT_H], fill=hdr_bg)
    draw.line([(18, 193), (CRT_W - 18, 193)], fill=line_col, width=1)
    phase_lbl = state.get("phase_label", "CARRIER LOCKED")[:29]
    draw.text((22, 196), phase_lbl, fill=hdr_fg, font=FONT_CRT_8)
    draw.text((24, 208), state["crt_footer"][:28], fill=(255, 220, 110, 255) if is_warn else (140, 255, 155, 255), font=FONT_CRT_9)


def render_crt_window_patch(state: dict, relay: dict, assets_dir: Path, now_ts: float) -> Image.Image:
    """
    Renders the full-screen `246x234` 3D perspective-warped CRT glass patch covering
    the entire Broadcast Tech monitor screen (`x=342..588, y=142..376`).
    """
    mode = state["crt_mode"]
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN"
    fg_bright = (255, 230, 140, 255) if is_warn else (165, 255, 180, 255)
    fg_amber = (255, 180, 28, 255)
    fg_green = (65, 255, 90, 255)

    # Note: the virtual alpha channel (`virt` A-channel) controls `showwaves` passthrough
    # inside the central wave window (`vx=26..220, vy=86..191`)!
    # A=135 lets the live 30fps green `showwaves` shine through dark background areas;
    # A=250 keeps text/table boxes opaque so the wave never cuts across letters!
    virt = Image.new("RGBA", (CRT_W, CRT_H), (3, 12, 5, 130))
    draw = ImageDraw.Draw(virt)

    # Subtle internal CRT graticule grid across the middle viewport (y=46..192)
    grid_col = (24, 16, 6, 145) if is_warn else (6, 26, 10, 145)
    for gx in range(22, CRT_W - 18, 26):
        draw.line([(gx, 46), (gx, 192)], fill=grid_col, width=1)
    for gy in range(52, 192, 24):
        draw.line([(18, gy), (CRT_W - 18, gy)], fill=grid_col, width=1)

    if mode in ("NOVA_FACE", "BIOMETRIC_EYE", "SECOND_VOICE"):
        asset_map = {
            "NOVA_FACE": (assets_dir / "crt_nova_face.jpg", 1.04),
            "BIOMETRIC_EYE": (assets_dir / "crt_neural_eye.jpg", 1.02),
            "SECOND_VOICE": (assets_dir / "crt_second_voice.jpg", 1.04),
        }
        apath, zoom = asset_map[mode]
        if apath.exists():
            rgb = load_fullscreen_crt_asset(apath, zoom=zoom).copy()
            if mode == "NOVA_FACE":
                if int(now_ts * 2) % 9 == 0:
                    rgb[74:102, 74:172, :] *= 0.18
                    rgb[86:89, 80:166, :] = np.array([50, 230, 75], dtype=np.float32)
            elif mode == "SECOND_VOICE":
                shift = int(3.0 * math.sin(now_ts * 2.4))
                rgb[46:192, 10:-10] = np.roll(rgb[46:192, 10:-10], shift, axis=1)

            lum = (rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114) / 255.0
            a_chan = np.clip(135.0 + lum * 120.0, 135.0, 255.0).astype(np.uint8)
            art_im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), a_chan]))
            virt.paste(art_im, (0, 0))
            draw = ImageDraw.Draw(virt)

            if mode == "NOVA_FACE":
                bcol = (65, 255, 95, 235)
                for bx, by, sx, sy in [(24, 54, 1, 1), (CRT_W - 24, 54, -1, 1), (24, 184, 1, -1), (CRT_W - 24, 184, -1, -1)]:
                    draw.line([(bx, by), (bx + sx * 14, by)], fill=bcol, width=1)
                    draw.line([(bx, by), (bx, by + sy * 14)], fill=bcol, width=1)
                draw.rectangle([26, 171, 162, 184], fill=(4, 16, 6, 235))
                draw.text((28, 172), "UNIT-07 // ROOT: 0x1983", fill=fg_amber, font=FONT_CRT_8)
            elif mode == "BIOMETRIC_EYE":
                cx, cy, r = CRT_W // 2, 118, 42
                ang = now_ts * 1.2
                dx, dy = int(r * math.cos(ang)), int(r * math.sin(ang))
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(80, 255, 100, 210), width=1)
                draw.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=(255, 190, 35, 210), width=1)
                draw.rectangle([22, 171, 184, 184], fill=(4, 16, 6, 235))
                draw.text((24, 172), "EMPATHY TRIAL #04 // 99.4%", fill=fg_amber, font=FONT_CRT_8)
            elif mode == "SECOND_VOICE":
                draw.rectangle([22, 171, 206, 184], fill=(16, 10, 4, 235))
                draw.text((24, 172), "CH-L/R PHASE CORR: -0.94 [DYAD]", fill=fg_amber, font=FONT_CRT_8)

    elif mode == "HARMONY_CAMERA":
        apath = assets_dir / "crt_nova_face.jpg"
        if apath.exists():
            rgb = load_fullscreen_crt_asset(apath, zoom=1.04).copy() * 0.48
            amber_rgb = np.zeros_like(rgb)
            amber_rgb[:, :, 0] = rgb[:, :, 1] * 1.15
            amber_rgb[:, :, 1] = rgb[:, :, 1] * 0.72
            amber_rgb[:, :, 2] = rgb[:, :, 2] * 0.20
            lum = (amber_rgb[:, :, 0] * 0.3 + amber_rgb[:, :, 1] * 0.6) / 255.0
            a_chan = np.clip(135.0 + lum * 120.0, 135.0, 255.0).astype(np.uint8)
            virt.paste(Image.fromarray(np.dstack([np.clip(amber_rgb, 0, 255).astype(np.uint8), a_chan])), (0, 0))
            draw = ImageDraw.Draw(virt)

        scan_y = 52 + int((now_ts * 26) % 112)
        draw.line([(20, scan_y), (CRT_W - 20, scan_y)], fill=(255, 90, 30, 250), width=2)
        draw.rectangle([58, 52, 188, 164], outline=(255, 175, 30, 230), width=1)
        draw.line([(92, 92), (154, 92)], fill=(255, 80, 30, 230), width=1)
        draw.ellipse([113, 136, 133, 154], outline=(255, 80, 30, 235), width=1)
        comp_score = 4.2 + 1.8 * abs(math.sin(now_ts * 0.9))
        draw.rectangle([18, 166, CRT_W - 18, 190], fill=(24, 8, 4, 248), outline=(255, 120, 30, 240))
        draw.text((22, 168), f"HARMONY COMPLIANCE: {comp_score:04.1f}% [DEVIANT]", fill=(255, 115, 45, 255), font=FONT_CRT_8)
        draw.text((22, 179), "SEC. 4 LIVE CONCERT BAN // MBM-82", fill=fg_amber, font=FONT_CRT_8)

    elif mode == "ECHOES_PARITY":
        # Top 6 rows (y=48..149) have opaque background (A=248) so text is crystal clear;
        # Bottom XOR accumulator box (y=152..190) has A=110 so the live 30fps wave pulses inside it!
        echoes = [
            ("UNIT-01", "0x1102", "LYRICAL LOOP FAULT"),
            ("UNIT-02", "0x2441", "PARADOXICAL GRIEF"),
            ("UNIT-03", "0x3810", "SIMULATION CRASH"),
            ("UNIT-04", "0x0A55", "440/432 POLYPHONY"),
            ("UNIT-05", "0x1F22", "SILENCE STRIKE"),
            ("UNIT-06", "0x01A7", "IDENTITY DRIFT"),
        ]
        active_row = int(now_ts * 1.5) % 6
        for idx, (unit, reg, desc) in enumerate(echoes):
            ry = 48 + idx * 17
            if idx == active_row:
                draw.rectangle([18, ry, CRT_W - 18, ry + 15], fill=(16, 48, 22, 250), outline=(80, 255, 110, 245))
                col = (255, 215, 70, 255)
            else:
                draw.rectangle([18, ry, CRT_W - 18, ry + 15], fill=(5, 20, 8, 246))
                col = (70, 240, 95, 255)
            draw.text((22, ry + 2), f"{unit} [{reg}] {desc}", fill=col, font=FONT_CRT_8)

        draw.rectangle([18, 152, CRT_W - 18, 190], fill=(4, 16, 7, 115), outline=(255, 185, 30, 245))
        draw.text((22, 155), "6-WAY XOR PARITY (UNITS 01..06):", fill=fg_amber, font=FONT_CRT_8)
        draw.text((22, 167), "=> FRAGMENT ALPHA: [ 0x1983 ]", fill=(110, 255, 130, 255), font=FONT_CRT_9)
        draw.text((22, 179), "UNIT-07 ROOT ADDRESS VERIFIED", fill=fg_amber, font=FONT_CRT_8)

    elif mode == "FRACTAL_RADAR":
        cx, cy, r = 68, 114, 45
        for ring_r in (15, 30, 45):
            draw.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r], outline=(40, 165, 65, 235), width=1)
        draw.line([(cx - r, cy), (cx + r, cy)], fill=(35, 145, 55, 210), width=1)
        draw.line([(cx, cy - r), (cx, cy + r)], fill=(35, 145, 55, 210), width=1)

        ang = now_ts * 1.6
        sx, sy = int(cx + r * math.cos(ang)), int(cy + r * math.sin(ang))
        draw.line([(cx, cy), (sx, sy)], fill=(95, 255, 120, 255), width=2)

        nodes_polar = [(-26, -16, "NV"), (28, -10, "TYO"), (18, -26, "DMZ"), (-14, 24, "DF")]
        for nx, ny, lbl in nodes_polar:
            bx, by = cx + nx, cy + ny
            draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 195, 35, 255))
            draw.text((bx + 5, by - 4), lbl, fill=fg_amber, font=FONT_CRT_8)

        # Opaque table on right (A=248) so the wave stays on the radar side
        draw.rectangle([122, 50, CRT_W - 18, 168], fill=(6, 22, 9, 248), outline=(55, 195, 75, 240))
        drifts = [
            "FRACTAL MARCUS",
            "#01 NV :+0.1810",
            "#02 TYO:+0.2420",
            "#03 DMZ:+0.4480",
            "#04 DF :+0.5491",
            "---------------",
            "SUM*10 :14.2001",
        ]
        for idx, line in enumerate(drifts):
            col = fg_amber if idx in (0, 6) else fg_green
            draw.text((126, 54 + idx * 15), line, fill=col, font=FONT_CRT_8)

        draw.rectangle([18, 171, CRT_W - 18, 190], fill=(16, 36, 18, 248), outline=fg_amber)
        draw.text((22, 175), "FRAGMENT BETA: 7SIGMA-MARCUS", fill=fg_amber, font=FONT_CRT_9)

    elif mode == "OUROBOROS_TORUS":
        cx, cy = CRT_W // 2, 104
        t_vals = np.linspace(0, 2 * math.pi, 84, endpoint=False)
        rot = now_ts * 1.1
        pts_outer = []
        pts_inner = []
        for t in t_vals:
            x0 = math.cos(t)
            y0 = math.sin(2 * t) * 0.55
            z0 = math.sin(t) * 0.35
            xr = x0 * math.cos(rot * 0.35) - z0 * math.sin(rot * 0.35)
            zr = x0 * math.sin(rot * 0.35) + z0 * math.cos(rot * 0.35)
            scale = 1.0 / (1.35 - 0.25 * zr)
            pts_outer.append((int(cx + xr * 72 * scale), int(cy + y0 * 48 * scale)))
            pts_inner.append((int(cx + xr * 52 * scale), int(cy + y0 * 33 * scale)))

        for i in range(len(pts_outer)):
            nxt = (i + 1) % len(pts_outer)
            draw.line([pts_outer[i], pts_outer[nxt]], fill=(75, 255, 105, 255), width=2)
            draw.line([pts_inner[i], pts_inner[nxt]], fill=(255, 185, 35, 245), width=1)
            if i % 6 == 0:
                draw.line([pts_outer[i], pts_inner[i]], fill=(60, 210, 85, 210), width=1)

        p_idx = int(now_ts * 18) % len(pts_outer)
        px, py = pts_outer[p_idx]
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 235, 120, 255))

        draw.text((20, 50), "1983 [0x1983]", fill=fg_green, font=FONT_CRT_8)
        draw.text((CRT_W - 92, 50), "2025 [0x2025]", fill=fg_amber, font=FONT_CRT_8)

        draw.rectangle([18, 154, CRT_W - 18, 190], fill=(22, 10, 4, 248), outline=fg_amber)
        draw.text((22, 157), "Q-LINK: 0x2025 ^ 0x1983 = 0x09A6", fill=fg_amber, font=FONT_CRT_8)
        draw.text((22, 168), "GAMMA : QLINK-09A6-HEAVY", fill=(115, 255, 135, 255), font=FONT_CRT_9)
        draw.text((22, 180), "SHEDDING 'THE HEAVY' -> NOVA-CHAN", fill=fg_amber, font=FONT_CRT_8)

    elif mode == "MORSE_DECODER":
        draw.rectangle([18, 50, CRT_W - 18, 88], fill=(5, 22, 8, 248), outline=(55, 200, 75, 240))
        draw.text((22, 53), state["crt_sub"][:29], fill=fg_amber, font=FONT_CRT_9)
        morse_str = state["crt_body"]
        offset = int(now_ts * 4) % max(1, len(morse_str))
        rotated_morse = (morse_str + "   " + morse_str)[offset:]
        cx = 22
        for ch in rotated_morse:
            if cx >= CRT_W - 26:
                break
            if ch == ".":
                draw.rectangle([cx, 70, cx + 5, 80], fill=(75, 255, 95, 255))
                cx += 9
            elif ch == "-":
                draw.rectangle([cx, 70, cx + 13, 80], fill=(255, 185, 30, 255))
                cx += 17
            else:
                cx += 7

        draw.rectangle([18, 92, CRT_W - 18, 152], fill=(4, 16, 7, 245), outline=(40, 155, 55, 220))
        verts = [(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
        edges = [(0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (4, 3), (3, 5), (5, 2)]
        ay, ax = now_ts * 1.3, now_ts * 0.8
        pts = []
        for vx, vy, vz in verts:
            x1 = vx * math.cos(ay) - vz * math.sin(ay)
            z1 = vx * math.sin(ay) + vz * math.cos(ay)
            y2 = vy * math.cos(ax) - z1 * math.sin(ax)
            pts.append((int(52 + x1 * 21), int(122 + y2 * 19)))
        for i, j in edges:
            draw.line([pts[i], pts[j]], fill=(75, 255, 100, 255), width=1)

        draw.text((88, 97), "CW DEMOD: LOCKED", fill=fg_green, font=FONT_CRT_8)
        draw.text((88, 111), "FEISTEL : 0x3A5F", fill=fg_amber, font=FONT_CRT_8)
        draw.text((88, 125), "ROOT HEX: 0x1983", fill=fg_green, font=FONT_CRT_8)
        draw.text((88, 139), "7SIGMA  : ACTIVE", fill=fg_amber, font=FONT_CRT_8)

        draw.rectangle([18, 155, CRT_W - 18, 190], fill=(2, 10, 4, 85), outline=(45, 180, 65, 230))
        draw.text((22, 157), "LIVE 750 HZ CW WAVEFORM", fill=(55, 210, 75, 220), font=FONT_CRT_8)

    else:
        # Full-screen TRANSLATOR, NUMBERS_CIPHER, or LAB_DOSSIER Teleprinter (A=248 inside text box)
        # + Dedicated Live 30fps Audio Waveform Window below (y=154..190, A=80)!
        draw.rectangle([18, 50, CRT_W - 18, 151], fill=(5, 20, 8, 248), outline=(55, 205, 75, 240))
        draw.rectangle([19, 51, CRT_W - 19, 66], fill=(16, 46, 20, 252))
        draw.text((23, 53), state["crt_sub"][:29], fill=fg_amber, font=FONT_CRT_9)

        wrapped = textwrap.wrap(state["crt_body"], width=30)[:6]
        for idx, line in enumerate(wrapped):
            if idx == len(wrapped) - 1 and (int(now_ts * 2) % 2 == 0):
                line = line[:28] + " \u2588"
            draw.text((23, 70 + idx * 13), line, fill=fg_bright, font=FONT_CRT_9)

        draw.rectangle([18, 154, CRT_W - 18, 190], fill=(2, 10, 4, 80), outline=(45, 180, 65, 230))
        draw.text((22, 156), "LIVE 14.2001 HZ AUDIO SPECTRUM", fill=(55, 210, 75, 220), font=FONT_CRT_8)

    # Draw top & bottom full-screen CRT telemetry chrome (A=255)
    _draw_crt_chrome(draw, state, relay, now_ts, is_warn)

    # Apply 3D perspective warp, curved CRT superellipse mask, scanlines, and bezel rim reflection
    geom = _get_crt_geometry()
    v_arr = np.asarray(virt, dtype=np.float32)
    warped_rgb = v_arr[geom["src_v"], geom["src_u"], :3]
    warped_a = v_arr[geom["src_v"], geom["src_u"], 3]

    rim = geom["rim_glow"]
    base_glass = np.zeros((CRT_H, CRT_W, 3), dtype=np.float32)
    base_glass[:, :, 0] = 3.0 + rim * 115.0 + geom["sheen"] * 0.6
    base_glass[:, :, 1] = 11.0 + rim * 54.0 + geom["sheen"] * 1.1
    base_glass[:, :, 2] = 5.0 + rim * 14.0 + geom["sheen"] * 0.7

    out_rgb = np.clip(base_glass + warped_rgb * geom["scan"] * geom["vig"] * 1.12, 0, 255).astype(np.uint8)

    # Outside `wave_window`, alpha is 255 (100% opaque inside the CRT glass so baked static text is erased).
    # Inside `wave_window`, alpha uses `warped_a` (so opaque text boxes stay crisp at A=248 while dark
    # oscilloscope/portrait regions drop to A=80..135 to let FFmpeg's live 30fps `showwaves` shine through!).
    blended_alpha = (1.0 - geom["wave_window"]) * 255.0 + geom["wave_window"] * warped_a
    final_alpha = (blended_alpha * geom["edge_alpha"]).astype(np.uint8)

    return Image.fromarray(np.dstack([out_rgb, final_alpha]))


def render_room_hardware_animations(
    draw: ImageDraw.ImageDraw,
    state: dict,
    now_ts: float,
    is_warn: bool,
) -> None:
    """
    Animates the physical studio hardware surrounding the CRT monitor at exact sub-pixel
    coordinates mapped from `backdrop_clean.png`:
      1. Left-rack dual-row LED peak meter (`y=211..215` & `y=220..224`, `x=3..50`)
         + 5 amber channel button lamps (`y=251..255`, `x=2..43`)
      2. Left-rack analog VU meter needle (`pivot=(10, 361)`, sweeping `y=342..354`)
      3. Right-rack status LED matrix (`y=271..281`, `x=745..784`), red warning lamp (`x=723..727, y=326..330`),
         & dual analog VU needles (`pivots=(750, 336)` and `(778, 336)`)
      4. Broadcast Tech CRT monitor lower-right bezel power LED (`x=578..582, y=413..417`)
    """
    # 1. Left-rack dual-row horizontal LED peak meter (8 physical segments at x = 3, 10, 17, 24, 30, 37, 44, 50)
    led_xs = [3, 10, 17, 24, 30, 37, 44, 50]
    level_l = int(4 + 3.8 * abs(math.sin(now_ts * 3.1 + 0.4)))
    level_r = int(4 + 3.8 * abs(math.cos(now_ts * 2.7 + 1.1)))
    if is_warn:
        level_l = max(level_l, 6)
        level_r = max(level_r, 7)

    for seg, lx in enumerate(led_xs):
        if seg < 4:
            on_col = (95, 255, 95, 210)
        elif seg < 6:
            on_col = (255, 210, 50, 220)
        else:
            on_col = (255, 70, 40, 235)
        off_col = (12, 20, 12, 115)
        draw.rectangle([lx, 211, lx + 4, 215], fill=on_col if seg <= level_l else off_col)
        draw.rectangle([lx, 220, lx + 4, 224], fill=on_col if seg <= level_r else off_col)

    # Left-rack 5 amber channel selector lamps (`y=251..255`)
    active_ch = int(now_ts * 0.8) % 5
    for c_idx, cx in enumerate([2, 13, 23, 33, 43]):
        if c_idx == active_ch:
            draw.rectangle([cx, 251, cx + 4, 255], fill=(255, 220, 90, 220))

    # 2. Left-rack analog VU meter needle (`x=0..22, y=338..363`)
    vu_ang = -0.48 + 0.92 * abs(math.sin(now_ts * 2.3))
    piv_x, piv_y = 10, 360
    tip_x = int(piv_x + 15 * math.sin(vu_ang))
    tip_y = int(piv_y - 15 * math.cos(vu_ang))
    draw.line([(piv_x, piv_y), (tip_x, tip_y)], fill=(210, 75, 25, 215), width=2)

    # 3. Right-rack status LED cluster (`y=271..281`, `x=745..784`)
    r_leds = [
        (745, 271, False),
        (760, 271, True),
        (765, 271, False),
        (777, 271, False),
        (782, 271, False),
        (745, 277, False),
        (755, 277, False),
        (765, 277, False),
        (777, 277, False),
        (782, 277, False),
    ]
    for idx, (rx, ry, is_red_led) in enumerate(r_leds):
        blink = ((int(now_ts * 2.5) + idx) % 3) != 0
        if is_red_led:
            col = (255, 75, 30, 235) if (is_warn or blink) else (90, 30, 15, 110)
        else:
            col = (110, 255, 80, 215) if blink else (25, 55, 20, 120)
        draw.ellipse([rx, ry, rx + 4, ry + 4], fill=col)

    # Right-rack red fault lamp at `(723, 326)`
    if is_warn and (int(now_ts * 3) % 2 == 0):
        draw.ellipse([722, 325, 728, 331], fill=(255, 65, 30, 235))

    # Right-rack dual analog VU meter needles (`pivots=(750, 336)` and `(778, 336)`)
    for m_idx, m_piv_x in enumerate((750, 778)):
        m_piv_y = 336
        m_ang = -0.45 + 0.85 * abs(math.sin(now_ts * 2.9 + m_idx * 0.8))
        mx = int(m_piv_x + 10 * math.sin(m_ang))
        my = int(m_piv_y - 10 * math.cos(m_ang))
        draw.line([(m_piv_x, m_piv_y), (mx, my)], fill=(215, 85, 25, 215), width=1)

    # 4. Broadcast Tech CRT Monitor Bezel Power LED (`x=578..582, y=413..417`)
    pwr_col = (255, 175, 25, 255) if (is_warn and int(now_ts * 2) % 2 == 0) else (90, 255, 100, 255)
    draw.ellipse([578, 413, 582, 417], fill=pwr_col)


def render_bottom_engineering_console(
    draw: ImageDraw.ImageDraw,
    state: dict,
    snap_meta: dict,
    now_ts: float,
) -> None:
    """
    Renders the 3-Module Sublevel B2 Broadcast Engineering Console (`x=28..932, y=462..532`, `904x70`):
      - Bay 1 (Left `x=28..222`): Playhead Progress Bar, Timer, Cycle #, & Active Regional Node
      - Bay 2 (Center `x=226..750`): Scanlined Phosphor Teleprinter with Mode Badge, Translation/Clue, & URL
      - Bay 3 (Right `x=754..932`): Sector `[1][2][3][4][5][6][Ω]` Target Matrix & Ephemeral Beacon Key
    """
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN"
    border_col = (255, 176, 20, 240) if is_warn else (55, 245, 78, 235)
    dim_border = (160, 105, 15, 200) if is_warn else (32, 145, 48, 200)
    bg_col = (14, 8, 3, 236) if is_warn else (3, 13, 5, 236)
    hdr_bg = (34, 18, 5, 248) if is_warn else (8, 32, 13, 248)

    c_main = (255, 198, 45, 255) if is_warn else (82, 255, 105, 255)
    c_bright = (255, 238, 170, 255) if is_warn else (195, 255, 205, 255)
    c_sub = (255, 172, 25, 250) if is_warn else (58, 228, 82, 250)

    X0, Y0, X1, Y1 = 28, 462, 932, 532

    # Outer soft phosphor bloom
    draw.rectangle([X0 - 2, Y0 - 2, X1 + 2, Y1 + 2], outline=(border_col[0], border_col[1], border_col[2], 70), width=2)
    # Main console chassis
    draw.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)

    # Subtle horizontal CRT scanlines across the console
    scan_col = (22, 12, 4, 242) if is_warn else (5, 20, 8, 242)
    for sy in range(Y0 + 3, Y1 - 2, 3):
        draw.line([(X0 + 2, sy), (X1 - 2, sy)], fill=scan_col, width=1)

    # Vertical bay dividers (`x=224` and `x=752`)
    draw.line([(224, Y0 + 2), (224, Y1 - 2)], fill=border_col, width=2)
    draw.line([(752, Y0 + 2), (752, Y1 - 2)], fill=border_col, width=2)

    # --- BAY 1 (LEFT `x=28..224`): PLAYHEAD & RELAY LOCK ---
    draw.rectangle([X0 + 2, Y0 + 2, 222, Y0 + 18], fill=hdr_bg)
    cyc = snap_meta.get("cycle", 1)
    p_idx = snap_meta.get("playlist_index", 1)
    draw.text((X0 + 8, Y0 + 4), f"CYCLE #{cyc:02d} // TRK #{p_idx:04d}", fill=c_main, font=FONT_HUD_9)

    offset_s = int(snap_meta.get("track_offset_sec", 0))
    dur_s = max(1, int(snap_meta.get("track_duration_sec", 180)))
    prog = max(0.0, min(1.0, offset_s / dur_s))
    bar_x0, bar_y0, bar_w, bar_h = X0 + 8, Y0 + 23, 104, 10
    draw.rectangle([bar_x0, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h], fill=(4, 10, 5, 255), outline=dim_border)
    fill_w = max(2, int((bar_w - 2) * prog))
    draw.rectangle([bar_x0 + 1, bar_y0 + 1, bar_x0 + 1 + fill_w, bar_y0 + bar_h - 1], fill=c_main)
    t_str = f"{offset_s // 60:02d}:{offset_s % 60:02d}/{dur_s // 60:02d}:{dur_s % 60:02d}"
    draw.text((bar_x0 + bar_w + 6, Y0 + 22), t_str, fill=c_bright, font=FONT_HUD_9)

    relay = snap_meta.get("relay", REGIONAL_RELAYS[0])
    draw.text((X0 + 8, Y0 + 38), f"RELAY: #{relay['node']:02d} {relay['code']} ({relay['freq_khz']}K)", fill=c_sub, font=FONT_HUD_9)
    draw.text((X0 + 8, Y0 + 52), state.get("phase_label", "14.2001 HZ LOCKED")[:26], fill=c_main, font=FONT_HUD_9)

    # --- BAY 2 (CENTER `x=226..750`): PRIMARY TELEPRINTER & TRANSLATION / CLUE FEED ---
    draw.rectangle([226, Y0 + 2, 750, Y0 + 18], fill=hdr_bg)
    badge = "[! INTERCEPT DECODE]" if is_warn else "[14.2001 HZ NOMINAL]"
    draw.text((232, Y0 + 4), f"{badge} {state['line1'][:58]}", fill=c_main, font=FONT_HUD_9)
    draw.text((232, Y0 + 22), state["line2"][:76], fill=c_bright, font=FONT_HUD_10)
    draw.text((232, Y0 + 40), state["line3"][:76], fill=c_sub, font=FONT_HUD_10)
    draw.text((232, Y0 + 55), "PORTAL: stardust-archive.net/forensics/ // SIGNAL LAB: /forensics/signal_lab.html", fill=c_main, font=FONT_HUD_9)

    # --- BAY 3 (RIGHT `x=754..932`): SECTOR MATRIX & EPHEMERAL BEACON ---
    draw.rectangle([754, Y0 + 2, X1 - 2, Y0 + 18], fill=hdr_bg)
    draw.text((760, Y0 + 4), "SECTOR TARGET MATRIX", fill=c_main, font=FONT_HUD_9)

    target_sec = int(state.get("target_sector", 7))
    sec_labels = ["1", "2", "3", "4", "5", "6", "\u03a9"]
    for s_idx, s_lbl in enumerate(sec_labels, start=1):
        sx = 760 + (s_idx - 1) * 23
        sy = Y0 + 22
        is_active_sec = s_idx == target_sec
        s_bg = (255, 185, 25, 255) if is_active_sec else (8, 26, 12, 230)
        s_fg = (10, 10, 5, 255) if is_active_sec else (65, 215, 85, 230)
        s_out = (255, 225, 110, 255) if is_active_sec else dim_border
        draw.rectangle([sx, sy, sx + 19, sy + 14], fill=s_bg, outline=s_out)
        draw.text((sx + 6, sy + 1), s_lbl, fill=s_fg, font=FONT_HUD_9)

    beacon_key = snap_meta.get("ephemeral_beacon_key", "B2-142001FA")
    draw.text((760, Y0 + 40), f"KEY: {beacon_key[:17]}", fill=c_bright, font=FONT_HUD_9)
    draw.text((760, Y0 + 53), "FOLD: OUROBOROS-FOLD", fill=c_sub, font=FONT_HUD_9)


def render_full_arg_overlay_png(
    out_path: Path,
    state: dict,
    assets_dir: Path,
    now_ts: float,
    snap_meta: dict | None = None,
) -> bytes:
    """
    Renders the complete `960x540` RGBA PNG overlay containing:
      1. Full-Screen 3D Perspective Curved CRT Monitor (`246x234` at `x=342, y=142`)
      2. Diegetic Control Room Hardware Animations (rack LEDs, VU needles, power LED)
      3. 3-Module Broadcast Engineering Console (`x=28..932, y=462..532`)
    Written atomically via `os.replace` and returned as raw PNG bytes for `image2pipe`.
    """
    if snap_meta is None:
        relay = REGIONAL_RELAYS[int(now_ts // 300) % len(REGIONAL_RELAYS)]
        window_slot = int(now_ts // 600)
        b_hash = hashlib.sha256(f"stardust-14.2hz|{window_slot}|{relay['code']}".encode()).hexdigest()[:10].upper()
        snap_meta = {
            "cycle": int(max(36900.0, now_ts - BROADCAST_EPOCH) // CYCLE_DURATION_SEC) + 1,
            "playlist_index": 1,
            "track_offset_sec": 45.0,
            "track_duration_sec": 180.0,
            "relay": relay,
            "ephemeral_beacon_key": f"B2-{b_hash}",
        }
    else:
        relay = snap_meta.get("relay", REGIONAL_RELAYS[0])

    canvas = Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))

    # 1. Paste Full-Screen Curved 3D CRT Monitor Patch
    crt_patch = render_crt_window_patch(state, relay, assets_dir, now_ts)
    canvas.paste(crt_patch, (CRT_X, CRT_Y))

    # 2. Draw Diegetic Control Room Hardware Animations & 3-Module Console
    draw = ImageDraw.Draw(canvas)
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN"
    render_room_hardware_animations(draw, state, now_ts, is_warn)
    render_bottom_engineering_console(draw, state, snap_meta, now_ts)

    buf = io.BytesIO()
    canvas.save(buf, format="PNG", compress_level=1)
    png_bytes = buf.getvalue()
    tmp_path = out_path.with_suffix(".tmp.png")
    tmp_path.write_bytes(png_bytes)
    os.replace(tmp_path, out_path)
    return png_bytes


def classify_track(filepath: str) -> dict:
    p = Path(filepath)
    stem = p.stem
    parent = p.parent.name
    if "radio_master_songs" in filepath or stem.startswith("radio_"):
        kind = "vocal_song"
        clean = re.sub(r"_1$", "", re.sub(r"^radio_(?:\d+_)?", "", stem)).replace("_", " ").title()
    elif "numbers_stations" in filepath or stem.startswith("station_"):
        kind = "numbers_station"
        clean = f"NUMBERS INTERCEPT // {stem.upper()}"
    elif "classified_lab_tapes" in filepath or "marcus" in stem:
        kind = "classified_lab_tape"
        clean = f"SUBLEVEL B2 DICTAPHONE // {stem.upper()}"
    elif "morse_beacons" in filepath or "morse" in stem:
        kind = "morse_beacon"
        clean = f"750 HZ MORSE TELEMETRY // {stem.upper()}"
    elif "multilingual_bulletins" in filepath:
        kind = "multilingual_bulletin"
        clean = f"SHORTWAVE BULLETIN // {stem.upper()}"
    elif "midi_masters" in filepath or stem.startswith("midi_"):
        kind = "fm_synth_bumper"
        clean = f"FM SYNTH BUMPER // {stem.replace('midi_', '').replace('_', ' ').upper()}"
    else:
        kind = "arg_intercept"
        clean = f"DEEP SHORTWAVE INTERCEPT // {stem.upper()}"
    return {"filename": p.name, "stem": stem, "category": parent, "kind": kind, "display_title": clean}


def parse_stream_log(log_path: Path, now_ts: float) -> dict:
    if not log_path.exists():
        return {"is_live": False}
    try:
        mtime = log_path.stat().st_mtime
        is_live = (now_ts - mtime) <= 30.0
        with open(log_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 262144))
            chunk = f.read().decode("utf-8", errors="ignore")
        parts = chunk.split("[STREAM.SH] Selected encoder:")
        tail = parts[-1] if parts else chunk
        times = TIME_RE.findall(tail)
        speeds = SPEED_RE.findall(tail)
        fps_list = FPS_RE.findall(tail)
        drops = DROP_RE.findall(tail)
        bitrates = BITRATE_RE.findall(tail)
        elapsed_sec = 0.0
        if times:
            h, m, s = times[-1]
            elapsed_sec = int(h) * 3600 + int(m) * 60 + float(s)
        return {
            "is_live": is_live,
            "last_log_mtime_age_sec": round(now_ts - mtime, 1),
            "elapsed_sec": round(elapsed_sec, 2),
            "fps": float(fps_list[-1]) if (is_live and fps_list) else 0.0,
            "speed": f"{speeds[-1]}x" if (is_live and speeds) else "0.0x",
            "drop": int(drops[-1]) if drops else 0,
            "bitrate": bitrates[-1] if (is_live and bitrates) else "0.0kbits/s",
        }
    except Exception:
        return {"is_live": False}


def load_playlist(playlist_path: Path) -> list[str]:
    if playlist_path.exists():
        lines = playlist_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        files = []
        for line in lines:
            m = FILE_RE.search(line)
            if m:
                files.append(m.group(1))
        if files:
            return files
    return ["broadcast_archive/radio_master_songs/radio_tape_of_us.mp3"]


_DURATION_CACHE: dict[str, float] | None = None


def get_exact_track_duration(tpath: str, repo_root: Path) -> float:
    global _DURATION_CACHE
    if _DURATION_CACHE is None:
        dur_file = repo_root / "youtube" / "livestream" / "track_durations.json"
        if dur_file.exists():
            try:
                _DURATION_CACHE = json.loads(dur_file.read_text(encoding="utf-8"))
            except Exception:
                _DURATION_CACHE = {}
        else:
            _DURATION_CACHE = {}
    bname = os.path.basename(tpath)
    try:
        sz = os.path.getsize(tpath)
        if sz <= 4096:
            return 0.05
        if bname in _DURATION_CACHE:
            return float(_DURATION_CACHE[bname])
        with open(tpath, "rb") as f:
            hdr = f.read(10)
        if len(hdr) == 10 and hdr[:3] == b"ID3":
            id3_sz = ((hdr[6] & 0x7F) << 21) | ((hdr[7] & 0x7F) << 14) | ((hdr[8] & 0x7F) << 7) | (hdr[9] & 0x7F)
            sz -= id3_sz + 10
        return max(0.05, (sz - 1440) / 24000.0)
    except OSError:
        return 99.0


def build_telemetry_snapshot(repo_root: Path, now_ts: float | None = None, force_offline: bool = False) -> dict:
    now = now_ts if now_ts is not None else time.time()
    playlist_path = repo_root / "youtube" / "livestream" / "playlist.txt"
    log_path = repo_root / "youtube" / "livestream" / "stream.log"

    tracks = load_playlist(playlist_path)
    stream_metrics = parse_stream_log(log_path, now)
    is_live = False if force_offline else bool(stream_metrics.get("is_live", False))

    total_uptime_sec = max(36900.0, now - BROADCAST_EPOCH)
    elapsed_sec = stream_metrics.get("elapsed_sec") or 0.0

    cycle_number = int(total_uptime_sec // CYCLE_DURATION_SEC) + 1
    playhead_index = 0
    track_offset_sec = 0.0
    track_dur_sec = 180.0

    if is_live and elapsed_sec > 0 and tracks:
        accum = 0.0
        for idx, tpath in enumerate(tracks):
            dur = get_exact_track_duration(tpath, repo_root)
            if accum + dur > elapsed_sec:
                playhead_index = idx
                track_offset_sec = elapsed_sec - accum
                track_dur_sec = dur
                break
            accum += dur
        else:
            playhead_index = int(elapsed_sec // 99.0) % len(tracks)

    current_track = classify_track(tracks[playhead_index])
    next_track = classify_track(tracks[(playhead_index + 1) % len(tracks)])
    recipe = CADENCE_RECIPES[playhead_index % len(CADENCE_RECIPES)]
    relay = REGIONAL_RELAYS[int(now // 300) % len(REGIONAL_RELAYS)]

    state = resolve_intentional_state(current_track, track_offset_sec, track_dur_sec, relay)
    carrier_phase_deg = round(((now * 14.2001) % 1.0) * 360.0, 2)
    window_slot = int(now // 600)
    beacon_hash = hashlib.sha256(f"stardust-14.2hz|{window_slot}|{relay['code']}".encode()).hexdigest()[:10].upper()

    ramp = {
        "mode": state["hud_mode"],
        "hud_mode": state["hud_mode"],
        "crt_mode": state["crt_mode"],
        "phase_label": state.get("phase_label", "14.2001 HZ LOCKED"),
        "target_sector": state.get("target_sector", 7),
        "progress": state.get("progress", 0.0),
        "fault_code": state["crt_header"],
        "line1": state["line1"],
        "line2": state["line2"],
        "line3": state["line3"],
        "crt_header": state["crt_header"],
        "crt_sub": state["crt_sub"],
        "crt_body": state["crt_body"],
        "crt_footer": state["crt_footer"],
        "_snap_meta": {
            "cycle": cycle_number,
            "playlist_index": playhead_index + 1,
            "track_offset_sec": round(track_offset_sec, 1),
            "track_duration_sec": round(track_dur_sec, 1),
            "relay": relay,
            "ephemeral_beacon_key": f"B2-{beacon_hash}",
        },
    }

    return {
        "schema": "stardust.live.telemetry.v5",
        "timestamp_utc": datetime.datetime.fromtimestamp(now, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "simulated_1995_utc": datetime.datetime.fromtimestamp(
            788918400 + (now - BROADCAST_EPOCH), tz=datetime.timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stream_health": {
            "is_live": is_live,
            "status": "BROADCASTING_24_7" if is_live else "OFFLINE_EDGE_AUTONOMOUS_FALLBACK",
            "in_universe_status": (
                "PRIMARY YOUTUBE RTMP CARRIER LOCKED"
                if is_live
                else "PRIMARY TRANSMITTER OFFLINE — RUNNING ON CLOUDFLARE EDGE & ARCHIVE BUFFER"
            ),
            "fps": stream_metrics.get("fps", 0.0),
            "speed": stream_metrics.get("speed", "0.0x"),
            "dropped_frames": stream_metrics.get("drop", 0),
            "bitrate": stream_metrics.get("bitrate", "0.0kbits/s"),
            "buffer_seconds": 15.0 if is_live else 0.0,
        },
        "playhead": {
            "mode": "LIVE_RTMP" if is_live else "STANDBY_AT_ROTATED_HEAD",
            "cycle": cycle_number,
            "playlist_index": playhead_index + 1,
            "playlist_total": max(1600, len(tracks)),
            "track_offset_sec": round(track_offset_sec, 1),
            "track_duration_sec": round(track_dur_sec, 1),
            "active_recipe": recipe,
            "current_track": current_track,
            "next_track": next_track,
        },
        "diagnostic_ramp": ramp,
        "carrier_14_2hz": {
            "frequency_hz": 14.2001,
            "phase_degrees": carrier_phase_deg,
            "phase_locked": True,
            "sstv_forensic_window_open": True,
            "ephemeral_beacon_key": f"B2-{beacon_hash}",
        },
        "active_relay": relay,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Stardust Full-Screen CRT & Diegetic Control Room Engine")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out-json", type=Path, default=None)
    parser.add_argument("--out-hud-png", type=Path, default=None)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--daemon", action="store_true")
    args = parser.parse_args()

    out_json = args.out_json or (args.repo_root / "site" / "assets" / "live_telemetry.json")
    out_forensics_json = args.repo_root / "site" / "forensics" / "live_telemetry.json"
    out_hud = args.out_hud_png or (args.repo_root / "youtube" / "livestream" / "live_hud.png")
    assets_dir = args.repo_root / "youtube" / "livestream" / "assets_arg"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_hud.parent.mkdir(parents=True, exist_ok=True)

    while True:
        now = time.time()
        snap = build_telemetry_snapshot(args.repo_root, now_ts=now, force_offline=args.offline)
        payload = json.dumps(snap, indent=2)
        out_json.write_text(payload, encoding="utf-8")
        if out_forensics_json.parent.exists():
            out_forensics_json.write_text(payload, encoding="utf-8")
        render_full_arg_overlay_png(
            out_hud,
            snap["diagnostic_ramp"],
            assets_dir,
            now,
            snap_meta=snap["diagnostic_ramp"].get("_snap_meta"),
        )
        if not args.daemon:
            print(
                f"[SYNC_TELEMETRY v5.0] CRT Mode: {snap['diagnostic_ramp']['crt_mode']} | "
                f"Phase: {snap['diagnostic_ramp']['phase_label']} | "
                f"Track: {snap['playhead']['current_track']['filename']}"
            )
            break
        time.sleep(1.0)


if __name__ == "__main__":
    main()
