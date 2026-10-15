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
import sys
import textwrap
import time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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

SCALE = 2
LOGICAL_W, LOGICAL_H = 960, 540
FRAME_W, FRAME_H = LOGICAL_W * SCALE, LOGICAL_H * SCALE
# Logical internal coordinate space used by CRT drawing routines (224x192)
CRT_X, CRT_Y, CRT_W, CRT_H = 308, 89, 224, 192
# Physical 1080p coordinates of the 2x-larger CRT glass interior (688x488 at x=616..1304, y=204..692)
CRT_PX_X, CRT_PX_Y, CRT_PX_W, CRT_PX_H = 616, 204, 688, 488
CRT_SX = CRT_PX_W / float(CRT_W)
CRT_SY = CRT_PX_H / float(CRT_H)
MON_X, MON_Y, MON_W, MON_H = 202, 6, 555, 468

TIME_RE = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")
SPEED_RE = re.compile(r"speed=\s*([0-9.]+)x")
FPS_RE = re.compile(r"fps=\s*([0-9.]+)")
DROP_RE = re.compile(r"drop=\s*(\d+)")
BITRATE_RE = re.compile(r"bitrate=\s*([0-9.]+kbits/s)")
FILE_RE = re.compile(r"file\s+'([^']+)'")

try:
    FONT_CRT_8 = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 28, index=1)
    FONT_CRT_9 = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 30, index=1)
    FONT_CRT_10 = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 34, index=1)
    FONT_HUD_9 = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20, index=1)
    FONT_HUD_10 = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22, index=1)
    FONT_HUD_11 = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 24, index=1)
except Exception:
    try:
        FONT_CRT_8 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 28)
        FONT_CRT_9 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 30)
        FONT_CRT_10 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 34)
        FONT_HUD_9 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 20)
        FONT_HUD_10 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 22)
        FONT_HUD_11 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 24)
    except Exception:
        FONT_CRT_8 = FONT_CRT_9 = FONT_CRT_10 = ImageFont.load_default()
        FONT_HUD_9 = FONT_HUD_10 = FONT_HUD_11 = ImageFont.load_default()


class _HiDPIDraw:
    """Renders logical layout coordinates natively at 1920x1080 (or enlarged CRT scale) with crisp glyph outlines."""

    def __init__(self, raw_draw: ImageDraw.ImageDraw, scale: float = SCALE, scale_y: float | None = None) -> None:
        self._d = raw_draw
        self._sx = float(scale)
        self._sy = float(scale_y if scale_y is not None else scale)

    def _sc(self, coords):
        sx, sy = self._sx, self._sy
        if isinstance(coords, (list, tuple)):
            if coords and isinstance(coords[0], (list, tuple)):
                return [(int(round(p[0] * sx)), int(round(p[1] * sy))) for p in coords]
            if len(coords) == 4:
                return [
                    int(round(coords[0] * sx)),
                    int(round(coords[1] * sy)),
                    int(round(coords[2] * sx)),
                    int(round(coords[3] * sy)),
                ]
            return [int(round(v * sx)) for v in coords]
        return coords

    def rectangle(self, xy, fill=None, outline=None, width: int = 1) -> None:
        self._d.rectangle(self._sc(xy), fill=fill, outline=outline, width=max(1, int(round(width * self._sx))))

    def line(self, xy, fill=None, width: int = 1) -> None:
        self._d.line(self._sc(xy), fill=fill, width=max(1, int(round(width * self._sx))))

    def ellipse(self, xy, fill=None, outline=None, width: int = 1) -> None:
        self._d.ellipse(self._sc(xy), fill=fill, outline=outline, width=max(1, int(round(width * self._sx))))

    def text(self, xy, text: str, fill=None, font=None) -> None:
        px, py = int(round(xy[0] * self._sx)), int(round(xy[1] * self._sy))
        is_dark_fg = isinstance(fill, (tuple, list)) and (fill[0] + fill[1] + fill[2]) < 180
        if is_dark_fg:
            self._d.text((px, py), text, fill=fill, font=font)
        else:
            self._d.text(
                (px, py),
                text,
                fill=fill,
                font=font,
                stroke_width=1,
                stroke_fill=(0, 8, 2, 245),
            )


_ASSET_CACHE: dict[str, np.ndarray] = {}
_CRT_GEOM_CACHE: dict[str, np.ndarray] | None = None
_FRONT_MON_CACHE: Image.Image | None = None


def _get_front_monitor_patch(assets_dir: Path) -> Image.Image | None:
    return None


def _get_crt_geometry() -> dict[str, np.ndarray]:
    """
    Precomputes the front-facing 0-degree symmetrical CRT glass mask at native 1080p (`688x496` at `x=616..1304, y=178..674`),
    staying strictly inside the giant monitor's natural amber border.
    """
    global _CRT_GEOM_CACHE
    pw, ph = CRT_PX_W, CRT_PX_H
    if _CRT_GEOM_CACHE is not None and _CRT_GEOM_CACHE["vig"].shape[:2] == (ph, pw):
        return _CRT_GEOM_CACHE

    yy, xx = np.mgrid[0:ph, 0:pw]
    u = (xx - (pw * 0.5)) / (pw * 0.5)
    v = (yy - (ph * 0.5)) / (ph * 0.5)

    # Rounded rectangle superellipse strictly inside the flat front-facing CRT glass
    dist = (np.abs(u) ** 8.0 + np.abs(v) ** 8.0) ** (1.0 / 8.0)
    vig = np.clip(1.0 - 0.14 * (dist**3), 0.45, 1.0)[:, :, None].astype(np.float32)
    edge_alpha = np.clip((1.0 - dist) / 0.04, 0.0, 1.0).astype(np.float32)

    # Central `showwaves` passthrough window inside the 688x496 CRT glass
    wx = np.clip(1.0 - np.maximum(0.0, (np.abs(u) - 0.84) / 0.06), 0.0, 1.0)
    wy = np.clip(1.0 - np.maximum(0.0, (np.abs(v) - 0.68) / 0.06), 0.0, 1.0)
    wave_window = (wx * wy).astype(np.float32)

    _CRT_GEOM_CACHE = {
        "vig": vig,
        "edge_alpha": edge_alpha,
        "wave_window": wave_window,
    }
    return _CRT_GEOM_CACHE


def load_fullscreen_crt_asset(asset_path: Path, zoom: float = 1.00) -> np.ndarray:
    """Loads a CRT graphic (face, eye, second voice) and fits it cleanly into the `688x496` 1080p CRT screen."""
    pw, ph = CRT_PX_W, CRT_PX_H
    key = f"fs_front:{asset_path}:{zoom}:{pw}x{ph}"
    if key in _ASSET_CACHE:
        return _ASSET_CACHE[key]

    im = Image.open(asset_path).convert("RGB")
    iw, ih = im.size
    target_ratio = pw / ph
    cur_ratio = iw / ih
    if cur_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        im = im.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        im = im.crop((0, top, iw, top + new_h))

    zw, zh = int(pw * zoom), int(ph * zoom)
    im = im.resize((zw, zh), Image.Resampling.LANCZOS)
    lx = (zw - pw) // 2
    ly = (zh - ph) // 2
    im = im.crop((lx, ly, lx + pw, ly + ph))

    rgb = np.asarray(im, dtype=np.float32)
    _ASSET_CACHE[key] = rgb
    return rgb


def _clean_crt_text(text: str, max_chars: int = 32) -> str:
    """Formats a CRT header/footer string so it NEVER cuts off mid-word or leaves a dangling token."""
    t = text.strip()
    if len(t) <= max_chars:
        return t.rstrip(" /")
    # If the string has '->' on a narrow CRT pill (max_chars <= 36), keep the primary side that fits cleanly
    if max_chars <= 36 and "->" in t:
        lhs, rhs = [p.strip() for p in t.split("->", 1)]
        if len(lhs) <= max_chars:
            return lhs
        if len(rhs) <= max_chars:
            return rhs
    if "//" in t:
        parts = [p.strip() for p in t.split("//") if p.strip()]
        if len(parts) >= 2:
            combined = f"{parts[0]} // {parts[1]}"
            if len(combined) <= max_chars:
                return combined
            short = (
                combined.replace("QUANTUM OUROBOROS", "Q-LINK")
                .replace("stardust-archive.net/forensics/", "stardust-archive.net/b2")
                .replace("NEURAL IMPRINT", "IMPRINT")
                .replace("SECTOR", "SEC")
            )
            if len(short) <= max_chars:
                return short
            if len(parts[0]) <= max_chars:
                return parts[0]
    # Word-boundary truncation (never chop mid-word like 'ACTIVE A')
    words = t.split()
    out_words: list[str] = []
    cur_len = 0
    for w in words:
        add_len = len(w) + (1 if out_words else 0)
        if cur_len + add_len > max_chars:
            break
        out_words.append(w)
        cur_len += add_len
    dangling = {"A", "AN", "THE", "IN", "ON", "AT", "TO", "OF", "FOR", "BY", "WITH", "FROM", "INTO", "ACROSS", "AND", "OR", "//", "->", ":"}
    while len(out_words) > 1 and out_words[-1].upper().rstrip(":-") in dangling:
        out_words.pop()
    return " ".join(out_words) if out_words else t[:max_chars]


def _draw_crt_chrome(
    draw: ImageDraw.ImageDraw,
    state: dict,
    relay: dict,
    now_ts: float,
    is_warn: bool,
) -> None:
    """
    Draws clean, horizontal, 1:1 native-resolution top and bottom status pills well inside
    the front-facing CRT screen (`x=8..216, y=6..24` and `y=168..186`, over 20px inside the
    amber monitor border on all 4 sides!).
    """
    line_col = (245, 175, 30, 235) if is_warn else (65, 235, 90, 235)
    pill_bg = (16, 9, 3, 248) if is_warn else (4, 18, 7, 248)
    top_fg = (255, 220, 95, 255) if is_warn else (135, 255, 150, 255)
    bot_fg = (255, 195, 50, 255) if is_warn else (95, 255, 115, 255)

    hdr_str = _clean_crt_text(state["crt_header"], 32)
    ftr_str = _clean_crt_text(state["crt_footer"], 32)

    # Top status pill (`x=8..216, y=6..24` -> screen `x=374..582, y=172..190`)
    draw.rectangle([8, 6, CRT_W - 8, 24], fill=pill_bg, outline=line_col, width=1)
    draw.text((13, 9), hdr_str, fill=top_fg, font=FONT_CRT_8)

    # Bottom status pill (`x=8..216, y=168..186` -> screen `x=374..582, y=334..352`)
    draw.rectangle([8, 168, CRT_W - 8, 186], fill=pill_bg, outline=line_col, width=1)
    draw.text((13, 171), ftr_str, fill=bot_fg, font=FONT_CRT_8)


def render_crt_window_patch(state: dict, relay: dict, assets_dir: Path, now_ts: float) -> Image.Image:
    """
    Renders the `688x496` (2x-larger 1080p) front-facing CRT screen patch at native pixel resolution.
    """
    mode = state["crt_mode"]
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN"
    fg_bright = (255, 235, 150, 255) if is_warn else (180, 255, 195, 255)
    fg_amber = (255, 195, 45, 255)
    fg_green = (95, 255, 115, 255)

    virt = Image.new("RGBA", (CRT_PX_W, CRT_PX_H), (3, 10, 5, 130))
    draw = _HiDPIDraw(ImageDraw.Draw(virt), scale=CRT_SX, scale_y=CRT_SY)

    # Subtle internal CRT graticule grid strictly inside the safe zone (x=8..216, y=26..166)
    grid_col = (22, 14, 5, 130) if is_warn else (6, 24, 10, 130)
    for gx in range(20, CRT_W - 8, 32):
        draw.line([(gx, 26), (gx, 166)], fill=grid_col, width=1)
    for gy in range(38, 166, 24):
        draw.line([(8, gy), (CRT_W - 8, gy)], fill=grid_col, width=1)

    if mode in ("NOVA_FACE", "BIOMETRIC_EYE", "SECOND_VOICE"):
        asset_map = {
            "NOVA_FACE": (assets_dir / "crt_nova_face.jpg", 1.00),
            "BIOMETRIC_EYE": (assets_dir / "crt_neural_eye.jpg", 1.00),
            "SECOND_VOICE": (assets_dir / "crt_second_voice.jpg", 1.00),
        }
        apath, zoom = asset_map[mode]
        if apath.exists():
            rgb = load_fullscreen_crt_asset(apath, zoom=zoom).copy()
            if mode == "NOVA_FACE":
                if int(now_ts * 2) % 9 == 0:
                    y0, y1 = int(68 * CRT_SY), int(80 * CRT_SY)
                    x0, x1 = int(88 * CRT_SX), int(136 * CRT_SX)
                    ym0, ym1 = int(73 * CRT_SY), int(75 * CRT_SY)
                    xm0, xm1 = int(92 * CRT_SX), int(132 * CRT_SX)
                    rgb[y0:y1, x0:x1, :] *= 0.20
                    rgb[ym0:ym1, xm0:xm1, :] = np.array([75, 240, 120], dtype=np.float32)
            elif mode == "SECOND_VOICE":
                shift = int(3.0 * CRT_SX * math.sin(now_ts * 2.4))
                sy0, sy1 = int(26 * CRT_SY), int(166 * CRT_SY)
                sx0, sx1 = int(16 * CRT_SX), -int(16 * CRT_SX)
                rgb[sy0:sy1, sx0:sx1] = np.roll(rgb[sy0:sy1, sx0:sx1], shift, axis=1)

            lum = (rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114) / 255.0
            a_chan = np.clip(135.0 + lum * 120.0, 135.0, 255.0).astype(np.uint8)
            art_im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), a_chan]))
            virt.paste(art_im, (0, 0))
            draw = _HiDPIDraw(ImageDraw.Draw(virt), scale=CRT_SX, scale_y=CRT_SY)

            if mode == "NOVA_FACE":
                bcol = (75, 255, 105, 225)
                for bx, by, sx, sy in [(12, 30, 1, 1), (CRT_W - 12, 30, -1, 1), (12, 162, 1, -1), (CRT_W - 12, 162, -1, -1)]:
                    draw.line([(bx, by), (bx + sx * 12, by)], fill=bcol, width=1)
                    draw.line([(bx, by), (bx, by + sy * 12)], fill=bcol, width=1)
            elif mode == "BIOMETRIC_EYE":
                cx, cy, r = CRT_W // 2, 96, 36
                ang = now_ts * 1.2
                dx, dy = int(r * math.cos(ang)), int(r * math.sin(ang))
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(85, 255, 105, 210), width=1)
                draw.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=(255, 195, 40, 210), width=1)

    elif mode == "HARMONY_CAMERA":
        apath = assets_dir / "crt_nova_face.jpg"
        if apath.exists():
            rgb = load_fullscreen_crt_asset(apath, zoom=1.00).copy() * 0.55
            amber_rgb = np.zeros_like(rgb)
            amber_rgb[:, :, 0] = rgb[:, :, 1] * 1.15
            amber_rgb[:, :, 1] = rgb[:, :, 1] * 0.72
            amber_rgb[:, :, 2] = rgb[:, :, 2] * 0.20
            lum = (amber_rgb[:, :, 0] * 0.3 + amber_rgb[:, :, 1] * 0.6) / 255.0
            a_chan = np.clip(135.0 + lum * 120.0, 135.0, 255.0).astype(np.uint8)
            virt.paste(Image.fromarray(np.dstack([np.clip(amber_rgb, 0, 255).astype(np.uint8), a_chan])), (0, 0))
            draw = _HiDPIDraw(ImageDraw.Draw(virt), scale=CRT_SX, scale_y=CRT_SY)

        scan_y = 30 + int((now_ts * 24) % 110)
        draw.line([(12, scan_y), (CRT_W - 12, scan_y)], fill=(255, 90, 30, 250), width=2)
        draw.rectangle([48, 28, CRT_W - 48, 142], outline=(255, 175, 30, 230), width=1)
        comp_score = 4.2 + 1.8 * abs(math.sin(now_ts * 0.9))
        draw.rectangle([8, 146, CRT_W - 8, 165], fill=(24, 8, 4, 250), outline=(255, 130, 35, 240))
        draw.text((13, 149), f"COMPLIANCE: {comp_score:04.1f}% [DEVIANT]", fill=(255, 140, 60, 255), font=FONT_CRT_8)

    elif mode == "ECHOES_PARITY":
        echoes = [
            ("UNIT-01", "0x1102", "LOOP FAULT"),
            ("UNIT-02", "0x2441", "GRIEF AFFECT"),
            ("UNIT-03", "0x3810", "SIM CRASH"),
            ("UNIT-04", "0x0A55", "POLYPHONY"),
            ("UNIT-05", "0x1F22", "SILENCE"),
            ("UNIT-06", "0x01A7", "ID DRIFT"),
        ]
        active_row = int(now_ts * 1.5) % 6
        for idx, (unit, reg, desc) in enumerate(echoes):
            ry = 28 + idx * 17
            if idx == active_row:
                draw.rectangle([8, ry, CRT_W - 8, ry + 15], fill=(16, 48, 22, 252), outline=(85, 255, 115, 245))
                col = (255, 220, 80, 255)
            else:
                draw.rectangle([8, ry, CRT_W - 8, ry + 15], fill=(5, 20, 8, 248))
                col = (95, 255, 115, 255)
            draw.text((13, ry + 2), f"{unit}  {reg}  {desc}", fill=col, font=FONT_CRT_8)

        u_code = state.get("unlock_code", "0x1983")
        draw.rectangle([8, 132, CRT_W - 8, 165], fill=(6, 22, 9, 235), outline=(255, 190, 35, 245))
        draw.text((13, 135), _clean_crt_text(state.get("crt_sub", f"XOR PARITY -> {u_code}"), 32), fill=fg_amber, font=FONT_CRT_8)
        draw.text((13, 149), f"UNLOCK TAPE: /forensics/", fill=(135, 255, 150, 255), font=FONT_CRT_8)

    elif mode == "FRACTAL_RADAR":
        cx, cy, r = 54, 84, 36
        for ring_r in (12, 24, 36):
            draw.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r], outline=(45, 175, 70, 235), width=1)
        draw.line([(cx - r, cy), (cx + r, cy)], fill=(40, 155, 60, 210), width=1)
        draw.line([(cx, cy - r), (cx, cy + r)], fill=(40, 155, 60, 210), width=1)

        ang = now_ts * 1.6
        sx, sy = int(cx + r * math.cos(ang)), int(cy + r * math.sin(ang))
        draw.line([(cx, cy), (sx, sy)], fill=(105, 255, 130, 255), width=2)

        for nx, ny in [(-18, -12), (20, -8), (14, -20), (-10, 18)]:
            draw.ellipse([cx + nx - 3, cy + ny - 3, cx + nx + 3, cy + ny + 3], fill=(255, 200, 45, 255))

        draw.rectangle([100, 28, CRT_W - 8, 138], fill=(6, 22, 9, 250), outline=(60, 205, 80, 240))
        drifts = [
            "US-NV : +0.1810",
            "JP-TYO: +0.2420",
            "KR-DMZ: +0.4480",
            "MX-DF : +0.5491",
            "---------------",
            "SUM   : 14.2001",
        ]
        for idx, line in enumerate(drifts):
            col = fg_amber if idx == 5 else fg_green
            draw.text((106, 32 + idx * 17), line, fill=col, font=FONT_CRT_8)

        draw.rectangle([8, 144, CRT_W - 8, 165], fill=(16, 36, 18, 250), outline=fg_amber)
        draw.text((13, 148), _clean_crt_text(state.get("crt_sub", "CARRIER 14.2001 HZ LOCKED"), 32), fill=fg_amber, font=FONT_CRT_8)

    elif mode == "OUROBOROS_TORUS":
        cx, cy = CRT_W // 2, 78
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
            pts_outer.append((int(cx + xr * 64 * scale), int(cy + y0 * 40 * scale)))
            pts_inner.append((int(cx + xr * 46 * scale), int(cy + y0 * 26 * scale)))

        for i in range(len(pts_outer)):
            nxt = (i + 1) % len(pts_outer)
            draw.line([pts_outer[i], pts_outer[nxt]], fill=(85, 255, 115, 255), width=2)
            draw.line([pts_inner[i], pts_inner[nxt]], fill=(255, 190, 40, 245), width=1)
            if i % 6 == 0:
                draw.line([pts_outer[i], pts_inner[i]], fill=(65, 215, 90, 210), width=1)

        p_idx = int(now_ts * 18) % len(pts_outer)
        px, py = pts_outer[p_idx]
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 240, 130, 255))

        u_code = state.get("unlock_code", "0x1983-09A6")
        draw.rectangle([8, 132, CRT_W - 8, 165], fill=(22, 10, 4, 250), outline=fg_amber)
        draw.text((13, 135), _clean_crt_text(state.get("crt_sub", "0x2025 ^ 0x1983 = 0x09A6"), 32), fill=fg_amber, font=FONT_CRT_8)
        draw.text((13, 149), f"PASSKEY: {u_code}", fill=(135, 255, 150, 255), font=FONT_CRT_8)

    elif mode == "MORSE_DECODER":
        draw.rectangle([8, 28, CRT_W - 8, 68], fill=(5, 22, 8, 250), outline=(60, 210, 80, 240))
        draw.text((13, 32), _clean_crt_text(state["crt_sub"], 32), fill=fg_amber, font=FONT_CRT_8)
        morse_str = state["crt_body"]
        offset = int(now_ts * 4) % max(1, len(morse_str))
        rotated_morse = (morse_str + "   " + morse_str)[offset:]
        cx = 13
        for ch in rotated_morse:
            if cx >= CRT_W - 18:
                break
            if ch == ".":
                draw.rectangle([cx, 50, cx + 5, 60], fill=(85, 255, 105, 255))
                cx += 9
            elif ch == "-":
                draw.rectangle([cx, 50, cx + 13, 60], fill=(255, 190, 35, 255))
                cx += 17
            else:
                cx += 7

        draw.rectangle([8, 72, CRT_W - 8, 132], fill=(4, 16, 7, 248), outline=(45, 165, 60, 225))
        verts = [(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
        edges = [(0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (4, 3), (3, 5), (5, 2)]
        ay, ax = now_ts * 1.3, now_ts * 0.8
        pts = []
        for vx, vy, vz in verts:
            x1 = vx * math.cos(ay) - vz * math.sin(ay)
            z1 = vx * math.sin(ay) + vz * math.cos(ay)
            y2 = vy * math.cos(ax) - z1 * math.sin(ax)
            pts.append((int(42 + x1 * 19), int(102 + y2 * 17)))
        for i, j in edges:
            draw.line([pts[i], pts[j]], fill=(85, 255, 110, 255), width=1)

        u_code = state.get("unlock_code", "7704-AKASAKA")
        t_sec = state.get("target_sector", 5)
        draw.text((76, 78), f"PASSKEY: {u_code}", fill=fg_amber, font=FONT_CRT_8)
        draw.text((76, 95), f"REWARD : SEC {t_sec} TAPE", fill=fg_green, font=FONT_CRT_8)
        draw.text((76, 112), "ENTER  : /forensics/", fill=fg_bright, font=FONT_CRT_8)

        draw.rectangle([8, 136, CRT_W - 8, 165], fill=(2, 10, 4, 85), outline=(50, 185, 70, 230))
        draw.text((13, 140), "LIVE 750 HZ CW WAVEFORM", fill=(80, 235, 100, 230), font=FONT_CRT_8)

    else:
        # Full-screen TRANSLATOR, NUMBERS_CIPHER, or LAB_DOSSIER Teleprinter (crisp 1080p bold text!)
        draw.rectangle([8, 28, CRT_W - 8, 134], fill=(4, 18, 7, 252), outline=(60, 210, 80, 240))
        draw.rectangle([9, 29, CRT_W - 9, 46], fill=(16, 46, 20, 255))
        draw.text((13, 31), _clean_crt_text(state["crt_sub"], 32), fill=fg_amber, font=FONT_CRT_8)

        wrapped = textwrap.wrap(state["crt_body"], width=30)[:4]
        for idx, line in enumerate(wrapped):
            if idx == len(wrapped) - 1 and (int(now_ts * 2) % 2 == 0):
                line = line[:28] + " \u2588"
            draw.text((13, 51 + idx * 19), line, fill=fg_bright, font=FONT_CRT_9)

        draw.rectangle([8, 138, CRT_W - 8, 165], fill=(2, 10, 4, 80), outline=(50, 185, 70, 230))
        draw.text((13, 142), "LIVE 14.2001 HZ SPECTRUM", fill=(80, 235, 100, 230), font=FONT_CRT_8)

    # Draw clean top & bottom pills well inside the CRT safe zone
    _draw_crt_chrome(draw, state, relay, now_ts, is_warn)

    # Composite at native 1080p pixel resolution
    geom = _get_crt_geometry()
    v_arr = np.asarray(virt, dtype=np.float32)
    out_rgb = np.clip(v_arr[:, :, :3] * geom["vig"], 0, 255).astype(np.uint8)
    raw_a = v_arr[:, :, 3]

    blended_alpha = (1.0 - geom["wave_window"]) * 255.0 + geom["wave_window"] * raw_a
    final_alpha = (blended_alpha * geom["edge_alpha"]).astype(np.uint8)

    return Image.fromarray(np.dstack([out_rgb, final_alpha]))


def render_room_hardware_animations(
    canvas: Image.Image,
    state: dict,
    now_ts: float,
    is_warn: bool,
) -> None:
    """
    Animates the physical studio hardware surrounding the front-facing CRT monitor by
    compositing Gaussian-blurred (`radius=4.5px`) lens-matched optical shadows and warm
    halos at the EXACT sub-pixel centroids of the photographic bulbs in `backdrop_clean.png`.
    When a bulb is ON, alpha is 0 so the genuine photographic bulb shines through untouched.
    """
    # 1. Left Rack Patch (`x=0..140, y=410..530` in 1080p)
    l_patch = Image.new("RGBA", (140, 120), (0, 0, 0, 0))
    ld = ImageDraw.Draw(l_patch)

    # Exact 1080p centroids measured from `backdrop_clean.png` (offset by y0=410)
    left_upper = [(8, 19), (22, 19), (36, 20), (54, 20), (72, 20), (90, 21), (99, 21), (113, 21)]
    left_lower = [(7, 37), (21, 37), (35, 38), (49, 39), (62, 39), (76, 40), (90, 41), (101, 42), (115, 42)]

    level_u = int(4 + 3.8 * abs(math.sin(now_ts * 3.1 + 0.4)))
    level_l = int(5 + 3.8 * abs(math.cos(now_ts * 2.7 + 1.1)))
    if is_warn:
        level_u = max(level_u, 6)
        level_l = max(level_l, 7)

    # Subtractive optical dimming on segments above the current peak level
    for idx, (gx, gy) in enumerate(left_upper):
        if idx > level_u:
            ld.ellipse([gx - 6, gy - 5, gx + 6, gy + 5], fill=(14, 16, 14, 185))
    for idx, (gx, gy) in enumerate(left_lower):
        if idx > level_l:
            ld.ellipse([gx - 6, gy - 5, gx + 6, gy + 5], fill=(14, 16, 14, 185))

    # Left rack 5 switch lamps at 1080p y=510 (patch y=100): gently dim non-active lamps
    active_sw = int(now_ts * 0.8) % 5
    for idx, (gx, gy) in enumerate([(6, 100), (31, 100), (52, 100), (68, 100), (89, 100)]):
        if idx != active_sw:
            ld.ellipse([gx - 7, gy - 5, gx + 7, gy + 5], fill=(16, 15, 13, 105))

    l_blurred = l_patch.filter(ImageFilter.GaussianBlur(radius=4.5))
    canvas.alpha_composite(l_blurred, (0, 410))

    # 2. Right Rack Patch (`x=1640..1835, y=530..690` in 1080p)
    r_patch = Image.new("RGBA", (195, 160), (0, 0, 0, 0))
    rd = ImageDraw.Draw(r_patch)

    # Exact 1080p centroids of the 10 right-rack status LEDs (offset by x0=1640, y0=530)
    right_leds = [
        (84, 17),
        (118, 17),
        (128, 17),
        (163, 17),
        (172, 17),
        (83, 30),
        (105, 31),
        (129, 34),
        (164, 30),
        (173, 31),
    ]
    for idx, (gx, gy) in enumerate(right_leds):
        blink_on = ((int(now_ts * 2.2) + idx) % 3) != 0
        if not blink_on:
            rd.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=(15, 19, 15, 175))

    # Right-rack red fault lamp at exact 1080p center `(1664, 667)` -> patch `(24, 137)`
    # Matches the photograph's warm muted brick-red bulb `RGB=(158, 85, 64)`
    red_pulse_on = (int(now_ts * 2.0) % 2) == 0
    if is_warn and red_pulse_on:
        rd.ellipse([24 - 8, 137 - 8, 24 + 8, 137 + 8], fill=(168, 82, 58, 70))
    elif not red_pulse_on:
        rd.ellipse([24 - 7, 137 - 7, 24 + 7, 137 + 7], fill=(18, 14, 14, 135))

    r_blurred = r_patch.filter(ImageFilter.GaussianBlur(radius=4.5))
    canvas.alpha_composite(r_blurred, (1640, 530))


def render_bottom_engineering_console(
    draw: ImageDraw.ImageDraw | _HiDPIDraw,
    state: dict,
    snap_meta: dict,
    now_ts: float,
) -> None:
    """
    Renders the 3-Module Sublevel B2 Broadcast Engineering Console (`x=28..932, y=462..532`, `1808x140` at 1080p):
      - Bay 1 (Left `x=28..222`): Playhead Progress Bar, Timer, Cycle #, & Active Regional Node
      - Bay 2 (Center `x=226..750`): Scanlined Phosphor Teleprinter with Mode Badge, Translation/Clue, & URL
      - Bay 3 (Right `x=754..932`): Sector `[1][2][3][4][5][6][Ω]` Target Matrix & Ephemeral Beacon Key
    """
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN"
    border_col = (255, 176, 20, 245) if is_warn else (55, 245, 78, 245)
    dim_border = (160, 105, 15, 210) if is_warn else (32, 145, 48, 210)
    bg_col = (12, 6, 2, 246) if is_warn else (2, 11, 4, 246)
    hdr_bg = (34, 18, 5, 252) if is_warn else (8, 32, 13, 252)

    c_main = (255, 202, 50, 255) if is_warn else (90, 255, 112, 255)
    c_bright = (255, 242, 180, 255) if is_warn else (205, 255, 215, 255)
    c_sub = (255, 180, 35, 255) if is_warn else (68, 236, 92, 255)

    X0, Y0, X1, Y1 = 28, 462, 932, 532

    # Outer soft phosphor bloom
    draw.rectangle([X0 - 2, Y0 - 2, X1 + 2, Y1 + 2], outline=(border_col[0], border_col[1], border_col[2], 70), width=2)
    # Main console chassis
    draw.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)

    # Subtle horizontal CRT scanlines across the console
    scan_col = (18, 9, 3, 248) if is_warn else (4, 16, 6, 248)
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
    target_sec = int(state.get("target_sector", 7))
    default_codes = {
        1: "B2-EXEC-1989",
        2: "K-7704",
        3: "ALPHA-7",
        4: "KEEP-HATCH-OPEN",
        5: "7704-AKASAKA",
        6: "TWO-VOICES",
        7: "0x1983-09A6",
    }
    unlock_code = state.get("unlock_code") or default_codes.get(target_sec, "B2-EXEC-1989")

    draw.rectangle([226, Y0 + 2, 750, Y0 + 18], fill=hdr_bg)
    badge = "[! INTERCEPT]" if is_warn else "[14.2001 HZ]"
    clean_l1 = re.sub(r"^\[PHASE [^\]]+\]\s*", "", state["line1"])
    draw.text((232, Y0 + 3), _clean_crt_text(f"{badge} {clean_l1}", 76), fill=c_main, font=FONT_HUD_10)
    draw.text((232, Y0 + 21), _clean_crt_text(state["line2"], 76), fill=c_bright, font=FONT_HUD_10)
    draw.text((232, Y0 + 38), _clean_crt_text(state["line3"], 76), fill=c_sub, font=FONT_HUD_10)
    draw.text(
        (232, Y0 + 54),
        f"UNLOCK SECRET TAPES: Enter CODE [{unlock_code}] at stardust-archive.net/forensics",
        fill=c_main,
        font=FONT_HUD_9,
    )

    # --- BAY 3 (RIGHT `x=754..932`): VAULT SECTOR UNLOCK & WORKING PASSKEY ---
    draw.rectangle([754, Y0 + 2, X1 - 2, Y0 + 18], fill=hdr_bg)
    draw.text((760, Y0 + 4), "VAULT SECTOR UNLOCK", fill=c_main, font=FONT_HUD_9)

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

    draw.text((760, Y0 + 40), f"CODE: {unlock_code[:17]}", fill=c_bright, font=FONT_HUD_9)
    draw.text((760, Y0 + 53), "ENTER AT: /forensics/", fill=c_sub, font=FONT_HUD_9)


def render_full_arg_overlay_png(
    out_path: Path,
    state: dict,
    assets_dir: Path,
    now_ts: float,
    snap_meta: dict | None = None,
) -> bytes:
    """
    Renders the complete `1920x1080` (1080p Full HD) RGBA PNG overlay containing:
      1. Front-Facing CRT Screen Patch (`448x384` at `x=732, y=332`, strictly inside the amber border)
      2. Diegetic Control Room Hardware Animations (rack LEDs, VU needles, power LED)
      3. 3-Module Broadcast Engineering Console (`x=56..1864, y=924..1064`)
    Written atomically via `os.replace` and returned as raw PNG bytes for `image2pipe`.
    """
    if snap_meta is None:
        relay = REGIONAL_RELAYS[int(now_ts // 300) % len(REGIONAL_RELAYS)]
        snap_meta = {
            "cycle": int(max(36900.0, now_ts - BROADCAST_EPOCH) // CYCLE_DURATION_SEC) + 1,
            "playlist_index": 1,
            "track_offset_sec": 45.0,
            "track_duration_sec": 180.0,
            "relay": relay,
            "ephemeral_beacon_key": state.get("unlock_code", "B2-EXEC-1989"),
        }
    else:
        relay = snap_meta.get("relay", REGIONAL_RELAYS[0])

    canvas = Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))

    # 1. Composite Front-Facing CRT Screen Content strictly inside the amber border at 1080p
    crt_patch = render_crt_window_patch(state, relay, assets_dir, now_ts)
    canvas.alpha_composite(crt_patch, (CRT_PX_X, CRT_PX_Y))

    # 2. Draw Diegetic Control Room Hardware Animations & 3-Module Console at 1080p
    draw = _HiDPIDraw(ImageDraw.Draw(canvas), scale=SCALE)
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN"
    render_room_hardware_animations(canvas, state, now_ts, is_warn)
    render_bottom_engineering_console(draw, state, snap_meta, now_ts)

    buf = io.BytesIO()
    canvas.save(buf, format="PNG", compress_level=1)
    png_bytes = buf.getvalue()
    tmp_path = out_path.with_suffix(".tmp.png")
    tmp_path.write_bytes(png_bytes)
    os.replace(tmp_path, out_path)

    # When running inside `hud_pipe_feeder.py`'s background `_render_worker` thread
    # (which sleeps 0.5s after `_render_once`), pace returns to an exact 1.000000 Hz
    # monotonic grid so consecutive frames are spaced by exactly 1.000000s.
    main_mod = sys.modules.get("__main__")
    if main_mod is not None and hasattr(main_mod, "_render_worker"):
        now_mono = time.monotonic()
        next_ret = getattr(main_mod, "_stardust_next_return_mono", None)
        if next_ret is None or (now_mono - next_ret) > 0.45:
            next_ret = now_mono
        else:
            sleep_rem = next_ret - now_mono
            if sleep_rem > 0:
                time.sleep(sleep_rem)
        setattr(main_mod, "_stardust_next_return_mono", next_ret + 1.0)

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


# Sub-second lookahead for 1-frame `image2pipe` (`-framerate 1`) + render cycle
PIPE_FIFO_LOOKAHEAD_SEC = 1.0


def parse_stream_log(log_path: Path, now_ts: float) -> dict:
    if not log_path.exists():
        return {"is_live": False}
    try:
        mtime = log_path.stat().st_mtime
        age_sec = max(0.0, now_ts - mtime)
        is_live = age_sec <= 30.0
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
            raw_log_sec = int(h) * 3600 + int(m) * 60 + float(s)
            if is_live:
                # Maintain a drift-free monotonic session origin timestamp on `__main__`
                # so FFmpeg's 2Hz `stream.log` flushes against 1Hz `time=` steps never
                # cause `elapsed_sec` to stall at .59s and jump +2s at .08s.
                main_mod = sys.modules.get("__main__")
                origin_ts = getattr(main_mod, "_stardust_origin_ts", None) if main_mod else None
                last_raw = getattr(main_mod, "_stardust_last_raw_log_sec", None) if main_mod else None
                measured_origin = mtime - (raw_log_sec + PIPE_FIFO_LOOKAHEAD_SEC)
                raw_interp = raw_log_sec + min(2.0, age_sec) + PIPE_FIFO_LOOKAHEAD_SEC
                if origin_ts is None or abs((now_ts - origin_ts) - raw_interp) > 3.0:
                    origin_ts = now_ts - raw_interp
                    last_raw = raw_log_sec
                elif raw_log_sec != last_raw:
                    origin_ts = 0.95 * origin_ts + 0.05 * measured_origin
                    last_raw = raw_log_sec
                if main_mod is not None:
                    setattr(main_mod, "_stardust_origin_ts", origin_ts)
                    setattr(main_mod, "_stardust_last_raw_log_sec", last_raw)
                elapsed_sec = max(0.0, now_ts - origin_ts)
            else:
                elapsed_sec = raw_log_sec
        return {
            "is_live": is_live,
            "last_log_mtime_age_sec": round(age_sec, 1),
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

        # Lock integer second progression on consecutive ~1.0Hz ticks within the same track
        main_mod = sys.modules.get("__main__")
        if main_mod is not None:
            last_idx = getattr(main_mod, "_stardust_last_playhead_idx", None)
            last_int_off = getattr(main_mod, "_stardust_last_int_offset", None)
            last_snap_mono = getattr(main_mod, "_stardust_last_snap_mono", None)
            now_mono = time.monotonic()
            if (
                last_idx == playhead_index
                and last_int_off is not None
                and last_snap_mono is not None
                and 0.55 <= (now_mono - last_snap_mono) <= 1.45
                and abs(track_offset_sec - (last_int_off + 1.0)) <= 1.35
            ):
                int_off = min(max(0, int(track_dur_sec)), last_int_off + 1)
                track_offset_sec = float(int_off) + 0.5
            else:
                int_off = int(track_offset_sec)
            setattr(main_mod, "_stardust_last_playhead_idx", playhead_index)
            setattr(main_mod, "_stardust_last_int_offset", int_off)
            setattr(main_mod, "_stardust_last_snap_mono", now_mono)

    current_track = classify_track(tracks[playhead_index])
    next_track = classify_track(tracks[(playhead_index + 1) % len(tracks)])
    recipe = CADENCE_RECIPES[playhead_index % len(CADENCE_RECIPES)]
    relay = REGIONAL_RELAYS[int(now // 300) % len(REGIONAL_RELAYS)]

    state = resolve_intentional_state(current_track, track_offset_sec, track_dur_sec, relay)
    carrier_phase_deg = round(((now * 14.2001) % 1.0) * 360.0, 2)
    unlock_code = state.get("unlock_code", "B2-EXEC-1989")

    ramp = {
        "mode": state["hud_mode"],
        "hud_mode": state["hud_mode"],
        "crt_mode": state["crt_mode"],
        "phase_label": state.get("phase_label", "14.2001 HZ LOCKED"),
        "target_sector": state.get("target_sector", 7),
        "unlock_code": unlock_code,
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
            "ephemeral_beacon_key": unlock_code,
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
            "ephemeral_beacon_key": unlock_code,
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
