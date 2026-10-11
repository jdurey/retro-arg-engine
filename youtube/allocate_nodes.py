#!/usr/bin/env python3
"""Maps every Nova Hart YouTube video to a unique, lore-matched ARG node URL."""

import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STATE = os.path.join(HERE, "state")
OUT_FILE = os.path.join(STATE, "video_links.json")


def load_data():
    with open(os.path.join(ROOT, "urls.csv")) as f:
        r = csv.reader(f)
        next(r)
        url_map = {row[0]: row[1] for row in r}

    with open(os.path.join(ROOT, "site_clues.json")) as f:
        clues = json.load(f)["clues"]

    with open(os.path.join(STATE, "videos.json")) as f:
        videos = json.load(f)["videos"]

    return url_map, clues, videos


def build_allocation():
    url_map, clues, videos = load_data()

    inst_pool = [
        p
        for p in [
            "ftp/ashford-poly/index.html",
            "ftp/kamome/index.html",
            "ftp/ashford-poly/hale_telemetry_1989-09.log",
            "ftp/kamome/anomalies.txt",
            "ftp/ashford-poly/idol_protocol_memo.txt",
            "ftp/kamome/audio/ghost_in_the_chorus.mp3",
            "ftp/ashford-poly/luna_credits.txt",
            "ftp/ashford-poly/nova_l_log9002.txt",
        ]
        if p in url_map
    ]

    reg_pool = [
        f"regional/{r}/index.html"
        for r in [
            "01-usa",
            "02-japan",
            "04-mexico",
            "08-ussr",
            "07-uk",
            "03-germany",
            "05-france",
            "06-italy",
            "09-korea",
            "10-india",
            "11-sweden",
            "12-fiji",
        ]
        if f"regional/{r}/index.html" in url_map
    ]

    hood_pool = [
        f"geocities/hood_{h}.html"
        for h in [
            "tokyo-garden",
            "hollywood-hills",
            "siliconvalley-lab",
            "sunsetstrip-club",
            "area51-vault",
            "bourbonstreet-delta",
            "capecanaveral-lab",
            "heartland-plains",
            "pentagon-quarters",
            "soho-studio",
            "timessquare-arcade",
            "paris-leftbank",
            "athens-forum",
            "vienna-strasse",
        ]
        if f"geocities/hood_{h}.html" in url_map
    ]

    clue_pool = []
    for c in clues:
        p = "geocities/" + c["slug"] + ".html"
        if p in url_map and p not in clue_pool:
            clue_pool.append(p)

    assigned = {}
    used = set()

    # Prioritized keyword matching for specific songs
    for v in videos:
        vid = v["id"]
        title = v["snippet"]["title"].lower()
        choice = None

        if any(
            k in title
            for k in [
                "quantum",
                "signal",
                "telemetry",
                "carrier",
                "harrison",
                "14.2",
                "frequency",
            ]
        ):
            for p in inst_pool:
                if "ashford" in p and p not in used:
                    choice = p
                    break
        elif any(
            k in title
            for k in [
                "japan",
                "tokyo",
                "idol",
                "pc-98",
                "yuki",
                "garden",
                "akasaka",
            ]
        ):
            for p in inst_pool + reg_pool + hood_pool:
                if (
                    "kamome" in p or "02-japan" in p or "tokyo" in p
                ) and p not in used:
                    choice = p
                    break
        elif any(k in title for k in ["cold", "soviet", "russia", "relcom"]):
            for p in reg_pool:
                if "08-ussr" in p and p not in used:
                    choice = p
                    break
        elif any(
            k in title
            for k in ["mexico", "coyoacan", "cassette", "plaza", "rock"]
        ):
            for p in reg_pool + hood_pool:
                if ("04-mexico" in p or "bourbon" in p) and p not in used:
                    choice = p
                    break
        elif any(
            k in title
            for k in ["neon", "night", "city", "hollywood", "hills", "graveyard"]
        ):
            for p in hood_pool:
                if (
                    "hollywood" in p or "sunsetstrip" in p or "times" in p
                ) and p not in used:
                    choice = p
                    break

        if not choice:
            for p in inst_pool + reg_pool + hood_pool + clue_pool:
                if p not in used:
                    choice = p
                    break

        used.add(choice)
        assigned[vid] = {
            "title": v["snippet"]["title"],
            "site_path": choice,
            "url": url_map[choice],
        }

    with open(OUT_FILE, "w") as f:
        json.dump(assigned, f, indent=2)

    print(
        f"Successfully assigned {len(assigned)} videos to {len(used)} unique URLs."
    )
    print(f"Mapping saved to: {OUT_FILE}\n")

    for i, (vid, info) in enumerate(list(assigned.items())[:25]):
        t = info["title"][:32]
        sp = info["site_path"]
        print(f" {i+1:2d}. [{vid}] {t:32s} -> {sp}")


if __name__ == "__main__":
    build_allocation()
