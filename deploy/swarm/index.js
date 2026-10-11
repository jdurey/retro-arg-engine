// Edge entry point for the generated swarm (v3).
//
// Pages:   geocities/<suburb-slug>-<NNNN>.html  -> member page for id = idOf(slug)
//          geocities/dir-index.html              -> all suburbs
//          geocities/dir-<suburb-slug>-p<N>.html -> suburb directory, 100 per page
//          geocities/lang-<code>.html            -> language hub (sample + suburb links)
//
// Rollout is by date: N_START pages live at LAUNCH, +N_STEP every 7 days, up to
// N_MAX. env.SWARM_CAP (wrangler var) caps it; SWARM_CAP=0 turns the swarm off.

import BANK from "./bank.js";
import TIER2, { LANG_HUBS } from "./tier2.js";
import { SUBURBS, BLOCK, addressOf, idOf, idsInSuburb, suburbSlug } from "./address.js";
import { header, page } from "./generate.js";
import { renderPage, esc, counterHtml } from "./render.js";
import { publicUrl } from "../urlmap.js";
import { hash32 } from "./rng.js";

export const N_MAX = 300000;
export const N_START = 50000;
export const N_STEP = 50000;
export const LAUNCH = Date.UTC(2026, 9, 11); // 2026-10-11
const PER_PAGE = 100;
const DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">';

export function liveCount(now = Date.now(), cap) {
  const weeks = Math.max(0, Math.floor((now - LAUNCH) / (7 * 86400e3)));
  let n = now < LAUNCH ? 0 : Math.min(N_MAX, N_START + weeks * N_STEP);
  if (cap !== undefined && cap !== null && cap !== "" && !Number.isNaN(Number(cap))) n = Math.min(n, Number(cap));
  return n;
}

const TIER2_SET = new Set(TIER2);
export const geoPath = (slug) => `geocities/${slug}.html`;
export const dirPath = (sub, p = 1) => `geocities/dir-${suburbSlug(sub)}-p${p}.html`;
export const langPath = (code) => `geocities/lang-${code.toLowerCase()}.html`;
export const DIR_INDEX = "geocities/dir-index.html";

/**
 * Classify a geocities key. staticSlugs: Set of legacy static page slugs (they win).
 * Returns null when the swarm doesn't own the key.
 */
export function classify(key, n, staticSlugs) {
  if (key === "dir-index") return { kind: "dir-index" };
  let m = /^dir-(.+)-p(\d+)$/.exec(key);
  if (m) {
    const sub = SUBURBS.findIndex((_, i) => suburbSlug(i) === m[1]);
    return sub >= 0 && Number(m[2]) >= 1 ? { kind: "dir", sub, p: Number(m[2]) } : null;
  }
  m = /^lang-([a-z]{2}(?:-[a-z]{2})?)$/.exec(key);
  if (m) {
    const code = Object.keys(BANK.langs).find((c) => c.toLowerCase() === m[1]);
    return code ? { kind: "lang", code } : null;
  }
  if (staticSlugs.has(key)) return null;
  const id = idOf(key);
  if (id < 0) return null;
  return id < n ? { kind: "member", id } : { kind: "pending" }; // valid address, not live yet
}

export const isTier2 = (id, n) => id < n && TIER2_SET.has(id);

function liveIdsInSuburb(sub, n, staticSlugs) {
  const out = [];
  for (const id of idsInSuburb(sub)) if (id < n && !staticSlugs.has(addressOf(id).slug)) out.push(id);
  return out;
}

function nextLive(id, step, n, staticSlugs) {
  for (let i = 1; i < 50; i++) {
    const j = (((id + step * i) % n) + n) % n;
    if (!staticSlugs.has(addressOf(j).slug)) return j;
  }
  return id;
}

export function renderMember(id, n, staticSlugs, assetVersion) {
  const hp = page(id);
  const indexable = isTier2(id, n);
  const html = renderPage(hp, {
    assetVersion, indexable,
    selfUrl: publicUrl(geoPath(hp.slug)),
    prev: addressOf(nextLive(id, -1, n, staticSlugs)).slug,
    next: addressOf(nextLive(id, 1, n, staticSlugs)).slug,
    random: addressOf(nextLive(hash32(`ring|${id}`) % n, 1, n, staticSlugs)).slug,
    ringOffset: 5039, ringSize: 5039 + n,
    dirUrl: publicUrl(dirPath(hp.suburbIndex, 1)),
    langUrl: publicUrl(langPath(hp.lang)),
    dirIndexUrl: publicUrl(DIR_INDEX),
    geoIndexUrl: publicUrl("geocities/index.html"),
  });
  return { html, indexable, page: hp };
}

function shell(title, desc, body, { lang = "en", indexable = false, selfUrl = "" } = {}) {
  const ld = indexable
    ? `<SCRIPT TYPE="application/ld+json">${JSON.stringify({ "@context": "https://schema.org", "@type": "CollectionPage", name: title, description: desc, url: selfUrl, inLanguage: lang }).replace(/</g, "\\u003c")}</SCRIPT>`
    : "";
  return `${DOCTYPE}\n<HTML LANG="${esc(lang)}"><HEAD><TITLE>${esc(title)}</TITLE>\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">\n` +
    `<META NAME="description" CONTENT="${esc(desc)}">${ld}</HEAD>\n<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000CC" VLINK="#663399" ALINK="#FF0000">\n<CENTER>\n` +
    `<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 WIDTH="720" BGCOLOR="#FFCC00"><TR>` +
    `<TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE=2><B><A HREF="${esc(publicUrl("index.html"))}">Main</A></B></FONT></TD>` +
    `<TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE=2><B><A HREF="${esc(publicUrl("geocities/index.html"))}">Homestead Directory</A></B></FONT></TD>` +
    `<TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE=2><B><A HREF="${esc(publicUrl(DIR_INDEX))}">All Neighborhoods</A></B></FONT></TD>` +
    `<TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE=2><B><A HREF="${esc(publicUrl("geocities/hollywood-hills-4127.html"))}">Ring Home</A></B></FONT></TD></TR></TABLE>\n` +
    `${body}\n<HR SIZE=3 NOSHADE><P><FONT SIZE=2>Hosted free by <B>GeoCities</B> &middot; Best viewed with <B>Netscape Navigator 2.0</B> at 640x480 &middot; Keep the channels open.</FONT></P>\n</CENTER></BODY></HTML>\n`;
}

const pageLinks = (sub, pages, cur) =>
  `<P><FONT SIZE=2>Pages: ${Array.from({ length: pages }, (_, i) => i + 1 === cur ? `<B>[${i + 1}]</B>` : `<A HREF="${esc(publicUrl(dirPath(sub, i + 1)))}">${i + 1}</A>`).join(" ")}</FONT></P>`;

export function renderDirIndex(n, staticSlugs) {
  const byHood = new Map();
  SUBURBS.forEach(([hood, suburb], i) => {
    if (!byHood.has(hood)) byHood.set(hood, []);
    byHood.get(hood).push([suburb, i]);
  });
  const rows = [...byHood].map(([hood, subs]) =>
    `<TR><TD VALIGN=TOP><B><FONT FACE="Arial,Helvetica">${esc(hood)}</FONT></B><BR><FONT SIZE=1>${esc(BANK.base.hood_themes[hood + "/" + subs[0][0]] || BANK.base.hood_themes[Object.keys(BANK.base.hood_themes).find((k) => k.startsWith(hood + "/"))] || "")}</FONT></TD>` +
    `<TD>${subs.map(([s, i]) => `<A HREF="${esc(publicUrl(dirPath(i, 1)))}">${esc(hood + "/" + s)}</A>`).join(" &middot; ")}</TD></TR>`).join("\n");
  const langs = Object.entries(BANK.langs).map(([c, L]) => `<A HREF="${esc(publicUrl(langPath(c)))}">${esc((L.info && L.info.name) || c)}</A>`).join(" &middot; ");
  const total = 5039 + n;
  return shell("GeoCities Neighborhoods - The Stardust Webring", `Directory of every GeoCities neighborhood and suburb in The Stardust Webring: ${total.toLocaleString("en-US")} member stations.`,
    `<H1><FONT FACE="Arial Black,Arial,Helvetica">GEOCITIES NEIGHBORHOODS &amp; SUBURBS</FONT></H1>\n<P>${total.toLocaleString("en-US")} registered homesteads across ${byHood.size} neighborhoods and ${SUBURBS.length} suburbs.</P>\n` +
    `<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="720">\n<TR BGCOLOR="#E6F2FF"><TH>Neighborhood</TH><TH>Suburbs</TH></TR>\n${rows}\n</TABLE>\n<H2>Language Hubs</H2>\n<P>${langs}</P>`,
    { indexable: true, selfUrl: publicUrl(DIR_INDEX) });
}

export function renderDir(sub, p, n, staticSlugs) {
  const ids = liveIdsInSuburb(sub, n, staticSlugs);
  const pages = Math.max(1, Math.ceil(ids.length / PER_PAGE));
  if (p > pages) return null;
  const [hood, suburb] = SUBURBS[sub];
  const rows = ids.slice((p - 1) * PER_PAGE, p * PER_PAGE).map((id) => {
    const h = header(id);
    const L = BANK.langs[h.lang];
    return `<TR><TD><TT>${esc(h.pathDisplay)}</TT></TD><TD><A HREF="${esc(publicUrl(geoPath(h.slug)))}"><B>${esc(h.title)}</B></A></TD>` +
      `<TD><FONT SIZE=2>${esc(h.name)} (${esc(h.city)})</FONT></TD><TD><FONT SIZE=2>${esc(((L && L.info && L.info.name) || h.lang).split(" ")[0])}</FONT></TD><TD ALIGN=RIGHT>${h.counter}</TD></TR>`;
  }).join("\n");
  return shell(`GeoCities ${hood}/${suburb} - Directory page ${p}`, `Member homesteads in the GeoCities ${hood}/${suburb} suburb (page ${p} of ${pages}).`,
    `<H1><FONT FACE="Arial Black,Arial,Helvetica">${esc(hood.toUpperCase())} / ${esc(suburb.toUpperCase())}</FONT></H1>\n<P>${ids.length} homesteads in this suburb.</P>\n${pageLinks(sub, pages, p)}\n` +
    `<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%">\n<TR BGCOLOR="#E6F2FF"><TH>Address</TH><TH>Homepage</TH><TH>Webmaster</TH><TH>Language</TH><TH>Hits</TH></TR>\n${rows}\n</TABLE>\n${pageLinks(sub, pages, p)}`);
}

export function renderLang(code, n, staticSlugs) {
  const L = BANK.langs[code];
  const rows = [];
  for (const id of LANG_HUBS[code] || []) {
    if (id >= n || rows.length >= 150) continue;
    const h = header(id);
    rows.push(`<TR><TD><TT>${esc(h.pathDisplay)}</TT></TD><TD><A HREF="${esc(publicUrl(geoPath(h.slug)))}">${esc(h.title)}</A></TD><TD><FONT SIZE=2>${esc(h.city)}</FONT></TD></TR>`);
  }
  const name = (L.info && L.info.name) || code;
  return shell(`GeoCities International Hub: ${name}`, `Nova Hart fan homepages written in ${name}, with links to every GeoCities suburb directory.`,
    `<H1><FONT FACE="Arial Black,Arial,Helvetica">GLOBAL LANGUAGE HUB: ${esc(name)}</FONT></H1>\n<P><B>${esc((L.info && L.info.node) || "")}</B> &middot; ${esc((L.info && L.info.region) || "")}</P>\n` +
    `<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%">\n<TR BGCOLOR="#FFF2E6"><TH>Address</TH><TH>Homepage</TH><TH>City</TH></TR>\n${rows.join("\n")}\n</TABLE>\n` +
    `<P>Browse every suburb: <A HREF="${esc(publicUrl(DIR_INDEX))}">GeoCities Neighborhoods</A></P>`,
    { lang: code, indexable: true, selfUrl: publicUrl(langPath(code)) });
}

/** Swarm URLs that belong in the sitemap for a given live count. */
export function sitemapSitePaths(n) {
  const out = [DIR_INDEX, ...Object.keys(BANK.langs).map(langPath)];
  for (const id of TIER2) if (id < n) out.push(geoPath(addressOf(id).slug));
  return out;
}

export { counterHtml };
