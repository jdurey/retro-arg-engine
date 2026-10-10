export default async (request, context) => {
  const url = new URL(request.url);
  const hostname = url.hostname;
  
  let path = url.pathname;
  if (path === "/") {
    path = "/index.html";
  }

  let rewritten = false;

  // Rewrite URL based on subdomain patterns
  if (hostname.includes(".geocities.")) {
    const slug = hostname.split(".geocities.")[0];
    path = `/geocities/${slug}.html`;
    rewritten = true;
  } else if (hostname.includes(".usenet.")) {
    const group = hostname.split(".usenet.")[0];
    path = (path === "/index.html" || path === "/") ? `/usenet/${group}/index.html` : `/usenet/${group}${path}`;
    rewritten = true;
  } else if (hostname.startsWith("ftp.")) {
    const site = hostname.split(".")[1];
    path = (path === "/index.html" || path === "/") ? `/ftp/${site}/index.html` : `/ftp/${site}${path}`;
    rewritten = true;
  } else if (hostname.includes(".regional.")) {
    const node = hostname.split(".regional.")[0];
    path = (path === "/index.html" || path === "/") ? `/regional/${node}/index.html` : `/regional/${node}${path}`;
    rewritten = true;
  }

  if (rewritten) {
    url.pathname = path;
  }

  // Pass the (potentially rewritten) request to the underlying static files
  const response = await context.next(rewritten ? new Request(url, request) : request);
  
  // Spoof 1994 server headers to maintain the ARG immersion
  response.headers.set("Server", "CERN-HTTPd/3.0");
  response.headers.set("X-Powered-By", "Stardust");

  return response;
};
