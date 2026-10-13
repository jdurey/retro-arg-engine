// Edge entry point for the generated swarm (v3 + v5 Cryptographic XOR Dyads).
//
// Pages:   geocities/<suburb-slug>-<NNNN>.html  -> member page for id = idOf(slug)
//          geocities/dir-index.html              -> all suburbs
//          geocities/dir-<suburb-slug>-p<N>.html -> suburb directory, 100 per page
//          geocities/lang-<code>.html            -> language hub (sample + suburb links)

import BANK from "./bank.js";
import TIER2 from "./tier2.js";
import { SUBURBS, BLOCK, addressOf, idOf, idsInSuburb, suburbSlug, pairedNodeOf } from "./address.js";
import { header, langOf, page } from "./generate.js";
import { renderPage, esc, counterHtml } from "./render.js";
import { publicUrl } from "../urlmap.js";
import { hash32 } from "./rng.js";

export const N_MAX = 300000;
export const N_START = 50000;
export const N_STEP = 50000;
export const LAUNCH = Date.UTC(2026, 9, 12); // 2026-10-12
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
  return id >= 0 && id < n ? { kind: "member", id } : null;
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
  const dyad = pairedNodeOf(id, n);
  const dyadUrl = publicUrl(geoPath(dyad.partnerSlug));
  const rawHtml = renderPage(hp, {
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
  const breadcrumb = `\n<!-- SUBLEVEL-B2-MEM: ${dyad.memoryAddress} | XOR-DYAD-SEED: ${dyad.xorSeed} | PAIRED-NODE: ${dyad.partnerSlug} (${dyadUrl}) | CARRIER: 14.2001 Hz -->`;
  const html = rawHtml + breadcrumb;
  return { html, indexable, page: hp, dyad };
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
    `${body}\n<HR SIZE=3 NOSHADE><P><FONT SIZE=2>Hosted free by <B>GeoCities</B> &middot; Best viewed with <B>Netscape Navigator 2.0</B></FONT></P></CENTER></BODY></HTML>\n`;
}

export function renderDirIndex(n, staticSlugs) {
  const byHood = new Map();
  SUBURBS.forEach(([hood, suburb], i) => {
    const cnt = liveIdsInSuburb(i, n, staticSlugs).length;
    if (!cnt) return;
    if (!byHood.has(hood)) byHood.set(hood, []);
    byHood.get(hood).push({ i, suburb, cnt });
  });
  const rows = [];
  for (const [hood, subs] of byHood) {
    const links = subs.map((s) => `<A HREF="${esc(publicUrl(dirPath(s.i, 1)))}">${esc(s.suburb)}</A> <FONT SIZE=1>(${s.cnt})</FONT>`).join(" &middot; ");
    rows.push(`<TR><TD VALIGN=TOP><B>${esc(hood)}</B></TD><TD>${links}</TD></TR>`);
  }
  const langLinks = Object.entries(BANK.langs).map(([c, v]) =>
    `<A HREF="${esc(publicUrl(langPath(c)))}">${esc(v.info?.name || c)}</A>`).join(" &middot; ");
  const body = `<H1>GeoCities Homestead Neighborhoods</H1>\n<P><FONT SIZE=2><B>${n.toLocaleString("en-US")}</B> active member pages across <B>${SUBURBS.length}</B> suburbs.</FONT></P>\n` +
    `<TABLE BORDER=1 CELLPADDING=5 CELLSPACING=0 WIDTH="720"><TR BGCOLOR="#CCCCCC"><TH ALIGN=LEFT>Neighborhood</TH><TH ALIGN=LEFT>Suburbs (member count)</TH></TR>\n${rows.join("\n")}</TABLE>\n` +
    `<H2>Browse by Language</H2><P WIDTH="720">${langLinks}</P>`;
  return shell("GeoCities - All Neighborhoods - The Stardust Webring",
    `Directory of all ${SUBURBS.length} GeoCities suburbs hosting Nova Hart & Project Stardust member pages.`,
    body, { indexable: true, selfUrl: publicUrl(DIR_INDEX) });
}

export function renderDir(sub, pageNum, n, staticSlugs) {
  const [hood, suburb] = SUBURBS[sub];
  const ids = liveIdsInSuburb(sub, n, staticSlugs);
  const pages = Math.max(1, Math.ceil(ids.length / PER_PAGE));
  if (pageNum < 1 || pageNum > pages) return null;
  const slice = ids.slice((pageNum - 1) * PER_PAGE, pageNum * PER_PAGE);
  const items = slice.map((id) => {
    const h = header(id);
    return `<TR><TD><TT>${h.num}</TT></TD><TD><A HREF="${esc(publicUrl(geoPath(h.slug)))}"><B>${esc(h.title)}</B></A></TD>` +
      `<TD>${esc(h.name)} <FONT SIZE=1>(${esc(h.city)})</FONT></TD><TD><TT>${h.lang}</TT></TD><TD><TT>${h.date}</TT></TD></TR>`;
  });
  const pager = Array.from({ length: pages }, (_, i) => i + 1).map((p) =>
    p === pageNum ? `<B>[${p}]</B>` : `<A HREF="${esc(publicUrl(dirPath(sub, p)))}">${p}</A>`).join(" ");
  const body = `<H1>${esc(hood)} / ${esc(suburb)} &mdash; Homestead Directory (Page ${pageNum} of ${pages})</H1>\n<P>Pages: ${pager}</P>\n` +
    `<TABLE BORDER=1 CELLPADDING=4 CELLSPACING=0 WIDTH="720"><TR BGCOLOR="#CCCCCC"><TH>Addr</TH><TH ALIGN=LEFT>Page Title</TH><TH ALIGN=LEFT>Homesteader</TH><TH>Lang</TH><TH>Updated</TH></TR>\n` +
    `${items.join("\n")}</TABLE>\n<P>Pages: ${pager}</P>`;
  return shell(`GeoCities ${hood}/${suburb} Directory (Page ${pageNum})`,
    `Member pages in GeoCities ${hood}/${suburb} belonging to The Stardust Webring.`,
    body, { indexable: pageNum === 1, selfUrl: publicUrl(dirPath(sub, pageNum)) });
}

export function renderLang(code, n, staticSlugs) {
  const L = BANK.langs[code];
  if (!L) return null;
  const hits = [];
  const step = Math.max(1, Math.floor(n / 1800));
  for (let id = 0; id < n && hits.length < 120; id += step) {
    if (langOf(id) !== code) continue;
    const h = header(id);
    if (staticSlugs.has(h.slug)) continue;
    hits.push(h);
  }
  const items = hits.map((h) =>
    `<LI><A HREF="${esc(publicUrl(geoPath(h.slug)))}"><B>${esc(h.title)}</B></A> &mdash; ${esc(h.name)} (${esc(h.city)}) &middot; <TT>${esc(h.pathDisplay)}</TT></LI>`);
  const langName = L.info?.name || code;
  const body = `<H1>${esc(langName)} &mdash; Stardust Webring Stations</H1>\n` +
    `<P>${esc(L.info?.region || "")}</P>\n<UL>\n${items.join("\n")}</UL>`;
  return shell(`${langName} - The Stardust Webring`,
    `GeoCities fan pages in ${langName} dedicated to Nova Hart and the 14.2 Hz Stardust signal.`,
    body, { lang: code, indexable: true, selfUrl: publicUrl(langPath(code)) });
}

export function sitemapSitePaths(n) {
  const out = [DIR_INDEX];
  for (let i = 0; i < SUBURBS.length; i++) out.push(dirPath(i, 1));
  for (const c of Object.keys(BANK.langs)) out.push(langPath(c));
  for (const id of TIER2) if (id < n) out.push(geoPath(addressOf(id).slug));
  return out;
}
