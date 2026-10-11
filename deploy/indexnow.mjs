// Submits NEW indexable URLs to IndexNow (Bing, Yandex, Naver, Seznam, Yep).
// The indexable set = static story pages + the swarm's live Tier-2 pages and hubs,
// which grows weekly as the rollout advances. URLs already accepted are recorded
// in deploy/indexnow_state.json (committed) and never resubmitted.
//
// Usage: node deploy/indexnow.mjs [--all] [--dry-run]
import fs from "node:fs";
import STORY from "./story_paths.js";
import { publicUrl, APEX } from "./urlmap.js";
import { liveCount, sitemapSitePaths } from "./swarm/index.js";

const KEY = "37feeed875722863fda484c68e6695e5";
const STATE = new URL("./indexnow_state.json", import.meta.url);
const BATCH_SIZE = 10000; // IndexNow maximum per request
const dryRun = process.argv.includes("--dry-run");

const n = liveCount(Date.now(), process.env.SWARM_CAP);
const allUrls = [...new Set([...STORY, ...sitemapSitePaths(n)].map((sp) => publicUrl(sp)).filter((u) => u && u.startsWith("https://")))];
const state = fs.existsSync(STATE) && !process.argv.includes("--all") ? JSON.parse(fs.readFileSync(STATE, "utf8")) : { submitted: [] };
const done = new Set(state.submitted);
const fresh = allUrls.filter((u) => !done.has(u));

console.log(`swarm live: ${n}; indexable URLs: ${allUrls.length}; new since last run: ${fresh.length}${dryRun ? " (dry run)" : ""}`);

let accepted = 0;
for (let i = 0; i < fresh.length && !dryRun; i += BATCH_SIZE) {
  const chunk = fresh.slice(i, i + BATCH_SIZE);
  const res = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({ host: APEX, key: KEY, keyLocation: `https://${APEX}/${KEY}.txt`, urlList: chunk }),
  });
  if (res.status === 200 || res.status === 202) {
    accepted += chunk.length;
    chunk.forEach((u) => done.add(u));
    console.log(`  batch ${i + 1}..${i + chunk.length}: accepted (${res.status})`);
  } else {
    console.error(`  batch ${i + 1}..${i + chunk.length}: error ${res.status} ${await res.text()}`);
    process.exitCode = 1;
  }
}
if (!dryRun) {
  fs.writeFileSync(STATE, JSON.stringify({ updated: new Date().toISOString(), submitted: [...done].sort() }, null, 0) + "\n");
  console.log(`IndexNow: ${accepted}/${fresh.length} new URLs accepted.`);
}
