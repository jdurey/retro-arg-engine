// Submits NEW indexable URLs to IndexNow (Bing, Yandex, Naver, Seznam, Yep).
// The indexable set = static story pages + the swarm's live Tier-2 pages and hubs,
// which grows weekly as the rollout advances. URLs already accepted are recorded
// in deploy/indexnow_state.json (committed) and never resubmitted.
//
// Usage: node deploy/indexnow.mjs [--all] [--dry-run]
import fs from "node:fs";
import STORY from "./story_paths.js";
import { publicUrl, APEX, resolveApex } from "./urlmap.js";
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

// Group URLs by apex domain
const byApex = new Map();
for (const u of fresh) {
  const host = new URL(u).hostname;
  const apex = resolveApex(host);
  if (!byApex.has(apex)) byApex.set(apex, []);
  byApex.get(apex).push(u);
}

let accepted = 0;
for (const [apex, urls] of byApex) {
  console.log(`Submitting ${urls.length} URLs for apex: ${apex}...`);
  for (let i = 0; i < urls.length && !dryRun; i += BATCH_SIZE) {
    const chunk = urls.slice(i, i + BATCH_SIZE);
    const res = await fetch("https://api.indexnow.org/indexnow", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({ host: apex, key: KEY, keyLocation: `https://${apex}/${KEY}.txt`, urlList: chunk }),
    });
    if (res.status === 200 || res.status === 202) {
      accepted += chunk.length;
      chunk.forEach((u) => done.add(u));
      console.log(`  [${apex}] batch ${i + 1}..${i + chunk.length}: accepted (${res.status})`);
    } else {
      console.error(`  [${apex}] batch ${i + 1}..${i + chunk.length}: error ${res.status} ${await res.text()}`);
      process.exitCode = 1;
    }
  }
}
if (!dryRun) {
  fs.writeFileSync(STATE, JSON.stringify({ updated: new Date().toISOString(), submitted: [...done].sort() }, null, 0) + "\n");
  console.log(`IndexNow: ${accepted}/${fresh.length} new URLs accepted across all apexes.`);
}
