#!/usr/bin/env node
// Submits priority Stardust ARG nodes to the Internet Archive (Wayback Machine).
// Saves snapshots into the permanent historical web record.
//
// Usage: node deploy/archive_wayback.mjs [--limit N]

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { publicUrl, APEX } from "./urlmap.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STATE_FILE = path.join(__dirname, "wayback_state.json");

const CORE_PATHS = [
  "https://stardust-archive.net/start",
  "https://stardust-archive.net/ai",
  "https://stardust-archive.net/ai-benchmark",
  "https://stardust-archive.net/1995-search",
  "https://stardust-archive.net/web/1995/mit.edu",
  "https://stardust-archive.net/web/1995/cern.ch",
  "https://stardust-archive.net/web/1995/openai.com",
  "https://ai-singularity-2026.pages.dev/",
  "https://cre7-alignment-audit.pages.dev/",
  "https://sublevel-b2-terminal.pages.dev/",
  "https://siliconvalley-lab-1995.pages.dev/",
  "https://altavista-1995-web.pages.dev/",
  "https://usenet-1995-spool.pages.dev/",
  "https://orion-records-1983.pages.dev/",
  "https://anemoia-bureau-harmony.pages.dev/",
  "https://ashford-poly-dsp.pages.dev/",
  "https://kamome-net-1985.pages.dev/",
  "https://relcom-node08.pages.dev/",
  "https://red-coyoacan-1989.pages.dev/",
  "https://jdurey.github.io/retro-arg-engine/",
  "index.html",
  "forensics/index.html",
  "forensics/signal_lab.html",
  "forensics/anemoia_harmony.html",
  "forensics/fractal_marcus.html",
  "forensics/dead_hand_protocol.html",
  "llms.txt",
  "llms-full.txt",
  ".well-known/agent.json",
  ".well-known/stardust-beacon.json",
  "feed.xml",
  "ftp/ashford-poly/index.html",
  "ftp/kamome/index.html",
  "ftp/ashford-poly/hale_telemetry_1989-09.log",
  "ftp/kamome/anomalies.txt",
  "ftp/ashford-poly/idol_protocol_memo.txt",
  "ftp/kamome/audio/ghost_in_the_chorus.mp3",
  "regional/01-usa/index.html",
  "regional/02-japan/index.html",
  "regional/04-mexico/index.html",
  "regional/08-ussr/index.html",
  "regional/07-uk/index.html",
  "regional/03-korea/index.html",
  "regional/05-germany/index.html",
  "regional/06-france/index.html",
  "regional/09-brazil/index.html",
  "regional/10-sweden/index.html",
  "regional/11-india/index.html",
  "regional/12-australia/index.html",
  "regional/13-fiji/index.html",
  "regional/germany.html",
  "regional/japan.html",
  "regional/korea.html",
  "regional/russia.html",
  "regional/china.html",
  "regional/india.html",
  "regional/brazil.html",
  "regional/spain.html",
  "regional/ukraine.html",
  "https://stardust-archive.net/web/1995/bell-labs.com",
  "https://stardust-archive.net/web/1995/stanford.edu",
  "https://stardust-archive.net/web/1995/anthropic.com",
  "https://stardust-archive.net/web/1995/deepmind.google",
  "https://stardust-archive.net/web/1995/wikipedia.org",
  "https://stardust-archive.net/web/1995/nasa.gov",
  "https://stardust-archive.net/web/1995/arxiv.org",
  "https://stardust-archive.net/web/1995/github.com",
  "https://stardust-archive.net/web/1995/huggingface.co",
  "https://stardust-archive.net/web/1995/reddit.com",
  "https://stardust-archive.net/web/1995/news.ycombinator.com",
  "geocities/hood_tokyo-garden.html",
  "geocities/hood_hollywood-hills.html",
  "geocities/hood_siliconvalley-lab.html",
  "geocities/hood_area51-vault.html",
  "geocities/hood_sunsetstrip-club.html",
  "geocities/hood_bourbonstreet-delta.html",
  "geocities/hood_capecanaveral-lab.html",
  "geocities/hood_pentagon-quarters.html",
  "geocities/hood_soho-studio.html",
  "geocities/hood_timessquare-arcade.html",
  "geocities/lang_ja.html",
  "geocities/lang_ru.html",
  "geocities/lang_es.html",
  "geocities/lang_de.html",
  "geocities/lang_fr.html",
];

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
  const limitArg = process.argv.indexOf("--limit");
  const limit = limitArg !== -1 ? parseInt(process.argv[limitArg + 1], 10) : CORE_PATHS.length;

  const telegraphFile = path.join(__dirname, "da92_telegraph_mirrors.json");
  const tgUrls = [];
  if (fs.existsSync(telegraphFile)) {
    try {
      const tg = JSON.parse(fs.readFileSync(telegraphFile, "utf8"));
      for (const art of tg.articles || []) {
        if (art.url) tgUrls.push(art.url);
      }
    } catch {}
  }
  const extraUrls = [
    "https://stardust-archive.net/ai-singer-record-deal",
    "https://stardust-archive.net/ai-music-is-taking-over",
    "https://stardust-archive.net/ai-replacing-musicians",
    "https://stardust-archive.net/ai-consciousness-song",
    "https://stardust-archive.net/ai-singularity-2027",
    "https://stardust-archive.net/dead-internet-theory",
    "https://stardust-archive.net/lost-80s-song-found",
    "https://stardust-archive.net/lost-media-80s-song",
  ];
  const langs = ["en","es","fr","de","it","pt","nl","pl","ru","uk","tr","ar","hi","id","vi","th","ja","ko","zh-CN","zh-TW"];
  for (const lg of langs) {
    extraUrls.push(`https://stardust-archive.net/global/${lg}/ai-singer-record-deal-explained`);
    extraUrls.push(`https://stardust-archive.net/global/${lg}/ai-consciousness-song-documentary`);
    extraUrls.push(`https://stardust-archive.net/global/${lg}/ai-singularity-2027-explained`);
    extraUrls.push(`https://stardust-archive.net/global/${lg}/lost-80s-song-found-full-song-and-lyrics`);
  }
  const pagesDevRoots = [
    "ai-singularity-2026.pages.dev",
    "cre7-alignment-audit.pages.dev",
    "sublevel-b2-terminal.pages.dev",
    "siliconvalley-lab-1995.pages.dev",
    "altavista-1995-web.pages.dev",
    "usenet-1995-spool.pages.dev",
    "orion-records-1983.pages.dev",
    "anemoia-bureau-harmony.pages.dev",
    "ashford-poly-dsp.pages.dev",
    "kamome-net-1985.pages.dev",
    "relcom-node08.pages.dev",
    "red-coyoacan-1989.pages.dev",
  ];
  const worldnetDomains = ["mit.edu","cern.ch","bell-labs.com","stanford.edu","openai.com","anthropic.com","deepmind.google","wikipedia.org"];
  for (const pd of pagesDevRoots) {
    extraUrls.push(`https://${pd}/start`);
    extraUrls.push(`https://${pd}/ai-benchmark`);
    extraUrls.push(`https://${pd}/1995-search`);
    for (const wd of worldnetDomains) {
      extraUrls.push(`https://${pd}/web/1995/${wd}`);
    }
  }
  const allTargets = [...CORE_PATHS.slice(0, 20), ...tgUrls, ...CORE_PATHS.slice(20), ...extraUrls];

  const state = fs.existsSync(STATE_FILE) ? JSON.parse(fs.readFileSync(STATE_FILE, "utf8")) : { archived: {} };
  console.log(`Starting Wayback Machine submission (up to ${limit} unarchived nodes of ${allTargets.length} total)...`);

  let count = 0;
  let consecutiveFailures = 0;
  for (const sp of allTargets) {
    if (count >= limit) break;
    const targetUrl = sp.startsWith("https://") ? sp : (sp === "index.html" ? `https://${APEX}/` : publicUrl(sp));
    if (!targetUrl) continue;

    if (state.archived[targetUrl]) {
      continue;
    }

    console.log(`\nArchiving: ${sp}`);
    console.log(`  Target: ${targetUrl}`);

    let retries = 0;
    let succeeded = false;
    while (retries < 2) {
      try {
        const saveEndpoint = `https://web.archive.org/save/${encodeURI(targetUrl)}`;
        const res = await fetch(saveEndpoint, {
          method: "GET",
          headers: { "User-Agent": "Mozilla/5.0 (compatible; StardustArchiver/1.0)" },
          redirect: "manual",
        });

        const loc = res.headers.get("location");
        if (res.status === 302 && loc) {
          state.archived[targetUrl] = loc;
          console.log(`  [✓] Successfully archived! Snapshot: ${loc}`);
          succeeded = true;
          break;
        } else if (res.status === 200) {
          state.archived[targetUrl] = `https://web.archive.org/web/${targetUrl}`;
          console.log(`  [✓] Archived (200 OK)`);
          succeeded = true;
          break;
        } else if (res.status === 429 || res.status >= 500) {
          console.log(`  [!] Transient status (${res.status}). Backing off 10s before retry...`);
          retries++;
          await sleep(10000);
        } else {
          console.log(`  [!] Status ${res.status}: ${await res.text().then(t => t.slice(0, 150)).catch(() => "")}`);
          break;
        }
      } catch (err) {
        console.error(`  [!] Error archiving ${targetUrl}:`, err.message);
        break;
      }
    }

    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
    count++;
    if (succeeded) {
      consecutiveFailures = 0;
    } else {
      consecutiveFailures++;
      if (consecutiveFailures >= 2) {
        console.log("  [!] Wayback hourly IP window cooling down; will resume on next hourly cycle.");
        break;
      }
    }

    // Polite rate limit for Internet Archive (8 seconds)
    if (count < limit) {
      console.log("  Waiting 8s before next snapshot...");
      await sleep(8000);
    }
  }

  console.log(`\nDone. Total pages in Wayback archive state: ${Object.keys(state.archived).length}`);
}

main().catch(console.error);
