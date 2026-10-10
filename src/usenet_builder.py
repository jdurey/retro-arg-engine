"""Procedural RFC-822 / RFC-1036 Usenet thread generator.

Curated thread seeds (data/lore_seeds.json) are wrapped with authentic headers,
bang-path routing, quoting, attributions and signatures. `swarm` threads are
generated procedurally from templates at zero token cost.
"""
import datetime
import os

from common import esc, group_slug, relay_table_lines, rng_for, write
import usenet_bank as ub

# Fictional UUCP backbone per regional node -> bang path toward the reading site.
NODE_ROUTES = {
    "01": ["bigsur", "cascade"],
    "02": ["kamome", "jpgate", "pacrim", "bigsur"],
    "03": ["eunha", "krgate", "pacrim", "bigsur"],
    "04": ["coyoacan", "mxgate", "cascade"],
    "05": ["hansebox", "eunet-de", "transat", "cascade"],
    "06": ["teletel", "eunet-fr", "transat", "cascade"],
    "07": ["fennimore", "ukc", "transat", "cascade"],
    "08": ["kiae", "relcom", "eunet-fi", "transat", "cascade"],
    "09": ["saturno", "brgate", "cascade"],
    "10": ["nordrelay", "sunet", "transat", "cascade"],
}
READER_SITE = "ashpoly"
GROUP_ORGS = {
    "comp.dsp": "Discussion of digital signal processing",
    "comp.sys.m68k": "Discussion of Motorola 68k-based systems",
    "alt.conspiracy": "Be paranoid -- they're out to get you",
    "alt.music.synth-pop": "Synthesizer-driven pop music, old and new",
    "alt.fan.nova-hart": "Nova Hart, SYNTHESIS, and the people looking for her",
    "news.groups": "Discussions and lists of newsgroups",
}


def faq_lines(lore, as_of="9999-12-31"):
    mv = lore["movement"]
    out = [
        "Archive-name: music/nova-hart/humans-for-nova-faq",
        "Posting-frequency: monthly (1st of month, 00:14 UTC)",
        "Version: 2.4",
        "",
        "        H U M A N S   F O R   N O V A",
        "        Frequently Asked Questions",
        "",
        "  '%s'" % mv["origin"].split(": ", 1)[-1].strip("'"),
        "",
        "Q1. What is Humans for Nova?",
        "    A loose, unincorporated network of listeners, engineers and fans who",
        "    want to know what happened to Nova Hart, why her broadcasts stopped in",
        "    December 1989, and where Marcus Hale ('the Architect') went. Nobody",
        "    is in charge. There are no dues. There is a mailing list.",
        "",
        "Q2. Where did the name come from?",
        "    %s" % mv["origin"],
        "",
        "Q3. How big is it?",
        "    DATE        MEMBERS  EVENT",
    ]
    for ms in [x for x in mv["milestones"] if x["date"] <= as_of]:
        words, line = ms["event"].split(), ""
        rows = []
        for w in words:
            if len(line) + len(w) + 1 > 50:
                rows.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
        rows.append(line)
        out.append("    %s  %7s  %s" % (ms["date"], "{:,}".format(ms["members"]), rows[0]))
        out += ["    %s  %7s  %s" % (" " * 10, "", r) for r in rows[1:]]
    out += ["    (Membership = nova-l subscribers + chapter rolls. Rough. Honest.)", "",
            "Q4. Is there a chapter near me?"]
    out += ["    %-28s since %d   %s" % (c["city"], c["founded"], c["contact"]) for c in mv["chapters"] if c["founded"] <= int(as_of[:4])]
    out += ["",
            "Q5. What is a Listening Night?",
            "    Every 9 September at 02:14 UTC we each play 'Threshold' from our own",
            "    pressing, wherever we are, and log in to say we did. Bring your own",
            "    pressing. Nobody hears anything new. Everybody comes back.",
            "",
            "Q6. How do I listen for the carrier myself?",
            "    Get stardust.c from ftp.ashford-poly.edu:/pub/telecom-archives/stardust/",
            "    (mirrors in /pub/mirrors/stardust on most big archive sites). You need",
            "    a clean transfer of a 1985 pressing, a sound card or ADC, and patience.",
            "",
            "Q7. What are the slogans about?"]
    out += ["    * %s" % s for s in mv["slogans"]]
    out += ["",
            "Q8. Is Nova Hart a real person?",
            "    This FAQ takes no position. Read the spectra. Read the memo. Decide.",
            "",
            "Q9. Orion sent me a letter.",
            "    Don't post Orion's masters. Do post your measurements. Measuring a",
            "    record you own is listening, not piracy. See news.groups, July 1994.",
            "",
            "Q10. What does 'Keep the channels open' mean?",
            "    Nobody knows. See the Akasaka reel, ftp.kamome-net.or.jp, May 1995.",
            "",
            "-- end of FAQ --"]
    return out


def newsreader(year, rng):
    if year < 1991:
        return rng.choice(["rn 4.3", "rn 4.3 patchlevel 1", "vnews 2.11"])
    if year < 1994:
        return rng.choice(["TIN [version 1.1 PL8]", "trn 2.5", "rn 4.4", "NN version 6.4.16"])
    return rng.choice(["TIN [version 1.2 PL2]", "NewsWatcher 2.0b24", "WinVN 0.99.5", "Netscape 1.1N"])


def fmt_date(dt):
    if dt.year < 1992:
        return dt.strftime("%d %b %y %H:%M:%S GMT").lstrip("0")
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")


def msg_id(dt, host, rng):
    return "<%s.%04d@%s>" % (dt.strftime("%Y%b%d.%H%M%S"), rng.randint(1000, 9999), host)


def build_thread(ctx, thread, rng):
    lore = ctx.lore
    dt = datetime.datetime.strptime(thread["start"], "%Y-%m-%dT%H:%M:%S")
    built = []
    for i, m in enumerate(thread["messages"]):
        p = ctx.personas[m["from"]]
        login, host = p["email"].split("@", 1)
        if i:
            dt = dt + datetime.timedelta(minutes=rng.randint(45, 60 * 52))
        mid = msg_id(dt, host, rng)

        # Body assembly
        own = []
        if "body_doc" in m:
            own = m.get("preface", []) + ["  " + l if l else "" for l in lore["documents"][m["body_doc"]]]
        elif m.get("body_relay_table"):
            own = m.get("preface", []) + relay_table_lines(lore) + m.get("postscript", [])
        elif m.get("body_faq"):
            own = faq_lines(lore, thread["start"][:10])
        else:
            own = list(m["body"])

        text = []
        refs = []
        if "reply_to" in m:
            parent = built[m["reply_to"]]
            refs = (parent["refs"] + [parent["mid"]])[-6:]
            text.append("In article %s, %s (%s) writes:" % (parent["mid"], parent["persona"]["email"], parent["persona"]["name"]))
            quoted = [l for l in parent["own"] if l.strip()][: m.get("quote", 2)]
            text += [">" + (" " + l if not l.startswith(">") else l) for l in quoted]
            text.append("")
        text += own
        text += ["", "-- "] + p["sig"]

        route = NODE_ROUTES.get(p["node"], ["cascade"])
        path = "!".join([READER_SITE] + list(reversed(route)) + [host.split(".")[0], login])
        subject = thread["subject"] if i == 0 else "Re: " + thread["subject"]
        headers = [
            ("Path", path),
            ("From", "%s (%s)" % (p["email"], p["name"])),
            ("Newsgroups", thread["group"]),
            ("Subject", subject),
            ("Message-ID", mid),
            ("Date", fmt_date(dt)),
        ]
        if refs:
            headers.append(("References", " ".join(refs)))
        headers.append(("Organization", p["org"]))
        if dt.year >= 1992:
            headers.append(("NNTP-Posting-Host", host))
        headers.append(("X-Newsreader", newsreader(dt.year, rng)))
        if p["id"] == "kestrel":
            headers.append(("X-Anonymously-To", thread["group"]))
            headers.append(("Comments", "This message was forwarded by an anonymous remailer."))
        headers.append(("Lines", str(len(text))))
        built.append({"mid": mid, "refs": refs, "persona": p, "own": own, "dt": dt, "headers": headers, "text": text, "subject": subject})
    return built


def render_thread_txt(thread, built):
    out = []
    for i, b in enumerate(built):
        out.append("From %s %s" % (b["persona"]["email"], b["dt"].strftime("%a %b %d %H:%M:%S %Y")))
        out += ["%s: %s" % kv for kv in b["headers"]]
        out.append("")
        out += b["text"]
        out.append("")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- swarm
def swarm_threads(ctx, count):
    return ub.build_swarm_threads(ctx, count)



# --------------------------------------------------------------------------- pages
def page(title, body):
    return ('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<HTML><HEAD><TITLE>%s</TITLE>'
            '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8"></HEAD>\n'
            '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000EE" VLINK="#551A8B">\n%s\n</BODY></HTML>\n') % (esc(title), body)


def build(ctx, swarm=0):
    threads = list(ctx.lore["usenet_threads"]) + swarm_threads(ctx, swarm)
    by_group = {}
    for t in threads:
        rng = rng_for(ctx.seed, "thread", t["id"])
        built = build_thread(ctx, t, rng)
        rel = "usenet/%s/%s.txt" % (group_slug(t["group"]), t["id"])
        write(os.path.join(ctx.out, rel), render_thread_txt(t, built))
        ctx.register(rel, "usenet-thread", t["subject"])
        by_group.setdefault(t["group"], []).append((t, built))

    # Per-group overview, styled after a tin/rn thread selector over an HTTP gateway.
    for g, items in sorted(by_group.items()):
        items.sort(key=lambda x: x[1][0]["dt"])
        rows = []
        for n, (t, built) in enumerate(items, 1):
            rows.append('%4d  %s %3d  <A HREF="%s.txt">%-58s</A>  %s' % (
                n, "+" if not t.get("swarm") else " ", len(built), t["id"], esc(t["subject"][:58]), esc(built[0]["persona"]["name"])))
        body = ("<H1>%s</H1>\n<P><I>%s</I></P>\n<PRE>\n    #  T  MSG  SUBJECT%sAUTHOR\n%s\n</PRE>\n<HR>\n"
                '<P><A HREF="../index.html">All newsgroups</A> | <A HREF="../../index.html">WWW Virtual Library</A></P>\n'
                "<ADDRESS>INN 1.4unoff3 / NNTP-HTTP gateway -- %d articles</ADDRESS>") % (
            esc(g), esc(GROUP_ORGS.get(g, "")), " " * 53, "\n".join(rows), sum(len(b) for _, b in items))
        rel = "usenet/%s/index.html" % group_slug(g)
        write(os.path.join(ctx.out, rel), page("News: " + g, body))
        ctx.register(rel, "usenet-group", g)

    lines = ['<A HREF="%s/index.html">%-24s</A> %5d %5d y   %s' % (group_slug(g), esc(g), len(i), sum(len(b) for _, b in i), esc(GROUP_ORGS.get(g, "")))
             for g, i in sorted(by_group.items())]
    body = ("<H1>Usenet News Archive</H1>\n<P>Selected newsgroups mirrored from the Ashford Polytechnic news spool. "
            "Articles are preserved verbatim with original headers.</P>\n<PRE>\nGROUP                    THRDS  ARTS MOD  DESCRIPTION\n%s\n</PRE>\n"
            '<HR><P><A HREF="../index.html">Back to the WWW Virtual Library</A></P>') % "\n".join(lines)
    write(os.path.join(ctx.out, "usenet/index.html"), page("Usenet News Archive", body))
    ctx.register("usenet/index.html", "usenet-index", "Usenet News Archive")
    return {"threads": len(threads), "articles": sum(len(b) for i in by_group.values() for _, b in i), "groups": len(by_group)}
