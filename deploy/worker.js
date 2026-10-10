import { APEX, publicUrl, resolve } from "./urlmap.js";

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
    const mapped = publicUrl(target.pathname);
    if (mapped) el.setAttribute(this.attr, mapped + target.hash);
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const { sitePath, canonical } = resolve(url.hostname, url.pathname);

    if (canonical) return Response.redirect(canonical, 301);
    if (url.protocol === "http:") {
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    if (!sitePath) return notFound();

    const base = env.BASE_STATIC_URL.replace(/\/+$/, "");
    const encoded = sitePath.split("/").map(encodeURIComponent).join("/");
    const upstream = await fetch(`${base}/${encoded}`, {
      method: request.method === "HEAD" ? "HEAD" : "GET",
      cf: { cacheTtl: 3600, cacheEverything: true },
    });
    if (!upstream.ok) return notFound();

    const type = upstream.headers.get("Content-Type") || "application/octet-stream";
    const response = new Response(upstream.body, { status: 200, headers: retroHeaders(type) });
    if (!type.startsWith("text/html")) return response;

    return new HTMLRewriter()
      .on("[href]", new LinkRewriter("href", sitePath))
      .on("[src]", new LinkRewriter("src", sitePath))
      .on("[background]", new LinkRewriter("background", sitePath))
      .transform(response);
  },
};
