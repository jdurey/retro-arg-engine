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
  "index.html",
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
  "regional/03-germany/index.html",
  "regional/05-france/index.html",
  "regional/06-italy/index.html",
  "regional/09-korea/index.html",
  "regional/10-india/index.html",
  "regional/11-sweden/index.html",
  "regional/12-fiji/index.html",
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

  const state = fs.existsSync(STATE_FILE) ? JSON.parse(fs.readFileSync(STATE_FILE, "utf8")) : { archived: {} };
  console.log(`Starting Wayback Machine submission for ${Math.min(limit, CORE_PATHS.length)} priority nodes...`);

  let count = 0;
  for (const sp of CORE_PATHS) {
    if (count >= limit) break;
    const targetUrl = sp === "index.html" ? `https://${APEX}/` : publicUrl(sp);
    if (!targetUrl) continue;

    if (state.archived[targetUrl]) {
      console.log(`[ALREADY ARCHIVED] ${sp} -> ${state.archived[targetUrl]}`);
      continue;
    }

    console.log(`\nArchiving: ${sp}`);
    console.log(`  Target: ${targetUrl}`);

    let retries = 0;
    while (retries < 3) {
      try {
        const saveEndpoint = `https://web.archive.org/save/${targetUrl}`;
        const res = await fetch(saveEndpoint, {
          method: "GET",
          headers: { "User-Agent": "Mozilla/5.0 (compatible; StardustArchiver/1.0)" },
          redirect: "manual",
        });

        const loc = res.headers.get("location");
        if (res.status === 302 && loc) {
          state.archived[targetUrl] = loc;
          console.log(`  [✓] Successfully archived! Snapshot: ${loc}`);
          break;
        } else if (res.status === 200) {
          state.archived[targetUrl] = `https://web.archive.org/web/${targetUrl}`;
          console.log(`  [✓] Archived (200 OK)`);
          break;
        } else if (res.status === 429) {
          console.log(`  [!] Rate limited (429). Backing off 15s before retry...`);
          retries++;
          await sleep(15000);
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

    // Polite rate limit for Internet Archive (8 seconds)
    if (count < limit) {
      console.log("  Waiting 8s before next snapshot...");
      await sleep(8000);
    }
  }

  console.log(`\nDone. Total pages in Wayback archive state: ${Object.keys(state.archived).length}`);
}

main().catch(console.error);
