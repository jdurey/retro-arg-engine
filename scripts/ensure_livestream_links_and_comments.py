#!/usr/bin/env python3
"""
Ensures every public VOD on @NovaHart_Official has:
  1. The 24/7 82.5 FM Livestream link on Line 1 of its description (plus a clean /start
     cassette jukebox link on Line 2, stripping legacy GeoCities subdomain & AI-cipher lines
     across both `snippet.description` and all `localizations[lang].description` entries,
     while keeping ALL titles, lyrics, playlists, and shop links 100% untouched).
  2. A @NovaHart_Official top-level comment inviting listeners into the 24/7 82.5 FM radio
     broadcast (updating existing @AnemoiaFM promo comments in-place via `comments.update`
     so already-pinned comments STAY PINNED automatically, or inserting a new comment via
     `commentThreads.insert` when none exists).

Processes videos strictly by `viewCount` descending and persists resumable state in
`youtube/state/livestream_funnel_rollout.json` so daily 10,000-unit YouTube Data API quota
boundaries resume seamlessly until 100% of public videos (and all future uploads) are covered.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ssl._create_default_https_context = ssl._create_unverified_context

ROOT = Path(__file__).resolve().parents[1]
TOKEN_PATH = ROOT / "youtube" / "token.json"
VIDEOS_JSON_PATH = ROOT / "youtube" / "state" / "videos.json"
STATE_PATH = ROOT / "youtube" / "state" / "livestream_funnel_rollout.json"
BACKUP_PATH = ROOT / "youtube" / "state" / "pre_livestream_funnel_backup.json"

CHANNEL_ID = "UCQ2nHAazpB_HIiiQCPqFm1w"
DEFAULT_LIVE_ID = "KLKLgb67ggg"
START_URL = "https://stardust-archive.net/start"

LOCALIZED_HEADERS: dict[str, tuple[str, str]] = {
    "en": (
        "🔴 Listen Live 24/7 — 80s Night Flight Radio Broadcast (82.5 FM • Rock, Synthwave & Live DJ Requests): {live_url}",
        "🎧 5-Track 1989 Studio Cassette Jukebox (Zero Ads): {start_url}",
    ),
    "es": (
        "🔴 Escucha en Vivo 24/7 — Radio Rock de los 80, Synthwave y Night Drive (82.5 FM • DJ en Vivo y Pedidos): {live_url}",
        "🎧 Tocadiscos de Casetes de Estudio 1989 (Sin Anuncios): {start_url}",
    ),
    "fr": (
        "🔴 Écoutez en Direct 24/7 — Radio Rock 80s, Synthwave & Night Drive (82.5 FM • DJ en Direct & Dédicaces) : {live_url}",
        "🎧 Jukebox Cassette Studio 1989 (Sans Pub) : {start_url}",
    ),
    "de": (
        "🔴 24/7 Live Hören — 80er Rock, Synthwave & Night Drive Radio (82.5 FM • Live-DJ & Musikwünsche): {live_url}",
        "🎧 1989 Studio-Kassetten-Jukebox (Ohne Werbung): {start_url}",
    ),
    "it": (
        "🔴 Ascolta dal Vivo 24/7 — Radio Rock Anni '80, Synthwave & Night Drive (82.5 FM • DJ Live e Richieste): {live_url}",
        "🎧 Jukebox su Cassetta Studio 1989 (Zero Pubblicità): {start_url}",
    ),
    "pt": (
        "🔴 Ouça ao Vivo 24/7 — Rádio Rock Anos 80, Synthwave & Night Drive (82.5 FM • DJ ao Vivo e Pedidos): {live_url}",
        "🎧 Jukebox de Fitas Cassete de Estúdio 1989 (Sem Anúncios): {start_url}",
    ),
    "nl": (
        "🔴 Luister 24/7 Live — Jaren 80 Rock, Synthwave & Night Drive Radio (82.5 FM • Live DJ & Verzoeknummers): {live_url}",
        "🎧 1989 Studio Cassette Jukebox (Zonder Reclame): {start_url}",
    ),
    "pl": (
        "🔴 Słuchaj na Żywo 24/7 — Radio Rock Lat 80., Synthwave & Night Drive (82.5 FM • Live DJ i Piosenki na Życzenie): {live_url}",
        "🎧 Szafa Grająca z Kasetami Studyjnymi 1989 (Bez Reklam): {start_url}",
    ),
    "ru": (
        "🔴 Слушать в прямом эфире 24/7 — Рок 80-х, Синтвейв и Ночное Радио (82.5 FM • Живой DJ и Заказ Песен): {live_url}",
        "🎧 Студийный кассетный плеер 1989 года (без рекламы): {start_url}",
    ),
    "uk": (
        "🔴 Слухати наживо 24/7 — Рок 80-х, Синтвейв та Нічне Радіо (82.5 FM • Наживо DJ і Замовлення Пісень): {live_url}",
        "🎧 Студійний касетний плеєр 1989 року (без реклами): {start_url}",
    ),
    "tr": (
        "🔴 7/24 Canlı Dinle — 80'ler Rock, Synthwave & Gece Sürüşü Radyosu (82.5 FM • Canlı DJ ve İstek Parçalar): {live_url}",
        "🎧 1989 Stüdyo Kaset Müzik Kutusu (Reklamsız): {start_url}",
    ),
    "ar": (
        "🔴 استمع مباشرة 24/7 — راديو روك الثمانينات وسينثويف (82.5 FM • دي جي مباشر وطلبات الأغاني): {live_url}",
        "🎧 مشغل كاسيت استوديو 1989 (بدون إعلانات): {start_url}",
    ),
    "hi": (
        "🔴 24/7 लाइव सुनें — 80s रॉक, सिंथवेव और नाइट ड्राइव रेडियो (82.5 FM • लाइव DJ और गानों की फरमाइश): {live_url}",
        "🎧 1989 स्टूडियो कैसेट ज्यूकबॉक्स (बिना विज्ञापन): {start_url}",
    ),
    "id": (
        "🔴 Dengarkan Live 24/7 — Radio Rock 80-an, Synthwave & Night Drive (82.5 FM • Live DJ & Request Lagu): {live_url}",
        "🎧 Jukebox Kaset Studio 1989 (Tanpa Iklan): {start_url}",
    ),
    "vi": (
        "🔴 Nghe Trực Tiếp 24/7 — Radio Rock Thập Niên 80, Synthwave & Đêm Khuya (82.5 FM • DJ Trực Tiếp & Yêu Cầu Nhạc): {live_url}",
        "🎧 Máy Nghe Băng Cassette Phòng Thu 1989 (Không Quảng Cáo): {start_url}",
    ),
    "th": (
        "🔴 ฟังสด 24/7 — วิทยุร็อกยุค 80, ซินธ์เวฟ & ไนท์ไดรฟ์ (82.5 FM • ดีเจสด & ขอเพลงได้ในแชท): {live_url}",
        "🎧 ตู้เพลงเทปคาสเซ็ทสตูดิโอปี 1989 (ไม่มีโฆษณา): {start_url}",
    ),
    "ja": (
        "🔴 24時間ライブ配信中 — 80年代ロック・シンセウェイヴ＆ナイトドライブ・ラジオ (82.5 FM • ライブDJ＆曲リクエスト受付中): {live_url}",
        "🎧 1989年スタジオ・カセット・ジュークボックス（広告なし）: {start_url}",
    ),
    "ko": (
        "🔴 24시간 실시간 라디오 — 80년대 록, 신스웨이브 & 나이트 드라이브 라디오 (82.5 FM • 라이브 DJ & 신청곡 접수): {live_url}",
        "🎧 1989 스튜디오 카세트 주크박스 (광고 없음): {start_url}",
    ),
    "zh-CN": (
        "🔴 24/7 全天候直播电台 — 80年代摇滚、合成器浪潮与夜驾电台 (82.5 FM • 现场DJ与点歌互动): {live_url}",
        "🎧 1989 录音室磁带点唱机（无广告）: {start_url}",
    ),
    "zh-TW": (
        "🔴 24/7 全天候直播電台 — 80年代搖滾、合成器浪潮與夜駕電台 (82.5 FM • 現場DJ與點歌互動): {live_url}",
        "🎧 1989 錄音室卡帶點唱機（無廣告）: {start_url}",
    ),
}

STRIP_LINE_PREFIXES = (
    "Someone kept the old webring online",
    "5,000 homepages.",
    "Alguien mantuvo en línea",
    "5.000 páginas",
    "Quelqu'un a gardé",
    "5 000 pages",
    "Jemand hat den alten Webring",
    "5.000 Homepages",
    "Qualcuno ha tenuto",
    "Iemand heeft de oude webring",
    "Ktoś utrzymał stary",
    "5000 stron",
    "Кто-то сохранил старый",
    "5000 домашних",
    "Хтось зберіг старий",
    "5000 домашніх",
    "Biri eski webring",
    "5.000 kişisel",
    "أحدهم أبقى",
    "5000 صفحة",
    "किसी ने पुरानी वेबरिंग",
    "5,000 होमपेज",
    "Seseorang menjaga webring",
    "Ai đó vẫn giữ webring",
    "5.000 trang",
    "มีใครบางคนยังเปิดเว็บริง",
    "โฮมเพจ 5,000",
    "誰かが、古いウェブリング",
    "5,000のホームページ",
    "누군가 오래된 웹링",
    "홈페이지 5,000개",
    "有人一直让那个旧网络环",
    "有人一直讓那個舊網路環",
    "5000 个个人主页",
    "5000 個個人首頁",
    "Alguém manteve o velho",
    "▶ Web Ring",
    "▶ Dedicated 1995",
    "▶ Nodo GeoCities",
    "▶ Nœud GeoCities",
    "▶ 1995 GeoCities",
    "▶ Węzeł GeoCities",
    "▶ Узел GeoCities",
    "▶ Вузол GeoCities",
    "▶ عقدة GeoCities",
    "▶ Node GeoCities",
    "▶ Nút GeoCities",
    "▶ โหนด GeoCities",
    "▶ 専用1995年GeoCities",
    "▶ 1995 지오시티",
    "▶ 1995 GeoCities专属",
    "▶ 1995 GeoCities專屬",
    "▶ Nó GeoCities",
    "⚡ ",
    "🧀 ",
    "📖 ",
    "📼 ",
    "📡 ",
    "🔴 ",
    "📻 ",
    "🕹️ ",
    "🌐 ",
    "🧠 ",
    "🎧 THE SIGNAL:",
    "[Declassified 1983-1989 Sublevel B2",
)

STRIP_SUBSTRINGS_LOWER = (
    "/ai-benchmark",
    "stardust-archive.net/ai",
    "stardust-archive.net/start",
    "stardust-archive.net/terminal",
    "stardust-archive.net/experiment",
    "stardust-archive.net/api/",
    "stardust-archive.net/dyad",
    ".stardust-archive.net/~",
    "geocities-",
    "stardust-archive.net/go/youtube",
    "@novahart_official/live",
    "reddit.com/r/novahart",
    "rick's nova hart shrine",
)


def build_pinned_comment_text(live_url: str) -> str:
    return (
        "📻 Loving this sound? Come hang out on the 24/7 82.5 FM Night Flight Radio broadcast "
        "— spinning nonstop 80s rock, synthwave & power ballads with live DJ breaks and song requests in chat:\n"
        f"🔴 Listen Live: {live_url}"
    )


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class QuotaExceededError(RuntimeError):
    pass


def get_access_token() -> str:
    tok = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    payload = urllib.parse.urlencode(
        {
            "client_id": tok["client_id"],
            "client_secret": tok["client_secret"],
            "refresh_token": tok["refresh_token"],
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        tok.get("token_uri", "https://oauth2.googleapis.com/token"),
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))["access_token"]


def yt_api(
    access_token: str,
    path_and_query: str,
    method: str = "GET",
    body: dict | None = None,
) -> dict:
    url = f"https://www.googleapis.com/youtube/v3/{path_and_query}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    for attempt in range(3):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                return json.loads(raw) if raw.strip() else {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            if e.code == 403 and "quota" in err_body.lower():
                raise QuotaExceededError(err_body)
            if e.code in (400, 403, 404) and ("commentsDisabled" in err_body or "forbidden" in err_body.lower()):
                return {"_http_error": e.code, "_error_body": err_body}
            if attempt == 2:
                raise RuntimeError(f"YouTube HTTP {e.code} on {method} {path_and_query}: {err_body[:400]}")
            time.sleep(1.5 * (attempt + 1))
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))
    return {}


def resolve_active_live_video_id(access_token: str) -> str:
    try:
        res = yt_api(
            access_token,
            "liveBroadcasts?part=id,snippet,status&broadcastStatus=active&maxResults=10",
        )
        for item in res.get("items") or []:
            st = item.get("status") or {}
            if st.get("privacyStatus") == "public" and st.get("lifeCycleStatus") == "live":
                return item["id"]
    except Exception:
        pass
    return DEFAULT_LIVE_ID


def transform_description(raw_desc: str, lang: str, live_url: str) -> str:
    line1_tpl, line2_tpl = LOCALIZED_HEADERS.get(lang, LOCALIZED_HEADERS["en"])
    shop_line = "💿 Official Digital Albums & Merch (20% Off Code LIVE): https://nova-hart-shop.fourthwall.com/promo/LIVE"
    header_block = f"{line1_tpl.format(live_url=live_url)}\n{line2_tpl.format(start_url=START_URL)}"

    # Replace dead Bandcamp links (post-Jan 2026 AI ban) & stale DSP IDs in-place
    repaired_raw = re.sub(
        r"https?://[a-z0-9\-]*\.?bandcamp\.com[^\s\)\]>\"']*",
        "https://nova-hart-shop.fourthwall.com/collections/all",
        raw_desc or "",
        flags=re.I,
    )
    repaired_raw = re.sub(r"\bBandcamp\b", "Official Album Store", repaired_raw, flags=re.I)
    repaired_raw = repaired_raw.replace("6P26L21YnF8L0QnJ46rO3m", "0zElHuJrzKbq0XjqK3HyYr")
    repaired_raw = repaired_raw.replace("1823348141", "1681398544")

    lines = repaired_raw.splitlines()
    promo_top_lines: list[str] = []
    body_lines: list[str] = []
    in_promo_offer = False

    for idx, ln in enumerate(lines):
        s = ln.strip()
        low = s.lower()

        # Keep Fourthwall 20%-off promo offer lines intact on TV-offer Shorts
        if idx == 0 and low.startswith("get 20% off"):
            in_promo_offer = True
            promo_top_lines.append(ln)
            continue
        if in_promo_offer:
            promo_top_lines.append(ln)
            if s.startswith("http") or not s:
                in_promo_offer = False
            continue

        if s.startswith("💿 "):
            continue
        if any(s.startswith(p) for p in STRIP_LINE_PREFIXES):
            continue
        if any(sub in low for sub in STRIP_SUBSTRINGS_LOWER):
            continue
        # Remove "#GeoCities" hashtag while keeping music hashtags intact
        if "#geocities" in low:
            ln = re.sub(r"\s*#GeoCities\b", "", ln, flags=re.I)
            if not ln.strip():
                continue

        body_lines.append(ln)

    # Collapse leading/trailing blank lines & excessive dividers at the very start
    body_text = "\n".join(body_lines).strip()
    body_text = re.sub(r"^-{5,}\s*\n+", "", body_text).strip()
    body_text = re.sub(r"\n{4,}", "\n\n\n", body_text)

    if "fourthwall.com" not in body_text.lower() and not promo_top_lines:
        header_block = f"{header_block}\n{shop_line}"

    if promo_top_lines:
        promo_block = "\n".join(promo_top_lines).strip()
        combined = f"{promo_block}\n\n{header_block}\n\n{body_text}".strip()
    elif body_text:
        combined = f"{header_block}\n\n{body_text}".strip()
    else:
        combined = header_block

    return combined[:4950]


def description_already_clean(desc: str, live_id: str) -> bool:
    if not desc:
        return False
    top_chunk = "\n".join(desc.splitlines()[:6])
    if live_id not in top_chunk:
        return False
    low = desc.lower()
    if (
        "/ai-benchmark" in low
        or ".stardust-archive.net/~" in low
        or "geocities-" in low
        or "bandcamp.com" in low
        or "6p26l21ynf8l0qnj46ro3m" in low
        or "1823348141" in low
    ):
        return False
    return True


def fetch_all_channel_video_ids(access_token: str) -> list[str]:
    ch = yt_api(access_token, f"channels?part=contentDetails&id={CHANNEL_ID}")
    uploads_pl = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids: list[str] = []
    seen: set[str] = set()
    page_token = None
    while True:
        q = f"playlistItems?part=contentDetails&playlistId={uploads_pl}&maxResults=50"
        if page_token:
            q += f"&pageToken={urllib.parse.quote(page_token)}"
        res = yt_api(access_token, q)
        for it in res.get("items") or []:
            vid = (it.get("contentDetails") or {}).get("videoId")
            if vid and vid not in seen:
                seen.add(vid)
                ids.append(vid)
        page_token = res.get("nextPageToken")
        if not page_token:
            break

    if VIDEOS_JSON_PATH.exists():
        try:
            cached = json.loads(VIDEOS_JSON_PATH.read_text(encoding="utf-8")).get("videos") or []
            for v in cached:
                vid = v.get("id")
                if vid and vid not in seen:
                    seen.add(vid)
                    ids.append(vid)
        except Exception:
            pass
    return ids


def fetch_live_video_records(access_token: str, video_ids: list[str]) -> list[dict]:
    records: list[dict] = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        q = "videos?part=snippet,localizations,status,statistics,liveStreamingDetails&id=" + ",".join(batch)
        res = yt_api(access_token, q)
        records.extend(res.get("items") or [])
    return records


def load_json_file(path: Path, default: dict) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return dict(default)
    return dict(default)


def save_json_file(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.json")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def is_replaceable_promo_comment(text: str) -> bool:
    low = (text or "").lower()
    return any(
        marker in low
        for marker in (
            "no vocals. just vibes",
            "anemoiafm",
            "anemoia_fm",
            "studying or gaming? check out",
            "ai-benchmark",
            "82.5 fm night drive radio",
            "listen live:",
        )
    )


def ensure_video_comment(
    access_token: str,
    vid: str,
    live_id: str,
    live_url: str,
    backup_entry: dict,
    dry_run: bool = False,
) -> dict:
    target_text = build_pinned_comment_text(live_url)
    res = yt_api(
        access_token,
        f"commentThreads?part=snippet&videoId={vid}&maxResults=30&order=relevance",
    )
    if res.get("_http_error"):
        return {
            "status": "comments_disabled_or_forbidden",
            "detail": res.get("_error_body", "")[:160],
        }

    items = res.get("items") or []
    existing_live_comment = None
    replaceable_owner_comment = None

    for rank_idx, it in enumerate(items):
        top = (it.get("snippet") or {}).get("topLevelComment") or {}
        cid = top.get("id")
        sn = top.get("snippet") or {}
        author_ch = (sn.get("authorChannelId") or {}).get("value", "")
        txt = sn.get("textOriginal") or sn.get("textDisplay") or ""
        if author_ch != CHANNEL_ID:
            continue

        if live_id in txt or ("82.5 fm" in txt.lower() and "http" in txt.lower()):
            existing_live_comment = {"comment_id": cid, "rank": rank_idx, "text": txt}
            break
        if replaceable_owner_comment is None and is_replaceable_promo_comment(txt):
            replaceable_owner_comment = {"comment_id": cid, "rank": rank_idx, "text": txt}

    if existing_live_comment:
        return {
            "status": "already_present",
            "action": "none",
            "comment_id": existing_live_comment["comment_id"],
            "relevance_rank": existing_live_comment["rank"],
            "likely_pinned": existing_live_comment["rank"] == 0,
        }

    if replaceable_owner_comment:
        cid = replaceable_owner_comment["comment_id"]
        was_rank0 = replaceable_owner_comment["rank"] == 0
        if dry_run:
            return {
                "status": "dry_run_update_in_place",
                "comment_id": cid,
                "was_rank0_pinned": was_rank0,
            }
        backup_entry.setdefault("original_replaced_comment", replaceable_owner_comment)
        upd = yt_api(
            access_token,
            "comments?part=snippet",
            method="PUT",
            body={
                "id": cid,
                "snippet": {
                    "textOriginal": target_text,
                },
            },
        )
        return {
            "status": "updated_in_place",
            "action": "comments.update",
            "comment_id": upd.get("id", cid),
            "was_rank0_pinned": was_rank0,
            "needs_studio_pin": not was_rank0,
        }

    if dry_run:
        return {"status": "dry_run_insert_new", "needs_studio_pin": True}

    ins = yt_api(
        access_token,
        "commentThreads?part=snippet",
        method="POST",
        body={
            "snippet": {
                "videoId": vid,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": target_text,
                    }
                },
            }
        },
    )
    if ins.get("_http_error"):
        return {
            "status": "insert_failed",
            "detail": ins.get("_error_body", "")[:160],
        }
    new_cid = ((ins.get("snippet") or {}).get("topLevelComment") or {}).get("id") or ins.get("id")
    return {
        "status": "inserted_new",
        "action": "commentThreads.insert",
        "comment_id": new_cid,
        "was_rank0_pinned": False,
        "needs_studio_pin": True,
    }


def pin_pending_comments_via_studio_mcp(state: dict, max_pins: int = 0) -> dict:
    """
    Uses the local thread-safe Chrome MCP bridge (`127.0.0.1:19897`) when online to click
    `Action menu -> Pin -> Pin` in YouTube Studio (`0` YouTube Data API quota units!).
    Opens a single background tab and closes it cleanly in `finally` so user tabs stay untouched.
    """
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open("http://127.0.0.1:19897/health", timeout=2.0) as h_resp:
            if h_resp.status != 200:
                return {"online": False, "pinned": 0}
    except Exception:
        return {"online": False, "pinned": 0}

    livestream_dir = ROOT / "youtube" / "livestream"
    if str(livestream_dir) not in sys.path:
        sys.path.insert(0, str(livestream_dir))
    try:
        import nova_sovereign_daemon as nsd  # type: ignore
        mcp = nsd.ProxiedMCPClient("http://127.0.0.1:19897")
    except Exception as exc:
        return {"online": False, "pinned": 0, "error": str(exc)}

    pending: list[tuple[int, str, dict]] = []
    for vid, v_state in (state.get("videos") or {}).items():
        if isinstance(v_state, dict) and v_state.get("comment_done") and v_state.get("needs_studio_pin"):
            pending.append((int(v_state.get("viewCount") or 0), vid, v_state))
    pending.sort(key=lambda x: x[0], reverse=True)
    if max_pins > 0:
        pending = pending[:max_pins]
    if not pending:
        return {"online": True, "pinned": 0, "remaining_unpinned": 0}

    flt_json = json.dumps(
        [{"isDisabled": False, "isPinned": True, "name": "SORT_BY", "value": "SORT_BY_NEWEST"}]
    )
    flt_q = urllib.parse.quote(flt_json)

    temp_pid: int | None = None
    prev_selected_pid: int | None = None
    pinned_count = 0
    failed_ids: list[str] = []

    try:
        try:
            lp_out = mcp.call_tool("list_pages", {})
            m_sel = re.search(r"^(\d+):.*\[selected\]", lp_out, re.M)
            if m_sel:
                prev_selected_pid = int(m_sel.group(1))
        except Exception:
            pass

        def _open_active_tab(target_url: str) -> int:
            out_new = mcp.call_tool("new_page", {"url": target_url, "background": False})
            m_ids = re.findall(r"^(\d+):", out_new, re.M)
            if not m_ids:
                raise RuntimeError("could_not_parse_page_id")
            return int(m_ids[-1])

        first_vid = pending[0][1]
        first_url = f"https://studio.youtube.com/video/{first_vid}/comments/inbox?filter={flt_q}"
        temp_pid = _open_active_tab(first_url)

        for idx, (vc, vid, v_state) in enumerate(pending, start=1):
            studio_url = f"https://studio.youtube.com/video/{vid}/comments/inbox?filter={flt_q}"
            try:
                if idx > 1:
                    mcp.call_tool("select_page", {"pageId": temp_pid})
                    mcp.call_tool("navigate_page", {"pageId": temp_pid, "type": "url", "url": studio_url})
                else:
                    mcp.call_tool("select_page", {"pageId": temp_pid})
            except Exception:
                temp_pid = _open_active_tab(studio_url)
            time.sleep(3.2)

            try:
                res = mcp.eval_json(
                    temp_pid,
                    """async () => {
                      const sleep = ms => new Promise(r => setTimeout(r, ms));
                      for (let waitIdx = 0; waitIdx < 10; waitIdx++) {
                        if (document.querySelectorAll("ytcp-comment-thread").length > 0) break;
                        await sleep(500);
                      }
                      const threads = Array.from(document.querySelectorAll("ytcp-comment-thread"));
                      const target = threads.find(t => {
                        const txt = t.innerText || "";
                        return txt.includes("@NovaHart_Official") && (txt.includes("82.5 FM") || txt.includes("Listen Live"));
                      });
                      if (!target) return {ok: false, step: "not_in_studio_newest", thread_count: threads.length};
                      if ((target.innerText || "").toLowerCase().includes("pinned by")) {
                        return {ok: true, already_pinned: true};
                      }
                      const menuBtn = target.querySelector("#action-menu-button button, #action-menu-button");
                      if (!menuBtn) return {ok: false, step: "menu_btn"};
                      menuBtn.click();
                      await sleep(500);
                      const items = Array.from(document.querySelectorAll("tp-yt-paper-item, ytcp-text-menu-item, [role=menuitem]"));
                      const pinItem = items.find(el => el.offsetParent !== null && /^pin$/i.test((el.innerText || "").trim()));
                      if (!pinItem) return {ok: false, step: "pin_item"};
                      pinItem.click();
                      await sleep(600);
                      const dlgBtns = Array.from(document.querySelectorAll("ytcp-confirmation-dialog #confirm-button button, ytcp-confirmation-dialog #confirm-button, ytcp-button#confirm-button button"));
                      const confirmBtn = dlgBtns.find(b => b.offsetParent !== null) || dlgBtns[0];
                      if (confirmBtn) {
                        confirmBtn.click();
                      }
                      for (let pIdx = 0; pIdx < 9; pIdx++) {
                        await sleep(500);
                        if ((target.innerText || "").toLowerCase().includes("pinned")) {
                          return {ok: true, pinned_text_seen: true};
                        }
                      }
                      return {ok: Boolean(confirmBtn), confirmed_without_label: Boolean(confirmBtn)};
                    }""",
                )
            except Exception as eval_exc:
                res = {"ok": False, "error": str(eval_exc)}

            # Fallback for older edited owner comments via Watch `&lc=<comment_id>` using trusted CDP click
            if not (isinstance(res, dict) and res.get("ok")) and v_state.get("comment_id"):
                cid = v_state["comment_id"]
                watch_url = f"https://www.youtube.com/watch?v={vid}&lc={urllib.parse.quote(str(cid))}"
                try:
                    mcp.call_tool("select_page", {"pageId": temp_pid})
                    mcp.call_tool("navigate_page", {"pageId": temp_pid, "type": "url", "url": watch_url})
                    time.sleep(4.2)
                    mcp.eval_json(
                        temp_pid,
                        """async () => {
                          const v = document.querySelector("video");
                          if (v) v.pause();
                          window.scrollTo(0, 650);
                          await new Promise(r => setTimeout(r, 1800));
                        }""",
                    )
                    snap1 = mcp.call_tool("take_snapshot", {"pageId": temp_pid})
                    if "Pinned by @NovaHart_Official" in snap1:
                        res = {"ok": True, "already_pinned": True, "via": "watch_lc"}
                    else:
                        s_lines = snap1.splitlines()
                        menu_uid = None
                        for i_ln, ln_s in enumerate(s_lines):
                            if "82.5 FM" in ln_s or "Loving this sound" in ln_s:
                                for j_ln in range(i_ln, min(len(s_lines), i_ln + 25)):
                                    m_u = re.search(r"uid=(\S+).*button.*(?:Action menu|More actions)", s_lines[j_ln], re.I)
                                    if m_u:
                                        menu_uid = m_u.group(1)
                                        break
                                if menu_uid:
                                    break
                        if menu_uid:
                            mcp.call_tool("click", {"pageId": temp_pid, "uid": menu_uid})
                            time.sleep(0.8)
                            snap2 = mcp.call_tool("take_snapshot", {"pageId": temp_pid})
                            m_p = re.search(r"uid=(\S+).*(?:menuitem|link|button)\s+\"Pin\"", snap2)
                            if m_p:
                                mcp.call_tool("click", {"pageId": temp_pid, "uid": m_p.group(1)})
                                time.sleep(0.9)
                                snap3 = mcp.call_tool("take_snapshot", {"pageId": temp_pid})
                                m_c = re.findall(r"uid=(\S+).*button\s+\"Pin\"", snap3)
                                if m_c:
                                    mcp.call_tool("click", {"pageId": temp_pid, "uid": m_c[-1]})
                                    time.sleep(1.8)
                                    chk = str(
                                        mcp.eval_json(
                                            temp_pid,
                                            "() => (document.querySelector('ytd-comment-thread-renderer')?.innerText || '').slice(0, 180)",
                                        )
                                    )
                                    res = {"ok": "pinned" in chk.lower(), "via": "watch_lc_cdp"}
                except Exception as w_exc:
                    res = {"ok": False, "watch_error": str(w_exc)}

            if isinstance(res, dict) and res.get("ok"):
                v_state["likely_pinned"] = True
                v_state["needs_studio_pin"] = False
                v_state["pinned_at"] = utc_now()
                pinned_count += 1
                print(f"  [STUDIO PIN ✓ {idx}/{len(pending)}] {vid} ({vc:,} views) | {v_state.get('title', '')[:50]}", flush=True)
                if pinned_count % 5 == 0:
                    state["updated_at"] = utc_now()
                    save_json_file(STATE_PATH, state)
            else:
                failed_ids.append(vid)
                print(f"  [STUDIO PIN WARN {idx}/{len(pending)}] {vid}: {res}", flush=True)
    finally:
        if temp_pid is not None:
            try:
                mcp.call_tool("close_page", {"pageId": temp_pid})
            except Exception:
                pass
        if prev_selected_pid is not None and prev_selected_pid != temp_pid:
            try:
                mcp.call_tool("select_page", {"pageId": prev_selected_pid})
            except Exception:
                pass
        state["updated_at"] = utc_now()
        save_json_file(STATE_PATH, state)

    rem = sum(
        1
        for v_st in (state.get("videos") or {}).values()
        if isinstance(v_st, dict) and v_st.get("needs_studio_pin")
    )
    return {"online": True, "pinned": pinned_count, "failed": failed_ids, "remaining_unpinned": rem}


def main() -> int:
    ap = argparse.ArgumentParser(description="Ensure every public YouTube video links to the 82.5 FM livestream in description + comment.")
    ap.add_argument("--dry-run", action="store_true", help="Preview changes without mutating YouTube.")
    ap.add_argument("--limit", type=int, default=50, help="Max videos to mutate in this run (default 50 ~= 5,050 quota units; 0 = unlimited).")
    ap.add_argument("--daily-cap", type=int, default=55, help="Max videos to mutate per Pacific quota day to preserve >=4,400 daily quota headroom (0 = unlimited).")
    ap.add_argument("--skip-comments", action="store_true", help="Only update descriptions in this pass.")
    ap.add_argument("--force-recheck", action="store_true", help="Re-inspect videos even if marked complete in state.")
    ap.add_argument("--pin-only", action="store_true", help="Pin pending comments via Studio MCP bridge (0 YouTube Data API quota).")
    ap.add_argument("--no-studio-pin", action="store_true", help="Skip automatic Studio MCP pinning at end of run.")
    args = ap.parse_args()

    state = load_json_file(STATE_PATH, {"live_video_id": DEFAULT_LIVE_ID, "updated_at": utc_now(), "videos": {}})
    if args.pin_only:
        pin_res = pin_pending_comments_via_studio_mcp(state, max_pins=args.limit)
        print(json.dumps({"pin_only_result": pin_res}, ensure_ascii=False, indent=2))
        return 0

    pt_today = datetime.datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    daily_ledger = state.setdefault("daily_mutations_by_pt_date", {})
    already_today = int(daily_ledger.get(pt_today, 0))
    if args.daily_cap > 0 and already_today >= args.daily_cap and not args.dry_run:
        print(json.dumps({
            "status": "DAILY_QUOTA_RESERVE_CAP_REACHED",
            "pt_date": pt_today,
            "mutated_today": already_today,
            "daily_cap": args.daily_cap,
            "note": "Preserving remaining YouTube Data API quota headroom until 00:00 PT reset.",
        }, ensure_ascii=False, indent=2))
        return 0

    effective_limit = args.limit
    if args.daily_cap > 0:
        rem_today = max(0, args.daily_cap - already_today)
        effective_limit = min(effective_limit, rem_today) if effective_limit > 0 else rem_today

    access_token = get_access_token()
    try:
        live_id = resolve_active_live_video_id(access_token)
        live_url = f"https://www.youtube.com/watch?v={live_id}"
        all_ids = fetch_all_channel_video_ids(access_token)
        live_records = fetch_live_video_records(access_token, all_ids)
    except QuotaExceededError:
        print(json.dumps({"status": "QUOTA_DEFERRED", "pt_date": pt_today, "quota_deferred": True}, indent=2))
        return 0

    public_vods: list[dict] = []
    for item in live_records:
        vid = item["id"]
        if vid == live_id:
            continue
        st = item.get("status") or {}
        if st.get("privacyStatus") != "public":
            continue
        # Skip active live broadcasts
        ls = item.get("liveStreamingDetails") or {}
        if ls.get("actualStartTime") and not ls.get("actualEndTime"):
            continue
        public_vods.append(item)

    public_vods.sort(
        key=lambda v: (
            1 if "bandcamp.com" in ((v.get("snippet") or {}).get("description") or "").lower() else 0,
            int((v.get("statistics") or {}).get("viewCount") or 0),
        ),
        reverse=True,
    )

    # If the active livestream video ID ever changed, re-verify everything automatically
    if state.get("live_video_id") != live_id:
        state["live_video_id"] = live_id
        state["videos"] = {}

    backup = load_json_file(BACKUP_PATH, {"created_at": utc_now(), "videos": {}})

    total_public = len(public_vods)
    total_views_all = sum(int((v.get("statistics") or {}).get("viewCount") or 0) for v in public_vods)

    mutated_this_run = 0
    desc_updated_count = 0
    desc_already_clean_count = 0
    comment_updated_in_place_count = 0
    comment_inserted_count = 0
    comment_already_present_count = 0
    quota_hit = False

    for rank_idx, item in enumerate(public_vods, start=1):
        vid = item["id"]
        sn = item.get("snippet") or {}
        locs = item.get("localizations") or {}
        vc = int((item.get("statistics") or {}).get("viewCount") or 0)
        orig_title = sn.get("title", "")
        orig_desc = sn.get("description", "")

        v_state = state["videos"].setdefault(vid, {})
        b_entry = backup["videos"].setdefault(vid, {"title": orig_title, "captured_at": utc_now()})

        # 1. Check & Update Description (+ all 20 localizations)
        en_loc_desc = (locs.get("en") or {}).get("description", orig_desc)
        needs_desc_update = not (
            description_already_clean(orig_desc, live_id)
            and description_already_clean(en_loc_desc, live_id)
        )

        did_mutate_video = False

        if not needs_desc_update:
            desc_already_clean_count += 1
            v_state["desc_done"] = True
            v_state["live_id"] = live_id
        else:
            if effective_limit and mutated_this_run >= effective_limit:
                break
            new_desc = transform_description(orig_desc, sn.get("defaultLanguage") or "en", live_url)
            new_locs: dict[str, dict] = {}
            for lang_code, loc_obj in locs.items():
                loc_title = loc_obj.get("title", orig_title)
                assert loc_title == loc_obj.get("title", orig_title), "Localization title must never change!"
                new_locs[lang_code] = {
                    "title": loc_title,
                    "description": transform_description(loc_obj.get("description", ""), lang_code, live_url),
                }

            assert orig_title == sn.get("title", ""), "Video title must NEVER be modified!"

            if args.dry_run:
                print(f"[DRY-RUN DESC #{rank_idx}/{total_public}] {vid} ({vc:,} views) | {orig_title[:60]}")
                print("  NEW TOP 2 LINES:", " // ".join(new_desc.splitlines()[:2]))
                did_mutate_video = True
                desc_updated_count += 1
            else:
                if "original_description" not in b_entry:
                    b_entry["original_description"] = orig_desc
                    if locs:
                        b_entry["original_localizations"] = locs

                upd_snippet = {
                    "title": orig_title,
                    "categoryId": sn.get("categoryId") or "10",
                    "description": new_desc,
                }
                if sn.get("tags") is not None:
                    upd_snippet["tags"] = sn["tags"]
                if sn.get("defaultLanguage"):
                    upd_snippet["defaultLanguage"] = sn["defaultLanguage"]
                if sn.get("defaultAudioLanguage"):
                    upd_snippet["defaultAudioLanguage"] = sn["defaultAudioLanguage"]

                put_body: dict = {"id": vid, "snippet": upd_snippet}
                part_str = "snippet"
                if new_locs:
                    put_body["localizations"] = new_locs
                    part_str = "snippet,localizations"

                try:
                    yt_api(access_token, f"videos?part={part_str}", method="PUT", body=put_body)
                    v_state["desc_done"] = True
                    v_state["desc_updated_at"] = utc_now()
                    v_state["live_id"] = live_id
                    desc_updated_count += 1
                    did_mutate_video = True
                    print(f"[DESC ✓ #{rank_idx}/{total_public}] {vid} ({vc:,} views) | {orig_title[:58]}")
                except QuotaExceededError:
                    print(f"[QUOTA REACHED] Stopped cleanly at rank #{rank_idx} ({vid}) during videos.update.")
                    quota_hit = True
                    break

        # 2. Check & Update/Insert @NovaHart_Official Comment
        if not args.skip_comments:
            already_comment_done = (
                not args.force_recheck
                and v_state.get("comment_done") is True
                and v_state.get("live_id") == live_id
            )
            if already_comment_done:
                comment_already_present_count += 1
            else:
                if effective_limit and mutated_this_run >= effective_limit and not did_mutate_video:
                    break
                try:
                    c_res = ensure_video_comment(
                        access_token=access_token,
                        vid=vid,
                        live_id=live_id,
                        live_url=live_url,
                        backup_entry=b_entry,
                        dry_run=args.dry_run,
                    )
                    st_code = c_res.get("status")
                    if st_code == "already_present":
                        comment_already_present_count += 1
                        v_state["comment_done"] = True
                        v_state["comment_id"] = c_res.get("comment_id")
                        v_state["likely_pinned"] = c_res.get("likely_pinned", False)
                        v_state["needs_studio_pin"] = not c_res.get("likely_pinned", False)
                        v_state["live_id"] = live_id
                    elif st_code in ("updated_in_place", "dry_run_update_in_place"):
                        comment_updated_in_place_count += 1
                        did_mutate_video = True
                        if not args.dry_run:
                            v_state["comment_done"] = True
                            v_state["comment_action"] = "updated_in_place"
                            v_state["comment_id"] = c_res.get("comment_id")
                            v_state["likely_pinned"] = bool(c_res.get("was_rank0_pinned"))
                            v_state["needs_studio_pin"] = bool(c_res.get("needs_studio_pin"))
                            v_state["comment_updated_at"] = utc_now()
                            v_state["live_id"] = live_id
                        print(
                            f"  [COMMENT IN-PLACE ✓] {vid} | id={c_res.get('comment_id')} | preserved_pin={c_res.get('was_rank0_pinned')}"
                        )
                    elif st_code in ("inserted_new", "dry_run_insert_new"):
                        comment_inserted_count += 1
                        did_mutate_video = True
                        if not args.dry_run:
                            v_state["comment_done"] = True
                            v_state["comment_action"] = "inserted_new"
                            v_state["comment_id"] = c_res.get("comment_id")
                            v_state["likely_pinned"] = False
                            v_state["needs_studio_pin"] = True
                            v_state["comment_updated_at"] = utc_now()
                            v_state["live_id"] = live_id
                        print(f"  [COMMENT INSERTED ✓] {vid} | id={c_res.get('comment_id')} (needs Studio pin)")
                    else:
                        v_state["comment_status"] = st_code
                        print(f"  [COMMENT SKIP] {vid} | {st_code}: {c_res.get('detail', '')}")
                except QuotaExceededError:
                    print(f"[QUOTA REACHED] Stopped cleanly at rank #{rank_idx} ({vid}) during comment sync.")
                    quota_hit = True
                    break

        v_state["viewCount"] = vc
        v_state["title"] = orig_title
        if did_mutate_video:
            mutated_this_run += 1
            if not args.dry_run:
                daily_ledger[pt_today] = int(daily_ledger.get(pt_today, 0)) + 1
            if not args.dry_run and mutated_this_run % 5 == 0:
                state["updated_at"] = utc_now()
                save_json_file(STATE_PATH, state)
                save_json_file(BACKUP_PATH, backup)

        if effective_limit and mutated_this_run >= effective_limit:
            break

    studio_pin_summary: dict = {}
    if not args.dry_run:
        state["updated_at"] = utc_now()
        save_json_file(STATE_PATH, state)
        save_json_file(BACKUP_PATH, backup)
        if not args.no_studio_pin:
            studio_pin_summary = pin_pending_comments_via_studio_mcp(state, max_pins=effective_limit or 50)

    # Compute exact coverage metrics across all public VODs
    covered_desc_ids = {
        v["id"]
        for v in public_vods
        if (state["videos"].get(v["id"]) or {}).get("desc_done") and (state["videos"].get(v["id"]) or {}).get("live_id") == live_id
    }
    covered_both_ids = {
        v["id"]
        for v in public_vods
        if v["id"] in covered_desc_ids and (state["videos"].get(v["id"]) or {}).get("comment_done")
    }
    views_covered_desc = sum(
        int((v.get("statistics") or {}).get("viewCount") or 0)
        for v in public_vods
        if v["id"] in covered_desc_ids
    )
    views_covered_both = sum(
        int((v.get("statistics") or {}).get("viewCount") or 0)
        for v in public_vods
        if v["id"] in covered_both_ids
    )
    needs_pin_top = [
        {
            "rank": idx,
            "id": v["id"],
            "views": int((v.get("statistics") or {}).get("viewCount") or 0),
            "title": (v.get("snippet") or {}).get("title", "")[:55],
            "comment_id": (state["videos"].get(v["id"]) or {}).get("comment_id"),
        }
        for idx, v in enumerate(public_vods, start=1)
        if (state["videos"].get(v["id"]) or {}).get("needs_studio_pin")
    ]

    summary = {
        "live_video_id": live_id,
        "live_url": live_url,
        "total_public_vods": total_public,
        "this_run": {
            "videos_mutated": mutated_this_run,
            "descriptions_updated": desc_updated_count,
            "descriptions_already_clean": desc_already_clean_count,
            "comments_updated_in_place_preserving_pin": comment_updated_in_place_count,
            "comments_inserted_new": comment_inserted_count,
            "comments_already_present": comment_already_present_count,
            "studio_auto_pin": studio_pin_summary,
            "quota_deferred": quota_hit,
        },
        "cumulative_coverage": {
            "descriptions_done": f"{len(covered_desc_ids)} / {total_public}",
            "both_desc_and_comment_done": f"{len(covered_both_ids)} / {total_public}",
            "share_of_total_views_with_desc_link": f"{100.0 * views_covered_desc / max(1, total_views_all):.2f}%",
            "share_of_total_views_with_both": f"{100.0 * views_covered_both / max(1, total_views_all):.2f}%",
            "needs_studio_pin_count": len(needs_pin_top),
            "top_15_needing_studio_pin": needs_pin_top[:15],
        },
    }
    print("\n=== LIVESTREAM FUNNEL ROLLOUT SUMMARY ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
