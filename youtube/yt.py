"""YouTube channel tool for the Stardust launch.

  python yt.py auth        # one-time OAuth (prints a URL to approve)
  python yt.py inventory   # read-only: dump all uploads to state/videos.json
  python yt.py apply [--dry-run] [--limit N]
                           # add the Web Ring block to each description and
                           # set per-language title/description localizations.
                           # Resumable; skips videos already done. ~50 quota units/video.
"""
import json
import re
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state")
TOKEN = os.path.join(HERE, "token.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
LINK = ("https://index-geocities-tmpaju-9w49787-users2097732-25sl7i9-ghostq0f.stardust-archive.net"
        "/~8p6028i/kamome5ff-idolyj4/h9284b8/p64r9/7961685-bh63kr/index.html")
MARKER = "stardust-archive.net"


def creds(interactive=False):
    c = Credentials.from_authorized_user_file(TOKEN, SCOPES) if os.path.exists(TOKEN) else None
    if c and c.expired and c.refresh_token:
        c.refresh(Request())
    if not c or not c.valid:
        if not interactive:
            sys.exit("Not authorized. Run: python yt.py auth")
        flow = InstalledAppFlow.from_client_secrets_file(os.path.join(HERE, "client_secret.json"), SCOPES)
        c = flow.run_local_server(port=8765, open_browser=False,
                                  authorization_prompt_message="AUTH_URL: {url}", success_message="Authorized. You can close this tab.")
    with open(TOKEN, "w") as fh:
        fh.write(c.to_json())
    return c


def yt():
    return build("youtube", "v3", credentials=creds(), cache_discovery=False)


def inventory():
    api = yt()
    ch = api.channels().list(part="snippet,contentDetails", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, token = [], None
    while True:
        r = api.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=token).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        token = r.get("nextPageToken")
        if not token:
            break
    videos = []
    for i in range(0, len(ids), 50):
        r = api.videos().list(part="snippet,localizations,status", id=",".join(ids[i:i + 50])).execute()
        videos += r["items"]
    os.makedirs(STATE, exist_ok=True)
    with open(os.path.join(STATE, "videos.json"), "w") as fh:
        json.dump({"channel": ch["snippet"]["title"], "videos": videos}, fh, ensure_ascii=False, indent=1)
    has_link = sum(MARKER in v["snippet"].get("description", "") for v in videos)
    langs = {v["snippet"].get("defaultLanguage") for v in videos}
    print(f"Channel: {ch['snippet']['title']}  videos: {len(videos)}  with link: {has_link}  defaultLanguage values: {langs}")


WEB_RING_LINE = re.compile(r"^\s*(▶\s*)?Web Ring\s*:.*stardust-archive\.net.*\n*", re.M)
HASHTAG = re.compile(r"(?<!\w)#\w+")


def with_block(block, desc):
    """Prepend a hook block, never exceeding YouTube's 15-hashtag cap."""
    if len(HASHTAG.findall(block)) + len(HASHTAG.findall(desc)) > 15:
        block = "\n".join(l for l in block.splitlines() if not l.strip().startswith("#"))
    return (block + "\n\n" + desc).strip()[:5000]


def apply(dry_run=False, limit=None, reset_done=False):
    api = yt() if not dry_run else None
    with open(os.path.join(STATE, "videos.json")) as fh:
        videos = json.load(fh)["videos"]
    with open(os.path.join(HERE, "translations.json")) as fh:
        tr = json.load(fh)  # {"blocks": {lang: text}, "source_lang": "en"}
    links_path = os.path.join(STATE, "video_links.json")
    if not os.path.exists(links_path):
        import allocate_nodes
        allocate_nodes.build_allocation()
    with open(links_path) as fh:
        video_links = json.load(fh)

    done_path = os.path.join(STATE, "done.json")
    done = set() if reset_done else (set(json.load(open(done_path))) if os.path.exists(done_path) else set())
    # Private videos are skipped; videos still missing the link go first.
    videos = [v for v in videos if v["status"]["privacyStatus"] != "private"]
    videos.sort(key=lambda v: MARKER in v["snippet"].get("description", ""))
    n = 0
    for v in videos:
        vid = v["id"]
        if vid in done:
            continue
        if limit and n >= limit:
            break
        sn = v["snippet"]
        desc = sn.get("description", "")
        body_desc = WEB_RING_LINE.sub("", desc).strip()  # original text minus any existing Web Ring line
        
        # Pull the specific, dedicated node URL allocated for this video
        v_link = video_links.get(vid, {}).get("url") or LINK
        v_path = video_links.get(vid, {}).get("site_path") or "default"

        src = tr["blocks"][tr["source_lang"]].replace("LINK", v_link)
        new_desc = with_block(src, body_desc)
        default_lang = sn.get("defaultLanguage") or tr["source_lang"]
        locs = dict(v.get("localizations") or {})
        for lang, block in tr["blocks"].items():
            if lang == tr["source_lang"] or lang == default_lang:
                continue
            existing = locs.get(lang, {})
            locs[lang] = {"title": existing.get("title") or sn["title"],
                          "description": with_block(block.replace("LINK", v_link), body_desc)}
        body = {"id": vid, "snippet": {"title": sn["title"], "categoryId": sn["categoryId"],
                                       "description": new_desc[:5000], "defaultLanguage": default_lang},
                "localizations": locs}
        for k in ("tags", "defaultAudioLanguage"):
            if sn.get(k):
                body["snippet"][k] = sn[k]
        if dry_run:
            print(f"[{n+1}/{len(videos)}] DRY RUN: {vid} ({sn['title'][:40]}) -> {v_path}")
            print(f"    URL: {v_link}")
            print(f"    Sample localized snippet:\n{new_desc[:220]}...\n")
            n += 1
            continue
        try:
            api.videos().update(part="snippet,localizations", body=body).execute()
        except HttpError as e:
            if e.resp.status == 403 and b"quota" in e.content.lower():
                print(f"\n[!] YouTube API daily quota reached after {n} video updates.")
                print("    Google resets quota daily at midnight Pacific Time (07:00 UTC).")
                print(f"    Progress saved ({len(done)}/{len(videos)} videos updated).")
                print("    Run 'python yt.py apply' again after quota resets to resume seamlessly.")
                break
            print("ERROR", vid, e.resp.status, e.content[:300])
            continue
        done.add(vid)
        json.dump(sorted(done), open(done_path, "w"))
        n += 1
        print(f"[{len(done)}/{len(videos)}] updated {vid} -> {v_path}", flush=True)
    print(f"\nDone this run: {n}; total {len(done)}/{len(videos)} videos updated.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "auth":
        creds(interactive=True)
        print("OK token saved")
    elif cmd == "inventory":
        inventory()
    elif cmd == "allocate":
        import allocate_nodes
        allocate_nodes.build_allocation()
    elif cmd == "apply":
        lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
        apply(dry_run="--dry-run" in sys.argv, limit=lim, reset_done="--all" in sys.argv)
    else:
        print(__doc__)
