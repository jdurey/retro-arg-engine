"""Shared helpers for the retro web swarm builders (Python 3.9+, stdlib only)."""
import hashlib
import html
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")


def load(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as fh:
        return json.load(fh)


def rng_for(*parts):
    """Deterministic RNG so every rebuild is byte-identical for the same seed."""
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def esc(text):
    return html.escape(str(text), quote=True)


def write(path, content, binary=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if binary:
        with open(path, "wb") as fh:
            fh.write(content)
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)


def group_slug(group):
    return group.replace(".", "-")


class Ctx:
    """Build context: loaded data + an index used to resolve cross-links."""

    def __init__(self, out_dir, seed="nova-hart"):
        self.out = out_dir
        self.seed = seed
        self.lore = load("lore_seeds.json")
        self.personas = {p["id"]: p for p in load("personas.json")["personas"]}
        self.nodes = load("regional_nodes.json")["nodes"]
        self.thread_group = {t["id"]: t["group"] for t in self.lore["usenet_threads"]}
        self.pages = []  # (relative path, kind, title) for manifest
        self.swarm_geo = []  # procedurally generated homepage slugs
        self.swarm_threads = []

    def register(self, rel_path, kind, title):
        self.pages.append({"path": "/" + rel_path.replace(os.sep, "/"), "kind": kind, "title": title})

    # ---- cross-link resolution -------------------------------------------------
    def target(self, token):
        kind, _, arg = token.partition(":")
        if kind == "home":
            return "index.html"
        if kind == "terminal":
            return "terminal/index.html"
        if kind == "usenet":
            return "usenet/%s/%s.txt" % (group_slug(self.thread_group[arg]), arg)
        if kind == "usenetgroup":
            return "usenet/%s/index.html" % group_slug(arg)
        if kind == "geo":
            return "geocities/%s.html" % arg
        if kind == "ftp":
            site, _, fname = arg.partition("/")
            return "ftp/%s/%s" % (site, fname or "index.html")
        if kind == "regional":
            return "regional/%s/index.html" % arg
        if kind == "asset":
            return "assets/%s" % arg
        raise ValueError("unknown link token: " + token)

    def link(self, token, from_rel_dir):
        return os.path.relpath(self.target(token), from_rel_dir or ".").replace(os.sep, "/")


def relay_table_lines(lore, width=64):
    rows = ["  NODE  SOURCE                                      LINE", "  ----  ------------------------------------------  " + "-" * 32]
    for n in lore["project_stardust"]["relay_nodes"]:
        rows.append("  %02d    %-42s  %s" % (n["node"], n["pressing"][:42], n["line"]))
    return rows
