"""GeoCities-era (1995-1996) HTML 3.2 homepage generator with webrings and hit counters."""
import json
import os

from common import esc, relay_table_lines, rng_for, write
from swarm_corner import generate_swarm_homepage

DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
RING = "The Stardust Webring"

HOOD_THEMES = {
    "SiliconValley/Lab": "DSP Hackers, Hardware Modems, Audio Spectrograms",
    "Hollywood/Hills": "Nova Hart Shrines, Los Angeles Lore, Media Archives",
    "SunsetStrip/Club": "80s Synthpop, Tape Trading Clubs, Neon Aesthetics",
    "Area51/Vault": "Government Conspiracies, Marcus Hale Case Files",
    "Tokyo/Garden": "Akasaka Master Tapes, PC-98 Users, J-Pop Otaku",
    "Athens/Forum": "University DSP Researchers, Fourier Analysis Labs",
    "Paris/LeftBank": "European Fan Clubs, 3615 Minitel Transmissions",
    "CapeCanaveral/Lab": "Satellite Telemetry, Microwave Relay Links",
    "Heartland/Plains": "Midwest Tape Traders, Ham Radio Enthusiasts",
    "SoHo/Studio": "Underground Cassette Culture, Synthwave Aesthetics",
    "Vienna/Strasse": "German & Austrian Broadcast Archives",
    "Colosseum/Field": "International Pen-Pals, Vinyl Collectors",
    "TimesSquare/Arcade": "East Coast Synth Fans, 80s Billboard Lore",
    "Nashville/Opry": "Session Musicians, Studio Vocal Analysis",
    "RainForest/Canopy": "South American Transmissions, Red Saturno BBS",
    "Pentagon/Quarters": "DoD Declassified Signal Intercepts",
    "BourbonStreet/Delta": "Southern Audio Engineers, Reel-to-Reel Collectors",
    "EnchantedForest/Glade": "Fantasy & Anime Fan Art, Tribute Pages",
}


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


def midi_jukebox_html(ctx, from_dir):
    midis = [
        ("gasoline_heart", "Gasoline Heart (ガソリン・ハート)", "1985 J-Rock / Synthpop", "7.3 KB"),
        ("ghost_transit", "Ghost Transit (ゴースト・トランジット)", "1985 Atmospheric Ballad", "4.3 KB"),
        ("midnight_animal", "Midnight Animal (ミッドナイト・アニマル)", "1986 Funky City Pop", "6.7 KB"),
        ("brighter_than_sun", "Brighter Than The Sun (太陽よりも、輝いて！)", "1987 80s Idol Anthem", "9.9 KB"),
        ("only_we_remain", "Only We Remain (残されたのは、私たちだけ)", "1989 Kayokyoku Ballad", "4.3 KB"),
        ("synthetic_dawn", "Synthetic Dawn", "1985 Industrial Synthwave", "3.7 KB"),
        ("memory_hatch", "Memory Hatch", "1985 Sophisti-Pop / Rhodes", "3.5 KB"),
    ]
    rows = []
    for slug, title, genre, sz in midis:
        m_link = ctx.link(f"asset:midi/{slug}.mid", from_dir)
        rows.append('<TR><TD><FONT FACE="Arial,Helvetica" SIZE=2><B>%s</B></FONT></TD><TD><FONT FACE="Arial,Helvetica" SIZE=2>%s</FONT></TD><TD ALIGN=RIGHT><TT>%s</TT></TD><TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE=2>[ <A HREF="%s"><B>DOWNLOAD .MID</B></A> ]</FONT></TD></TR>' % (
            esc(title), esc(genre), sz, m_link))
    return ('<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 BGCOLOR="#000000" WIDTH="92%%">'
            '<TR BGCOLOR="#222255"><TH><FONT COLOR="#FFFF00" FACE="Arial,Helvetica" SIZE=2>TRACK TITLE</FONT></TH><TH><FONT COLOR="#FFFF00" FACE="Arial,Helvetica" SIZE=2>GENRE / STYLE</FONT></TH><TH><FONT COLOR="#FFFF00" FACE="Arial,Helvetica" SIZE=2>SIZE</FONT></TH><TH><FONT COLOR="#FFFF00" FACE="Arial,Helvetica" SIZE=2>GENERAL MIDI</FONT></TH></TR>'
            + "".join(rows) + '</TABLE>')


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
        if s.get("midi_list"):
            sec_parts.append("<CENTER>" + midi_jukebox_html(ctx, from_dir) + "</CENTER>")
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
    ]
    if hp.get("midi"):
        m_link = ctx.link(hp["midi"], from_dir)
        parts.append('<BGSOUND SRC="%s" LOOP="INFINITE">' % m_link)
        parts.append('<EMBED SRC="%s" AUTOSTART="TRUE" LOOP="TRUE" HIDDEN="TRUE" WIDTH="0" HEIGHT="0">' % m_link)
    parts.append('<FONT SIZE=1 FACE="Arial,Helvetica">GeoCities &gt; %s</FONT>' % esc(" > ".join(hp["path_display"].split("/"))))
    
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

    # 1. Curated Archive / Ring Hub Table
    curated_rows = []
    for hp, _ in curated:
        curated_rows.append(
            '<TR><TD><TT>%s</TT></TD><TD><A HREF="%s.html"><B>%s</B></A></TD><TD ALIGN=RIGHT><FONT COLOR="#006600"><B>%d</B></FONT></TD></TR>' % (
                esc(hp["path_display"]), hp["slug"], esc(hp["title"]), hp["counter"]))

    # 2. Neighborhood Summary Table
    hood_map = {}
    for hp, _ in homes:
        parts = hp["path_display"].split("/")
        hood_prefix = "/".join(parts[:2]) if len(parts) >= 2 else parts[0]
        if hood_prefix not in hood_map:
            hood_map[hood_prefix] = []
        hood_map[hood_prefix].append(hp)
    
    hood_rows = []
    for hood in sorted(hood_map.keys()):
        h_list = hood_map[hood]
        theme = HOOD_THEMES.get(hood, "Early Web Fan Community")
        sample_hp = h_list[0]
        hood_rows.append(
            '<TR><TD><B><FONT FACE="Arial,Helvetica">%s</FONT></B></TD><TD><FONT SIZE=2>%s</FONT></TD><TD ALIGN=RIGHT><B>%d</B></TD><TD><FONT SIZE=2><A HREF="%s.html">%s</A></FONT></TD></TR>' % (
                esc(hood), esc(theme), len(h_list), sample_hp["slug"], esc(sample_hp["title"])))

    # 3. Active Stations Spotlight (Top 60 stations by counter)
    spotlight_sorted = sorted(swarm_homes, key=lambda x: x[0]["counter"], reverse=True)[:60]
    spotlight_rows = []
    for hp, _ in spotlight_sorted:
        spotlight_rows.append(
            '<TR><TD><TT>%s</TT></TD><TD><A HREF="%s.html">%s</A></TD><TD ALIGN=RIGHT>%d</TD></TR>' % (
                esc(hp["path_display"]), hp["slug"], esc(hp["title"]), hp["counter"]))

    rand_slug = ring[rng_for(ctx.seed, "index_rand").randrange(len(ring))]

    body = (
        DOCTYPE + '\n<HTML><HEAD><TITLE>GeoCities - Homestead Directory - %s</TITLE>'
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">'
        '<META NAME="description" CONTENT="Official GeoCities Homestead Directory for The Stardust Webring, cataloguing over 5,000 personal fan pages.">'
        '</HEAD>\n'
        '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000CC" VLINK="#663399" ALINK="#FF0000">\n'
        '<CENTER>\n'
        '<TABLE BORDER=0 CELLPADDING=4 CELLSPACING=0 WIDTH="95%%"><TR><TD ALIGN=CENTER>'
        '<H1><FONT FACE="Arial Black,Arial,Helvetica" COLOR="#006633">GeoCities</FONT></H1>'
        '<FONT FACE="Arial,Helvetica" SIZE=3><B>HOMESTEAD DIRECTORY &middot; THE STARDUST WEBRING</B></FONT><BR>'
        '<FONT SIZE=2>Official registry of %d member fan stations across %d virtual neighborhoods &middot; CERN-HTTPd 3.0</FONT>'
        '</TD></TR></TABLE>\n'
        '<HR SIZE=3 NOSHADE>\n'
        '<P>[ <A HREF="hollywood-hills-4127.html">&#9733; Ring Home (Rick\'s Shrine)</A> | '
        '<A HREF="%s.html">Random Member Station</A> | '
        '<A HREF="#neighborhoods">Browse Neighborhoods</A> | '
        '<A HREF="#spotlight">Top Stations Spotlight</A> | '
        '<A HREF="../index.html">WWW Virtual Library</A> ]</P>\n'
        '</CENTER>\n'
        '<A NAME="ring"></A>\n'
        '<H2><FONT FACE="Arial,Helvetica" COLOR="#003366">&#9733; Ring Home &amp; Featured Homesteads</FONT></H2>\n'
        '<P>Core research outposts, signal analysis labs, and original tape archives curated by the Stardust community:</P>\n'
        '<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFFFFF">'
        '<TR BGCOLOR="#CCFFCC"><TH><FONT FACE="Arial,Helvetica">Address</FONT></TH><TH><FONT FACE="Arial,Helvetica">Homepage Title &amp; Archive</FONT></TH><TH><FONT FACE="Arial,Helvetica">Visitors</FONT></TH></TR>\n'
        '%s</TABLE>\n'
        '<HR SIZE=2 NOSHADE>\n'
        '<A NAME="neighborhoods"></A>\n'
        '<H2><FONT FACE="Arial,Helvetica" COLOR="#003366">&#9733; Neighborhood Directory (%d Communities)</FONT></H2>\n'
        '<P>Personal homepages grouped by GeoCities theme. Each neighborhood hosts hundreds of independent member shrines:</P>\n'
        '<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFFFFF">'
        '<TR BGCOLOR="#E6F2FF"><TH><FONT FACE="Arial,Helvetica">Neighborhood</FONT></TH><TH><FONT FACE="Arial,Helvetica">Community Focus &amp; Archive Theme</FONT></TH><TH><FONT FACE="Arial,Helvetica">Stations</FONT></TH><TH><FONT FACE="Arial,Helvetica">Sample Homestead</FONT></TH></TR>\n'
        '%s</TABLE>\n'
        '<HR SIZE=2 NOSHADE>\n'
        '<A NAME="spotlight"></A>\n'
        '<H2><FONT FACE="Arial,Helvetica" COLOR="#003366">&#9733; Active Member Stations Spotlight (Top 60)</FONT></H2>\n'
        '<P>High-traffic personal homepages logged by the Stardust webring crawler:</P>\n'
        '<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFFFFF">'
        '<TR BGCOLOR="#FFFFCC"><TH><FONT FACE="Arial,Helvetica">Address</FONT></TH><TH><FONT FACE="Arial,Helvetica">Station Title</FONT></TH><TH><FONT FACE="Arial,Helvetica">Visitors</FONT></TH></TR>\n'
        '%s</TABLE>\n'
        '<HR SIZE=3 NOSHADE>\n'
        '<CENTER>\n'
        '<P><FONT SIZE=2>Hosted free by <B>GeoCities</B> &middot; The web\'s premier homestead community.<BR>'
        'Best viewed with <B>Netscape Navigator 2.0</B> at 640x480 &middot; Keep the channels open.</FONT></P>\n'
        '</CENTER></BODY></HTML>\n'
    ) % (
        RING, len(homes), len(hood_map), rand_slug,
        "".join(curated_rows),
        len(hood_map), "".join(hood_rows),
        "".join(spotlight_rows)
    )
    write(os.path.join(ctx.out, "geocities/index.html"), body)
    ctx.register("geocities/index.html", "geocities-index", "GeoCities Homestead Directory")
    ctx.swarm_geo = ring
    return {"homepages": len(homes), "clues_assigned": len(clues_manifest)}
