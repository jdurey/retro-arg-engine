// Page id <-> GeoCities address, e.g. 41207 <-> "Tokyo/Ginza/4412" (slug
// "tokyo-ginza-4412"). A keyed Feistel permutation scatters ids over every
// suburb's 1000-9999 address block, and it is invertible, so the Worker can turn
// any requested hostname back into the id that generates the page.

import { hash32 } from "./rng.js";

// [Neighborhood, Suburb]. The first 18 are the v2 suburbs (legacy static pages
// live there too; a static page always wins over a generated one at the same
// address). The rest are period GeoCities suburbs of the same neighborhoods.
export const SUBURBS = [
  ["SiliconValley", "Lab"], ["Hollywood", "Hills"], ["SunsetStrip", "Club"], ["Area51", "Vault"], ["Tokyo", "Garden"],
  ["Athens", "Forum"], ["Paris", "LeftBank"], ["CapeCanaveral", "Lab"], ["Heartland", "Plains"], ["SoHo", "Studio"],
  ["Vienna", "Strasse"], ["Colosseum", "Field"], ["TimesSquare", "Arcade"], ["Nashville", "Opry"], ["RainForest", "Canopy"],
  ["Pentagon", "Quarters"], ["BourbonStreet", "Delta"], ["EnchantedForest", "Glade"],
  ["SiliconValley", "Park"], ["SiliconValley", "Heights"], ["SiliconValley", "Pines"], ["SiliconValley", "Bay"],
  ["Hollywood", "Lot"], ["Hollywood", "Set"], ["Hollywood", "Academy"], ["Hollywood", "Bungalow"],
  ["SunsetStrip", "Stage"], ["SunsetStrip", "Palms"], ["SunsetStrip", "Alley"], ["SunsetStrip", "Towers"],
  ["Area51", "Zone"], ["Area51", "Hangar"], ["Area51", "Nebula"], ["Area51", "Corridor"],
  ["Tokyo", "Ginza"], ["Tokyo", "Temple"], ["Tokyo", "Pagoda"], ["Tokyo", "Island"],
  ["Athens", "Acropolis"], ["Athens", "Agora"], ["Athens", "Delphi"], ["Athens", "Olympus"],
  ["Paris", "Cafe"], ["Paris", "Metro"], ["Paris", "Salon"],
  ["CapeCanaveral", "Launchpad"], ["CapeCanaveral", "Hall"], ["CapeCanaveral", "Station"],
  ["Heartland", "Prairie"], ["Heartland", "Valley"], ["Heartland", "Ranch"], ["Heartland", "Woods"],
  ["SoHo", "Lofts"], ["SoHo", "Square"], ["SoHo", "Gallery"],
  ["Vienna", "Opera"], ["Vienna", "Choir"], ["Vienna", "Waltz"],
  ["Colosseum", "Track"], ["Colosseum", "Arena"], ["Colosseum", "Bleachers"],
  ["TimesSquare", "Alley"], ["TimesSquare", "Lobby"], ["TimesSquare", "Dungeon"], ["TimesSquare", "Maze"],
  ["Nashville", "Stage"], ["Nashville", "Rodeo"],
  ["RainForest", "Vines"], ["RainForest", "Andes"], ["RainForest", "Jungle"],
  ["Pentagon", "Barracks"], ["Pentagon", "Bunker"], ["Pentagon", "Fort"],
  ["BourbonStreet", "Bayou"], ["BourbonStreet", "Square"],
  ["EnchantedForest", "Dell"], ["EnchantedForest", "Meadow"], ["EnchantedForest", "Tower"],
];

export const BLOCK = 9000; // addresses 1000..9999 per suburb
export const DOMAIN = SUBURBS.length * BLOCK;
export const suburbSlug = (i) => `${SUBURBS[i][0]}-${SUBURBS[i][1]}`.toLowerCase();
const SLUG_TO_SUBURB = new Map(SUBURBS.map((_, i) => [suburbSlug(i), i]));

// ---- keyed Feistel permutation over [0, 2^BITS), cycle-walked into [0, DOMAIN)
const HALF = 10;
const BITS = HALF * 2;
const MASK = (1 << HALF) - 1;
const ROUNDS = 4;
const KEYS = Array.from({ length: ROUNDS }, (_, i) => hash32(`stardust-swarm-v3|feistel|${i}`));
if (DOMAIN > 1 << BITS) throw new Error("address domain exceeds permutation width");

function round(x, k) {
  let h = Math.imul(x ^ k, 0x45d9f3b);
  h ^= h >>> 13;
  h = Math.imul(h, 0x45d9f3b);
  return (h ^ (h >>> 16)) & MASK;
}
function feistel(x) {
  let l = x >>> HALF, r = x & MASK;
  for (let i = 0; i < ROUNDS; i++) [l, r] = [r, l ^ round(r, KEYS[i])];
  return (l << HALF) | r;
}
function feistelInv(x) {
  let l = x >>> HALF, r = x & MASK;
  for (let i = ROUNDS - 1; i >= 0; i--) [l, r] = [r ^ round(l, KEYS[i]), l];
  return (l << HALF) | r;
}
function perm(x) {
  do { x = feistel(x); } while (x >= DOMAIN);
  return x;
}
function permInv(x) {
  do { x = feistelInv(x); } while (x >= DOMAIN);
  return x;
}

export function addressOf(id) {
  const slot = perm(id);
  const sub = Math.floor(slot / BLOCK);
  const num = 1000 + (slot % BLOCK);
  const [hood, suburb] = SUBURBS[sub];
  return { suburbIndex: sub, num, hood, suburb, slug: `${suburbSlug(sub)}-${num}`, pathDisplay: `${hood}/${suburb}/${num}` };
}

/** slug -> id, or -1 if the slug is not a generated-swarm address. */
export function idOf(slug) {
  const m = /^(.+)-(\d{4})$/.exec(slug);
  if (!m) return -1;
  const sub = SLUG_TO_SUBURB.get(m[1]);
  const num = Number(m[2]);
  if (sub === undefined || num < 1000) return -1;
  return permInv(sub * BLOCK + (num - 1000));
}

/** ids whose address falls in a suburb, in address order (for directories). */
const suburbMemo = new Map();
export function idsInSuburb(sub) {
  let out = suburbMemo.get(sub);
  if (!out) {
    out = new Int32Array(BLOCK);
    for (let n = 0; n < BLOCK; n++) out[n] = permInv(sub * BLOCK + n);
    suburbMemo.set(sub, out);
  }
  return out;
}
