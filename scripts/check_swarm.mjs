// CI gate for the generated swarm. Renders every Tier-2 page, every suburb
// directory's first page, all hubs and a random sample of members, then checks:
// canon (no Sloan), unfilled slots / JS leakage, every link resolves to a real
// page, DNS label length, address bijection, and render time.
//
// Usage: node scripts/check_swarm.mjs [site_dir]   (site_dir enables static-link existence checks)
import fs from "node:fs";
import path from "node:path";
import STORY_PATHS from "../deploy/story_paths.js";
import TIER2 from "../deploy/swarm/tier2.js";
import BANK from "../deploy/swarm/bank.js";
import { resolve } from "../deploy/urlmap.js";
import { DOMAIN, SUBURBS, addressOf, idOf } from "../deploy/swarm/address.js";
import { N_MAX, classify, renderMember, renderDir, renderDirIndex, renderLang } from "../deploy/swarm/index.js";
import { rngFor } from "../deploy/swarm/rng.js";

const siteDir = process.argv[2];
const errors = [];
const err = (m) => { if (errors.length < 200) errors.push(m); };
const STATIC = new Set(STORY_PATHS.filter((p) => /^geocities\/[^/]+\.html$/.test(p)).map((p) => p.slice(10, -5)));
const N = N_MAX;

// 1. address bijection over the whole domain
for (let id = 0; id < DOMAIN; id++) if (idOf(addressOf(id).slug) !== id) { err(`address roundtrip failed for id ${id}`); break; }

// 2. tier2 sanity
const t2 = new Set(TIER2);
if (t2.size !== TIER2.length) err("tier2 has duplicate ids");
for (const id of TIER2) {
  if (id < 0 || id >= N) err(`tier2 id ${id} out of range`);
  else if (STATIC.has(addressOf(id).slug)) err(`tier2 id ${id} is shadowed by a static page`);
}

// 3. render + inspect
const linkOk = new Map();
function checkLink(u, where) {
  if (linkOk.has(u)) { if (!linkOk.get(u)) err(`${where}: dead link ${u}`); return; }
  let ok = true;
  if (u.startsWith("/assets/")) {
    ok = !siteDir || fs.existsSync(path.join(siteDir, u.split("?")[0]));
  } else if (u.startsWith("https://")) {
    const x = new URL(u);
    const label = x.hostname.split(".")[0];
    if (label.length > 63) { err(`${where}: DNS label too long ${x.hostname}`); ok = false; }
    const { sitePath, canonical } = resolve(x.hostname, x.pathname);
    if (!sitePath || canonical) ok = false;
    else {
      const m = /^geocities\/([^/]+)\.html$/.exec(sitePath);
      if (m && !STATIC.has(m[1]) && !["member", "dir", "dir-index", "lang"].includes((classify(m[1], N, STATIC) || {}).kind)) ok = false;
      else if (!m && siteDir && sitePath !== "index.html" && !fs.existsSync(path.join(siteDir, sitePath))) ok = false;
    }
  } else if (!u.startsWith("mailto:") && !u.startsWith("#")) ok = false;
  linkOk.set(u, ok);
  if (!ok) err(`${where}: dead link ${u}`);
}

function inspect(html, where) {
  if (/sloan/i.test(html)) err(`${where}: forbidden name`);
  const slot = html.match(/\{[a-z_]{2,}\}/);
  if (slot) err(`${where}: unfilled slot ${slot[0]}`);
  const leak = html.match(/undefined|NaN|\[object Object\]|null<|>null/);
  if (leak) err(`${where}: JS leakage '${leak[0]}'`);
  for (const m of html.matchAll(/(?:HREF|SRC|href|src)="([^"]+)"/g)) checkLink(m[1].replace(/&amp;/g, "&"), where);
}

const times = [];
const sample = rngFor("check-swarm");
const ids = new Set(TIER2);
while (ids.size < TIER2.length + 3000) ids.add(sample.int(0, N - 1));
for (const id of ids) {
  if (STATIC.has(addressOf(id).slug)) continue;
  const t = performance.now();
  const { html } = renderMember(id, N, STATIC, "test");
  times.push(performance.now() - t);
  inspect(html, `member ${id}`);
}
for (let s = 0; s < SUBURBS.length; s++) {
  const html = renderDir(s, 1, N, STATIC);
  if (!html) err(`suburb ${s} has no directory page`);
  else inspect(html, `dir ${s}`);
}
inspect(renderDirIndex(N, STATIC), "dir-index");
for (const code of Object.keys(BANK.langs)) inspect(renderLang(code, N, STATIC), `lang ${code}`);

times.sort((a, b) => a - b);
const p99 = times[Math.floor(times.length * 0.99)];
if (p99 > 5) err(`member render p99 ${p99.toFixed(2)} ms exceeds 5 ms budget`);
console.error(`checked ${times.length} members, ${SUBURBS.length} directories, ${Object.keys(BANK.langs).length} hubs, ${linkOk.size} distinct links; render p50 ${times[times.length >> 1].toFixed(2)} ms, p99 ${p99.toFixed(2)} ms`);
if (errors.length) {
  console.error(`${errors.length} swarm errors:\n  ` + errors.slice(0, 40).join("\n  "));
  process.exit(1);
}
console.error("swarm OK");
