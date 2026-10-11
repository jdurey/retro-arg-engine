// HTML 3.2 renderer for swarm v3 pages. Emits final public URLs directly (no
// HTMLRewriter pass needed at the edge).

import { publicUrl } from "../urlmap.js";

export const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
// Bank fragments may carry <b>/<i>; everything else is escaped.
const frag = (s) => esc(s).replace(/&lt;(\/?)([bi])&gt;/gi, "<$1$2>");

const DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">';
const RING = "The Stardust Webring";
const geoUrl = (slug) => publicUrl(`geocities/${slug}.html`);

export function counterHtml(n, style) {
  const digits = String(n).padStart(6, "0");
  if (style === "text") return `<B>${digits}</B>`;
  if (style === "bracket") return `<TT>[ ${digits} ]</TT>`;
  return '<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0><TR>' +
    [...digits].map((d) => `<TD BGCOLOR="#000000"><FONT FACE="Courier New,Courier" COLOR="#33FF33"><B>${d}</B></FONT></TD>`).join("") + "</TR></TABLE>";
}

function underConstruction() {
  const stripes = Array.from({ length: 16 }, (_, i) => `<TD BGCOLOR="${i % 2 ? "#000000" : "#FFCC00"}" WIDTH=14>&nbsp;</TD>`).join("");
  return `<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0><TR>${stripes}</TR></TABLE><FONT FACE="Arial,Helvetica" COLOR="#FFCC00"><B>&#9888; UNDER CONSTRUCTION &#9888;</B></FONT><TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0><TR>${stripes}</TR></TABLE>`;
}

function sectionsHtml(hp, ctx) {
  const st = hp.style;
  const out = [];
  hp.sections.forEach((s, i) => {
    out.push(`<A NAME="s${i}"></A><H2>${st.font ? `<FONT FACE="${st.font}">` : ""}${st.marker}${esc(s.h)}${st.font ? "</FONT>" : ""}${s.newFlag ? ' <BLINK><FONT COLOR="#FF0000" SIZE=2>NEW!</FONT></BLINK>' : ""}</H2>`);
    for (const p of s.p || []) out.push(`<P>${frag(p)}</P>`);
    if (s.list) out.push("<UL>" + s.list.map((x) => `<LI>${frag(x)}`).join("") + "</UL>");
    if (s.ol) out.push("<OL>" + s.ol.map((x) => `<LI>${esc(x)}`).join("") + "</OL>");
    for (const p of s.p2 || []) out.push(`<P>${frag(p)}</P>`);
    if (s.pre) out.push(`<PRE>${esc(s.pre.join("\n"))}</PRE>`);
    if (s.midis) out.push("<UL>" + s.midis.map((m) => `<LI><A HREF="/assets/midi/${m}.mid?v=${ctx.assetVersion}">${esc(m.replace(/_/g, " "))}.mid</A>`).join("") + "</UL>");
    if (s.guestbook) {
      out.push(`<TABLE BORDER=1 CELLPADDING=4 CELLSPACING=0 WIDTH="90%">` + s.guestbook.map((g) =>
        `<TR><TD><FONT SIZE=2><B>${esc(g.who)}</B> (${esc(g.from)}) &middot; <I>${g.date}</I></FONT><BR>${frag(g.text)}</TD></TR>`).join("") + "</TABLE>");
    }
  });
  return out.join("\n");
}

function badgesHtml(hp, ctx) {
  const imgs = hp.badges.map((b) => `<IMG SRC="/assets/badges/${b}.gif?v=${ctx.assetVersion}" WIDTH=88 HEIGHT=31 BORDER=1 HSPACE=3 VSPACE=3 ALT="[${esc(b)}]">`);
  return `<CENTER><P>${imgs.join("")}</P></CENTER>`;
}

function linksHtml(hp, ui, ctx, title) {
  const items = hp.links.map((l) => {
    const u = publicUrl(l.p);
    return u ? `<LI><A HREF="${esc(u)}">${esc(l.t)}</A>` : "";
  });
  items.unshift(`<LI><A HREF="${esc(geoUrl("hollywood-hills-4127"))}">Rick's Nova Hart Shrine (ring home)</A>`);
  return `<H2>${hp.style.marker}${esc(title || ui.links_title || "Cool Links")}</H2><UL>${items.join("")}</UL>`;
}

function webringHtml(hp, ui, ctx) {
  const banner = (ui.webring_banner || "&#10022; This <B>%s</B> site is station #%d of %d &#10022;")
    .replace("%s", RING).replace("%d", String(hp.id + 1 + ctx.ringOffset)).replace("%d", String(ctx.ringSize));
  return `<CENTER><TABLE BORDER=3 CELLPADDING=4 BGCOLOR="#000000"><TR><TD ALIGN=CENTER><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica" SIZE=2>${banner}<BR>` +
    `[ <A HREF="${esc(geoUrl(ctx.prev))}">${ui.prev || "&lt;&lt; Prev"}</A> | <A HREF="${esc(geoUrl(ctx.random))}">${ui.random || "Random"}</A> | ` +
    `<A HREF="${esc(ctx.dirUrl)}">${ui.list || "List Stations"}</A> | <A HREF="${esc(geoUrl(ctx.next))}">${ui.next || "Next &gt;&gt;"}</A> ]</FONT></TD></TR></TABLE></CENTER>`;
}

function navHtml(hp, ui, ctx) {
  return `<P><FONT SIZE=2>[ <B>${esc(ui.nav_hood || "Neighborhood")}:</B> <A HREF="${esc(ctx.dirUrl)}">${esc(hp.hood + "/" + hp.suburb)}</A> | ` +
    `<B>${esc(ui.nav_lang || "Language")}:</B> <A HREF="${esc(ctx.langUrl)}">${esc((hp.langInfo && hp.langInfo.name) || hp.lang)}</A> | ` +
    `<A HREF="${esc(ctx.dirIndexUrl)}">${esc(ui.nav_all || "All Neighborhoods")}</A> ]</FONT></P>`;
}

function footer(hp, ui, ctx, { mail = true } = {}) {
  const st = hp.style;
  const parts = ["<CENTER>"];
  if (!st.badgesTop) parts.push(badgesHtml(hp, ctx));
  if (st.construction) parts.push(underConstruction());
  if (mail) {
    parts.push(`<P><A HREF="mailto:${esc(hp.email)}">&#9993; ${esc((ui.email || "Email %s").replace("%s", hp.name))}</A> | ` +
      `<A HREF="mailto:${esc(hp.email)}?subject=Guestbook">${esc(ui.guestbook || "Sign Guestbook")}</A></P>`);
  }
  parts.push(navHtml(hp, ui, ctx), webringHtml(hp, ui, ctx));
  parts.push(`<P><FONT SIZE=1>${ui.disclaimer || "Hosted Free by GeoCities &middot; Best viewed with Netscape Navigator 2.0 at 640x480"}</FONT></P>`);
  parts.push("</CENTER>");
  return parts.join("\n");
}

function head(hp, ctx) {
  const [bg, text, link, vlink] = hp.palette;
  const h = [DOCTYPE, `<HTML LANG="${esc(hp.lang)}"><HEAD><TITLE>${esc(hp.title)}</TITLE>`,
    '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">',
    `<META NAME="description" CONTENT="${esc(hp.description)}">`,
    '<META NAME="keywords" CONTENT="Nova Hart, SYNTHESIS, Orion Records, Stardust, 14.2 Hz, GeoCities">'];
  if (hp.style.generator) h.push(`<META NAME="GENERATOR" CONTENT="${esc(hp.style.generator)}">`);
  if (ctx.indexable) {
    h.push(`<META PROPERTY="og:site_name" CONTENT="${RING}"><META PROPERTY="og:type" CONTENT="website"><META PROPERTY="og:url" CONTENT="${esc(ctx.selfUrl)}">` +
      `<META PROPERTY="og:description" CONTENT="${esc(hp.description)}"><META PROPERTY="og:image" CONTENT="https://stardust-archive.net/assets/og_card.jpg">`);
    const ld = {
      "@context": "https://schema.org", "@type": "WebPage", name: hp.title, description: hp.description, inLanguage: hp.lang,
      dateModified: hp.date, url: ctx.selfUrl,
      isPartOf: { "@type": "WebSite", name: RING, url: "https://stardust-archive.net/" },
      about: [{ "@type": "MusicGroup", name: "Nova Hart" }, { "@type": "MusicAlbum", name: "SYNTHESIS" }],
      author: { "@type": "Person", name: hp.name, address: { "@type": "PostalAddress", addressLocality: hp.city } },
    };
    h.push(`<SCRIPT TYPE="application/ld+json">${JSON.stringify(ld).replace(/</g, "\\u003c")}</SCRIPT>`);
  }
  h.push("</HEAD>");
  const midi = hp.midi ? `<BGSOUND SRC="/assets/midi/${hp.midi}.mid?v=${ctx.assetVersion}" LOOP=INFINITE>` : "";
  h.push(`<BODY BGCOLOR="${bg}" TEXT="${text}" LINK="${link}" VLINK="${vlink}" ALINK="#FF0000">${midi}`);
  return h;
}

function topBar(hp, ui, ctx) {
  return `<TABLE BORDER=0 CELLPADDING=3 CELLSPACING=0 WIDTH="100%" BGCOLOR="#FFCC00"><TR><TD><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B>` +
    `<A HREF="${esc(ctx.geoIndexUrl)}" STYLE="color:#000000;text-decoration:none;"><IMG SRC="/assets/badges/geocities_g_box.png?v=${ctx.assetVersion}" WIDTH=24 HEIGHT=22 BORDER=0 ALIGN=ABSMIDDLE ALT="[G]"> GeoCities</A>` +
    ` &gt; <A HREF="${esc(ctx.dirUrl)}" STYLE="color:#000000;">${esc(hp.pathDisplay)}</A></B></FONT></TD>` +
    `<TD ALIGN=RIGHT><FONT FACE="Arial,Helvetica" SIZE=1 COLOR="#000000"><B>[ <A HREF="${esc(ctx.dirIndexUrl)}" STYLE="color:#000000;">${esc(ui.top_hoods || "Neighborhoods")}</A> | ` +
    `<A HREF="${esc(ctx.geoIndexUrl)}" STYLE="color:#000000;">${esc(ui.top_dir || "Homestead Directory")}</A> ]</B></FONT></TD></TR></TABLE>`;
}

const lowerTags = (html) => html.replace(/<[^>]+>/g, (tag) =>
  tag.startsWith("<!") ? tag : tag.replace(/^<\/?[A-Z0-9]+/, (m) => m.toLowerCase()).replace(/\s([A-Z-]+)=/g, (m, a) => " " + a.toLowerCase() + "="));

/**
 * ctx: { assetVersion, indexable, selfUrl, prev, next, random (slugs), ringOffset, ringSize,
 *        dirUrl, langUrl, dirIndexUrl, geoIndexUrl }
 */
export function renderPage(hp, ctx) {
  const ui = hp.ui || {};
  const st = hp.style;
  const parts = head(hp, ctx);
  const updated = (ui.updated || "Updated:") + " " + hp.date;
  const title = esc(hp.title);
  const marquee = hp.marquee ? `<MARQUEE BEHAVIOR=SCROLL SCROLLAMOUNT=${3 + (hp.id % 4)} WIDTH="90%"><FONT FACE="Courier New,Courier"><B>${esc(hp.marquee)}</B></FONT></MARQUEE>` : "";
  const wrapOpen = st.width ? `<CENTER><TABLE WIDTH=${st.width} BORDER=0 CELLPADDING=6><TR><TD>` : "";
  const wrapClose = st.width ? "</TD></TR></TABLE></CENTER>" : "";

  if (hp.layout !== "plain") parts.push(topBar(hp, ui, ctx));
  parts.push(wrapOpen);
  if (st.badgesTop) parts.push(badgesHtml(hp, ctx));

  switch (hp.layout) {
    case "two_column":
      parts.push(`<CENTER>${marquee}<H1>${title}</H1></CENTER>${st.hr}`,
        '<TABLE BORDER=0 CELLPADDING=8 CELLSPACING=0 WIDTH="100%"><TR><TD VALIGN=TOP WIDTH=200 BGCOLOR="#111111"><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica" SIZE=2><CENTER>',
        `<B>${esc(ui.stats_title || "HOMESTEAD STATS")}</B><BR><IMG SRC="/assets/badges/novachan_chibi.gif?v=${ctx.assetVersion}" WIDTH=48 HEIGHT=48 ALT="[Nova-chan]">`,
        `<P>${esc(ui.visitor || "Visitor #:")}<BR>${counterHtml(hp.counter, st.counterStyle)}</P><P><FONT SIZE=1>${esc(updated)}</FONT></P>`,
        `<HR SIZE=1><P>${hp.sections.map((s, i) => `<A HREF="#s${i}"><FONT COLOR="#FFFFFF">${esc(s.h)}</FONT></A>`).join("<BR>")}</P>`,
        "</CENTER></FONT></TD><TD VALIGN=TOP>", sectionsHtml(hp, ctx), st.hr, linksHtml(hp, ui, ctx), "</TD></TR></TABLE>", st.hr, footer(hp, ui, ctx));
      break;
    case "terminal":
      parts.push("<CENTER><PRE>", "=".repeat(72),
        `  ${(ui.term_node || "TERMINAL NODE").slice(0, 14).padEnd(14)}: ${hp.pathDisplay.slice(0, 26).padEnd(26)} ${(ui.term_updated || "UPDATED").slice(0, 8)}: ${hp.date}`,
        "  PROJECT STARDUST ARCHIVE // 14.2 HZ // CERN-HTTPd 3.0", "=".repeat(72), "</PRE>",
        `<H1><TT>${title}</TT></H1>`, hp.marquee ? `<PRE>[ TRANSMISSION ]: ${esc(hp.marquee)}</PRE>` : "",
        `<P><TT>[ ${esc(ui.visitor || "VISITOR")} ${String(hp.counter).padStart(6, "0")} ]</TT></P></CENTER><HR SIZE=2 NOSHADE>`,
        sectionsHtml(hp, ctx), "<HR SIZE=2 NOSHADE>", linksHtml(hp, ui, ctx, ui.term_matrix || "[ HYPERLINK MATRIX ]"), "<HR SIZE=2 NOSHADE>", footer(hp, ui, ctx));
      break;
    case "hub":
      parts.push('<CENTER><TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 BGCOLOR="#000000"><TR>',
        `<TD><FONT COLOR="#00FFCC" FACE="Arial,Helvetica"><B>&nbsp;${esc(ui.hub_home || "HOME")}&nbsp;</B></FONT></TD>`,
        `<TD><A HREF="#s0"><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica">${esc(ui.hub_articles || "ARTICLES")}</FONT></A></TD>`,
        `<TD><A HREF="#links"><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica">${esc(ui.hub_links || "LINKS")}</FONT></A></TD>`,
        `<TD><A HREF="mailto:${esc(hp.email)}"><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica">${esc(ui.hub_mailbox || "MAILBOX")}</FONT></A></TD></TR></TABLE>`,
        marquee, `<H1>${title}</H1><IMG SRC="/assets/badges/cassette.gif?v=${ctx.assetVersion}" WIDTH=48 HEIGHT=32 BORDER=1 ALT="[Cassette]">`,
        `<P>${esc(ui.hub_listener || "You are listener number:")}</P>${counterHtml(hp.counter, st.counterStyle)}`,
        `<P><FONT SIZE=2>${esc((ui.hub_updated || "Broadcast log updated: %s").replace("%s", hp.date))}</FONT></P></CENTER>${st.hr}`,
        sectionsHtml(hp, ctx), st.hr, '<A NAME="links"></A>', linksHtml(hp, ui, ctx, ui.hub_ring_net), footer(hp, ui, ctx));
      break;
    case "plain":
      parts.push(`<H1>${title}</H1>`, `<P><I>${esc(updated)}</I></P><HR>`, sectionsHtml(hp, ctx), "<HR>", linksHtml(hp, ui, ctx), "<HR>",
        footer(hp, ui, ctx, { mail: false }), `<ADDRESS><A HREF="mailto:${esc(hp.email)}">${esc(hp.email)}</A></ADDRESS>`);
      break;
    case "index_table":
      parts.push(`<CENTER>${marquee}<TABLE BORDER=4 CELLPADDING=6 WIDTH="95%"><TR><TD COLSPAN=2 ALIGN=CENTER><H1>${title}</H1>`,
        `${esc(ui.visitor || "Visitor #:")} ${counterHtml(hp.counter, st.counterStyle === "digits" ? "text" : st.counterStyle)} &middot; ${esc(updated)}</TD></TR>`,
        `<TR><TD VALIGN=TOP WIDTH="25%"><B>CONTENTS</B><OL>${hp.sections.map((s, i) => `<LI><A HREF="#s${i}">${esc(s.h)}</A>`).join("")}<LI><A HREF="#links">Links</A></OL></TD>`,
        `<TD VALIGN=TOP>${sectionsHtml(hp, ctx)}</TD></TR></TABLE></CENTER><A NAME="links"></A>`, linksHtml(hp, ui, ctx), st.hr, footer(hp, ui, ctx));
      break;
    default: // shrine
      parts.push(`<CENTER>${marquee}<H1>${st.font ? `<FONT FACE="${st.font}">` : ""}${title}${st.font ? "</FONT>" : ""}</H1>`,
        `<P>${esc(ui.shrine_visitor || "You are visitor number")}</P>${counterHtml(hp.counter, st.counterStyle)}`,
        `<P><FONT SIZE=2>${esc((ui.shrine_updated || "Last updated: %s").replace("%s", hp.date))} <BLINK><FONT COLOR="#FF0000"><B>NEW!</B></FONT></BLINK></FONT></P></CENTER>${st.hr}`,
        sectionsHtml(hp, ctx), st.hr, linksHtml(hp, ui, ctx), footer(hp, ui, ctx));
  }
  parts.push(wrapClose, "</BODY></HTML>");
  const html = parts.filter(Boolean).join("\n") + "\n";
  return st.lowercase ? lowerTags(html) : html;
}
