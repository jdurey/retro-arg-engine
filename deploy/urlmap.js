// Shared, deterministic mapping between the static build layout (site/...)
// and the long single-level public URLs, e.g.
//   site/geocities/hollywood-hills-4127.html
//   <->  https://hollywood-hills-4127-geocities-nova3289429-i88sjj.stardust-archive.net/~hart/sie/172-sdu9wew/index.html
//
// Single-level hostnames are required so Cloudflare's free Universal SSL
// certificate (*.stardust-archive.net) covers every page.
// The junk in the hostname/path is derived from a hash of the page key, so a
// page always gets the same URL. The router only reads the key/kind out of the
// hostname (and the filename from the last path segment); the rest is cosmetic.

export const APEX = "stardust-archive.net";
export const KINDS = ["geocities", "usenet", "ftp", "regional"];
const MAX_LABEL = 63; // DNS hard limit per label

// Hand-authored homepages (data/personas.json). Everything else under
// geocities/ is procedurally generated swarm.
const CURATED_GEO = new Set(["index", "siliconvalley-lab-1984", "athens-forum-3317", "capecanaveral-lab-0068", "tokyo-garden-1420", "area51-vault-7734", "sunsetstrip-club-2210", "hollywood-hills-4127", "paris-leftbank-0142"]);

/**
 * True for hand-authored story pages that should be indexed by search engines.
 * Swarm pages (generated GeoCities homepages, sNNNNN Usenet posts) get
 * `noindex, follow` so tens of thousands of templated pages can't trigger a
 * scaled-content demotion of the whole domain. Players still reach them in-world.
 */
export function isStory(sitePath) {
  const p = sitePath.replace(/^\/+/, "");
  if (p.startsWith("geocities/")) return CURATED_GEO.has(p.slice(10, -5));
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

export function hostFor(kind, key) {
  const r = prng(`host|${kind}|${key}`);
  let label = `${key}-${kind}`;
  // Pad with junk tokens until the label is as long as DNS allows.
  for (let i = 0; i < 12; i++) {
    const t = token(r);
    if (label.length + 1 + t.length > MAX_LABEL) continue;
    label += "-" + t;
  }
  return `${label}.${APEX}`;
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
  if (p === "" || p === "index.html") return `https://${APEX}/`;
  if (p.startsWith("assets/")) return "/" + p;
  const segs = p.split("/");
  const kind = segs[0];
  if (!KINDS.includes(kind)) return null;
  if (kind === "geocities" && segs.length === 2 && segs[1].endsWith(".html")) {
    const key = segs[1].slice(0, -5);
    return `https://${hostFor(kind, key)}${junkPath(kind, key)}index.html`;
  }
  if (segs.length === 2 && segs[1] === "index.html") {
    return `https://${hostFor(kind, "index")}${junkPath(kind, "index")}`;
  }
  if (segs.length >= 3) {
    const key = segs[1];
    const file = segs.slice(2).join("/");
    return `https://${hostFor(kind, key)}${junkPath(kind, key)}${file === "index.html" ? "" : file}`;
  }
  return null;
}

const LABEL_RE = new RegExp(`^(.+?)-(${KINDS.join("|")})(?:-[a-z0-9-]*)?$`);

/**
 * Public request -> { sitePath, canonical? }.
 * `canonical` is set when the request should be redirected (legacy two-level
 * hosts, path-style access on the apex) to the long single-level URL.
 */
export function resolve(hostname, pathname) {
  const host = hostname.toLowerCase();
  const path = decodeURIComponent(pathname);

  if (path.startsWith("/assets/")) return { sitePath: path.slice(1) };

  if (host === APEX || host === `www.${APEX}`) {
    if (path === "/" || path === "/index.html") return { sitePath: "index.html" };
    const sp = path.slice(1).replace(/\/$/, "/index.html");
    const canon = publicUrl(sp);
    return { sitePath: sp, canonical: canon && canon !== `https://${APEX}/` ? canon : null };
  }

  if (!host.endsWith("." + APEX)) return { sitePath: null };
  const labels = host.slice(0, -(APEX.length + 1)).split(".");

  // Legacy two-level form: <key>.<kind>.stardust-archive.net  /  ftp.<site>.stardust-archive.net
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
  // Strip the deterministic junk prefix to recover nested paths; fall back to
  // the last segment if someone hand-edits the junk.
  const jp = junkPath(kind, key);
  const rest = path.startsWith(jp) ? path.slice(jp.length) : path.split("/").pop();
  const file = rest.endsWith("/") || rest === "" ? rest + "index.html" : rest;
  return { sitePath: `${kind}/${key}/${file}` };
}
