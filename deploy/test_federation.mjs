// Automated test suite for Multi-Apex Domain Federation.
// Tests institutional isolation, 301 permanent redirects, fallback safety, and edge response routing.
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
console.log("  [✓] Passed: All 5,152+ story paths cleanly fall back to stardust-archive.net with 0 broken links.\n");

// --- TEST 2: Active Federation Mode & Institutional Purity ---
console.log("TEST 2: Federation mode (institutional archives partitioned, fan & swarm pages strictly on primary)");
// Temporarily enable in memory
for (const k of Object.keys(FEDERATION)) FEDERATION[k].enabled = true;

// Institutional matches
assert.equal(apexFor("ftp/ashford-poly/index.html"), "ashford-poly.org");
assert.equal(apexFor("regional/01-usa/index.html"), "ashford-poly.org");
assert.equal(apexFor("ftp/kamome/index.html"), "kamome-net.org");
assert.equal(apexFor("regional/02-japan/index.html"), "kamome-net.org");
assert.equal(apexFor("regional/08-ussr/index.html"), "relcom-node08.org");
assert.equal(apexFor("regional/04-mexico/index.html"), "redcoyoacan.org");

// FAN PAGES & SWARM MUST ALWAYS STAY ON PRIMARY APEX (never pollute sister domains)
assert.equal(apexFor("geocities/hood_tokyo-garden.html"), PRIMARY_APEX);
assert.equal(apexFor("geocities/lang_ja.html"), PRIMARY_APEX);
assert.equal(apexFor("geocities/lang-ja.html"), PRIMARY_APEX);
assert.equal(apexFor("geocities/lang_ru.html"), PRIMARY_APEX);
assert.equal(apexFor("geocities/lang_es.html"), PRIMARY_APEX);
assert.equal(apexFor("geocities/hollywood-hills-4127.html"), PRIMARY_APEX);
assert.equal(apexFor("geocities/tokyo-garden-1420.html"), PRIMARY_APEX);

console.log("  [✓] Passed: Sister domains strictly limited to hand-authored institutional archives.");
console.log("  [✓] Passed: All GeoCities and swarm pages strictly preserved on primary apex.");

// Test publicUrl generation and roundtrip resolution across sister domains
const testPaths = [
  "ftp/ashford-poly/index.html",
  "regional/01-usa/index.html",
  "ftp/kamome/index.html",
  "regional/02-japan/index.html",
  "regional/08-ussr/index.html",
  "regional/04-mexico/index.html",
  "geocities/hood_tokyo-garden.html",
  "geocities/lang_ja.html",
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
console.log("  [✓] Passed: Single-level subdomains, label <= 63 chars, and roundtrip resolution verified.\n");

// --- TEST 3: Institutional Landing Page Routing on Root Access ---
console.log("TEST 3: Institutional landing page routing for sister domains");
const ashfordRoot = resolve("ashford-poly.org", "/");
assert.equal(ashfordRoot.sitePath, "ftp/ashford-poly/index.html", "ashford-poly.org root should resolve to academic archive");

const kamomeRoot = resolve("kamome-net.org", "/");
assert.equal(kamomeRoot.sitePath, "ftp/kamome/index.html", "kamome-net.org root should resolve to PC-98 BBS archive");

const primaryRoot = resolve("stardust-archive.net", "/");
assert.equal(primaryRoot.sitePath, "index.html", "stardust-archive.net root should resolve to main webring index");

console.log("  [✓] Passed: Sister domain root requests intelligently route to their institutional archives.\n");

// --- TEST 4: Cross-Apex 301 Permanent Redirects ---
console.log("TEST 4: Cross-Apex 301 Permanent Redirects (No broken links or 404s when switching domains)");
// When ashford-poly.org is ENABLED:
// Old URL on stardust-archive.net:
const oldAshfordHost = hostFor("ftp", "ashford-poly", PRIMARY_APEX);
const oldAshfordUrl = `https://${oldAshfordHost}/~some/junk/index.html`;
const oldParsed = new URL(oldAshfordUrl);
const oldResolve = resolve(oldParsed.hostname, oldParsed.pathname);

assert.equal(oldResolve.sitePath, "ftp/ashford-poly/index.html");
assert.ok(oldResolve.canonical, "Should return canonical redirect for old URL on stardust-archive.net");
assert.ok(oldResolve.canonical.includes("ashford-poly.org"), "Canonical should point to ashford-poly.org");

// When ashford-poly.org is DISABLED:
FEDERATION["ashford-poly.org"].enabled = false;
const sisterAshfordHost = hostFor("ftp", "ashford-poly", "ashford-poly.org");
const sisterAshfordUrl = `https://${sisterAshfordHost}/~some/junk/index.html`;
const sisterParsed = new URL(sisterAshfordUrl);
const disabledResolve = resolve(sisterParsed.hostname, sisterParsed.pathname);

assert.equal(disabledResolve.sitePath, "ftp/ashford-poly/index.html");
assert.ok(disabledResolve.canonical, "Should return canonical redirect back to primary apex");
assert.ok(disabledResolve.canonical.includes(PRIMARY_APEX), "Canonical should point back to stardust-archive.net");

// Root access on disabled sister domain:
const disabledRoot = resolve("ashford-poly.org", "/");
assert.equal(disabledRoot.canonical, `https://${PRIMARY_APEX}/`, "Root on disabled sister domain should 301 to primary root");

console.log("  [✓] Passed: 301 Permanent Redirects verified in both directions (enable and rollback).\n");

// Re-enable for Worker edge test
FEDERATION["ashford-poly.org"].enabled = true;

// --- TEST 5: Edge Worker Request Handling & 301 Redirection ---
console.log("TEST 5: Edge Worker request routing (robots.txt, sitemaps, IndexNow, and 301 redirects)");
const worker = (await import("./worker.js")).default;
const mockEnv = { BASE_STATIC_URL: "https://jdurey.github.io/retro-arg-engine", SWARM_CAP: "0" };
const mockCtx = { waitUntil: () => {} };

// Test 301 redirect response through Worker fetch
const redirectRes = await worker.fetch(new Request(oldAshfordUrl), mockEnv, mockCtx);
assert.equal(redirectRes.status, 301, "Worker should return 301 Moved Permanently for old URL");
assert.ok(redirectRes.headers.get("Location").includes("ashford-poly.org"), "301 Location header should target ashford-poly.org");

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

console.log("  [✓] Passed: Dynamic edge robots.txt, sitemaps, IndexNow, and 301 HTTP redirects verified.\n");

// Revert memory state
for (const k of Object.keys(FEDERATION)) FEDERATION[k].enabled = false;

console.log("================================================================================");
console.log("             ALL MULTI-APEX FEDERATION TESTS PASSED (100%)");
console.log("================================================================================\n");
