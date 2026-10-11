// Shared, deterministic mapping between the static build layout (site/...)
// and the long single-level public URLs, e.g.
//   site/geocities/hollywood-hills-4127.html
//   <->  https://hollywood-hills-4127-geocities-nova3289429-i88sjj.stardust-archive.net/~hart/sie/172-sdu9wew/index.html
//
// Single-level hostnames are required so Cloudflare's free Universal SSL
// certificate covers every page without multi-level SSL handshake failures.
// Supports Multi-Apex Domain Federation (stardust-archive.net, ashford-poly.org, kamome-net.org, etc.)

import { PRIMARY_APEX, FEDERATION } from "./federation.js";

export const APEX = PRIMARY_APEX;
export const KINDS = ["geocities", "usenet", "ftp", "regional"];
const MAX_LABEL = 63; // DNS hard limit per label

// Returns list of all active apex domains (primary + enabled federation domains)
export function getActiveApexes() {
  return [
    PRIMARY_APEX,
    ...Object.keys(FEDERATION).filter((k) => FEDERATION[k].enabled),
  ];
}
export const ALL_APEXES = getActiveApexes();

/**
 * Returns which apex domain a site path belongs to.
 * If sister domains are disabled, gracefully defaults to PRIMARY_APEX.
 */
export function apexFor(sitePath) {
  const p = sitePath.replace(/^\/+/, "");
  for (const [domain, conf] of Object.entries(FEDERATION)) {
    if (!conf.enabled) continue;
    const m = conf.match || {};
    if (m.paths && m.paths.some((prefix) => p.startsWith(prefix))) return domain;
    if (m.regional && m.regional.some((node) => p.startsWith(`regional/${node}`))) return domain;
    if (m.hoods && m.hoods.some((hood) => p.startsWith(`geocities/hood_${hood}`) || p.includes(hood))) return domain;
    if (m.langs && m.langs.some((lang) => p.startsWith(`geocities/lang_${lang}`) || p.startsWith(`geocities/lang-${lang}`))) return domain;
  }
  return PRIMARY_APEX;
}

/**
 * Identifies which apex domain an incoming hostname matches.
 */
export function resolveApex(hostname) {
  const host = hostname.toLowerCase();
  for (const apex of getActiveApexes()) {
    if (host === apex || host === `www.${apex}` || host.endsWith("." + apex)) {
      return apex;
    }
  }
  return PRIMARY_APEX;
}

/**
 * True for pages that should be indexed by search engines & AI crawlers (Google, GPTBot, ClaudeBot, etc.).
 * Includes all GeoCities fan pages, neighborhood directories, language hubs, regional nodes, and FTP mirrors.
 * Individual raw Usenet spool files (sNNNNN.txt) get `noindex, follow` so thread indexes are indexed instead of 25k text dumps.
 */
export function isStory(sitePath) {
  const p = sitePath.replace(/^\/+/, "");
  if (p.startsWith("geocities/")) return true;
  if (/^usenet\/[^/]+\/s\d+\.txt$/.test(p)) return false;
  return true;
}

const WORDS = ["nova", "hart", "sie", "akasaka", "reel", "node", "relay", "dust", "idol", "kamome", "hale", "carrier", "ghost", "chorus", "spool", "mirror", "pub", "incoming", "tmp", "users"];
const ALNUM = "abcdefghijklmnopqrstuvwxyz0123456789";

function fnv1a(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h >>> 0;
}

function prng(seedStr) {
  let a = fnv1a(seedStr);
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function token(r) {
  const style = Math.floor(r() * 4);
  const rnd = (n) => Array.from({ length: n }, () => ALNUM[Math.floor(r() * ALNUM.length)]).join("");
  const word = WORDS[Math.floor(r() * WORDS.length)];
  if (style === 0) return word + Math.floor(r() * 9999999);
  if (style === 1) return rnd(4 + Math.floor(r() * 4));
  if (style === 2) return word + rnd(3);
  return rnd(2) + Math.floor(r() * 999) + rnd(2);
}

export function hostFor(kind, key, apex = PRIMARY_APEX) {
  const r = prng(`host|${kind}|${key}`);
  let label = `${key}-${kind}`;
  // Pad with junk tokens until the label is as long as DNS allows.
  for (let i = 0; i < 12; i++) {
    const t = token(r);
    if (label.length + 1 + t.length > MAX_LABEL) continue;
    label += "-" + t;
  }
  return `${label}.${apex}`;
}

function junkPath(kind, key) {
  const r = prng(`path|${kind}|${key}`);
  const segs = [`~${token(r)}`];
  const n = 3 + Math.floor(r() * 3);
  for (let i = 0; i < n; i++) segs.push(r() < 0.4 ? `${token(r)}-${token(r)}` : token(r));
  return "/" + segs.join("/") + "/";
}

/** site-relative path (no leading slash) -> public absolute URL (or root-relative for assets). */
export function publicUrl(sitePath) {
  const p = sitePath.replace(/^\/+/, "");
  const apex = apexFor(p);
  if (p === "" || p === "index.html") return `https://${apex}/`;
  if (p.startsWith("assets/")) return "/" + p;
  const segs = p.split("/");
  const kind = segs[0];
  if (!KINDS.includes(kind)) return null;
  if (kind === "geocities" && segs.length === 2 && segs[1].endsWith(".html")) {
    const key = segs[1].slice(0, -5);
    return `https://${hostFor(kind, key, apex)}${junkPath(kind, key)}index.html`;
  }
  if (segs.length === 2 && segs[1] === "index.html") {
    return `https://${hostFor(kind, "index", apex)}${junkPath(kind, "index")}`;
  }
  if (segs.length >= 3) {
    const key = segs[1];
    const file = segs.slice(2).join("/");
    return `https://${hostFor(kind, key, apex)}${junkPath(kind, key)}${file === "index.html" ? "" : file}`;
  }
  return null;
}

const LABEL_RE = new RegExp(`^(.+?)-(${KINDS.join("|")})(?:-[a-z0-9-]*)?$`);

/**
 * Public request -> { sitePath, canonical? }.
 * Resolves single-level subdomains across any active apex domain.
 */
export function resolve(hostname, pathname) {
  const host = hostname.toLowerCase();
  const path = decodeURIComponent(pathname);

  if (path.startsWith("/assets/")) return { sitePath: path.slice(1) };

  // Match which registered apex domain this request is targeting
  let matchedApex = null;
  for (const apex of getActiveApexes()) {
    if (host === apex || host === `www.${apex}` || host.endsWith("." + apex)) {
      matchedApex = apex;
      break;
    }
  }
  if (!matchedApex) return { sitePath: null };

  // Root or apex path access
  if (host === matchedApex || host === `www.${matchedApex}`) {
    if (path === "/" || path === "/index.html") {
      // If this is an enabled sister domain, route root to its canon entry point!
      if (matchedApex !== PRIMARY_APEX) {
        const conf = FEDERATION[matchedApex];
        if (conf && conf.match) {
          if (conf.match.paths && conf.match.paths.length > 0) return { sitePath: `${conf.match.paths[0]}/index.html` };
          if (conf.match.regional && conf.match.regional.length > 0) return { sitePath: `regional/${conf.match.regional[0]}/index.html` };
        }
      }
      return { sitePath: "index.html" };
    }
    const sp = path.slice(1).replace(/\/$/, "/index.html");
    const canon = publicUrl(sp);
    return { sitePath: sp, canonical: canon && canon !== `https://${matchedApex}/` ? canon : null };
  }

  const labels = host.slice(0, -(matchedApex.length + 1)).split(".");

  // Legacy two-level form: <key>.<kind>.<apex>
  if (labels.length === 2) {
    let kind, key;
    if (labels[0] === "ftp") [kind, key] = ["ftp", labels[1]];
    else [key, kind] = labels;
    if (!KINDS.includes(kind)) return { sitePath: null };
    const file = path.split("/").pop() || "index.html";
    const sp = kind === "geocities" ? `geocities/${key}.html` : `${kind}/${key}/${file}`;
    return { sitePath: sp, canonical: publicUrl(sp) };
  }
  if (labels.length !== 1) return { sitePath: null };

  const m = LABEL_RE.exec(labels[0]);
  if (!m) return { sitePath: null };
  const [, key, kind] = m;
  if (kind === "geocities") return { sitePath: `geocities/${key}.html` };
  if (key === "index") return { sitePath: `${kind}/index.html` };
  const jp = junkPath(kind, key);
  const rest = path.startsWith(jp) ? path.slice(jp.length) : path.split("/").pop();
  const file = rest.endsWith("/") || rest === "" ? rest + "index.html" : rest;
  return { sitePath: `${kind}/${key}/${file}` };
}
