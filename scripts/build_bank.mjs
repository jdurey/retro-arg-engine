// Compiles data/bank_v3/{base,regions/*,lang/*,expand/*}.json into
// deploy/swarm/bank.js and validates it. Exits non-zero on any violation, so CI
// blocks a bad bank before deploy.
//
// Usage: node scripts/build_bank.mjs [--check]   (--check: validate, and fail if bank.js is stale)
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const SRC = path.join(ROOT, "data", "bank_v3");
const OUT = path.join(ROOT, "deploy", "swarm", "bank.js");
const read = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const ls = (d) => (fs.existsSync(d) ? fs.readdirSync(d).filter((f) => f.endsWith(".json")).sort() : []);

const base = read(path.join(SRC, "base.json"));
const regions = Object.fromEntries(ls(path.join(SRC, "regions")).map((f) => [f.slice(0, -5), read(path.join(SRC, "regions", f))]));
const langs = Object.fromEntries(ls(path.join(SRC, "lang")).map((f) => [f.slice(0, -5), read(path.join(SRC, "lang", f))]));

function appendPools(target, add) {
  for (const [k, v] of Object.entries(add || {})) {
    if (!Array.isArray(v)) { target[k] = target[k] ?? v; continue; }
    const have = target[k] || (target[k] = []);
    const seen = new Set(have.map((f) => JSON.stringify(f)));
    for (const f of v) if (!seen.has(JSON.stringify(f))) { have.push(f); seen.add(JSON.stringify(f)); }
  }
}

for (const f of ls(path.join(SRC, "expand"))) {
  const key = f.slice(0, -5);
  const add = read(path.join(SRC, "expand", f));
  if (key === "en") {
    const { marquees, titles, ...pools } = add.native || {};
    appendPools(base.en, pools);
    appendPools(base, { marquees_en: marquees || [], titles_en: titles || [] });
  } else if (regions[key] && regions[key].native) { // region-level native (e.g. Australian English)
    appendPools(regions[key].native, add.native);
    regions[key].native.headings = { ...regions[key].native.headings, ...add.headings };
  } else if (langs[key]) {
    appendPools(langs[key].native, add.native);
    langs[key].native.headings = { ...(langs[key].native.headings || {}), ...add.headings };
  } else {
    throw new Error(`expand/${f}: no matching lang or region`);
  }
}

// ---------------------------------------------------------------- validation
const errors = [];
const SLOTS = new Set(("name city age age_then fan_since how how_cap song year format n mmss secs cents db emo receiver deck computer modem phones " +
  "price grade nick date year_hard jp_file jp_title jp_en pressing pressing_short node region_name line fake pp_regions langs friends who gen copy_no " +
  "chain date_jp host station path_display").split(" "));
const ANACHRONISMS = /\b(dvd|napster|google|wi-?fi|broadband|smartphone|iphone|ipod|blog|facebook|myspace|youtube|twitter|windows 98|windows xp|y2k|mp3 player|usb|bluetooth|texting|emoji)\b/i;
const FORBIDDEN = /sloan|слоан|スローン|슬론|斯隆|σλόαν|σλοαν/i;
const BAD_YEAR = /(?<!\d)(199[7-9]|20(?:0\d|1\d|2[0-4]|2[6-9]))(?!\d)/;
// Canon dates: anything dated in the lore file, plus nb dates in the original (v2) export.
const timelineDates = new Set([
  ...fs.readFileSync(path.join(ROOT, "data", "lore_seeds.json"), "utf8").matchAll(/\b(19[89]\d-\d{2}-\d{2})\b/g),
  ...JSON.stringify(base).matchAll(/"nb":"(\d{4}-\d{2}-\d{2})"/g),
].map((m) => m[1]));

function checkString(s, where, extraSlots) {
  if (FORBIDDEN.test(s)) errors.push(`${where}: forbidden name: ${s.slice(0, 80)}`);
  if (ANACHRONISMS.test(s)) errors.push(`${where}: anachronism '${s.match(ANACHRONISMS)[0]}': ${s.slice(0, 80)}`);
  if (BAD_YEAR.test(s)) errors.push(`${where}: post-1996 year '${s.match(BAD_YEAR)[0]}': ${s.slice(0, 80)}`);
  for (const m of s.matchAll(/\{([^{}]*)\}/g)) {
    const before = s[m.index - 1], after = s[m.index + m[0].length];
    if (before === "{" && after === "}") continue; // {{literal}}
    const k = m[1];
    if (!SLOTS.has(k) && !(extraSlots && extraSlots.has(k))) errors.push(`${where}: unknown slot {${k}}: ${s.slice(0, 80)}`);
  }
}
const nbWarn = [];
function walk(v, where, extraSlots) {
  if (typeof v === "string") return checkString(v, where, extraSlots);
  if (Array.isArray(v)) return v.forEach((x, i) => walk(x, `${where}[${i}]`, extraSlots));
  if (v && typeof v === "object") {
    if ("t" in v && Object.keys(v).every((k) => k === "t" || k === "nb")) {
      if (v.nb !== undefined) {
        if (!/^\d{4}-\d{2}-\d{2}$/.test(v.nb) || v.nb > "1996-12-31") errors.push(`${where}: bad nb '${v.nb}'`);
        else if (!timelineDates.has(v.nb)) nbWarn.push(`${where}: nb ${v.nb} not a canon date`);
      }
      return checkString(v.t, where, extraSlots);
    }
    for (const [k, x] of Object.entries(v)) walk(x, `${where}.${k}`, extraSlots);
  }
}

const UI_EN = langs.en.ui;
const fmtCount = (s) => (String(s).match(/%[sd]/g) || []).join("");
for (const [code, L] of Object.entries(langs)) {
  const hows = new Set(Object.keys(L.native || {}).filter((k) => k.startsWith("how_")));
  walk(L.native, `lang/${code}.native`, hows);
  if (code !== "en") {
    for (const k of Object.keys(UI_EN)) {
      if (!(k in (L.ui || {}))) errors.push(`lang/${code}.ui missing key ${k}`);
      else if (fmtCount(L.ui[k]) !== fmtCount(UI_EN[k])) errors.push(`lang/${code}.ui.${k}: placeholders differ from en`);
    }
    for (const k of ["name", "region", "node"]) if (!L.info || !L.info[k]) errors.push(`lang/${code}.info missing ${k}`);
  }
}
for (const [key, R] of Object.entries(regions)) {
  for (const k of ["weight", "lang", "emo", "names", "cities", "domains", "palettes", "pressing", "node"]) if (R[k] === undefined) errors.push(`regions/${key} missing ${k}`);
  if (!langs[R.lang]) errors.push(`regions/${key}: lang '${R.lang}' has no lang file`);
  if (R.emo && !base.emo[R.emo]) errors.push(`regions/${key}: emo '${R.emo}' not in base.emo`);
  for (const p of R.palettes || []) if (!(Array.isArray(p) && p.length === 4 && p.every((c) => /^#[0-9A-Fa-f]{6}$/.test(c)))) errors.push(`regions/${key}: bad palette ${JSON.stringify(p)}`);
  const hows = new Set(Object.keys(R.native || {}).filter((k) => k.startsWith("how_")));
  walk({ titles: R.titles, native: R.native, names: R.names, cities: R.cities }, `regions/${key}`, hows);
}
walk(base.en, "base.en");
walk({ titles_en: base.titles_en, marquees_en: base.marquees_en, links: base.links }, "base");

// ---------------------------------------------------------------- emit
const bank = { base, regions, langs };
const js = "// Generated by scripts/build_bank.mjs from data/bank_v3 - do not edit\nexport default " + JSON.stringify(bank) + ";\n";
const counts = {
  english: Object.values(base.en).reduce((n, v) => n + (Array.isArray(v) ? v.length : 0), 0),
  ...Object.fromEntries(Object.entries(langs).map(([c, L]) => [c, Object.values(L.native || {}).reduce((n, v) => n + (Array.isArray(v) ? v.length : 0), 0)])),
};
console.error("fragments:", JSON.stringify(counts));
if (nbWarn.length) console.error(`${nbWarn.length} nb dates not found in canon (warning; review):\n  ` + nbWarn.slice(0, 15).join("\n  "));
if (errors.length) {
  console.error(`${errors.length} bank errors:\n  ` + errors.slice(0, 60).join("\n  "));
  process.exit(1);
}
if (process.argv.includes("--check")) {
  const cur = fs.existsSync(OUT) ? fs.readFileSync(OUT, "utf8") : "";
  if (cur !== js) { console.error("deploy/swarm/bank.js is stale: run node scripts/build_bank.mjs"); process.exit(1); }
  console.error("bank OK (up to date)");
} else {
  fs.writeFileSync(OUT, js);
  console.error(`wrote ${path.relative(ROOT, OUT)} (${(js.length / 1024).toFixed(0)} KB)`);
}
