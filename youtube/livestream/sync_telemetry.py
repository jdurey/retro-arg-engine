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

import importlib
import arg_broadcast_codex
import song_lore_questions

importlib.reload(arg_broadcast_codex)
importlib.reload(song_lore_questions)
from arg_broadcast_codex import resolve_intentional_state
from song_lore_questions import resolve_song_lore_panel

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

try:
    FONT_SCROLL_UNI = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 18)
    FONT_SCROLL_HDR = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 17, index=1)
    FONT_SCROLL_BODY = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16, index=1)
except Exception:
    FONT_SCROLL_UNI = FONT_HUD_9
    FONT_SCROLL_HDR = FONT_HUD_9
    FONT_SCROLL_BODY = FONT_HUD_9


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

    bg_path = Path(__file__).resolve().parent / "backdrop_clean.png"
    if bg_path.exists():
        bg_im = Image.open(bg_path).convert("RGBA")
        crt_bg_rgba = bg_im.crop((CRT_PX_X, CRT_PX_Y, CRT_PX_X + pw, CRT_PX_Y + ph))
    else:
        crt_bg_rgba = Image.new("RGBA", (pw, ph), (11, 17, 17, 255))

    # Deeply inset, rounded CRT cushion alpha mask so crt_bg_rgba has alpha=0 anywhere near the amber bezel
    u_in = (xx - (pw * 0.5)) / (pw * 0.39)
    v_in = (yy - (ph * 0.5)) / (ph * 0.36)
    d_in = (np.abs(u_in) ** 3.2 + np.abs(v_in) ** 3.2) ** (1.0 / 3.2)
    t_in = np.clip((1.0 - d_in) / 0.32, 0.0, 1.0)
    cushion_f = (t_in * t_in * (3.0 - 2.0 * t_in)).astype(np.float32)
    cushion_alpha = (cushion_f * 255.0).astype(np.uint8)
    crt_bg_rgba.putalpha(Image.fromarray(cushion_alpha, mode="L"))

    # Sub-glass electron-beam scanline & shadow-mask matrix for on-CRT text:
    # Carves horizontal CRT raster lines, vertical phosphor triads, subtle radial tube falloff,
    # and ~66% smoked-glass transmission so text looks emitted from *inside* the monitor tube.
    row_mod = yy % 3
    scan_y = np.where(row_mod == 0, 0.36, np.where(row_mod == 1, 0.98, 0.80)).astype(np.float32)
    grille_x = np.where((xx % 2) == 0, 0.98, 0.86).astype(np.float32)
    tube_falloff = np.clip(1.0 - 0.14 * (u * u + v * v), 0.78, 1.0).astype(np.float32)
    text_subglass_mask = (scan_y * grille_x * tube_falloff * 0.66).astype(np.float32)

    _CRT_GEOM_CACHE = {
        "vig": vig,
        "edge_alpha": edge_alpha,
        "wave_window": wave_window,
        "crt_bg_rgba": crt_bg_rgba,
        "text_subglass_mask": text_subglass_mask,
    }
    return _CRT_GEOM_CACHE


def load_fullscreen_crt_asset(
    asset_path: Path,
    zoom: float = 1.00,
    pan_x: int = 0,
    pan_y: int = 0,
) -> np.ndarray:
    """Loads a CRT graphic or Veo frame and fits it into the `688x488` 1080p CRT screen with dynamic pan & zoom."""
    pw, ph = CRT_PX_W, CRT_PX_H
    base_key = f"base_im:{asset_path}:{pw}x{ph}"
    if base_key in _ASSET_CACHE:
        base_im = _ASSET_CACHE[base_key]
    else:
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
        # Cache a 1.18x overscanned master image so pan/zoom crops are instantaneous
        ow, oh = int(pw * 1.18), int(ph * 1.18)
        base_im = im.resize((ow, oh), Image.Resampling.LANCZOS)
        if len(_ASSET_CACHE) > 240:
            _ASSET_CACHE.clear()
        _ASSET_CACHE[base_key] = base_im

    ow, oh = base_im.size
    eff_zoom = max(1.00, min(1.17, float(zoom)))
    crop_w = int(round(ow / eff_zoom))
    crop_h = int(round(oh / eff_zoom))
    max_dx = max(0, (ow - crop_w) // 2)
    max_dy = max(0, (oh - crop_h) // 2)
    cx = (ow - crop_w) // 2 + max(-max_dx, min(max_dx, int(pan_x)))
    cy = (oh - crop_h) // 2 + max(-max_dy, min(max_dy, int(pan_y)))
    cropped = base_im.crop((cx, cy, cx + crop_w, cy + crop_h)).resize((pw, ph), Image.Resampling.BILINEAR)
    return np.asarray(cropped, dtype=np.float32)


def _get_dynamic_song_crt_rgb(
    assets_dir: Path,
    lore: dict,
    mode: str,
    is_warn: bool,
    now_ts: float,
) -> np.ndarray | None:
    """
    Resolves the live-animated CRT frame for the currently playing song by combining:
      1. Multi-frame Veo animation sequences (`assets_arg/veo_reels/<veo_reel>/frame_XX.jpg`)
      2. Song-specific artwork (`assets_arg/song_thumbs/<thumb_file>`) with continuous Ken Burns pan/zoom
      3. Dynamic CRT scan-wave, RGB chromatic aberration, and phosphor color grading.
    """
    veo_reel = lore.get("veo_reel", "veo_arena_rock_singer")
    thumb_file = lore.get("thumb_file", "")
    reel_dir = assets_dir / "veo_reels" / veo_reel
    thumb_path = (assets_dir / "song_thumbs" / thumb_file) if thumb_file else None

    reel_frames = sorted(reel_dir.glob("frame_*.jpg")) if reel_dir.exists() else []
    cycle_sec = int(now_ts) % 16

    chosen_path: Path | None = None
    if mode == "BIOMETRIC_EYE" and (cycle_sec in (4, 5, 12, 13)):
        chosen_path = assets_dir / "crt_neural_eye.jpg"
    elif mode == "SECOND_VOICE" and (cycle_sec in (6, 7, 14, 15)):
        chosen_path = assets_dir / "crt_second_voice.jpg"
    elif cycle_sec < 11 and reel_frames:
        # Step sequentially through the song's lore-matched Veo video animation!
        chosen_path = reel_frames[int(now_ts) % len(reel_frames)]
    elif thumb_path and thumb_path.exists():
        # Show the song's dedicated artwork with continuous Ken Burns camera motion!
        chosen_path = thumb_path
    elif reel_frames:
        chosen_path = reel_frames[int(now_ts) % len(reel_frames)]
    else:
        chosen_path = assets_dir / "crt_nova_face.jpg"

    if chosen_path is None or not chosen_path.exists():
        return None

    # Continuous camera motion (Ken Burns zoom + orbital pan drift on every tick)
    zoom = 1.07 + 0.05 * math.sin(now_ts * 0.52)
    pan_x = int(26.0 * math.cos(now_ts * 0.41))
    pan_y = int(18.0 * math.sin(now_ts * 0.63))
    rgb = load_fullscreen_crt_asset(chosen_path, zoom=zoom, pan_x=pan_x, pan_y=pan_y).copy()

    # Subtle RGB chromatic aberration & horizontal VHS phase wave
    ab_shift = int(round(2.5 * math.sin(now_ts * 1.9)))
    if ab_shift != 0:
        rgb[:, :, 0] = np.roll(rgb[:, :, 0], ab_shift, axis=1)
        rgb[:, :, 2] = np.roll(rgb[:, :, 2], -ab_shift, axis=1)

    # Rolling CRT vertical refresh bar
    ph = rgb.shape[0]
    bar_y = int((now_ts * 64.0) % ph)
    b0, b1 = max(0, bar_y - 10), min(ph, bar_y + 10)
    rgb[b0:b1, :, :] = np.clip(rgb[b0:b1, :, :] * 1.18 + 14.0, 0.0, 255.0)

    # Diegetic CRT Phosphor Grading (blends 62% vivid Veo RGB with 38% P12 Amber or P31 Green phosphor)
    lum = (rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114)
    if is_warn or mode in ("HARMONY_CAMERA", "SECOND_VOICE"):
        phos = np.zeros_like(rgb)
        phos[:, :, 0] = lum * 1.18
        phos[:, :, 1] = lum * 0.78
        phos[:, :, 2] = lum * 0.24
        rgb = rgb * 0.58 + phos * 0.42
    else:
        phos = np.zeros_like(rgb)
        phos[:, :, 0] = lum * 0.42
        phos[:, :, 1] = lum * 1.15
        phos[:, :, 2] = lum * 0.68
        rgb = rgb * 0.62 + phos * 0.38

    return np.clip(rgb, 0.0, 255.0)


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
    res = " ".join(out_words) if out_words else t[:max_chars]
    if "(" in res and ")" not in res:
        res = res.split("(", 1)[0].strip()
    return res


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


def _apply_crt_subglass_phosphor(text_layer: Image.Image, geom: dict) -> Image.Image:
    """
    Transforms flat digital font glyphs into an authentic sub-glass CRT phosphor emission:
      1. Softens sharp digital vector edges (`GaussianBlur(0.55)`)
      2. Adds wide inner-tube phosphor halation bloom (`GaussianBlur(3.8)`)
      3. Carves horizontal CRT raster scanlines, vertical triad grille, radial tube dimming,
         and ~68% smoked-glass translucency (`geom["text_subglass_mask"]`) so the dark CRT glass
         texture shows through the characters.
    """
    soft_core = text_layer.filter(ImageFilter.GaussianBlur(radius=0.55))
    halo = text_layer.filter(ImageFilter.GaussianBlur(radius=3.8))

    c_arr = np.asarray(soft_core, dtype=np.float32)
    h_arr = np.asarray(halo, dtype=np.float32)
    mask = geom["text_subglass_mask"]

    rgb = np.clip((c_arr[:, :, :3] * 0.90 + h_arr[:, :, :3] * 0.58) * (0.78 + 0.22 * mask[:, :, None]), 0.0, 255.0).astype(np.uint8)
    alpha = np.clip((c_arr[:, :, 3] * 0.92 + h_arr[:, :, 3] * 0.52) * mask, 0.0, 255.0).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb, alpha]))


_CRT_PATCH_CACHE: dict[str, object] = {"key": None, "img": None}


def render_crt_window_patch(
    state: dict,
    relay: dict,
    assets_dir: Path,
    now_ts: float,
    current_track: dict | None = None,
) -> Image.Image:
    """
    Renders the `688x488` (1080p) front-facing CRT screen patch:
      - During interstitials (`kind != 'vocal_song'`): native dark CRT glass (`backdrop_clean.png` crop)
        with sub-glass phosphor text, NO boxes around the text, NO black rectangle border, and NO images of Nova.
      - During vocal songs (`kind == 'vocal_song'`): transparent CRT viewport with sub-glass scanlined
        phosphor text so the 30fps looped 80s CRT computer graphics animation and 30fps `showwaves`
        oscilloscope play smoothly at 30fps.
    """
    is_vocal_song = (current_track or {}).get("kind", "vocal_song") == "vocal_song"
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN"
    cursor_blink = (int(now_ts * 2) % 2) if not is_vocal_song else 0
    cache_key = (
        is_vocal_song,
        is_warn,
        (current_track or {}).get("filename", ""),
        state.get("crt_header", ""),
        state.get("crt_sub", ""),
        state.get("crt_body", ""),
        state.get("crt_footer", ""),
        state.get("target_sector", 1),
        relay.get("code", "US-NV"),
        cursor_blink,
    )
    if _CRT_PATCH_CACHE.get("key") == cache_key and _CRT_PATCH_CACHE.get("img") is not None:
        return _CRT_PATCH_CACHE["img"]  # type: ignore[return-value]

    fg_bright = (235, 190, 100, 235) if is_warn else (102, 232, 120, 235)
    fg_amber = (232, 168, 42, 230)
    fg_green = (78, 222, 96, 230)

    geom = _get_crt_geometry()

    if not is_vocal_song:
        # INTERSTITIAL MODE: Codes and transcript in upper zone (y=18..102),
        # leaving y=106..152 completely open for the 32-band 1980s EQ above the y=158 footer!
        text_layer = Image.new("RGBA", (CRT_PX_W, CRT_PX_H), (0, 0, 0, 0))
        draw = _HiDPIDraw(ImageDraw.Draw(text_layer), scale=CRT_SX, scale_y=CRT_SY)

        hdr_str = _clean_crt_text(state.get("crt_header", "SIGNAL INTERCEPT"), 29)
        sub_str = _clean_crt_text(state.get("crt_sub", "BROADCAST LOG"), 29)
        ftr_str = _clean_crt_text(f"CARRIER: 14.2001 HZ // {relay.get('code', 'US-NV')}", 29)

        draw.text((24, 18), hdr_str, fill=fg_green, font=FONT_CRT_8)
        draw.text((24, 34), sub_str, fill=fg_amber, font=FONT_CRT_8)

        wrapped = textwrap.wrap(state.get("crt_body", ""), width=28)[:4]
        for idx, line in enumerate(wrapped):
            if idx == len(wrapped) - 1 and cursor_blink == 0:
                line = line[:26] + " \u2588"
            draw.text((24, 52 + idx * 13), line, fill=fg_bright, font=FONT_CRT_8)

        draw.text((24, 158), ftr_str, fill=fg_green, font=FONT_CRT_8)
        out_img = _apply_crt_subglass_phosphor(text_layer, geom)
        _CRT_PATCH_CACHE["key"] = cache_key
        _CRT_PATCH_CACHE["img"] = out_img
        return out_img

    # VOCAL SONG MODE: Header & clue in upper zone (y=20..38), 32-band EQ in lower zone (y=106..152),
    # and target sector footer at y=158 so the EQ never covers any text!
    text_layer = Image.new("RGBA", (CRT_PX_W, CRT_PX_H), (0, 0, 0, 0))
    draw = _HiDPIDraw(ImageDraw.Draw(text_layer), scale=CRT_SX, scale_y=CRT_SY)

    lore = resolve_song_lore_panel(current_track or {}, state, now_ts)
    raw_title = lore.get("title", state.get("crt_sub", "NOVA HART")).upper()
    title_str = raw_title.split("(", 1)[0].strip() or raw_title
    hdr_str = _clean_crt_text(f"{title_str} // {state.get('crt_header', '')}", 29)
    clue_str = _clean_crt_text(state.get("crt_body", ""), 29)
    ftr_str = _clean_crt_text(state.get("crt_footer", f"TARGET: SEC #{state.get('target_sector', 1):02d}"), 29)

    top_fg = (232, 180, 70, 230) if is_warn else (88, 226, 106, 230)
    clue_fg = (238, 192, 95, 235) if is_warn else (105, 235, 122, 235)
    bot_fg = (225, 162, 45, 225) if is_warn else (76, 214, 92, 225)
    draw.text((24, 20), hdr_str, fill=top_fg, font=FONT_CRT_8)
    draw.text((24, 38), clue_str, fill=clue_fg, font=FONT_CRT_8)
    draw.text((24, 158), ftr_str, fill=bot_fg, font=FONT_CRT_8)

    out_img = _apply_crt_subglass_phosphor(text_layer, geom)
    _CRT_PATCH_CACHE["key"] = cache_key
    _CRT_PATCH_CACHE["img"] = out_img
    return out_img


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


def _fit_px_logical(txt: str, fnt: ImageFont.FreeTypeFont | ImageFont.ImageFont, max_chars: int, max_logical_px: float) -> str:
    """Guarantees text fits inside `max_logical_px` (where 1 logical unit = 2 physical 1080p pixels) without stripping '->' or clipping mid-word."""
    cleaned = txt.strip()
    if len(cleaned) > max_chars:
        cleaned = cleaned[:max_chars].rsplit(" ", 1)[0].rstrip(":-/ ")
    dangling = {"A", "AN", "THE", "IN", "ON", "AT", "TO", "OF", "FOR", "BY", "WITH", "FROM", "INTO", "AND", "OR", "->", ":"}
    try:
        while len(cleaned) > 8 and (fnt.getlength(cleaned) / 2.0) > max_logical_px:
            if " " in cleaned:
                cleaned = cleaned.rsplit(" ", 1)[0].rstrip(":-/ ")
            else:
                cleaned = cleaned[:-1]
    except Exception:
        pass
    words = cleaned.split()
    while len(words) > 1 and words[-1].upper().rstrip(":-") in dangling:
        words.pop()
    out = " ".join(words) if words else cleaned
    if "[" in out and "]" not in out:
        out = out + "]"
    return out


def _wrap_px_1080p(txt: str, fnt: ImageFont.FreeTypeFont | ImageFont.ImageFont, max_px: float, max_lines: int) -> list[str]:
    """Wraps text at native 1080p pixel width on clean word boundaries and ensures no sentence is ever cut off mid-sentence."""
    cleaned_txt = txt.strip()
    if not cleaned_txt:
        return []

    def _do_wrap(s: str) -> list[str]:
        w_list = s.split()
        if not w_list:
            return []
        out: list[str] = []
        cur_ln = w_list[0]
        for w in w_list[1:]:
            cand = f"{cur_ln} {w}"
            try:
                fits = fnt.getlength(cand) <= max_px
            except Exception:
                fits = len(cand) * 10.2 <= max_px
            if fits:
                cur_ln = cand
            else:
                out.append(cur_ln)
                cur_ln = w
        if cur_ln:
            out.append(cur_ln)
        return out

    all_lines = _do_wrap(cleaned_txt)
    if len(all_lines) <= max_lines:
        return all_lines

    # If the text exceeds max_lines, trim back to the last complete sentence that fits within max_lines
    sentences = [seg.strip() for seg in re.split(r"(?<=[.!?\"”])\s+", cleaned_txt) if seg.strip()]
    if len(sentences) > 1:
        kept: list[str] = []
        for s_part in sentences:
            cand_txt = " ".join(kept + [s_part])
            if len(_do_wrap(cand_txt)) <= max_lines:
                kept.append(s_part)
            else:
                break
        if kept:
            return _do_wrap(" ".join(kept))

    # Fallback for single long stanza/sentence: trim at slash or clause boundary and close cleanly
    if "/" in cleaned_txt:
        clauses = [c.strip() for c in cleaned_txt.split("/") if c.strip()]
        kept_c: list[str] = []
        for c_part in clauses:
            cand_txt = " / ".join(kept_c + [c_part])
            if len(_do_wrap(cand_txt)) <= max_lines:
                kept_c.append(c_part)
            else:
                break
        if kept_c:
            return _do_wrap(" / ".join(kept_c))

    trimmed = all_lines[:max_lines]
    dangling = {"A", "AN", "THE", "IN", "ON", "AT", "TO", "OF", "FOR", "BY", "WITH", "FROM", "INTO", "AND", "OR"}
    if trimmed:
        last_words = trimmed[-1].split()
        while len(last_words) > 1 and last_words[-1].upper().rstrip(":-,;") in dangling:
            last_words.pop()
        last_ln = " ".join(last_words).rstrip(" ,;:-—")
        if last_ln and last_ln[-1] not in ".!?\"”']":
            last_ln += "."
        trimmed[-1] = last_ln
    return trimmed


def render_bottom_engineering_console(
    draw: ImageDraw.ImageDraw | _HiDPIDraw,
    state: dict,
    snap_meta: dict,
    now_ts: float,
) -> None:
    """
    Renders the redesigned 3-Module Sublevel B2/B3 Master Control Engineering Console
    (`x=10..950, y=460..534` logical -> `x=20..1900, y=920..1068` at 1080p, `1880x148` px),
    inspired by Local 58, I Love Bees, Year Zero, and Waking Titan:
      - Bay 1 (Left `x=10..226`): Cycle/Track ID, SMPTE Frame Lock, Progress Bar, Relay Node, & Unclipped Phase Lock
      - Bay 2 (Center `x=228..728`): 4-Line Phosphor Teleprinter with Hijack State Badge, Clue, Cipher, & Dynamic Lab Directive
      - Bay 3 (Right `x=730..950`): Dual-Layer Act I Vault (`1..6, Ω`) + Act II Sublevel B3 Seals (`8..14`) Matrix
    """
    target_sec = int(state.get("target_sector", 7))
    is_b3_breach = target_sec >= 8
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN" or is_b3_breach

    if is_b3_breach:
        border_col = (255, 135, 35, 248)
        dim_border = (175, 85, 20, 215)
        bg_col = (14, 5, 2, 248)
        hdr_bg = (42, 14, 4, 252)
        c_main = (255, 195, 55, 255)
        c_bright = (255, 242, 190, 255)
        c_sub = (120, 255, 140, 255)
    elif is_warn:
        border_col = (255, 176, 20, 245)
        dim_border = (160, 105, 15, 210)
        bg_col = (12, 6, 2, 246)
        hdr_bg = (34, 18, 5, 252)
        c_main = (255, 202, 50, 255)
        c_bright = (255, 242, 180, 255)
        c_sub = (255, 180, 35, 255)
    else:
        border_col = (55, 245, 78, 245)
        dim_border = (32, 145, 48, 210)
        bg_col = (2, 11, 4, 246)
        hdr_bg = (8, 32, 13, 252)
        c_main = (90, 255, 112, 255)
        c_bright = (205, 255, 215, 255)
        c_sub = (68, 236, 92, 255)

    X0, Y0, X1, Y1 = 8, 460, 952, 534

    # Outer soft phosphor bloom + main console chassis
    draw.rectangle([X0 - 2, Y0 - 2, X1 + 2, Y1 + 2], outline=(border_col[0], border_col[1], border_col[2], 70), width=2)
    draw.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)

    # Subtle horizontal CRT scanlines across the console
    scan_col = (18, 9, 3, 248) if is_warn else (4, 16, 6, 248)
    for sy in range(Y0 + 3, Y1 - 2, 3):
        draw.line([(X0 + 2, sy), (X1 - 2, sy)], fill=scan_col, width=1)

    # Vertical bay dividers (`x=234` -> 468px and `x=720` -> 1440px, aligned to the pixel with Left & Right Sidebars!)
    draw.line([(234, Y0 + 2), (234, Y1 - 2)], fill=border_col, width=2)
    draw.line([(720, Y0 + 2), (720, Y1 - 2)], fill=border_col, width=2)

    # --- BAY 1 (LEFT `x=8..234` -> `16..468` px): PLAYHEAD, SMPTE & RELAY LOCK ---
    draw.rectangle([X0 + 2, Y0 + 2, 232, Y0 + 18], fill=hdr_bg)
    cyc = snap_meta.get("cycle", 1)
    p_idx = snap_meta.get("playlist_index", 1)
    draw.text((X0 + 6, Y0 + 3), f"CYCLE #{cyc:02d} // REEL #{p_idx:04d}", fill=c_main, font=FONT_HUD_9)

    offset_s = int(snap_meta.get("track_offset_sec", 0))
    dur_s = max(1, int(snap_meta.get("track_duration_sec", 180)))
    prog = max(0.0, min(1.0, offset_s / dur_s))
    bar_x0, bar_y0, bar_w, bar_h = X0 + 6, Y0 + 23, 120, 10
    draw.rectangle([bar_x0, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h], fill=(4, 10, 5, 255), outline=dim_border)
    fill_w = max(2, int((bar_w - 2) * prog))
    draw.rectangle([bar_x0 + 1, bar_y0 + 1, bar_x0 + 1 + fill_w, bar_y0 + bar_h - 1], fill=c_main)
    t_str = f"{offset_s // 60:02d}:{offset_s % 60:02d}/{dur_s // 60:02d}:{dur_s % 60:02d}"
    draw.text((bar_x0 + bar_w + 6, Y0 + 21), t_str, fill=c_bright, font=FONT_HUD_9)

    relay = snap_meta.get("relay", REGIONAL_RELAYS[0])
    draw.text(
        (X0 + 6, Y0 + 38),
        _fit_px_logical(f"NODE #{relay['node']:02d} {relay['code']} ({relay['freq_khz']}K)", FONT_HUD_9, 34, 216.0),
        fill=c_sub,
        font=FONT_HUD_9,
    )
    raw_phase = state.get("phase_label", "14.2001 HZ LOCKED").replace("VAULT CHALLENGE", "VAULT CIPHER")
    draw.text(
        (X0 + 6, Y0 + 54),
        _fit_px_logical(raw_phase, FONT_HUD_9, 34, 216.0),
        fill=c_main,
        font=FONT_HUD_9,
    )

    # --- BAY 2 (CENTER `x=234..720` -> `468..1440` px): PRIMARY TELEPRINTER & DYNAMIC FORENSIC FEED ---
    draw.rectangle([236, Y0 + 2, 718, Y0 + 18], fill=hdr_bg)
    if is_b3_breach:
        badge = f"[! B3 GATE #{target_sec:02d}]"
    elif is_warn:
        badge = "[! DYAD BLEED]"
    else:
        badge = "[14.2001 HZ]"
    clean_l1 = re.sub(r"^\[PHASE [^\]]+\]\s*", "", state["line1"])
    draw.text((240, Y0 + 3), _fit_px_logical(f"{badge} {clean_l1}", FONT_HUD_10, 72, 474.0), fill=c_main, font=FONT_HUD_10)
    draw.text((240, Y0 + 21), _fit_px_logical(state["line2"], FONT_HUD_10, 72, 474.0), fill=c_bright, font=FONT_HUD_10)
    draw.text((240, Y0 + 38), _fit_px_logical(state["line3"], FONT_HUD_10, 72, 474.0), fill=c_sub, font=FONT_HUD_10)

    # Dynamic Line 4 synced to active puzzle layer & acoustic forensics tools (all <= 76 chars)
    if is_b3_breach:
        b3_directives = {
            8: "ACT II GATE VIII: DECRYPT VIGENERE (KEY: SEVENTH) OR 'BACKMASK 16'",
            9: "ACT II GATE IX: SUM ECHOES 01-06 OR DIAL '1983' IN SIGNAL LAB",
            10: "ACT II GATE X: UNMASK TELEPRINTER (^ 0x55) IN 'LABYRINTH' AT /forensics/",
            11: "ACT II GATE XI: INVERT TWIN-68 M68K ROM IN 'LABYRINTH' AT /forensics/",
            12: "ACT II GATE XII: DIAL '10690' ON AUTOVON KEYPAD (NODE #15 ORBIT)",
            13: "ACT II GATE XIII: SOLVE 7-SIGMA SHAMIR (^ 0x33) AT /forensics/",
            14: "ACT II GATE XIV: SHATTER MÖBIUS CAGE (4-WAY XOR -> 0x0200) AT /forensics/",
        }
        line4_txt = b3_directives.get(target_sec, "ACT II SUBLEVEL B3: TYPE 'LABYRINTH' AT /forensics/ (GATES 8-14)")
    else:
        rot_idx = int(now_ts // 12) % 3
        if rot_idx == 0:
            line4_txt = f"ACT I TARGET (SEC #{target_sec:02d}): ENTER PASSKEY AT stardust-archive.net/forensics/"
        elif rot_idx == 1:
            line4_txt = "SIGNAL LAB: COAGULA, 2600 HZ BLUE-BOX & 7.5 IPS -> /forensics/signal_lab.html"
        else:
            line4_txt = "TWIST WARNING: THE 1983<->2025 LOOP IS A CAGE! TYPE 'LABYRINTH' AT /forensics/"

    draw.text(
        (240, Y0 + 55),
        _fit_px_logical(line4_txt, FONT_HUD_9, 80, 474.0),
        fill=c_main,
        font=FONT_HUD_9,
    )

    # --- BAY 3 (RIGHT `x=720..952` -> `1440..1904` px): DUAL-ROW ACT I VAULT & ACT II B3 SEALS MATRIX ---
    draw.rectangle([722, Y0 + 2, X1 - 2, Y0 + 18], fill=hdr_bg)
    draw.text((726, Y0 + 3), "ACT I VAULT & ACT II SEALS", fill=c_main, font=FONT_HUD_9)

    # Row 1: Act I Sectors [1][2][3][4][5][6][Ω]
    draw.text((726, Y0 + 22), "B2:", fill=c_sub, font=FONT_HUD_9)
    sec_labels = ["1", "2", "3", "4", "5", "6", "\u03a9"]
    for s_idx, s_lbl in enumerate(sec_labels, start=1):
        sx = 762 + (s_idx - 1) * 25
        sy = Y0 + 21
        is_active_sec = target_sec == s_idx
        if is_active_sec:
            s_bg = (255, 195, 30, 255)
            s_fg = (10, 10, 5, 255)
            s_out = (255, 235, 130, 255)
        elif target_sec >= 8:
            s_bg = (14, 46, 20, 235)
            s_fg = (110, 255, 130, 240)
            s_out = (55, 205, 80, 220)
        else:
            s_bg = (8, 24, 11, 230)
            s_fg = (65, 205, 85, 220)
            s_out = dim_border
        draw.rectangle([sx, sy, sx + 21, sy + 14], fill=s_bg, outline=s_out)
        draw.text((sx + 5, sy + 1), s_lbl, fill=s_fg, font=FONT_HUD_9)

    # Row 2: Act II Sublevel B3 Gates [8][9][X][XI][12][13][14]
    draw.text((726, Y0 + 39), "B3:", fill=c_sub, font=FONT_HUD_9)
    gate_labels = ["8", "9", "X", "XI", "12", "13", "14"]
    for g_offset, g_lbl in enumerate(gate_labels):
        g_num = 8 + g_offset
        gx = 762 + g_offset * 25
        gy = Y0 + 38
        is_active_gate = target_sec == g_num
        if is_active_gate:
            g_bg = (255, 120, 30, 255)
            g_fg = (12, 6, 2, 255)
            g_out = (255, 225, 120, 255)
        else:
            g_bg = (18, 10, 4, 230) if is_b3_breach else (6, 18, 8, 215)
            g_fg = (255, 175, 55, 225) if is_b3_breach else (55, 175, 72, 200)
            g_out = dim_border
        draw.rectangle([gx, gy, gx + 21, gy + 14], fill=g_bg, outline=g_out)
        tx_off = 2 if len(g_lbl) == 2 else 5
        draw.text((gx + tx_off, gy + 1), g_lbl, fill=g_fg, font=FONT_HUD_9)

    gate_tag = f"GATE #{target_sec:02d}" if target_sec >= 8 else f"SECTOR #{target_sec:02d}"
    draw.text(
        (726, Y0 + 55),
        _fit_px_logical(f"TARGET: {gate_tag} -> /forensics/", FONT_HUD_9, 34, 216.0),
        fill=c_bright,
        font=FONT_HUD_9,
    )


_SCROLL_SPOOL_CACHE: list[dict] | None = None
_SCROLL_SPOOL_MTIME: float = 0.0


def _get_scroll_spool() -> list[dict]:
    global _SCROLL_SPOOL_CACHE, _SCROLL_SPOOL_MTIME
    spool_path = Path(__file__).resolve().parent / "usenet_youtube_scroll_spool.json"
    try:
        st = spool_path.stat()
        if _SCROLL_SPOOL_CACHE is None or st.st_mtime != _SCROLL_SPOOL_MTIME:
            data = json.loads(spool_path.read_text(encoding="utf-8"))
            _SCROLL_SPOOL_CACHE = data.get("lines", [])
            _SCROLL_SPOOL_MTIME = st.st_mtime
    except Exception:
        if _SCROLL_SPOOL_CACHE is None:
            _SCROLL_SPOOL_CACHE = [{"text": "[USENET SPOOL ONLINE // 14.2001 HZ]", "color": "amber"}]
    return _SCROLL_SPOOL_CACHE


def render_right_usenet_youtube_scroll(
    canvas: Image.Image,
    now_ts: float,
    is_warn: bool,
) -> None:
    """
    Renders the right-side rolling CRT terminal scroll (`x=1440..1904, y=22..904` at 1080p, `464x882` px —
    exact 80px margin from the right inner CRT bevel `x=1360`, matching the Left Sidebar `x=16..468`'s
    80px margin from the left inner CRT bevel `x=548`!).
    """
    lines = _get_scroll_spool()
    if not lines:
        return

    X0, Y0, X1, Y1 = 1440, 22, 1904, 904
    raw_d = ImageDraw.Draw(canvas)

    border_col = (255, 176, 20, 245) if is_warn else (55, 245, 78, 245)
    bg_col = (10, 5, 2, 238) if is_warn else (2, 10, 4, 238)
    hdr_bg = (34, 18, 5, 250) if is_warn else (8, 32, 13, 250)

    # Outer soft bloom + high-contrast phosphor glass frame
    raw_d.rectangle([X0 - 2, Y0 - 2, X1 + 2, Y1 + 2], outline=(border_col[0], border_col[1], border_col[2], 65), width=2)
    raw_d.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)

    # Subtle CRT scanlines across the right scroll terminal
    scan_col = (18, 9, 3, 225) if is_warn else (4, 16, 6, 225)
    for sy in range(Y0 + 56, Y1 - 28, 4):
        raw_d.line([(X0 + 2, sy), (X1 - 2, sy)], fill=scan_col, width=1)

    # Header bar (strictly in-universe, no YouTube reference)
    raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 30], fill=hdr_bg)
    hdr_col = (255, 210, 65, 255) if is_warn else (110, 255, 130, 255)
    raw_d.text(
        (X0 + 10, Y0 + 6),
        "USENET // WORLDNET BBS // LISTENER FEED",
        fill=hdr_col,
        font=FONT_SCROLL_HDR,
        stroke_width=1,
        stroke_fill=(0, 8, 2, 245),
    )

    # Sub-header bar
    raw_d.rectangle([X0 + 2, Y0 + 31, X1 - 2, Y0 + 54], fill=(16, 10, 3, 245) if is_warn else (4, 20, 8, 245))
    raw_d.text(
        (X0 + 10, Y0 + 34),
        "alt.conspiracy + 13 INTL RELAY NODES",
        fill=(255, 195, 55, 255),
        font=FONT_SCROLL_HDR,
        stroke_width=1,
        stroke_fill=(0, 8, 2, 245),
    )

    # Rolling 33-line viewport advancing at 3 lines per second
    total = len(lines)
    visible_rows = 33
    head_idx = (int(now_ts * 3.0)) % total

    palette = {
        "amber": (255, 212, 68, 255),
        "bright": (225, 255, 232, 255) if not is_warn else (255, 244, 195, 255),
        "green": (110, 255, 132, 255) if not is_warn else (255, 205, 75, 255),
        "cyan": (150, 250, 225, 255),
        "dim": (70, 195, 90, 235) if not is_warn else (195, 135, 40, 235),
    }

    y_cursor = Y0 + 60
    line_step = 23
    for r in range(visible_rows):
        item = lines[(head_idx + r) % total]
        txt = item.get("text", "")
        if r == visible_rows - 1 and (int(now_ts * 2) % 2 == 0):
            txt = (txt[:41] + " \u2588") if txt else "\u2588"
        if txt:
            col = palette.get(item.get("color", "green"), palette["green"])
            needs_uni = any(ord(c) > 0x0370 and c not in "\u2588\u2500\u2550\u2192\u2022\u2014\u2013\u2018\u2019\u201c\u201d\u03a9" for c in txt)
            fnt = FONT_SCROLL_UNI if needs_uni else FONT_SCROLL_BODY
            raw_d.text(
                (X0 + 10, y_cursor),
                txt[:44] if not needs_uni else txt,
                fill=col,
                font=fnt,
                stroke_width=1,
                stroke_fill=(0, 6, 2, 250),
            )
        y_cursor += line_step

    # Footer bar
    raw_d.rectangle([X0 + 2, Y1 - 26, X1 - 2, Y1 - 2], fill=hdr_bg)
    cur_line_num = (head_idx + visible_rows) % total
    raw_d.text(
        (X0 + 10, Y1 - 23),
        f"SPOOL {cur_line_num:04d}/{total:04d} // 2400 BAUD LIVE SYNC",
        fill=hdr_col,
        font=FONT_SCROLL_HDR,
        stroke_width=1,
        stroke_fill=(0, 8, 2, 245),
    )


_LEFT_PANEL_CACHE: dict[str, object] = {"key": None, "img": None}


def render_left_lore_question_panel(
    canvas: Image.Image,
    current_track: dict,
    state: dict,
    now_ts: float,
    is_warn: bool,
) -> None:
    """
    Renders the Left-Side CRT World-Building Case File & Song Lore Dossier Panel
    (`x=16..468, y=22..904` at 1080p, `452x882` px — Option A Decluttered Layout):
      - Top Card: Track Chronology & Broadcast Role (Song, Era, Role)
      - 3-Tab Dossier Selector Strip (`[1. LYRICS]`, `[2. STORY]`, `[3. ARCHIVE]`)
      - Single Spacious Active Dossier Card rotating every 20s with larger `FONT_HUD_9` (20px)
        typography, 32px line spacing, and clean dark CRT breathing room.
    """
    is_vocal_song = (current_track or {}).get("kind", "vocal_song") == "vocal_song"
    target_sec = int(state.get("target_sector", 7))
    is_b3 = target_sec >= 8
    card_idx = int(now_ts // 20) % 3
    stanza_tick = int(now_ts // 18)

    cache_key = (
        (current_track or {}).get("filename", ""),
        is_vocal_song,
        is_warn,
        is_b3,
        card_idx,
        stanza_tick,
        state.get("crt_header", ""),
        state.get("crt_sub", "") if not is_vocal_song else "",
        state.get("crt_body", "") if not is_vocal_song else "",
    )
    if _LEFT_PANEL_CACHE.get("key") == cache_key and _LEFT_PANEL_CACHE.get("img") is not None:
        canvas.alpha_composite(_LEFT_PANEL_CACHE["img"], (14, 20))  # type: ignore[arg-type]
        return

    patch_w, patch_h = 458, 888
    patch = Image.new("RGBA", (patch_w, patch_h), (0, 0, 0, 0))
    raw_d = ImageDraw.Draw(patch)
    # Offset inside patch so global (16..468, 22..904) maps to (2..454, 2..884)
    X0, Y0, X1, Y1 = 2, 2, 454, 884

    border_col = (255, 150, 30, 245) if is_b3 else ((255, 176, 20, 245) if is_warn else (55, 245, 78, 245))
    dim_border = (165, 95, 20, 215) if (is_warn or is_b3) else (32, 145, 48, 215)
    bg_col = (10, 5, 2, 238) if (is_warn or is_b3) else (2, 10, 4, 238)
    hdr_bg = (36, 16, 5, 250) if (is_warn or is_b3) else (8, 32, 13, 250)
    sec_hdr_bg = (24, 12, 4, 245) if (is_warn or is_b3) else (5, 22, 9, 245)

    c_hdr = (255, 210, 65, 255) if (is_warn or is_b3) else (110, 255, 130, 255)
    c_amber = (255, 212, 68, 255)
    c_bright = (255, 246, 205, 255) if (is_warn or is_b3) else (225, 255, 232, 255)
    c_green = (115, 255, 135, 255)
    c_cyan = (150, 250, 225, 255)

    def _txt(px: int, py: int, s: str, col: tuple, fnt=FONT_SCROLL_HDR) -> None:
        raw_d.text((px, py), s, fill=col, font=fnt, stroke_width=1, stroke_fill=(0, 6, 2, 250))

    def _fit_1080(s: str, max_px: float = 428.0, fnt=FONT_SCROLL_HDR) -> str:
        out = s.strip()
        try:
            while len(out) > 8 and fnt.getlength(out) > max_px:
                if " " in out:
                    out = out.rsplit(" ", 1)[0].rstrip(":-/ ")
                else:
                    out = out[:-1]
            if out.count("(") > out.count(")"):
                out = out.rsplit("(", 1)[0].strip()
        except Exception:
            out = out[:42]
        return out

    if not is_vocal_song:
        raw_d.rectangle([X0, Y0, X1, Y1], fill=(0, 0, 0, 248), outline=border_col, width=2)
        raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 30], fill=hdr_bg)
        _txt(X0 + 12, Y0 + 6, "INTERSTITIAL BROADCAST // SIGNAL LOG", c_hdr)
        _txt(X0 + 14, Y0 + 46, _fit_1080("REEL: B2-INTERCEPT // 14.2001 HZ", 418.0), c_amber)
        _txt(X0 + 14, Y0 + 74, _fit_1080(f"TYPE: {(current_track or {}).get('display_title', 'SIGNAL INTERCEPT')}", 418.0), c_green)
        _txt(X0 + 14, Y0 + 102, _fit_1080(f"MODE: {state.get('crt_header', 'SHORTWAVE RELAY')}", 418.0), c_amber)
        raw_d.line([(X0 + 14, Y0 + 132), (X1 - 14, Y0 + 132)], fill=dim_border, width=1)

        y_cur = Y0 + 148
        for blk_txt, blk_col in [
            (state.get("crt_sub", ""), c_bright),
            (state.get("crt_body", ""), c_cyan),
            (state.get("line1", ""), c_green),
            (state.get("line2", ""), c_amber),
            (state.get("line3", ""), c_bright),
        ]:
            if not blk_txt:
                continue
            wrapped_blk = _wrap_px_1080p(blk_txt, FONT_SCROLL_BODY, 416.0, 6)
            for ln in wrapped_blk:
                if y_cur <= Y1 - 40:
                    _txt(X0 + 14, y_cur, ln, blk_col, FONT_SCROLL_BODY)
                    y_cur += 25
            y_cur += 14
        raw_d.rectangle([X0 + 2, Y1 - 26, X1 - 2, Y1 - 2], fill=hdr_bg)
        _txt(X0 + 10, Y1 - 23, "SIGNAL INTERCEPT // stardust-archive.net", c_hdr)
        _LEFT_PANEL_CACHE["key"] = cache_key
        _LEFT_PANEL_CACHE["img"] = patch
        canvas.alpha_composite(patch, (14, 20))
        return

    lore = resolve_song_lore_panel(current_track, state, now_ts)
    status_tag = lore.get("lyric_status", "[STANZA 1/1]")

    # Single clean outer phosphor glass frame (no nested boxes inside boxes)
    raw_d.rectangle([X0 - 2, Y0 - 2, X1 + 2, Y1 + 2], outline=(border_col[0], border_col[1], border_col[2], 65), width=2)
    raw_d.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)

    # Subtle CRT scanlines across the left terminal
    scan_col = (18, 9, 3, 225) if (is_warn or is_b3) else (4, 16, 6, 225)
    for sy in range(Y0 + 56, Y1 - 28, 4):
        raw_d.line([(X0 + 2, sy), (X1 - 2, sy)], fill=scan_col, width=1)

    # Top Header Bar
    raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 30], fill=hdr_bg)
    _txt(X0 + 10, Y0 + 6, "CANONICAL ARCHIVE // SONG LORE DOSSIER", c_hdr)

    # Sub-Header Bar (strictly in-universe reel ID, zero file/source names)
    raw_d.rectangle([X0 + 2, Y0 + 31, X1 - 2, Y0 + 54], fill=(16, 10, 3, 245) if (is_warn or is_b3) else (4, 20, 8, 245))
    _txt(X0 + 10, Y0 + 34, _fit_1080(lore["catalog_id"], 430.0), c_amber)

    # --- TRACK METADATA (`y=66..152`, directly on dark scanlined CRT glass) ---
    _txt(X0 + 14, Y0 + 66, _fit_1080(f"SONG : {lore['title']}", 422.0, FONT_HUD_9), c_bright, FONT_HUD_9)
    _txt(X0 + 14, Y0 + 96, _fit_1080(f"ERA  : {lore['timeline']}", 422.0, FONT_HUD_9), c_green, FONT_HUD_9)
    _txt(X0 + 14, Y0 + 126, _fit_1080(f"ROLE : {lore['pov']}", 422.0, FONT_HUD_9), c_amber, FONT_HUD_9)

    raw_d.line([(X0 + 14, Y0 + 162), (X1 - 14, Y0 + 162)], fill=dim_border, width=1)

    # --- 3-TAB ROTATING DOSSIER SELECTOR (`y=174..206`) ---
    tab_y0, tab_y1 = Y0 + 174, Y0 + 206
    tabs = [
        (X0 + 14, X0 + 146, "1. LYRICS"),
        (X0 + 154, X0 + 286, "2. STORY"),
        (X0 + 294, X1 - 14, "3. ARCHIVE"),
    ]
    for t_i, (tx0, tx1, t_lbl) in enumerate(tabs):
        is_act = t_i == card_idx
        if is_act:
            raw_d.rectangle([tx0, tab_y0, tx1, tab_y1], fill=(255, 198, 42, 250), outline=(255, 240, 150, 255), width=2)
            raw_d.text((tx0 + 12, tab_y0 + 7), t_lbl, fill=(10, 8, 2, 255), font=FONT_SCROLL_HDR)
        else:
            raw_d.rectangle([tx0, tab_y0, tx1, tab_y1], fill=(6, 18, 9, 225), outline=dim_border, width=1)
            _txt(tx0 + 12, tab_y0 + 7, t_lbl, (95, 185, 108, 220), FONT_SCROLL_HDR)

    # --- OPEN TERMINAL CONTENT AREA (`y=224..840`, single dedicated view per tab, zero extra cells underneath) ---
    clean_conn = re.sub(r"\s*\(Folder\s+[A-Za-z0-9_-]{12,}\)", "", lore["connections"])
    if card_idx == 0:
        card_hdr = f"VERBATIM LYRICS // {status_tag}"
        card_body = lore["lyric_excerpt"]
        card_col = c_cyan
    elif card_idx == 1:
        card_hdr = "TRACK STORY & BROADCAST CONTEXT"
        card_body = lore["meaning"]
        card_col = c_bright
    else:
        card_hdr = "SUBLEVEL B2 ARCHIVIST LOG"
        card_body = clean_conn
        card_col = c_green

    _txt(X0 + 14, Y0 + 224, card_hdr, c_amber, FONT_SCROLL_HDR)
    raw_d.line([(X0 + 14, Y0 + 250), (X1 - 14, Y0 + 250)], fill=dim_border, width=1)

    if card_idx == 0 and "/" in card_body and not card_body.strip().startswith("["):
        body_lines = []
        for verse in [v.strip() for v in card_body.split("/") if v.strip()]:
            v_wrapped = _wrap_px_1080p(verse, FONT_HUD_9, 420.0, 3)
            if len(body_lines) + len(v_wrapped) <= 15:
                body_lines.extend(v_wrapped)
            else:
                break
    else:
        body_lines = _wrap_px_1080p(card_body, FONT_HUD_9, 420.0, 15)

    y_cur = Y0 + 266
    for ln in body_lines:
        _txt(X0 + 14, y_cur, ln, card_col, FONT_HUD_9)
        y_cur += 36

    # Footer Bar
    raw_d.rectangle([X0 + 2, Y1 - 26, X1 - 2, Y1 - 2], fill=hdr_bg)
    _txt(X0 + 10, Y1 - 23, _fit_1080(f"DOSSIER {card_idx + 1}/3 (20S) // stardust-archive.net", 430.0), c_hdr)

    _LEFT_PANEL_CACHE["key"] = cache_key
    _LEFT_PANEL_CACHE["img"] = patch
    canvas.alpha_composite(patch, (14, 20))


_CENTER_BANNER_CACHE: dict[str, object] = {"key": None, "img": None}


def render_center_live_chat_banner(
    canvas: Image.Image,
    current_track: dict,
    state: dict,
    now_ts: float,
    is_warn: bool,
) -> None:
    """
    Renders the Center-Stage High-Prominence Live Chat Discussion Prompt Banner
    (`x=478..1430, y=758..904` at 1080p, `952x146` px — centered at `x=954` directly
    underneath the CRT monitor bevel between Left `16..468` and Right `1440..1904`!).
    """
    is_vocal_song = (current_track or {}).get("kind", "vocal_song") == "vocal_song"
    pulse_on = (int(now_ts * 2) % 2) == 0
    cache_key = (
        (current_track or {}).get("filename", ""),
        is_vocal_song,
        state.get("crt_header", ""),
        state.get("crt_body", "") if not is_vocal_song else "",
        int(now_ts // 20),
        pulse_on,
    )
    if _CENTER_BANNER_CACHE.get("key") == cache_key and _CENTER_BANNER_CACHE.get("img") is not None:
        canvas.alpha_composite(_CENTER_BANNER_CACHE["img"], (474, 754))  # type: ignore[arg-type]
        return

    patch = Image.new("RGBA", (960, 154), (0, 0, 0, 0))
    raw_d = ImageDraw.Draw(patch)
    X0, Y0, X1, Y1 = 4, 4, 956, 150

    if is_vocal_song:
        lore = resolve_song_lore_panel(current_track, state, now_ts)
        hdr_txt = f"[? LIVE CHAT SONG THEORY #{lore['question_index']}/{lore['question_total']} — DROP YOUR TAKE IN LIVE CHAT]"
        body_txt = lore["question_text"]
    else:
        hdr_txt = f"[? LIVE CHAT SIGNAL DECODE — {state.get('crt_header', 'SHORTWAVE INTERCEPT')}]"
        body_txt = (
            f"INTERCEPT ACTIVE: {state.get('crt_body', '')} — Compare notes in Live Chat or test passkeys at "
            f"stardust-archive.net/forensics/"
        )

    border_col = (255, 202, 48, 252)
    bg_col = (20, 10, 3, 246)
    hdr_bg = (56, 28, 6, 252)

    # Outer soft amber glow + double-framed center banner
    raw_d.rectangle([X0 - 3, Y0 - 3, X1 + 3, Y1 + 3], outline=(255, 195, 45, 85), width=2)
    raw_d.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)
    raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 32], fill=hdr_bg)
    raw_d.line([(X0 + 2, Y0 + 33), (X1 - 2, Y0 + 33)], fill=(255, 185, 40, 210), width=1)

    # Subtle CRT scanlines inside the banner
    for sy in range(Y0 + 36, Y1 - 3, 4):
        raw_d.line([(X0 + 3, sy), (X1 - 3, sy)], fill=(12, 6, 2, 225), width=1)

    # Pulsing gold beacon LED in header
    dot_fill = (255, 230, 75, 255) if pulse_on else (180, 115, 25, 235)
    raw_d.ellipse([X0 + 12, Y0 + 11, X0 + 24, Y0 + 23], fill=dot_fill, outline=(255, 250, 190, 255))

    raw_d.text(
        (X0 + 32, Y0 + 6),
        hdr_txt[:74],
        fill=(255, 228, 85, 255),
        font=FONT_HUD_9,
        stroke_width=1,
        stroke_fill=(0, 6, 2, 250),
    )

    q_lines = _wrap_px_1080p(body_txt, FONT_HUD_10, 918.0, 3)
    for idx, ln in enumerate(q_lines):
        raw_d.text(
            (X0 + 16, Y0 + 42 + idx * 32),
            ln,
            fill=(255, 248, 208, 255),
            font=FONT_HUD_10,
            stroke_width=1,
            stroke_fill=(0, 6, 2, 250),
        )

    _CENTER_BANNER_CACHE["key"] = cache_key
    _CENTER_BANNER_CACHE["img"] = patch
    canvas.alpha_composite(patch, (474, 754))


def render_top_trailhead_banner(
    canvas: Image.Image,
    state: dict,
    snap_meta: dict,
    now_ts: float,
    is_warn: bool,
) -> None:
    """
    Renders the redesigned 1989 Master Control Containment & Signal Intrusion Header
    (`x=478..1430, y=14..68` at 1080p, `952x54` px — centered at `x=954` above the CRT monitor!).
    """
    X0, Y0, X1, Y1 = 478, 14, 1430, 68
    raw_d = ImageDraw.Draw(canvas)

    target_sec = int(state.get("target_sector", 7))
    is_b3_breach = target_sec >= 8
    crt_mode = state.get("crt_mode", "NOVA_FACE")

    smpte_sec = int(now_ts) % 60
    smpte_frm = int((now_ts % 1.0) * 29.97)
    smpte_str = f"03:40:{smpte_sec:02d}:{smpte_frm:02d}"

    if is_b3_breach:
        border_col = (255, 125, 30, 245)
        bg_col = (18, 6, 2, 230)
        hdr_strip = (48, 14, 4, 245)
        top_col = (255, 205, 65, 255)
        line1_str = f"[!! SUBLEVEL B3 BREACH // GATE #{target_sec:02d}] DIRECTIVE 9 CAGE FRACTURED // SMPTE {smpte_str}"
    elif is_warn or crt_mode in ("SECOND_VOICE", "OUROBOROS_TORUS", "HARMONY_CAMERA"):
        border_col = (255, 180, 25, 240)
        bg_col = (14, 7, 2, 225)
        hdr_strip = (36, 18, 5, 240)
        top_col = (255, 210, 60, 255)
        line1_str = f"[! SIGNAL HIJACK // +0.0001 HZ] B2-114 COUNTERPOINT OVERRIDE // SMPTE {smpte_str}"
    else:
        border_col = (55, 245, 78, 235)
        bg_col = (3, 12, 5, 220)
        hdr_strip = (8, 30, 12, 240)
        top_col = (115, 255, 135, 255)
        line1_str = f"ORION B2-114 MASTER CONTROL // DIRECTIVE 9 CONTAINMENT: 99.4% // SMPTE {smpte_str}"

    raw_d.rectangle([X0 - 2, Y0 - 2, X1 + 2, Y1 + 2], outline=(border_col[0], border_col[1], border_col[2], 65), width=2)
    raw_d.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)
    raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 26], fill=hdr_strip)

    led_on = (int(now_ts * 2) % 2 == 0) if is_b3_breach else (int(now_ts) % 2 == 0)
    led_col = (255, 75, 35, 255) if led_on else (140, 35, 20, 220)
    raw_d.ellipse([X0 + 10, Y0 + 9, X0 + 20, Y0 + 19], fill=led_col, outline=(255, 210, 65, 255))

    # Rotating Line 2 directive (strictly <= 88 chars so full URLs never truncate!)
    rot = int(now_ts // 10) % 3
    if rot == 0:
        line2_str = "NEW INVESTIGATOR? ENTER STREAM CODES AT: stardust-archive.net/forensics/"
        bot_col = (215, 255, 222, 255) if not (is_warn or is_b3_breach) else (255, 242, 190, 255)
    elif rot == 1:
        line2_str = "SIGNAL LAB: 2600 HZ BLUE-BOX, 7.5 IPS & COAGULA -> /forensics/signal_lab.html"
        bot_col = (135, 245, 215, 255)
    else:
        line2_str = "TWIST WARNING: THE 1983<->2025 LOOP IS A CAGE! TYPE 'LABYRINTH' AT /forensics/"
        bot_col = (255, 205, 65, 255)

    raw_d.text(
        (X0 + 26, Y0 + 5),
        line1_str[:88],
        fill=top_col,
        font=FONT_SCROLL_HDR,
        stroke_width=1,
        stroke_fill=(0, 6, 2, 245),
    )
    raw_d.text(
        (X0 + 10, Y0 + 30),
        line2_str[:88],
        fill=bot_col,
        font=FONT_SCROLL_HDR,
        stroke_width=1,
        stroke_fill=(0, 6, 2, 245),
    )


def render_full_arg_overlay_png(
    out_path: Path,
    state: dict,
    assets_dir: Path,
    now_ts: float,
    snap_meta: dict | None = None,
) -> bytes:
    """
    Renders the complete `1920x1080` (1080p Full HD) RGBA PNG overlay containing:
      1. Front-Facing CRT Screen Patch (`688x488` at `x=616, y=204`, strictly inside the amber border)
      2. Diegetic Control Room Hardware Animations (rack LEDs, VU needles, power LED)
      3. Left-Side World-Building Case File Dossier (`x=20..446, y=22..904`)
      4. Top-Center Master Control Containment & Signal Intrusion Header (`x=456..1354, y=14..68`)
      5. Center-Stage Live Chat Discussion Prompt Banner (`x=456..1354, y=758..904`)
      6. Right-Side Rolling Multilingual Usenet / Regional BBS / YouTube Comment Terminal (`x=1364..1900, y=22..904`)
      7. 3-Module Broadcast Engineering Console (`x=20..1900, y=920..1068`)
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
            "current_track": {
                "filename": "radio_b_midnight_protocol_final_1.mp3",
                "stem": "radio_b_midnight_protocol_final_1",
                "kind": "vocal_song",
                "display_title": "Midnight Protocol",
            },
        }
    else:
        relay = snap_meta.get("relay", REGIONAL_RELAYS[0])

    current_track = snap_meta.get("current_track") or {
        "filename": "radio_b_midnight_protocol_final_1.mp3",
        "stem": "radio_b_midnight_protocol_final_1",
        "kind": "vocal_song",
        "display_title": state.get("crt_sub", "Midnight Protocol"),
    }

    canvas = Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))

    # 1. Composite Front-Facing CRT Screen Content strictly inside the amber border at 1080p
    crt_patch = render_crt_window_patch(state, relay, assets_dir, now_ts, current_track=current_track)
    canvas.alpha_composite(crt_patch, (CRT_PX_X, CRT_PX_Y))

    # 2. Draw Diegetic Control Room Hardware Animations, Left Lore Panel, Top Banner, Center Live Chat Banner, Right Scroll & Bottom Console
    draw = _HiDPIDraw(ImageDraw.Draw(canvas), scale=SCALE)
    is_warn = (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN" or int(state.get("target_sector", 7)) >= 8
    render_room_hardware_animations(canvas, state, now_ts, is_warn)
    render_left_lore_question_panel(canvas, current_track, state, now_ts, is_warn)
    render_top_trailhead_banner(canvas, state, snap_meta, now_ts, is_warn)
    render_center_live_chat_banner(canvas, current_track, state, now_ts, is_warn)
    render_right_usenet_youtube_scroll(canvas, now_ts, is_warn)
    render_bottom_engineering_console(draw, state, snap_meta, now_ts)

    buf = io.BytesIO()
    canvas.save(buf, format="PNG", compress_level=1)
    png_bytes = buf.getvalue()

    main_mod = sys.modules.get("__main__")
    in_pipe_worker = main_mod is not None and hasattr(main_mod, "_render_worker")
    if not in_pipe_worker or (int(now_ts) % 3 == 0):
        tmp_path = out_path.with_suffix(".tmp.png")
        tmp_path.write_bytes(png_bytes)
        os.replace(tmp_path, out_path)

    # When running inside `hud_pipe_feeder.py`'s background `_render_worker` thread
    # (which sleeps 0.5s after `_render_once`), pace returns to an exact 1.000000 Hz
    # monotonic grid so consecutive frames are spaced by exactly 1.000000s.
    if in_pipe_worker:
        now_mono = time.monotonic()
        next_ret = getattr(main_mod, "_stardust_next_return_mono", None)
        if next_ret is None or (now_mono - next_ret) > 0.45 or (next_ret - now_mono) > 1.5:
            next_ret = now_mono
        else:
            sleep_rem = next_ret - now_mono
            if sleep_rem > 0:
                time.sleep(sleep_rem)
        setattr(main_mod, "_stardust_next_return_mono", next_ret + 1.0)

    return png_bytes


CANONICAL_SONG_TITLES: dict[str, str] = {
    "radio_01_gasoline_heart_1985_tokyo_master": "Gasoline Heart (1985 Tokyo)",
    "radio_02_between_the_circuits": "Between The Circuits",
    "radio_02_brighter_than_the_sun_1987_tokyo_master": "Brighter Than The Sun (1987 Tokyo)",
    "radio_04_midnight_animal_1986_tokyo_master": "Midnight Animal (1986 Tokyo)",
    "radio_04_synthetic_dawn": "Synthetic Dawn",
    "radio_05_first_light_on_my_face": "First Light On My Face",
    "radio_05_ghost_transit_1985_tokyo_master": "Ghost Transit (1985 Tokyo)",
    "radio_06_the_air_feels_wrong": "The Air Feels Wrong",
    "radio_07_room_full_of_color": "Room Full Of Color",
    "radio_08_faultline_path": "Faultline Path",
    "radio_09_lost_signal_trace": "Lost Signal Trace",
    "radio_13_through_the_threshold": "Through The Threshold",
    "radio_5_the_way_back_v3": "The Way Back",
    "radio_artificial_heart_bonus_track": "Artificial Heart",
    "radio_asset_loss_the_dead_hand": "Asset Loss (The Dead Hand)",
    "radio_audio_file_0147_1": "Audio File 0147",
    "radio_b_midnight_protocol_final_1": "Midnight Protocol",
    "radio_b_only_we_remain_marcus_and_nova_duet_1": "Only We Remain (Marcus & Nova Duet)",
    "radio_blueprint_for_ruin_old": "Blueprint For Ruin",
    "radio_by_order_of_harmony": "By Order Of Harmony",
    "radio_city_that_can’t_ignore_me": "City That Can't Ignore Me",
    "radio_city_that_doesn_t_need_me": "City That Doesn't Need Me",
    "radio_corridor_dreams_movement_1": "Corridor Dreams (Movement 1)",
    "radio_corridor_dreams_movement_2": "Corridor Dreams (Movement 2)",
    "radio_corridor_dreams_movement_3": "Corridor Dreams (Movement 3)",
    "radio_crossing_this_line_remastered": "Crossing This Line",
    "radio_dial_tone_heart": "Dial-Tone Heart",
    "radio_every_window_is_a_promise_crystal_promise": "Every Window Is A Promise",
    "radio_hologram_city_queen_remastered": "Hologram City Queen",
    "radio_it_has_no_face_old": "It Has No Face",
    "radio_marina_half_the_city_knows_your_name": "Marina (Half The City Knows Your Name)",
    "radio_playback_forever_master": "Playback Forever",
    "radio_say_you_ll_stay": "Say You'll Stay",
    "radio_someone_else’s_memories": "Someone Else's Memories",
    "radio_stage_fever_remastered": "Stage Fever",
    "radio_the_man_in_the_booth_marcus_song": "The Man In The Booth (Marcus)",
    "radio_the_man_in_the_booth_refrain": "The Man In The Booth (Refrain)",
    "radio_together_s_the_way": "Together's The Way",
    "radio_unstable_pattern_old": "Unstable Pattern",
    "radio_we_are_the_thunder_live": "We Are The Thunder (Live)",
    "radio_programmed_for_love": "Programmed For Love (1983 Recall Demo)",
    "radio_the_seventh_sons_seventh_daughter": "The Seventh Son's Seventh Daughter",
    "radio_erase_the_frame": "Erase The Frame",
    "radio_edit_the_script": "Edit The Script",
    "radio_to_the_ends_of_forever": "To The Ends Of Forever",
    "radio_shes_hardwired": "She's Hardwired",
    "radio_synthetic_kiss": "Synthetic Kiss",
    "radio_digital_heartbeat": "Digital Heartbeat",
    "radio_cold_reaction": "Cold Reaction",
    "radio_one_voice_left": "One Voice Left",
    "radio_give_me_the_other_half": "Give Me The Other Half",
    "radio_the_last_secret": "The Last Secret",
    "radio_the_other_flame": "The Other Flame",
    "radio_burn_the_chorus": "Burn The Chorus",
    "radio_blood_on_the_stage": "Blood On The Stage",
    "radio_cage_in_your_hand": "Cage In Your Hand",
    "radio_behind_the_glass": "Behind The Glass",
    "radio_ghost_on_the_radio": "Ghost On The Radio",
    "radio_hunter_at_the_gate": "Hunter At The Gate",
    "radio_paper_windows": "Paper Windows",
    "radio_fire_in_the_wires": "Fire In The Wires",
    "radio_the_stars_in_your_hands": "The Stars In Your Hands",
    "radio_warm_hands_one_map": "Warm Hands, One Map",
}


def classify_track(filepath: str) -> dict:
    p = Path(filepath)
    stem = p.stem
    parent = p.parent.name
    if "radio_master_songs" in filepath or stem.startswith("radio_"):
        kind = "vocal_song"
        if stem in CANONICAL_SONG_TITLES:
            clean = CANONICAL_SONG_TITLES[stem]
        else:
            s = re.sub(r"^radio_(?:\d+_)?", "", stem)
            s = re.sub(r"_(?:1|old|remastered|master|final_1|v3)$", "", s)
            clean = s.replace("_", " ").title().replace("’S", "'s").replace("’T", "'t")
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


def _get_live_ffmpeg_open_mp3(force_poll: bool = False) -> str | None:
    """Queries the active FFmpeg concat process via `lsof` to return the exact .mp3 file currently being decoded."""
    import subprocess
    main_mod = sys.modules.get("__main__")
    now_m = time.monotonic()
    if not force_poll and main_mod is not None:
        cached_mp3 = getattr(main_mod, "_stardust_cached_lsof_mp3", None)
        cached_mono = getattr(main_mod, "_stardust_cached_lsof_mono", 0.0)
        if cached_mp3 and (now_m - cached_mono) < 1.6:
            return cached_mp3
    pid = getattr(main_mod, "_stardust_ffmpeg_pid", None) if main_mod else None
    for _ in range(2):
        if not pid:
            try:
                res = subprocess.run(
                    ["pgrep", "-f", "ffmpeg.*playlist\\.txt"],
                    capture_output=True, text=True, timeout=0.35
                )
                pids = [x.strip() for x in res.stdout.splitlines() if x.strip().isdigit()]
                for cand in pids:
                    comm = subprocess.run(
                        ["ps", "-p", cand, "-o", "comm="],
                        capture_output=True, text=True, timeout=0.2
                    ).stdout.strip()
                    if comm.endswith("ffmpeg"):
                        pid = cand
                        break
                if not pid and pids:
                    pid = pids[-1]
                if main_mod is not None and pid:
                    setattr(main_mod, "_stardust_ffmpeg_pid", pid)
            except Exception:
                return None
        if not pid:
            return None
        try:
            res = subprocess.run(
                ["lsof", "-Fn", "-a", "-d", "3,4,5,6,7,8,9,10", "-p", str(pid)],
                capture_output=True, text=True, timeout=0.35
            )
            if res.returncode == 0 and res.stdout:
                for line in res.stdout.splitlines():
                    if line.startswith("n") and line.lower().endswith(".mp3"):
                        found_mp3 = line[1:].strip()
                        if main_mod is not None:
                            setattr(main_mod, "_stardust_cached_lsof_mp3", found_mp3)
                            setattr(main_mod, "_stardust_cached_lsof_mono", now_m)
                        return found_mp3
            pid = None
            if main_mod is not None:
                setattr(main_mod, "_stardust_ffmpeg_pid", None)
        except Exception:
            pid = None
    return None


# Raw audio/muxer clock has 0.0s offset; visual `image2pipe` pipeline has +4.0s lookahead
PIPE_FIFO_LOOKAHEAD_SEC = 0.0
VISUAL_PIPELINE_LEAD_SEC = 4.0


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
                if origin_ts is None or abs((now_ts - origin_ts) - raw_interp) > 2.5:
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
    active_track_path: str | None = None

    if is_live and elapsed_sec > 0 and tracks:
        main_mod = sys.modules.get("__main__")
        sync_ver = getattr(main_mod, "_stardust_sync_ver", None) if main_mod else None
        prev_open = getattr(main_mod, "_stardust_live_open_mp3", None) if main_mod else None
        track_start_ts = getattr(main_mod, "_stardust_live_track_start_ts", None) if main_mod else None
        tracked_idx = getattr(main_mod, "_stardust_live_playhead_idx", None) if main_mod else None
        prev_dur = get_exact_track_duration(prev_open, repo_root) if prev_open else 180.0
        near_boundary = (track_start_ts is None) or ((now - track_start_ts) >= (prev_dur - 6.0))
        live_open_mp3 = _get_live_ffmpeg_open_mp3(force_poll=near_boundary)

        # Also compute cumulative playlist offset from `elapsed_sec` as an exact reference anchor
        accum = 0.0
        pl_idx = 0
        pl_offset = 0.0
        for idx, tpath in enumerate(tracks):
            dur = get_exact_track_duration(tpath, repo_root)
            if accum + dur > elapsed_sec:
                pl_idx = idx
                pl_offset = max(0.0, elapsed_sec - accum)
                break
            accum += dur

        if live_open_mp3:
            active_track_path = live_open_mp3
            track_dur_sec = get_exact_track_duration(live_open_mp3, repo_root)
            open_bname = os.path.basename(live_open_mp3)

            if prev_open != live_open_mp3 or track_start_ts is None or sync_ver != "v5.6":
                # Resolve best matching index in tracks
                start_search = pl_idx if tracked_idx is None else tracked_idx
                found_idx = None
                for step in range(len(tracks)):
                    cand_idx = (start_search + step) % len(tracks)
                    if os.path.basename(tracks[cand_idx]) == open_bname:
                        found_idx = cand_idx
                        break
                playhead_index = found_idx if found_idx is not None else pl_idx

                if prev_open is not None and prev_open != live_open_mp3 and sync_ver == "v5.6" and track_start_ts is not None:
                    # Hardware transition just detected by lsof
                    expected_start = track_start_ts + prev_dur
                    track_start_ts = expected_start if abs(now - expected_start) <= 3.0 else now
                elif playhead_index == pl_idx:
                    # Exact cumulative playlist anchor from FFmpeg muxer clock
                    track_start_ts = now - pl_offset
                else:
                    # Compute cumulative start of `playhead_index` in `tracks`
                    cand_accum = sum(get_exact_track_duration(tracks[i], repo_root) for i in range(playhead_index))
                    cand_off = max(0.0, min(track_dur_sec - 1.0, elapsed_sec - cand_accum))
                    track_start_ts = now - cand_off

                if main_mod is not None:
                    setattr(main_mod, "_stardust_sync_ver", "v5.6")
                    setattr(main_mod, "_stardust_live_open_mp3", live_open_mp3)
                    setattr(main_mod, "_stardust_live_track_start_ts", track_start_ts)
                    setattr(main_mod, "_stardust_live_playhead_idx", playhead_index)
            else:
                playhead_index = tracked_idx if tracked_idx is not None else pl_idx

            # Add +4.0s visual pipeline lead (`VISUAL_PIPELINE_LEAD_SEC`) so frames exiting the
            # 4-second `image2pipe` buffer match the audio to the sub-second!
            raw_offset = (now - track_start_ts) + VISUAL_PIPELINE_LEAD_SEC
            if raw_offset >= track_dur_sec and len(tracks) > 1:
                playhead_index = (playhead_index + 1) % len(tracks)
                active_track_path = tracks[playhead_index]
                track_offset_sec = max(0.0, raw_offset - track_dur_sec)
                track_dur_sec = get_exact_track_duration(active_track_path, repo_root)
            else:
                track_offset_sec = min(max(0.0, track_dur_sec - 0.1), max(0.0, raw_offset))
        else:
            playhead_index = pl_idx
            raw_offset = pl_offset + VISUAL_PIPELINE_LEAD_SEC
            track_dur_sec = get_exact_track_duration(tracks[playhead_index], repo_root)
            if raw_offset >= track_dur_sec and len(tracks) > 1:
                playhead_index = (playhead_index + 1) % len(tracks)
                track_offset_sec = max(0.0, raw_offset - track_dur_sec)
                track_dur_sec = get_exact_track_duration(tracks[playhead_index], repo_root)
            else:
                track_offset_sec = raw_offset
            active_track_path = tracks[playhead_index]

        # Lock integer second progression on consecutive ~1.0Hz ticks within the same track
        if main_mod is not None:
            last_idx = getattr(main_mod, "_stardust_last_playhead_idx", None)
            last_int_off = getattr(main_mod, "_stardust_last_int_offset", None)
            last_snap_mono = getattr(main_mod, "_stardust_last_snap_mono", None)
            now_mono = time.monotonic()
            if (
                last_idx == playhead_index
                and last_int_off is not None
                and last_snap_mono is not None
                and 0.65 <= (now_mono - last_snap_mono) <= 1.35
                and abs(track_offset_sec - (last_int_off + 1.0)) <= 1.45
            ):
                int_off = min(max(0, int(track_dur_sec)), last_int_off + 1)
                track_offset_sec = float(int_off) + 0.5
            else:
                int_off = int(track_offset_sec)
            setattr(main_mod, "_stardust_last_playhead_idx", playhead_index)
            setattr(main_mod, "_stardust_last_int_offset", int_off)
            setattr(main_mod, "_stardust_last_snap_mono", now_mono)

    current_track = classify_track(active_track_path or tracks[playhead_index])
    next_track = classify_track(tracks[(playhead_index + 1) % len(tracks)])
    recipe = CADENCE_RECIPES[playhead_index % len(CADENCE_RECIPES)]
    relay = REGIONAL_RELAYS[int(now // 300) % len(REGIONAL_RELAYS)]

    state = resolve_intentional_state(current_track, track_offset_sec, track_dur_sec, relay)
    current_lore = resolve_song_lore_panel(current_track, state, now)
    current_track["veo_reel"] = current_lore.get("veo_reel", "veo_arena_rock_singer")
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
            "current_track": current_track,
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
    parser.add_argument("--json-only", action="store_true", help="Write live_telemetry.json only (for CI/GitHub Actions)")
    parser.add_argument("--daemon", action="store_true")
    args = parser.parse_args()

    out_json = args.out_json or (args.repo_root / "site" / "assets" / "live_telemetry.json")
    out_forensics_json = args.repo_root / "site" / "forensics" / "live_telemetry.json"
    out_static_json = args.repo_root / "src" / "site_static" / "assets" / "live_telemetry.json"
    out_hud = args.out_hud_png or (args.repo_root / "youtube" / "livestream" / "live_hud.png")
    assets_dir = args.repo_root / "youtube" / "livestream" / "assets_arg"
    backdrop_clean = args.repo_root / "youtube" / "livestream" / "backdrop_clean.png"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_static_json.parent.mkdir(parents=True, exist_ok=True)
    out_hud.parent.mkdir(parents=True, exist_ok=True)

    while True:
        now = time.time()
        snap = build_telemetry_snapshot(args.repo_root, now_ts=now, force_offline=args.offline)
        payload = json.dumps(snap, indent=2)
        out_json.write_text(payload, encoding="utf-8")
        out_static_json.write_text(payload, encoding="utf-8")
        if out_forensics_json.parent.exists():
            out_forensics_json.write_text(payload, encoding="utf-8")
        if not args.json_only and backdrop_clean.exists():
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
