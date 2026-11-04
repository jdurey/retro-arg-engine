#!/usr/bin/env python3
"""
Encodes a clean, headerless 128kbps CBR 44.1kHz stereo MP3 rotation of Nova Hart's
top crowd-proven English hits + verified ElevenLabs 82.5 FM DJ intros into
`site/assets/audio/radio825/` (and `src/site_static/assets/audio/radio825/`),
strips any ID3v1/ID3v2/Xing tags so 100% of bytes are pure MPEG-1 Layer 3 frames,
and generates `deploy/radio_stream_edge.js` for the 24/7 Icecast-compatible stream
at `https://stardust-archive.net/stream/825fm.mp3` (+ `/825fm.m3u` & `/825fm.pls`).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_OUT = ROOT / "site" / "assets" / "audio" / "radio825"
STATIC_OUT = ROOT / "src" / "site_static" / "assets" / "audio" / "radio825"
EDGE_JS_OUT = ROOT / "deploy" / "radio_stream_edge.js"

ROTATION_SOURCES = [
    (
        "01_dj_intro_chrome_river.mp3",
        "82.5 FM Live DJ — Chrome River Intro",
        ROOT / "youtube/livestream/broadcast_archive/dj_intros/dj_intro_radio_chrome_river.mp3",
    ),
    (
        "02_chrome_river.mp3",
        "Nova Hart - Chrome River",
        ROOT / "youtube/livestream/broadcast_archive/radio_master_songs/radio_chrome_river.mp3",
    ),
    (
        "03_the_stars_in_your_hands.mp3",
        "Nova Hart - The Stars in Your Hands",
        ROOT / "youtube/livestream/broadcast_archive/radio_master_songs/radio_the_stars_in_your_hands.mp3",
    ),
    (
        "04_dj_intro_midnight_animal.mp3",
        "82.5 FM Live DJ — Midnight Animal Intro",
        ROOT / "youtube/livestream/broadcast_archive/dj_intros/dj_intro_radio_midnight_animal.mp3",
    ),
    (
        "05_midnight_animal.mp3",
        "Nova Hart - Midnight Animal",
        ROOT / "anemoia_fm/bandcamp_complete/Static and Steel CD/06 midnight Animal.wav",
    ),
    (
        "06_only_we_remain.mp3",
        "Nova Hart - Only We Remain",
        ROOT / "anemoia_fm/bandcamp_complete/Through the Wires/03 Only We Remain.wav",
    ),
    (
        "07_iron_claws.mp3",
        "Nova Hart - Iron Claws",
        ROOT / "anemoia_fm/bandcamp_complete/Iron Claws EP/Iron Claws.wav",
    ),
    (
        "08_dj_intro_gasoline_heart.mp3",
        "82.5 FM Live DJ — Gasoline Heart Intro",
        ROOT / "youtube/livestream/broadcast_archive/dj_intros/dj_intro_radio_gasoline_heart.mp3",
    ),
    (
        "09_gasoline_heart.mp3",
        "Nova Hart - Gasoline Heart",
        ROOT / "anemoia_fm/bandcamp_complete/Static and Steel CD/09 Gasoline Heart.wav",
    ),
    (
        "10_dont_just_watch_me_rise.mp3",
        "Nova Hart - Don't Just Watch Me Rise",
        ROOT / "anemoia_fm/bandcamp_complete/Deep Cuts Vol 1 EP/09 DON’T JUST WATCH ME RISE .wav",
    ),
    (
        "11_static_and_steel.mp3",
        "Nova Hart - Static and Steel",
        ROOT / "anemoia_fm/bandcamp_complete/Static and Steel CD/05 Static and Steel.wav",
    ),
    (
        "12_we_are_the_thunder.mp3",
        "Nova Hart - We Are the Thunder",
        ROOT / "anemoia_fm/bandcamp_complete/Static and Steel CD/04 We Are the Thunder.wav",
    ),
    (
        "13_summer_of_85.mp3",
        "Nova Hart - Summer of '85",
        ROOT / "anemoia_fm/bandcamp_complete/Static and Steel CD/10 Summer of '85.wav",
    ),
]


def strip_non_mpeg_headers_and_footers(mp3_path: Path) -> int:
    data = mp3_path.read_bytes()
    # Strip ID3v2 header if present
    if data[:3] == b"ID3" and len(data) >= 10:
        size = (
            ((data[6] & 0x7F) << 21)
            | ((data[7] & 0x7F) << 14)
            | ((data[8] & 0x7F) << 7)
            | (data[9] & 0x7F)
        )
        data = data[10 + size :]
    # Strip ID3v1 128-byte TAG footer if present
    if len(data) > 128 and data[-128:-125] == b"TAG":
        data = data[:-128]
    # Advance to first MPEG-1 Layer 3 sync word (0xFF 0xFB or 0xFF 0xFA)
    start = 0
    for i in range(min(4096, len(data) - 4)):
        if data[i] == 0xFF and data[i + 1] in (0xFB, 0xFA):
            start = i
            break
    clean = data[start:]
    mp3_path.write_bytes(clean)
    return len(clean)


def probe_duration_ms(mp3_path: Path) -> int:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(mp3_path),
        ],
        text=True,
    ).strip()
    return int(round(float(out) * 1000.0))


def main() -> int:
    SITE_OUT.mkdir(parents=True, exist_ok=True)
    STATIC_OUT.mkdir(parents=True, exist_ok=True)

    manifest = []
    total_ms = 0
    total_bytes = 0

    for out_name, title, src in ROTATION_SOURCES:
        if not src.exists():
            raise FileNotFoundError(f"Missing audio source: {src}")
        dst = SITE_OUT / out_name
        subprocess.run(
            [
                "ffmpeg",
                "-nostdin",
                "-y",
                "-i",
                str(src),
                "-vn",
                "-map_metadata",
                "-1",
                "-ac",
                "2",
                "-ar",
                "44100",
                "-c:a",
                "libmp3lame",
                "-b:a",
                "128k",
                "-minrate",
                "128k",
                "-maxrate",
                "128k",
                "-bufsize",
                "256k",
                "-write_xing",
                "0",
                "-id3v2_version",
                "0",
                str(dst),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        byte_len = strip_non_mpeg_headers_and_footers(dst)
        dur_ms = probe_duration_ms(dst)
        shutil.copy2(dst, STATIC_OUT / out_name)

        manifest.append(
            {
                "file": out_name,
                "title": title,
                "duration_ms": dur_ms,
                "bytes": byte_len,
            }
        )
        total_ms += dur_ms
        total_bytes += byte_len
        print(f"  [ENCODED 128k CBR] {out_name} | {dur_ms/1000:.1f}s | {byte_len/1024:.0f} KB | {title}")

    edge_js = f"""// ============================================================================
//  82.5 FM — NOVA HART 24/7 ICECAST-COMPATIBLE HTTP MP3 RADIO STREAM
// ============================================================================
//  Endpoints:
//    - GET / HEAD /stream/825fm.mp3 -> Continuous 128kbps 44.1kHz CBR MP3 stream
//    - GET /825fm.m3u               -> M3U playlist for VLC / iTunes / Radio apps
//    - GET /825fm.pls               -> Shoutcast PLS playlist
//    - GET /api/radio825/now-playing.json -> Live clock-synced track metadata
// ============================================================================

export const RADIO_825_SEGMENTS = {json.dumps(manifest, indent=2)};

export const RADIO_825_TOTAL_MS = {total_ms};

const ICY_HEADERS = {{
  "Content-Type": "audio/mpeg",
  "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
  "Pragma": "no-cache",
  "Access-Control-Allow-Origin": "*",
  "Connection": "keep-alive",
  "icy-name": "82.5 FM - Nova Hart (1989 Arena Rock, Synthwave & Night Drive Radio)",
  "icy-description": "24/7 1985-1989 Melodic Arena Rock, Synthwave, AOR & Power Ballads from Orion Records Studio B2",
  "icy-genre": "80s Rock, Synthwave, AOR, Melodic Rock",
  "icy-br": "128",
  "icy-sr": "44100",
  "icy-pub": "1",
  "icy-url": "https://stardust-archive.net/start",
}};

export function getRadio825NowPlaying(nowMs = Date.now()) {{
  const posMs = ((nowMs % RADIO_825_TOTAL_MS) + RADIO_825_TOTAL_MS) % RADIO_825_TOTAL_MS;
  let acc = 0;
  for (let i = 0; i < RADIO_825_SEGMENTS.length; i++) {{
    const seg = RADIO_825_SEGMENTS[i];
    if (posMs < acc + seg.duration_ms) {{
      const offsetMs = posMs - acc;
      const nextSeg = RADIO_825_SEGMENTS[(i + 1) % RADIO_825_SEGMENTS.length];
      return {{ index: i, segment: seg, offsetMs, nextSegment: nextSeg }};
    }}
    acc += seg.duration_ms;
  }}
  return {{ index: 0, segment: RADIO_825_SEGMENTS[0], offsetMs: 0, nextSegment: RADIO_825_SEGMENTS[1] }};
}}

function findMpegFrameSync(buf, approxOffset) {{
  const start = Math.max(0, Math.min(approxOffset, buf.length - 4));
  // Align to MPEG-1 Layer 3 128kbps 44.1kHz stereo sync word (0xFF 0xFB 0x90 / 0x92)
  for (let i = start; i < buf.length - 4; i++) {{
    if (buf[i] === 0xff && (buf[i + 1] === 0xfb || buf[i + 1] === 0xfa) && (buf[i + 2] & 0xf0) === 0x90) {{
      return i;
    }}
  }}
  return 0;
}}

export async function handleRadio825Request(request, url, baseStaticUrl = "https://jdurey.github.io/retro-arg-engine") {{
  const cleanPath = url.pathname.replace(/\\/+$/, "") || "/";
  const apex = url.hostname || "stardust-archive.net";

  if (cleanPath === "/825fm.m3u" || cleanPath === "/radio.m3u") {{
    const body = `#EXTM3U\\n#EXTINF:-1,82.5 FM - Nova Hart (1989 Arena Rock, Synthwave & Night Drive Radio)\\nhttps://${{apex}}/stream/825fm.mp3\\n`;
    return new Response(body, {{
      status: 200,
      headers: {{
        "Content-Type": "audio/x-mpegurl; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "public, max-age=300",
      }},
    }});
  }}

  if (cleanPath === "/825fm.pls" || cleanPath === "/radio.pls") {{
    const body = `[playlist]\\nNumberOfEntries=1\\nFile1=https://${{apex}}/stream/825fm.mp3\\nTitle1=82.5 FM - Nova Hart (1989 Arena Rock, Synthwave & Night Drive Radio)\\nLength1=-1\\nVersion=2\\n`;
    return new Response(body, {{
      status: 200,
      headers: {{
        "Content-Type": "audio/x-scpls; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "public, max-age=300",
      }},
    }});
  }}

  if (cleanPath === "/api/radio825/now-playing.json") {{
    const state = getRadio825NowPlaying();
    return new Response(
      JSON.stringify(
        {{
          station: "82.5 FM - Nova Hart (1989 Arena Rock, Synthwave & Night Drive Radio)",
          stream_mp3_url: `https://${{apex}}/stream/825fm.mp3`,
          playlist_m3u_url: `https://${{apex}}/825fm.m3u`,
          playlist_pls_url: `https://${{apex}}/825fm.pls`,
          youtube_24_7_crt_live: "https://www.youtube.com/@NovaHart_Official/live",
          now_playing: state.segment.title,
          elapsed_sec: Math.round(state.offsetMs / 1000),
          duration_sec: Math.round(state.segment.duration_ms / 1000),
          up_next: state.nextSegment.title,
        }},
        null,
        2
      ),
      {{
        status: 200,
        headers: {{
          "Content-Type": "application/json; charset=utf-8",
          "Access-Control-Allow-Origin": "*",
          "Cache-Control": "no-store",
        }},
      }}
    );
  }}

  if (cleanPath === "/stream/825fm.mp3" || cleanPath === "/stream/825fm" || cleanPath === "/825fm.mp3") {{
    if (request.method === "HEAD") {{
      return new Response(null, {{ status: 200, headers: ICY_HEADERS }});
    }}

    const {{ readable, writable }} = new TransformStream();
    const writer = writable.getWriter();
    const cleanBase = baseStaticUrl.replace(/\\/+$/, "");

    (async () => {{
      try {{
        const startState = getRadio825NowPlaying();
        let idx = startState.index;
        let firstTrackOffsetMs = startState.offsetMs;
        // Stream up to 72 tracks (~4.5 hours per continuous TCP connection; radio players auto-reconnect seamlessly)
        for (let step = 0; step < 72; step++) {{
          const seg = RADIO_825_SEGMENTS[idx];
          const assetUrl = `${{cleanBase}}/assets/audio/radio825/${{seg.file}}`;
          const resp = await fetch(assetUrl, {{
            cf: {{ cacheTtl: 86400, cacheEverything: true }},
          }});
          if (!resp.ok) {{
            break;
          }}
          const buf = new Uint8Array(await resp.arrayBuffer());
          let byteStart = 0;
          if (step === 0 && firstTrackOffsetMs > 2000 && firstTrackOffsetMs < seg.duration_ms - 5000) {{
            const approxBytes = Math.floor((firstTrackOffsetMs / seg.duration_ms) * buf.length);
            byteStart = findMpegFrameSync(buf, approxBytes);
          }}
          // Write in 32KB chunks so TCP backpressure responds cleanly when a listener disconnects
          const CHUNK = 32768;
          for (let off = byteStart; off < buf.length; off += CHUNK) {{
            const slice = buf.subarray(off, Math.min(off + CHUNK, buf.length));
            await writer.write(slice);
          }}
          idx = (idx + 1) % RADIO_825_SEGMENTS.length;
        }}
      }} catch (_err) {{
        // Listener disconnected or stream closed cleanly
      }} finally {{
        try {{
          await writer.close();
        }} catch (_e) {{}}
      }}
    }})();

    return new Response(readable, {{
      status: 200,
      headers: ICY_HEADERS,
    }});
  }}

  return null;
}}
"""
    EDGE_JS_OUT.write_text(edge_js, encoding="utf-8")
    print(
        f"[RADIO 825] Built {len(manifest)} segments ({total_ms/60000:.1f} min, {total_bytes/(1024*1024):.1f} MB) -> {EDGE_JS_OUT}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
