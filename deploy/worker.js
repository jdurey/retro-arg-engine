import { APEX, isStory, publicUrl, resolve } from "./urlmap.js";
import STORY_PATHS from "./story_paths.js";

const OG_DESCRIPTION = "A 1994 webring for fans of Nova Hart and the 14.2 Hz Stardust signal. Something is still transmitting.";
const OG_IMAGE = `https://${APEX}/assets/og_card.jpg`;

const ROBOTS = `User-agent: *\nAllow: /\n\nSitemap: https://${APEX}/sitemap.xml\n`;
// IndexNow keys are public by design (they prove control of the host, nothing more).
const INDEXNOW_KEY = "37feeed875722863fda484c68e6695e5";
// Bump when files in assets/ are replaced so edge + browser caches refetch.
const ASSET_VERSION = "9";

function sitemap() {
  const urls = STORY_PATHS.map((sp) => publicUrl(sp)).filter((u) => u && u.startsWith("https://"));
  const body = urls.map((u) => `  <url><loc>${u.replace(/&/g, "&amp;")}</loc></url>`).join("\n");
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
}

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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/robots.txt") {
      return new Response(ROBOTS, { headers: retroHeaders("text/plain; charset=utf-8") });
    }
    if (url.pathname === "/sitemap.xml") {
      return new Response(sitemap(), { headers: retroHeaders("application/xml; charset=utf-8") });
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
    if (!sitePath.startsWith("assets/") && !isStory(sitePath)) headers.set("X-Robots-Tag", "noindex, follow");
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
