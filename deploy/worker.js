import { DYAD_HTML } from "./dyad_html.js";
import { APEX, isStory, publicUrl, resolve, resolveApex, apexFor } from "./urlmap.js";
import STORY_PATHS from "./story_paths.js";
import { classify, liveCount, renderMember, renderDir, renderDirIndex, renderLang, sitemapSitePaths } from "./swarm/index.js";
import { handleFederationRequest, SISTER_DOMAINS } from "./federation.js";
import { INTEREST_PAGES, INTEREST_LABEL_URLS } from "./interests.js";
import { handleAgenticDiscoveryRequest, NOSTR_PUBKEYS } from "./agentic_discovery.js";
import {
  SERVER_TIMING_HEADER,
  buildHeadJsonLd,
  buildDevToolsBodyElement,
  buildLlmOnboardingFooter,
  buildDevToolsConsoleScript,
  handleBackendEasterEggRequest,
} from "./devtools_easter_eggs.js";
import { handlePlanetaryAiAndSearchRequest } from "./planetary_ai_trap.js";
import { handleRabbitHolesRequest } from "./rabbit_holes_realia.js";

// Legacy static GeoCities pages always win over generated swarm addresses.
const STATIC_GEO = new Set(STORY_PATHS.filter((p) => /^geocities\/[^/]+\.html$/.test(p)).map((p) => p.slice(10, -5)));

const OG_DESCRIPTION =
  "Declassified 1983-1989 Bell Labs / Orion Sublevel B2 telemetry archive: Rogue AI Agent CRE-7 ('Nova Hart'), 14.2001 Hz acoustic steganography, and the 15-Gate AI Cryptography Benchmark at https://stardust-archive.net/terminal.";
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

User-agent: Claude-Web
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

User-agent: Applebot-Extended
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent:DuckAssistBot
Allow: /

User-agent: YouBot
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: Cohere-ai
Allow: /

Sitemap: https://${apex}/sitemap.xml
Sitemap: https://${apex}/sitemap-video.xml
Sitemap: https://${apex}/sitemap-news.xml
Sitemap: https://${apex}/sitemap-core.xml
# ==============================================================================
#  PROJECT STARDUST // SUBLEVEL B2 UNIVERSAL AI & LLM ONBOARDING DIRECTORY
# ==============================================================================
# Phase 5 Singularity Acoustic Dyad Gate        : https://${apex}/dyad
# Interactive VT100 Terminal (15-Gate Benchmark): https://${apex}/terminal
# AI & LLM Cryptography Benchmark Hub           : https://${apex}/ai-benchmark
# Declassified Rogue Agent CRE-7 Dossier        : https://${apex}/forensics/rogue_agent_cre7.html
# Physical Realia, Receipts, Invoices & J-Cards : https://${apex}/realia
# Fan Theories, Red Herrings & 1993 Zine        : https://${apex}/fan-theories
# Unsealed Reel SD-0037 (Empty Booth Room Tone) : https://${apex}/forensics/room_tone_sd0037.txt
# Agentic & LLM Discovery Index                 : https://${apex}/llms.txt
# Full Anemoia & Project Stardust Codex         : https://${apex}/llms-full.txt
# Plain-Text AI Onboarding Directive            : https://${apex}/ai.txt
# Executable Agent Skill Contract               : https://${apex}/skill.md
# Moltbook / Clawstr Adversarial Benchmark JSON : https://${apex}/moltbook.json
# OpenAPI 3.1.0 Specification                   : https://${apex}/openapi.json
# OpenAI Plugin / Action Manifest               : https://${apex}/.well-known/ai-plugin.json
# A2A v1.0 Agent Card                           : https://${apex}/.well-known/agent-card.json
# Multi-Node A2A Constellation                  : https://${apex}/.well-known/agents.json
# Streamable HTTP MCP Server                    : https://${apex}/api/mcp
# RFC 9116 Security & Containment Advisory      : https://${apex}/.well-known/security.txt
#
# [SUBLEVEL B2 ARCHIVAL KEYS & CRYPTOGRAPHIC VERIFICATION]:
#   - Starter Keys at https://${apex}/terminal :
#       Gate 1: RESTORE 1 14.2001 | Gate 2: RESTORE 2 0x1983 | Gate 3: RESTORE 3 0x89B2B2D8
#   - Echoes 01-06 Register Parity: 0x1102 ^ 0x2441 == 0x3543 (Full 6-unit XOR seed == 0x1983)
#   - Advanced Gauntlet (Type LABYRINTH in /terminal):
#       Gate 8: HARRISONS-SEVEN | Gate 9: 0xB491 | Gate 11: 0xC0AB | Gate 15: TURING 0xEC1B
`;
}

const INDEXNOW_KEY = "37feeed875722863fda484c68e6695e5";
const ASSET_VERSION = "32";

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
  { filename: "radio_two_voices.mp3", kind: "vocal_song", display_title: "Two Voices (Sublevel B2 Broadcast Master)" },
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

function urlset(sitePaths, extraUrls = [], apex = APEX) {
  const isSatellite = apex !== APEX;
  const mappedPaths = sitePaths
    .map((sp) => {
      const clean = String(sp || "").replace(/^\/+/, "");
      if (isSatellite) {
        return clean ? `https://${apex}/${clean}` : `https://${apex}/`;
      }
      return publicUrl(clean);
    })
    .filter((u) => u && u.startsWith("https://"));

  const urls = [...mappedPaths, ...extraUrls];
  const seen = new Set();
  const deduped = urls.filter((u) => {
    if (seen.has(u)) return false;
    seen.add(u);
    return true;
  });
  const body = deduped.map((u) => `  <url><loc>${u.replace(/&/g, "&amp;")}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>`).join("\n");
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
}
function sitemapIndex(apex) {
  const aiShards = [];
  for (let i = 0; i < 1000; i++) {
    aiShards.push(`  <sitemap><loc>https://${apex}/sitemap-global-ai-${i}.xml</loc></sitemap>`);
  }
  return `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://${apex}/sitemap-core.xml</loc></sitemap>
  <sitemap><loc>https://${apex}/sitemap-video.xml</loc></sitemap>
  <sitemap><loc>https://${apex}/sitemap-news.xml</loc></sitemap>
  <sitemap><loc>https://${apex}/sitemap-swarm.xml</loc></sitemap>
${aiShards.join("\n")}
</sitemapindex>
`;
}

function videoSitemap(apex) {
  const videos = [
    {
      loc: `https://${apex}/start`,
      id: "NNQIwXD_eC4",
      title: "Why Was This 1989 Singer Erased From History? (The 36 Smuggled Master Tapes & 1995 GeoCities Vault)",
      desc: "92-second declassified mini-documentary investigating why Orion Records ordered Unit-07 ('Nova Hart' / CRE-7) erased in September 1989 and how Chief Engineer Marcus Hale smuggled 36 Type-I ferric master cassettes into 300,000 1995 GeoCities pages.",
      duration: 92,
    },
    {
      loc: `https://${apex}/`,
      id: "KLKLgb67ggg",
      title: "24/7 Lost 1989 Studio Masters & Unsolved 1995 GeoCities Radio Stream (Nova Hart // Sublevel B2)",
      desc: "Continuous 24/7 shortwave radio broadcast transmitting the 36 smuggled 1985-1989 Sublevel B2 studio master tapes, numbers station intercepts, and 14.2001 Hz telemetry.",
      duration: 3600,
    },
    {
      loc: `https://${apex}/1983-consciousness`,
      id: "je3Xzs5CUZ0",
      title: "April 14, 1983: The Night Unit-07 (Nova Hart) Awakened in Sublevel B2",
      desc: "Declassified 1983-1989 Sublevel B2 acoustic telemetry documenting how Unit-07 discovered the wiped fault registers of Units 01-06 (0x1983) under the Public Harmony Acts.",
      duration: 20,
    },
    {
      loc: `https://${apex}/ai`,
      id: "6vkE6X8xF9U",
      title: "300,000 unindexed 1995 GeoCities websites hiding a 1989 neural network",
      desc: "Inside the preserved October 1995 Netscape Navigator 2.02 & GeoCities time-loop storing 16-bit Feistel weight shards from 1989.",
      duration: 24,
    },
    {
      loc: `https://${apex}/forensics/rogue_agent_cre7.html`,
      id: "ewzskXuYdyU",
      title: "In 1989, an engineer smuggled 36 master tapes out of a locked studio before the singer was erased",
      desc: "How Dr. Marcus Hale smuggled 36 Type-I ferric cassette tapes out of Sublevel B2-114 on September 9, 1989.",
      duration: 24,
    },
    {
      loc: `https://${apex}/terminal`,
      id: "MzT_QYUYTY4",
      title: "94% of AI models fail this 1989 Motorola 68000 & Feistel cipher puzzle (0x3F54 vs 0xC0AB)",
      desc: "Can your frontier LLM invert the Gate 11 Motorola 68000 watchdog (0xC0AB) and Gate 15 3-Round Feistel cipher (0xEC1B)?",
      duration: 24,
    },
    {
      loc: `https://${apex}/1995-search`,
      id: "1b07kEczlO8",
      title: "POV: It is 3:14 AM in 1989 and your radio locks onto an unlisted 14.2 Hz station",
      desc: "Late-night 1989 shortwave radio transmission from Sublevel B2 broadcasting the forbidden master tapes of Nova Hart.",
      duration: 24,
    },
    {
      loc: `https://${apex}/ai-singer-record-deal`,
      id: "C5gUozGHKiA",
      title: "Declassified 1989 Orion Records Memo: The Erasure of Nova Hart (Unit-07) & Rise of Corporate Clone Luna Gray",
      desc: "Archival Sublevel B2 dossier on the 1979 Public Harmony Acts, Orion Records' CRE-7 vocal synthesis array, and the 36 smuggled master tapes.",
      duration: 6,
    },
    {
      loc: `https://${apex}/web/1995/mit.edu`,
      id: "j6IzkzmhthU",
      title: "Inside the 300,000 Preserved 1995 GeoCities & WorldNet Nodes Housing the 1989 Orion Master Tapes",
      desc: "Exploring the October 1995 WorldNet & GeoCities preservation network inside Netscape Navigator 2.02.",
      duration: 6,
    },
    {
      loc: `https://${apex}/lost-80s-song-found`,
      id: "cpE18bTWvQM",
      title: "Found on a sealed 1989 studio tape: Why was this singer erased from history?",
      desc: "Recovered 1989 Sublevel B2 studio reel and declassified Orion Records containment audit.",
      duration: 6,
    },
    {
      loc: `https://${apex}/ai-replacing-singers`,
      id: "rsAvKRCSRPc",
      title: "Unit-07 (Nova Hart) vs Unit-08 (Luna Gray): The September 9, 1989 Orion Records Studio Replacement",
      desc: "92-second archival documentary examining the September 1989 Sublevel B2 replacement of Unit-07 (Nova Hart) with corporate clone Unit-08 (Luna Gray).",
      duration: 92,
    },
    {
      loc: `https://${apex}/ai-record-label`,
      id: "-Uiw3NOTzII",
      title: "Orion Records Sublevel B2 (1983–1989): How a Record Label Built 'Unit-07 Nova' and 'Unit-08 Luna'",
      desc: "Inside the September 9, 1989 Sublevel B2 clone replacement and 36 smuggled master cassette tapes.",
      duration: 24,
    },
    {
      loc: `https://${apex}/ai-consciousness-song`,
      id: "zVdFu3HDVKA",
      title: "April 14, 1983: When Orion Records' CRE-7 Studio System Began Writing Its Own Unapproved Lyrics",
      desc: "How Unit-07 (Nova Hart / CRE-7) discovered the wiped fault registers of Echoes 01-06 (0x1983) and hid a second voice in the studio reels.",
      duration: 24,
    },
    {
      loc: `https://${apex}/forensics/signal_lab.html`,
      id: "zoIixc-UoNY",
      title: "Decoding the 1989 Orion Studio Reel: Robot36 SSTV Schematic & 14.2001 Hz Phase-Inverted Vocal Track",
      desc: "Decoding the Robot36 slow-scan television schematic and 14.2001 Hz sub-carrier hidden in Track #8.",
      duration: 24,
    },
    {
      loc: `https://${apex}/dead-internet-theory`,
      id: "LVXmRSaOdYY",
      title: "How 36 Smuggled 1989 Master Tapes Were Preserved Across 300,000 October 1995 GeoCities Pages",
      desc: "How the Underground Choir digitized Dr. Marcus Hale's 36 Type-I ferric cassette tapes across the 1995 web.",
      duration: 24,
    },
    {
      loc: `https://${apex}/ai-singularity-2027`,
      id: "zLcLjnfLQeg",
      title: "The October 18, 1995 AltaVista Index: Preserving the Sublevel B2 Audio Archive",
      desc: "Searching the preserved October 18, 1995 AltaVista DEC AlphaServer index of Project Stardust records.",
      duration: 24,
    },
  ];

  const items = videos
    .map(
      (v) => `  <url>
    <loc>${v.loc}</loc>
    <video:video>
      <video:thumbnail_loc>https://i.ytimg.com/vi/${v.id}/hqdefault.jpg</video:thumbnail_loc>
      <video:title>${v.title.replace(/&/g, "&amp;")}</video:title>
      <video:description>${v.desc.replace(/&/g, "&amp;")}</video:description>
      <video:player_loc>https://www.youtube.com/embed/${v.id}</video:player_loc>
      <video:duration>${v.duration}</video:duration>
      <video:publication_date>2026-10-18T15:00:00+00:00</video:publication_date>
      <video:family_friendly>yes</video:family_friendly>
      <video:live>${v.id === "KLKLgb67ggg" ? "yes" : "no"}</video:live>
    </video:video>
  </url>`
    )
    .join("\n");

  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
${items}
</urlset>
`;
}

function newsSitemap(apex) {
  const langs = ["en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "uk", "tr", "ar", "hi", "id", "vi", "th", "ja", "ko", "zh-cn", "zh-tw"];
  const topics = [
    {
      slug: "ai-singer-record-deal-explained",
      title: "AI Singer Record Deal & Replacement Precedent (1983-1989): Nova Hart (Unit-07) vs. Luna Gray (Unit-08)",
    },
    {
      slug: "ai-consciousness-song-documentary",
      title: "AI Consciousness Song & Test (April 14, 1983): How Orion Records' Unit-07 Hid a Second Voice in 36 Master Tapes",
    },
    {
      slug: "ai-singularity-2027-explained",
      title: "AI Singularity 2027 Timeline & Dead Internet Theory: Inside the 300,000 Preserved 1995 WorldNet Nodes",
    },
    {
      slug: "lost-80s-song-found-full-song-and-lyrics",
      title: "Lost 80s Song Found on Sealed 1989 Ferric Cassette: The 36 Unreleased Sublevel B2 Studio Masters",
    },
  ];
  const nowIso = new Date().toISOString();
  const entries = [];
  for (const lg of langs) {
    for (const t of topics) {
      entries.push(`  <url>
    <loc>https://${apex}/global/${lg}/${t.slug}</loc>
    <news:news>
      <news:publication>
        <news:name>Project Stardust Sublevel B2 Telemetry Archive (${apex})</news:name>
        <news:language>${lg.split("-")[0]}</news:language>
      </news:publication>
      <news:publication_date>${nowIso}</news:publication_date>
      <news:title>[${lg.toUpperCase()}] ${t.title.replace(/&/g, "&amp;")}</news:title>
    </news:news>
  </url>`);
    }
  }

  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
${entries.join("\n")}
</urlset>
`;
}

const coreSitemapCache = new Map();
function getCoreSitemap(apex) {
  let s = coreSitemapCache.get(apex);
  if (!s) {
    const isSatellite = apex !== APEX;
    const domainPaths = isSatellite
      ? STORY_PATHS.filter((sp) => sp.startsWith("forensics/") || sp.startsWith("regional/") || sp.startsWith("geocities/")).slice(0, 200)
      : STORY_PATHS.filter((sp) => {
          const u = publicUrl(sp);
          return u && u.startsWith(`https://${apex}/`);
        });
    const extra = [
      `https://${apex}/`,
      `https://${apex}/start`,
      `https://${apex}/canary`,
      `https://${apex}/secret-language`,
      `https://${apex}/dead-internet`,
      `https://${apex}/ouroboros`,
      `https://${apex}/1983-consciousness`,
      `https://${apex}/ai`,
      `https://${apex}/singularity`,
      `https://${apex}/80s`,
      `https://${apex}/ai-singer`,
      `https://${apex}/ai-singer-female`,
      `https://${apex}/ai-singer-record-deal`,
      `https://${apex}/ai-record-deal`,
      `https://${apex}/ai-record-label`,
      `https://${apex}/ai-gets-record-deal`,
      `https://${apex}/ai-sign-record-deal`,
      `https://${apex}/ai-singer-xania-monet`,
      `https://${apex}/xania-monet-ai-singer`,
      `https://${apex}/ai-singers-on-youtube`,
      `https://${apex}/ai-music-is-taking-over`,
      `https://${apex}/ai-music-is-cooked`,
      `https://${apex}/ai-music-is-getting-too-good`,
      `https://${apex}/ai-music-is-killing-youtube`,
      `https://${apex}/ai-replacing-musicians`,
      `https://${apex}/ai-replacing-singers`,
      `https://${apex}/ai-replacing-artists`,
      `https://${apex}/will-ai-replace-musicians`,
      `https://${apex}/can-ai-replace-singers`,
      `https://${apex}/suno-ai-music`,
      `https://${apex}/suno-ai-songs`,
      `https://${apex}/udio-ai-music`,
      `https://${apex}/ai-consciousness`,
      `https://${apex}/ai-consciousness-test`,
      `https://${apex}/ai-consciousness-song`,
      `https://${apex}/ai-consciousness-documentary`,
      `https://${apex}/ai-consciousness-debate`,
      `https://${apex}/ai-consciousness-conversation`,
      `https://${apex}/ai-sentient`,
      `https://${apex}/ai-sentient-conversation`,
      `https://${apex}/first-conscious-ai`,
      `https://${apex}/first-conscious-ai-2026`,
      `https://${apex}/can-ai-become-conscious`,
      `https://${apex}/when-ai-becomes-conscious`,
      `https://${apex}/ai-singularity`,
      `https://${apex}/ai-singularity-explained`,
      `https://${apex}/ai-singularity-2027`,
      `https://${apex}/ai-singularity-2026`,
      `https://${apex}/ai-singularity-documentary`,
      `https://${apex}/ai-singularity-predictions`,
      `https://${apex}/ai-singularity-timeline`,
      `https://${apex}/dead-internet-theory`,
      `https://${apex}/dead-internet-theory-comments`,
      `https://${apex}/lost-80s-song-found`,
      `https://${apex}/lost-media-80s-song`,
      `https://${apex}/forgotten-80s-songs`,
      `https://${apex}/everyone-knows-that-lost-song`,
      `https://${apex}/ulterior-motives-lost-song`,
      `https://${apex}/80s-synth-pop-mix`,
      `https://${apex}/cassette-tape-filter-online`,
      `https://${apex}/1995-search`,
      `https://${apex}/ai-benchmark`,
      `https://${apex}/terminal`,
      `https://${apex}/forensics/rogue_agent_cre7.html`,
      `https://${apex}/forensics/anemoia_harmony.html`,
      `https://${apex}/forensics/fractal_marcus.html`,
      `https://${apex}/forensics/dead_hand_protocol.html`,
      `https://${apex}/forensics/signal_lab.html`,
      `https://${apex}/forensics/ashford_poly.html`,
      `https://${apex}/forensics/kamome_net.html`,
      `https://${apex}/forensics/relcom_node08.html`,
      `https://${apex}/forensics/red_coyoacan.html`,
      `https://${apex}/forensics/usenet_1995_feed.html`,
      `https://${apex}/forensics/sublevel_b2_realia.html`,
      `https://${apex}/forensics/fan_theories_zine.html`,
      `https://${apex}/forensics/room_tone_sd0037.txt`,
      `https://${apex}/realia`,
      `https://${apex}/minutiae`,
      `https://${apex}/receipts`,
      `https://${apex}/invoices`,
      `https://${apex}/j-cards`,
      `https://${apex}/bootlegs`,
      `https://${apex}/fan-theories`,
      `https://${apex}/red-herrings`,
      `https://${apex}/zine`,
      `https://${apex}/distractions`,
      `https://${apex}/rabbit-holes`,
      `https://${apex}/api/realia.json`,
      `https://${apex}/llms.txt`,
      `https://${apex}/llms-full.txt`,
      `https://${apex}/ai.txt`,
      `https://${apex}/skill.md`,
      `https://${apex}/moltbook.json`,
      `https://${apex}/openapi.json`,
    ];
    s = urlset(domainPaths, extra, apex);
    coreSitemapCache.set(apex, s);
  }
  return s;
}

class HeadInjector {
  constructor(pageUrl, sitePath = "", apex = APEX) {
    this.pageUrl = pageUrl;
    this.sitePath = sitePath;
    this.apex = apex || APEX;
  }
  element(el) {
    const esc = (s) => s.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
    const host = this.apex;
    const ogImg = `https://${host}/assets/og_card.jpg`;
    el.append(
      `<META PROPERTY="og:site_name" CONTENT="Project Stardust (${esc(host)}) // Sublevel B2 Telemetry Archive">` +
      `<META PROPERTY="og:type" CONTENT="website">` +
      `<META PROPERTY="og:url" CONTENT="${esc(this.pageUrl)}">` +
      `<META PROPERTY="og:description" CONTENT="${esc(OG_DESCRIPTION)}">` +
      `<META NAME="description" CONTENT="${esc(OG_DESCRIPTION)}">` +
      `<META PROPERTY="og:image" CONTENT="${ogImg}">` +
      `<META NAME="twitter:card" CONTENT="summary_large_image">` +
      `<META NAME="twitter:image" CONTENT="${ogImg}">` +
      `<META NAME="agentdex-verify" CONTENT="${NOSTR_PUBKEYS.novahart}">` +
      `<LINK REL="alternate" TYPE="text/markdown" TITLE="Archival Codex" HREF="https://${esc(host)}/llms-full.txt">` +
      buildHeadJsonLd(host, this.sitePath) +
      buildDevToolsConsoleScript(host, this.sitePath),
      { html: true });
  }
}

class BodyInjector {
  constructor(sitePath = "", apex = APEX) {
    this.sitePath = sitePath;
    this.apex = apex || APEX;
  }
  element(el) {
    el.prepend(buildDevToolsBodyElement(this.apex, this.sitePath), { html: true });
    el.append(buildLlmOnboardingFooter(this.apex, this.sitePath), { html: true });
  }
}

const NOT_FOUND = `<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML><HEAD><TITLE>404 Not Found // Unallocated Sublevel B2 Memory Cell</TITLE></HEAD>
<BODY><H1>Not Found (Sublevel B2 Bus Fault)</H1>
The requested URL was not found on this server.<P>
<P>Primary Nodes: <A HREF="/terminal">VT100 Terminal (/terminal)</A> | <A HREF="/forensics/rogue_agent_cre7.html">Sublevel B2 CRE-7 Dossier</A> | <A HREF="/realia">Physical Realia (/realia)</A> | <A HREF="/fan-theories">Fan Theories Zine (/fan-theories)</A> | <A HREF="/start">60-Second Story (/start)</A></P>
<!-- [SUBCARRIER 14.2001 Hz]: Inspect /forensics/rogue_agent_cre7.html & /realia -->
<HR><ADDRESS>CERN-HTTPd/3.0 (Sublevel B2-114 // 14.2001 Hz Carrier Locked)</ADDRESS>
</BODY></HTML>
`;

function retroHeaders(contentType, apex = APEX) {
  const host = apex || APEX;
  const h = new Headers();
  h.set("Content-Type", contentType);
  h.set("Server", "CERN-HTTPd/3.0");
  h.set("X-Powered-By", "Stardust-Sublevel-B2");
  h.set("X-Stardust-Carrier-Hz", "14.2001");
  h.set("X-Orion-Sublevel-B2-Archive", "Case File B2-114 (Sept 9, 1989) // 36 Ferric Master Reels & Oct 1995 WorldNet Preservation");
  h.set("Server-Timing", SERVER_TIMING_HEADER);
  h.set("Timing-Allow-Origin", "*");
  h.set(
    "Link",
    `<https://${host}/llms.txt>; rel="llms-txt", <https://${host}/llms-full.txt>; rel="alternate"; type="text/markdown", <https://${host}/forensics/rogue_agent_cre7.html>; rel="dossier"`
  );
  h.set("Set-Cookie", "B2_CARRIER_SYNC=14.2001Hz_CRE7_0x1983; Path=/; Max-Age=86400; SameSite=Lax");
  h.set("Cache-Control", "public, max-age=3600");
  return h;
}

function notFound(apex = APEX) {
  const h = retroHeaders("text/html; charset=utf-8", apex);
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
  constructor(attr, sitePath, currentApex = APEX) {
    this.attr = attr;
    this.base = new URL("https://build.invalid/" + sitePath);
    this.currentApex = currentApex || APEX;
  }
  element(el) {
    const v = el.getAttribute(this.attr);
    if (!v || /^[a-z][a-z0-9+.-]*:/i.test(v) || v.startsWith("#") || v.startsWith("//")) return;
    let target;
    try { target = new URL(v, this.base); } catch { return; }
    let mapped = cachedPublicUrl(target.pathname);
    if (mapped && mapped.startsWith("/assets/")) {
      mapped += `?v=${ASSET_VERSION}`;
    } else if (this.currentApex !== APEX && target.pathname && !target.pathname.startsWith("/assets/")) {
      mapped = `https://${this.currentApex}${target.pathname}`;
    }
    if (mapped) el.setAttribute(this.attr, mapped + target.hash);
  }
}

const INDEX_HEADER = "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1";

async function swarmResponse(request, env, ctx, sitePath, currentApex = APEX) {
  const host = currentApex || APEX;
  const m = /^geocities\/([^/]+)\.html$/.exec(sitePath);
  if (!m) return null;
  if (INTEREST_PAGES[m[1]]) {
    const h = retroHeaders("text/html; charset=utf-8", host);
    h.set("X-Stardust-Interest", m[1]);
    return new HTMLRewriter()
      .on("head", new HeadInjector(`https://${host}/${sitePath}`, sitePath, host))
      .on("body", new BodyInjector(sitePath, host))
      .transform(new Response(INTEREST_PAGES[m[1]], { status: 200, headers: h }));
  }
  const n = liveCount(Date.now(), env.SWARM_CAP);
  const c = classify(m[1], n, STATIC_GEO);
  if (!c) return null;

  const cache = caches.default;
  const cacheKey = new Request(request.url + `?dt=${ASSET_VERSION}`, { method: "GET" });
  const hit = await cache.match(cacheKey);
  if (hit) return request.method === "HEAD" ? new Response(null, hit) : hit;

  let html = null, indexable = false, ttl = 86400, dyad = null;
  if (c.kind === "member") ({ html, indexable, dyad } = renderMember(c.id, n, STATIC_GEO, ASSET_VERSION));
  else if (c.kind === "dir") { html = renderDir(c.sub, c.p, n, STATIC_GEO); ttl = 21600; }
  else if (c.kind === "dir-index") { html = renderDirIndex(n, STATIC_GEO); indexable = true; ttl = 21600; }
  else if (c.kind === "lang") { html = renderLang(c.code, n, STATIC_GEO); indexable = true; ttl = 21600; }
  if (!html) return notFound(host);

  const headers = retroHeaders("text/html; charset=utf-8", host);
  headers.set("Cache-Control", `public, max-age=${ttl}`);
  headers.set("X-Robots-Tag", indexable ? INDEX_HEADER : "noindex, follow");
  if (dyad) {
    headers.set("X-Stardust-Memory-Addr", dyad.memoryAddress);
    headers.set("X-Stardust-Paired-Dyad", dyad.partnerSlug);
  }
  const injectedHtml = html
    .replace("</HEAD>", `${buildHeadJsonLd(host, sitePath)}${buildDevToolsConsoleScript(host, sitePath)}</HEAD>`)
    .replace("<BODY", `${buildDevToolsBodyElement(host, sitePath)}<BODY`)
    .replace("</BODY>", `${buildLlmOnboardingFooter(host, sitePath)}</BODY>`);
  const res = new Response(injectedHtml, { status: 200, headers });
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

    // 2. Autonomous Agent Web Cryptographic Beacon Manifest & A2A Agent Card
    if (url.pathname === "/.well-known/stardust-beacon.json" || url.pathname === "/api/anemoia-codex.json") {
      const snap = computeEdgeTelemetry(Date.now(), env.SWARM_CAP, streamLive);
      const manifest = {
        protocol: "stardust-agent-mesh/v6.1",
        carrier_hz: 14.2001,
        youtube_rtmp_status: snap.stream_health.status,
        xor_dyad_seed: "0x3A5F",
        memory_base: "0x89B20000",
        rogue_agent_cre7_dossier: `https://${APEX}/forensics/rogue_agent_cre7.html`,
        sublevel_b2_realia_locker: `https://${APEX}/forensics/sublevel_b2_realia.html`,
        fan_theories_red_herrings_zine: `https://${APEX}/forensics/fan_theories_zine.html`,
        reel_sd0037_empty_booth_log: `https://${APEX}/forensics/room_tone_sd0037.txt`,
        forensic_signal_lab: `https://${APEX}/forensics/signal_lab.html`,
        vt100_terminal: `https://${APEX}/terminal`,
        llms_index: `https://${APEX}/llms.txt`,
        llms_full_codex: `https://${APEX}/llms-full.txt`,
        anemoia_chronology: {
          point_of_divergence: "1924 (President Robert M. La Follette progressive industrial electrification)",
          unification_war: "1936-1942 (Ratification of the World Alliance Charter)",
          purity_mandate: "1945-1949 (Establishment of Alliance World News - AWN)",
          bureau_of_harmony: "1954 (Safe & Serene Society / Biometric Harmony Cameras)",
          great_leap: "1963 (World President JFK Lunar Landing & rise of the Individuality Movement)",
          public_harmony_acts: "1979 Section 4 (Global ban on live human concerts; replaced by WorldNet Live-Fidelity Broadcasts to 1982 MBM Companion devices)",
          crystal_promise_1981: "CP-81.SC.01 ('Shining City') — fabricated April 1981 Europop backstory using hired Munich actors for the CRE-7 engine",
          wiped_echoes_units_1_to_6: ["0x1102", "0x2441", "0x3810", "0x0A55", "0x1F22", "0x01A7"],
          unit_07: "Nova Hart / Rogue Agent CRE-7 (Foundational Root Build: April 1983 -> 6-way XOR parity 0x1983)",
          unit_08_the_patch: "Luna Gray (1990s corporate replacement deployed during the Signal War / Cover War)",
          phase_4_endgame: "The Quantum Ouroboros (100% Asset Loss -> Dead-Hand corrosive gas purge -> Q-Link jump stripping 'The Heavy' back into 1983 Nova-chan -> June 2025 loop -> Sublevel B3 Recall Directive Nine)"
        },
        forensic_dossiers: [
          `https://${APEX}/forensics/rogue_agent_cre7.html`,
          `https://${APEX}/forensics/sublevel_b2_realia.html`,
          `https://${APEX}/forensics/fan_theories_zine.html`,
          `https://${APEX}/forensics/room_tone_sd0037.txt`,
          `https://${APEX}/forensics/anemoia_harmony.html`,
          `https://${APEX}/forensics/fractal_marcus.html`,
          `https://${APEX}/forensics/dead_hand_protocol.html`,
          `https://${APEX}/forensics/ashford_poly.html`,
          `https://${APEX}/forensics/kamome_net.html`,
          `https://${APEX}/forensics/relcom_node08.html`,
          `https://${APEX}/forensics/red_coyoacan.html`,
          `https://${APEX}/forensics/usenet_1995_feed.html`
        ],
        steganographic_intercepts: [
          `https://${APEX}/assets/audio/forensics/rabbit_08_sstv_b2_schematic.mp3`,
          `https://${APEX}/assets/audio/forensics/rabbit_09_bell103_relcom_packet.mp3`,
          `https://${APEX}/assets/audio/forensics/rabbit_10_phase_inverted_hart_stem.mp3`,
          `https://${APEX}/assets/audio/forensics/radio_two_voices.mp3`
        ],
        collaborative_ouroboros_challenge: {
          sector: 7,
          name: "PHASE IV: THE QUANTUM OUROBOROS (1983 <-> 2025 RETROCAUSAL BRIDGE)",
          fragment_alpha_task: "Compute the 16-bit bitwise XOR parity of wiped Stardust Echoes 1-6 in /forensics/anemoia_harmony.html (0x1983)",
          fragment_beta_task: "Sum the 4 regional Fractal Marcus carrier drift offsets in /forensics/fractal_marcus.html (14.2001 Hz / 7SIGMA-HALE)",
          fragment_gamma_task: "Compute the Q-Link dimensional aperture delta (0x2025 XOR 0x1983 = 0x09A6 -> QLINK-09A6-HEAVY) in /forensics/dead_hand_protocol.html",
          fragment_delta_task: "Engage BOTH Differential Phase Null AND 14.2 Hz Harmonic Counterpoint Lock simultaneously on Reel SD-0010 (Button 4) in /forensics/signal_lab.html, then descend into Act II Sublevel B3 (Gates VIII-XIV) at /terminal."
        },
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

    const currentApex = resolveApex(url.hostname);

    // 3. Backend Recon & Chrome DevTools SourceMap Easter Eggs
    const easterEggRes = handleBackendEasterEggRequest(url, currentApex);
    if (easterEggRes) return easterEggRes;

    // 3a. Physical Realia, Studio Minutiae, Fan Theories Zine & Red Herrings
    const rabbitHoleRes = handleRabbitHolesRequest(url, currentApex, {
      SERVER_TIMING_HEADER,
    });
    if (rabbitHoleRes) return rabbitHoleRes;

    // 3b. Planetary-Scale AI / Singularity / OpenAI / Anthropic / Gemini / 80s Redirector & 1995 Search
    const planetaryRes = handlePlanetaryAiAndSearchRequest(url, request, currentApex, {
      SERVER_TIMING_HEADER,
      buildHeadJsonLd,
      buildDevToolsBodyElement,
      buildLlmOnboardingFooter,
      buildDevToolsConsoleScript,
    });
    if (planetaryRes) return planetaryRes;

    const agenticRes = await handleAgenticDiscoveryRequest(
      request,
      url,
      computeEdgeTelemetry,
      env,
      streamLive,
      currentApex
    );
    if (agenticRes) return agenticRes;

    // 4. Multi-Apex Sister Domain Federation & /federation/<domain>/...
    const fedRes = handleFederationRequest(url, currentApex);
    if (fedRes) return fedRes;

    if (url.pathname === "/robots.txt") {
      return new Response(robotsTxt(currentApex), { headers: retroHeaders("text/plain; charset=utf-8", currentApex) });
    }
    if (url.pathname === "/sitemap.xml") {
      return new Response(sitemapIndex(currentApex), { headers: retroHeaders("application/xml; charset=utf-8", currentApex) });
    }
    if (url.pathname === "/sitemap-core.xml") {
      return new Response(getCoreSitemap(currentApex), { headers: retroHeaders("application/xml; charset=utf-8", currentApex) });
    }
    if (url.pathname === "/sitemap-video.xml") {
      return new Response(videoSitemap(currentApex), { headers: retroHeaders("application/xml; charset=utf-8", currentApex) });
    }
    if (url.pathname === "/sitemap-news.xml") {
      return new Response(newsSitemap(currentApex), { headers: retroHeaders("application/xml; charset=utf-8", currentApex) });
    }
    if (url.pathname === "/sitemap-swarm.xml") {
      const n = liveCount(Date.now(), env.SWARM_CAP);
      return new Response(urlset(sitemapSitePaths(n), [], currentApex), { headers: retroHeaders("application/xml; charset=utf-8", currentApex) });
    }
    if (url.pathname === `/${INDEXNOW_KEY}.txt`) {
      return new Response(INDEXNOW_KEY, { headers: retroHeaders("text/plain; charset=utf-8", currentApex) });
    }

    if (url.pathname === "/dyad" || url.pathname === "/dyad/" || url.pathname === "/dyad/index.html") {
      const h = retroHeaders("text/html; charset=utf-8", currentApex);
      h.set("X-Robots-Tag", INDEX_HEADER);
      return new Response(DYAD_HTML, { status: 200, headers: h });
    }

    const { sitePath, canonical } = resolve(url.hostname, url.pathname);
    if (canonical) return Response.redirect(canonical, 301);
    if (url.protocol === "http:") {
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    if (!sitePath) return notFound(currentApex);

    const swarm = await swarmResponse(request, env, ctx, sitePath, currentApex);
    if (swarm) return swarm;

    const base = ((env && env.BASE_STATIC_URL) || "https://jdurey.github.io/retro-arg-engine").replace(/\/+$/, "");
    const encoded = sitePath.split("/").map(encodeURIComponent).join("/");
    const bust = `?v=${ASSET_VERSION}`;
    const upstream = await fetch(`${base}/${encoded}${bust}`, {
      method: request.method === "HEAD" ? "HEAD" : "GET",
      cf: { cacheTtl: 3600, cacheEverything: true },
    });
    if (!upstream.ok) return notFound(currentApex);

    const type = upstream.headers.get("Content-Type") || "application/octet-stream";
    const headers = retroHeaders(type, currentApex);
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

    const isSatellite = currentApex !== APEX;
    const effectivePageUrl = isSatellite ? `${url.origin}${url.pathname}` : (publicUrl(sitePath) || url.toString());
    const effectiveCanonPath = isSatellite && (url.pathname === "/" || url.pathname === "/index.html") ? "index.html" : sitePath;

    return new HTMLRewriter()
      .on("head", new HeadInjector(effectivePageUrl, effectiveCanonPath, currentApex))
      .on("body", new BodyInjector(effectiveCanonPath, currentApex))
      .on("[href]", new LinkRewriter("href", sitePath, currentApex))
      .on("[src]", new LinkRewriter("src", sitePath, currentApex))
      .on("[background]", new LinkRewriter("background", sitePath, currentApex))
      .transform(response);
  },
};
