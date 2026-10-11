#!/usr/bin/env python3
"""Pre-generates and caches AI translations for all catalog videos on disk.

Translates video titles and full descriptions into 19 languages using Gemini 2.5 Flash via OpenRouter.
All results are saved into youtube/state/translations_cache/<vid>.json.
"""

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state")
import translate_ai


def pregenerate(limit=None):
    with open(os.path.join(STATE, "videos.json")) as fh:
        videos = json.load(fh)["videos"]
    with open(os.path.join(HERE, "translations.json")) as fh:
        tr = json.load(fh)

    target_langs = [l for l in tr["blocks"].keys() if l != tr["source_lang"]]
    public_videos = [v for v in videos if v["status"]["privacyStatus"] != "private"]

    print(f"Starting pre-generation for {len(public_videos)} public videos across {len(target_langs)} languages...")

    n = 0
    cached_count = 0
    for i, v in enumerate(public_videos):
        vid = v["id"]
        title = v["snippet"]["title"]
        desc = v["snippet"].get("description", "")

        cached = translate_ai.get_cached_translation(vid)
        if cached and all(l in cached for l in target_langs):
            cached_count += 1
            continue

        if limit and n >= limit:
            break

        print(f"[{i+1}/{len(public_videos)}] Translating {vid} ({title[:36]})...", flush=True)
        res = translate_ai.translate_video(vid, title, desc, target_langs)
        if res:
            n += 1
            print(f"    -> Cached {len(res)} languages for {vid}")
        time.sleep(0.5)

    print(f"\nDone! Pre-generated {n} new video translations. Total cached: {cached_count + n}/{len(public_videos)}.")


if __name__ == "__main__":
    import sys
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    pregenerate(limit=lim)
