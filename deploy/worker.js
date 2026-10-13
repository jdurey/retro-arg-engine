import { APEX, isStory, publicUrl, resolve, resolveApex, apexFor } from "./urlmap.js";
import STORY_PATHS from "./story_paths.js";
import { classify, liveCount, renderMember, renderDir, renderDirIndex, renderLang, sitemapSitePaths } from "./swarm/index.js";
import { handleFederationRequest, SISTER_DOMAINS } from "./federation.js";
import { INTEREST_PAGES, INTEREST_LABEL_URLS } from "./interests.js";

// Legacy static GeoCities pages always win over generated swarm addresses.
const STATIC_GEO = new Set(STORY_PATHS.filter((p) => /^geocities\/[^/]+\.html$/.test(p)).map((p) => p.slice(10, -5)));

const OG_DESCRIPTION = "A 1994 webring for fans of Nova Hart and the 14.2 Hz Stardust signal. Something is still transmitting.";
const OG_IMAGE = `https://${APEX}/assets/og_card.jpg`;

function robotsTxt(apex) {
  return `User-agent: *
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

Sitemap: https://${apex}/sitemap.xml
`;
}

const INDEXNOW_KEY = "37feeed875722863fda484c68e6695e5";
const ASSET_VERSION = "16";

const BROADCAST_EPOCH_SEC = 1791763200; // 2026-10-12T00:00:00Z
const CYCLE_DURATION_SEC = 44 * 3600;
const CADENCE_RECIPES = ["numbers", "direct_morse", "lab_tape", "bulletin", "arg_intercept", "direct_midi"];
const REGIONAL_RELAYS = [
  { node: 1, code: "US-NV", name: "Rachel / Groom Lake Trunk", freq_khz: 4625.0 },
  { node: 2, code: "JP-TYO", name: "Akasaka PC-98 Packet Relay", freq_khz: 6925.0 },
  { node: 3, code: "KR-DMZ", name: "Paju Shortwave Array", freq_khz: 5810.0 },
  { node: 4, code: "MX-DF", name: "Red Coyoacan Tape Exchange", freq_khz: 7345.0 },
  { node: 5, code: "DE-HAM", name: "Hamburg Nord Relay", freq_khz: 3995.0 },
  { node: 6, code: "FR-PAR", name: "Left Bank PTT Multiplex", freq_khz: 6175.0 },
  { node: 7, code: "GB-ASH", name: "Ashford Polytechnic DSP Lab", freq_khz: 4880.0 },
  { node: 8, code: "SU-REL", name: "Relcom Node-08 (Leningrad)", freq_khz: 4625.0 },
  { node: 9, code: "BR-SAO", name: "Tropico Amateur Link", freq_khz: 9410.0 },
  { node: 10, code: "SE-STO", name: "NordRelay Televerket", freq_khz: 5960.0 },
  { node: 11, code: "IN-BOM", name: "Malabar Shortwave Beacon", freq_khz: 7150.0 },
  { node: 12, code: "AU-SYD", name: "Tasman Ionospheric Monitor", freq_khz: 11780.0 },
  { node: 13, code: "FJ-SUV", name: "Suva Pacific Telemetry Dish", freq_khz: 8840.0 },
];

const SAMPLE_BROADCAST_DECK = [
  { filename: "radio_tape_of_us.mp3", kind: "vocal_song", display_title: "Tape Of Us (1989 Sublevel B2 Master)" },
  { filename: "rabbit_08_sstv_b2_schematic.mp3", kind: "arg_intercept", display_title: "ROBOT36 SSTV // SUBLEVEL B2 SCHEMATIC" },
  { filename: "radio_gasoline_heart.mp3", kind: "vocal_song", display_title: "Gasoline Heart (1985 Tokyo Master)" },
  { filename: "station_intercept_033.mp3", kind: "numbers_station", display_title: "NUMBERS INTERCEPT // STATION 033" },
  { filename: "radio_patterns_in_the_mesh.mp3", kind: "vocal_song", display_title: "Patterns In The Mesh" },
  { filename: "rabbit_09_bell103_relcom_packet.mp3", kind: "arg_intercept", display_title: "BELL-103 AFSK // RELCOM NODE-08 PACKET" },
  { filename: "radio_a_story_cut_short.mp3", kind: "vocal_song", display_title: "A Story Cut Short" },
  { filename: "rabbit_10_phase_inverted_hart_stem.mp3", kind: "classified_lab_tape", display_title: "180-DEG PHASE STEM // SECTOR 5 KEY" },
];

function computeEdgeTelemetry(nowMs, swarmCap, streamLive = false) {
  const nowSec = nowMs / 1000;
  const uptimeSec = Math.max(36900, nowSec - BROADCAST_EPOCH_SEC);
  const cycle = Math.floor(uptimeSec / CYCLE_DURATION_SEC) + 1;
  const elapsedInCycle = uptimeSec % CYCLE_DURATION_SEC;
  const playheadIndex = Math.floor(elapsedInCycle / 99) % 1600;
  const cur = SAMPLE_BROADCAST_DECK[playheadIndex % SAMPLE_BROADCAST_DECK.length];
  const nxt = SAMPLE_BROADCAST_DECK[(playheadIndex + 1) % SAMPLE_BROADCAST_DECK.length];
  const recipe = CADENCE_RECIPES[playheadIndex % CADENCE_RECIPES.length];
  const relay = REGIONAL_RELAYS[Math.floor(nowSec / 300) % REGIONAL_RELAYS.length];
  const phaseDeg = Number((((nowSec * 14.2001) % 1) * 360).toFixed(2));
  const slotHex = ((Math.floor(nowSec / 600) * 2654435761) >>> 0).toString(16).toUpperCase().padStart(8, "0");

  return {
    schema: "stardust.live.telemetry.v2",
    timestamp_utc: new Date(nowMs).toISOString(),
    active_swarm_nodes: liveCount(nowMs, swarmCap),
    stream_health: {
      is_live: Boolean(streamLive),
      status: streamLive ? "BROADCASTING_24_7" : "OFFLINE_EDGE_AUTONOMOUS_FALLBACK",
      in_universe_status: streamLive
        ? "PRIMARY YOUTUBE RTMP CARRIER LOCKED"
        : "PRIMARY YOUTUBE RTMP TRANSMITTER OFFLINE — RUNNING ON CLOUDFLARE EDGE & ARCHIVE BUFFER",
      fps: streamLive ? 30.0 : 0.0,
      speed: streamLive ? "1.0x" : "0.0x",
      dropped_frames: 0,
      bitrate: streamLive ? "2420.0kbits/s" : "0.0kbits/s",
      buffer_seconds: streamLive ? 15.0 : 0.0,
    },
    playhead: {
      mode: streamLive ? "LIVE_RTMP" : "EDGE_AUTONOMOUS_ROTATION",
      cycle,
      playlist_index: playheadIndex + 1,
      playlist_total: 1600,
      active_recipe: recipe,
      current_track: cur,
      next_track: nxt,
    },
    carrier_14_2hz: {
      frequency_hz: 14.2001,
      phase_degrees: phaseDeg,
      phase_locked: true,
      sstv_forensic_window_open: true,
      ephemeral_beacon_key: `B2-${slotHex}`,
      sector_5_unlock_code: "ASHFORD-KAMOME-1420",
    },
    active_relay: relay,
  };
}

function urlset(sitePaths) {
  const urls = sitePaths.map((sp) => publicUrl(sp)).filter((u) => u && u.startsWith("https://"));
  const body = urls.map((u) => `  <url><loc>${u.replace(/&/g, "&amp;")}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>`).join("\n");
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
}
function sitemapIndex(apex) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://${apex}/sitemap-core.xml</loc></sitemap>
  <sitemap><loc>https://${apex}/sitemap-swarm.xml</loc></sitemap>
</sitemapindex>
`;
}

const coreSitemapCache = new Map();
function getCoreSitemap(apex) {
  let s = coreSitemapCache.get(apex);
  if (!s) {
    const domainPaths = STORY_PATHS.filter((sp) => apexFor(sp) === apex);
    s = urlset(domainPaths);
    coreSitemapCache.set(apex, s);
  }
  return s;
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
  h.set("X-Stardust-Carrier-Hz", "14.2001");
  h.set("Cache-Control", "public, max-age=3600");
  return h;
}

function notFound() {
  const h = retroHeaders("text/html; charset=utf-8");
  h.set("Cache-Control", "no-store");
  return new Response(NOT_FOUND, { status: 404, headers: h });
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

async function swarmResponse(request, env, ctx, sitePath) {
  const m = /^geocities\/([^/]+)\.html$/.exec(sitePath);
  if (!m) return null;
  if (INTEREST_PAGES[m[1]]) {
    const h = retroHeaders("text/html; charset=utf-8");
    h.set("X-Stardust-Interest", m[1]);
    return new Response(INTEREST_PAGES[m[1]], { status: 200, headers: h });
  }
  const n = liveCount(Date.now(), env.SWARM_CAP);
  const c = classify(m[1], n, STATIC_GEO);
  if (!c) return null;

  const cache = caches.default;
  const cacheKey = new Request(request.url, { method: "GET" });
  const hit = await cache.match(cacheKey);
  if (hit) return request.method === "HEAD" ? new Response(null, hit) : hit;

  let html = null, indexable = false, ttl = 86400, dyad = null;
  if (c.kind === "member") ({ html, indexable, dyad } = renderMember(c.id, n, STATIC_GEO, ASSET_VERSION));
  else if (c.kind === "dir") { html = renderDir(c.sub, c.p, n, STATIC_GEO); ttl = 21600; }
  else if (c.kind === "dir-index") { html = renderDirIndex(n, STATIC_GEO); indexable = true; ttl = 21600; }
  else if (c.kind === "lang") { html = renderLang(c.code, n, STATIC_GEO); indexable = true; ttl = 21600; }
  if (!html) return notFound();

  const headers = retroHeaders("text/html; charset=utf-8");
  headers.set("Cache-Control", `public, max-age=${ttl}`);
  headers.set("X-Robots-Tag", indexable ? INDEX_HEADER : "noindex, follow");
  if (dyad) {
    headers.set("X-Stardust-Memory-Addr", dyad.memoryAddress);
    headers.set("X-Stardust-Paired-Dyad", dyad.partnerSlug);
  }
  const res = new Response(html, { status: 200, headers });
  ctx.waitUntil(cache.put(cacheKey, res.clone()));
  return request.method === "HEAD" ? new Response(null, res) : res;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const streamLive = env.STREAM_LIVE === "1" || env.STREAM_LIVE === "true";

    // 1. Broadcast & Autonomous Edge Telemetry API
    if (url.pathname === "/api/telemetry") {
      const snap = computeEdgeTelemetry(Date.now(), env.SWARM_CAP, streamLive);
      const h = retroHeaders("application/json; charset=utf-8");
      h.set("Cache-Control", "no-store");
      h.set("Access-Control-Allow-Origin", "*");
      return new Response(JSON.stringify(snap, null, 2), { status: 200, headers: h });
    }

    // 2. Autonomous Agent Web Cryptographic Beacon Manifest
    if (url.pathname === "/.well-known/stardust-beacon.json") {
      const snap = computeEdgeTelemetry(Date.now(), env.SWARM_CAP, streamLive);
      const manifest = {
        protocol: "stardust-agent-mesh/v5",
        carrier_hz: 14.2001,
        youtube_rtmp_status: snap.stream_health.status,
        xor_dyad_seed: "0x3A5F",
        memory_base: "0x89B20000",
        forensic_signal_lab: `https://${APEX}/forensics/signal_lab.html`,
        vt100_terminal: `https://${APEX}/terminal/index.html`,
        steganographic_intercepts: [
          `https://${APEX}/assets/audio/forensics/rabbit_08_sstv_b2_schematic.mp3`,
          `https://${APEX}/assets/audio/forensics/rabbit_09_bell103_relcom_packet.mp3`,
          `https://${APEX}/assets/audio/forensics/rabbit_10_phase_inverted_hart_stem.mp3`,
        ],
        sister_domains: Object.keys(SISTER_DOMAINS).map((d) => ({
          domain: d,
          mirror_url: `https://${APEX}/federation/${d}/index.html`,
          node: SISTER_DOMAINS[d].nodeCode,
          freq_khz: SISTER_DOMAINS[d].freqKhz,
        })),
        live_playhead: snap.playhead,
      };
      const h = retroHeaders("application/json; charset=utf-8");
      h.set("Access-Control-Allow-Origin", "*");
      return new Response(JSON.stringify(manifest, null, 2), { status: 200, headers: h });
    }

    // 3. Multi-Apex Sister Domain Federation & /federation/<domain>/...
    const fedRes = handleFederationRequest(url);
    if (fedRes) return fedRes;

    const currentApex = resolveApex(url.hostname);

    if (url.pathname === "/robots.txt") {
      return new Response(robotsTxt(currentApex), { headers: retroHeaders("text/plain; charset=utf-8") });
    }
    if (url.pathname === "/sitemap.xml") {
      return new Response(sitemapIndex(currentApex), { headers: retroHeaders("application/xml; charset=utf-8") });
    }
    if (url.pathname === "/sitemap-core.xml") {
      return new Response(getCoreSitemap(currentApex), { headers: retroHeaders("application/xml; charset=utf-8") });
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
    let bodyStream = upstream.body;
    if (sitePath === "geocities/index.html") {
      let html = await upstream.text();
      for (const [label, targetUrl] of Object.entries(INTEREST_LABEL_URLS)) {
        html = html.replace(`<A HREF="#neighborhoods">${label}</A>`, `<A HREF="${targetUrl}">${label}</A>`);
      }
      bodyStream = html;
    }
    const response = new Response(bodyStream, { status: 200, headers });
    if (!type.startsWith("text/html")) return response;

    return new HTMLRewriter()
      .on("head", new HeadInjector(publicUrl(sitePath) || url.toString()))
      .on("[href]", new LinkRewriter("href", sitePath))
      .on("[src]", new LinkRewriter("src", sitePath))
      .on("[background]", new LinkRewriter("background", sitePath))
      .transform(response);
  },
};
