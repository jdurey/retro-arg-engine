#!/usr/bin/env python3
"""
/audio-analog — 1989 Sublevel B2 Eerie Distant Type-I Ferric Cassette Dub Processor

Applies the signature Project Stardust 1989 worn cassette dub DSP chain to any
local audio file, directory, HTML file with base64-embedded MP3s, or live URL:
  1. 35% (0.35x) Wow & Flutter (capstan 0.52 Hz & 1.15 Hz drift + 6.4 Hz pinch-roller flutter + initial motor spin-up scoop)
  2. Eerie Distant Stereo Collapse (22% width) + 6-sample head azimuth phase skew + 0.37 Hz R-channel head-contact drift
  3. Periodic Magnetic Oxide Crinkles & Asymmetric Dropouts (every 14.2s)
  4. Type-I Ferric Bandpass (165 Hz - 2,950 Hz) + 240 Hz & 780 Hz cassette shell resonance + asymmetric tanh saturation (drive=3.2) + 3,100 Hz post-rolloff
  5. Dynamic Analog Bias Hiss (350 Hz - 4,200 Hz) + 60/120/180 Hz power transformer hum
  6. No mechanical tape-button clicks by default (enable with --clicks)
"""

import argparse
import base64
import concurrent.futures
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request
import numpy as np
import soundfile as sf
from scipy import signal
import librosa


def process_waveform(
    y: np.ndarray,
    sr: int = 44100,
    wow_scale: float = 0.35,
    add_clicks: bool = False,
    seed: int = 19890909,
) -> np.ndarray:
    """Apply the exact 1989 eerie distant Type-I ferric cassette dub DSP chain."""
    if y.ndim == 1:
        y = np.vstack([y, y])
    elif y.shape[0] > 2 and y.shape[1] <= 2:
        y = y.T
    if y.shape[0] == 1:
        y = np.vstack([y[0], y[0]])
    elif y.shape[0] > 2:
        y = y[:2]

    n_samples = y.shape[1]
    if n_samples < 64:
        return y

    t = np.arange(n_samples, dtype=np.float64) / sr
    rng = np.random.default_rng(seed)

    # 1. Wow & Flutter (default 0.35x = 35% of original v2 pass)
    spinup_scoop = -0.018 * np.exp(-t / 0.28)
    wow_offset_sec = wow_scale * (
        spinup_scoop
        + 0.0038 * np.sin(2 * np.pi * 0.52 * t + 0.2)
        + 0.0021 * np.sin(2 * np.pi * 1.15 * t + 1.4)
        + 0.00055 * np.sin(2 * np.pi * 6.4 * t)
    )
    warped_idx = np.clip(
        np.arange(n_samples, dtype=np.float64) + wow_offset_sec * sr,
        0,
        n_samples - 1,
    )
    idx0 = np.floor(warped_idx).astype(np.int64)
    idx1 = np.minimum(idx0 + 1, n_samples - 1)
    frac = (warped_idx - idx0).astype(np.float32)

    y_w = np.zeros_like(y, dtype=np.float32)
    for ch in range(2):
        y_w[ch] = y[ch, idx0] * (1.0 - frac) + y[ch, idx1] * frac

    # 2. Eerie Distant Stereo Collapse & Azimuth Phase Drift
    mid = 0.5 * (y_w[0] + y_w[1])
    side = 0.5 * (y_w[0] - y_w[1])
    y_w[0] = mid + 0.22 * side
    y_w[1] = np.roll(mid - 0.22 * side, 6)
    y_w[1] *= (0.82 + 0.16 * np.sin(2 * np.pi * 0.37 * t)).astype(np.float32)

    # 3. Magnetic Oxide Crinkles & Dropouts
    dropout_env = np.ones((2, n_samples), dtype=np.float32)
    duration_sec = n_samples / float(sr)
    for drop_t in np.arange(8.5, max(8.5, duration_sec - 1.0), 14.2):
        c_i = int(drop_t * sr)
        w_i = int(0.14 * sr)
        s0, s1 = max(0, c_i - w_i), min(n_samples, c_i + w_i)
        if s1 > s0:
            win = np.hanning(s1 - s0)
            dropout_env[0, s0:s1] *= 1.0 - 0.55 * win
            dropout_env[1, s0:s1] *= 1.0 - 0.35 * win
    y_w *= dropout_env

    # 4. Eerie Distant Lo-Fi Type-I Ferric Cassette EQ & Heavy Magnetic Saturation (165 Hz .. 2,950 Hz)
    sos_hp = signal.butter(3, 165.0 / (sr / 2), btype="highpass", output="sos")
    sos_lp = signal.butter(4, 2950.0 / (sr / 2), btype="lowpass", output="sos")
    b_warm, a_warm = signal.iirpeak(240.0 / (sr / 2), Q=1.2)
    b_box, a_box = signal.iirpeak(780.0 / (sr / 2), Q=1.0)
    sos_post = signal.butter(3, 3100.0 / (sr / 2), btype="lowpass", output="sos")

    for ch in range(2):
        s_mus = y_w[ch]
        s_mus = signal.sosfilt(sos_hp, s_mus)
        s_mus = signal.sosfilt(sos_lp, s_mus)
        warm = signal.lfilter(b_warm, a_warm, s_mus)
        box = signal.lfilter(b_box, a_box, s_mus)
        s_mus = 0.55 * s_mus + 0.30 * warm + 0.32 * box
        drive = 3.2
        s_mus = np.tanh(s_mus * drive + 0.09 * (s_mus ** 2)) / np.tanh(drive)
        s_mus = signal.sosfilt(sos_post, s_mus) * 0.72
        y_w[ch] = s_mus.astype(np.float32)

    # 5. Prominent Analog Cassette Tape Hiss & 60/120/180 Hz Transformer Hum
    white = rng.standard_normal((2, n_samples)).astype(np.float32)
    sos_hiss_bp = signal.butter(
        2, [350.0 / (sr / 2), 4200.0 / (sr / 2)], btype="bandpass", output="sos"
    )
    hiss = signal.sosfilt(sos_hiss_bp, white, axis=1)
    hiss_level = 0.018 + 0.022 * np.abs(y_w)
    hum = (
        0.0045 * np.sin(2 * np.pi * 60.0 * t)
        + 0.0028 * np.sin(2 * np.pi * 120.0 * t + 0.8)
        + 0.0018 * np.sin(2 * np.pi * 180.0 * t + 1.5)
    ).astype(np.float32)

    y_out = y_w + hiss * hiss_level + hum[None, :]

    # 6. Optional mechanical cassette button clicks (OFF by default)
    if add_clicks:
        for clk_t, amp in [(0.05, 0.35), (0.12, 0.22)]:
            ci = int(clk_t * sr)
            clen = int(0.025 * sr)
            if ci + clen < n_samples:
                burst = (
                    rng.standard_normal(clen).astype(np.float32)
                    * np.exp(-np.linspace(0, 5, clen))
                    * amp
                )
                y_out[:, ci : ci + clen] += burst[None, :]

    return np.clip(y_out, -0.95, 0.95).astype(np.float32)


def get_clean_backup_path(audio_path: str) -> str:
    """Return a deterministic clean backup path so re-runs never double-degrade."""
    abs_p = os.path.abspath(audio_path)
    path_hash = hashlib.md5(abs_p.encode("utf-8")).hexdigest()[:10]
    base_name = os.path.basename(abs_p)
    bak_dir = "/tmp/audio_analog_clean_backups"
    os.makedirs(bak_dir, exist_ok=True)
    return os.path.join(bak_dir, f"{path_hash}__{base_name}")


def process_audio_file(
    audio_path: str,
    output_path: str = None,
    wow_scale: float = 0.35,
    add_clicks: bool = False,
    bitrate: str = "128k",
    extra_mirror_paths: list = None,
) -> str:
    """Process a local audio file (and any mirror copies) with the analog cassette chain."""
    audio_path = os.path.abspath(audio_path)
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    bak_path = get_clean_backup_path(audio_path)
    if not os.path.exists(bak_path):
        shutil.copy2(audio_path, bak_path)

    sr = 44100
    y, _ = librosa.load(bak_path, sr=sr, mono=False)
    y_out = process_waveform(y, sr=sr, wow_scale=wow_scale, add_clicks=add_clicks)

    target_out = os.path.abspath(output_path) if output_path else audio_path
    ext = os.path.splitext(target_out)[1].lower()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_f:
        tmp_wav = tmp_f.name

    try:
        sf.write(tmp_wav, y_out.T, sr, subtype="PCM_16")
        if ext == ".wav":
            shutil.copy2(tmp_wav, target_out)
        elif ext == ".ogg":
            subprocess.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-i", tmp_wav,
                    "-c:a", "libvorbis", "-q:a", "4", "-ar", str(sr),
                    target_out,
                ],
                check=True,
            )
        elif ext in (".m4a", ".aac", ".mp4"):
            subprocess.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-i", tmp_wav,
                    "-c:a", "aac", "-b:a", bitrate, "-ar", str(sr),
                    target_out,
                ],
                check=True,
            )
        else:
            subprocess.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-i", tmp_wav,
                    "-c:a", "libmp3lame", "-b:a", bitrate, "-ar", str(sr),
                    target_out,
                ],
                check=True,
            )
    finally:
        if os.path.exists(tmp_wav):
            os.remove(tmp_wav)

    if extra_mirror_paths:
        for mirror in extra_mirror_paths:
            m_abs = os.path.abspath(mirror)
            if m_abs != target_out:
                os.makedirs(os.path.dirname(m_abs), exist_ok=True)
                shutil.copy2(target_out, m_abs)

    with open(target_out, "rb") as f:
        md5_hex = hashlib.md5(f.read()).hexdigest()
    return md5_hex


def process_embedded_base64_in_html(
    html_paths: list,
    wow_scale: float = 0.35,
    add_clicks: bool = False,
) -> int:
    """Find base64-encoded MP3 strings (e.g. MARCUS_EMBEDDED) in HTML/JS files and analog-process them."""
    if not html_paths:
        return 0

    b64_cache = {}
    pattern = re.compile(r'(\b\d+\s*:\s*")([A-Za-z0-9+/=]{800,})(")')

    def _repl(match):
        prefix, b64_str, suffix = match.group(1), match.group(2), match.group(3)
        if b64_str in b64_cache:
            return f"{prefix}{b64_cache[b64_str]}{suffix}"
        raw_bytes = base64.b64decode(b64_str)
        if len(raw_bytes) < 4096:
            return match.group(0)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf_in:
            tf_in.write(raw_bytes)
            in_name = tf_in.name
        out_name = in_name + ".out.mp3"
        try:
            y, _ = librosa.load(in_name, sr=44100, mono=False)
            y_out = process_waveform(y, sr=44100, wow_scale=wow_scale, add_clicks=add_clicks)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf_wav:
                wav_name = tf_wav.name
            sf.write(wav_name, y_out.T, 44100, subtype="PCM_16")
            subprocess.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-i", wav_name,
                    "-c:a", "libmp3lame", "-b:a", "64k", "-ar", "44100",
                    out_name,
                ],
                check=True,
            )
            os.remove(wav_name)
            with open(out_name, "rb") as f_out:
                new_b64 = base64.b64encode(f_out.read()).decode("ascii")
            b64_cache[b64_str] = new_b64
            return f"{prefix}{new_b64}{suffix}"
        finally:
            for p in (in_name, out_name):
                if os.path.exists(p):
                    os.remove(p)

    for hp in html_paths:
        if not os.path.exists(hp):
            continue
        bak_html = get_clean_backup_path(hp)
        if not os.path.exists(bak_html):
            shutil.copy2(hp, bak_html)
        with open(bak_html, "r", encoding="utf-8") as f:
            orig_content = f.read()
        new_content = pattern.sub(_repl, orig_content)
        with open(hp, "w", encoding="utf-8") as f:
            f.write(new_content)
    return len(b64_cache)


def main():
    parser = argparse.ArgumentParser(
        description="Apply the 1989 Sublevel B2 eerie distant Type-I ferric cassette dub sound to local or live audio files."
    )
    parser.add_argument(
        "targets",
        nargs="+",
        help="Audio file path(s), directory path(s), HTML file(s), or live URL(s).",
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional output file path (when processing a single input file).",
    )
    parser.add_argument(
        "--wow",
        type=float,
        default=0.35,
        help="Wow & flutter intensity multiplier (default: 0.35).",
    )
    parser.add_argument(
        "--clicks",
        action="store_true",
        help="Include mechanical tape play/stop button clicks (default: False).",
    )
    parser.add_argument(
        "--bitrate",
        default="128k",
        help="MP3/AAC output bitrate (default: 128k).",
    )
    parser.add_argument(
        "--repo-root",
        default="/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine",
        help="Path to retro_arg_engine repository for resolving stardust-archive.net URLs and mirror copies.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Parallel worker count for batch processing (default: 4).",
    )
    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    jobs = []  # list of (primary_path, mirror_paths)
    html_embed_groups = []

    def add_repo_rel_audio(rel_url: str):
        rel = rel_url.lstrip("/").split("?")[0]
        candidates = [
            os.path.join(repo_root, rel),
            os.path.join(repo_root, "src", "site_static", rel),
            os.path.join(repo_root, "site", rel),
        ]
        # Also check if /forensics/xyz.mp3 maps to assets/audio/forensics/xyz.mp3
        if rel.startswith("forensics/"):
            alt_rel = os.path.join("assets", "audio", rel)
            candidates.extend([
                os.path.join(repo_root, alt_rel),
                os.path.join(repo_root, "src", "site_static", alt_rel),
                os.path.join(repo_root, "site", alt_rel),
            ])
        elif rel.startswith("assets/audio/forensics/"):
            alt_rel = rel[len("assets/audio/"):]
            candidates.extend([
                os.path.join(repo_root, alt_rel),
                os.path.join(repo_root, "src", "site_static", alt_rel),
                os.path.join(repo_root, "site", alt_rel),
            ])
        existing = []
        for c in candidates:
            c_abs = os.path.abspath(c)
            if os.path.exists(c_abs) and c_abs not in existing:
                existing.append(c_abs)
        if existing:
            jobs.append((existing[0], existing[1:]))

    for target in args.targets:
        if target.startswith("http://") or target.startswith("https://"):
            parsed = urllib.parse.urlparse(target)
            if any(
                 parsed.path.lower().endswith(ext)
                for ext in (".mp3", ".wav", ".ogg", ".m4a", ".aac")
            ):
                if "stardust-archive.net" in parsed.netloc or "github.io" in parsed.netloc:
                    add_repo_rel_audio(parsed.path)
                else:
                    out_file = args.output or os.path.basename(parsed.path)
                    req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=30) as resp, open(out_file, "wb") as f:
                        f.write(resp.read())
                    jobs.append((os.path.abspath(out_file), []))
            else:
                # Web page URL (e.g. https://stardust-archive.net/terminal)
                page_path = parsed.path.strip("/")
                local_htmls = []
                if page_path:
                    for cand in [
                        os.path.join(repo_root, "site", page_path, "index.html"),
                        os.path.join(repo_root, "src", "site_static", page_path, "index.html"),
                        os.path.join(repo_root, "site", page_path),
                        os.path.join(repo_root, "src", "site_static", page_path),
                    ]:
                        if os.path.isfile(cand) and cand not in local_htmls:
                            local_htmls.append(cand)
                    if page_path == "terminal":
                        for extra_cand in [
                            os.path.join(repo_root, "site", "forensics", "index.html"),
                            os.path.join(repo_root, "src", "site_static", "forensics", "index.html"),
                            os.path.join(repo_root, "deploy", "terminal_html.js"),
                        ]:
                            if os.path.isfile(extra_cand) and extra_cand not in local_htmls:
                                local_htmls.append(extra_cand)
                if local_htmls:
                    with open(local_htmls[0], "r", encoding="utf-8") as f:
                        html_text = f.read()
                    html_embed_groups.append(local_htmls)
                else:
                    req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"})
                    html_text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="ignore")
                found_urls = sorted(set(re.findall(r'["\'](/[^"\']+\.(?:mp3|wav|ogg))["\']', html_text)))
                for u in found_urls:
                    add_repo_rel_audio(u)
        elif os.path.isdir(target):
            for root_dir, _, files in os.walk(target):
                for fn in sorted(files):
                    if fn.lower().endswith((".mp3", ".wav", ".ogg", ".m4a", ".aac")):
                        jobs.append((os.path.abspath(os.path.join(root_dir, fn)), []))
        elif os.path.isfile(target):
            if target.lower().endswith((".html", ".htm", ".js")):
                with open(target, "r", encoding="utf-8") as f:
                    html_text = f.read()
                html_embed_groups.append([os.path.abspath(target)])
                found_urls = sorted(set(re.findall(r'["\'](/[^"\']+\.(?:mp3|wav|ogg))["\']', html_text)))
                for u in found_urls:
                    add_repo_rel_audio(u)
            else:
                # Check if target is inside repo_root and has mirror copies
                abs_t = os.path.abspath(target)
                if abs_t.startswith(repo_root) and not args.output:
                    rel = os.path.relpath(abs_t, repo_root)
                    for prefix in ("site/", "src/site_static/"):
                        if rel.startswith(prefix):
                            rel = rel[len(prefix):]
                            break
                    add_repo_rel_audio(rel)
                else:
                    jobs.append((abs_t, []))
        else:
            add_repo_rel_audio(target)

    # Deduplicate jobs by canonical set of file paths
    unique_jobs = []
    seen_paths = set()
    for primary, mirrors in jobs:
        all_p = tuple(sorted({primary, *mirrors}))
        if all_p[0] not in seen_paths:
            for p in all_p:
                seen_paths.add(p)
            unique_jobs.append((primary, mirrors))

    print(f"[audio-analog] Processing {len(unique_jobs)} unique audio track(s) (wow={args.wow}, clicks={args.clicks})...", flush=True)

    def _run_one(job):
        primary, mirrors = job
        out_p = args.output if (args.output and len(unique_jobs) == 1) else None
        md5_hex = process_audio_file(
            primary,
            output_path=out_p,
            wow_scale=args.wow,
            add_clicks=args.clicks,
            bitrate=args.bitrate,
            extra_mirror_paths=mirrors,
        )
        return primary, len(mirrors) + 1, md5_hex

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(_run_one, j) for j in unique_jobs]
        for idx, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            prim, n_copies, md5_hex = fut.result()
            print(
                f"  [{idx}/{len(unique_jobs)}] {os.path.basename(prim)} -> MD5 {md5_hex} ({n_copies} copies synced)",
                flush=True,
            )

    for grp in html_embed_groups:
        n_emb = process_embedded_base64_in_html(grp, wow_scale=args.wow, add_clicks=args.clicks)
        if n_emb:
            print(f"[audio-analog] Updated {n_emb} embedded base64 MP3 blob(s) in {[os.path.basename(p) for p in grp]}", flush=True)


if __name__ == "__main__":
    main()
