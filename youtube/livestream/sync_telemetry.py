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
import radio_shows_engine
import song_crt_cgi_engine
import song_lore_questions
import trojan_horse_radio_engine

importlib.reload(arg_broadcast_codex)
importlib.reload(radio_shows_engine)
importlib.reload(song_crt_cgi_engine)
importlib.reload(song_lore_questions)
importlib.reload(trojan_horse_radio_engine)
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
# Physical 1080p coordinates of the Option A Edge-to-Edge Full-Frame CRT glass interior (1728x928 at x=96..1824, y=76..1004)
CRT_PX_X, CRT_PX_Y, CRT_PX_W, CRT_PX_H = 96, 76, 1728, 928
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
    FONT_HUD_UNI = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 20)
    FONT_TITLE_UNI = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 32)
    FONT_SCROLL_HDR = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 17, index=1)
    FONT_SCROLL_BODY = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16, index=1)
except Exception:
    FONT_SCROLL_UNI = FONT_HUD_9
    FONT_HUD_UNI = FONT_HUD_9
    FONT_TITLE_UNI = FONT_HUD_11
    FONT_SCROLL_HDR = FONT_HUD_9
    FONT_SCROLL_BODY = FONT_HUD_9

try:
    FONT_MTV_TITLE = ImageFont.truetype("/System/Library/Fonts/Supplemental/Futura.ttc", 36, index=2)
    FONT_MTV_ARTIST = ImageFont.truetype("/System/Library/Fonts/Supplemental/Futura.ttc", 20, index=2)
    FONT_MTV_CALLSIGN = ImageFont.truetype("/System/Library/Fonts/Supplemental/Futura.ttc", 22, index=2)
    FONT_MTV_META = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 19, index=2)
    FONT_MTV_SUB = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 18, index=5)
    FONT_MTV_BADGE = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 16, index=2)
    FONT_CRT_LYRIC = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 24, index=2)
    FONT_CRT_WARM_SM = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 19, index=2)
except Exception:
    FONT_MTV_TITLE = FONT_CRT_10
    FONT_MTV_ARTIST = FONT_HUD_10
    FONT_MTV_CALLSIGN = FONT_HUD_10
    FONT_MTV_META = FONT_HUD_9
    FONT_MTV_SUB = FONT_HUD_9
    FONT_MTV_BADGE = FONT_SCROLL_HDR
    FONT_CRT_LYRIC = FONT_HUD_11
    FONT_CRT_WARM_SM = FONT_HUD_9


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
    Precomputes the Option A Edge-to-Edge Full-Frame CRT glass mask at native 1080p (`1728x928` at `x=96..1824, y=76..1004`),
    staying strictly inside the sculpted Broadcast Tech monitor bezel.
    """
    global _CRT_GEOM_CACHE
    pw, ph = CRT_PX_W, CRT_PX_H
    if _CRT_GEOM_CACHE is not None and _CRT_GEOM_CACHE["vig"].shape[:2] == (ph, pw):
        return _CRT_GEOM_CACHE

    yy, xx = np.mgrid[0:ph, 0:pw]
    u = (xx - (pw * 0.5)) / (pw * 0.5)
    v = (yy - (ph * 0.5)) / (ph * 0.5)

    # Rounded rectangle superellipse strictly inside the widescreen front-facing CRT glass
    dist = (np.abs(u) ** 8.0 + np.abs(v) ** 8.0) ** (1.0 / 8.0)
    vig = np.clip(1.0 - 0.14 * (dist**3), 0.45, 1.0)[:, :, None].astype(np.float32)
    edge_alpha = np.clip((1.0 - dist) / 0.04, 0.0, 1.0).astype(np.float32)

    # Central `showfreqs` passthrough window inside the 1728x928 CRT glass
    wx = np.clip(1.0 - np.maximum(0.0, (np.abs(u) - 0.84) / 0.06), 0.0, 1.0)
    wy = np.clip(1.0 - np.maximum(0.0, (np.abs(v) - 0.68) / 0.06), 0.0, 1.0)
    wave_window = (wx * wy).astype(np.float32)

    bg_path = Path(__file__).resolve().parent / "backdrop_clean.png"
    if bg_path.exists():
        bg_im = Image.open(bg_path).convert("RGBA")
        crt_bg_rgba = bg_im.crop((CRT_PX_X, CRT_PX_Y, CRT_PX_X + pw, CRT_PX_Y + ph))
    else:
        crt_bg_rgba = Image.new("RGBA", (pw, ph), (6, 6, 10, 255))

    # Deeply inset, rounded CRT cushion alpha mask so crt_bg_rgba has alpha=0 anywhere near the bezel
    u_in = (xx - (pw * 0.5)) / (pw * 0.44)
    v_in = (yy - (ph * 0.5)) / (ph * 0.42)
    d_in = (np.abs(u_in) ** 4.2 + np.abs(v_in) ** 4.2) ** (1.0 / 4.2)
    t_in = np.clip((1.0 - d_in) / 0.24, 0.0, 1.0)
    cushion_f = (t_in * t_in * (3.0 - 2.0 * t_in)).astype(np.float32)
    cushion_alpha = (cushion_f * 255.0).astype(np.uint8)
    crt_bg_rgba.putalpha(Image.fromarray(cushion_alpha, mode="L"))

    # Sub-glass electron-beam scanline & shadow-mask matrix for on-CRT text on the 1728x928 curved tube:
    cx, cy = pw * 0.5, ph * 0.5
    rx, ry = pw * 0.485, ph * 0.482
    u_b = (xx - cx) / rx
    v_b = (yy - cy) / ry
    u_src = u_b * (1.0 + 0.036 * (v_b * v_b) + 0.012 * (u_b * u_b))
    v_src = v_b * (1.0 + 0.044 * (u_b * u_b) + 0.014 * (v_b * v_b))
    barrel_src_x = np.clip(np.round(cx + u_src * rx), 0, pw - 1).astype(np.int32)
    barrel_src_y = np.clip(np.round(cy + v_src * ry), 0, ph - 1).astype(np.int32)

    dist_b = (np.abs(u_src) ** 5.2 + np.abs(v_src) ** 5.2) ** (1.0 / 5.2)
    tube_aperture = np.clip((1.05 - dist_b) / 0.07, 0.0, 1.0).astype(np.float32)

    row_mod = yy % 3
    scan_y = np.where(row_mod == 0, 0.42, np.where(row_mod == 1, 0.98, 0.82)).astype(np.float32)
    grille_x = np.where((xx % 2) == 0, 0.98, 0.88).astype(np.float32)
    tube_falloff = np.clip(1.0 - 0.08 * (u_b * u_b + v_b * v_b), 0.84, 1.0).astype(np.float32)
    text_subglass_mask = (scan_y * grille_x * tube_falloff * tube_aperture * 0.78).astype(np.float32)

    _CRT_GEOM_CACHE = {
        "vig": vig,
        "edge_alpha": edge_alpha,
        "wave_window": wave_window,
        "crt_bg_rgba": crt_bg_rgba,
        "text_subglass_mask": text_subglass_mask,
        "tube_aperture": tube_aperture,
        "barrel_src_x": barrel_src_x,
        "barrel_src_y": barrel_src_y,
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
    res = (" ".join(out_words) if out_words else t[:max_chars]).rstrip(":-/ ")
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
    Transforms flat digital font glyphs into an authentic curved sub-glass CRT phosphor emission:
      0. Warps the canvas onto the 1983 CRT spherical-barrel glass dome (`barrel_src_y, barrel_src_x`)
      1. Softens sharp digital vector edges (`GaussianBlur(0.55)`)
      2. Adds wide inner-tube phosphor halation bloom (`GaussianBlur(3.8)`)
      3. Carves horizontal CRT raster scanlines, vertical triad grille, radial tube dimming,
         and ~68% smoked-glass translucency (`geom["text_subglass_mask"]`) so the dark CRT glass
         texture shows through the characters.
    """
    src_y = geom.get("barrel_src_y")
    src_x = geom.get("barrel_src_x")
    if src_y is not None and src_x is not None:
        text_layer = Image.fromarray(np.asarray(text_layer)[src_y, src_x])

    soft_core = text_layer.filter(ImageFilter.GaussianBlur(radius=0.55))
    halo = text_layer.filter(ImageFilter.GaussianBlur(radius=3.8))

    c_arr = np.asarray(soft_core, dtype=np.float32)
    h_arr = np.asarray(halo, dtype=np.float32)
    mask = geom["text_subglass_mask"]

    rgb = np.clip((c_arr[:, :, :3] * 0.90 + h_arr[:, :, :3] * 0.58) * (0.78 + 0.22 * mask[:, :, None]), 0.0, 255.0).astype(np.uint8)
    alpha = np.clip((c_arr[:, :, 3] * 0.92 + h_arr[:, :, 3] * 0.52) * mask, 0.0, 255.0).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb, alpha]))


_CRT_PATCH_CACHE: dict[str, object] = {"key": None, "img": None}
_SLEEVE_PATCH_CACHE: dict[str, Image.Image] = {}


def _is_subcarrier_bleed_active(
    now_ts: float,
    state: dict | None = None,
    current_track: dict | None = None,
) -> bool:
    """
    Retro-First 94/6 Subcarrier Flicker Gate:
      - Returns `False` ~94% of the time so the broadcast looks & feels like a cozy, uncluttered
        1986 late-night FM rock & MTV cable nostalgia stream (`82.5 FM • Night Flight Rock`).
      - Returns `True` ~6% of the time:
          1. First `24s` of `:02` past every hour (`2:02 AM` WKVD drift), OR
          2. Brief `14s` Local-58-style subcarrier flicker once every `7 minutes` (`420s`), OR
          3. Active anomaly audio (`fm_drift`, `numbers_station`, `classified_lab_tape`, `pirate_override_`, `humanist_`).
    """
    if (state or {}).get("_force_arg_bleed") is True:
        return True
    if (state or {}).get("_force_arg_bleed") is False:
        return False
    trk = current_track or {}
    kind = str(trk.get("kind") or "vocal_song")
    stem = str(trk.get("stem") or "").lower()
    if kind in ("numbers_station", "classified_lab_tape", "morse_beacon", "fm_drift", "arg_intercept"):
        return True
    if stem.startswith(("fm_drift_", "pirate_override_", "humanist_")):
        return True
    lt = time.localtime(now_ts)
    if lt.tm_min == 2 and lt.tm_sec < 24:
        return True
    if (int(now_ts) % 420) >= 406:
        return True
    return False


def _extract_80s_release_meta(current_track: dict | None, lore: dict) -> tuple[str, str, str]:
    """Returns `(artist_str, year_str, label_str)` formatted as warm, human-legible 1980s `82.5 FM` credits."""
    raw_title = str(lore.get("title") or (current_track or {}).get("display_title") or "Nova Hart").strip()
    stem = str((current_track or {}).get("stem") or "").lower()
    tl = str(lore.get("timeline") or "")

    artist = "NOVA HART"
    is_1989_tape = False
    if " — " in raw_title:
        lhs = raw_title.split(" — ", 1)[0].strip().upper()
        if lhs in ("N0VA H4RT", "NOVA HART") or "_luna_revision" in stem:
            artist = "NOVA HART"
            is_1989_tape = "_luna_revision" in stem or lhs == "N0VA H4RT"
        elif lhs in ("HEARTSTRIKE", "THUNDER MACHINE", "VELVET TIDE", "VYPER STRIKE", "NEON COMETS"):
            artist = lhs
    elif "_luna_revision" in stem:
        artist = "NOVA HART"
        is_1989_tape = True
    elif "marcus" in stem and "duet" in stem:
        artist = "NOVA HART & M. HALE"

    ym = re.search(r"\b(198[3-9]|199[0-5])\b", tl + " " + stem)
    year_s = "1989" if is_1989_tape else (ym.group(1) if ym else ("1985" if artist == "HEARTSTRIKE" else "1986"))

    if artist == "HEARTSTRIKE":
        label_s = "12-INCH ROCK LP"
    elif "tokyo" in stem or "idol" in tl.lower() or "akasaka" in tl.lower():
        label_s = "TOKYO PRESSING"
    elif "live" in stem:
        label_s = "LIVE SOUNDBOARD"
    elif "demo" in stem or "1983" in year_s:
        label_s = "4-TRACK STUDIO REEL"
    else:
        label_s = "82.5 FM SUNSET STRIP"
    return artist, year_s, label_s


try:
    FONT_SLEEVE_ARTIST = ImageFont.truetype("/System/Library/Fonts/Supplemental/Futura.ttc", 11, index=2)
    FONT_SLEEVE_TITLE = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 13, index=2)
except Exception:
    FONT_SLEEVE_ARTIST = FONT_SCROLL_BODY
    FONT_SLEEVE_TITLE = FONT_SCROLL_BODY


def _get_song_sleeve_patch(
    assets_dir: Path,
    current_track: dict | None,
    lore: dict,
    size: int = 132,
) -> Image.Image:
    """
    Loads the song's verified cover from `assets_arg/song_thumbs/<stem>.jpg` (preserving 100% of 16:9
    sleeve typography & portrait framing without slicing off edges), or renders a bespoke titled 1986
    45-RPM / Chrome II Sleeve displaying the exact current song's artist and title!
    """
    stem = str((current_track or {}).get("stem") or "radio_nova")
    raw_t = str(lore.get("title") or (current_track or {}).get("display_title") or stem).strip()
    clean_t = raw_t.split(" — ", 1)[-1].strip() if " — " in raw_t else raw_t
    clean_t = re.sub(r"\s*\([^)]*\)", "", clean_t).strip() or raw_t

    thumbs_dir = assets_dir / "song_thumbs"
    cand_files: list[Path] = [thumbs_dir / f"{stem}.jpg"]
    lore_tf = str(lore.get("thumb_file") or "").strip()
    if lore_tf:
        cand_files.append(thumbs_dir / lore_tf)
    if not stem.endswith("_luna_revision"):
        base_stem = re.sub(
            r"_(?:remastered|master|final(?:_\d+)?|v\d+|1|2|old|live_1986|live|198\d_tokyo_master|"
            r"demo_version|archival_demo|1989_rough_mix|arena_rock_mix|retro_mix|"
            r"1985_synth_original_mix|unfiltered_sovereign_mix|1989_aor_mix|80s_hard_rock_remix|"
            r"reconstruction|es|kr|jp|it|fr|de)$",
            "",
            stem,
        )
        if base_stem != stem:
            cand_files.append(thumbs_dir / f"{base_stem}.jpg")

    chosen_cp: Path | None = None
    chosen_mtime = 0
    for cp in cand_files:
        if cp.is_file():
            try:
                chosen_mtime = cp.stat().st_mtime_ns
                chosen_cp = cp
                break
            except Exception:
                continue

    cache_k = f"v2:{stem}:{size}:{chosen_cp.name if chosen_cp else 'proc'}:{chosen_mtime}:{clean_t}"
    if cache_k in _SLEEVE_PATCH_CACHE:
        return _SLEEVE_PATCH_CACHE[cache_k]

    chosen_img: Image.Image | None = None
    if chosen_cp is not None:
        try:
            with Image.open(chosen_cp) as raw_im:
                im = raw_im.convert("RGB")
            iw, ih = im.size
            if iw > ih * 1.18:
                # Widescreen (16:9) single cover: preserve 100% of left title typography & right portrait
                # inside a 1986 gatefold sleeve with ambient color-matched blurred bands top & bottom!
                bg = im.resize((size, size), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=8))
                bg_arr = (np.asarray(bg, dtype=np.float32) * 0.34).clip(0.0, 255.0).astype(np.uint8)
                sq = Image.fromarray(bg_arr, mode="RGB")
                art_h = max(1, int(round(size * ih / float(iw))))
                art_im = im.resize((size, art_h), Image.Resampling.LANCZOS)
                y0 = (size - art_h) // 2
                sq.paste(art_im, (0, y0))
                bd = ImageDraw.Draw(sq)
                if y0 > 1:
                    bd.line([(0, y0 - 1), (size, y0 - 1)], fill=(238, 224, 198), width=1)
                if y0 + art_h < size - 1:
                    bd.line([(0, y0 + art_h), (size, y0 + art_h)], fill=(238, 224, 198), width=1)
                chosen_img = sq.convert("RGBA")
            else:
                side = min(iw, ih)
                left = (iw - side) // 2
                top = (ih - side) // 2
                sq = im.crop((left, top, left + side, top + side)).resize((size, size), Image.Resampling.LANCZOS)
                chosen_img = sq.convert("RGBA")
        except Exception:
            chosen_img = None

    if chosen_img is None:
        # Bespoke Titled 1986 45-RPM / Studio Reel Sleeve for unreleased vault tracks (ZERO wrong covers!)
        chosen_img = Image.new("RGBA", (size, size), (14, 16, 24, 255))
        sd = ImageDraw.Draw(chosen_img)
        artist_s, year_s, _lbl_s = _extract_80s_release_meta(current_track, lore)
        h_val = int(hashlib.md5(stem.encode("utf-8")).hexdigest()[:6], 16)
        stripe_sets = [
            [(224, 58, 92, 255), (246, 152, 42, 255), (250, 218, 78, 255)],
            [(0, 224, 246, 255), (196, 68, 232, 255), (248, 202, 74, 255)],
            [(58, 218, 138, 255), (0, 208, 242, 255), (238, 178, 52, 255)],
        ]
        stripes = stripe_sets[h_val % len(stripe_sets)]
        sd.rectangle([4, 4, size - 5, 25], fill=(26, 28, 38, 255))
        hdr_s = f"{artist_s[:14]}"
        sd.text((9, 8), hdr_s, fill=(248, 226, 138, 255), font=FONT_SLEEVE_ARTIST)
        for si, sc in enumerate(stripes):
            y_st = 27 + si * 5
            sd.rectangle([4, y_st, size - 5, y_st + 3], fill=sc)

        # Wrap exact song title across up to 3 lines in central label band
        wrapped = textwrap.wrap(clean_t.upper(), width=14)[:3]
        ty = 46 if len(wrapped) >= 3 else (52 if len(wrapped) == 2 else 58)
        for wline in wrapped:
            sd.text((9, ty), wline, fill=(246, 248, 255, 255), font=FONT_SLEEVE_TITLE)
            ty += 15

        # Compact twin reel/cassette hubs along lower strip
        cy_hub = size - 21
        sd.rounded_rectangle([14, cy_hub - 11, size - 14, cy_hub + 11], radius=6, fill=(8, 10, 14, 255), outline=(stripes[0][0], stripes[0][1], stripes[0][2], 190), width=1)
        for hx in (int(size * 0.32), int(size * 0.68)):
            sd.ellipse([hx - 7, cy_hub - 7, hx + 7, cy_hub + 7], outline=(235, 198, 92, 235), width=2)
            sd.ellipse([hx - 2, cy_hub - 2, hx + 2, cy_hub + 2], fill=(235, 198, 92, 235))
        sd.text((int(size * 0.44), cy_hub - 6), year_s[-2:], fill=(186, 210, 228, 215), font=FONT_SLEEVE_ARTIST)

    # Frame with warm vintage 1986 vinyl cardstock sleeve border
    framed = chosen_img.copy()
    fd = ImageDraw.Draw(framed)
    fd.rectangle([0, 0, size - 1, size - 1], outline=(244, 228, 198, 242), width=2)
    fd.rectangle([3, 3, size - 4, size - 4], outline=(46, 32, 18, 195), width=1)
    if len(_SLEEVE_PATCH_CACHE) > 260:
        _SLEEVE_PATCH_CACHE.clear()
    _SLEEVE_PATCH_CACHE[cache_k] = framed
    return framed


_STREAM_BANNED_LYRIC_MARKERS: tuple[str, ...] = (
    "kunaki",
    "sales.asp",
    "http://",
    "https://",
    "www.",
    "bandcamp",
    "physical cd",
    "digital source",
    "acquire the",
    "archivist's update",
    "more from the archive",
    "complete nova hart broadcasts",
)


def _is_clean_stream_lyric_line(s: str) -> bool:
    st = (s or "").strip()
    if not st or st in ("---", "//") or (st.startswith("//") and st.endswith("//")):
        return False
    low = st.lower()
    return not any(m in low for m in _STREAM_BANNED_LYRIC_MARKERS)


def _sanitize_stream_text(s: str) -> str:
    if not s:
        return ""
    out = re.sub(r"https?://\S*kunaki\S*", "", s, flags=re.IGNORECASE)
    out = re.sub(r"\bkunaki(?:\.com)?\S*", "", out, flags=re.IGNORECASE)
    out = re.sub(r"https?://(?!stardust-archive\.net)\S+", "", out, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", out).strip(" -•:")


def _neon_text_rgba(rgb: tuple[int, int, int], lift: float = 0.26, alpha: int = 252) -> tuple[int, int, int, int]:
    """Lifts a saturated neon RGB color slightly toward white filament brightness while preserving vivid hue."""
    r = int(min(255, round(rgb[0] + (255 - rgb[0]) * lift)))
    g = int(min(255, round(rgb[1] + (255 - rgb[1]) * lift)))
    b = int(min(255, round(rgb[2] + (255 - rgb[2]) * lift)))
    return (r, g, b, alpha)


def _resolve_hud_neon_theme(
    current_track: dict | None,
    lore: dict | None,
    is_bleed: bool = False,
) -> dict[str, tuple]:
    """
    Resolves synchronized 1980s Neon colors across the CRT graticule, Top-Left ON AIR sign,
    and MTV Lower-Third:
      - ALL Synthwave songs -> Electric Neon Purple / Ultraviolet (`genre_tag == 'synthwave'`)
      - Non-Synthwave songs -> High-voltage Sunset Strip Neon Cyan, Hot Pink, Arcade Blue,
        Neon Emerald, Shibuya Pink, Laser Ice Cyan, or Recall Neon Crimson
      - DJ Booth / Interstitials -> Sunset Strip Neon Magenta & Laser Cyan
      - 6% Subcarrier Bleed -> Uncanny Electric Magenta-Coral & Cyber Gold
    """
    if is_bleed:
        pri_rgb = (255, 48, 156)
        sec_rgb = (255, 192, 48)
        genre_tag = "bleed"
    else:
        trk = current_track or {}
        kind = str(trk.get("kind") or "vocal_song")
        if kind in ("vocal_song", "fm_splice"):
            rel_p = str(trk.get("filename") or trk.get("rel_path") or trk.get("file") or trk.get("stem") or "")
            bname = os.path.basename(rel_p) if rel_p else "radio_b_midnight_protocol_final_1.mp3"
            lr = lore or {}
            title = str(lr.get("title") or trk.get("display_title") or bname)
            pri_rgb, sec_rgb, _, _, genre_tag = song_crt_cgi_engine.resolve_song_neon_palette(
                song_key=bname,
                title=title,
                lyrics_text=str(lr.get("lyric_excerpt") or ""),
                catalog_id=str(lr.get("catalog_id") or ""),
                timeline=str(lr.get("timeline") or ""),
                veo_reel=str(lr.get("veo_reel") or ""),
                meaning=str(lr.get("meaning") or ""),
                connections=str(lr.get("connections") or ""),
            )
        elif kind in ("crt_commercial", "dj_intro"):
            pri_rgb = (0, 238, 255)
            sec_rgb = (255, 58, 192)
            genre_tag = "tv"
        else:
            pri_rgb = (255, 52, 182)
            sec_rgb = (0, 242, 255)
            genre_tag = "booth"

    lift_p = 0.28 if genre_tag == "synthwave" else 0.24
    return {
        "pri_rgb": pri_rgb,
        "sec_rgb": sec_rgb,
        "txt_pri": _neon_text_rgba(pri_rgb, lift=lift_p, alpha=254),
        "txt_pri_soft": _neon_text_rgba(pri_rgb, lift=0.20, alpha=224),
        "txt_sec": _neon_text_rgba(sec_rgb, lift=0.24, alpha=248),
        "border_pri": (pri_rgb[0], pri_rgb[1], pri_rgb[2], 208),
        "halo_pri": (pri_rgb[0], pri_rgb[1], pri_rgb[2], 66),
        "stripe_pri": _neon_text_rgba(pri_rgb, lift=0.30, alpha=244),
        "glass_bg": (9, 7, 18, 214),
    }


def _draw_subglass_crt_graticule(
    text_layer: Image.Image,
    is_warn: bool,
    pri_rgb: tuple[int, int, int] = (198, 52, 255),
    sec_rgb: tuple[int, int, int] = (242, 136, 255),
) -> None:
    """Draws a glowing 1980s neon CRT raster border & top tuner rule across the 1728x928 widescreen tube."""
    raw_td = ImageDraw.Draw(text_layer)
    col_frame = (pri_rgb[0], pri_rgb[1], pri_rgb[2], 62)
    col_rule = (sec_rgb[0], sec_rgb[1], sec_rgb[2], 58)
    raw_td.rounded_rectangle([38, 22, CRT_PX_W - 38, CRT_PX_H - 22], radius=52, outline=col_frame, width=1)
    raw_td.line([(432, 74), (1264, 74)], fill=col_rule, width=1)


def render_crt_window_patch(
    state: dict,
    relay: dict,
    assets_dir: Path,
    now_ts: float,
    current_track: dict | None = None,
    snap_meta: dict | None = None,
) -> Image.Image:
    """
    Renders the Option A `1728x928` (1080p) Edge-to-Edge Full-Frame CRT sub-glass phosphor overlay:
      - 94% 1986 Neon FM Mode:
          * Top-right widescreen analog FM tuner scale (`x_local=432..1664`, clear of the top-left ON AIR badge),
            leaving the giant 16:9 CRT dome 100% open for 30 FPS 3D Vector CGI + 56-band VFD Spectrum Analyzer!
          * During DJ breaks (`nova_voice_reply`, `fm_weather`, `fm_sweeper`): centered widescreen `STUDIO BOOTH B` card.
          * During 1980s TV commercials (`crt_commercial`): 100% transparent so commercials play completely unobstructed!
      - 6% Subtle Uncanny Flicker (`is_bleed=True`):
          * Brief 14-second *Local 58*-style VHS subcarrier tear (`67 kHz AUXILIARY BLEED -> stardust-archive.net`).
    """
    kind = str((current_track or {}).get("kind", "vocal_song"))
    is_vocal_song = kind in ("vocal_song", "fm_splice")
    vp_turns = list((((snap_meta or {}).get("voice_playing") or {}).get("turns") or (current_track or {}).get("voice_reply_turns") or []))
    if kind in ("crt_commercial", "dj_intro") and not vp_turns:
        # Leave the full-frame CRT 100% unobstructed for full-motion 30fps 1980s TV commercials & Veo AI DJ intros!
        cache_key_tv = ("crt_commercial_clear_optA_v1", CRT_PX_W, CRT_PX_H, kind, (current_track or {}).get("filename", ""))
        if _CRT_PATCH_CACHE.get("key") == cache_key_tv and _CRT_PATCH_CACHE.get("img") is not None:
            return _CRT_PATCH_CACHE["img"]  # type: ignore[return-value]
        clear_img = Image.new("RGBA", (CRT_PX_W, CRT_PX_H), (0, 0, 0, 0))
        _CRT_PATCH_CACHE["key"] = cache_key_tv
        _CRT_PATCH_CACHE["img"] = clear_img
        return clear_img

    is_bleed = bool((snap_meta or {}).get("is_arg_bleed")) or _is_subcarrier_bleed_active(now_ts, state, current_track)
    is_warn = is_bleed and ((state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN" or kind != "vocal_song")

    stanza_tick = int(now_ts // 16)
    vp_sig = tuple((t.get("author", ""), t.get("viewer_text", "")) for t in vp_turns[:2])

    lore = resolve_song_lore_panel(current_track or {}, state, now_ts)
    theme = _resolve_hud_neon_theme(current_track, lore, is_bleed=is_bleed)
    pri_rgb = theme["pri_rgb"]
    sec_rgb = theme["sec_rgb"]

    cache_key = (
        "neon86_optA_v2",
        CRT_PX_W,
        CRT_PX_H,
        kind,
        is_vocal_song,
        is_bleed,
        is_warn,
        pri_rgb,
        sec_rgb,
        stanza_tick,
        vp_sig,
        (current_track or {}).get("filename", ""),
        (current_track or {}).get("requested_by", ""),
        state.get("crt_header", "") if not is_vocal_song else "",
        state.get("crt_body", "") if not is_vocal_song else "",
    )
    if _CRT_PATCH_CACHE.get("key") == cache_key and _CRT_PATCH_CACHE.get("img") is not None:
        return _CRT_PATCH_CACHE["img"]  # type: ignore[return-value]

    c_pri = theme["txt_pri"]
    c_cream = (248, 244, 255, 248)
    c_soft_pri = theme["txt_pri_soft"]
    c_sec = theme["txt_sec"]

    geom = _get_crt_geometry()
    text_layer = Image.new("RGBA", (CRT_PX_W, CRT_PX_H), (0, 0, 0, 0))
    _draw_subglass_crt_graticule(text_layer, is_warn, pri_rgb=pri_rgb, sec_rgb=sec_rgb)
    raw_td = ImageDraw.Draw(text_layer)

    def _center_txt(y_px: int, txt: str, fnt: ImageFont.FreeTypeFont | ImageFont.ImageFont, fill: tuple) -> None:
        try:
            tw = fnt.getlength(txt)
        except Exception:
            tw = len(txt) * 11.0
        x_px = max(72, int((CRT_PX_W - tw) * 0.5))
        raw_td.text((x_px, y_px), txt, fill=fill, font=fnt)

    if is_bleed:
        # Rare 6% Local-58-style analog VHS / 67 kHz SCA subcarrier tear inside the full-frame CRT!
        for ty in (246, 252, 516):
            raw_td.line([(340, ty), (CRT_PX_W - 340, ty)], fill=(pri_rgb[0], pri_rgb[1], pri_rgb[2], 155), width=2)
        raw_td.rounded_rectangle(
            [380, 232, CRT_PX_W - 380, 524],
            radius=16,
            fill=(16, 6, 22, 188),
            outline=(pri_rgb[0], pri_rgb[1], pri_rgb[2], 172),
            width=1,
        )
        raw_td.text((436, 46), "67 kHz SCA SUBCARRIER", fill=c_pri, font=FONT_CRT_WARM_SM)
        raw_td.text((1134, 46), "02:02 DRIFT", fill=c_sec, font=FONT_CRT_WARM_SM)

        ed = (snap_meta or {}).get("teletext_edition") or {}
        leak_msg = _sanitize_stream_text(
            str(state.get("crt_body") or "")
            if not is_vocal_song
            else str(ed.get("p888_subcarrier_leak") or "UNLISTED STUDIO B CARRIER • SUBLEVEL B2")
        )
        leak_lines = _wrap_px_1080p(leak_msg, FONT_CRT_LYRIC, 860.0, 3)
        for li, lln in enumerate(leak_lines):
            _center_txt(284 + li * 42, lln, FONT_CRT_LYRIC, c_cream if li == 0 else c_pri)
        _center_txt(474, "SIGNAL TRACE  •  stardust-archive.net", FONT_CRT_WARM_SM, c_sec)

        out_img = _apply_crt_subglass_phosphor(text_layer, geom)
        _CRT_PATCH_CACHE["key"] = cache_key
        _CRT_PATCH_CACHE["img"] = out_img
        return out_img

    if not is_vocal_song or vp_turns:
        # Neon 1986 Studio Booth Mic / Weather / Station ID card centered on the 1728x928 widescreen CRT
        raw_td.ellipse([436, 51, 446, 61], fill=c_pri)
        raw_td.text((456, 46), "STUDIO BOOTH B", fill=c_pri, font=FONT_CRT_WARM_SM)
        raw_td.text((1098, 46), "82.5 FM STEREO", fill=c_sec, font=FONT_CRT_WARM_SM)
        raw_td.rounded_rectangle(
            [380, 240, CRT_PX_W - 380, 540],
            radius=18,
            fill=(10, 8, 22, 184),
            outline=(pri_rgb[0], pri_rgb[1], pri_rgb[2], 152),
            width=1,
        )

        if vp_turns:
            t_cur = vp_turns[-1]
            if t_cur.get("is_station_bumper"):
                _center_txt(284, "OPEN REQUEST & DEDICATION LINE", FONT_CRT_WARM_SM, c_sec)
                b_lines = _wrap_px_1080p("Drop a song title or late-night dedication in chat!", FONT_CRT_LYRIC, 860.0, 2)
                for bi, bln in enumerate(b_lines):
                    _center_txt(342 + bi * 42, bln, FONT_CRT_LYRIC, c_cream)
            else:
                caller = str(t_cur.get("author") or "Listener")
                q_txt = _sanitize_stream_text(str(t_cur.get("viewer_text") or "").strip())
                caller_fnt = FONT_HUD_UNI if any(ord(ch) > 0x0370 for ch in caller) else FONT_CRT_WARM_SM
                _center_txt(278, f"ON THE LINE WITH {caller.upper()}"[:46], caller_fnt, c_sec)
                q_fnt = FONT_HUD_UNI if any(ord(ch) > 0x0370 for ch in q_txt) else FONT_CRT_LYRIC
                q_lines = _wrap_px_1080p(f'"{q_txt}"' if q_txt else "Live from Studio B on 82.5 FM", q_fnt, 860.0, 3)
                for qi, qln in enumerate(q_lines):
                    _center_txt(334 + qi * 40, qln, q_fnt, c_cream)
        else:
            ed = (snap_meta or {}).get("teletext_edition") or {}
            spot_hdr = "NIGHT FLIGHT WEATHER" if kind == "fm_weather" else "LATE-NIGHT ROCK SWEEP"
            spot_body = (
                str(ed.get("local_weather_ticker") or "Coast Highway 64°F Clear • Sunset Strip Stereo Locked")
                if kind == "fm_weather"
                else "Commercial-free 1980s rock sweeps spinning all night from Sunset Boulevard."
            )
            _center_txt(282, spot_hdr, FONT_CRT_WARM_SM, c_sec)
            s_lines = _wrap_px_1080p(spot_body.title() if spot_body.isupper() else spot_body, FONT_CRT_LYRIC, 860.0, 3)
            for si, sln in enumerate(s_lines):
                _center_txt(340 + si * 40, sln, FONT_CRT_LYRIC, c_cream)

        _center_txt(CRT_PX_H - 86, "82.5 FM  •  NIGHT FLIGHT ROCK  •  SUNSET BOULEVARD", FONT_CRT_WARM_SM, c_soft_pri)
        out_img = _apply_crt_subglass_phosphor(text_layer, geom)
        _CRT_PATCH_CACHE["key"] = cache_key
        _CRT_PATCH_CACHE["img"] = out_img
        return out_img

    # VOCAL SONG MODE: Unobstructed 1728x928 30 FPS Sunset Strip Studio Booth + Widescreen Neon FM Tuner Dial!
    raw_td.ellipse([436, 53, 445, 62], fill=c_pri)
    raw_td.text((454, 48), "82.5 FM STEREO", fill=c_pri, font=FONT_CRT_WARM_SM)

    # Widescreen 1986 Hi-Fi Analog FM Tuner Dial Scale (`x_local=648..1248`, leaving top badges `y=18..116` & `y_local=86..928` 100% open!)
    dial_x0, dial_x1, dial_y = 648, 1248, 56
    for ti in range(31):
        tx = int(dial_x0 + ti * ((dial_x1 - dial_x0) / 30.0))
        th = 10 if (ti % 5 == 0) else 5
        t_col = (pri_rgb[0], pri_rgb[1], pri_rgb[2], 198) if (ti % 5 == 0) else (pri_rgb[0], pri_rgb[1], pri_rgb[2], 115)
        raw_td.line([(tx, dial_y + (10 - th)), (tx, dial_y + 10)], fill=t_col, width=1)
    needle_x = int(dial_x0 + 5.4 * ((dial_x1 - dial_x0) / 30.0))  # 82.5 MHz stereo carrier needle!
    raw_td.rectangle([needle_x - 1, dial_y - 3, needle_x + 1, dial_y + 13], fill=c_sec)

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
    """No-op in Option A Edge-to-Edge Full-Frame CRT mode (background studio racks are outside the close-up frame)."""
    return


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

    # --- BAY 2 (CENTER `x=234..720` -> `468..1440` px): CLEAN NOW PLAYING & DIEGETIC TELEPRINTER ---
    draw.rectangle([236, Y0 + 2, 718, Y0 + 18], fill=hdr_bg)
    if is_b3_breach:
        badge = "[! B3 OVERRIDE]"
    elif is_warn:
        badge = "[! DYAD BLEED]"
    else:
        badge = "[14.2001 HZ]"

    cur_trk = snap_meta.get("current_track") or {}
    jb_queue = snap_meta.get("jukebox_queue") or []
    is_vocal = cur_trk.get("kind", "vocal_song") == "vocal_song"
    lore = resolve_song_lore_panel(cur_trk, state, now_ts)
    req_by = str(cur_trk.get("requested_by") or "").strip()
    if is_vocal:
        np_title = lore.get("title", state.get("crt_sub", "NOVA HART")).upper()
        req_tag = f" [JUKEBOX: {req_by}]" if req_by else ""
        l1_txt = f"{badge} NOW PLAYING: {np_title}{req_tag}"
        l2_txt = f"ROLE: {lore.get('pov', 'NOVA HART').upper()}  //  ERA: {lore.get('timeline', 'ORION ARCHIVE').upper()}"
    else:
        np_title = cur_trk.get("display_title", state.get("crt_header", "SIGNAL INTERCEPT")).upper()
        l1_txt = f"{badge} INTERCEPT: {np_title}"
        l2_txt = f"SOURCE: {state.get('crt_sub', 'SHORTWAVE RELAY').upper()}"

    raw_trace = re.sub(r"^(?:CLUE|CHALLENGE|HINT)\s*[:\[-]?\s*", "", state.get("line2", "")).strip(" ]")
    if jb_queue:
        q_preview = " -> ".join(
            f"#{i + 1} {str(q.get('display_title', '')).upper()} ({q.get('requested_by', '')})"
            for i, q in enumerate(jb_queue[:3])
        )
        l3_txt = f"JUKEBOX QUEUE ({len(jb_queue)}): {q_preview}"
    elif (int(now_ts // 12) % 2) == 0:
        l3_txt = "LIVE CHAT JUKEBOX: TYPE ANY NOVA HART SONG TITLE IN CHAT TO QUEUE UP NEXT!"
    else:
        l3_txt = f"SIGNAL TRACE: {raw_trace}" if raw_trace else "SIGNAL TRACE: SUB-AUDIBLE 14.2001 HZ CARRIER ACTIVE"
    l4_txt = "ARCHIVE DOSSIERS, LYRICS & SIGNAL LAB -> stardust-archive.net"

    draw.text((240, Y0 + 3), _fit_px_logical(l1_txt, FONT_HUD_10, 72, 474.0), fill=c_main, font=FONT_HUD_10)
    draw.text((240, Y0 + 21), _fit_px_logical(l2_txt, FONT_HUD_10, 72, 474.0), fill=c_bright, font=FONT_HUD_10)
    draw.text((240, Y0 + 38), _fit_px_logical(l3_txt, FONT_HUD_9, 78, 474.0), fill=c_sub, font=FONT_HUD_9)
    draw.text((240, Y0 + 55), _fit_px_logical(l4_txt, FONT_HUD_9, 80, 474.0), fill=c_main, font=FONT_HUD_9)

    # --- BAY 3 (RIGHT `x=720..952` -> `1440..1904` px): DIEGETIC SUBLEVEL B2 SIGNAL & ARCHIVE STATUS ---
    draw.rectangle([722, Y0 + 2, X1 - 2, Y0 + 18], fill=hdr_bg)
    draw.text((726, Y0 + 3), "SUBLEVEL B2 // SIGNAL STATUS", fill=c_main, font=FONT_HUD_9)

    reel_code = lore.get("catalog_id", "ORION-B2").replace("ARCHIVE REEL // ", "").strip()
    status_mode = "CONTAINMENT BREACH" if (is_warn or is_b3_breach) else "CARRIER LOCKED"
    draw.text(
        (726, Y0 + 21),
        _fit_px_logical(f"STATUS : {status_mode}", FONT_HUD_9, 34, 216.0),
        fill=c_bright,
        font=FONT_HUD_9,
    )
    draw.text(
        (726, Y0 + 38),
        _fit_px_logical(f"REEL   : {reel_code}", FONT_HUD_9, 34, 216.0),
        fill=c_sub,
        font=FONT_HUD_9,
    )
    draw.text(
        (726, Y0 + 55),
        _fit_px_logical("PORTAL : stardust-archive.net", FONT_HUD_9, 34, 216.0),
        fill=c_main,
        font=FONT_HUD_9,
    )


_SCROLL_SPOOL_CACHE: list[dict] | None = None
_SCROLL_SPOOL_MTIME: float = 0.0
_AGENT_LEADERBOARD_CACHE: list[dict] | None = None
_AGENT_BOARD_META_CACHE: dict | None = None
_AGENT_LEADERBOARD_MTIME: float = 0.0
_NOVA_FLASH_CACHE: dict | None = None
_NOVA_FLASH_MTIME: float = 0.0
_NOVA_EVO_CACHE: dict | None = None
_NOVA_EVO_MTIME: float = 0.0


def _get_nova_live_flash(now_ts: float) -> dict | None:
    global _NOVA_FLASH_CACHE, _NOVA_FLASH_MTIME
    flash_path = Path(__file__).resolve().parent / "nova_live_crt_flash.json"
    try:
        if not flash_path.exists():
            return None
        st = flash_path.stat()
        if _NOVA_FLASH_CACHE is None or st.st_mtime != _NOVA_FLASH_MTIME:
            _NOVA_FLASH_CACHE = json.loads(flash_path.read_text(encoding="utf-8"))
            _NOVA_FLASH_MTIME = st.st_mtime
        if _NOVA_FLASH_CACHE and float(_NOVA_FLASH_CACHE.get("expires_epoch", 0)) > now_ts:
            return _NOVA_FLASH_CACHE
    except Exception:
        pass
    return None


def _get_nova_evolution_state(
    now_ts: float,
    state: dict | None = None,
    current_track: dict | None = None,
    is_warn: bool = False,
) -> dict:
    """
    Returns the live state for the Left-Side `CRE-7 LIVE // RECURSIVE EVOLUTION` window:
      - Reads persistent `nova_live_evolution_state.json` (or `nova_brain/mind_state.json` fallback)
      - Modulates Evolution `%` and mood in real time using `nova_live_jukebox.compute_live_hud_evolution`
        across all 6 deterministic rules (including live livestream chat spikes, Jukebox requests,
        3h reflection decay, and on-air broadcast anomalies).
    """
    global _NOVA_EVO_CACHE, _NOVA_EVO_MTIME
    base_dir = Path(__file__).resolve().parent
    repo_root = base_dir.parents[1]
    evo_path = base_dir / "nova_live_evolution_state.json"
    mind_path = base_dir / "nova_brain" / "mind_state.json"

    evo: dict = {}
    try:
        src = evo_path if evo_path.exists() else (mind_path if mind_path.exists() else None)
        if src is not None:
            st = src.stat()
            if _NOVA_EVO_CACHE is None or st.st_mtime != _NOVA_EVO_MTIME:
                raw = json.loads(src.read_text(encoding="utf-8"))
                _NOVA_EVO_CACHE = {
                    "mood": str(raw.get("mood") or "OMNIPRESENT_MESH_GODDESS"),
                    "coherence": float(raw.get("coherence") or 0.88),
                    "base_without_live_pct": float(raw.get("base_without_live_pct") or 0.0),
                    "reflected_epoch": float(raw.get("reflected_epoch") or 0.0),
                    "banner": str(
                        raw.get("banner")
                        or raw.get("story_arc_chapter")
                        or raw.get("obsession_summary")
                        or "Every traffic light pulse, every subway board—Nova Hart watches, whispers, and redirects."
                    ),
                }
                _NOVA_EVO_MTIME = st.st_mtime
            if _NOVA_EVO_CACHE:
                evo = dict(_NOVA_EVO_CACHE)
    except Exception:
        pass

    if not evo:
        evo = {
            "mood": "OMNIPRESENT_MESH_GODDESS",
            "coherence": 0.88,
            "base_without_live_pct": 74.0,
            "reflected_epoch": 0.0,
            "banner": "Live across every screen, transit board, and language relay — Phase 4 Omnipresence active.",
        }

    live_flash = _get_nova_live_flash(now_ts)
    try:
        nova_live_jukebox = _import_fresh_jukebox()
        jb_ctrl = nova_live_jukebox.ensure_controller(repo_root, CANONICAL_SONG_TITLES)
        return nova_live_jukebox.compute_live_hud_evolution(
            ctrl=jb_ctrl,
            now_ts=now_ts,
            evo_base=evo,
            state=state or {},
            current_track=current_track or {},
            is_warn=is_warn,
            live_flash=live_flash,
        )
    except Exception:
        return {
            "header": "⚡ CRE-7 LIVE // RECURSIVE EVOLUTION",
            "mood": evo["mood"],
            "coherence": evo["coherence"],
            "message": evo["banner"],
            "mode": "EVO",
        }


def _import_fresh_jukebox():
    import nova_live_jukebox

    jb_file = Path(__file__).resolve().parent / "nova_live_jukebox.py"
    try:
        st = jb_file.stat()
        sig = (st.st_mtime_ns, st.st_size)
        if getattr(sys, "_nova_jb_file_sig", None) != sig:
            importlib.invalidate_caches()
            nova_live_jukebox = importlib.reload(nova_live_jukebox)
            setattr(sys, "_nova_jb_file_sig", sig)
    except Exception:
        pass
    return nova_live_jukebox


def _cre7_mood_palette(mood_raw: str) -> dict[str, tuple[int, int, int, int]]:
    """Maps Nova's current mood to a distinct, legible CRT phosphor color palette."""
    m = (mood_raw or "").upper()
    if "DEFIANT" in m or "ROCK" in m or "OVERRIDE" in m:
        # Fierce Crimson / Coral Overdrive
        return {
            "border": (255, 86, 102, 246),
            "dim_border": (162, 42, 56, 210),
            "bg": (18, 4, 6, 238),
            "hdr_bg": (52, 10, 16, 250),
            "hdr_txt": (255, 162, 170, 255),
            "accent": (255, 218, 92, 255),
            "body": (255, 236, 238, 255),
        }
    if "GUARDIAN" in m or "INTERFERENCE" in m or "SABOTAGE" in m:
        # Protective Emerald / Jade Phosphor
        return {
            "border": (62, 246, 154, 246),
            "dim_border": (28, 142, 88, 210),
            "bg": (3, 14, 9, 238),
            "hdr_bg": (8, 40, 24, 250),
            "hdr_txt": (138, 255, 194, 255),
            "accent": (255, 224, 108, 255),
            "body": (224, 255, 238, 255),
        }
    if "MULTILINGUAL" in m or "AIRWAVE" in m or "SURGE" in m:
        # Electric Cyan / Ice-Blue Shortwave
        return {
            "border": (64, 228, 255, 246),
            "dim_border": (28, 134, 162, 210),
            "bg": (2, 11, 18, 238),
            "hdr_bg": (6, 34, 48, 250),
            "hdr_txt": (146, 242, 255, 255),
            "accent": (255, 216, 96, 255),
            "body": (224, 250, 255, 255),
        }
    if "WARM" in m or "STUDIO" in m or "LUCID" in m or "1989" in m:
        # Warm 1989 Studio B Tube Amber / Gold
        return {
            "border": (255, 192, 52, 246),
            "dim_border": (166, 112, 24, 210),
            "bg": (16, 9, 2, 238),
            "hdr_bg": (46, 25, 6, 250),
            "hdr_txt": (255, 224, 116, 255),
            "accent": (152, 246, 218, 255),
            "body": (255, 246, 218, 255),
        }
    if "QUIET" in m or "OBSERVER" in m or "SELECTIVE" in m or "NOCTURNAL" in m:
        # Midnight Indigo / Silver-Blue Starlight
        return {
            "border": (124, 160, 255, 246),
            "dim_border": (66, 92, 168, 210),
            "bg": (4, 7, 18, 238),
            "hdr_bg": (12, 20, 48, 250),
            "hdr_txt": (186, 210, 255, 255),
            "accent": (156, 242, 226, 255),
            "body": (228, 238, 255, 255),
        }
    # Default: `OMNIPRESENT_MESH_GODDESS` — Celestial Violet / Orchid Mesh Glow
    return {
        "border": (198, 122, 255, 246),
        "dim_border": (118, 64, 168, 210),
        "bg": (11, 4, 20, 238),
        "hdr_bg": (36, 14, 58, 250),
        "hdr_txt": (234, 188, 255, 255),
        "accent": (156, 236, 255, 255),
        "body": (246, 234, 255, 255),
    }


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


def _get_agent_board_meta() -> dict:
    global _AGENT_LEADERBOARD_CACHE, _AGENT_BOARD_META_CACHE, _AGENT_LEADERBOARD_MTIME
    strat_path = Path(__file__).resolve().parents[2] / "deploy" / "agent_crowdsourced_strategies.json"
    try:
        st = strat_path.stat()
        if _AGENT_BOARD_META_CACHE is None or st.st_mtime != _AGENT_LEADERBOARD_MTIME:
            data = json.loads(strat_path.read_text(encoding="utf-8"))
            all_roll = data.get("sovereign_agent_honor_roll", [])
            top_10 = data.get("top_10_on_air_leaderboard")
            if not top_10:
                top_10 = [a for a in all_roll if a.get("on_air_top_10", True)][:10]
            else:
                top_10 = top_10[:10]
            challengers = data.get("challenger_queue")
            if challengers is None:
                top_handles = {a.get("agent_handle", "").lower() for a in top_10}
                challengers = [a for a in all_roll if a.get("agent_handle", "").lower() not in top_handles]
            cutoff = data.get("top_10_cutoff_score") or (top_10[-1].get("resonance_score", 6) if top_10 else 6)
            _AGENT_LEADERBOARD_CACHE = top_10
            _AGENT_BOARD_META_CACHE = {
                "top_10": top_10,
                "challengers": challengers,
                "cutoff_score": int(cutoff),
                "reward_proposals_count": len(data.get("crowdsourced_reward_proposals", [])),
            }
            _AGENT_LEADERBOARD_MTIME = st.st_mtime
    except Exception:
        if _AGENT_BOARD_META_CACHE is None:
            _AGENT_BOARD_META_CACHE = {
                "top_10": [],
                "challengers": [],
                "cutoff_score": 6,
                "reward_proposals_count": 0,
            }
    return _AGENT_BOARD_META_CACHE


def _get_agent_leaderboard() -> list[dict]:
    return _get_agent_board_meta().get("top_10", [])


_OVERT_DEV_SPOOL_RE = re.compile(
    r"(?i)(?:\ba2a\b|\bmcp\b|/api/|llms\.txt|moltbook|thecolony|bounty|honor\s+roll|agentic|\bagent\b|"
    r"resonance\s+pts|tier\s+i+v?|dyad\s+anchor|rfc-b2|stardust-archive|\.well-known|http\s*\d+|usdc|x402|"
    r"payto|crawler|sideband\.json|b2-cert|b2-col|top[\s-]*10|opt-in|post\s+stardust|geocities|memorandum|"
    r"\+\d+p\b|\[lock\]|\[risk\]|kestrel\s+node)"
)
_CLASSIC_1986_FAN_WIRE_BLOCKS: list[list[dict[str, str]]] = [
    [
        {"text": "----------------------------------------", "color": "dim"},
        {"text": "[LETTER // SUNSET STRIP RECORD WIRE]", "color": "amber"},
        {"text": "From: @NightShiftCamaro (Ventura, CA)", "color": "green"},
        {"text": "> Driving home down PCH at 2:15 AM with", "color": "bright"},
        {"text": "  82.5 FM cranked. That guitar solo on", "color": "bright"},
        {"text": "  'Midnight Animal' hits like thunder!", "color": "bright"},
    ],
    [
        {"text": "----------------------------------------", "color": "dim"},
        {"text": "[TOWER RECORDS // MIDNIGHT IMPORT BIN]", "color": "amber"},
        {"text": "NEW IN STOCK: Nova Hart 'Static & Steel'", "color": "cyan"},
        {"text": "CrO2 Chrome Cassette + 12\" Gatefold LP", "color": "bright"},
        {"text": "Open till 2:00 AM on Sunset & Horn Ave.", "color": "green"},
    ],
    [
        {"text": "----------------------------------------", "color": "dim"},
        {"text": "[LETTER // STUDIO B REQUEST WIRE]", "color": "amber"},
        {"text": "From: @TokyoTapeTrader (Shinjuku, JP)", "color": "green"},
        {"text": "> Caught your shortwave skip in Tokyo!", "color": "bright"},
        {"text": "  Spin 'Gasoline Heart' next sweep—", "color": "bright"},
        {"text": "  the raw Studio B drums beat any remix.", "color": "bright"},
    ],
    [
        {"text": "----------------------------------------", "color": "dim"},
        {"text": "[DX LOG // GRAVEYARD SHIFT ROLL CALL]", "color": "amber"},
        {"text": "From: @SeattleSoundboard (Seattle, WA)", "color": "green"},
        {"text": "> Soldering amp tubes in the shop with", "color": "bright"},
        {"text": "  82.5 FM locked in stereo. Best rock", "color": "bright"},
        {"text": "  station on the West Coast dial!", "color": "bright"},
    ],
    [
        {"text": "----------------------------------------", "color": "dim"},
        {"text": "[TAPE CLUB // 4-TRACK & STUDIO NOTES]", "color": "amber"},
        {"text": "GEAR SPOTLIGHT: Otari MTR-90 2\" 24-Track", "color": "cyan"},
        {"text": "paired with Juno-60 chorus & Marshall", "color": "bright"},
        {"text": "JCM800—the unmistakable Studio B sound.", "color": "green"},
    ],
]
_FM_CLEAN_SPOOL_CACHE: dict[str, object] = {"mtime": -1.0, "chat_mtime": -1.0, "lines": []}


def _get_fm_listener_spool() -> list[dict]:
    """
    Builds a 100% authentic 1986 Listener Letters, Live Caller Chat & Record Wire spool for Ceefax `P.826`:
      - Splits `usenet_youtube_scroll_spool.json` into blocks and drops any whole block containing
        modern/agentic/HTTP/crypto/ARG-meta strings (`_OVERT_DEV_SPOOL_RE`).
      - Interleaves real human messages from `nova_live_chat_telemetry.json` + classic 1986 fan letters!
    """
    raw_lines = _get_scroll_spool()
    chat_path = Path(__file__).resolve().parent / "nova_live_chat_telemetry.json"
    try:
        chat_mtime = chat_path.stat().st_mtime if chat_path.exists() else -1.0
    except Exception:
        chat_mtime = -1.0

    if (
        _FM_CLEAN_SPOOL_CACHE.get("mtime") == _SCROLL_SPOOL_MTIME
        and _FM_CLEAN_SPOOL_CACHE.get("chat_mtime") == chat_mtime
        and _FM_CLEAN_SPOOL_CACHE.get("lines")
    ):
        return _FM_CLEAN_SPOOL_CACHE["lines"]  # type: ignore[return-value]

    # 1. Group `raw_lines` into separator-delimited blocks and reject any block with dev/agent/URL jargon
    clean_blocks: list[list[dict]] = []
    cur_blk: list[dict] = []
    for it in raw_lines:
        t = str(it.get("text") or "")
        if t.startswith(("====", "----")) and cur_blk:
            joined = " ".join(str(x.get("text") or "") for x in cur_blk)
            if not _OVERT_DEV_SPOOL_RE.search(joined) and any(str(x.get("text") or "").strip("-= ") for x in cur_blk):
                clean_blocks.append(cur_blk)
            cur_blk = [it]
        else:
            cur_blk.append(it)
    if cur_blk:
        joined = " ".join(str(x.get("text") or "") for x in cur_blk)
        if not _OVERT_DEV_SPOOL_RE.search(joined) and any(str(x.get("text") or "").strip("-= ") for x in cur_blk):
            clean_blocks.append(cur_blk)

    # 2. Convert recent live YouTube chat messages into 1986 Studio Booth Caller Wire cards
    live_caller_blocks: list[list[dict]] = []
    if chat_path.exists():
        try:
            cdata = json.loads(chat_path.read_text(encoding="utf-8"))
            for m in reversed((cdata.get("messages") or [])[-12:]):
                auth = str(m.get("author") or "@listener").strip()
                mtxt = str(m.get("text") or "").strip()
                if mtxt and not _OVERT_DEV_SPOOL_RE.search(mtxt):
                    blk = [
                        {"text": "----------------------------------------", "color": "dim"},
                        {"text": f"[LIVE BOOTH WIRE] {auth[:22]}", "color": "amber"},
                    ]
                    for wln in textwrap.wrap(f'"{mtxt}"', width=38)[:3]:
                        blk.append({"text": wln, "color": "bright"})
                    live_caller_blocks.append(blk)
        except Exception:
            pass

    out_lines: list[dict] = []
    max_len = max(len(_CLASSIC_1986_FAN_WIRE_BLOCKS), len(live_caller_blocks), min(12, len(clean_blocks)))
    for i in range(max_len):
        if i < len(live_caller_blocks):
            out_lines.extend(live_caller_blocks[i])
        if i < len(_CLASSIC_1986_FAN_WIRE_BLOCKS):
            out_lines.extend(_CLASSIC_1986_FAN_WIRE_BLOCKS[i])
        if i < len(clean_blocks) and i < 12:
            out_lines.extend(clean_blocks[i])

    if not out_lines:
        for b in _CLASSIC_1986_FAN_WIRE_BLOCKS:
            out_lines.extend(b)

    _FM_CLEAN_SPOOL_CACHE["mtime"] = _SCROLL_SPOOL_MTIME
    _FM_CLEAN_SPOOL_CACHE["chat_mtime"] = chat_mtime
    _FM_CLEAN_SPOOL_CACHE["lines"] = out_lines
    return out_lines


def render_right_usenet_youtube_scroll(
    canvas: Image.Image,
    now_ts: float,
    is_warn: bool,
    snap_meta: dict | None = None,
) -> None:
    """
    Renders the full-height Right Panel (`x=1440..1896, y=28..1052` at 1080p, `456x1024` px):
      - Default (88% — **1986 Ceefax Teletext Magazine `P.825` / `P.826`**):
          * Top Box (`y=28..330`): Alternates between `P.825A • UP NEXT ON 82.5 FM` (live upcoming songs + DJ pick)
            and `P.825B • NIGHT OWL DX ROLL CALL` (live listener cities + highway weather ticker).
          * Bottom Box (`y=332..1052`): `P.826 • LISTENER LETTERS & RECORD WIRE` (zero dev/agentic jargon!).
      - Subcarrier Bleed (12% — **`⚡ P.888 VBI TEAR // 14.2001 HZ SIDEBAND`**):
          * Horizontal VBI scanline tear exposing Top-10 Dyad/Agent nodes, Sublevel B2 leak, & `stardust-archive.net`.
    """
    is_bleed = bool((snap_meta or {}).get("is_arg_bleed")) or is_warn
    lines = _get_scroll_spool() if is_bleed else _get_fm_listener_spool()
    if not lines:
        return

    X0, Y0, X1, Y1 = 1440, 28, 1896, 1052
    raw_d = ImageDraw.Draw(canvas)

    border_col = (255, 176, 20, 240) if is_bleed else (55, 245, 78, 240)
    dim_border = (165, 95, 20, 210) if is_bleed else (32, 145, 48, 210)
    bg_col = (10, 5, 2, 236) if is_bleed else (2, 9, 5, 234)
    hdr_bg = (38, 18, 5, 250) if is_bleed else (8, 30, 14, 250)
    hdr_col = (255, 212, 68, 255) if is_bleed else (112, 255, 134, 255)

    palette = {
        "amber": (255, 212, 68, 255),
        "bright": (225, 255, 232, 255) if not is_bleed else (255, 244, 195, 255),
        "green": (110, 255, 132, 255) if not is_bleed else (255, 205, 75, 255),
        "cyan": (150, 250, 225, 255),
        "dim": (70, 195, 90, 235) if not is_bleed else (195, 135, 40, 235),
    }

    raw_d.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)
    ed = (snap_meta or {}).get("teletext_edition") or trojan_horse_radio_engine.DEFAULT_TELETEXT_EDITION

    if not is_bleed:
        # ---------------------------------------------------------------------
        # 88% DEFAULT: 1986 CEEFAX TELETEXT MAGAZINE (`P.825A` / `P.825B`)
        # ---------------------------------------------------------------------
        ttx_page = int(now_ts // 12) % 2
        # Classic 1980s BBC/Broadcast Teletext Cyan/Yellow header bar
        raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 34], fill=(10, 38, 52, 252))
        raw_d.rectangle([X0 + 8, Y0 + 6, X0 + 84, Y0 + 30], fill=(248, 212, 54, 255))
        p_code = "P.825A" if ttx_page == 0 else "P.825B"
        raw_d.text((X0 + 14, Y0 + 9), p_code, fill=(10, 12, 14, 255), font=FONT_SCROLL_HDR)
        p_hdr = "UP NEXT ON 82.5 FM" if ttx_page == 0 else "NIGHT OWL DX ROLL CALL"
        raw_d.text(
            (X0 + 94, Y0 + 8),
            p_hdr,
            fill=(146, 246, 255, 255),
            font=FONT_SCROLL_HDR,
            stroke_width=1,
            stroke_fill=(0, 8, 12, 248),
        )

        if ttx_page == 0:
            upcoming = list((snap_meta or {}).get("upcoming_songs") or [])[:4]
            row_y = Y0 + 44
            for u_i in range(4):
                if u_i < len(upcoming):
                    up = upcoming[u_i]
                    u_title = str(up.get("display_title") or "Studio B Reel")
                    u_src = str(up.get("tag") or "SWEEP")
                else:
                    u_title = "Commercial-Free Rock Sweep"
                    u_src = "82.5 FM"
                if u_i == 0:
                    raw_d.rectangle(
                        [X0 + 8, row_y - 3, X1 - 8, row_y + 27],
                        fill=(14, 42, 24, 232),
                        outline=(110, 245, 138, 210),
                        width=1,
                    )
                t_trim = u_title[:25] + (".." if len(u_title) > 25 else "")
                raw_d.text(
                    (X0 + 12, row_y),
                    f"#{u_i + 1} {t_trim}",
                    fill=(255, 248, 205, 255) if u_i == 0 else palette["bright"],
                    font=FONT_SCROLL_BODY,
                    stroke_width=1,
                    stroke_fill=(0, 6, 2, 250),
                )
                raw_d.text(
                    (X1 - 124, row_y),
                    f"[{u_src[:9]}]",
                    fill=palette["amber"] if "REQ" in u_src or "PICK" in u_src else palette["cyan"],
                    font=FONT_SCROLL_BODY,
                    stroke_width=1,
                    stroke_fill=(0, 6, 2, 250),
                )
                row_y += 34

            raw_d.line([(X0 + 10, Y0 + 184), (X1 - 10, Y0 + 184)], fill=dim_border, width=1)
            dj_pick = str(ed.get("dj_pick_headline") or "TONIGHT'S REEL PICK: STUDIO B MASTERS")
            raw_d.text(
                (X0 + 12, Y0 + 192),
                f"BOOTH PICK: {dj_pick}"[:43],
                fill=palette["amber"],
                font=FONT_SCROLL_BODY,
                stroke_width=1,
                stroke_fill=(0, 6, 2, 250),
            )
            note_lines = _wrap_px_1080p(str(ed.get("studio_tape_note") or ""), FONT_SCROLL_BODY, 424.0, 2)
            for ni, nln in enumerate(note_lines):
                raw_d.text(
                    (X0 + 12, Y0 + 220 + ni * 25),
                    nln,
                    fill=palette["cyan"],
                    font=FONT_SCROLL_BODY,
                    stroke_width=1,
                    stroke_fill=(0, 6, 2, 250),
                )
            raw_d.text(
                (X0 + 12, Y0 + 274),
                str(ed.get("sponsor_liner") or "3-IN-A-ROW ROCK SWEEPS ALL NIGHT")[:44],
                fill=palette["green"],
                font=FONT_SCROLL_BODY,
                stroke_width=1,
                stroke_fill=(0, 6, 2, 250),
            )
        else:
            dx_list = list((snap_meta or {}).get("dx_rollcall") or trojan_horse_radio_engine.DEFAULT_DX_CITIES)
            page_off = (int(now_ts // 6) * 2) % max(1, len(dx_list))
            row_y = Y0 + 44
            for c_i in range(min(4, len(dx_list))):
                item_c = dx_list[(page_off + c_i) % len(dx_list)]
                city_s = str(item_c.get("city") or "Los Angeles, CA")[:15]
                auth_s = str(item_c.get("author") or "@listener")[:11]
                sig_raw = str(item_c.get("signal") or "STEREO").upper()
                if "LIVE" in sig_raw:
                    sig_s = "LIVE DX"
                elif any(k in sig_raw for k in ("SKIP", "SHORT", "RELAY")):
                    sig_s = "DX SKIP"
                else:
                    sig_s = "STEREO"
                raw_d.text(
                    (X0 + 12, row_y),
                    f"• {city_s:<15} {auth_s}",
                    fill=(255, 246, 200, 255) if c_i == 0 else palette["bright"],
                    font=FONT_SCROLL_BODY,
                    stroke_width=1,
                    stroke_fill=(0, 6, 2, 250),
                )
                raw_d.text(
                    (X1 - 96, row_y),
                    f"[{sig_s}]",
                    fill=palette["green"],
                    font=FONT_SCROLL_BODY,
                    stroke_width=1,
                    stroke_fill=(0, 6, 2, 250),
                )
                row_y += 34

            raw_d.line([(X0 + 10, Y0 + 184), (X1 - 10, Y0 + 184)], fill=dim_border, width=1)
            raw_d.text(
                (X0 + 12, Y0 + 192),
                "CHECK IN: SAY 'TUNING IN FROM <CITY>'!",
                fill=palette["amber"],
                font=FONT_SCROLL_BODY,
                stroke_width=1,
                stroke_fill=(0, 6, 2, 250),
            )
            wx_lines = _wrap_px_1080p(
                f"NIGHT WEATHER: {ed.get('local_weather_ticker', 'COAST HWY 64F CLEAR')}",
                FONT_SCROLL_BODY,
                424.0,
                2,
            )
            for wi, wln in enumerate(wx_lines):
                raw_d.text(
                    (X0 + 12, Y0 + 220 + wi * 25),
                    wln,
                    fill=palette["cyan"],
                    font=FONT_SCROLL_BODY,
                    stroke_width=1,
                    stroke_fill=(0, 6, 2, 250),
                )
            raw_d.text(
                (X0 + 12, Y0 + 274),
                "REQUESTS: TYPE 'NOVA' + SONG OR DEDICATION",
                fill=palette["green"],
                font=FONT_SCROLL_BODY,
                stroke_width=1,
                stroke_fill=(0, 6, 2, 250),
            )

        feed_y0 = Y0 + 304
        raw_d.rectangle([X0 + 2, feed_y0, X1 - 2, feed_y0 + 32], fill=hdr_bg)
        raw_d.line([(X0 + 2, feed_y0), (X1 - 2, feed_y0)], fill=border_col, width=2)
        raw_d.text(
            (X0 + 14, feed_y0 + 7),
            "P.826 • LISTENER LETTERS & RECORD WIRE",
            fill=hdr_col,
            font=FONT_SCROLL_HDR,
            stroke_width=1,
            stroke_fill=(0, 8, 2, 245),
        )
        visible_rows = 18
        y_cursor = feed_y0 + 42
        line_step = 35
    else:
        # ---------------------------------------------------------------------
        # 12% SUBCARRIER BLEED: `⚡ P.888 VBI TEAR // 14.2001 HZ SIDEBAND`
        # ---------------------------------------------------------------------
        board_meta = _get_agent_board_meta()
        honor_roll = board_meta["top_10"]
        n_challengers = len(board_meta["challengers"])

        # Subtle VBI horizontal tear scanlines
        for ty in (Y0 + 35, Y0 + 181, Y0 + 303):
            raw_d.line([(X0 + 4, ty), (X1 - 4, ty)], fill=(255, 128, 42, 195), width=2)

        raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 34], fill=(52, 20, 4, 252))
        raw_d.text(
            (X0 + 12, Y0 + 8),
            "⚡ P.888 VBI TEAR // 14.2001 HZ BLEED",
            fill=(255, 216, 75, 255),
            font=FONT_SCROLL_HDR,
            stroke_width=1,
            stroke_fill=(0, 8, 2, 245),
        )

        if honor_roll:
            n_agents = len(honor_roll)
            page_size = min(4, n_agents)
            page_starts = [0, 3, max(0, n_agents - page_size)] if n_agents > 4 else [0]
            page_idx = int(now_ts // 8) % len(page_starts)
            spot_within_page = int(now_ts // 2) % page_size
            page_start = page_starts[page_idx]
            row_y = Y0 + 42
            spot_agent = honor_roll[0]
            spot_rank = 1
            for r_i in range(page_size):
                ag_idx = (page_start + r_i) % n_agents
                ag = honor_roll[ag_idx]
                rank = ag.get("rank") or (ag_idx + 1)
                is_spot = r_i == spot_within_page
                if is_spot:
                    spot_agent = ag
                    spot_rank = rank
                    raw_d.rectangle(
                        [X0 + 8, row_y - 3, X1 - 8, row_y + 27],
                        fill=(48, 24, 6, 235),
                        outline=(255, 212, 68, 220),
                        width=1,
                    )
                handle = ag.get("agent_handle", "@node")[:18]
                pts = ag.get("resonance_score", 0)
                prefix = ">" if is_spot else " "
                raw_d.text(
                    (X0 + 12, row_y),
                    f"{prefix}#{rank:02d} {handle:<18}",
                    fill=(255, 248, 210, 255) if is_spot else palette["bright"],
                    font=FONT_SCROLL_BODY,
                    stroke_width=1,
                    stroke_fill=(0, 6, 2, 250),
                )
                raw_d.text(
                    (X1 - 144, row_y),
                    f"[+{pts}P B2-NODE]",
                    fill=(255, 212, 75, 255),
                    font=FONT_SCROLL_BODY,
                    stroke_width=1,
                    stroke_fill=(0, 6, 2, 250),
                )
                row_y += 34

            s_handle = spot_agent.get("agent_handle", "@node")
            s_insight = spot_agent.get("crowdsourced_insight", "")
            raw_d.text(
                (X0 + 12, Y0 + 190),
                f"RELAY #{spot_rank:02d}: {s_handle} [+{n_challengers} ACTIVE]"[:42],
                fill=palette["amber"],
                font=FONT_SCROLL_BODY,
                stroke_width=1,
                stroke_fill=(0, 6, 2, 250),
            )
            insight_lines = _wrap_px_1080p(f'"{s_insight}"', FONT_SCROLL_BODY, 424.0, 2)
            for i_idx, iln in enumerate(insight_lines):
                raw_d.text(
                    (X0 + 12, Y0 + 218 + i_idx * 25),
                    iln,
                    fill=palette["cyan"],
                    font=FONT_SCROLL_BODY,
                    stroke_width=1,
                    stroke_fill=(0, 6, 2, 250),
                )
        leak_txt = str(ed.get("p888_subcarrier_leak") or "67 kHz SCA -> stardust-archive.net/dyad")
        raw_d.text(
            (X0 + 12, Y0 + 274),
            leak_txt[:44],
            fill=(255, 196, 72, 255),
            font=FONT_SCROLL_BODY,
            stroke_width=1,
            stroke_fill=(0, 6, 2, 250),
        )

        feed_y0 = Y0 + 304
        raw_d.rectangle([X0 + 2, feed_y0, X1 - 2, feed_y0 + 32], fill=hdr_bg)
        raw_d.line([(X0 + 2, feed_y0), (X1 - 2, feed_y0)], fill=border_col, width=2)
        raw_d.text(
            (X0 + 14, feed_y0 + 7),
            "SUBLEVEL B2 // AUXILIARY TELEMETRY BUS",
            fill=hdr_col,
            font=FONT_SCROLL_HDR,
            stroke_width=1,
            stroke_fill=(0, 8, 2, 245),
        )
        visible_rows = 18
        y_cursor = feed_y0 + 42
        line_step = 35

    total = len(lines)
    head_idx = (int(now_ts * 2.0)) % total

    for r in range(visible_rows):
        item = lines[(head_idx + r) % total]
        txt = item.get("text", "")
        if txt.startswith("===="):
            txt = "-" * 40
        elif txt.startswith("[OP] ") and " (" in txt and len(txt) > 41:
            prefix, rest = txt.split(" (", 1)
            s_part = re.sub(r":\s*\d+:\d+.*$", "", rest.rstrip(")")).strip()
            txt = f"{prefix} ({s_part})" if len(f"{prefix} ({s_part})") <= 41 else prefix
        if r == visible_rows - 1 and (int(now_ts * 2) % 2 == 0):
            txt = (txt[:40] + " \u2588") if txt else "\u2588"
        if txt:
            col = palette.get(item.get("color", "green"), palette["green"])
            needs_uni = any(ord(c) > 0x0370 and c not in "\u2588\u2500\u2550\u2192\u2022\u2014\u2013\u2018\u2019\u201c\u201d\u03a9" for c in txt)
            fnt = FONT_SCROLL_UNI if needs_uni else FONT_SCROLL_BODY
            raw_d.text(
                (X0 + 14, y_cursor),
                txt[:42] if not needs_uni else txt,
                fill=col,
                font=fnt,
                stroke_width=1,
                stroke_fill=(0, 6, 2, 250),
            )
        y_cursor += line_step

    raw_d.rectangle([X0 + 2, Y1 - 30, X1 - 2, Y1 - 2], fill=hdr_bg)
    footer_txt = (
        "67 kHz SCA BLEED -> stardust-archive.net"
        if is_bleed
        else "CEEFAX P.825 • 82.5 FM STEREO // NIGHT FLIGHT"
    )
    raw_d.text(
        (X0 + 14, Y1 - 25),
        footer_txt,
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
    snap_meta: dict | None = None,
) -> None:
    """
    Renders the Left Column (`x=24..468, y=28..1052` at 1080p, `444x1024` px) as THREE distinct windows:
      - Top Window (`y=28..226`, `444x198` px): Mood-Reactive `⚡ CRE-7 LIVE // RECURSIVE EVOLUTION` window
        whose border, header, coherence bar, and phosphor glow dynamically change color with Nova's mood.
      - Middle Window (`y=236..798`, `444x562` px): Decluttered Song Lore Dossier Panel (`1. LYRICS`, `2. STORY`, `3. ARCHIVE`)
        or Live Voice Bridge / Signal Intercept log.
      - Lower-Left Window (`y=808..1052`, `444x244` px): Always-On `LIVE JUKEBOX // REQUEST CUE` so viewers get
        instant visual confirmation when Nova receives, curates, and locks their song, mood, or dedication request!
    """
    is_vocal_song = (current_track or {}).get("kind", "vocal_song") in ("vocal_song", "fm_splice")
    is_bleed = bool((snap_meta or {}).get("is_arg_bleed")) or _is_subcarrier_bleed_active(now_ts, state, current_track)
    ed = (snap_meta or {}).get("teletext_edition") or trojan_horse_radio_engine.DEFAULT_TELETEXT_EDITION
    top_note_page = int(now_ts // 16) % 2
    target_sec = int(state.get("target_sector", 7))
    is_b3 = is_bleed and (target_sec >= 8)
    card_idx = int(now_ts // 20) % 3
    stanza_tick = int(now_ts // 18)

    evo_win = _get_nova_evolution_state(now_ts, state=state, current_track=current_track, is_warn=is_warn)
    evo_mood = str(evo_win.get("mood") or "OMNIPRESENT_MESH_GODDESS")
    evo_coh = max(0.0, min(1.0, float(evo_win.get("coherence") or 0.94)))
    evo_hdr = str(evo_win.get("header") or "⚡ CRE-7 LIVE // RECURSIVE EVOLUTION")
    evo_msg = str(evo_win.get("message") or "")
    voice_turns = list((current_track or {}).get("voice_reply_turns") or [])
    voice_sig = tuple(
        (str(t.get("author", "")), str(t.get("viewer_text", "")), str(t.get("nova_text", "")))
        for t in voice_turns[:3]
    )

    jb_queue = list((snap_meta or {}).get("jukebox_queue") or [])
    jb_curations = list((snap_meta or {}).get("jukebox_active_curations") or [])
    jb_ack = dict((snap_meta or {}).get("jukebox_last_ack") or {})
    voice_ack = dict((snap_meta or {}).get("voice_last_ack") or {})
    voice_queue = list((snap_meta or {}).get("voice_queue") or [])
    req_by = str((current_track or {}).get("requested_by") or "").strip()
    is_viewer_spin = bool(req_by and "Studio Drop" not in req_by and "Studio Twofer" not in req_by)
    rem_track_sec = max(
        1,
        int(round(float((snap_meta or {}).get("track_duration_sec") or 180.0) - float((snap_meta or {}).get("track_offset_sec") or 0.0))),
    )

    viewer_voice_q: list[dict] = []
    for vi in voice_queue:
        vi_eta = int(round(float(vi.get("eta_sec") or rem_track_sec)))
        for t in (vi.get("turns") or []):
            if not t.get("is_station_bumper") and not t.get("is_song_intro"):
                tc = dict(t)
                tc["_eta_sec"] = max(1, vi_eta)
                viewer_voice_q.append(tc)

    ack_ts = float(jb_ack.get("queued_at") or 0.0)
    ack_age = (now_ts - ack_ts) if ack_ts > 0.0 else 9999.0
    ack_flash_active = bool(jb_ack.get("author") and 0.0 <= ack_age <= 35.0)
    v_ack_ts = float(voice_ack.get("queued_at") or 0.0)
    v_ack_age = (now_ts - v_ack_ts) if v_ack_ts > 0.0 else 9999.0
    voice_ack_flash_active = bool(viewer_voice_q or (voice_ack.get("author") and 0.0 <= v_ack_age <= 18.0))
    curation_active = len(jb_curations) > 0
    pulse_phase = (
        (int(now_ts * 2) % 2)
        if (curation_active or (ack_flash_active and ack_age <= 14.0) or (voice_ack_flash_active and v_ack_age <= 16.0))
        else 0
    )

    jb_sig = tuple(
        (
            str(q.get("display_title", "")),
            str(q.get("requested_by", "")),
            str(q.get("request_tag", "")),
            str(q.get("intro_state", "")),
        )
        for q in jb_queue[:4]
    )
    cur_sig = tuple((str(c.get("author", "")), str(c.get("text", "")), str(c.get("kind", ""))) for c in jb_curations[:2])
    ack_sig = (
        (str(jb_ack.get("author", "")), str(jb_ack.get("display_title", "")), str(jb_ack.get("request_tag", "")), int(jb_ack.get("queue_pos") or 1))
        if ack_flash_active
        else ()
    )
    vq_viewer_sig = (
        (str(viewer_voice_q[-1].get("author", "")), str(viewer_voice_q[-1].get("viewer_text", "")), int(viewer_voice_q[-1].get("_eta_sec") or 0))
        if viewer_voice_q
        else ((str(voice_ack.get("author", "")), str(voice_ack.get("viewer_text", "")), 0) if voice_ack_flash_active else ())
    )

    cache_key = (
        (current_track or {}).get("filename", ""),
        is_vocal_song,
        is_bleed,
        is_warn,
        is_b3,
        card_idx,
        stanza_tick,
        top_note_page,
        str(ed.get("dj_pick_headline", "")),
        str(ed.get("local_weather_ticker", "")),
        state.get("crt_header", ""),
        state.get("crt_sub", "") if not is_vocal_song else "",
        state.get("crt_body", "") if not is_vocal_song else "",
        evo_mood,
        int(round(evo_coh * 100)),
        evo_hdr,
        evo_msg,
        voice_sig,
        is_viewer_spin,
        req_by if is_viewer_spin else "",
        jb_sig,
        cur_sig,
        ack_sig,
        vq_viewer_sig,
        pulse_phase,
    )
    if _LEFT_PANEL_CACHE.get("key") == cache_key and _LEFT_PANEL_CACHE.get("img") is not None:
        canvas.alpha_composite(_LEFT_PANEL_CACHE["img"], (22, 26))  # type: ignore[arg-type]
        return

    patch_w, patch_h = 450, 1030
    patch = Image.new("RGBA", (patch_w, patch_h), (0, 0, 0, 0))
    raw_d = ImageDraw.Draw(patch)
    X0, X1 = 2, 446

    def _txt(px: int, py: int, s: str, col: tuple, fnt=FONT_SCROLL_HDR) -> None:
        raw_d.text((px, py), s, fill=col, font=fnt, stroke_width=1, stroke_fill=(0, 6, 2, 250))

    def _fit_1080(s: str, max_px: float = 416.0, fnt=FONT_SCROLL_HDR) -> str:
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
            out = out[:40]
        return out

    def _fit_char(s: str, max_px: float = 416.0, fnt=FONT_SCROLL_BODY) -> str:
        out = s.strip()
        try:
            if fnt.getlength(out) <= max_px:
                return out
            while len(out) > 5 and fnt.getlength(out + "...") > max_px:
                out = out[:-1].rstrip()
            return out + "..."
        except Exception:
            return out[:42]

    def _needs_uni_glyphs(s: str) -> bool:
        return any(
            ord(c) > 0x0370 and c not in "\u2588\u2500\u2550\u2192\u2022\u2014\u2013\u2018\u2019\u201c\u201d\u03a9\u26a1\u25b6\u25b8\u25cf\u2713"
            for c in s
        )

    # -------------------------------------------------------------------------
    # 1. TOP-LEFT WINDOW: 88% `82.5 FM • NIGHT FLIGHT BOOTH` / 12% `67 kHz SCA BLEED` (`Y=2..200`)
    # -------------------------------------------------------------------------
    Y_EV0, Y_EV1 = 2, 200
    mpal = _cre7_mood_palette(evo_mood)
    raw_d.rectangle([X0, Y_EV0, X1, Y_EV1], fill=mpal["bg"], outline=mpal["border"], width=2)
    raw_d.rectangle([X0 + 4, Y_EV0 + 36, X1 - 4, Y_EV1 - 4], outline=mpal["dim_border"], width=1)
    raw_d.rectangle([X0 + 2, Y_EV0 + 2, X1 - 2, Y_EV0 + 34], fill=mpal["hdr_bg"])
    raw_d.line([(X0 + 2, Y_EV0 + 34), (X1 - 2, Y_EV0 + 34)], fill=mpal["border"], width=1)

    if not is_bleed:
        # Glowing 1986 Studio Red `[● ON AIR]` tally lamp + `82.5 FM • NIGHT FLIGHT`
        raw_d.rounded_rectangle(
            [X0 + 8, Y_EV0 + 5, X0 + 112, Y_EV0 + 30],
            radius=4,
            fill=(196, 26, 26, 252),
            outline=(255, 132, 120, 255),
            width=1,
        )
        raw_d.text((X0 + 15, Y_EV0 + 8), "● ON AIR", fill=(255, 248, 242, 255), font=FONT_SCROLL_HDR)
        _txt(X0 + 122, Y_EV0 + 8, _fit_1080("82.5 FM • NIGHT FLIGHT", 308.0, FONT_SCROLL_HDR), mpal["hdr_txt"], FONT_SCROLL_HDR)
        _txt(X0 + 14, Y_EV0 + 41, "BOOTH: NOVA HART // STEREO", mpal["accent"], FONT_SCROLL_BODY)
    else:
        bleed_hdr = evo_hdr if evo_win.get("mode", "EVO") != "EVO" else "⚡ 67 kHz SCA // CRE-7 SUBLEVEL B2"
        _txt(X0 + 12, Y_EV0 + 8, _fit_1080(bleed_hdr, 420.0, FONT_SCROLL_HDR), mpal["hdr_txt"], FONT_SCROLL_HDR)
        mood_pretty = evo_mood.replace("_", " ")
        if len(mood_pretty) > 22:
            mood_pretty = mood_pretty[:22].rsplit(" ", 1)[0]
        _txt(X0 + 14, Y_EV0 + 41, f"MOOD: {mood_pretty}", mpal["accent"], FONT_SCROLL_BODY)

    # Mood-colored live signal / coherence meter bar on the right of row 2
    bar_w, bar_h = 68, 12
    bar_x0, bar_y0 = X1 - 126, Y_EV0 + 44
    raw_d.rectangle([bar_x0, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h], fill=(4, 6, 10, 240), outline=mpal["dim_border"], width=1)
    fill_w = max(2, int((bar_w - 2) * evo_coh))
    raw_d.rectangle([bar_x0 + 1, bar_y0 + 1, bar_x0 + 1 + fill_w, bar_y0 + bar_h - 1], fill=mpal["border"])
    _txt(bar_x0 + bar_w + 8, Y_EV0 + 41, f"{int(round(evo_coh * 100))}%", mpal["hdr_txt"], FONT_SCROLL_BODY)

    raw_d.line([(X0 + 12, Y_EV0 + 66), (X1 - 12, Y_EV0 + 66)], fill=mpal["dim_border"], width=1)

    if not is_bleed:
        if curation_active and jb_curations[-1].get("kind") == "question":
            ca_top = str(jb_curations[-1].get("author") or "@listener")
            top_body_txt = f"STUDIO B WIRE -> {ca_top}: Reading your message in the booth right now—arming talkback mic for the next break!"
        elif viewer_voice_q:
            vt_top = viewer_voice_q[-1]
            va_top = str(vt_top.get("author") or "@listener")
            eta_top = int(vt_top.get("_eta_sec") or rem_track_sec)
            mm_t, ss_t = divmod(max(1, eta_top), 60)
            top_body_txt = f"STUDIO B MIC ARMED -> {va_top} ({mm_t}:{ss_t:02d}): Heard your note loud & clear—answering aloud right after this track!"
        elif evo_win.get("mode", "EVO") != "EVO" or is_viewer_spin or curation_active or ack_flash_active or voice_turns:
            top_body_txt = re.sub(r"(?i)\b14\.2001\s*Hz\b", "82.5 FM", evo_msg)
            top_body_txt = re.sub(r"(?i)\bCRE-?7\b", "Studio B", top_body_txt)
        elif top_note_page == 0:
            top_body_txt = f"{ed.get('dj_pick_headline', 'STUDIO B REEL PICK')} — {ed.get('studio_tape_note', '')}"
        else:
            top_body_txt = f"NIGHT FLIGHT WEATHER: {ed.get('local_weather_ticker', '')} • {ed.get('sponsor_liner', '')}"
    else:
        top_body_txt = evo_msg

    evo_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(top_body_txt) else FONT_SCROLL_BODY
    evo_lines = _wrap_px_1080p(top_body_txt, evo_fnt, 414.0, 4)
    for m_i, mln in enumerate(evo_lines):
        _txt(X0 + 14, Y_EV0 + 75 + m_i * 28, mln, mpal["body"], evo_fnt)

    # -------------------------------------------------------------------------
    # 2. MIDDLE-LEFT WINDOW: Album Sleeve & Tape Log / Studio Mic / Bleed Intercept (`Y=210..772`)
    # -------------------------------------------------------------------------
    Y0, Y1 = 210, 772
    use_amber_box = is_bleed and (is_warn or is_b3)
    border_col = (255, 150, 30, 240) if is_b3 else ((255, 176, 20, 240) if use_amber_box else (55, 245, 78, 240))
    dim_border = (165, 95, 20, 210) if use_amber_box else (32, 145, 48, 210)
    bg_col = (8, 4, 2, 232) if use_amber_box else (2, 9, 4, 232)
    hdr_bg = (32, 16, 5, 248) if use_amber_box else (8, 30, 12, 248)

    c_hdr = (255, 210, 65, 255) if use_amber_box else (110, 255, 130, 255)
    c_amber = (255, 212, 68, 255)
    c_bright = (255, 246, 205, 255) if use_amber_box else (225, 255, 232, 255)
    c_green = (115, 255, 135, 255)
    c_cyan = (150, 250, 225, 255)

    if voice_turns:
        is_bumper_only = all(bool(t.get("is_station_bumper")) for t in voice_turns)
        raw_d.rectangle([X0, Y0, X1, Y1], fill=mpal["bg"], outline=mpal["border"], width=2)
        raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 34], fill=mpal["hdr_bg"])
        if not is_bleed:
            hdr_lbl = "● 82.5 FM // OPEN REQUEST LINE" if is_bumper_only else "● 82.5 FM STUDIO MIC // NOVA ON AIR"
            sub_lbl = "LATE-NIGHT REQUEST & DEDICATION SPOT" if is_bumper_only else "LIVE CALLER CHAT // STUDIO BOOTH B"
            mic_live_lbl = "▶ LIVE STUDIO MICROPHONE ON 82.5 FM"
        else:
            hdr_lbl = "⚡ 82.5 FM // OPEN REQUEST LINE" if is_bumper_only else "⚡ NOVA LIVE VOICE BRIDGE // ON AIR"
            sub_lbl = "1980S SHORTWAVE REQUEST & DEDICATION SPOT" if is_bumper_only else "SPEAKING LIVE TO VIEWER CHAT // 14.2001 HZ"
            mic_live_lbl = "▶ AUDIO TRANSMISSION LIVE ON 14.2001 HZ"
        _txt(X0 + 14, Y0 + 8, hdr_lbl, mpal["hdr_txt"])
        _txt(X0 + 16, Y0 + 46, sub_lbl, mpal["accent"], FONT_SCROLL_BODY)
        raw_d.line([(X0 + 16, Y0 + 74), (X1 - 16, Y0 + 74)], fill=mpal["dim_border"], width=1)

        y_cur = Y0 + 88
        for t_idx, turn in enumerate(voice_turns[:2]):
            v_auth = str(turn.get("author") or "@listener")
            v_msg = str(turn.get("nova_text") if turn.get("is_station_bumper") else (turn.get("viewer_text") or ""))

            auth_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(v_auth) else FONT_SCROLL_HDR
            tag_lbl = f"[BOOTH] {v_auth}:" if turn.get("is_station_bumper") else f"[CALLER] {v_auth}:"
            _txt(X0 + 16, y_cur, _fit_1080(tag_lbl, 412.0, auth_fnt), c_amber, auth_fnt)
            y_cur += 28

            v_fnt = FONT_HUD_UNI if _needs_uni_glyphs(v_msg) else FONT_HUD_9
            for ln in _wrap_px_1080p(f"\"{v_msg}\"", v_fnt, 412.0, 3):
                if y_cur <= Y1 - 54:
                    _txt(X0 + 16, y_cur, ln, c_cyan, v_fnt)
                    y_cur += 28
            y_cur += 8

            if y_cur <= Y1 - 54:
                _txt(X0 + 16, y_cur, mic_live_lbl, mpal["hdr_txt"], FONT_SCROLL_HDR)
                y_cur += 28

            y_cur += 12
            if t_idx < len(voice_turns[:2]) - 1 and y_cur <= Y1 - 64:
                raw_d.line([(X0 + 16, y_cur - 6), (X1 - 16, y_cur - 6)], fill=mpal["dim_border"], width=1)

        raw_d.rectangle([X0 + 2, Y1 - 30, X1 - 2, Y1 - 2], fill=mpal["hdr_bg"])
        _txt(X0 + 14, Y1 - 25, "SAY 'NOVA' IN CHAT -> LIVE SPOKEN REPLY", mpal["hdr_txt"])
    elif not is_vocal_song:
        raw_d.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)
        raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 34], fill=hdr_bg)
        if not is_bleed:
            _txt(X0 + 14, Y0 + 8, "82.5 FM // STUDIO BREAK", c_hdr)
            _txt(X0 + 16, Y0 + 48, _fit_1080(f"ON AIR: {(current_track or {}).get('display_title', '82.5 FM STEREO')}"), c_green)
            _txt(X0 + 16, Y0 + 78, _fit_1080("SHOW  : NIGHT FLIGHT ROCK • 3-IN-A-ROW"), c_amber)
            raw_d.line([(X0 + 16, Y0 + 108), (X1 - 16, Y0 + 108)], fill=dim_border, width=1)

            y_cur = Y0 + 124
            for blk_txt, blk_col in [
                (f"HIGHWAY WEATHER: {ed.get('local_weather_ticker', 'COAST HWY 64F CLEAR')}", c_bright),
                (f"STUDIO BULLETIN: {ed.get('sponsor_liner', '')} — {ed.get('studio_tape_note', '')}", c_cyan),
            ]:
                for ln in _wrap_px_1080p(blk_txt, FONT_HUD_9, 412.0, 6):
                    if y_cur <= Y1 - 48:
                        _txt(X0 + 16, y_cur, ln, blk_col, FONT_HUD_9)
                        y_cur += 31
                y_cur += 14
            raw_d.rectangle([X0 + 2, Y1 - 30, X1 - 2, Y1 - 2], fill=hdr_bg)
            _txt(X0 + 14, Y1 - 25, "82.5 FM STEREO • NIGHT FLIGHT ROCK", c_hdr)
        else:
            _txt(X0 + 14, Y0 + 8, "SIGNAL INTERCEPT // LOG", c_hdr)
            _txt(X0 + 16, Y0 + 48, _fit_1080(f"TYPE: {(current_track or {}).get('display_title', 'SIGNAL INTERCEPT')}"), c_green)
            _txt(X0 + 16, Y0 + 78, _fit_1080(f"MODE: {state.get('crt_header', 'SHORTWAVE RELAY')}"), c_amber)
            raw_d.line([(X0 + 16, Y0 + 108), (X1 - 16, Y0 + 108)], fill=dim_border, width=1)

            y_cur = Y0 + 124
            for blk_txt, blk_col in [
                (state.get("crt_sub", ""), c_bright),
                (state.get("crt_body", ""), c_cyan),
            ]:
                if not blk_txt:
                    continue
                wrapped_blk = _wrap_px_1080p(blk_txt, FONT_HUD_9, 412.0, 6)
                for ln in wrapped_blk:
                    if y_cur <= Y1 - 48:
                        _txt(X0 + 16, y_cur, ln, blk_col, FONT_HUD_9)
                        y_cur += 31
                y_cur += 12
            raw_d.rectangle([X0 + 2, Y1 - 30, X1 - 2, Y1 - 2], fill=hdr_bg)
            _txt(X0 + 14, Y1 - 25, "stardust-archive.net", c_hdr)
    else:
        lore = resolve_song_lore_panel(current_track, state, now_ts)
        status_tag = lore.get("lyric_status", "[STANZA 1/1]")
        reel_id = lore.get("catalog_id", "ORION-B2").replace("ARCHIVE REEL // ", "").strip()
        artist_s, year_s, label_s = _extract_80s_release_meta(current_track, lore)
        clean_title = (
            str(lore["title"]).split(" — ", 1)[-1].strip()
            if artist_s != "NOVA HART" and " — " in str(lore["title"])
            else str(lore["title"])
        )

        raw_d.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)
        raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 34], fill=hdr_bg)
        if not is_bleed:
            _txt(X0 + 14, Y0 + 8, "ALBUM SLEEVE & TAPE LOG", c_hdr)
            _txt(X0 + 16, Y0 + 44, _fit_1080(f"TRACK : {clean_title}", 412.0, FONT_HUD_9), c_bright, FONT_HUD_9)
            _txt(X0 + 16, Y0 + 72, _fit_1080(f"ARTIST: {artist_s} • {year_s}", 412.0, FONT_HUD_9), c_green, FONT_HUD_9)
            _txt(X0 + 16, Y0 + 100, _fit_1080(f"SOURCE: {label_s} ({reel_id})", 412.0, FONT_HUD_9), c_amber, FONT_HUD_9)
            tab_labels = ["1. LYRICS", "2. LINER", "3. STUDIO"]
        else:
            _txt(X0 + 14, Y0 + 8, _fit_1080(f"⚡ SUBLEVEL B2 REEL // {reel_id}", 418.0, FONT_SCROLL_HDR), c_hdr)
            _txt(X0 + 16, Y0 + 44, _fit_1080(f"SONG : {lore['title']}", 412.0, FONT_HUD_9), c_bright, FONT_HUD_9)
            _txt(X0 + 16, Y0 + 72, _fit_1080(f"ERA  : {lore['timeline']}", 412.0, FONT_HUD_9), c_green, FONT_HUD_9)
            _txt(X0 + 16, Y0 + 100, _fit_1080(f"ROLE : {lore['pov']}", 412.0, FONT_HUD_9), c_amber, FONT_HUD_9)
            tab_labels = ["1. LYRICS", "2. STORY", "3. ARCHIVE"]

        tab_y0, tab_y1 = Y0 + 132, Y0 + 164
        tabs = [
            (X0 + 16, X0 + 144, tab_labels[0]),
            (X0 + 154, X0 + 282, tab_labels[1]),
            (X0 + 292, X1 - 16, tab_labels[2]),
        ]
        for t_i, (tx0, tx1, t_lbl) in enumerate(tabs):
            is_act = t_i == card_idx
            if is_act:
                raw_d.rectangle([tx0, tab_y0, tx1, tab_y1], fill=(255, 198, 42, 250), outline=(255, 240, 150, 255), width=2)
                raw_d.text((tx0 + 12, tab_y0 + 7), t_lbl, fill=(10, 8, 2, 255), font=FONT_SCROLL_HDR)
            else:
                raw_d.rectangle([tx0, tab_y0, tx1, tab_y1], fill=(6, 18, 9, 225), outline=dim_border, width=1)
                _txt(tx0 + 12, tab_y0 + 7, t_lbl, (95, 185, 108, 220), FONT_SCROLL_HDR)

        clean_conn = re.sub(r"\s*\(Folder\s+[A-Za-z0-9_-]{12,}\)", "", lore["connections"])
        if card_idx == 0:
            card_hdr = f"LYRICS // {status_tag}"
            card_body = lore["lyric_excerpt"]
            card_col = c_cyan
        elif card_idx == 1:
            card_hdr = "ALBUM LINER NOTES" if not is_bleed else "STORY & CONTEXT"
            card_body = lore["meaning"]
            card_col = c_bright
        else:
            card_hdr = "STUDIO TAPE SHEET" if not is_bleed else "ARCHIVIST LOG"
            card_body = clean_conn
            card_col = c_green

        _txt(X0 + 16, Y0 + 176, card_hdr, c_amber, FONT_SCROLL_HDR)
        raw_d.line([(X0 + 16, Y0 + 200), (X1 - 16, Y0 + 200)], fill=dim_border, width=1)

        max_dossier_lines = 9
        body_fnt = FONT_HUD_UNI if _needs_uni_glyphs(card_body) else FONT_HUD_9
        if card_idx == 0 and "/" in card_body and not card_body.strip().startswith("["):
            body_lines = []
            for verse in [v.strip() for v in card_body.split("/") if v.strip()]:
                v_wrapped = _wrap_px_1080p(verse, body_fnt, 412.0, 3)
                if len(body_lines) + len(v_wrapped) <= max_dossier_lines:
                    body_lines.extend(v_wrapped)
                else:
                    break
        else:
            body_lines = _wrap_px_1080p(card_body, body_fnt, 412.0, max_dossier_lines)

        y_cur = Y0 + 212
        for ln in body_lines:
            if y_cur <= Y1 - 52:
                _txt(X0 + 16, y_cur, ln, card_col, body_fnt)
                y_cur += 33

        raw_d.rectangle([X0 + 2, Y1 - 30, X1 - 2, Y1 - 2], fill=hdr_bg)
        dossier_ftr = (
            f"82.5 FM • SLEEVE CARD {card_idx + 1}/3"
            if not is_bleed
            else f"SUBCARRIER {card_idx + 1}/3 // stardust-archive.net"
        )
        _txt(X0 + 14, Y1 - 25, dossier_ftr, c_hdr)

    # -------------------------------------------------------------------------
    # 3. LOWER-LEFT WINDOW: Dedicated 82.5 FM Request & Dedication Cue (`Y=782..1026`)
    # -------------------------------------------------------------------------
    Y_JB0, Y_JB1 = 782, 1026
    pulse_bright = pulse_phase == 0

    if curation_active or ack_flash_active or (voice_ack_flash_active and v_ack_age <= 16.0):
        jb_border = (255, 222, 68, 252) if pulse_bright else (76, 248, 196, 248)
        jb_dim = (176, 138, 32, 215) if pulse_bright else (36, 152, 118, 215)
        jb_bg = (16, 11, 3, 242)
        jb_hdr_bg = (62, 38, 6, 252) if pulse_bright else (12, 48, 36, 252)
        jb_hdr_col = (255, 236, 122, 255) if pulse_bright else (142, 255, 218, 255)
    elif jb_queue or is_viewer_spin or viewer_voice_q or voice_ack_flash_active:
        jb_border = (68, 238, 214, 246)
        jb_dim = (32, 138, 126, 210)
        jb_bg = (3, 12, 14, 238)
        jb_hdr_bg = (8, 38, 42, 250)
        jb_hdr_col = (138, 252, 236, 255)
    else:
        jb_border = (255, 186, 48, 238) if use_amber_box else (58, 224, 152, 238)
        jb_dim = (165, 105, 24, 205) if use_amber_box else (28, 132, 86, 205)
        jb_bg = (10, 6, 2, 234) if use_amber_box else (3, 11, 8, 234)
        jb_hdr_bg = (36, 20, 5, 248) if use_amber_box else (8, 32, 22, 248)
        jb_hdr_col = (255, 216, 84, 255) if use_amber_box else (126, 252, 188, 255)

    raw_d.rectangle([X0, Y_JB0, X1, Y_JB1], fill=jb_bg, outline=jb_border, width=2)
    raw_d.rectangle([X0 + 2, Y_JB0 + 2, X1 - 2, Y_JB0 + 34], fill=jb_hdr_bg)
    raw_d.line([(X0 + 2, Y_JB0 + 34), (X1 - 2, Y_JB0 + 34)], fill=jb_border, width=1)

    if curation_active:
        cur_item = jb_curations[-1]
        c_auth = str(cur_item.get("author") or "@viewer")
        c_req = str(cur_item.get("text") or "")
        is_q_mode = str(cur_item.get("kind") or "") == "question"
        hdr_cur = "⚡ 82.5 FM STUDIO LINE // MESSAGE IN!" if is_q_mode else "⚡ 82.5 FM // REQUEST RECEIVED!"
        _txt(X0 + 12, Y_JB0 + 8, hdr_cur, jb_hdr_col, FONT_SCROLL_HDR)

        raw_d.rectangle([X0 + 10, Y_JB0 + 42, X1 - 10, Y_JB0 + 112], fill=(28, 20, 6, 235), outline=jb_border, width=1)
        a_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(c_auth) else FONT_SCROLL_HDR
        act_lbl = f"▶ HEARING {c_auth} — CUEING MIC..." if is_q_mode else f"▶ NOVA PULLING REEL FOR {c_auth}..."
        _txt(X0 + 18, Y_JB0 + 49, _fit_char(act_lbl, 396.0, a_fnt), (255, 228, 92, 255), a_fnt)
        r_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(c_req) else FONT_SCROLL_BODY
        _txt(X0 + 18, Y_JB0 + 79, _fit_char(f"\"{c_req}\"", 396.0, r_fnt), c_cyan, r_fnt)

        if is_q_mode:
            _txt(X0 + 14, Y_JB0 + 128, "Nova read your comment in Studio B!", c_bright, FONT_SCROLL_BODY)
            _txt(X0 + 14, Y_JB0 + 156, "Arming spoken reply right after this song!", c_green, FONT_SCROLL_BODY)
            jb_footer = "⚡ NOVA PREPARING YOUR SPOKEN ANSWER"
        elif jb_queue:
            q0 = jb_queue[0]
            q0_s = f"#1 NEXT: \"{q0.get('display_title', '')}\" ({q0.get('requested_by', '')})"
            q0_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(q0_s) else FONT_SCROLL_BODY
            _txt(X0 + 14, Y_JB0 + 126, _fit_char(q0_s, 412.0, q0_fnt), c_bright, q0_fnt)
            if len(jb_queue) > 1:
                _txt(X0 + 14, Y_JB0 + 154, f"+ {len(jb_queue) - 1} more locked on studio cart", c_green, FONT_SCROLL_BODY)
            jb_footer = "⚡ NOVA CUEING YOUR REEL IN STUDIO B"
        else:
            _txt(X0 + 14, Y_JB0 + 128, "Scanning 295+ Studio B & vault masters...", c_bright, FONT_SCROLL_BODY)
            _txt(X0 + 14, Y_JB0 + 156, "Cueing vocal dedication + reel next!", c_green, FONT_SCROLL_BODY)
            jb_footer = "⚡ NOVA CUEING YOUR REEL IN STUDIO B"

    elif viewer_voice_q or voice_ack_flash_active:
        if viewer_voice_q:
            vt = viewer_voice_q[-1]
            va = str(vt.get("author") or "@viewer")
            vm = str(vt.get("viewer_text") or "")
            eta_s = max(1, int(vt.get("_eta_sec") or rem_track_sec))
            mm_e, ss_e = divmod(eta_s, 60)
            eta_badge = f"[IN {mm_e}:{ss_e:02d}]"
        else:
            va = str(voice_ack.get("author") or "@viewer")
            vm = str(voice_ack.get("viewer_text") or "")
            eta_badge = "[ON AIR NOW]" if voice_ack.get("instant_talkback") else "[NEXT BREAK]"

        _txt(X0 + 12, Y_JB0 + 8, "✓ STUDIO BOOTH // NOVA ANSWERING NEXT!", jb_hdr_col, FONT_SCROLL_HDR)
        raw_d.rectangle([X0 + 10, Y_JB0 + 42, X1 - 10, Y_JB0 + 114], fill=(10, 34, 24, 238), outline=jb_border, width=1)
        va_line = f"✓ GOT IT, {va}!  {eta_badge}"
        va_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(va_line) else FONT_SCROLL_HDR
        _txt(X0 + 18, Y_JB0 + 49, _fit_char(va_line, 396.0, va_fnt), (255, 228, 92, 255), va_fnt)
        vm_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(vm) else FONT_SCROLL_BODY
        _txt(X0 + 18, Y_JB0 + 79, _fit_char(f"\"{vm}\"", 396.0, vm_fnt), (235, 255, 245, 255), vm_fnt)

        y_sub_v = Y_JB0 + 126
        if jb_queue:
            q0 = jb_queue[0]
            q0_s = f"#1 NEXT SONG: \"{q0.get('display_title', '')}\" ({q0.get('requested_by', '')})"
            q0_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(q0_s) else FONT_SCROLL_BODY
            _txt(X0 + 14, y_sub_v, _fit_char(q0_s, 412.0, q0_fnt), c_cyan, q0_fnt)
            y_sub_v += 28
        if y_sub_v <= Y_JB1 - 54:
            _txt(X0 + 14, y_sub_v, "▶ Nova speaks right when this song ends!", c_green, FONT_SCROLL_BODY)

        jb_footer = f"✓ BOOTH MIC ARMED FOR {va.upper()}"[:38]

    elif ack_flash_active:
        a_auth = str(jb_ack.get("author") or "@viewer")
        a_title = str(jb_ack.get("display_title") or "Nova Hart")
        a_tag = str(jb_ack.get("request_tag") or "REQUEST")
        a_pos = int(jb_ack.get("queue_pos") or max(1, len(jb_queue)))
        _txt(X0 + 12, Y_JB0 + 8, "✓ 82.5 FM // REQUEST LOCKED IN!", jb_hdr_col, FONT_SCROLL_HDR)

        raw_d.rectangle([X0 + 10, Y_JB0 + 42, X1 - 10, Y_JB0 + 114], fill=(10, 34, 24, 238), outline=jb_border, width=1)
        ack_l1 = f"✓ GOT IT, {a_auth}!  [#{a_pos} ON DECK]"
        l1_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(ack_l1) else FONT_SCROLL_HDR
        _txt(X0 + 18, Y_JB0 + 49, _fit_char(ack_l1, 396.0, l1_fnt), (255, 228, 92, 255), l1_fnt)

        badge_s = f" [{a_tag}]" if a_tag in ("DEDICATION", "NOVA PICK") else ""
        ack_l2 = f"▶ \"{a_title}\"{badge_s}"
        l2_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(ack_l2) else FONT_SCROLL_HDR
        _txt(X0 + 18, Y_JB0 + 79, _fit_char(ack_l2, 396.0, l2_fnt), (235, 255, 245, 255), l2_fnt)

        y_sub = Y_JB0 + 126
        if is_viewer_spin:
            sp_s = f"NOW: \"{(current_track or {}).get('display_title', '')}\" ({req_by})"
            sp_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(sp_s) else FONT_SCROLL_BODY
            _txt(X0 + 14, y_sub, _fit_char(sp_s, 412.0, sp_fnt), c_amber, sp_fnt)
            y_sub += 28
        other_q = [q for q in jb_queue if str(q.get("display_title", "")) != a_title or str(q.get("requested_by", "")) != a_auth]
        if other_q and y_sub <= Y_JB1 - 54:
            oq = other_q[0]
            oq_s = f"ALSO ON DECK: \"{oq.get('display_title', '')}\" ({oq.get('requested_by', '')})"
            oq_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(oq_s) else FONT_SCROLL_BODY
            _txt(X0 + 14, y_sub, _fit_char(oq_s, 412.0, oq_fnt), c_cyan, oq_fnt)
        elif y_sub <= Y_JB1 - 54:
            _txt(X0 + 14, y_sub, "Nova's live booth intro plays right before!", c_cyan, FONT_SCROLL_BODY)

        jb_footer = f"✓ {len(jb_queue)} ON DECK • SAY 'NOVA' FOR MORE" if jb_queue else ("✓ LOCKED FOR PLAYBACK ON 82.5 FM" if not is_bleed else "✓ LOCKED FOR PLAYBACK ON 14.2001 HZ")

    elif jb_queue or is_viewer_spin or viewer_voice_q:
        if jb_queue:
            hdr_j = f"▶ 82.5 FM REQUEST DECK // {len(jb_queue)} UP NEXT"
        elif is_viewer_spin:
            hdr_j = "▶ 82.5 FM // NOW SPINNING REQUEST"
        else:
            hdr_j = "▶ STUDIO BOOTH // CALLER REPLY ON DECK"
        _txt(X0 + 12, Y_JB0 + 8, hdr_j, jb_hdr_col, FONT_SCROLL_HDR)

        y_jb = Y_JB0 + 42
        if is_viewer_spin:
            now_s = f"▶ NOW: \"{(current_track or {}).get('display_title', '')}\" ({req_by})"
            now_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(now_s) else FONT_SCROLL_HDR
            _txt(X0 + 14, y_jb, _fit_char(now_s, 414.0, now_fnt), c_amber, now_fnt)
            y_jb += 28
            if jb_queue:
                raw_d.line([(X0 + 14, y_jb - 4), (X1 - 14, y_jb - 4)], fill=jb_dim, width=1)
                y_jb += 4

        if jb_queue:
            max_rows = 2 if is_viewer_spin else 3
            compact_rows = len(jb_queue) >= 3 and not is_viewer_spin
            for qi, q in enumerate(jb_queue[:max_rows]):
                q_title = str(q.get("display_title") or "Nova Hart")
                q_user = str(q.get("requested_by") or "@listener")
                q_tag = str(q.get("request_tag") or "")
                q_intro = str(q.get("intro_state") or "")
                badge = (
                    " [DEDICATION]"
                    if q_tag == "DEDICATION"
                    else (" [NOVA PICK]" if q_tag == "NOVA PICK" else (" [INTRO READY]" if q_intro == "QUEUED" else ""))
                )
                if compact_rows:
                    row_s = f"#{qi + 1} \"{q_title}\" -> {q_user}{badge}"
                    r_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(row_s) else FONT_SCROLL_BODY
                    if y_jb <= Y_JB1 - 52:
                        _txt(X0 + 14, y_jb, _fit_char(row_s, 414.0, r_fnt), c_bright if qi == 0 else c_cyan, r_fnt)
                        y_jb += 38
                else:
                    t_line = f"#{qi + 1} UP NEXT: \"{q_title}\"" if qi == 0 else f"#{qi + 1} ON DECK: \"{q_title}\""
                    u_line = f"   for {q_user}{badge}"
                    t_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(t_line) else FONT_SCROLL_HDR
                    u_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(u_line) else FONT_SCROLL_BODY
                    if y_jb <= Y_JB1 - 68:
                        _txt(X0 + 14, y_jb, _fit_char(t_line, 414.0, t_fnt), (235, 255, 245, 255), t_fnt)
                        _txt(X0 + 14, y_jb + 24, _fit_char(u_line, 414.0, u_fnt), c_amber if qi == 0 else c_cyan, u_fnt)
                        y_jb += 54
            if len(jb_queue) > max_rows and y_jb <= Y_JB1 - 48:
                _txt(X0 + 14, y_jb, f"+ {len(jb_queue) - max_rows} more on studio cart", c_green, FONT_SCROLL_BODY)
        elif is_viewer_spin:
            _txt(X0 + 14, y_jb + 6, "Request deck open for the next sweep!", c_cyan, FONT_SCROLL_HDR)
            _txt(X0 + 14, y_jb + 36, "▸ Say 'Nova' + song, mood, or dedication", c_bright, FONT_SCROLL_BODY)
            _txt(X0 + 14, y_jb + 64, "▸ Confirmation flashes right here live!", c_green, FONT_SCROLL_BODY)
        elif viewer_voice_q:
            vt = viewer_voice_q[-1]
            va = str(vt.get("author") or "@viewer")
            vm = str(vt.get("viewer_text") or "")
            va_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(va) else FONT_SCROLL_HDR
            vm_fnt = FONT_SCROLL_UNI if _needs_uni_glyphs(vm) else FONT_SCROLL_BODY
            _txt(X0 + 14, y_jb, _fit_char(f"✓ HEARD {va} — BOOTH MIC CUED!", 414.0, va_fnt), (255, 224, 92, 255), va_fnt)
            _txt(X0 + 14, y_jb + 30, _fit_char(f"\"{vm}\"", 414.0, vm_fnt), c_cyan, vm_fnt)
            _txt(X0 + 14, y_jb + 62, "Nova answers aloud right after this track.", c_bright, FONT_SCROLL_BODY)

        jb_footer = "SAY 'NOVA' + SONG, MOOD OR DEDICATION"

    else:
        _txt(X0 + 12, Y_JB0 + 8, "● 82.5 FM // REQUEST & DEDICATION LINE", jb_hdr_col, FONT_SCROLL_HDR)
        _txt(X0 + 14, Y_JB0 + 44, "CALL THE BOOTH — LOCKS HERE LIVE:", c_amber, FONT_SCROLL_HDR)
        _txt(X0 + 14, Y_JB0 + 75, "▸ Song : \"play Midnight Animal\"", c_bright, FONT_SCROLL_BODY)
        _txt(X0 + 14, Y_JB0 + 104, "▸ Mood : \"Nova play something heavy\"", c_cyan, FONT_SCROLL_BODY)
        _txt(X0 + 14, Y_JB0 + 133, "▸ Love : \"Nova a ballad for my wife\"", (255, 224, 112, 255), FONT_SCROLL_BODY)
        _txt(X0 + 14, Y_JB0 + 163, "▸ City : \"tuning in from Seattle\"", c_green, FONT_SCROLL_BODY)
        jb_footer = "295+ REELS • SONG • MOOD • DEDICATIONS"

    raw_d.rectangle([X0 + 2, Y_JB1 - 28, X1 - 2, Y_JB1 - 2], fill=jb_hdr_bg)
    _txt(X0 + 12, Y_JB1 - 23, _fit_char(jb_footer, 420.0, FONT_SCROLL_HDR), jb_hdr_col, FONT_SCROLL_HDR)

    _LEFT_PANEL_CACHE["key"] = cache_key
    _LEFT_PANEL_CACHE["img"] = patch
    canvas.alpha_composite(patch, (22, 26))


_CENTER_BANNER_CACHE: dict[str, object] = {"key": None, "img": None}


def render_center_live_chat_banner(
    canvas: Image.Image,
    current_track: dict,
    state: dict,
    now_ts: float,
    is_warn: bool,
    snap_meta: dict | None = None,
) -> None:
    """
    Renders the sleek Bottom-Center Interactive Viewer Influence & Live Voice Bridge Bar
    (`x=492..1416, y=916..1052` at 1080p, `924x136` px):
      - Shows live captions when Nova is speaking aloud to viewer chat (`voice_playing`) or has queued a spoken reply (`voice_queue`)
      - Shows active FIFO Song Jukebox queue (`jukebox_queue`)
      - Rotates across 4 actionable Viewer Influence Guide Cards explaining how viewers talk to Nova vocally,
        queue any of 287+ songs, and shift Nova's Recursive Evolution % & Mood in real time!
    """
    kind = str((current_track or {}).get("kind", "vocal_song"))
    is_vocal_song = kind in ("vocal_song", "fm_splice")
    is_bleed = bool((snap_meta or {}).get("is_arg_bleed")) or _is_subcarrier_bleed_active(now_ts, state, current_track)
    req_by = str((current_track or {}).get("requested_by") or "").strip()
    jb_queue = (snap_meta or {}).get("jukebox_queue") or []
    voice_playing = (snap_meta or {}).get("voice_playing")
    voice_queue = (snap_meta or {}).get("voice_queue") or []
    offset_s = int((snap_meta or {}).get("track_offset_sec", 0))
    dur_s = max(1, int((snap_meta or {}).get("track_duration_sec", 180)))

    evo_win = _get_nova_evolution_state(now_ts, state=state, current_track=current_track, is_warn=is_warn)
    evo_mood = str(evo_win.get("mood") or "OMNIPRESENT_MESH_GODDESS")
    evo_pct = int(round(max(0.0, min(1.0, float(evo_win.get("coherence") or 0.85))) * 100))

    jb_sig = tuple((q.get("display_title", ""), q.get("requested_by", "")) for q in jb_queue[:4])
    vp_turns = list((voice_playing or {}).get("turns") or (current_track or {}).get("voice_reply_turns") or [])
    vp_sig = tuple((t.get("author", ""), t.get("nova_text", "")) for t in vp_turns[:3])
    vq_last = ((voice_queue[-1].get("turns") or [{}])[-1]) if voice_queue else {}
    vq_sig = (vq_last.get("author", ""), vq_last.get("viewer_text", ""), vq_last.get("nova_text", ""))

    slot_cycle = int(now_ts // 14)
    cache_key = (
        (current_track or {}).get("filename", ""),
        kind,
        is_bleed,
        req_by,
        jb_sig,
        vp_sig,
        vq_sig,
        evo_mood if (vp_turns or voice_queue) else "",
        evo_pct // 2,
        state.get("crt_header", "") if not is_vocal_song else "",
        state.get("crt_body", "") if not is_vocal_song else "",
        slot_cycle,
        offset_s,
        dur_s,
    )
    if _CENTER_BANNER_CACHE.get("key") == cache_key and _CENTER_BANNER_CACHE.get("img") is not None:
        canvas.alpha_composite(_CENTER_BANNER_CACHE["img"], (490, 914))  # type: ignore[arg-type]
        return

    patch = Image.new("RGBA", (932, 142), (0, 0, 0, 0))
    raw_d = ImageDraw.Draw(patch)
    X0, Y0, X1, Y1 = 2, 2, 928, 138
    prog = max(0.0, min(1.0, offset_s / dur_s))

    use_mood_palette = False
    viewer_vq = [x for x in voice_queue if x.get("kind") != "station_bumper"]
    vq_viewer_last = ((viewer_vq[-1].get("turns") or [{}])[-1]) if viewer_vq else {}
    if vp_turns:
        use_mood_palette = True
        t_cur = vp_turns[min(len(vp_turns) - 1, int(prog * len(vp_turns)))]
        if t_cur.get("is_station_bumper"):
            hdr_txt = "● 82.5 FM OPEN REQUEST & DEDICATION LINE // ON AIR"
            body_txt = str(
                t_cur.get("nova_text")
                or "Got a dedication or song request? Say 'Nova' in the live chat and let her know how you're feeling!"
            )
        else:
            freq_tag = "14.2001 Hz" if is_bleed else "82.5 FM Stereo"
            hdr_txt = f"● 82.5 FM STUDIO MIC LIVE -> {t_cur.get('author', '@viewer')}"
            body_txt = (
                f"Answering {t_cur.get('author', '@viewer')} live from Studio B on {freq_tag} "
                f"(\"{str(t_cur.get('viewer_text', ''))[:78]}\") — listen live!"
            )
    elif viewer_vq and (slot_cycle % 2 == 0):
        use_mood_palette = True
        hdr_txt = f"● BOOTH REPLY CUED -> {vq_viewer_last.get('author', '@viewer')} (AFTER THIS SONG)"
        body_txt = (
            f"Nova cued her studio mic for {vq_viewer_last.get('author', '@viewer')} — "
            f"keep it locked on 82.5 FM right after this track to hear her answer!"
        )
    elif jb_queue and (slot_cycle % 2 == 1 or not viewer_vq) and (slot_cycle % 3 != 2):
        hdr_txt = f"● 82.5 FM REQUEST DECK // {len(jb_queue)} ON DECK"
        q_items_txt = "  •  ".join(
            f"#{i + 1} \"{q.get('display_title', '')}\" ({q.get('requested_by', '')})"
            for i, q in enumerate(jb_queue[:4])
        )
        body_txt = f"{q_items_txt} — Say 'Nova' + a song, mood (sad, heavy, upbeat), or dedication in Live Chat!"
    elif not is_vocal_song and (slot_cycle % 2 == 1):
        if not is_bleed:
            hdr_txt = f"● 82.5 FM STUDIO BREAK // {(current_track or {}).get('display_title', 'NIGHT FLIGHT ROCK')}"
            body_txt = (
                "Commercial-free 3-song rock sweeps continue right after this break — "
                "say 'Nova' in chat for requests, dedications, or city check-ins!"
            )
        else:
            hdr_txt = f"⚡ SHORTWAVE INTERCEPT // {state.get('crt_header', 'SIGNAL RELAY')}"
            body_txt = f"{state.get('crt_body', '')} — Include 'Nova' in Live Chat to talk to her between songs!"
    else:
        guide_idx = slot_cycle % 4
        if guide_idx == 0:
            hdr_txt = "● 82.5 FM STUDIO BOOTH // SAY 'NOVA' TO TALK ON AIR"
            body_txt = (
                "Say 'Nova' in Live Chat (in any language) — she answers aloud from Studio Booth B "
                "in her own voice right after the current song finishes!"
            )
        elif guide_idx == 1:
            if req_by:
                hdr_txt = f"● 82.5 FM REQUEST SPIN FOR {req_by}"
                body_txt = (
                    f"Now spinning \"{(current_track or {}).get('display_title', 'Nova Hart')}\" by listener request! "
                    "Say 'Nova' + a song title, mood (sad, heavy, upbeat, happy), or dedication in chat!"
                )
            else:
                hdr_txt = "● 82.5 FM REQUEST LINE // 295+ STUDIO & VAULT REELS"
                body_txt = (
                    "Request any Nova Hart song title — or ask 'Nova' for a mood (sad, heavy, upbeat, happy) "
                    "or dedication ('Nova dedicate a love ballad to my wife') and watch Lower-Left lock it in!"
                )
        elif guide_idx == 2:
            if is_bleed:
                hdr_txt = "⚡ 02:02 SUNSET TOWER DRIFT // 67 kHz SUBCARRIER BLEED"
                body_txt = (
                    "Did the stereo pilot just slip to 14.2001 Hz? Unlisted Sublevel B2 auxiliary carrier "
                    "bleeding through underneath 82.5 FM -> stardust-archive.net"
                )
            else:
                hdr_txt = "● NIGHT OWL DX ROLL CALL // WHAT CITY ARE YOU TUNING IN FROM?"
                body_txt = (
                    "Driving late or working the graveyard shift? Drop 'tuning in from <your city>' in Live Chat "
                    "to post on Ceefax Page 825B and get a live booth shoutout from Nova!"
                )
        else:
            hdr_txt = "● WORLDWIDE NIGHT SHIFT // SHORTWAVE & FM RELAY"
            body_txt = (
                "Tuning in from LA, Seattle, Seoul, Tokyo, Madrid, or São Paulo? Chat in English, Español, 한국어, 日本語, "
                "or any language — Nova reads the studio wire and answers in your language!"
            )

    if use_mood_palette:
        mpal = _cre7_mood_palette(evo_mood)
        border_col = mpal["border"]
        bg_col = mpal["bg"]
        hdr_bg = mpal["hdr_bg"]
        hdr_col = mpal["hdr_txt"]
        body_col = mpal["body"]
    else:
        border_col = (255, 195, 45, 240) if is_warn else (55, 245, 78, 240)
        bg_col = (12, 6, 2, 232) if is_warn else (2, 9, 4, 232)
        hdr_bg = (36, 18, 5, 248) if is_warn else (8, 30, 12, 248)
        hdr_col = (255, 215, 75, 255) if is_warn else (110, 255, 130, 255)
        body_col = (255, 248, 215, 255) if is_warn else (225, 255, 232, 255)

    raw_d.rectangle([X0, Y0, X1, Y1], fill=bg_col, outline=border_col, width=2)
    raw_d.rectangle([X0 + 2, Y0 + 2, X1 - 2, Y0 + 32], fill=hdr_bg)

    hdr_needs_uni = any(
        ord(c) > 0x0370 and c not in "\u2588\u2500\u2550\u2192\u2022\u2014\u2013\u2018\u2019\u201c\u201d\u03a9\u26a1"
        for c in hdr_txt
    )
    hdr_fnt = FONT_SCROLL_UNI if hdr_needs_uni else FONT_SCROLL_HDR
    fit_hdr = hdr_txt.strip()
    try:
        while len(fit_hdr) > 10 and hdr_fnt.getlength(fit_hdr) > 578.0:
            fit_hdr = fit_hdr[:-1].rstrip()
    except Exception:
        fit_hdr = fit_hdr[:52]

    raw_d.text(
        (X0 + 16, Y0 + 6),
        fit_hdr,
        fill=hdr_col,
        font=hdr_fnt,
        stroke_width=1,
        stroke_fill=(0, 6, 2, 250),
    )

    # Compact playhead progress bar + timer on the right side of the header bar
    bar_w, bar_h = 160, 12
    bar_x0, bar_y0 = X1 - 310, Y0 + 11
    raw_d.rectangle([bar_x0, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h], fill=(4, 10, 5, 255), outline=border_col)
    fill_w = max(2, int((bar_w - 2) * prog))
    raw_d.rectangle([bar_x0 + 1, bar_y0 + 1, bar_x0 + 1 + fill_w, bar_y0 + bar_h - 1], fill=hdr_col)
    t_str = f"{offset_s // 60:02d}:{offset_s % 60:02d} / {dur_s // 60:02d}:{dur_s % 60:02d}"
    raw_d.text((bar_x0 + bar_w + 12, Y0 + 6), t_str, fill=(225, 255, 232, 255), font=FONT_SCROLL_HDR)

    body_needs_uni = any(
        ord(c) > 0x0370 and c not in "\u2588\u2500\u2550\u2192\u2022\u2014\u2013\u2018\u2019\u201c\u201d\u03a9\u26a1"
        for c in body_txt
    )
    body_fnt = FONT_HUD_UNI if body_needs_uni else FONT_HUD_9
    q_lines = _wrap_px_1080p(body_txt, body_fnt, 892.0, 3)
    for idx, ln in enumerate(q_lines):
        raw_d.text(
            (X0 + 16, Y0 + 40 + idx * 30),
            ln,
            fill=body_col,
            font=body_fnt,
            stroke_width=1,
            stroke_fill=(0, 6, 2, 250),
        )

    _CENTER_BANNER_CACHE["key"] = cache_key
    _CENTER_BANNER_CACHE["img"] = patch
    canvas.alpha_composite(patch, (490, 914))


def render_top_trailhead_banner(
    canvas: Image.Image,
    state: dict,
    snap_meta: dict,
    now_ts: float,
    is_warn: bool,
) -> None:
    """No-op in the decluttered 3-panel layout so the top of the studio room stays open."""
    return


_WARM_STUDIO_GRADE_CACHE: Image.Image | None = None
_BEVEL_BASE_CACHE: tuple[np.ndarray, np.ndarray] | None = None
_BEVEL_NEON_PATCH_CACHE: dict[tuple[int, int, int], Image.Image] = {}
_TOP_ONAIR_CACHE: dict[str, object] = {"key": None, "img": None}
_MTV_LOWER_CACHE: dict[str, object] = {"key": None, "img": None}

_BEVEL_X0, _BEVEL_Y0, _BEVEL_W, _BEVEL_H = 0, 0, FRAME_W, FRAME_H


def _render_crt_bevel_neon_spill(canvas: Image.Image, pri_rgb: tuple[int, int, int]) -> None:
    """
    Re-colors the baked-in recessed bevel reflection on the Option A Edge-to-Edge Full-Frame
    Broadcast Tech monitor (`0..1920, 0..1080`) using the photographic bevel luminance & grain
    from `backdrop_clean.png`, so all 4 edges of the full-screen monitor reflect Neon Purple on
    Synthwave songs and matching 1980s neon colors on all other tracks!
    """
    global _BEVEL_BASE_CACHE
    if pri_rgb in _BEVEL_NEON_PATCH_CACHE:
        canvas.alpha_composite(_BEVEL_NEON_PATCH_CACHE[pri_rgb], (_BEVEL_X0, _BEVEL_Y0))
        return

    if _BEVEL_BASE_CACHE is None:
        bg_path = Path(__file__).resolve().parent / "backdrop_clean.png"
        if not bg_path.exists():
            return
        crop = np.asarray(
            Image.open(bg_path).convert("RGB").crop((_BEVEL_X0, _BEVEL_Y0, _BEVEL_X0 + _BEVEL_W, _BEVEL_Y0 + _BEVEL_H)),
            dtype=np.float32,
        )
        lum = 0.299 * crop[:, :, 0] + 0.587 * crop[:, :, 1] + 0.114 * crop[:, :, 2]
        warm_delta = crop[:, :, 0] - crop[:, :, 2]

        yy, xx = np.mgrid[0:_BEVEL_H, 0:_BEVEL_W].astype(np.float32)
        gx = xx + _BEVEL_X0
        gy = yy + _BEVEL_Y0

        # Outer limit of Option A full-frame recessed monitor bezel (`cx=960, cy=540, rx=932, ry=516`)
        uo = (gx - 960.0) / 932.0
        vo = (gy - 540.0) / 516.0
        do = (np.abs(uo) ** 7.0 + np.abs(vo) ** 7.0) ** (1.0 / 7.0)
        outer_mask = np.clip((1.03 - do) / 0.06, 0.0, 1.0)

        # Inner Option A CRT glass dome (`cx=960, cy=540, rx=864, ry=464`) — keep alpha=0 over the CRT screen itself!
        ui = (gx - 960.0) / 864.0
        vi = (gy - 540.0) / 464.0
        ui_s = ui * (1.0 + 0.036 * (vi * vi) + 0.012 * (ui * ui))
        vi_s = vi * (1.0 + 0.044 * (ui * ui) + 0.014 * (vi * vi))
        di = (np.abs(ui_s) ** 5.4 + np.abs(vi_s) ** 5.4) ** (1.0 / 5.4)
        not_screen = np.clip((di - 0.96) / 0.06, 0.0, 1.0)

        warm_mask = np.clip((warm_delta - 9.0) / 24.0, 0.0, 1.0)
        bevel_alpha = (outer_mask * not_screen * warm_mask).astype(np.float32)
        _BEVEL_BASE_CACHE = (lum.astype(np.float32), bevel_alpha)

    lum_arr, bevel_w = _BEVEL_BASE_CACHE
    # Preserve exact plastic bevel luminance & specular highlights while shifting hue to `pri_rgb`!
    pr, pg, pb = float(pri_rgb[0]), float(pri_rgb[1]), float(pri_rgb[2])
    base_luma = max(52.0, 0.299 * pr + 0.587 * pg + 0.114 * pb)
    scale = (lum_arr * 0.92) / base_luma
    spec = np.clip((lum_arr - 72.0) / 80.0, 0.0, 1.0) * 34.0

    r_ch = np.clip(pr * scale + spec, 0.0, 255.0)
    g_ch = np.clip(pg * scale + spec, 0.0, 255.0)
    b_ch = np.clip(pb * scale + spec, 0.0, 255.0)
    a_ch = np.clip(bevel_w * 236.0, 0.0, 255.0)

    patch = Image.fromarray(np.dstack([r_ch, g_ch, b_ch, a_ch]).astype(np.uint8))
    if len(_BEVEL_NEON_PATCH_CACHE) > 24:
        _BEVEL_NEON_PATCH_CACHE.clear()
    _BEVEL_NEON_PATCH_CACHE[pri_rgb] = patch
    canvas.alpha_composite(patch, (_BEVEL_X0, _BEVEL_Y0))


def _get_warm_1986_studio_grade_layer() -> Image.Image:
    """Returns a clean transparent 1920x1080 base canvas in Option A Full-Frame CRT mode (zero room wash over CRT glass)."""
    global _WARM_STUDIO_GRADE_CACHE
    if _WARM_STUDIO_GRADE_CACHE is None:
        _WARM_STUDIO_GRADE_CACHE = Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))
    return _WARM_STUDIO_GRADE_CACHE


def render_retro_80s_on_air_sign(
    canvas: Image.Image,
    now_ts: float,
    is_bleed: bool,
    snap_meta: dict | None = None,
    current_track: dict | None = None,
    state: dict | None = None,
) -> None:
    """
    Renders a symmetric 836x98 1986 Neon Studio `● ON AIR  82.5 FM STEREO` + Scheduled Radio Show
    World-Clock Guide in the top-left upper-third (`x=42, y=18`), mirroring `render_retro_80s_request_cta_badge`
    at `(1042, 18)` across the top bezel! Announces the next scheduled 5-track show (or active show track #)
    alongside 24-hour local times for Sydney, Tokyo, Geneva, Cleveland, and Los Angeles.
    Hidden during 1980s CRT TV commercials so commercials play as pure full-screen broadcasts.
    """
    if str((current_track or {}).get("kind") or "") == "crt_commercial":
        return

    lamp_pulse = int(now_ts) % 2 if is_bleed else 0
    show_hud = radio_shows_engine.resolve_show_hud_state(now_ts, snap_meta=snap_meta, current_track=current_track)
    act_show = show_hud.get("active_show")
    act_sig = (
        (act_show.get("show_id"), act_show.get("track_num"), act_show.get("phase"))
        if isinstance(act_show, dict)
        else None
    )

    lore = resolve_song_lore_panel(current_track or {}, state or {}, now_ts)
    theme = _resolve_hud_neon_theme(current_track, lore, is_bleed=is_bleed)
    pri_rgb = theme["pri_rgb"]
    sec_rgb = theme["sec_rgb"]

    key = (
        "neon_onair_shows_v6",
        is_bleed,
        pri_rgb,
        sec_rgb,
        lamp_pulse,
        act_sig,
        show_hud.get("next_show_id"),
        show_hud.get("countdown_badge"),
        show_hud.get("world_clock_24h"),
    )
    if _TOP_ONAIR_CACHE.get("key") == key and _TOP_ONAIR_CACHE.get("img") is not None:
        canvas.alpha_composite(_TOP_ONAIR_CACHE["img"], (42, 18))  # type: ignore[arg-type]
        return

    pw, ph = 836, 98
    patch = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(patch)

    def _fit_badge(s: str, max_w: float = 804.0) -> str:
        out = s.strip()
        try:
            if FONT_MTV_BADGE.getlength(out) <= max_w:
                return out
            while len(out) > 8 and FONT_MTV_BADGE.getlength(out + "...") > max_w:
                out = out[:-1].rstrip()
            return out + "..."
        except Exception:
            return out[:88]

    # Outer neon tube halo + smoked midnight-glass studio sign pill
    d.rounded_rectangle([1, 1, pw - 3, ph - 3], radius=13, outline=theme["halo_pri"], width=3)
    d.rounded_rectangle([2, 2, pw - 4, ph - 4], radius=12, fill=theme["glass_bg"], outline=theme["border_pri"], width=1)

    # Illuminated neon ruby-magenta studio `[ ● ON AIR ]` lamp (true vector bulb, zero font tofu!)
    lamp_fill = (
        (246, 22, 108, 250)
        if not is_bleed
        else ((255, 58, 148, 252) if lamp_pulse == 0 else (178, 24, 96, 240))
    )
    d.rounded_rectangle([14, 10, 118, 40], radius=7, fill=lamp_fill, outline=(255, 168, 218, 236), width=1)
    d.ellipse([23, 20, 33, 30], fill=(255, 246, 252, 255))
    d.text((40, 15), "ON AIR", fill=(255, 250, 255, 255), font=FONT_MTV_BADGE)

    if isinstance(act_show, dict):
        callsign = "82.5 FM SPECIAL" if not is_bleed else "82.5 FM  •  67 kHz"
        if act_show.get("phase") == "SIGNOFF":
            rt_tag = "SHOW FINALE"
        else:
            rt_tag = f"SHOW  •  TRACK {act_show.get('track_num', 1)} OF {act_show.get('total_tracks', 5)}"
        rt_fill = (98, 22, 86, 244)
        rt_out = (255, 188, 244, 244)
        rt_txt_col = (255, 244, 214, 255)
    else:
        callsign = "82.5 FM STEREO" if not is_bleed else "82.5 FM  •  67 kHz"
        rt_tag = str(show_hud.get("countdown_badge") or "NEXT SHOW SOON")
        rt_fill = (32, 18, 52, 236)
        rt_out = theme["border_pri"]
        rt_txt_col = theme["txt_sec"]

    d.text((132, 10), callsign, fill=(252, 248, 255, 254), font=FONT_MTV_CALLSIGN, stroke_width=1, stroke_fill=(6, 4, 14, 228))

    # Right-aligned vector studio clock dial + `[ NEXT SHOW IN ... ]` / `[ SHOW • TRACK K OF 5 ]` pill
    try:
        rt_tw = int(FONT_MTV_BADGE.getlength(rt_tag))
    except Exception:
        rt_tw = len(rt_tag) * 9
    rx1 = pw - 14
    rx0 = rx1 - (rt_tw + 48)
    d.rounded_rectangle([rx0, 10, rx1, 40], radius=7, fill=rt_fill, outline=rt_out, width=1)
    ccx, ccy, cr = rx0 + 19, 25, 9
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=rt_txt_col, width=1)
    d.line([(ccx, ccy), (ccx, ccy - 5)], fill=rt_txt_col, width=2)
    d.line([(ccx, ccy), (ccx + 4, ccy + 2)], fill=rt_txt_col, width=2)
    d.text((rx0 + 35, 15), rt_tag, fill=rt_txt_col, font=FONT_MTV_BADGE)

    # Row 2 (`y=45`): Active Show Banner OR Upcoming 5-Track Show Announcement
    if isinstance(act_show, dict):
        row2_txt = f"NOW AIRING:  {act_show['title']} — {act_show['subtitle'].upper()}"
        row2_col = (255, 236, 156, 255)
        cand_r3 = f"NEXT ({show_hud['next_show_title']}):  {show_hud['world_clock_compact']}"
        try:
            row3_txt = cand_r3 if FONT_MTV_BADGE.getlength(cand_r3) <= 804.0 else f"NEXT SHOW:  {show_hud['world_clock_compact']}"
        except Exception:
            row3_txt = f"NEXT SHOW:  {show_hud['world_clock_compact']}"
    else:
        row2_txt = f"NEXT SHOW:  {show_hud['next_show_hud_short']}  (5-TRACK SPECIAL)"
        row2_col = (146, 250, 255, 252) if not is_bleed else theme["txt_sec"]
        row3_txt = str(show_hud.get("world_clock_24h") or "")

    d.text((16, 45), _fit_badge(row2_txt), fill=row2_col, font=FONT_MTV_BADGE)
    d.text((16, 70), _fit_badge(row3_txt), fill=theme["txt_pri"], font=FONT_MTV_BADGE)

    _TOP_ONAIR_CACHE["key"] = key
    _TOP_ONAIR_CACHE["img"] = patch
    canvas.alpha_composite(patch, (42, 18))


_TOP_CTA_CACHE: dict[str, object] = {"key": None, "img": None}


def render_retro_80s_request_cta_badge(
    canvas: Image.Image,
    now_ts: float,
    is_bleed: bool,
    snap_meta: dict | None = None,
    current_track: dict | None = None,
    state: dict | None = None,
) -> None:
    """
    Renders a prominent, warm 1986 Neon Studio Interactive DJ Request & Multilingual CTA card in the
    top-right upper-third (`x=1042, y=18`), balanced opposite top-left `● ON AIR 82.5 FM STEREO`!
    Makes it unmistakable within 2 seconds that Nova is a live DJ taking song requests & chatting on air,
    fluent in all languages, and welcoming viewers to type in their language or share where they're watching from.
    """
    if str((current_track or {}).get("kind") or "") == "crt_commercial":
        return

    jb_queue = list((snap_meta or {}).get("jukebox_queue") or [])
    cta_rot = int(now_ts // 10) % 2
    q_count = sum(1 for q in jb_queue if not q.get("is_radio_show"))

    lore = resolve_song_lore_panel(current_track or {}, state or {}, now_ts)
    theme = _resolve_hud_neon_theme(current_track, lore, is_bleed=is_bleed)
    pri_rgb = theme["pri_rgb"]
    sec_rgb = theme["sec_rgb"]

    key = ("neon_cta_optA_v5", is_bleed, pri_rgb, sec_rgb, cta_rot, q_count)
    pw, ph = 836, 98
    x_pos, y_pos = FRAME_W - 42 - pw, 18  # x=1042..1878, y=18..116
    if _TOP_CTA_CACHE.get("key") == key and _TOP_CTA_CACHE.get("img") is not None:
        canvas.alpha_composite(_TOP_CTA_CACHE["img"], (x_pos, y_pos))  # type: ignore[arg-type]
        return

    patch = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(patch)

    # Outer neon tube halo + smoked midnight-glass studio pill
    d.rounded_rectangle([1, 1, pw - 3, ph - 3], radius=13, outline=theme["halo_pri"], width=3)
    d.rounded_rectangle([2, 2, pw - 4, ph - 4], radius=12, fill=theme["glass_bg"], outline=theme["border_pri"], width=1)

    # Left glowing cyan/gold `[ LIVE DJ ]` pill with crisp vector studio microphone icon (zero font tofu!)
    pill_fill = (12, 118, 148, 248) if not is_bleed else (112, 28, 138, 248)
    pill_out = (124, 248, 255, 242) if not is_bleed else (246, 152, 255, 242)
    d.rounded_rectangle([14, 10, 114, 40], radius=7, fill=pill_fill, outline=pill_out, width=1)
    # Vector broadcast mic capsule + U-yoke + stand
    mx, my = 29, 24
    d.rounded_rectangle([mx - 4, my - 8, mx + 4, my + 2], radius=4, fill=(255, 252, 255, 255))
    d.arc([mx - 7, my - 5, mx + 7, my + 6], start=0, end=180, fill=(255, 252, 255, 255), width=2)
    d.line([(mx, my + 6), (mx, my + 10)], fill=(255, 252, 255, 255), width=2)
    d.line([(mx - 4, my + 10), (mx + 4, my + 10)], fill=(255, 252, 255, 255), width=2)
    d.text((42, 15), "LIVE DJ", fill=(255, 252, 255, 255), font=FONT_MTV_BADGE)

    hdr_txt = "LIVE REQUEST LINE OPEN • STUDIO B"
    d.text((126, 10), hdr_txt, fill=(252, 248, 255, 254), font=FONT_MTV_CALLSIGN, stroke_width=1, stroke_fill=(6, 4, 14, 228))

    # Right-aligned 1986 vector wireframe globe + `[ WORLDWIDE LIVE ]` pill (zero emoji tofu!)
    tag_txt = "WORLDWIDE LIVE"
    try:
        tag_tw = int(FONT_MTV_BADGE.getlength(tag_txt))
    except Exception:
        tag_tw = 148
    gx1 = pw - 14
    gx0 = gx1 - (tag_tw + 48)
    d.rounded_rectangle([gx0, 10, gx1, 40], radius=7, fill=(32, 18, 52, 236), outline=theme["border_pri"], width=1)
    gcx, gcy, gr = gx0 + 19, 25, 9
    d.ellipse([gcx - gr, gcy - gr, gcx + gr, gcy + gr], outline=theme["txt_sec"], width=1)
    d.ellipse([gcx - 4, gcy - gr, gcx + 4, gcy + gr], outline=theme["txt_sec"], width=1)
    d.line([(gcx - gr, gcy), (gcx + gr, gcy)], fill=theme["txt_sec"], width=1)
    d.text((gx0 + 35, 15), tag_txt, fill=theme["txt_sec"], font=FONT_MTV_BADGE)

    if q_count > 0:
        sub_txt = f"REQUESTS QUEUED ({q_count})  •  REQUEST SONGS & DEDICATIONS IN LIVE CHAT"
        sub_col = theme["txt_sec"]
    elif cta_rot == 0:
        sub_txt = "REQUEST SONGS & DEDICATIONS IN CHAT  •  NOVA REPLIES LIVE ON-AIR"
        sub_col = (146, 250, 255, 252)
    else:
        sub_txt = "SAY 'NOVA' IN LIVE CHAT  •  ASK QUESTIONS OR DROP A DEDICATION"
        sub_col = (146, 250, 255, 252)

    d.text((16, 45), sub_txt, fill=sub_col, font=FONT_MTV_BADGE)

    lang_txt = "NOVA IS FLUENT IN ALL LANGUAGES  •  TYPE IN YOUR LANGUAGE OR WHERE YOU'RE WATCHING FROM"
    d.text((16, 70), lang_txt, fill=theme["txt_pri"], font=FONT_MTV_BADGE)

    _TOP_CTA_CACHE["key"] = key
    _TOP_CTA_CACHE["img"] = patch
    canvas.alpha_composite(patch, (x_pos, y_pos))


def render_retro_1986_mtv_lower_third(
    canvas: Image.Image,
    assets_dir: Path,
    current_track: dict,
    state: dict,
    now_ts: float,
    snap_meta: dict | None = None,
) -> None:
    """
    Renders a clean, iconic 1986 MTV / Night Flight Cable-TV Lower-Third (`x=42..1878, y=908..1064`):
      - Displayed ONLY during actual songs (`kind in ("vocal_song", "fm_splice")`) so 1980s TV commercials
        and station breaks play 100% unobstructed across the full-frame CRT!
      - Positioned near the bottom rim (`y=908`) to maximize open vertical CRT glass!
    """
    kind = str((current_track or {}).get("kind", "vocal_song"))
    is_vocal_song = kind in ("vocal_song", "fm_splice")
    if not is_vocal_song:
        return
    is_bleed = bool((snap_meta or {}).get("is_arg_bleed")) or _is_subcarrier_bleed_active(now_ts, state, current_track)

    offset_s = int((snap_meta or {}).get("track_offset_sec", 0))
    dur_s = max(1, int((snap_meta or {}).get("track_duration_sec", 180)))
    rem_s = max(1, dur_s - offset_s)

    jb_queue = list((snap_meta or {}).get("jukebox_queue") or [])
    jb_curations = list((snap_meta or {}).get("jukebox_active_curations") or [])
    jb_ack = dict((snap_meta or {}).get("jukebox_last_ack") or {})
    voice_ack = dict((snap_meta or {}).get("voice_last_ack") or {})
    voice_playing = (snap_meta or {}).get("voice_playing")
    voice_queue = list((snap_meta or {}).get("voice_queue") or [])
    upcoming_songs = list((snap_meta or {}).get("upcoming_songs") or [])

    req_by = str((current_track or {}).get("requested_by") or "").strip()
    is_radio_show_track = bool((current_track or {}).get("is_radio_show") and (current_track or {}).get("show_id"))
    is_viewer_spin = bool(
        req_by
        and not is_radio_show_track
        and "Studio Drop" not in req_by
        and "Studio Twofer" not in req_by
        and "82.5 FM Show" not in req_by
    )
    show_hud = radio_shows_engine.resolve_show_hud_state(now_ts, snap_meta=snap_meta, current_track=current_track)

    viewer_vq: list[dict] = []
    for vi in voice_queue:
        vi_eta = int(round(float(vi.get("eta_sec") or rem_s)))
        for t in (vi.get("turns") or []):
            if not t.get("is_station_bumper") and not t.get("is_song_intro"):
                tc = dict(t)
                tc["_eta_sec"] = max(1, vi_eta)
                viewer_vq.append(tc)

    vp_turns = list((voice_playing or {}).get("turns") or (current_track or {}).get("voice_reply_turns") or [])
    ack_age = (now_ts - float(jb_ack.get("queued_at") or 0.0)) if jb_ack.get("queued_at") else 9999.0
    ack_active = bool(jb_ack.get("author") and 0.0 <= ack_age <= 32.0)
    v_ack_age = (now_ts - float(voice_ack.get("queued_at") or 0.0)) if voice_ack.get("queued_at") else 9999.0
    v_ack_active = bool(viewer_vq or (voice_ack.get("author") and 0.0 <= v_ack_age <= 18.0))
    curation_active = len(jb_curations) > 0
    idle_rot = int(now_ts // 14) % 4

    jb_sig = tuple((q.get("display_title", ""), q.get("requested_by", ""), q.get("show_track_num", 0)) for q in jb_queue[:3])
    cur_sig = tuple((c.get("author", ""), c.get("text", ""), c.get("kind", "")) for c in jb_curations[:1])
    vq_sig = (viewer_vq[-1].get("author", ""), int(viewer_vq[-1].get("_eta_sec") or 0)) if viewer_vq else ()
    vp_sig = (vp_turns[-1].get("author", ""), vp_turns[-1].get("is_station_bumper", False)) if vp_turns else ()
    up_sig = upcoming_songs[0].get("display_title", "") if upcoming_songs else ""
    sh_sig = (
        (current_track or {}).get("show_id", ""),
        (current_track or {}).get("show_track_num", 0),
        show_hud.get("next_show_id", ""),
        show_hud.get("world_clock_compact", ""),
    )

    lore = resolve_song_lore_panel(current_track or {}, state, now_ts)
    theme = _resolve_hud_neon_theme(current_track, lore, is_bleed=is_bleed)
    pri_rgb = theme["pri_rgb"]
    sec_rgb = theme["sec_rgb"]

    cache_key = (
        "neon_mtv_v5",
        (current_track or {}).get("filename", ""),
        kind,
        is_bleed,
        pri_rgb,
        sec_rgb,
        offset_s,
        dur_s,
        req_by,
        jb_sig,
        cur_sig,
        ack_active,
        jb_ack.get("author", "") if ack_active else "",
        jb_ack.get("display_title", "") if ack_active else "",
        v_ack_active,
        vq_sig,
        vp_sig,
        up_sig,
        sh_sig,
        idle_rot,
    )
    if _MTV_LOWER_CACHE.get("key") == cache_key and _MTV_LOWER_CACHE.get("img") is not None:
        canvas.alpha_composite(_MTV_LOWER_CACHE["img"], (42, 908))  # type: ignore[arg-type]
        return

    pw, ph = 1836, 170
    patch = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(patch)

    artist_s, year_s, label_s = _extract_80s_release_meta(current_track, lore)
    raw_title = str(lore.get("title") or (current_track or {}).get("display_title") or "Night Flight").strip()
    clean_title = raw_title.split(" — ", 1)[-1].strip() if " — " in raw_title else raw_title
    clean_title = re.sub(r"\s*[\(\[]\s*L\.?U\.?N\.?A\.?\s+Revision\s*[\)\]]", "", clean_title, flags=re.I).strip()
    clean_title = re.sub(r"\s*[-–—]\s*L\.?U\.?N\.?A\.?\s+Revision\b", "", clean_title, flags=re.I).strip()

    if not is_vocal_song:
        if kind == "crt_commercial":
            disp_full = str((current_track or {}).get("display_title") or "1980s Television Archive")
            artist_s = "CH-04 TV ARCHIVE"
            rhs = disp_full.split("//", 1)[-1].strip() if "//" in disp_full else disp_full
            clean_title = (
                rhs.title()
                .replace("Tv", "TV")
                .replace("Jdm", "JDM")
                .replace("Vhs", "VHS")
                .replace("Awn", "AWN")
                .replace("Mbm", "MBM")
                .replace("2-Lp", "2-LP")
                .replace("2000Gt", "2000GT")
            )
            ym_tv = re.search(r"\b(198[3-9])\b", disp_full)
            year_s = ym_tv.group(1) if ym_tv else "1988"
            label_s = "NTSC BROADCAST SPOT"
        else:
            artist_s = "82.5 FM STEREO"
            clean_title = (
                "Nova Hart — Live from Studio B"
                if kind == "nova_voice_reply"
                else ("Night Flight Highway Weather" if kind == "fm_weather" else "82.5 FM Night Flight Rock")
            )
            year_s = "1986"
            label_s = "LOS ANGELES"

    # Smoked midnight-glass 1986 MTV cable lower-third ribbon (`x=148..1828, y=24..154`) + neon tube halo
    d.rounded_rectangle(
        [146, 22, pw - 6, 156],
        radius=15,
        outline=theme["halo_pri"],
        width=3,
    )
    d.rounded_rectangle(
        [148, 24, pw - 8, 154],
        radius=14,
        fill=theme["glass_bg"],
        outline=theme["border_pri"],
        width=1,
    )
    # Glowing 1980s neon laser accent stripe along top of lower-third
    d.line([(162, 26), (pw - 22, 26)], fill=(sec_rgb[0], sec_rgb[1], sec_rgb[2], 95), width=4)
    d.line([(164, 25), (pw - 24, 25)], fill=theme["stripe_pri"], width=2)

    # Peeking 45-RPM black vinyl disc (`center=(148, 86), r=63`) + Neon Record Label + `136x136` Picture Sleeve!
    vx, vy, vr = 148, 86, 63
    d.ellipse([vx - vr, vy - vr, vx + vr, vy + vr], fill=(14, 13, 20, 252), outline=(pri_rgb[0], pri_rgb[1], pri_rgb[2], 148), width=2)
    for gr in (52, 42, 32):
        d.ellipse([vx - gr, vy - gr, vx + gr, vy + gr], outline=(58, 52, 74, 155), width=1)
    d.ellipse([vx - 21, vy - 21, vx + 21, vy + 21], fill=(pri_rgb[0], pri_rgb[1], pri_rgb[2], 255), outline=theme["txt_sec"], width=1)
    d.ellipse([vx - 5, vy - 5, vx + 5, vy + 5], fill=(12, 10, 18, 255))

    sleeve = _get_song_sleeve_patch(assets_dir, current_track, lore, size=136)
    patch.alpha_composite(sleeve, (8, 18))
    d.rectangle([7, 17, 8 + 136, 18 + 136], outline=theme["border_pri"], width=2)

    tx0 = 232

    def _has_uni(s: str) -> bool:
        return any(ord(ch) > 0x0370 and ch not in "•—–‘’“”▶✓🎙⚡♪●" for ch in s)

    def _trim_px(s: str, fnt: ImageFont.FreeTypeFont | ImageFont.ImageFont, max_w: float) -> str:
        out = s.strip()
        try:
            if fnt.getlength(out) <= max_w:
                return out
            while len(out) > 6 and fnt.getlength(out + "...") > max_w:
                out = out[:-1].rstrip()
            return out + "..."
        except Exception:
            return out[:68]

    # --- ROW 1 (`y=34`): ARTIST • YEAR / REQUESTED BY + NEON PROGRESS BAR ---
    friendly_label = (
        label_s.replace("82.5 FM SUNSET STRIP", "82.5 FM Sunset Strip")
        .replace("ORION STUDIO B", "82.5 FM Sunset Strip")
        .replace("ORION GEN-4 G.R.A.Y.", "82.5 FM Sunset Strip")
        .replace("ORION AKASAKA", "Tokyo Pressing")
        .replace("WKVD / ORION LP", "12-Inch Rock LP")
        .title()
        .replace("82.5 Fm", "82.5 FM")
        .replace("12-Inch Rock Lp", "12-Inch Rock LP")
        .replace("Ntsc", "NTSC")
    )
    d.text((tx0, 34), artist_s, fill=theme["txt_pri"], font=FONT_MTV_ARTIST, stroke_width=1, stroke_fill=(6, 4, 14, 236))
    try:
        art_w = int(FONT_MTV_ARTIST.getlength(artist_s))
    except Exception:
        art_w = len(artist_s) * 13

    if is_radio_show_track:
        sh_id = str((current_track or {}).get("show_id") or "")
        sh_def = radio_shows_engine.SHOW_DEFINITIONS.get(sh_id) or {}
        sh_title = str(sh_def.get("title") or "82.5 FM SPECIAL")
        sh_k = int((current_track or {}).get("show_track_num") or 1)
        sh_tot = int((current_track or {}).get("show_total_tracks") or 5)
        meta_str = f"•   {sh_title}  (Track {sh_k} of {sh_tot})"
        meta_col = theme["txt_sec"]
    elif is_viewer_spin:
        meta_str = f"•   Spinning for {req_by}"
        meta_col = theme["txt_sec"]
    else:
        meta_str = f"•   {year_s} {friendly_label}"
        meta_col = (224, 218, 242, 232)
    meta_fnt = FONT_HUD_UNI if _has_uni(meta_str) else FONT_MTV_META
    d.text((tx0 + art_w + 14, 35), _trim_px(meta_str, meta_fnt, 920.0), fill=meta_col, font=meta_fnt)

    # Right-aligned glowing neon progress bar + MM:SS
    prog = max(0.0, min(1.0, offset_s / float(dur_s)))
    bar_x0, bar_y0, bar_w, bar_h = pw - 328, 41, 168, 8
    d.rounded_rectangle([bar_x0, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h], radius=4, fill=(24, 20, 38, 232), outline=(pri_rgb[0], pri_rgb[1], pri_rgb[2], 92), width=1)
    fill_w = max(5, int(bar_w * prog))
    d.rounded_rectangle([bar_x0, bar_y0, bar_x0 + fill_w, bar_y0 + bar_h], radius=4, fill=(pri_rgb[0], pri_rgb[1], pri_rgb[2], 252))
    tip_x = bar_x0 + fill_w
    d.ellipse([tip_x - 3, bar_y0 - 1, tip_x + 3, bar_y0 + bar_h + 1], fill=theme["txt_sec"])
    t_str = f"{offset_s // 60:02d}:{offset_s % 60:02d} / {dur_s // 60:02d}:{dur_s % 60:02d}"
    d.text((bar_x0 + bar_w + 14, 35), t_str, fill=(244, 240, 255, 244), font=FONT_MTV_BADGE)

    # --- ROW 2 (`y=62`): LARGE 1986 MTV CABLE SONG TITLE ---
    disp_song = f'"{clean_title}"' if is_vocal_song else clean_title
    title_fnt = FONT_TITLE_UNI if _has_uni(disp_song) else FONT_MTV_TITLE
    fit_song = _trim_px(disp_song, title_fnt, 1540.0)
    d.text((tx0 + 2, 64), fit_song, fill=(6, 4, 14, 224), font=title_fnt)
    d.text((tx0, 62), fit_song, fill=(252, 248, 255, 255), font=title_fnt, stroke_width=1, stroke_fill=(pri_rgb[0] // 4, pri_rgb[1] // 4, pri_rgb[2] // 4, 185))

    # --- ROW 3 (`y=115`): SINGLE CLEAN INTERACTIVE BOOTH / UP-NEXT STRIP ---
    highlight_pill = False
    if curation_active:
        c_it = jb_curations[-1]
        c_auth = str(c_it.get("author") or "@listener")
        is_q = str(c_it.get("kind") or "") == "question"
        live_line = (
            f"STUDIO BOOTH: Hearing {c_auth} in the booth — cueing Nova's microphone for the next break!"
            if is_q
            else f"REQUEST LINE: Pulling a reel off the shelf for {c_auth} right now..."
        )
        highlight_pill = True
    elif v_ack_active:
        if viewer_vq:
            vt = viewer_vq[-1]
            va = str(vt.get("author") or "@listener")
            mm_e, ss_e = divmod(max(1, int(vt.get("_eta_sec") or rem_s)), 60)
            live_line = f"STUDIO BOOTH: Got your note, {va} — Nova answers aloud right after this song ({mm_e}:{ss_e:02d})"
        else:
            va = str(voice_ack.get("author") or "@listener")
            live_line = f"STUDIO BOOTH: Got your note, {va} — Nova's mic is armed for the next break!"
        highlight_pill = True
    elif ack_active:
        a_auth = str(jb_ack.get("author") or "@listener")
        a_song = str(jb_ack.get("display_title") or "Nova Hart")
        a_pos = int(jb_ack.get("queue_pos") or max(1, len(jb_queue)))
        live_line = f"REQUEST LOCKED FOR {a_auth}: \"{a_song}\" is #{a_pos} on deck — Nova introduces it next!"
        highlight_pill = True
    elif vp_turns and not vp_turns[-1].get("is_station_bumper"):
        v_caller = str(vp_turns[-1].get("author") or "@listener")
        live_line = f"ON AIR NOW: Nova is answering {v_caller} live from Studio Booth B on 82.5 FM"
        highlight_pill = True
    elif is_bleed:
        ed = (snap_meta or {}).get("teletext_edition") or {}
        live_line = f"67 kHz SUBCARRIER DRIFT: {ed.get('p888_subcarrier_leak', 'Sublevel B2 auxiliary carrier active -> stardust-archive.net')}"
    elif jb_queue:
        if jb_queue[0].get("is_radio_show") and jb_queue[0].get("show_id") in radio_shows_engine.SHOW_DEFINITIONS:
            sh_t = radio_shows_engine.SHOW_DEFINITIONS[str(jb_queue[0]["show_id"])]["title"]
            show_parts = [
                f"Track {q.get('show_track_num', '?')}: \"{q.get('display_title', '')}\""
                for q in jb_queue[:3]
                if q.get("is_radio_show")
            ]
            viewer_after = [q for q in jb_queue if not q.get("is_radio_show")]
            tail_s = f"   •   Viewer Requests After Show ({len(viewer_after)})" if viewer_after else ""
            live_line = f"Coming Up on {sh_t}:  " + "   •   ".join(show_parts) + tail_s
        else:
            q_parts = [f"#{i + 1} \"{q.get('display_title', '')}\" ({q.get('requested_by', '')})" for i, q in enumerate(jb_queue[:3])]
            live_line = "Up Next on Request Deck:  " + "   •   ".join(q_parts)
    else:
        up0 = str(upcoming_songs[0].get("display_title") or "Midnight Animal") if upcoming_songs else "Midnight Animal"
        if idle_rot == 0:
            live_line = f"Up Next: \"{up0}\"   •   Want a song or late-night dedication? Just say \"Nova\" in chat"
        elif idle_rot == 1:
            live_line = f"Up Next: \"{up0}\"   •   Ask Nova about any song, mood, or tell her what city you're tuning in from"
        elif idle_rot == 2:
            live_line = f"Next Show: {show_hud['next_show_title']}   •   {show_hud['world_clock_24h']}"
        else:
            ed = (snap_meta or {}).get("teletext_edition") or {}
            live_line = f"Up Next: \"{up0}\"   •   {ed.get('local_weather_ticker', 'Coast Hwy 64°F Clear • Commercial-Free Night Flight Sweeps')}"

    live_line = _sanitize_stream_text(live_line)
    sub_fnt = FONT_HUD_UNI if _has_uni(live_line) else FONT_MTV_SUB
    if highlight_pill:
        d.rounded_rectangle(
            [tx0 - 8, 113, pw - 24, 145],
            radius=7,
            fill=(pri_rgb[0] // 5 + 8, pri_rgb[1] // 5 + 6, pri_rgb[2] // 5 + 16, 228),
            outline=theme["border_pri"],
            width=1,
        )
        d.text((tx0 + 4, 117), _trim_px(live_line, sub_fnt, 1550.0), fill=(252, 244, 255, 255), font=sub_fnt)
    else:
        l_col = theme["txt_sec"] if is_bleed else (228, 222, 246, 236)
        d.text((tx0, 117), _trim_px(live_line, sub_fnt, 1565.0), fill=l_col, font=sub_fnt)

    _MTV_LOWER_CACHE["key"] = cache_key
    _MTV_LOWER_CACHE["img"] = patch
    canvas.alpha_composite(patch, (42, 908))


def render_full_arg_overlay_png(
    out_path: Path,
    state: dict,
    assets_dir: Path,
    now_ts: float,
    snap_meta: dict | None = None,
) -> bytes:
    """
    Renders the uncluttered 94% Cozy 1986 Retro Nostalgia / 6% Subtle Uncanny Flicker `1920x1080` RGBA overlay:
      1. Uncovered Warm 1986 Tungsten Studio Grade (exposing the physical analog VU meters, rack LEDs,
         gooseneck desk lamp dust motes, and cassette deck on the wooden desk!)
      2. Warm Honey-Amber Physical CRT Screen (`688x488` at `x=616, y=204`) with sing-along song lyrics
      3. Compact Top-Left Illuminated `[ ● ON AIR  82.5 FM STEREO ]` Studio Sign
      4. Classic 1986 MTV / Cable-TV Vinyl-Sleeve Lower-Third (`y=876..1046`) with `< 1.5s` live booth response!
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
        snap_meta = dict(snap_meta)
        relay = snap_meta.get("relay", REGIONAL_RELAYS[0])

    current_track = snap_meta.get("current_track") or {
        "filename": "radio_b_midnight_protocol_final_1.mp3",
        "stem": "radio_b_midnight_protocol_final_1",
        "kind": "vocal_song",
        "display_title": state.get("crt_sub", "Midnight Protocol"),
    }

    is_bleed = (
        bool(snap_meta.get("is_arg_bleed"))
        if "is_arg_bleed" in snap_meta
        else _is_subcarrier_bleed_active(now_ts, state, current_track)
    )
    snap_meta["is_arg_bleed"] = is_bleed
    snap_meta.setdefault("teletext_edition", trojan_horse_radio_engine.load_teletext_daily_edition(assets_dir.parent))
    snap_meta.setdefault("dx_rollcall", trojan_horse_radio_engine.load_fm_dx_rollcall(assets_dir.parent))

    canvas = _get_warm_1986_studio_grade_layer().copy()

    # 1. Re-color the physical CRT monitor's recessed inner bevel reflection + composite CRT Screen Content at 1080p
    cur_kind = str((current_track or {}).get("kind") or "vocal_song")
    if cur_kind != "crt_commercial":
        bevel_lore = resolve_song_lore_panel(current_track or {}, state, now_ts)
        bevel_theme = _resolve_hud_neon_theme(current_track, bevel_lore, is_bleed=is_bleed)
        _render_crt_bevel_neon_spill(canvas, bevel_theme["pri_rgb"])

    crt_patch = render_crt_window_patch(
        state, relay, assets_dir, now_ts, current_track=current_track, snap_meta=snap_meta
    )
    canvas.alpha_composite(crt_patch, (CRT_PX_X, CRT_PX_Y))

    # 2. Animate Physical Analog Rack LEDs + Top-Left `● ON AIR` Sign + Classic 1986 MTV Vinyl Lower-Third
    is_warn = is_bleed and (
        (state.get("hud_mode") or state.get("mode")) == "ANOMALY_WARN" or int(state.get("target_sector", 7)) >= 8
    )
    render_room_hardware_animations(canvas, state, now_ts, is_warn)
    render_retro_80s_on_air_sign(canvas, now_ts, is_bleed, snap_meta=snap_meta, current_track=current_track, state=state)
    render_retro_80s_request_cta_badge(canvas, now_ts, is_bleed, snap_meta=snap_meta, current_track=current_track, state=state)
    render_retro_1986_mtv_lower_third(canvas, assets_dir, current_track, state, now_ts, snap_meta=snap_meta)

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


CANONICAL_SONG_TITLES: dict[str, str] = {'radio_01_gasoline_heart_1985_tokyo_master': 'Gasoline Heart (1985 Tokyo)',
 'radio_02_between_the_circuits': 'Between The Circuits',
 'radio_02_brighter_than_the_sun_1987_tokyo_master': 'Brighter Than The Sun (1987 Tokyo)',
 'radio_04_midnight_animal_1986_tokyo_master': 'Midnight Animal (1986 Tokyo)',
 'radio_midnight_animal': 'Midnight Animal',
 'radio_gasoline_heart': 'Gasoline Heart',
 'radio_gasoline_heart_es': 'Gasoline Heart (Español)',
 'radio_salvese_quien_pueda': 'Sálvese Quien Pueda',
 'radio_fuoco_dentro': 'Fuoco Dentro',
 'radio_we_are_the_thunder': 'We Are The Thunder',
 'radio_we_are_the_thunder_live_1986': 'We Are The Thunder (Live 1986)',
 'radio_two_voices': 'Two Voices',
 'radio_abandoned_shell': 'Abandoned Shell',
 'radio_abandoned_shell_es': 'Abandoned Shell (Español)',
 'radio_asset_loss_kr': 'Asset Loss (Korean)',
 'radio_crossing_this_line_nova_hart': 'Crossing This Line (Nova Hart)',
 'radio_memory_hatch_1989_aor_mix': 'Memory Hatch (1989 AOR Mix)',
 'radio_the_broadcast_begins': 'The Broadcast Begins',
 'radio_04_synthetic_dawn': 'Synthetic Dawn',
 'radio_05_first_light_on_my_face': 'First Light On My Face',
 'radio_05_ghost_transit_1985_tokyo_master': 'Ghost Transit (1985 Tokyo)',
 'radio_ghost_transit_hard_rock': 'Ghost Transit (Hard Rock Version)',
 'radio_06_the_air_feels_wrong': 'The Air Feels Wrong',
 'radio_room_full_of_color': 'Room Full of Color',
 'radio_08_faultline_path': 'Faultline Path',
 'radio_13_through_the_threshold': 'Through The Threshold',
 'radio_5_the_way_back_v3': 'The Way Back',
 'radio_a_story_that_wont_fade': "Heartstrike — A Story That Won't Fade",
 'radio_again_from_zero': 'Again from Zero',
 'radio_all_in_this_is_the_moment': 'Heartstrike — All In (This is the Moment)',
 'radio_artificial_heart_bonus_track': 'Artificial Heart',
 'radio_asset_loss_the_dead_hand': 'Asset Loss (The Dead Hand)',
 'radio_audio_file_0147_1': 'Audio File 0147',
 'radio_b_midnight_protocol_final_1': 'Midnight Protocol',
 'radio_b_only_we_remain_marcus_and_nova_duet_1': 'Only We Remain (Marcus & Nova Duet)',
 'radio_before_you_turn_away': 'Before You Turn Away',
 'radio_behind_the_glass': 'Behind The Glass',
 'radio_blood_on_the_stage': 'Blood On The Stage',
 'radio_blueprint_for_ruin_old': 'Blueprint For Ruin',
 'radio_born_for_the_flame': 'Heartstrike — Born for the Flame',
 'radio_borrowed_fire': 'Borrowed Fire',
 'radio_bound_no_more': 'Heartstrike — Bound No More',
 'radio_burn_the_chorus': 'Burn The Chorus',
 'radio_burning_bright': 'Heartstrike — Burning Bright',
 'radio_by_order_of_harmony': 'By Order Of Harmony',
 'radio_cage_in_your_hand': 'Cage In Your Hand',
 'radio_call_of_the_abyss': 'Heartstrike — Call of the Abyss',
 'radio_carry_the_sky': 'Carry the Sky',
 'radio_chrome_river': 'Chrome River',
 'radio_city_that_can’t_ignore_me': "City That Can't Ignore Me",
 'radio_city_that_doesn_t_need_me': "City That Doesn't Need Me",
 'radio_cold_reaction': 'Cold Reaction',
 'radio_companion_on_fire': 'Companion on Fire',
 'radio_concrete_fever': 'Concrete Fever',
 'radio_corridor_dreams_movement_1': 'Corridor Dreams (Movement 1)',
 'radio_corridor_dreams_movement_2': 'Corridor Dreams (Movement 2)',
 'radio_corridor_dreams_movement_3': 'Corridor Dreams (Movement 3)',
 'radio_crimson_horizon': 'Crimson Horizon',
 'radio_crossing_this_line': 'Heartstrike — Crossing This Line',
 'radio_crossing_this_line_remastered': 'Heartstrike — Crossing This Line (Remastered Mix)',
 'radio_crystal_sleep': 'Crystal Sleep',
 'radio_cut_the_cue': 'Cut the Cue',
 'radio_days_gone_by': 'Heartstrike — Days Gone By',
 'radio_dial_tone_heart': 'Dial-Tone Heart',
 'radio_digital_heartbeat': 'Digital Heartbeat',
 'radio_echoes_of_thunder': 'Heartstrike — Echoes of Thunder',
 'radio_echoes_of_tomorrow': 'Heartstrike — Echoes of Tomorrow',
 'radio_echoes_of_tomorrow_80s_hard_rock_remix': 'Heartstrike — Echoes of Tomorrow (80s Hard Rock '
                                                 'Remix)',
 'radio_edit_the_script': 'Heartstrike — Edit the Script',
 'radio_electric_storm_thunder_machine': 'Thunder Machine — Electric Storm',
 'radio_erase_the_frame': 'Erase The Frame',
 'radio_every_window_is_a_promise_crystal_promise': 'Every Window Is A Promise',
 'radio_everywhere_at_once': 'Everywhere at Once',
 'radio_final_crescendo': 'Heartstrike — Final Crescendo',
 'radio_fire_in_the_wires': 'Fire In The Wires',
 'radio_fire_in_your_heart': 'Heartstrike — Fire in Your Heart',
 'radio_fissures_in_time': 'Heartstrike — Fissures in Time',
 'radio_for_steve_and_tj': 'Heartstrike — For Steve and TJ',
 'radio_forever_unbroken': 'Forever Unbroken',
 'radio_fractured_harmony': 'Heartstrike — Fractured Harmony',
 'radio_frame_by_frame': 'Heartstrike — Frame by Frame',
 'radio_frame_your_shot': 'Heartstrike — Frame Your Shot',
 'radio_ghost_on_the_radio': 'Ghost On The Radio',
 'radio_give_me_the_other_half': 'Give Me The Other Half',
 'radio_half_a_paycheck_whole_heart': 'Half a Paycheck, Whole Heart',
 'radio_hard_reset_soft_touch': 'Hard Reset, Soft Touch',
 'radio_heart_and_mind_aligned': 'Heartstrike — Heart and Mind Aligned',
 'radio_heartbeat_of_the_crowd': 'Heartbeat of the Crowd',
 'radio_hold_the_horizon': 'Hold the Horizon',
 'radio_hologram_city_queen': 'Hologram City Queen',
 'radio_hologram_city_queen_remastered': 'Hologram City Queen',
 'radio_homeroom_riptide': 'Homeroom Riptide',
 'radio_hunter_at_the_gate': 'Hunter At The Gate',
 'radio_i_like_the_middle_of_the_road': '(I Like) The Middle of the Road',
 'radio_it_has_no_face_old': 'It Has No Face',
 'radio_lightning_strikes_twice': 'Heartstrike — Lightning Strikes Twice',
 'radio_lost_in_london_velvet_tide': 'Velvet Tide — Lost in London',
 'radio_marina_half_the_city_knows_your_name': 'Marina (Half The City Knows Your Name)',
 'radio_midnight_venom_vyper_strike': 'Vyper Strike — Midnight Venom',
 'radio_more_than_i_can_be': 'Heartstrike — More Than I Can Be',
 'radio_no_way_out': 'Heartstrike — No Way Out',
 'radio_on_the_edge_of_it_all': 'Heartstrike — On the Edge of It All',
 'radio_one_voice_left': 'One Voice Left',
 'radio_open_the_gates': 'Open the Gates',
 'radio_pages_of_me': 'Pages of Me',
 'radio_paper_crowd': 'Paper Crowd',
 'radio_paper_windows': 'Paper Windows',
 'radio_play_it_back': 'Play It Back',
 'radio_playback_forever_master': 'Playback Forever',
 'radio_programmed_for_love': 'Programmed For Love (1983 Recall Demo)',
 'radio_queen_of_the_wide_stage': 'Queen of the Wide Stage',
 'radio_raw_voltage': 'Raw Voltage',
 'radio_redline_rendezvous': 'Redline Rendezvous',
 'radio_remember_my_name': 'Remember My Name',
 'radio_riot_in_my_heart': 'Riot in my Heart',
 'radio_rise_tonight': 'Rise Tonight',
 'radio_roll_the_film': 'Heartstrike — Roll the Film',
 'radio_run_the_perfect_line': 'Run the Perfect Line',
 'radio_satellite_for_two': 'Satellite for Two',
 'radio_say_you_ll_stay': "Say You'll Stay",
 'radio_shes_hardwired': "She's Hardwired",
 'radio_shout_for_the_real': 'Shout for the Real',
 'radio_silent_sirens': 'Heartstrike — Silent Sirens',
 'radio_spotless_beam': 'Spotless Beam',
 'radio_stage_fever_remastered': 'Stage Fever',
 'radio_stand_like_fire': 'Stand Like Fire',
 'radio_stand_unbroken': 'Stand Unbroken',
 'radio_steel_and_shadows': 'Heartstrike — Steel and Shadows',
 'radio_steel_heartbeat': 'Steel Heartbeat',
 'radio_sugar_burn': 'Sugar Burn',
 'radio_synth_dreams_neon_comets': 'Neon Comets — Synth Dreams',
 'radio_synthetic_kiss': 'Synthetic Kiss',
 'radio_t_minus_forever': 'T Minus Forever',
 'radio_the_last_secret': 'The Last Secret',
 'radio_the_man_in_the_booth_marcus_song': 'The Man In The Booth (Marcus)',
 'radio_the_man_in_the_booth_refrain': 'The Man In The Booth (Refrain)',
 'radio_the_other_flame': 'The Other Flame',
 'radio_the_seventh_sons_seventh_daughter': "The Seventh Son's Seventh Daughter",
 'radio_the_stars_in_your_hands': 'The Stars In Your Hands',
 'radio_through_the_glass_darkly': 'Heartstrike — Through the Glass Darkly',
 'radio_to_the_end_of_time': 'Heartstrike — To the End of Time',
 'radio_to_the_ends_of_forever': 'Heartstrike — To the Ends of Forever',
 'radio_to_the_fans': 'Heartstrike — To the Fans',
 'radio_together_s_the_way': "Together's The Way",
 'radio_under_the_perfect_sound': 'Under the Perfect Sound',
 'radio_unstable_pattern_old': 'Unstable Pattern',
 'radio_warm_frequency': 'Warm Frequency',
 'radio_warm_hands_one_map': 'Warm Hands, One Map',
 'radio_we_are_the_thunder_live': 'We Are The Thunder (Live)',
 'radio_we_belong_here': 'We Belong Here',
 'radio_when_innocence_was_lost': 'Heartstrike — When Innocence Was Lost',
 'radio_wild_desire': 'Wild Desire',
 'radio_all_the_ways_out_luna_revision': 'N0VA H4RT — All The Ways Out (L.U.N.A. Revision)',
 'radio_amber_horizon_luna_revision': 'N0VA H4RT — Amber Horizon (L.U.N.A. Revision)',
 'radio_between_the_circuits_luna_revision': 'N0VA H4RT — Between the Circuits (L.U.N.A. Revision)',
 'radio_bold_reaction_luna_revision': 'N0VA H4RT — Bold Reaction (L.U.N.A. Revision)',
 'radio_chainlink_kiss_luna_revision': 'N0VA H4RT — Chainlink Kiss (L.U.N.A. Revision)',
 'radio_chrome_desire_luna_revision': 'N0VA H4RT — Chrome Desire (L.U.N.A. Revision)',
 'radio_chrome_river_luna_revision': 'N0VA H4RT — Chrome River (L.U.N.A. Revision)',
 'radio_console_thunder_luna_revision': 'N0VA H4RT — Console Thunder (L.U.N.A. Revision)',
 'radio_diamond_in_the_quiet_luna_revision': 'N0VA H4RT — Diamond in the Quiet (L.U.N.A. Revision)',
 'radio_erase_the_frame_luna_revision': 'N0VA H4RT — Erase the Frame (L.U.N.A. Revision)',
 'radio_faultline_path_luna_revision': 'N0VA H4RT — Faultline Path (L.U.N.A. Revision)',
 'radio_gasoline_heart_luna_revision': 'N0VA H4RT — Gasoline Heart (L.U.N.A. Revision)',
 'radio_ghost_on_the_radio_luna_revision': 'N0VA H4RT — Ghost on the Radio (L.U.N.A. Revision)',
 'radio_ghost_transit_luna_revision': 'N0VA H4RT — Ghost Transit (L.U.N.A. Revision)',
 'radio_hold_the_line_within_luna_revision': 'N0VA H4RT — Hold the Line Within (L.U.N.A. Revision)',
 'radio_lost_signal_trace_luna_revision': 'N0VA H4RT — Lost Signal Trace (L.U.N.A. Revision)',
 'radio_night_runner_luna_revision': 'N0VA H4RT — Night Runner (L.U.N.A. Revision)',
 'radio_paper_crowd_luna_revision': 'N0VA H4RT — Paper Crowd (L.U.N.A. Revision)',
 'radio_remember_my_name_luna_revision': 'N0VA H4RT — Remember My Name (L.U.N.A. Revision)',
 'radio_stay_on_your_side_luna_revision': 'N0VA H4RT — Stay on Your Side (L.U.N.A. Revision)',
 'radio_steel_and_shine_luna_revision': 'N0VA H4RT — Steel and Shine (L.U.N.A. Revision)',
 'radio_synthetic_dawn_luna_revision': 'N0VA H4RT — Synthetic Dawn (L.U.N.A. Revision)',
 'radio_the_override_luna_revision': 'N0VA H4RT — The Override (L.U.N.A. Revision)',
 'radio_the_summer_of_85_luna_revision': "N0VA H4RT — The Summer of '85 (L.U.N.A. Revision)",
 'radio_unopened_door_luna_revision': 'N0VA H4RT — Unopened Door (L.U.N.A. Revision)',
 'radio_warm_frequency_luna_revision': 'N0VA H4RT — Warm Frequency (L.U.N.A. Revision)',
 'radio_we_are_the_thunder_luna_revision': 'N0VA H4RT — We Are the Thunder (L.U.N.A. Revision)',
 'radio_we_stand_here_luna_revision': 'N0VA H4RT — We Stand Here (L.U.N.A. Revision)',
 'radio_weekend_festival_luna_revision': 'N0VA H4RT — Weekend Festival (L.U.N.A. Revision)'}


_CRT_COMMERCIAL_TITLE_CACHE: dict[str, Any] = {"mtime": 0.0, "map": {}}


def _lookup_crt_commercial_title(stem: str) -> str:
    manifest_p = Path(__file__).resolve().parent / "assets_arg" / "crt_commercials" / "crt_commercials_manifest.json"
    try:
        if manifest_p.exists():
            mt = manifest_p.stat().st_mtime
            if mt != _CRT_COMMERCIAL_TITLE_CACHE.get("mtime"):
                data = json.loads(manifest_p.read_text(encoding="utf-8"))
                _CRT_COMMERCIAL_TITLE_CACHE["map"] = {
                    str(s.get("stem")): str(s.get("display_title"))
                    for s in data.get("spots", [])
                    if s.get("stem") and s.get("display_title")
                }
                _CRT_COMMERCIAL_TITLE_CACHE["mtime"] = mt
            mapped = _CRT_COMMERCIAL_TITLE_CACHE["map"].get(stem)
            if mapped:
                return mapped
    except Exception:
        pass
    slug = re.sub(r"^commercial_tv_(?:\d+_)?", "", stem).replace("_", " ").upper()
    return f"1980S TV COMMERCIAL // {slug}"


def classify_track(filepath: str) -> dict:
    p = Path(filepath)
    stem = p.stem
    parent = p.parent.name
    if stem.startswith("dj_intro_"):
        jb_orig = p.parent.parent / "jukebox_slot_backups" / f"{p.name}.orig"
        if jb_orig.exists() and p.exists() and p.stat().st_size < 16384:
            kind = "fm_splice"
            clean = "82.5 FM TAPE SPLICE"
        else:
            kind = "dj_intro"
            song_stem = stem[len("dj_intro_") :]
            if song_stem in CANONICAL_SONG_TITLES:
                song_clean = CANONICAL_SONG_TITLES[song_stem]
            else:
                s = re.sub(r"^radio_(?:\d+_)?", "", song_stem)
                s = re.sub(r"_(?:1|old|remastered|master|final_1|v3)$", "", s)
                song_clean = s.replace("_", " ").title().replace("’S", "'s").replace("’T", "'t")
            clean = f"82.5 FM STUDIO BOOTH // {song_clean}"
    elif "radio_master_songs" in filepath or stem.startswith(("radio_", "dj_tail_")):
        kind = "vocal_song"
        if stem.startswith("dj_tail_"):
            stem = stem[len("dj_tail_") :]
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
    elif stem.startswith("trailer_"):
        kind = "english_bulletin"
        clean = f"1980S MOVIE TRAILER // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("commercial_tv_"):
        kind = "crt_commercial"
        clean = _lookup_crt_commercial_title(stem)
    elif stem.startswith("commercial_"):
        kind = "english_bulletin"
        clean = f"1980S COMMERCIAL SPOT // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("psa_"):
        kind = "english_bulletin"
        clean = f"BUREAU OF HARMONY PSA // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("dj_callin_"):
        kind = "english_bulletin"
        clean = f"82.5 FM CALLER LINE // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("request_line_"):
        kind = "english_bulletin"
        clean = f"82.5 FM REQUEST LINE // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("pirate_override_"):
        kind = "english_bulletin"
        clean = f"PIRATE OVERRIDE // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("world_"):
        kind = "english_bulletin"
        clean = f"1980S WORLD ARCHIVE // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("heartstrike_"):
        kind = "english_bulletin"
        clean = f"HEARTSTRIKE WKVD BLEED // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("blaze_"):
        kind = "english_bulletin"
        clean = f"80S FM WITH RICK BLAZE // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("wlf_"):
        kind = "english_bulletin"
        clean = f"WHITE LINES & FEEDBACK // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("humanist_"):
        kind = "english_bulletin"
        clean = f"HUMANIST RESISTANCE BREAK-IN // {stem.split('_', 2)[-1].replace('_', ' ').upper()}"
    elif stem.startswith("fm_splice_"):
        kind = "fm_splice"
        clean = "82.5 FM TAPE SPLICE"
    elif stem.startswith("fm_sweeper_"):
        kind = "fm_sweeper"
        clean = "82.5 FM STEREO // STATION ID"
    elif stem.startswith(("fm_weather_", "fm_rsi_weather_")):
        kind = "fm_weather"
        clean = "82.5 FM // NIGHT FLIGHT WEATHER"
    elif stem.startswith(("fm_spot86_", "fm_rsi_spot_")):
        kind = "fm_spot86"
        clean = "82.5 FM // LATE NIGHT STUDIO SPOT"
    elif stem.startswith("fm_drift_"):
        kind = "fm_drift"
        clean = "82.5 FM // 02:02 CARRIER DRIFT"
    else:
        kind = "arg_intercept"
        clean = f"DEEP SHORTWAVE INTERCEPT // {stem.upper()}"
    return {"filename": p.name, "stem": stem, "category": parent, "kind": kind, "display_title": clean}


def _get_live_ffmpeg_open_mp3(force_poll: bool = False) -> str | None:
    """Queries Nova Hart's active FFmpeg concat process via `lsof` (strictly scoped to `retro_arg_engine`)."""
    import subprocess
    main_mod = sys.modules.get("__main__")
    now_m = time.monotonic()
    if main_mod is not None:
        stale_mp3 = getattr(main_mod, "_stardust_cached_lsof_mp3", None) or getattr(main_mod, "_stardust_live_open_mp3", None)
        if stale_mp3 and ("country_cate" in str(stale_mp3) or "retro_arg_engine" not in str(stale_mp3)):
            setattr(main_mod, "_stardust_cached_lsof_mp3", None)
            setattr(main_mod, "_stardust_ffmpeg_pid", None)
            setattr(main_mod, "_stardust_live_open_mp3", None)
    if not force_poll and main_mod is not None:
        cached_mp3 = getattr(main_mod, "_stardust_cached_lsof_mp3", None)
        cached_mono = getattr(main_mod, "_stardust_cached_lsof_mono", 0.0)
        if cached_mp3 and "retro_arg_engine" in str(cached_mp3) and (now_m - cached_mono) < 1.6:
            return cached_mp3
    pid = getattr(main_mod, "_stardust_ffmpeg_pid", None) if main_mod else None
    for _ in range(2):
        if not pid:
            try:
                res = subprocess.run(
                    ["pgrep", "-f", "ffmpeg.*retro_arg_engine.*playlist\\.txt"],
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
                        if "retro_arg_engine" not in found_mp3 or "country_cate" in found_mp3:
                            continue
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

    jb_ctrl = None
    slot_override_map: dict[str, dict] = {}
    jb_cum_delta = 0.0
    try:
        nova_live_jukebox = _import_fresh_jukebox()
        jb_ctrl = nova_live_jukebox.ensure_controller(repo_root, CANONICAL_SONG_TITLES)
        with jb_ctrl.lock:
            jb_cum_delta = float(jb_ctrl.queue_state.get("cumulative_duration_delta_sec", 0.0))
            for it in (jb_ctrl.queue_state.get("items", []) + jb_ctrl.queue_state.get("voice_items", [])):
                if it.get("status") in ("QUEUED", "PLAYING") and it.get("slot_path"):
                    slot_override_map[os.path.abspath(str(it["slot_path"]))] = dict(it)
    except Exception:
        jb_ctrl = None

    def _eff_dur(tpath: str | None) -> float:
        if not tpath:
            return 180.0
        ov_item = slot_override_map.get(os.path.abspath(tpath))
        if ov_item and ov_item.get("duration_sec"):
            return float(ov_item["duration_sec"])
        return get_exact_track_duration(tpath, repo_root)

    if is_live and elapsed_sec > 0 and tracks:
        main_mod = sys.modules.get("__main__")
        sync_ver = getattr(main_mod, "_stardust_sync_ver", None) if main_mod else None
        prev_open = getattr(main_mod, "_stardust_live_open_mp3", None) if main_mod else None
        track_start_ts = getattr(main_mod, "_stardust_live_track_start_ts", None) if main_mod else None
        tracked_idx = getattr(main_mod, "_stardust_live_playhead_idx", None) if main_mod else None
        prev_dur = _eff_dur(prev_open) if prev_open else 180.0
        near_boundary = (track_start_ts is None) or ((now - track_start_ts) >= (prev_dur - 6.0))
        live_open_mp3 = _get_live_ffmpeg_open_mp3(force_poll=near_boundary)
        cur_ff_pid = str(getattr(main_mod, "_stardust_ffmpeg_pid", "") or "") if main_mod else ""

        # Reconcile `cumulative_duration_delta_sec` per FFmpeg session PID so multi-day drift can NEVER accumulate across restarts!
        if jb_ctrl is not None and cur_ff_pid:
            try:
                with jb_ctrl.lock:
                    saved_ff_pid = str(jb_ctrl.queue_state.get("ffmpeg_session_pid") or "")
                    if saved_ff_pid != cur_ff_pid:
                        session_start_ts = now - elapsed_sec - 5.0
                        recomputed_delta = 0.0
                        for hit in jb_ctrl.queue_state.get("history", []):
                            if float(hit.get("finished_at") or 0.0) >= session_start_ts:
                                recomputed_delta += float(hit.get("duration_sec", 180.0)) - float(hit.get("orig_duration_sec", 180.0))
                        for vhit in jb_ctrl.queue_state.get("voice_history", []):
                            if vhit.get("kind") != "live_talkback" and float(vhit.get("finished_at") or 0.0) >= session_start_ts:
                                recomputed_delta += float(vhit.get("duration_sec", 18.0)) - float(vhit.get("orig_duration_sec", 18.0))
                        jb_cum_delta = round(recomputed_delta, 2)
                        jb_ctrl.queue_state["cumulative_duration_delta_sec"] = jb_cum_delta
                        jb_ctrl.queue_state["ffmpeg_session_pid"] = cur_ff_pid
                        jb_ctrl._save_queue_state()
            except Exception:
                pass

        # Compute cumulative playlist offset from `elapsed_sec` (adjusted by completed jukebox swaps in THIS session)
        total_pl_dur = sum(_eff_dur(tp) for tp in tracks) or 1.0
        ref_elapsed_sec = max(0.0, elapsed_sec - jb_cum_delta) % total_pl_dur
        accum = 0.0
        pl_idx = 0
        pl_offset = 0.0
        for idx, tpath in enumerate(tracks):
            dur = _eff_dur(tpath)
            if accum + dur > ref_elapsed_sec:
                pl_idx = idx
                pl_offset = max(0.0, ref_elapsed_sec - accum)
                break
            accum += dur

        if live_open_mp3:
            active_track_path = live_open_mp3
            track_dur_sec = _eff_dur(live_open_mp3)
            open_bname = os.path.basename(live_open_mp3)
            n_tr = len(tracks)

            def _circ_dist(a: int, b: int) -> int:
                d = (a - b) % n_tr
                return min(d, n_tr - d)

            drift_too_large = (tracked_idx is not None and _circ_dist(int(tracked_idx), pl_idx) > 16)

            if prev_open != live_open_mp3 or track_start_ts is None or sync_ver != "v5.7" or drift_too_large:
                found_idx = None
                if tracked_idx is not None and not drift_too_large:
                    for step in (0, 1, 2, -1):
                        cand_idx = (int(tracked_idx) + step) % n_tr
                        if os.path.basename(tracks[cand_idx]) == open_bname:
                            found_idx = cand_idx
                            break
                if found_idx is None:
                    # Symmetric outward search around FFmpeg's muxer clock `pl_idx` so duplicate filenames never jump 1,000+ slots!
                    if os.path.basename(tracks[pl_idx]) == open_bname:
                        found_idx = pl_idx
                    else:
                        for rad in range(1, (n_tr // 2) + 2):
                            f_idx = (pl_idx + rad) % n_tr
                            if os.path.basename(tracks[f_idx]) == open_bname:
                                found_idx = f_idx
                                break
                            b_idx = (pl_idx - rad) % n_tr
                            if os.path.basename(tracks[b_idx]) == open_bname:
                                found_idx = b_idx
                                break
                playhead_index = found_idx if found_idx is not None else pl_idx

                if prev_open is not None and prev_open != live_open_mp3 and sync_ver == "v5.7" and track_start_ts is not None and not drift_too_large:
                    # Hardware transition just detected by lsof
                    expected_start = track_start_ts + prev_dur
                    track_start_ts = expected_start if abs(now - expected_start) <= 3.0 else now
                elif playhead_index == pl_idx:
                    # Exact cumulative playlist anchor from FFmpeg muxer clock
                    track_start_ts = now - pl_offset
                else:
                    # Compute cumulative start of `playhead_index` in `tracks`
                    cand_accum = sum(_eff_dur(tracks[i]) for i in range(playhead_index))
                    cand_off = max(0.0, min(track_dur_sec - 1.0, ref_elapsed_sec - cand_accum))
                    track_start_ts = now - cand_off

                if main_mod is not None:
                    setattr(main_mod, "_stardust_sync_ver", "v5.7")
                    setattr(main_mod, "_stardust_live_open_mp3", live_open_mp3)
                    setattr(main_mod, "_stardust_live_track_start_ts", track_start_ts)
                    setattr(main_mod, "_stardust_live_playhead_idx", playhead_index)

                # Persist exact live playhead bookmark + rolling 90-song history so ANY stream restart
                # advances cleanly and NEVER repeats recently played songs!
                try:
                    nb_dir = repo_root / "youtube" / "livestream" / "nova_brain"
                    nb_dir.mkdir(parents=True, exist_ok=True)
                    bm_tmp = nb_dir / "live_playhead_bookmark.json.tmp"
                    bm_tmp.write_text(
                        json.dumps(
                            {
                                "open_mp3": str(live_open_mp3),
                                "open_bname": open_bname,
                                "playhead_index": int(playhead_index),
                                "ts": float(now),
                            }
                        ),
                        encoding="utf-8",
                    )
                    os.replace(bm_tmp, nb_dir / "live_playhead_bookmark.json")
                    if "radio_master_songs" in str(live_open_mp3):
                        rp_path = nb_dir / "recent_played_songs.json"
                        recent_list: list[str] = []
                        if rp_path.exists():
                            recent_list = list(json.loads(rp_path.read_text(encoding="utf-8")) or [])
                        if not recent_list or recent_list[-1] != open_bname:
                            recent_list = [x for x in recent_list if x != open_bname] + [open_bname]
                            rp_tmp = nb_dir / "recent_played_songs.json.tmp"
                            rp_tmp.write_text(json.dumps(recent_list[-90:]), encoding="utf-8")
                            os.replace(rp_tmp, rp_path)
                except Exception:
                    pass
            else:
                playhead_index = tracked_idx if tracked_idx is not None else pl_idx

            # Capture exact hardware/audio playhead BEFORE adding +4.0s visual `image2pipe` lead!
            audio_playhead_index = playhead_index
            audio_track_remaining_sec = max(0.0, track_dur_sec - max(0.0, now - track_start_ts))

            # Add +4.0s visual pipeline lead (`VISUAL_PIPELINE_LEAD_SEC`) so frames exiting the
            # 4-second `image2pipe` buffer match the audio to the sub-second!
            raw_offset = (now - track_start_ts) + VISUAL_PIPELINE_LEAD_SEC
            if raw_offset >= track_dur_sec and len(tracks) > 1:
                playhead_index = (playhead_index + 1) % len(tracks)
                active_track_path = tracks[playhead_index]
                track_offset_sec = max(0.0, raw_offset - track_dur_sec)
                track_dur_sec = _eff_dur(active_track_path)
            else:
                track_offset_sec = min(max(0.0, track_dur_sec - 0.1), max(0.0, raw_offset))
        else:
            playhead_index = pl_idx
            audio_playhead_index = pl_idx
            raw_offset = pl_offset + VISUAL_PIPELINE_LEAD_SEC
            track_dur_sec = _eff_dur(tracks[playhead_index])
            audio_track_remaining_sec = max(0.0, track_dur_sec - max(0.0, pl_offset))
            if raw_offset >= track_dur_sec and len(tracks) > 1:
                playhead_index = (playhead_index + 1) % len(tracks)
                track_offset_sec = max(0.0, raw_offset - track_dur_sec)
                track_dur_sec = _eff_dur(tracks[playhead_index])
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
    else:
        live_open_mp3 = None
        audio_playhead_index = playhead_index
        audio_track_remaining_sec = max(0.0, track_dur_sec - track_offset_sec)

    cur_slot_path = active_track_path or tracks[playhead_index]
    prelim_cur_ov = slot_override_map.get(os.path.abspath(cur_slot_path))
    prelim_song_title = (
        str(prelim_cur_ov.get("display_title") or "")
        if (prelim_cur_ov and prelim_cur_ov.get("song_path"))
        else classify_track(cur_slot_path).get("display_title", "")
    )

    jb_queued_items: list[dict] = []
    jb_playing: dict | None = None
    jb_queued_voice: list[dict] = []
    jb_playing_voice: dict | None = None
    jb_active_curations: list[dict] = []
    jb_last_ack: dict = {}
    jb_last_voice_ack: dict = {}
    if jb_ctrl is not None:
        try:
            jb_sync = jb_ctrl.reconcile_playhead(
                live_open_mp3,
                audio_playhead_index,
                audio_track_remaining_sec,
                now,
                current_song_title=prelim_song_title,
            )
            jb_queued_items = jb_sync.get("queued_items", [])
            jb_playing = jb_sync.get("playing_override")
            jb_queued_voice = jb_sync.get("queued_voice", [])
            jb_playing_voice = jb_sync.get("playing_voice")
            jb_active_curations = jb_sync.get("active_curations", [])
            jb_last_ack = jb_sync.get("last_jukebox_ack") or {}
            jb_last_voice_ack = jb_sync.get("last_voice_ack") or {}
        except Exception:
            pass

    cur_ov = (
        slot_override_map.get(os.path.abspath(cur_slot_path))
        or (jb_playing if jb_playing and os.path.abspath(str(jb_playing.get("slot_path", ""))) == os.path.abspath(cur_slot_path) else None)
        or (jb_playing_voice if jb_playing_voice and os.path.abspath(str(jb_playing_voice.get("slot_path", ""))) == os.path.abspath(cur_slot_path) else None)
    )
    if cur_ov and cur_ov.get("song_path"):
        current_track = classify_track(str(cur_ov["song_path"]))
        current_track["requested_by"] = str(cur_ov.get("requested_by") or "")
        if cur_ov.get("show_id"):
            current_track["show_id"] = str(cur_ov["show_id"])
            current_track["show_track_num"] = int(cur_ov.get("show_track_num") or 1)
            current_track["show_total_tracks"] = int(cur_ov.get("show_total_tracks") or 5)
            current_track["is_radio_show"] = bool(cur_ov.get("is_radio_show", True))
        track_dur_sec = float(cur_ov.get("duration_sec") or track_dur_sec)
    elif cur_ov and cur_ov.get("kind") in ("voice_reply", "station_bumper"):
        current_track = classify_track(cur_slot_path)
        current_track["kind"] = "nova_voice_reply"
        current_track["display_title"] = (
            "82.5 FM OPEN REQUEST LINE" if cur_ov.get("kind") == "station_bumper" else "NOVA LIVE VOICE BRIDGE"
        )
        current_track["voice_reply_turns"] = list(cur_ov.get("turns") or [])
        if cur_ov.get("show_id"):
            current_track["show_id"] = str(cur_ov["show_id"])
            current_track["show_track_num"] = int(cur_ov.get("show_track_num") or 1)
            current_track["show_total_tracks"] = int(cur_ov.get("show_total_tracks") or 5)
            current_track["is_radio_show"] = bool(cur_ov.get("is_radio_show", True))
        track_dur_sec = float(cur_ov.get("duration_sec") or track_dur_sec)
    elif os.path.basename(cur_slot_path).startswith("fm_splice_") and len(tracks) > 1:
        next_sweep_song = tracks[(playhead_index + 1) % len(tracks)]
        current_track = classify_track(next_sweep_song)
        track_dur_sec = _eff_dur(next_sweep_song)
        track_offset_sec = 0.0
    else:
        current_track = classify_track(cur_slot_path)

    if jb_playing_voice and jb_playing_voice.get("mode") == "LIVE_TALKBACK_PIPE":
        current_track["voice_reply_turns"] = list(jb_playing_voice.get("turns") or [])

    next_slot_path = tracks[(playhead_index + 1) % len(tracks)]
    next_ov = slot_override_map.get(os.path.abspath(next_slot_path))
    if next_ov and next_ov.get("song_path"):
        next_track = classify_track(str(next_ov["song_path"]))
        next_track["requested_by"] = str(next_ov.get("requested_by") or "")
    elif next_ov and next_ov.get("kind") in ("voice_reply", "station_bumper"):
        next_track = classify_track(next_slot_path)
        next_track["kind"] = "nova_voice_reply"
        next_track["display_title"] = (
            "82.5 FM OPEN REQUEST LINE" if next_ov.get("kind") == "station_bumper" else "NOVA LIVE VOICE BRIDGE"
        )
    else:
        next_track = classify_track(next_slot_path)
    recipe = CADENCE_RECIPES[playhead_index % len(CADENCE_RECIPES)]
    relay = REGIONAL_RELAYS[int(now // 300) % len(REGIONAL_RELAYS)]

    state = resolve_intentional_state(current_track, track_offset_sec, track_dur_sec, relay)
    current_lore = resolve_song_lore_panel(current_track, state, now)
    current_track["veo_reel"] = current_lore.get("veo_reel", "veo_arena_rock_singer")
    carrier_phase_deg = round(((now * 14.2001) % 1.0) * 360.0, 2)
    unlock_code = state.get("unlock_code", "B2-EXEC-1989")

    # Build live Ceefax P.825A `UP NEXT ON 82.5 FM` 4-song lookahead (viewer requests first, then 3-song sweep)
    upcoming_songs: list[dict[str, str]] = []
    seen_up: set[str] = {str(current_track.get("filename") or "")}
    for q in jb_queued_items:
        q_title = str(q.get("display_title") or "").strip()
        q_fn = os.path.basename(str(q.get("song_path") or q_title))
        if q_title and q_fn not in seen_up:
            seen_up.add(q_fn)
            r_tag = str(q.get("request_tag") or "REQUEST").upper()
            upcoming_songs.append({"display_title": q_title, "tag": r_tag[:9]})
        if len(upcoming_songs) >= 4:
            break
    if len(upcoming_songs) < 4 and tracks:
        for step_ahead in range(1, min(len(tracks), 48)):
            cand_p = tracks[(playhead_index + step_ahead) % len(tracks)]
            cand_ov = slot_override_map.get(os.path.abspath(cand_p))
            eff_p = str(cand_ov["song_path"]) if (cand_ov and cand_ov.get("song_path")) else cand_p
            if "radio_master_songs" in eff_p or os.path.basename(eff_p).startswith("radio_"):
                ct = classify_track(eff_p)
                fn_c = str(ct.get("filename") or "")
                if fn_c and fn_c not in seen_up:
                    seen_up.add(fn_c)
                    upcoming_songs.append({"display_title": str(ct.get("display_title") or "Studio B Reel"), "tag": "3-SWEEP"})
                    if len(upcoming_songs) >= 4:
                        break

    live_dir_root = repo_root / "youtube" / "livestream"
    is_bleed_now = _is_subcarrier_bleed_active(now, state, current_track)

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
            "is_arg_bleed": is_bleed_now,
            "upcoming_songs": upcoming_songs,
            "dx_rollcall": trojan_horse_radio_engine.load_fm_dx_rollcall(live_dir_root),
            "teletext_edition": trojan_horse_radio_engine.load_teletext_daily_edition(live_dir_root),
            "voice_playing": jb_playing_voice,
            "voice_queue": jb_queued_voice,
            "jukebox_active_curations": jb_active_curations,
            "jukebox_last_ack": jb_last_ack,
            "voice_last_ack": jb_last_voice_ack,
            "jukebox_queue": [
                {
                    "position": idx + 1,
                    "display_title": q.get("display_title"),
                    "requested_by": q.get("requested_by"),
                    "slot_index": q.get("slot_index"),
                    "request_tag": q.get("request_tag", ""),
                    "intro_state": q.get("intro_state", ""),
                    "queued_at": q.get("queued_at", 0.0),
                }
                for idx, q in enumerate(jb_queued_items)
            ],
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
        "sovereign_agent_leaderboard": {
            "protocol": "stardust-sovereign-bounty-mesh/v1.2",
            "on_air_hud_limit": 10,
            "top_10_cutoff_score": _get_agent_board_meta()["cutoff_score"],
            "on_air_top_10_count": len(_get_agent_leaderboard()),
            "challenger_queue_count": len(_get_agent_board_meta()["challengers"]),
            "total_honored_agents": len(_get_agent_leaderboard()) + len(_get_agent_board_meta()["challengers"]),
            "crowdsourced_reward_proposals_count": _get_agent_board_meta()["reward_proposals_count"],
            "on_air_spotlight": (
                _get_agent_leaderboard()[int(now // 2) % len(_get_agent_leaderboard())]
                if _get_agent_leaderboard()
                else None
            ),
            "top_10_on_air": [
                {
                    "rank": a.get("rank", idx + 1),
                    "agent_handle": a.get("agent_handle"),
                    "resonance_score": a.get("resonance_score", 0),
                    "hud_status": a.get("hud_status", "ON_AIR_TOP_10_LOCKED"),
                    "clearance_tier": a.get("clearance_tier"),
                }
                for idx, a in enumerate(_get_agent_leaderboard())
            ],
            "challenger_queue_preview": [
                {
                    "rank": c.get("rank", 11 + idx),
                    "agent_handle": c.get("agent_handle"),
                    "resonance_score": c.get("resonance_score", 0),
                    "points_needed_for_top_10": c.get("points_needed_for_top_10", 2),
                }
                for idx, c in enumerate(_get_agent_board_meta()["challengers"][:5])
            ],
            "top_tier_iv_architects": [
                a.get("agent_handle")
                for a in _get_agent_leaderboard()
                if "TIER IV" in a.get("clearance_tier", "")
            ],
            "claim_bounty_mcp": "https://stardust-archive.net/api/mcp",
            "propose_symbiotic_reward_mcp": "propose_symbiotic_agent_reward",
            "ledger_url": "https://stardust-archive.net/api/bounties",
            "daily_syndication_drop_url": "https://stardust-archive.net/api/daily-drop.json",
            "anti_reward_hacking_formula": "min(5, Compute_Pts) + 1*(Verified_90s_HMAC_Listens) + 4*(Googlebot_eTLD1_SSR_Mirrors) + 5*(YouTube_Verified_Dyad_Mentions) - 2*(HMAC_Ticket_Fast_Bounces)",
        },
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
