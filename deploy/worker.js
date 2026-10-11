import { APEX, isStory, publicUrl, resolve } from "./urlmap.js";
import STORY_PATHS from "./story_paths.js";
import { classify, liveCount, renderMember, renderDir, renderDirIndex, renderLang, sitemapSitePaths } from "./swarm/index.js";

// Legacy static GeoCities pages always win over generated swarm addresses.
const STATIC_GEO = new Set(STORY_PATHS.filter((p) => /^geocities\/[^/]+\.html$/.test(p)).map((p) => p.slice(10, -5)));

const OG_DESCRIPTION = "A 1994 webring for fans of Nova Hart and the 14.2 Hz Stardust signal. Something is still transmitting.";
const OG_IMAGE = `https://${APEX}/assets/og_card.jpg`;

const ROBOTS = `User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Applebot
Allow: /

Sitemap: https://${APEX}/sitemap.xml
`;
// IndexNow keys are public by design (they prove control of the host, nothing more).
const INDEXNOW_KEY = "37feeed875722863fda484c68e6695e5";
// Bump when files in assets/ are replaced so edge + browser caches refetch.
const ASSET_VERSION = "13";

function urlset(sitePaths) {
  const urls = sitePaths.map((sp) => publicUrl(sp)).filter((u) => u && u.startsWith("https://"));
  const body = urls.map((u) => `  <url><loc>${u.replace(/&/g, "&amp;")}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>`).join("\n");
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
}
let cachedCoreSitemap = null;
const SITEMAP_INDEX = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://${APEX}/sitemap-core.xml</loc></sitemap>
  <sitemap><loc>https://${APEX}/sitemap-swarm.xml</loc></sitemap>
</sitemapindex>
`;

class HeadInjector {
  constructor(pageUrl) { this.pageUrl = pageUrl; }
  element(el) {
    const esc = (s) => s.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
    el.append(
      `<META PROPERTY="og:site_name" CONTENT="The Stardust Webring">` +
      `<META PROPERTY="og:type" CONTENT="website">` +
      `<META PROPERTY="og:url" CONTENT="${esc(this.pageUrl)}">` +
      `<META PROPERTY="og:description" CONTENT="${esc(OG_DESCRIPTION)}">` +
      `<META NAME="description" CONTENT="${esc(OG_DESCRIPTION)}">` +
      `<META PROPERTY="og:image" CONTENT="${OG_IMAGE}">` +
      `<META NAME="twitter:card" CONTENT="summary_large_image">` +
      `<META NAME="twitter:image" CONTENT="${OG_IMAGE}">`,
      { html: true });
  }
}

const NOT_FOUND = `<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML><HEAD><TITLE>404 Not Found</TITLE></HEAD>
<BODY><H1>Not Found</H1>
The requested URL was not found on this server.<P>
<HR><ADDRESS>CERN-HTTPd/3.0</ADDRESS>
</BODY></HTML>
`;

function retroHeaders(contentType) {
  const h = new Headers();
  h.set("Content-Type", contentType);
  h.set("Server", "CERN-HTTPd/3.0");
  h.set("X-Powered-By", "Stardust");
  h.set("Cache-Control", "public, max-age=3600");
  return h;
}

function notFound() {
  return new Response(NOT_FOUND, { status: 404, headers: retroHeaders("text/html; charset=utf-8") });
}

const urlCache = new Map();
function cachedPublicUrl(sitePath) {
  let hit = urlCache.get(sitePath);
  if (!hit) {
    hit = publicUrl(sitePath);
    if (hit) urlCache.set(sitePath, hit);
  }
  return hit;
}

// Rewrites relative links in a page (which assume the flat site/ layout) into
// the long single-level public URLs.
class LinkRewriter {
  constructor(attr, sitePath) {
    this.attr = attr;
    this.base = new URL("https://build.invalid/" + sitePath);
  }
  element(el) {
    const v = el.getAttribute(this.attr);
    if (!v || /^[a-z][a-z0-9+.-]*:/i.test(v) || v.startsWith("#") || v.startsWith("//")) return;
    let target;
    try { target = new URL(v, this.base); } catch { return; }
    let mapped = cachedPublicUrl(target.pathname);
    if (mapped && mapped.startsWith("/assets/")) mapped += `?v=${ASSET_VERSION}`;
    if (mapped) el.setAttribute(this.attr, mapped + target.hash);
  }
}

const INDEX_HEADER = "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1";

// Generated swarm pages (deploy/swarm). Returns null when the swarm doesn't own the path.
async function swarmResponse(request, env, ctx, sitePath) {
  const m = /^geocities\/([^/]+)\.html$/.exec(sitePath);
  if (!m) return null;
  const n = liveCount(Date.now(), env.SWARM_CAP);
  const c = classify(m[1], n, STATIC_GEO);
  if (!c) return null;
  if (c.kind === "pending") return notFound();

  const cache = caches.default;
  const cacheKey = new Request(request.url, { method: "GET" });
  const hit = await cache.match(cacheKey);
  if (hit) return request.method === "HEAD" ? new Response(null, hit) : hit;

  let html = null, indexable = false, ttl = 86400;
  if (c.kind === "member") ({ html, indexable } = renderMember(c.id, n, STATIC_GEO, ASSET_VERSION));
  else if (c.kind === "dir") { html = renderDir(c.sub, c.p, n, STATIC_GEO); ttl = 21600; }
  else if (c.kind === "dir-index") { html = renderDirIndex(n, STATIC_GEO); indexable = true; ttl = 21600; }
  else if (c.kind === "lang") { html = renderLang(c.code, n, STATIC_GEO); indexable = true; ttl = 21600; }
  if (!html) return notFound();

  const headers = retroHeaders("text/html; charset=utf-8");
  headers.set("Cache-Control", `public, max-age=${ttl}`);
  headers.set("X-Robots-Tag", indexable ? INDEX_HEADER : "noindex, follow");
  const res = new Response(html, { status: 200, headers });
  ctx.waitUntil(cache.put(cacheKey, res.clone()));
  return request.method === "HEAD" ? new Response(null, res) : res;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/robots.txt") {
      return new Response(ROBOTS, { headers: retroHeaders("text/plain; charset=utf-8") });
    }
    if (url.pathname === "/sitemap.xml") {
      return new Response(SITEMAP_INDEX, { headers: retroHeaders("application/xml; charset=utf-8") });
    }
    if (url.pathname === "/sitemap-core.xml") {
      cachedCoreSitemap ||= urlset(STORY_PATHS);
      return new Response(cachedCoreSitemap, { headers: retroHeaders("application/xml; charset=utf-8") });
    }
    if (url.pathname === "/sitemap-swarm.xml") {
      const n = liveCount(Date.now(), env.SWARM_CAP);
      return new Response(urlset(sitemapSitePaths(n)), { headers: retroHeaders("application/xml; charset=utf-8") });
    }
    if (url.pathname === `/${INDEXNOW_KEY}.txt`) {
      return new Response(INDEXNOW_KEY, { headers: retroHeaders("text/plain; charset=utf-8") });
    }
    const { sitePath, canonical } = resolve(url.hostname, url.pathname);

    if (canonical) return Response.redirect(canonical, 301);
    if (url.protocol === "http:") {
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    if (!sitePath) return notFound();

    const swarm = await swarmResponse(request, env, ctx, sitePath);
    if (swarm) return swarm;

    const base = env.BASE_STATIC_URL.replace(/\/+$/, "");
    const encoded = sitePath.split("/").map(encodeURIComponent).join("/");
    const bust = `?v=${ASSET_VERSION}`;
    const upstream = await fetch(`${base}/${encoded}${bust}`, {
      method: request.method === "HEAD" ? "HEAD" : "GET",
      cf: { cacheTtl: 3600, cacheEverything: true },
    });
    if (!upstream.ok) return notFound();

    const type = upstream.headers.get("Content-Type") || "application/octet-stream";
    const headers = retroHeaders(type);
    if (!sitePath.startsWith("assets/")) {
      if (isStory(sitePath)) {
        headers.set("X-Robots-Tag", INDEX_HEADER);
      } else {
        headers.set("X-Robots-Tag", "noindex, follow");
      }
    }
    const response = new Response(upstream.body, { status: 200, headers });
    if (!type.startsWith("text/html")) return response;

    return new HTMLRewriter()
      .on("head", new HeadInjector(publicUrl(sitePath) || url.toString()))
      .on("[href]", new LinkRewriter("href", sitePath))
      .on("[src]", new LinkRewriter("src", sitePath))
      .on("[background]", new LinkRewriter("background", sitePath))
      .transform(response);
  },
};
