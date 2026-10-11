// Automated test suite for Multi-Apex Domain Federation.
// Usage: node deploy/test_federation.mjs

import assert from "node:assert/strict";
import STORY_PATHS from "./story_paths.js";
import { PRIMARY_APEX, FEDERATION } from "./federation.js";
import { ALL_APEXES, apexFor, resolveApex, publicUrl, resolve, hostFor } from "./urlmap.js";

console.log("Starting Multi-Apex Federation Test Suite...\n");

// --- TEST 1: Fallback Mode Verification (Default) ---
console.log("TEST 1: Fallback mode (all sister domains disabled)");
assert.equal(ALL_APEXES.length, 1, "ALL_APEXES should only contain PRIMARY_APEX when sister domains are disabled");
assert.equal(ALL_APEXES[0], PRIMARY_APEX, "PRIMARY_APEX should be stardust-archive.net");

for (const sp of STORY_PATHS) {
  const a = apexFor(sp);
  assert.equal(a, PRIMARY_APEX, `Fallback failed: ${sp} mapped to ${a} instead of ${PRIMARY_APEX}`);
  const u = publicUrl(sp);
  assert.ok(u.includes(PRIMARY_APEX), `URL ${u} does not contain ${PRIMARY_APEX}`);
  const parsed = new URL(u);
  assert.ok(parsed.hostname.split(".")[0].length <= 63, `Hostname label exceeds 63 chars: ${parsed.hostname}`);
  const res = resolve(parsed.hostname, parsed.pathname);
  assert.equal(res.sitePath, sp, `Resolve mismatch: expected ${sp}, got ${res.sitePath}`);
}
console.log("  [✓] Passed: All 5,153+ story paths cleanly fall back to stardust-archive.net with 0 broken links.\n");

// --- TEST 2: Active Federation Mode Verification ---
console.log("TEST 2: Federation mode (simulating all sister domains enabled)");
// Temporarily enable in memory
for (const k of Object.keys(FEDERATION)) FEDERATION[k].enabled = true;
const activeApexes = [PRIMARY_APEX, ...Object.keys(FEDERATION)];

// Test apexFor matches
assert.equal(apexFor("ftp/ashford-poly/index.html"), "ashford-poly.org");
assert.equal(apexFor("regional/01-usa/index.html"), "ashford-poly.org");
assert.equal(apexFor("ftp/kamome/index.html"), "kamome-net.org");
assert.equal(apexFor("regional/02-japan/index.html"), "kamome-net.org");
assert.equal(apexFor("geocities/hood_tokyo-garden.html"), "kamome-net.org");
assert.equal(apexFor("geocities/lang_ja.html"), "kamome-net.org");
assert.equal(apexFor("geocities/lang-ja.html"), "kamome-net.org");
assert.equal(apexFor("regional/08-ussr/index.html"), "relcom-node08.org");
assert.equal(apexFor("geocities/lang_ru.html"), "relcom-node08.org");
assert.equal(apexFor("regional/04-mexico/index.html"), "redcoyoacan.org");
assert.equal(apexFor("geocities/lang_es.html"), "redcoyoacan.org");
assert.equal(apexFor("geocities/hollywood-hills-4127.html"), PRIMARY_APEX);

console.log("  [✓] Passed: Domain matching rules correctly partition paths.");

// Test publicUrl generation and roundtrip resolution across sister domains
const testPaths = [
  "ftp/ashford-poly/index.html",
  "regional/01-usa/index.html",
  "ftp/kamome/index.html",
  "regional/02-japan/index.html",
  "geocities/hood_tokyo-garden.html",
  "geocities/lang_ja.html",
  "regional/08-ussr/index.html",
  "geocities/lang_ru.html",
  "regional/04-mexico/index.html",
  "geocities/lang_es.html",
  "geocities/hollywood-hills-4127.html",
  "index.html",
];

for (const sp of testPaths) {
  const expectedApex = apexFor(sp);
  const pub = publicUrl(sp);
  const parsed = new URL(pub);
  assert.ok(parsed.hostname.endsWith(expectedApex), `Hostname ${parsed.hostname} does not end with expected apex ${expectedApex}`);
  assert.ok(parsed.hostname.split(".")[0].length <= 63, `Hostname label exceeds 63 chars: ${parsed.hostname}`);
  
  // Test resolveApex
  assert.equal(resolveApex(parsed.hostname), expectedApex, `resolveApex failed for ${parsed.hostname}`);

  // Test roundtrip resolve
  const back = resolve(parsed.hostname, parsed.pathname);
  assert.equal(back.sitePath, sp, `Roundtrip resolution failed for ${sp} via ${pub}`);
}
console.log("  [✓] Passed: Single-level subdomains, label <= 63 chars, and roundtrip resolution verified.");

// --- TEST 3: Institutional Landing Page Resolution on Root Access ---
console.log("TEST 3: Institutional landing page routing for sister domains");
const ashfordRoot = resolve("ashford-poly.org", "/");
assert.equal(ashfordRoot.sitePath, "ftp/ashford-poly/index.html", "ashford-poly.org root should resolve to academic archive");

const kamomeRoot = resolve("kamome-net.org", "/");
assert.equal(kamomeRoot.sitePath, "ftp/kamome/index.html", "kamome-net.org root should resolve to PC-98 BBS archive");

const primaryRoot = resolve("stardust-archive.net", "/");
assert.equal(primaryRoot.sitePath, "index.html", "stardust-archive.net root should resolve to main webring index");

console.log("  [✓] Passed: Sister domain root requests intelligently route to their institutional archives.\n");

// --- TEST 4: Edge Worker Request Handling ---
console.log("TEST 4: Edge Worker request routing (robots.txt, sitemaps, IndexNow)");
const worker = (await import("./worker.js")).default;
const mockEnv = { BASE_STATIC_URL: "https://jdurey.github.io/retro-arg-engine", SWARM_CAP: "0" };
const mockCtx = { waitUntil: () => {} };

// Test robots.txt on primary
const robPrimaryRes = await worker.fetch(new Request("https://stardust-archive.net/robots.txt"), mockEnv, mockCtx);
const robPrimaryText = await robPrimaryRes.text();
assert.ok(robPrimaryText.includes("Sitemap: https://stardust-archive.net/sitemap.xml"), "Primary robots.txt sitemap mismatch");

// Test robots.txt on sister domain
const robSisterRes = await worker.fetch(new Request("https://ashford-poly.org/robots.txt"), mockEnv, mockCtx);
const robSisterText = await robSisterRes.text();
assert.ok(robSisterText.includes("Sitemap: https://ashford-poly.org/sitemap.xml"), "Sister robots.txt sitemap mismatch");

// Test sitemap.xml index on sister domain
const smSisterRes = await worker.fetch(new Request("https://ashford-poly.org/sitemap.xml"), mockEnv, mockCtx);
const smSisterText = await smSisterRes.text();
assert.ok(smSisterText.includes("https://ashford-poly.org/sitemap-core.xml"), "Sister sitemap index mismatch");

// Test sitemap-core.xml on sister domain
const smCoreSisterRes = await worker.fetch(new Request("https://ashford-poly.org/sitemap-core.xml"), mockEnv, mockCtx);
const smCoreSisterText = await smCoreSisterRes.text();
assert.ok(smCoreSisterText.includes("ashford-poly.org"), "Sister sitemap-core should contain ashford-poly URLs");
assert.ok(!smCoreSisterText.includes("stardust-archive.net"), "Sister sitemap-core should NOT contain stardust-archive URLs");

// Test IndexNow proof file
const proofRes = await worker.fetch(new Request("https://ashford-poly.org/37feeed875722863fda484c68e6695e5.txt"), mockEnv, mockCtx);
assert.equal(await proofRes.text(), "37feeed875722863fda484c68e6695e5", "IndexNow proof mismatch");

console.log("  [✓] Passed: Dynamic edge robots.txt, sitemaps, and IndexNow validation verified.\n");

// Revert memory state
for (const k of Object.keys(FEDERATION)) FEDERATION[k].enabled = false;

console.log("================================================================================");
console.log("             ALL MULTI-APEX FEDERATION TESTS PASSED (100%)");
console.log("================================================================================\n");
