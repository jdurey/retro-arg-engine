#!/usr/bin/env node
// CLI manager for Multi-Apex Domain Federation.
// Makes enabling, disabling, and managing sister domains effortless.
//
// Usage:
//   node deploy/federate.mjs status               - View status & URL distribution
//   node deploy/federate.mjs enable <domain>      - Enable sister domain
//   node deploy/federate.mjs disable <domain>     - Disable sister domain (safe fallback)
//   node deploy/federate.mjs rename <old> <new>   - Replace placeholder domain with your own domain
//   node deploy/federate.mjs guide [domain]       - Print 2-minute Cloudflare DNS setup guide

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FEDERATION_PATH = path.join(__dirname, "federation.js");
const WRANGLER_PATH = path.join(__dirname, "wrangler.toml");
const URLMAP_PATH = path.join(__dirname, "urlmap.js");
const STORY_PATH = path.join(__dirname, "story_paths.js");

async function loadConfig() {
  const fedModule = await import(`./federation.js?t=${Date.now()}`);
  const storyModule = await import(`./story_paths.js?t=${Date.now()}`);
  const urlmapModule = await import(`./urlmap.js?t=${Date.now()}`);
  return {
    PRIMARY_APEX: fedModule.PRIMARY_APEX,
    FEDERATION: fedModule.FEDERATION,
    STORY_PATHS: storyModule.default || [],
    apexFor: urlmapModule.apexFor,
  };
}

function showStatus(cfg) {
  console.log("\n================================================================================");
  console.log("             STARDUST MULTI-APEX DOMAIN FEDERATION STATUS");
  console.log("================================================================================");
  console.log(`Primary Apex : ${cfg.PRIMARY_APEX}`);
  console.log("--------------------------------------------------------------------------------");

  const wranglerContent = fs.readFileSync(WRANGLER_PATH, "utf8");

  // Calculate URL distribution
  const counts = { [cfg.PRIMARY_APEX]: 0 };
  for (const domain of Object.keys(cfg.FEDERATION)) counts[domain] = 0;
  for (const sp of cfg.STORY_PATHS) {
    const a = cfg.apexFor(sp);
    counts[a] = (counts[a] || 0) + 1;
  }

  console.log(
    " DOMAIN".padEnd(25) +
    " STATUS".padEnd(14) +
    " URLS".padEnd(10) +
    " WRANGLER ROUTE".padEnd(20) +
    " DESCRIPTION"
  );
  console.log("-".repeat(80));

  // Primary
  const primaryRouteActive = wranglerContent.includes(`zone_name = "${cfg.PRIMARY_APEX}"`) &&
    !wranglerContent.includes(`# { pattern = "*${cfg.PRIMARY_APEX}/*"`);
  console.log(
    ` ${cfg.PRIMARY_APEX}`.padEnd(25) +
    " [PRIMARY]".padEnd(14) +
    ` ${counts[cfg.PRIMARY_APEX]}`.padEnd(10) +
    ` ${primaryRouteActive ? "ACTIVE" : "MISSING"}`.padEnd(20) +
    " Main Stardust webring & collective hub"
  );

  // Sisters
  for (const [domain, conf] of Object.entries(cfg.FEDERATION)) {
    const isEnabled = !!conf.enabled;
    const isWranglerActive = new RegExp(`^\\s*\\{\\s*pattern\\s*=\\s*"\\*${domain.replace(".", "\\.")}\\/\\*"`, "m").test(wranglerContent);
    const statusStr = isEnabled ? " [ENABLED]" : " [STANDBY]";
    const routeStr = isWranglerActive ? "ACTIVE" : (isEnabled ? "NEEDS DEPLOY" : "COMMENTED");

    console.log(
      ` ${domain}`.padEnd(25) +
      statusStr.padEnd(14) +
      ` ${counts[domain] || 0}`.padEnd(10) +
      ` ${routeStr}`.padEnd(20) +
      ` ${conf.name || ""}`
    );
  }

  console.log("--------------------------------------------------------------------------------");
  const enabledCount = Object.values(cfg.FEDERATION).filter((c) => c.enabled).length;
  if (enabledCount === 0) {
    console.log(" [i] Sister domains are in STANDBY (all URLs cleanly route to stardust-archive.net).");
    console.log("     To activate a domain: node deploy/federate.mjs enable <domain>");
  } else {
    console.log(` [✓] ${enabledCount} sister domain(s) ACTIVE. Traffic & backlinks are partitioned.`);
    console.log("     Deploy edge updates: npx wrangler deploy --config deploy/wrangler.toml");
  }
  console.log("================================================================================\n");
}

function enableDomain(domain) {
  let content = fs.readFileSync(FEDERATION_PATH, "utf8");
  if (!content.includes(`"${domain}"`) && !content.includes(`'${domain}'`)) {
    console.error(`[!] Domain "${domain}" not found in deploy/federation.js.`);
    console.log("    Use 'node deploy/federate.mjs status' to see available domains.");
    process.exit(1);
  }

  // Set enabled: true for domain block
  const domainRegex = new RegExp(`(["']${domain}["']\\s*:\\s*\\{[\\s\\S]*?enabled\\s*:\\s*)(false|true)`);
  if (!domainRegex.test(content)) {
    console.error(`[!] Could not parse block for "${domain}".`);
    process.exit(1);
  }
  content = content.replace(domainRegex, `$1true`);
  fs.writeFileSync(FEDERATION_PATH, content, "utf8");

  // Activate route in wrangler.toml
  let wrangler = fs.readFileSync(WRANGLER_PATH, "utf8");
  const commentedRoute = new RegExp(`^\\s*#\\s*(\\{\\s*pattern\\s*=\\s*"\\*${domain.replace(".", "\\.")}\\/\\*"[^\n]*)`, "m");
  if (commentedRoute.test(wrangler)) {
    wrangler = wrangler.replace(commentedRoute, "  $1");
    fs.writeFileSync(WRANGLER_PATH, wrangler, "utf8");
    console.log(`[✓] Activated route for ${domain} in deploy/wrangler.toml.`);
  } else if (!wrangler.includes(`zone_name = "${domain}"`)) {
    // Add route before ]
    const routeInsert = `  { pattern = "*${domain}/*", zone_name = "${domain}" },\n`;
    wrangler = wrangler.replace(/(\nroutes\s*=\s*\[\n)/, `$1${routeInsert}`);
    fs.writeFileSync(WRANGLER_PATH, wrangler, "utf8");
    console.log(`[✓] Added new route for ${domain} in deploy/wrangler.toml.`);
  }

  console.log(`[✓] Domain "${domain}" is now ENABLED!`);
  console.log(`\nNext steps:`);
  console.log(`  1. Ensure ${domain} is added to Cloudflare and DNS is proxied (run: node deploy/federate.mjs guide ${domain})`);
  console.log(`  2. Deploy router: npx wrangler deploy --config deploy/wrangler.toml`);
  console.log(`  3. Ping search engines: node deploy/indexnow.mjs\n`);
}

function disableDomain(domain) {
  let content = fs.readFileSync(FEDERATION_PATH, "utf8");
  if (!content.includes(`"${domain}"`) && !content.includes(`'${domain}'`)) {
    console.error(`[!] Domain "${domain}" not found in deploy/federation.js.`);
    process.exit(1);
  }

  const domainRegex = new RegExp(`(["']${domain}["']\\s*:\\s*\\{[\\s\\S]*?enabled\\s*:\\s*)(false|true)`);
  content = content.replace(domainRegex, `$1false`);
  fs.writeFileSync(FEDERATION_PATH, content, "utf8");

  // Comment out route in wrangler.toml
  let wrangler = fs.readFileSync(WRANGLER_PATH, "utf8");
  const activeRoute = new RegExp(`^(\\s*)(\\{\\s*pattern\\s*=\\s*"\\*${domain.replace(".", "\\.")}\\/\\*"[^\n]*)`, "m");
  if (activeRoute.test(wrangler)) {
    wrangler = wrangler.replace(activeRoute, "$1# $2");
    fs.writeFileSync(WRANGLER_PATH, wrangler, "utf8");
    console.log(`[✓] Commented out route for ${domain} in deploy/wrangler.toml.`);
  }

  console.log(`[✓] Domain "${domain}" is now DISABLED.`);
  console.log(`    All matching paths safely fall back to stardust-archive.net.`);
  console.log(`    To apply: npx wrangler deploy --config deploy/wrangler.toml\n`);
}

function renameDomain(oldDomain, newDomain) {
  let content = fs.readFileSync(FEDERATION_PATH, "utf8");
  if (!content.includes(`"${oldDomain}"`) && !content.includes(`'${oldDomain}'`)) {
    console.error(`[!] Old domain "${oldDomain}" not found in deploy/federation.js.`);
    process.exit(1);
  }

  content = content.replaceAll(oldDomain, newDomain);
  fs.writeFileSync(FEDERATION_PATH, content, "utf8");

  let wrangler = fs.readFileSync(WRANGLER_PATH, "utf8");
  wrangler = wrangler.replaceAll(oldDomain, newDomain);
  fs.writeFileSync(WRANGLER_PATH, wrangler, "utf8");

  console.log(`[✓] Successfully renamed "${oldDomain}" -> "${newDomain}" across federation configs!`);
  console.log(`    Run 'node deploy/federate.mjs guide ${newDomain}' for DNS setup instructions.`);
}

function printGuide(domain = "<your-domain.org>") {
  console.log(`
================================================================================
          CLOUDFLARE 2-MINUTE SETUP GUIDE FOR SISTER DOMAIN: ${domain}
================================================================================

Step 1: Buy / Acquire the Domain
--------------------------------------------------------------------------------
Purchase any domain name of your choice (e.g. at Porkbun, Namecheap, Cloudflare, etc.).
Example: ${domain}

Step 2: Add Domain to Cloudflare
--------------------------------------------------------------------------------
1. In Cloudflare Dashboard (dash.cloudflare.com), click "Add a domain".
2. Enter "${domain}" and select the FREE plan.
3. Cloudflare will give you 2 nameservers (e.g. bob.ns.cloudflare.com).
4. At your domain registrar, update the nameservers to Cloudflare's.

Step 3: Add Wildcard & Apex DNS Records
--------------------------------------------------------------------------------
In Cloudflare -> ${domain} -> DNS -> Records, add these TWO records:

  Record 1 (Wildcard Subdomains):
    Type         : CNAME
    Name         : *
    Target       : stardust-archive.net
    Proxy status : Proxied (Orange cloud ON)  <-- CRITICAL!
    TTL          : Auto

  Record 2 (Apex / Root):
    Type         : CNAME
    Name         : @
    Target       : stardust-archive.net
    Proxy status : Proxied (Orange cloud ON)  <-- CRITICAL!
    TTL          : Auto

Step 4: Enable & Deploy
--------------------------------------------------------------------------------
Run these two commands:
  node deploy/federate.mjs enable ${domain}
  npx wrangler deploy --config deploy/wrangler.toml

Step 5: Notify Search Engines
--------------------------------------------------------------------------------
  node deploy/indexnow.mjs

THAT'S IT! 
- Cloudflare automatically provisions a free Universal SSL certificate.
- The single Worker serves both stardust-archive.net and ${domain}.
- Search engines & AI crawlers will now index them as completely separate,
  independent authoritative domains with bidirectional cross-linking!
================================================================================
`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || "status";

  if (command === "status") {
    const cfg = await loadConfig();
    showStatus(cfg);
  } else if (command === "enable") {
    const domain = args[1];
    if (!domain) { console.error("Usage: node deploy/federate.mjs enable <domain>"); process.exit(1); }
    enableDomain(domain);
  } else if (command === "disable") {
    const domain = args[1];
    if (!domain) { console.error("Usage: node deploy/federate.mjs disable <domain>"); process.exit(1); }
    disableDomain(domain);
  } else if (command === "rename") {
    const oldDomain = args[1];
    const newDomain = args[2];
    if (!oldDomain || !newDomain) { console.error("Usage: node deploy/federate.mjs rename <oldDomain> <newDomain>"); process.exit(1); }
    renameDomain(oldDomain, newDomain);
  } else if (command === "guide") {
    printGuide(args[1] || "ashford-poly.org");
  } else {
    console.log("Usage: node deploy/federate.mjs [status|enable|disable|rename|guide]");
  }
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
