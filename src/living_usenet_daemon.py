#!/usr/bin/env python3
"""
Project Stardust — Autonomous "Living Usenet" Chronological Thread Progression Engine
Advances the 1995 Usenet newsgroup spools day-by-day in lockstep with real-world
elapsed days since launch, appending RFC-1036 compliant articles and cross-posted
federated mysteries across:
  - alt.music.heartstrike
  - alt.fan.nova-hart
  - comp.dsp
  - alt.conspiracy
  - comp.sys.ibm-pc.hardware
"""

from __future__ import annotations
import datetime
import html
import json
import time
from pathlib import Path

LAUNCH_EPOCH = 1791763200  # 2026-10-12T00:00:00Z
BASE_1995_DATE = datetime.datetime(1995, 10, 12, 4, 12, 0, tzinfo=datetime.timezone.utc)

CHRONOLOGICAL_DISPATCHES = [
    {
        "day_offset": 0,
        "group": "comp.dsp",
        "from": "m.chen@ee.ashford-poly.org (Dr. Mei-Ling Chen)",
        "subject": "Re: 14.2001 Hz phase-locked sub-carrier in Orion Records master dubs",
        "msgid": "<1995Oct12.041201.9912@ee.ashford-poly.org>",
        "path": "ashpoly!uknet!uunet!comp.dsp",
        "body": """In article <1995Oct10.221904.4102@mit.edu>, r_vance@mit.edu writes:
> Has anyone run a 16384-point Blackman-Harris FFT on the runout groove of
> the 1989 "Tape of Us" rough mix? There is a phase reversal between Left and Right.

We just ran the 3rd-generation dub from Red Coyoacan through our VAXstation 4000
at Ashford Polytechnic (Substation K-7704).

The 330/495/990 Hz chord in the runout is recorded 180 degrees out of phase
between Left and Right (correlation = -0.94). When you sum L+R to mono, the
masking chord drops by 42 dB and reveals a 750 Hz CW Morse burst:
  "SECTOR 5 KEY ASHFORD-KAMOME-1420"

Whoever engineered Sublevel B2 (Marcus Hale's signature is all over the bias
calibration) built a cross-domain lock between our lab and the Akasaka BBS.
See our Fortran-77 PLL filter at /federation/ashford-poly.org/index.html.""",
    },
    {
        "day_offset": 1,
        "group": "alt.fan.nova-hart",
        "from": "kenji_t@kamome-net.org (Kenji Takahashi // PC-9801RA)",
        "subject": "Akasaka Branch closure boxes (31 March 1993) & Robot36 SSTV burst!",
        "msgid": "<1995Oct13.110844.1420@kamome-net.org>",
        "path": "kamome!twics!iiJnet!uunet!alt.fan.nova-hart",
        "body": """Konbanwa from Tokyo/Garden/1420,

Last night at 02:14 UTC while recording the shortwave relay on 6925 kHz,
a Robot36 VIS header (1900 Hz / 1200 Hz sync) broke through right after
the Polish marine bulletin.

When we rasterized the 1500-2300 Hz scanlines in the Signal Lab
(/forensics/signal_lab.html), it drew a floorplan of Orion Sublevel B2-114
pointing to Nevada trunk coordinates 37.242N, 115.810W.

Also: try running `FINGER nova@kamome-net.org` on the VT100 terminal
(/terminal/index.html). Her `.plan` file from 31 March 1993 is still live!""",
    },
    {
        "day_offset": 2,
        "group": "alt.conspiracy",
        "from": "op08@relcom-node08.org (Dimitri V. // Leningrad AX.25 Relay)",
        "subject": "UVB-76 / Bell-103 AFSK Packet Intercept: XOR Dyad Seed 0x3A5F",
        "msgid": "<1995Oct14.021419.0808@relcom-node08.org>",
        "path": "relcom08!demos!fuug!mcsun!uunet!alt.conspiracy",
        "body": """At 02:14 UTC on 4625 kHz, immediately following the Russian buzzer burst,
Relcom Node-08 captured a 110-baud Bell-103 AFSK frame (1270 Hz mark / 1070 Hz space).

Raw hex dump of the AX.25 UI frame:
  RELCOM-NODE08 FRAME // XOR-DYAD: 0x3A5F // SECTOR-5-KEY: ASHFORD-KAMOME-1420

Even stranger: every GeoCities homestead in the Stardust Webring now carries
an `X-Stardust-Memory-Addr` header in the `0x89B2xxxx` range. If you XOR two
paired homesteads with seed `0x3A5F` (type `XOR tokyo-garden-1420 siliconvalley-lab-1984`
in the forensic terminal), it reconstructs lines of `stardust.c`!""",
    },
    {
        "day_offset": 2,
        "group": "alt.music.heartstrike",
        "from": "elena_v@redcoyoacan.org (Elena Villalobos // Mexico DF)",
        "subject": "Heartstrike '86 Monterrey bootleg vs. Steel Thunder soundtrack stem",
        "msgid": "<1995Oct14.051022.7345@redcoyoacan.org>",
        "path": "coyoacan!unam!utexas!uunet!alt.music.heartstrike",
        "body": """Hola todos,

We compared our 2nd-gen CrO2 cassette of Heartstrike's 1986 set against the
*Steel Thunder* VHS hi-fi stereo track. The 6400 Hz FM broadcast lowpass filter
on the Orion promo pressing hides a 14.2 Hz sub-carrier pulse right before
the guitar solo.

We uploaded our tape-exchange matrix notes to the Red Coyoacan mirror
(/federation/redcoyoacan.org/index.html). Don't trust the re-equalized CD reissues—
keep your analog decks calibrated!""",
    },
    {
        "day_offset": 2,
        "group": "comp.sys.ibm-pc.hardware",
        "from": "b_keller@vienna-strasse.at (Bernd Keller)",
        "subject": "Re: 16MB 72-pin EDO SIMMs + Gravis Ultrasound vs. Sound Blaster AWE32",
        "msgid": "<1995Oct14.063011.4419@vienna-strasse.at>",
        "path": "tuwien!mcsun!uunet!comp.sys.ibm-pc.hardware",
        "body": """Anyone telling you that you need more than 16MB of RAM for real-time FFT
waterfall rendering hasn't written tight protected-mode assembly.

With a 486DX2-66, 16MB RAM, and a Sound Blaster 16 (jumper set to IRQ 5, DMA 1),
we are decoding the 14.2001 Hz Stardust telemetry stream in real time without
dropping a single DMA buffer. Check your ISA bus clock divider if your
oscilloscope stutters!""",
    },
]


def render_rfc1036(post: dict, post_date: datetime.datetime) -> str:
    date_str = post_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    from_addr = post["from"].split(" ")[0]
    return (
        f"From {from_addr} {post_date.strftime('%a %b %d %H:%M:%S %Y')}\n"
        f"Path: {post['path']}\n"
        f"From: {post['from']}\n"
        f"Newsgroups: {post['group']}\n"
        f"Subject: {post['subject']}\n"
        f"Message-ID: {post['msgid']}\n"
        f"Date: {date_str}\n"
        f"X-Stardust-Carrier: 14.2001 Hz Phase-Locked\n\n"
        f"{post['body']}\n"
    )


def build_living_usenet(site_dir: Path, now_ts: float | None = None) -> dict:
    now = now_ts if now_ts is not None else time.time()
    elapsed_days = max(2, int((now - LAUNCH_EPOCH) // 86400))
    usenet_root = site_dir / "usenet"
    usenet_root.mkdir(parents=True, exist_ok=True)

    active_posts = [p for p in CHRONOLOGICAL_DISPATCHES if p["day_offset"] <= elapsed_days]
    written_files = []

    by_group: dict[str, list[tuple[str, dict, datetime.datetime]]] = {}
    for idx, post in enumerate(active_posts, start=901):
        pdate = BASE_1995_DATE + datetime.timedelta(days=post["day_offset"], hours=idx % 5)
        spool_name = f"s{idx:05d}.txt"
        grp_dir = usenet_root / post["group"]
        grp_dir.mkdir(parents=True, exist_ok=True)
        spool_path = grp_dir / spool_name
        spool_path.write_text(render_rfc1036(post, pdate), encoding="utf-8")
        written_files.append(str(spool_path))
        by_group.setdefault(post["group"], []).append((spool_name, post, pdate))

    # Write a Living Usenet Live Feed HTML index at site/usenet/live_1995_feed.html
    rows_html = []
    for grp, items in sorted(by_group.items()):
        rows_html.append(f"<H2>Newsgroup: <TT>{html.escape(grp)}</TT></H2><UL>")
        for spool_name, post, pdate in items:
            d_short = pdate.strftime("%Y-%m-%d %H:%M UTC")
            rows_html.append(
                f'<LI><B><A HREF="/usenet/{html.escape(grp)}/{spool_name}">{html.escape(post["subject"])}</A></B> '
                f'&mdash; <I>{html.escape(post["from"])}</I> <TT>[{d_short}]</TT></LI>'
            )
        rows_html.append("</UL>")

    feed_html = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<HTML><HEAD><TITLE>USENET SPOOL // OCTOBER 1995 LIVE CHRONOLOGICAL FEED</TITLE>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
<META NAME="description" CONTENT="October 1995 Usenet Newsgroup Spool Feed — Ashford Polytechnic, Kamome-Net, Relcom Node-08, and Red Coyoacan.">
</HEAD>
<BODY BGCOLOR="#000000" TEXT="#CCCCCC" LINK="#33FF33" VLINK="#00AA00">
<PRE>
========================================================================
 INN 1.4unoff3 // STARDUST USENET SPOOL FEED (SIMULATED CLOCK: OCT 1995)
 ACTIVE GROUPS: alt.music.heartstrike | alt.fan.nova-hart | comp.dsp
                alt.conspiracy | comp.sys.ibm-pc.hardware
========================================================================
</PRE>
{"".join(rows_html)}
<HR>
<P><FONT SIZE=2>[ <A HREF="/terminal/index.html">Open VT100 Forensic Terminal</A> |
<A HREF="/forensics/signal_lab.html">Open SSTV / AFSK Signal Lab</A> |
<A HREF="/federation/ashford-poly.org/index.html">Sister Domain Federation</A> ]</FONT></P>
</BODY></HTML>
"""
    feed_path = usenet_root / "live_1995_feed.html"
    feed_path.write_text(feed_html, encoding="utf-8")
    written_files.append(str(feed_path))
    return {"elapsed_days": elapsed_days, "articles_written": len(active_posts), "files": written_files}


if __name__ == "__main__":
    out = build_living_usenet(Path("/tmp/stardust_expansion/site"))
    print(json.dumps(out, indent=2))
