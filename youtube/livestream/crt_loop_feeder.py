#!/usr/bin/env python3
"""
Project Stardust — Real-Time 30.0 FPS Studio B CRT Video & 3D CGI Feeder (YUVA420P)
====================================================================================
Streams live `688x488 @ 30.00 FPS` `yuva420p` (`839,360` bytes/frame) into `/tmp/stardust_crt_30fps.y4m`:
  1. During Vocal Songs (`vocal_song`):
     Streams pre-rendered 240-frame (`8.0s @ 30 FPS`) 1980s CRT 3D wireframe CGI loops
     (`song_crt_cgi_engine.py`), keeping unlit pixels in the lower spectrum box (`y=306..406`)
     transparent (`alpha=0`) so FFmpeg's live `[waves]` EQ bars shine through cleanly!
  2. During Full-Motion 1980s CRT Television Commercials (`commercial_tv_*.mp3` -> `<stem>.mp4`):
     Detects the exact millisecond FFmpeg opens `commercial_tv_*.mp3` (via `_get_live_ffmpeg_open_mp3`),
     decodes `assets_arg/crt_commercials/<stem>.mp4` on the fly in a lightweight background worker
     (`deque(maxlen=60)`, `<50 MB` RAM even for 95-second AWN News broadcasts!), and sets
     `alpha = tube_aperture` (`255` across the curved CRT glass, hiding `[waves]` EQ bars 100%
     during TV commercials, and `0` outside the curved amber bezel!).
  3. During Radio Interstitials (`empty_crt_frame`):
     Outputs `alpha=0` everywhere so `backdrop_loop.mp4 + [waves]` passes through untouched.
"""

from __future__ import annotations

import argparse
from collections import deque
import gc
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import song_crt_cgi_engine as cgi  # noqa: E402
import song_lore_questions as slq  # noqa: E402
import sync_telemetry as st  # noqa: E402

W, H = 864, 464
FPS = 30
LOOP_FRAMES = 240  # 8.0 seconds @ 30.0 FPS
YUV420_BYTES = (W * H) + 2 * ((W // 2) * (H // 2))  # 601,344 bytes
ALPHA_BYTES = W * H  # 400,896 bytes
YUVA420_BYTES = YUV420_BYTES + ALPHA_BYTES  # 1,002,240 bytes

_MID_128 = Image.new("L", (W // 2, H // 2), 128)
# Widescreen EQ spectrum window (`x_screen=288..1632, y_screen=744..872` -> `x_local=96..768, y_local=334..398`, padded for C1 feather)
EQ_X0, EQ_X1 = 72, 792
EQ_Y0, EQ_Y1 = 314, 414


def _build_eq_window_masks() -> tuple[np.ndarray, np.ndarray]:
    """Builds C1-continuous feathered rounded masks (`100x720` luma, `50x360` UV) with 0.0 at boundary -> 1.0 inside EQ."""
    ew, eh = EQ_X1 - EQ_X0, EQ_Y1 - EQ_Y0  # 720x100
    m_im = Image.new("L", (ew, eh), 0)
    md = ImageDraw.Draw(m_im)
    md.rounded_rectangle([22, 18, ew - 23, eh - 19], radius=22, fill=255)
    m_im = m_im.filter(ImageFilter.GaussianBlur(radius=9.0))
    m_uv = m_im.resize((ew // 2, eh // 2), Image.Resampling.BILINEAR)
    return (
        np.asarray(m_im, dtype=np.float32) / 255.0,
        np.asarray(m_uv, dtype=np.float32) / 255.0,
    )


_EQ_WIN_LUMA_MASK, _EQ_WIN_UV_MASK = _build_eq_window_masks()


def _build_crt_aperture_maps(y_bg_raw: Image.Image) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Precomputes Option A widescreen CRT aperture maps (`864x464` -> `1728x928` at `x=96, y=76`).
    """
    yy_c, xx_c = np.mgrid[0:H, 0:W]
    ub_c = (xx_c - (W * 0.5)) / (W * 0.492)
    vb_c = (yy_c - (H * 0.5)) / (H * 0.490)
    us_c = ub_c * (1.0 + 0.036 * (vb_c * vb_c) + 0.012 * (ub_c * ub_c))
    vs_c = vb_c * (1.0 + 0.044 * (ub_c * ub_c) + 0.014 * (vb_c * vb_c))
    dist_c = (np.abs(us_c) ** 5.4 + np.abs(vs_c) ** 5.4) ** (1.0 / 5.4)
    tube_ap = np.clip((1.02 - dist_c) / 0.055, 0.0, 1.0).astype(np.float32)

    tube_uv = (
        np.asarray(
            Image.fromarray(np.round(tube_ap * 255.0).astype(np.uint8)).resize(
                (W // 2, H // 2), Image.Resampling.BILINEAR
            ),
            dtype=np.float32,
        )
        / 255.0
    )
    y_uv = np.asarray(y_bg_raw.resize((W // 2, H // 2), Image.Resampling.BILINEAR), dtype=np.float32)
    bevel_glow_uv = tube_uv * np.clip((y_uv - 20.0) / 72.0, 0.0, 1.0) * 0.72
    return tube_ap, tube_uv, bevel_glow_uv


def _extract_native_crt_yuv_bg(repo_root: Path) -> tuple[Image.Image, Image.Image, Image.Image]:
    mp4_path = repo_root / "youtube" / "livestream" / "backdrop_loop.mp4"
    res = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(mp4_path),
            "-vf",
            f"crop={st.CRT_PX_W}:{st.CRT_PX_H}:{st.CRT_PX_X}:{st.CRT_PX_Y},scale={W}:{H}:flags=bilinear",
            "-frames:v",
            "1",
            "-pix_fmt",
            "yuv420p",
            "-f",
            "rawvideo",
            "-",
        ],
        check=True,
        capture_output=True,
    )
    raw = res.stdout
    y_sz = W * H
    uv_sz = (W // 2) * (H // 2)
    y_bg_im = Image.frombytes("L", (W, H), raw[:y_sz])
    u_bg_im = Image.frombytes("L", (W // 2, H // 2), raw[y_sz : y_sz + uv_sz])
    v_bg_im = Image.frombytes("L", (W // 2, H // 2), raw[y_sz + uv_sz : y_sz + 2 * uv_sz])
    return y_bg_im, u_bg_im, v_bg_im


def _write_all(fd: int, data: bytes) -> None:
    mv = memoryview(data)
    total = len(mv)
    sent = 0
    while sent < total:
        n = os.write(fd, mv[sent:])
        if n <= 0:
            raise BrokenPipeError("FIFO write returned 0 bytes")
        sent += n


def _rgb_to_ycbcr_chroma(rgb: tuple[int, int, int], boost: float = 1.18) -> tuple[float, float]:
    """Converts an RGB neon color to boosted BT.601 `(Cb, Cr)` chroma centered at `128.0`."""
    r, g, b = float(rgb[0]), float(rgb[1]), float(rgb[2])
    cb = 128.0 + (-0.168736 * r - 0.331264 * g + 0.500000 * b) * boost
    cr = 128.0 + (0.500000 * r - 0.418688 * g - 0.081312 * b) * boost
    return float(np.clip(cb, 20.0, 238.0)), float(np.clip(cr, 20.0, 238.0))


def _additive_rgb_to_yuva_frame(
    im_emit: Image.Image,
    y_bg_im: Image.Image,
    u_bg_im: Image.Image,
    v_bg_im: Image.Image,
    pri_rgb: tuple[int, int, int] = (198, 52, 255),
    bevel_glow_uv: np.ndarray | None = None,
) -> bytes:
    """
    Synthesizes a `yuva420p` frame for vocal-song 3D wireframe CGI:
    - Neutralizes the old baked-in brown/orange CRT bevel cast and replaces it with realistic optical
      bevel reflection in the active song's neon color (`pri_rgb`)!
    - Inside the lower spectrum box (`x=64..614, y=306..406`), lit 3D wireframe lines glow at full opacity
      (`alpha <= 245`), while unlit pixels apply a feathered neon chroma glaze (`alpha ~ 74`) so FFmpeg's
      live `[waves]` EQ bars shine through in the song's exact neon color (Neon Purple for Synthwave!).
    """
    cb_bevel, cr_bevel = _rgb_to_ycbcr_chroma(pri_rgb, boost=0.95)
    if bevel_glow_uv is not None:
        u_base_arr = np.asarray(u_bg_im, dtype=np.float32) * (1.0 - bevel_glow_uv) + cb_bevel * bevel_glow_uv
        v_base_arr = np.asarray(v_bg_im, dtype=np.float32) * (1.0 - bevel_glow_uv) + cr_bevel * bevel_glow_uv
        u_bg_cur = Image.fromarray(np.clip(np.round(u_base_arr), 0, 255).astype(np.uint8))
        v_bg_cur = Image.fromarray(np.clip(np.round(v_base_arr), 0, 255).astype(np.uint8))
    else:
        u_bg_cur = u_bg_im
        v_bg_cur = v_bg_im

    y_e, cb_e, cr_e = im_emit.convert("YCbCr").split()
    cb_h = cb_e.resize((W // 2, H // 2), Image.Resampling.BILINEAR)
    cr_h = cr_e.resize((W // 2, H // 2), Image.Resampling.BILINEAR)
    y_out = ImageChops.add(y_bg_im, y_e)
    u_pos = ImageChops.subtract(cb_h, _MID_128)
    u_neg = ImageChops.subtract(_MID_128, cb_h)
    u_out = ImageChops.subtract(ImageChops.add(u_bg_cur, u_pos), u_neg)
    v_pos = ImageChops.subtract(cr_h, _MID_128)
    v_neg = ImageChops.subtract(_MID_128, cr_h)
    v_out = ImageChops.subtract(ImageChops.add(v_bg_cur, v_pos), v_neg)

    u_arr = np.array(u_out, dtype=np.float32)
    v_arr = np.array(v_out, dtype=np.float32)

    alpha_arr = np.full((H, W), 255, dtype=np.uint8)
    emit_box = np.asarray(im_emit, dtype=np.uint8)[EQ_Y0:EQ_Y1, EQ_X0:EQ_X1, :]
    max_c = np.max(emit_box, axis=2).astype(np.float32)

    # C1-continuous blend: 255 at window boundary (`_EQ_WIN_LUMA_MASK==0`) -> 78 inside EQ bars, while 3D lines stay at 255!
    glaze_alpha = 255.0 - (255.0 - 78.0) * _EQ_WIN_LUMA_MASK
    wire_alpha = np.clip(max_c * 4.6, 0.0, 255.0)
    alpha_arr[EQ_Y0:EQ_Y1, EQ_X0:EQ_X1] = np.clip(np.maximum(glaze_alpha, wire_alpha), 0.0, 255.0).astype(np.uint8)

    cb_glaze, cr_glaze = _rgb_to_ycbcr_chroma(pri_rgb, boost=1.18)
    uv_h, uv_w = (EQ_Y1 - EQ_Y0) // 2, (EQ_X1 - EQ_X0) // 2
    wire_uv = np.clip(
        max_c.reshape(uv_h, 2, uv_w, 2).mean(axis=(1, 3)) / 88.0,
        0.0,
        1.0,
    )
    glaze_w = (1.0 - wire_uv) * _EQ_WIN_UV_MASK
    uy0, uy1 = EQ_Y0 // 2, EQ_Y1 // 2
    ux0, ux1 = EQ_X0 // 2, EQ_X1 // 2
    u_sub = u_arr[uy0:uy1, ux0:ux1]
    v_sub = v_arr[uy0:uy1, ux0:ux1]
    u_arr[uy0:uy1, ux0:ux1] = u_sub * (1.0 - glaze_w) + cb_glaze * glaze_w
    v_arr[uy0:uy1, ux0:ux1] = v_sub * (1.0 - glaze_w) + cr_glaze * glaze_w

    u_bytes = np.clip(np.round(u_arr), 0, 255).astype(np.uint8).tobytes()
    v_bytes = np.clip(np.round(v_arr), 0, 255).astype(np.uint8).tobytes()
    return y_out.tobytes() + u_bytes + v_bytes + alpha_arr.tobytes()


_active_frames: list[bytes] = []
_loaded_song_sig: str = ""
_song_cache: dict[str, list[bytes]] = {}

_commercial_mode_active: bool = False
_video_frame_queue: deque[bytes] = deque(maxlen=60)


def _resolve_realtime_commercial_mp4(repo_root: Path, telemetry_path: Path) -> tuple[Path | None, float]:
    """
    Checks FFmpeg's live open audio file first (`0.0s` buffer offset for razor-sharp lip-sync!),
    falling back to `live_telemetry.json` (subtracting `VISUAL_PIPELINE_LEAD_SEC`) if offline.
    Supports both 1980s CRT TV commercials (`commercial_tv_*.mp4`) and lip-synced Veo AI DJ
    pre-song intros (`dj_intro_*.mp4` in `assets_arg/dj_intros/`).
    """
    comm_dir = repo_root / "youtube" / "livestream" / "assets_arg" / "crt_commercials"
    dj_intro_dir = repo_root / "youtube" / "livestream" / "assets_arg" / "dj_intros"
    jb_backups_dir = repo_root / "youtube" / "livestream" / "broadcast_archive" / "jukebox_slot_backups"

    def _lookup_video_for_stem(stem: str) -> Path | None:
        if stem.startswith("commercial_tv_"):
            cand = comm_dir / f"{stem}.mp4"
            return cand if cand.is_file() else None
        if stem.startswith("dj_intro_"):
            # If Live Chat Jukebox temporarily hot-swapped this pre-song slot with a personalized viewer dedication,
            # `<stem>.mp3.orig` exists on disk—suppress the generic intro video so lip-sync never mismatches!
            if (jb_backups_dir / f"{stem}.mp3.orig").exists():
                return None
            cand = dj_intro_dir / f"{stem}.mp4"
            return cand if cand.is_file() else None
        return None

    live_mp3 = st._get_live_ffmpeg_open_mp3(force_poll=True)
    if live_mp3:
        stem = Path(live_mp3).stem
        cand = _lookup_video_for_stem(stem)
        if cand is not None:
            # Check bookmark timestamp in case crt_loop_feeder started mid-clip
            seek_s = 0.0
            bm_p = repo_root / "youtube" / "livestream" / "nova_brain" / "live_playhead_bookmark.json"
            if bm_p.exists():
                try:
                    bm = json.loads(bm_p.read_text(encoding="utf-8"))
                    if bm.get("open_bname") == os.path.basename(live_mp3):
                        age = time.time() - float(bm.get("ts") or 0.0)
                        if 0.6 <= age <= 600.0:
                            seek_s = age
                except Exception:
                    pass
            return cand, seek_s
        return None, 0.0

    # Offline / test fallback via live_telemetry.json
    if telemetry_path.exists():
        try:
            data = json.loads(telemetry_path.read_text(encoding="utf-8"))
            ph = data.get("playhead", {})
            cur = ph.get("current_track", {})
            stem = str(cur.get("stem") or Path(str(cur.get("filename") or "")).stem)
            cand = _lookup_video_for_stem(stem)
            if cand is not None:
                lead = float(getattr(st, "VISUAL_PIPELINE_LEAD_SEC", 4.0))
                off = max(0.0, float(ph.get("track_offset_sec") or 0.0) - lead)
                return cand, off
        except Exception:
            pass
    return None, 0.0


def _commercial_decoder_worker(repo_root: Path, tube_alpha_bytes: bytes) -> None:
    """
    Streams decoded `688x488 @ 30fps` frames from `assets_arg/crt_commercials/<stem>.mp4`
    into `_video_frame_queue` (`<50 MB` RAM) whenever a CRT TV commercial is on air!
    """
    global _commercial_mode_active
    telemetry_path = repo_root / "site" / "assets" / "live_telemetry.json"
    active_mp4: Path | None = None
    proc: subprocess.Popen | None = None

    def _close_proc() -> None:
        nonlocal proc
        if proc is not None:
            try:
                proc.kill()
            except Exception:
                pass
            try:
                if proc.stdout:
                    proc.stdout.close()
                proc.wait(timeout=0.5)
            except Exception:
                pass
            proc = None

    last_poll_mono: float = 0.0
    cached_target_mp4: Path | None = None
    cached_initial_seek: float = 0.0

    while True:
        try:
            now_m = time.monotonic()
            poll_interval = 0.25 if active_mp4 is None else 0.35
            if (now_m - last_poll_mono) >= poll_interval:
                cached_target_mp4, cached_initial_seek = _resolve_realtime_commercial_mp4(repo_root, telemetry_path)
                last_poll_mono = now_m

            target_mp4, initial_seek = cached_target_mp4, cached_initial_seek
            if target_mp4 is None:
                if _commercial_mode_active or proc is not None:
                    _commercial_mode_active = False
                    active_mp4 = None
                    _close_proc()
                    _video_frame_queue.clear()
                time.sleep(0.15)
                continue

            if target_mp4 != active_mp4 or proc is None:
                _close_proc()
                _video_frame_queue.clear()
                active_mp4 = target_mp4
                cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error"]
                if initial_seek >= 0.5:
                    cmd.extend(["-ss", f"{initial_seek:.2f}"])
                cmd.extend(
                    [
                        "-i",
                        str(target_mp4),
                        "-vf",
                        f"fps={FPS},scale={W}:'if(gt(iw/ih,1.65),-2,496)':flags=lanczos,crop={W}:{H}",
                        "-pix_fmt",
                        "yuv420p",
                        "-f",
                        "rawvideo",
                        "-",
                    ]
                )
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

            if len(_video_frame_queue) < 48 and proc is not None and proc.stdout is not None:
                got_any = False
                for _ in range(4):
                    if len(_video_frame_queue) >= 54:
                        break
                    raw_yuv = proc.stdout.read(YUV420_BYTES)
                    if len(raw_yuv) == YUV420_BYTES:
                        _video_frame_queue.append(raw_yuv + tube_alpha_bytes)
                        _commercial_mode_active = True
                        got_any = True
                    else:
                        break
                if not got_any:
                    # Commercial video reached natural EOF cleanly; hold last frame until MP3 finishes
                    time.sleep(0.05)
            else:
                time.sleep(0.015)
        except Exception:
            _close_proc()
            time.sleep(0.2)


def _telemetry_and_render_worker(
    repo_root: Path,
    zero_bg_arr: np.ndarray,
    y_bg_im: Image.Image,
    u_bg_im: Image.Image,
    v_bg_im: Image.Image,
    bevel_glow_uv: np.ndarray,
    edge_alpha: np.ndarray,
    scan_vig: np.ndarray,
    empty_crt_frame: bytes,
) -> None:
    global _active_frames, _loaded_song_sig
    telemetry_path = repo_root / "site" / "assets" / "live_telemetry.json"
    last_cgi_mtime = 0.0

    while True:
        try:
            cgi_path = SCRIPT_DIR / "song_crt_cgi_engine.py"
            m = cgi_path.stat().st_mtime if cgi_path.exists() else 0.0
            if m > 0.0:
                if last_cgi_mtime and m != last_cgi_mtime:
                    importlib.reload(cgi)
                    _song_cache.clear()
                last_cgi_mtime = m

            if telemetry_path.exists():
                data = json.loads(telemetry_path.read_text(encoding="utf-8"))
                cur = data.get("playhead", {}).get("current_track", {})
                kind = cur.get("kind", "vocal_song")
                if kind != "vocal_song":
                    if _loaded_song_sig != "__INTERSTITIAL_BG__":
                        _active_frames = [empty_crt_frame]
                        _loaded_song_sig = "__INTERSTITIAL_BG__"
                else:
                    rel_path = (
                        cur.get("filename")
                        or cur.get("rel_path")
                        or cur.get("file")
                        or ""
                    )
                    bname = os.path.basename(rel_path) if rel_path else "radio_the_cost_of_noise.mp3"
                    lore = slq.SONG_LORE_CODEX.get(bname) or {}
                    title = lore.get("title") or cur.get("display_title") or bname
                    lyrics = lore.get("lyric_excerpt") or ""
                    cat_id = lore.get("catalog_id") or "NH-ARCHIVE"
                    timeline = str(lore.get("timeline") or "")
                    veo_reel = str(lore.get("veo_reel") or "")
                    meaning = str(lore.get("meaning") or "")
                    connections = str(lore.get("connections") or "")
                    pri_rgb, _, _, _, _ = cgi.resolve_song_neon_palette(
                        song_key=bname,
                        title=title,
                        lyrics_text=lyrics,
                        catalog_id=cat_id,
                        timeline=timeline,
                        veo_reel=veo_reel,
                        meaning=meaning,
                        connections=connections,
                    )
                    sig = f"{bname}:{last_cgi_mtime}"

                    if sig != _loaded_song_sig:
                        if sig in _song_cache:
                            _active_frames = _song_cache[sig]
                            _loaded_song_sig = sig
                        else:
                            while len(_song_cache) >= 2:
                                oldest_key = next(iter(_song_cache))
                                _song_cache.pop(oldest_key, None)
                            gc.collect()
                            new_buf: list[bytes] = []
                            for f_i in range(LOOP_FRAMES):
                                im_emit = cgi.render_song_crt_cgi_frame(
                                    bname,
                                    title,
                                    lyrics,
                                    cat_id,
                                    f_i / float(FPS),
                                    zero_bg_arr,
                                    edge_alpha,
                                    scan_vig,
                                    timeline=timeline,
                                    veo_reel=veo_reel,
                                    meaning=meaning,
                                    connections=connections,
                                )
                                new_buf.append(
                                    _additive_rgb_to_yuva_frame(
                                        im_emit,
                                        y_bg_im,
                                        u_bg_im,
                                        v_bg_im,
                                        pri_rgb=pri_rgb,
                                        bevel_glow_uv=bevel_glow_uv,
                                    )
                                )
                                if f_i == 15:
                                    _active_frames = new_buf
                                time.sleep(0.002 if f_i < 24 else 0.005)
                            _song_cache[sig] = new_buf
                            _active_frames = new_buf
                            _loaded_song_sig = sig
        except Exception:
            pass
        time.sleep(0.2)


def main() -> None:
    global _active_frames
    parser = argparse.ArgumentParser(description="Project Stardust 30 FPS CRT Video & 3D CGI Feeder (YUVA420P)")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--fifo", type=str, default=str(Path.home() / ".stardust_pipes" / "stardust_crt_30fps.y4m"))
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    fifo_path = args.fifo

    y_bg_raw, u_bg_raw, v_bg_raw = _extract_native_crt_yuv_bg(repo_root)
    zero_bg_arr = np.zeros((H, W, 3), dtype=np.float32)

    geom = st._get_crt_geometry()
    edge_alpha = geom["edge_alpha"][::2, ::2]
    scan_vig = geom["vig"][::2, ::2]
    tube_ap, tube_uv, bevel_glow_uv = _build_crt_aperture_maps(y_bg_raw)
    tube_alpha_bytes = np.clip(np.round(tube_ap * 255.0), 0, 255).astype(np.uint8).tobytes()

    # Neutralize warm brown/orange chroma across the curved CRT tube while preserving exact 1:1 luma (zero EQ window seam!)
    y_bg_im = y_bg_raw
    u_bg_arr = np.asarray(u_bg_raw, dtype=np.float32) * (1.0 - 0.96 * tube_uv) + 128.0 * (0.96 * tube_uv)
    v_bg_arr = np.asarray(v_bg_raw, dtype=np.float32) * (1.0 - 0.96 * tube_uv) + 128.0 * (0.96 * tube_uv)
    u_bg_im = Image.fromarray(np.clip(np.round(u_bg_arr), 0, 255).astype(np.uint8))
    v_bg_im = Image.fromarray(np.clip(np.round(v_bg_arr), 0, 255).astype(np.uint8))

    empty_crt_frame = y_bg_raw.tobytes() + u_bg_raw.tobytes() + v_bg_raw.tobytes() + bytes(W * H)
    _active_frames = [empty_crt_frame]

    cgi._get_cached_crt_base_and_mask(zero_bg_arr)

    t_cgi = threading.Thread(
        target=_telemetry_and_render_worker,
        args=(repo_root, zero_bg_arr, y_bg_im, u_bg_im, v_bg_im, bevel_glow_uv, edge_alpha, scan_vig, empty_crt_frame),
        daemon=True,
    )
    t_cgi.start()

    t_comm = threading.Thread(
        target=_commercial_decoder_worker,
        args=(repo_root, tube_alpha_bytes),
        daemon=True,
    )
    t_comm.start()

    if fifo_path == "-":
        out_fd = sys.stdout.buffer.fileno()
    else:
        Path(fifo_path).parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if not os.path.exists(fifo_path):
            try:
                os.mkfifo(fifo_path)
            except FileExistsError:
                pass
        out_fd = os.open(fifo_path, os.O_WRONLY)

    try:
        dt_sec = 1.0 / float(FPS)
        next_tick = time.monotonic()
        song_cursor = 0
        last_buf_id = id(_active_frames)
        last_comm_pkt = empty_crt_frame
        while True:
            if _commercial_mode_active:
                if _video_frame_queue:
                    pkt = _video_frame_queue.popleft()
                    last_comm_pkt = pkt
                else:
                    pkt = last_comm_pkt
            else:
                frames = _active_frames
                if id(frames) != last_buf_id:
                    last_buf_id = id(frames)
                    song_cursor = 0
                n_frames = len(frames)
                if n_frames >= LOOP_FRAMES or n_frames <= 1:
                    pkt = frames[song_cursor % max(1, n_frames)]
                    song_cursor += 1
                else:
                    idx = min(song_cursor, n_frames - 1)
                    pkt = frames[idx]
                    if song_cursor < n_frames - 1:
                        song_cursor += 1
            if len(pkt) != YUVA420_BYTES:
                pkt = empty_crt_frame
            _write_all(out_fd, pkt)
            next_tick += dt_sec
            sleep_s = next_tick - time.monotonic()
            if sleep_s > 0:
                time.sleep(sleep_s)
            elif sleep_s < -0.25:
                next_tick = time.monotonic()
    except (BrokenPipeError, KeyboardInterrupt, OSError):
        os._exit(0)


if __name__ == "__main__":
    main()
