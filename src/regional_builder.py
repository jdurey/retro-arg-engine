"""Generates the regional nodes (BBS, Gopher, Minitel, etc.) as terminal-style HTML."""
import os

from common import esc, write

DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">'

def build_node(ctx, node):
    skin = node["skin"]
    lines = []
    lines.append(DOCTYPE)
    lines.append(f'<HTML LANG="{node["lang"]}"><HEAD><TITLE>{esc(node["title"])}</TITLE>')
    lines.append('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">')
    lines.append('</HEAD>')
    lines.append(f'<BODY BGCOLOR="{skin["bg"]}" TEXT="{skin["fg"]}" LINK="{skin.get("accent", "#FFFFFF")}" VLINK="{skin.get("accent", "#FFFFFF")}">')
    lines.append('<PRE>')
    for line in node["screen"]:
        lines.append(esc(line))
    lines.append('</PRE>')
    if node.get("menu") or node.get("links"):
        lines.append('<HR>')
    if "menu" in node:
        lines.append('<UL>')
        for key, text in node["menu"]:
            lines.append(f'<LI>[{esc(key)}] {esc(text)}')
        lines.append('</UL>')
    if "links" in node:
        lines.append('<UL>')
        rel_dir = f'regional/{node["id"]}'
        for link in node["links"]:
            lines.append(f'<LI><A HREF="{ctx.link(link["u"], rel_dir)}">{esc(link["t"])}</A>')
        lines.append('</UL>')
    lines.append('</BODY></HTML>')
    return "\n".join(lines) + "\n"

def build(ctx, **kwargs):
    nodes = ctx.nodes
    count = 0
    for node in nodes:
        rel = f'regional/{node["id"]}/index.html'
        write(os.path.join(ctx.out, rel), build_node(ctx, node))
        ctx.register(rel, "regional", node["title"])
        count += 1
    return {"regional_nodes": count}
