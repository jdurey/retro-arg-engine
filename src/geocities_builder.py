"""GeoCities-era (1995-1996) HTML 3.2 homepage generator with webrings and hit counters."""
import os

from common import esc, relay_table_lines, rng_for, write

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


def render(ctx, hp, owner, ring, idx):
    from_dir = "geocities"
    parts = [DOCTYPE, '<HTML LANG="%s"><HEAD><TITLE>%s</TITLE>' % (hp.get("lang", "en"), esc(hp["title"])),
             '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">',
             '<META NAME="description" CONTENT="%s">' % esc(hp["title"] + " - a personal homepage at GeoCities " + hp["path_display"]),
             '<META NAME="keywords" CONTENT="Nova Hart, SYNTHESIS, Orion Records, Marcus Hale, Stardust, 14.2 Hz">',
             '</HEAD>',
             '<BODY BGCOLOR="%s" TEXT="%s" LINK="%s" VLINK="%s" ALINK="#FF0000">' % (hp["bg"], hp["text"], hp["link"], hp["vlink"]),
             '<FONT SIZE=1 FACE="Arial,Helvetica">GeoCities &gt; %s</FONT>' % esc(" > ".join(hp["path_display"].split("/"))),
             '<CENTER>']
    if hp.get("marquee"):
        parts.append('<MARQUEE BEHAVIOR=SCROLL SCROLLAMOUNT=4 WIDTH="90%%"><FONT FACE="Courier New,Courier"><B>%s</B></FONT></MARQUEE>' % esc(hp["marquee"]))
    parts.append('<H1><FONT FACE="Arial Black,Arial,Helvetica">%s</FONT></H1>' % esc(hp["title"]))
    if hp.get("image"):
        parts.append('<IMG SRC="%s" WIDTH=240 HEIGHT=240 BORDER=4 ALT="[ SYNTHESIS - Nova Hart - Orion Records 1985 ]" HSPACE=8 VSPACE=8><BR>'
                     '<FONT SIZE=2><I>My original 1985 copy. Scanned at Kinko\'s!</I></FONT>' % (ctx.link(hp["image"], from_dir) if ":" in hp["image"] else hp["image"]))
    parts += ['<P>You are visitor number</P>', counter_html(hp["counter"]),
              '<P><FONT SIZE=2>Last updated: %s <BLINK><FONT COLOR="#FF0000"><B>NEW!</B></FONT></BLINK></FONT></P>' % esc(hp["updated"]),
              '</CENTER>', '<HR SIZE=4 NOSHADE>']
    for s in hp["sections"]:
        parts.append('<H2><FONT FACE="Arial,Helvetica">&#9733; %s</FONT></H2>' % esc(s["h"]))
        if s.get("img"):
            parts.append('<CENTER><IMG SRC="%s" WIDTH=%d HEIGHT=%d BORDER=2 ALT="%s"><BR><FONT SIZE=2><I>%s</I></FONT></CENTER>' % (
                ctx.link(s["img"], from_dir), s.get("w", 320), s.get("h", 240), esc(s.get("alt", "")), esc(s.get("caption", ""))))
        for p in s.get("p", []):
            parts.append("<P>%s</P>" % esc(p))
        if s.get("list"):
            parts.append("<UL>" + "".join("<LI>%s" % esc(i) for i in s["list"]) + "</UL>")
        if s.get("pre"):
            parts.append("<PRE>%s</PRE>" % esc("\n".join(s["pre"])))
        if s.get("relay_table"):
            parts.append("<CENTER>" + relay_table_html(ctx.lore, hp) + "</CENTER>")
    parts.append('<HR SIZE=4 NOSHADE><H2><FONT FACE="Arial,Helvetica">&#9733; Cool Links</FONT></H2><UL>')
    for l in hp.get("links", []):
        parts.append('<LI><A HREF="%s">%s</A>' % (ctx.link(l["u"], from_dir), esc(l["t"])))
    parts += ['</UL>', '<CENTER>', under_construction(), '<P>',
              '<A HREF="mailto:%s">&#9993; Email me!</A> | <A HREF="mailto:%s?subject=Guestbook">Sign my Guestbook</A> | <A HREF="%s">WWW Virtual Library</A>' % (
                  owner["email"], owner["email"], ctx.link("home", from_dir)),
              '</P>', webring(ctx, hp["slug"], ring, idx),
              '<P><FONT SIZE=1>Best viewed with Netscape Navigator 2.0 at 640x480. This page is hosted free by GeoCities.<BR>'
              '<A HREF="index.html">GeoCities Homestead Directory</A></FONT></P>', '</CENTER></BODY></HTML>']
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------- swarm
HOODS = ["SiliconValley/Lab", "Hollywood/Hills", "SunsetStrip/Club", "Area51/Vault", "Tokyo/Garden", "Athens/Forum",
         "Paris/LeftBank", "CapeCanaveral/Lab", "Heartland/Plains", "SoHo/Studio", "Vienna/Strasse", "Colosseum/Field",
         "TimesSquare/Arcade", "Nashville/Opry", "RainForest/Canopy", "Pentagon/Quarters", "BourbonStreet/Delta", "EnchantedForest/Glade"]
NAMES = ["Kim", "Jess", "Marco", "Aiko", "Pete", "Sven", "Lucia", "Nadia", "Chris", "Hana", "Jordan", "Mateo", "Ines", "Ollie", "Priya", "Tobias", "Min-jun", "Camila"]
CITIES = ["Ohio", "Osaka", "Hamburg", "Guadalajara", "Busan", "Leeds", "Lyon", "Porto Alegre", "Uppsala", "St. Petersburg", "Perth", "Toronto", "Austin", "Kyoto"]
PALETTES = [("#000000", "#00FF00", "#FF00FF", "#AA00AA"), ("#FFFFCC", "#000066", "#CC0000", "#660000"), ("#000080", "#FFFFFF", "#FFFF00", "#FFCC00"),
            ("#330000", "#FFCC99", "#FF6600", "#CC6600"), ("#E0E0E0", "#000000", "#0000FF", "#800080"), ("#001010", "#99FFFF", "#FF99CC", "#CC6699")]
THEORIES = [
    "I think Marcus is still out there, hiding in plain sight. Kestrel said ask WHERE not WHO.",
    "My theory: Luna Gray is literally the 'copy' from line 5. Orion built her after the fire.",
    "The 14.2 Hz thing is an error-correction code for Nova's voice. Read the patent, claim 5!!",
    "Line 14 will be broadcast when all the countries find their Marcus at the same time. I believe it.",
    "Nova was too heavy for this world. 7 sigma! Even the physicists say so.",
    "Every pressing is a piece of a person. We are putting someone back together.",
    "The whisper at the end of the Akasaka tape says June 2025. I'm writing it on my wall so I don't forget. Keep the channels open.",
    "The Idol Protocol songs are her smiling because they made her. Listen to Ghost in the Chorus with headphones. Wa-ta-shi-o-ke-su.",
]
TRACKS = ["Synthetic Dawn", "Memory Hatch", "Threshold", "Memory Hatch (City Pop Version)"]


def swarm_homepage(ctx, i):
    r = rng_for(ctx.seed, "swarm-geo", i)
    hood = r.choice(HOODS)
    num = r.randint(1000, 9999)
    name, city = r.choice(NAMES), r.choice(CITIES)
    bg, text, link, vlink = r.choice(PALETTES)
    slug = ("%s-%d" % (hood.replace("/", "-"), num)).lower()
    hp = {"slug": slug, "path_display": "%s/%d" % (hood, num), "title": "%s's Nova Hart Corner" % name,
          "bg": bg, "text": text, "link": link, "vlink": vlink, "counter": r.randint(12, 9999),
          "updated": "199%d-%02d-%02d" % (r.choice([5, 6]), r.randint(1, 12), r.randint(1, 28)), "lang": "en",
          "marquee": r.choice(["~ hold for relay ~", "welcome station!!", "NOVA HART 4EVER", "the hatch is open"]),
          "sections": [
              {"h": "Hi!", "p": ["My name is %s and I live in %s. I found out about the Stardust signal on the Internet and now I can't stop thinking about it." % (name, city)]},
              {"h": "Favorite Song", "p": ["'%s' -- I play it every night." % r.choice(TRACKS)]},
              {"h": "My Theory", "p": [r.choice(THEORIES)]}],
          "links": [{"t": "Rick's Nova Hart Shrine (ring home)", "u": "geo:hollywood-hills-4127"},
                    {"t": "alt.music.synth-pop", "u": "usenetgroup:alt.music.synth-pop"}]}
    owner = {"email": "%s%d@pacnet-online.com" % (name.lower().replace("-", ""), num)}
    return hp, owner


def build(ctx, swarm=0):
    curated = [(p["homepage"], p) for p in ctx.personas.values() if p.get("homepage")]
    # Webring order: ring home (Rick's shrine) first, then curated stations, then swarm.
    curated.sort(key=lambda hp: 0 if hp[0]["slug"] == "hollywood-hills-4127" else 1)
    homes = curated + [swarm_homepage(ctx, i) for i in range(swarm)]
    seen = set()
    for hp, _ in homes:
        base, n = hp["slug"], 1
        while hp["slug"] in seen:
            n += 1
            hp["slug"] = "%s-%d" % (base, n)
            hp["path_display"] = "%s-%d" % (hp["path_display"].split("-")[0], n)
        seen.add(hp["slug"])
    ring = [hp["slug"] for hp, _ in homes]
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
    return {"homepages": len(homes)}
