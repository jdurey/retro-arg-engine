/**
 * Wildcard Edge Router for Nova Hart ARG
 * 
 * Intercepts wildcard subdomain requests (e.g. *.your-domain.com) and internally
 * rewrites them to the correct static path served by the underlying host.
 * 
 * Subdomain mapping:
 * - [slug].geocities.your-domain.com -> /geocities/[slug].html
 * - [group].usenet.your-domain.com -> /usenet/[group]/...
 * - ftp.[site].your-domain.com -> /ftp/[site]/...
 * - [node].regional.your-domain.com -> /regional/[node]/...
 */

// If hosting the site/ folder on Cloudflare Pages, bind this worker to the Pages project
// OR set this to your Pages dev URL (e.g., https://my-retro-arg.pages.dev)
const BASE_STATIC_URL = "https://your-pages-project.pages.dev"; 

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const hostname = url.hostname;
    
    let path = url.pathname;
    if (path === "/") {
      path = "/index.html";
    }

    // Rewrite URL based on subdomain patterns
    if (hostname.includes(".geocities.")) {
      const slug = hostname.split(".geocities.")[0];
      path = `/geocities/${slug}.html`;
    } 
    else if (hostname.includes(".usenet.")) {
      const group = hostname.split(".usenet.")[0];
      if (path === "/index.html" || path === "/") {
        path = `/usenet/${group}/index.html`;
      } else {
        path = `/usenet/${group}${path}`;
      }
    } 
    else if (hostname.startsWith("ftp.")) {
      const parts = hostname.split(".");
      const site = parts[1]; // ftp.ashford-poly.your-domain.com -> ashford-poly
      if (path === "/index.html" || path === "/") {
        path = `/ftp/${site}/index.html`;
      } else {
        path = `/ftp/${site}${path}`;
      }
    }
    else if (hostname.includes(".regional.")) {
      const node = hostname.split(".regional.")[0]; // e.g., 01-usa
      if (path === "/index.html" || path === "/") {
        path = `/regional/${node}/index.html`;
      } else {
        path = `/regional/${node}${path}`;
      }
    }

    // 1. Fetch the static asset from the backend bucket/Pages project
    const targetUrl = new URL(path, env.BASE_STATIC_URL || BASE_STATIC_URL);
    let response = await fetch(targetUrl.toString(), request);
    
    // 2. Spoof 1994 server headers to maintain the ARG immersion
    response = new Response(response.body, response);
    response.headers.set("Server", "CERN-HTTPd/3.0");
    response.headers.set("X-Powered-By", "Stardust");

    return response;
  }
};
