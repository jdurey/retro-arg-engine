"""GeoCities-era (1995-1996) HTML 3.2 homepage generator with webrings and hit counters."""
import json
import os

from common import esc, relay_table_lines, rng_for, write
from swarm_corner import generate_swarm_homepage

DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
RING = "The Stardust Webring"


def counter_html(n):
    digits = "%06d" % n
    cells = "".join('<TD BGCOLOR="#000000"><FONT FACE="Courier New,Courier" COLOR="#33FF33"><B>%s</B></FONT></TD>' % d for d in digits)
    return ('<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0><TR>%s</TR></TABLE>' % cells)


def under_construction():
    stripes = "".join('<TD BGCOLOR="%s" WIDTH=14>&nbsp;</TD>' % ("#FFCC00" if i % 2 == 0 else "#000000") for i in range(16))
    return ('<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0><TR>%s</TR></TABLE>'
            '<FONT FACE="Arial,Helvetica" COLOR="#FFCC00"><B>&#9888; UNDER CONSTRUCTION &#9888;</B></FONT>'
            '<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0><TR>%s</TR></TABLE>') % (stripes, stripes)


def relay_table_html(lore, hp):
    rows = []
    for n in lore["project_stardust"]["relay_nodes"]:
        known = "?" not in n["line"]
        rows.append('<TR><TD ALIGN=CENTER><TT>%02d</TT></TD><TD>%s</TD><TD><TT>%s</TT></TD></TR>' % (
            n["node"], esc(n["pressing"]), esc(n["line"]) if known else '<BLINK>%s</BLINK>' % esc(n["line"])))
    return ('<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 BORDERCOLOR="%s"><TR><TH>NODE</TH><TH>SOURCE</TH><TH>LINE</TH></TR>%s</TABLE>'
            % (hp["link"], "".join(rows)))


def webring(ctx, slug, ring, i):
    prev_s, next_s = ring[i - 1], ring[(i + 1) % len(ring)]
    rand_s = ring[rng_for(ctx.seed, "ring", slug).randrange(len(ring))]
    return ('<CENTER><TABLE BORDER=3 CELLPADDING=4 BGCOLOR="#000000"><TR><TD ALIGN=CENTER>'
            '<FONT COLOR="#FFFFFF" FACE="Arial,Helvetica" SIZE=2>&#10022; This <B>%s</B> site is station #%d of %d &#10022;<BR>'
            '[ <A HREF="%s.html">&lt;&lt; Prev</A> | <A HREF="%s.html">Random</A> | <A HREF="index.html#ring">List Stations</A> | <A HREF="%s.html">Next &gt;&gt;</A> ]'
            '</FONT></TD></TR></TABLE></CENTER>') % (RING, i + 1, len(ring), prev_s, rand_s, next_s)


def render_badges(ctx, badges, from_dir):
    if not badges:
        return ""
    imgs = []
    for b in badges:
        imgs.append('<IMG SRC="%s" WIDTH=88 HEIGHT=31 BORDER=1 HSPACE=3 VSPACE=3 ALT="[%s]">' % (
            ctx.link("asset:badges/" + b + ".gif", from_dir), esc(b)))
    imgs.append('<IMG SRC="%s" WIDTH=32 HEIGHT=32 BORDER=0 HSPACE=3 VSPACE=3 ALT="[*]">' % (
        ctx.link("asset:badges/spinning_star.gif", from_dir)))
    return '<CENTER><P>' + "".join(imgs) + '</P></CENTER>'


def render_sections_html(ctx, sections, from_dir, hp):
    sec_parts = []
    for s in sections:
        sec_parts.append('<H2><FONT FACE="Arial,Helvetica">&#9733; %s</FONT></H2>' % esc(s["h"]))
        if s.get("img"):
            sec_parts.append('<CENTER><IMG SRC="%s" WIDTH=%d HEIGHT=%d BORDER=2 ALT="%s"><BR><FONT SIZE=2><I>%s</I></FONT></CENTER>' % (
                ctx.link(s["img"], from_dir), s.get("w", 320), s.get("h", 240), esc(s.get("alt", "")), esc(s.get("caption", ""))))
        for p in s.get("p", []):
            sec_parts.append("<P>%s</P>" % p)
        if s.get("list"):
            sec_parts.append("<UL>" + "".join("<LI>%s" % i for i in s["list"]) + "</UL>")
        if s.get("pre"):
            sec_parts.append("<PRE>%s</PRE>" % esc("\n".join(s["pre"])))
        if s.get("relay_table"):
            sec_parts.append("<CENTER>" + relay_table_html(ctx.lore, hp) + "</CENTER>")
    return "\n".join(sec_parts)


def render(ctx, hp, owner, ring, idx):
    from_dir = "geocities"
    layout = hp.get("layout", "shrine")
    badges_html = render_badges(ctx, hp.get("badges"), from_dir)
    
    parts = [
        DOCTYPE,
        '<HTML LANG="%s"><HEAD><TITLE>%s</TITLE>' % (hp.get("lang", "en"), esc(hp["title"])),
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">',
        '<META NAME="description" CONTENT="%s">' % esc(hp["title"] + " - a personal homepage at GeoCities " + hp["path_display"]),
        '<META NAME="keywords" CONTENT="Nova Hart, SYNTHESIS, Orion Records, Marcus Hale, Stardust, 14.2 Hz">',
        '</HEAD>',
        '<BODY BGCOLOR="%s" TEXT="%s" LINK="%s" VLINK="%s" ALINK="#FF0000">' % (hp["bg"], hp["text"], hp["link"], hp["vlink"]),
        '<FONT SIZE=1 FACE="Arial,Helvetica">GeoCities &gt; %s</FONT>' % esc(" > ".join(hp["path_display"].split("/"))),
    ]
    
    # ------------------------------------------------ Layout: TWO COLUMN
    if layout == "two_column":
        if hp.get("marquee"):
            parts.append('<CENTER><MARQUEE BEHAVIOR=SCROLL SCROLLAMOUNT=4 WIDTH="90%%"><FONT FACE="Courier New,Courier"><B>%s</B></FONT></MARQUEE></CENTER>' % esc(hp["marquee"]))
        parts.append('<CENTER><H1><FONT FACE="Arial Black,Arial,Helvetica">%s</FONT></H1></CENTER>' % esc(hp["title"]))
        parts.append('<HR SIZE=3 NOSHADE>')
        parts.append('<TABLE BORDER=0 CELLPADDING=8 CELLSPACING=0 WIDTH="100%"><TR>')
        
        # Sidebar Left
        parts.append('<TD VALIGN=TOP WIDTH=220 BGCOLOR="#111111">')
        parts.append('<FONT COLOR="#FFFFFF" FACE="Arial,Helvetica" SIZE=2>')
        parts.append('<CENTER><B>HOMESTEAD STATS</B><BR>')
        parts.append('<IMG SRC="%s" WIDTH=48 HEIGHT=48 BORDER=0 ALT="[Nova-chan]"><BR>' % ctx.link("asset:badges/novachan_chibi.gif", from_dir))
        parts.append('<P>Visitor #:<BR>' + counter_html(hp["counter"]) + '</P>')
        parts.append('<P><FONT SIZE=1>Updated:<BR>%s</FONT></P>' % esc(hp["updated"]))
        parts.append('<HR SIZE=1>')
        parts.append('<P><B>Webring Station</B><BR>Station #%d of %d</P>' % (idx + 1, len(ring)))
        parts.append('<HR SIZE=1>')
        parts.append(badges_html)
        parts.append('</CENTER></FONT></TD>')
        
        # Main Column Right
        parts.append('<TD VALIGN=TOP>')
        parts.append(render_sections_html(ctx, hp["sections"], from_dir, hp))
        parts.append('<HR SIZE=3 NOSHADE><H2><FONT FACE="Arial,Helvetica">&#9733; Cool Links</FONT></H2><UL>')
        for l in hp.get("links", []):
            parts.append('<LI><A HREF="%s">%s</A>' % (ctx.link(l["u"], from_dir), esc(l["t"])))
        parts.append('</UL>')
        parts.append('</TD></TR></TABLE>')
        
        parts.append('<HR SIZE=3 NOSHADE><CENTER>')
        parts.append(under_construction())
        parts.append('<P><A HREF="mailto:%s">&#9993; Email %s</A> | <A HREF="mailto:%s?subject=Guestbook">Sign Guestbook</A> | <A HREF="%s">Homestead Directory</A></P>' % (
            owner["email"], esc(hp["title"].split("'")[0]), owner["email"], ctx.link("home", from_dir)))
        parts.append(webring(ctx, hp["slug"], ring, idx))
        parts.append('<P><FONT SIZE=1>Hosted Free by GeoCities &middot; Best viewed with Netscape Navigator 2.0 at 640x480</FONT></P>')
        parts.append('</CENTER></BODY></HTML>')
        return "\n".join(parts) + "\n"

    # ------------------------------------------------ Layout: TERMINAL / ZINE
    elif layout == "terminal":
        parts.append('<CENTER>')
        parts.append('<PRE>')
        parts.append('=============================================================================')
        parts.append('  TERMINAL NODE: %-20s  STATION: #%04d  UPDATED: %s' % (hp["path_display"][:20], idx + 1, hp["updated"]))
        parts.append('  PROJECT STARDUST ARCHIVE // REVOLUTION 14.2 HZ // CERN-HTTPd 3.0')
        parts.append('=============================================================================')
        parts.append('</PRE>')
        parts.append('<H1><TT>%s</TT></H1>' % esc(hp["title"]))
        if hp.get("marquee"):
            parts.append('<PRE>[ TRANSMISSION ]: %s</PRE>' % esc(hp["marquee"]))
        parts.append('<P><TT>[ VISITOR REGISTER: %06d ]</TT></P>' % hp["counter"])
        parts.append('</CENTER><HR SIZE=2 NOSHADE>')
        parts.append(render_sections_html(ctx, hp["sections"], from_dir, hp))
        parts.append('<HR SIZE=2 NOSHADE><H2><TT>[ HYPERLINK MATRIX ]</TT></H2><UL>')
        for l in hp.get("links", []):
            parts.append('<LI><TT><A HREF="%s">%s</A></TT></LI>' % (ctx.link(l["u"], from_dir), esc(l["t"])))
        parts.append('</UL>')
        parts.append('<HR SIZE=2 NOSHADE><CENTER>')
        parts.append(badges_html)
        parts.append('<P><TT><A HREF="mailto:%s">[ CONTACT SYSOP: %s ]</A> | <A HREF="%s">[ ARCHIVE INDEX ]</A></TT></P>' % (
            owner["email"], esc(owner["email"]), ctx.link("home", from_dir)))
        parts.append(webring(ctx, hp["slug"], ring, idx))
        parts.append('</CENTER></BODY></HTML>')
        return "\n".join(parts) + "\n"

    # ------------------------------------------------ Layout: HUB
    elif layout == "hub":
        parts.append('<CENTER>')
        parts.append('<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 BGCOLOR="#000000"><TR>')
        parts.append('<TD><FONT COLOR="#00FFCC" FACE="Arial,Helvetica"><B>&nbsp;HOME&nbsp;</B></FONT></TD>')
        parts.append('<TD><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica"><A HREF="#sections"><FONT COLOR="#FFFFFF">ARTICLES</FONT></A></FONT></TD>')
        parts.append('<TD><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica"><A HREF="#links"><FONT COLOR="#FFFFFF">LINKS</FONT></A></FONT></TD>')
        parts.append('<TD><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica"><A HREF="mailto:%s"><FONT COLOR="#FFFFFF">MAILBOX</FONT></A></FONT></TD>' % owner["email"])
        parts.append('</TR></TABLE>')
        if hp.get("marquee"):
            parts.append('<P><MARQUEE BEHAVIOR=SCROLL SCROLLAMOUNT=4 WIDTH="85%%"><FONT FACE="Courier New,Courier"><B>%s</B></FONT></MARQUEE></P>' % esc(hp["marquee"]))
        parts.append('<H1><FONT FACE="Arial,Helvetica">%s</FONT></H1>' % esc(hp["title"]))
        parts.append('<IMG SRC="%s" WIDTH=48 HEIGHT=32 BORDER=1 ALT="[Cassette Tape]"><BR>' % ctx.link("asset:badges/cassette.gif", from_dir))
        parts.append('<P>You are listener number:</P>')
        parts.append(counter_html(hp["counter"]))
        parts.append('<P><FONT SIZE=2>Broadcast log updated: %s</FONT></P>' % esc(hp["updated"]))
        parts.append('</CENTER><HR SIZE=3 NOSHADE><A NAME="sections"></A>')
        parts.append(render_sections_html(ctx, hp["sections"], from_dir, hp))
        parts.append('<HR SIZE=3 NOSHADE><A NAME="links"></A><H2><FONT FACE="Arial,Helvetica">&#9733; The Stardust Ring Network</FONT></H2><UL>')
        for l in hp.get("links", []):
            parts.append('<LI><A HREF="%s">%s</A>' % (ctx.link(l["u"], from_dir), esc(l["t"])))
        parts.append('</UL>')
        parts.append('<CENTER><HR SIZE=3 NOSHADE>')
        parts.append(badges_html)
        parts.append(under_construction())
        parts.append('<P><A HREF="mailto:%s">&#9993; Send Mail</A> | <A HREF="mailto:%s?subject=Guestbook">Guestbook</A></P>' % (
            owner["email"], owner["email"]))
        parts.append(webring(ctx, hp["slug"], ring, idx))
        parts.append('<P><FONT SIZE=1>GeoCities Homestead Free Web &middot; Stardust Webring Member Station</FONT></P>')
        parts.append('</CENTER></BODY></HTML>')
        return "\n".join(parts) + "\n"

    # ------------------------------------------------ Layout: SHRINE (Default / Curated)
    else:
        parts.append('<CENTER>')
        if hp.get("marquee"):
            parts.append('<MARQUEE BEHAVIOR=SCROLL SCROLLAMOUNT=4 WIDTH="90%%"><FONT FACE="Courier New,Courier"><B>%s</B></FONT></MARQUEE>' % esc(hp["marquee"]))
        parts.append('<H1><FONT FACE="Arial Black,Arial,Helvetica">%s</FONT></H1>' % esc(hp["title"]))
        if hp.get("image"):
            parts.append('<IMG SRC="%s" WIDTH=240 HEIGHT=240 BORDER=4 ALT="[ SYNTHESIS - Nova Hart - Orion Records 1985 ]" HSPACE=8 VSPACE=8><BR>'
                         '<FONT SIZE=2><I>My original 1985 copy. Scanned at Kinko\'s!</I></FONT>' % (ctx.link(hp["image"], from_dir) if ":" in hp["image"] else hp["image"]))
        parts += ['<P>You are visitor number</P>', counter_html(hp["counter"]),
                  '<P><FONT SIZE=2>Last updated: %s <BLINK><FONT COLOR="#FF0000"><B>NEW!</B></FONT></BLINK></FONT></P>' % esc(hp["updated"]),
                  '</CENTER>', '<HR SIZE=4 NOSHADE>']
        parts.append(render_sections_html(ctx, hp["sections"], from_dir, hp))
        parts.append('<HR SIZE=4 NOSHADE><H2><FONT FACE="Arial,Helvetica">&#9733; Cool Links</FONT></H2><UL>')
        for l in hp.get("links", []):
            parts.append('<LI><A HREF="%s">%s</A>' % (ctx.link(l["u"], from_dir), esc(l["t"])))
        parts += ['</UL>', '<CENTER>', badges_html, under_construction(), '<P>',
                  '<A HREF="mailto:%s">&#9993; Email me!</A> | <A HREF="mailto:%s?subject=Guestbook">Sign my Guestbook</A> | <A HREF="%s">WWW Virtual Library</A>' % (
                      owner["email"], owner["email"], ctx.link("home", from_dir)),
                  '</P>', webring(ctx, hp["slug"], ring, idx),
                  '<P><FONT SIZE=1>Best viewed with Netscape Navigator 2.0 at 640x480. This page is hosted free by GeoCities.<BR>'
                  '<A HREF="index.html">GeoCities Homestead Directory</A></FONT></P>', '</CENTER></BODY></HTML>']
        return "\n".join(parts) + "\n"


def build(ctx, swarm=0):
    curated = [(p["homepage"], p) for p in ctx.personas.values() if p.get("homepage")]
    # Webring order: ring home (Rick's shrine) first, then curated stations, then swarm.
    curated.sort(key=lambda hp: 0 if hp[0]["slug"] == "hollywood-hills-4127" else 1)
    
    clues_manifest = []
    swarm_homes = []
    print(f"Generating {swarm} procedurally expanded GeoCities fan pages...")
    for i in range(swarm):
        hp, owner, clue_rec = generate_swarm_homepage(ctx, i, total_swarm=swarm)
        swarm_homes.append((hp, owner))
        if clue_rec:
            clues_manifest.append(clue_rec)
            
    # Save the private ARG clue manifest (kept in project root, gitignored)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clues_path = os.path.join(root_dir, "site_clues.json")
    with open(clues_path, "w", encoding="utf-8") as fh:
        json.dump({
            "total_clues": len(clues_manifest),
            "clues": clues_manifest
        }, fh, indent=2, ensure_ascii=False)
    print(f"Saved {len(clues_manifest)} clues to private manifest: {clues_path}")

    homes = curated + swarm_homes
    seen = set()
    for hp, _ in homes:
        base, n = hp["slug"], 1
        while hp["slug"] in seen:
            n += 1
            hp["slug"] = "%s-%d" % (base, n)
            hp["path_display"] = "%s-%d" % (hp["path_display"].split("-")[0], n)
        seen.add(hp["slug"])
    ring = [hp["slug"] for hp, _ in homes]
    
    print(f"Writing {len(homes)} HTML homepages to {ctx.out}/geocities/...")
    for idx, (hp, owner) in enumerate(homes):
        rel = "geocities/%s.html" % hp["slug"]
        write(os.path.join(ctx.out, rel), render(ctx, hp, owner, ring, idx))
        ctx.register(rel, "geocities", hp["title"])

    rows = "".join('<TR><TD><TT>%s</TT></TD><TD><A HREF="%s.html">%s</A></TD><TD ALIGN=RIGHT>%d</TD></TR>' % (
        esc(hp["path_display"]), hp["slug"], esc(hp["title"]), hp["counter"]) for hp, _ in homes)
    body = (DOCTYPE + '\n<HTML><HEAD><TITLE>GeoCities - Homestead Directory - %s</TITLE>'
            '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8"></HEAD>\n'
            '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000CC" VLINK="#663399">\n'
            '<CENTER><H1><FONT FACE="Arial,Helvetica" COLOR="#006633">GeoCities</FONT></H1>'
            '<FONT FACE="Arial,Helvetica"><B>Homestead Directory</B> &middot; Free personal homepages in 29 neighborhoods</FONT></CENTER><HR>\n'
            '<H2><A NAME="ring">%s</A> &mdash; %d stations</H2>\n'
            '<P>Webring for fans and researchers of Nova Hart and the 14.2 Hz Stardust signal. Ring home: Rick\'s Nova Hart Shrine.</P>\n'
            '<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0><TR BGCOLOR="#CCFFCC"><TH>Address</TH><TH>Homepage</TH><TH>Visitors</TH></TR>%s</TABLE>\n'
            '<HR><P><A HREF="../index.html">WWW Virtual Library</A></P></BODY></HTML>\n') % (RING, RING, len(homes), rows)
    write(os.path.join(ctx.out, "geocities/index.html"), body)
    ctx.register("geocities/index.html", "geocities-index", "GeoCities Homestead Directory")
    ctx.swarm_geo = ring
    return {"homepages": len(homes), "clues_assigned": len(clues_manifest)}
