export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const hostname = url.hostname;
    
    let path = url.pathname;
    if (path === "/") {
      path = "/index.html";
    }

    if (hostname.includes(".geocities.")) {
      const slug = hostname.split(".geocities.")[0];
      path = `/geocities/${slug}.html`;
    } 
    else if (hostname.includes(".usenet.")) {
      const group = hostname.split(".usenet.")[0];
      path = (path === "/index.html" || path === "/") ? `/usenet/${group}/index.html` : `/usenet/${group}${path}`;
    } 
    else if (hostname.startsWith("ftp.")) {
      const parts = hostname.split(".");
      const site = parts[1];
      path = (path === "/index.html" || path === "/") ? `/ftp/${site}/index.html` : `/ftp/${site}${path}`;
    }
    else if (hostname.includes(".regional.")) {
      const node = hostname.split(".regional.")[0];
      path = (path === "/index.html" || path === "/") ? `/regional/${node}/index.html` : `/regional/${node}${path}`;
    }

    // Fetch the static asset from Cloudflare Pages
    // Note: ensure BASE_STATIC_URL points to the Cloudflare Pages deploy URL (e.g. https://your-site.pages.dev)
    const targetUrl = new URL(path, env.BASE_STATIC_URL);
    let response = await fetch(targetUrl.toString(), request);
    
    response = new Response(response.body, response);
    response.headers.set("Server", "CERN-HTTPd/3.0");
    response.headers.set("X-Powered-By", "Stardust");

    return response;
  }
};
