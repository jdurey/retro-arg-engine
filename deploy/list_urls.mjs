// Exports every public URL (for YouTube descriptions) and verifies that each
// URL routes back to the exact file it came from.
// Usage: node deploy/list_urls.mjs [site_dir] > urls.csv
import fs from "node:fs";
import path from "node:path";
import { publicUrl, resolve } from "./urlmap.js";

const siteDir = process.argv[2] || "site";
const rows = [];
const hosts = new Map();
let errors = 0;

function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full);
    else rows.push(path.relative(siteDir, full).split(path.sep).join("/"));
  }
}
walk(siteDir);

const out = ["site_path,public_url"];
for (const sp of rows.sort()) {
  if (sp.startsWith("assets/")) continue;
  const pub = publicUrl(sp);
  if (!pub) { console.error("UNMAPPED", sp); errors++; continue; }
  const u = new URL(pub);
  const label = u.hostname.split(".")[0];
  if (label.length > 63) { console.error("LABEL TOO LONG", pub); errors++; }
  const back = resolve(u.hostname, u.pathname);
  const expect = sp;
  if (back.sitePath !== expect || back.canonical) { console.error("ROUNDTRIP FAIL", sp, pub, JSON.stringify(back)); errors++; }
  const owner = hosts.get(u.hostname);
  const group = sp.split("/").slice(0, sp.startsWith("geocities/") ? 2 : 2).join("/");
  if (owner && owner !== group) { console.error("HOST COLLISION", u.hostname, owner, group); errors++; }
  hosts.set(u.hostname, group);
  out.push(`${sp},${pub}`);
}
console.log(out.join("\n"));
console.error(`${out.length - 1} URLs, ${hosts.size} hosts, ${errors} errors`);
process.exit(errors ? 1 : 0);
