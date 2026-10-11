// Procedural 1995-1996 GeoCities fan page generator (swarm v3).
// JS port of src/swarm_corner.py (which stays frozen for the 5,039 legacy static
// pages), extended with more regions/languages, more section types, visitor
// guestbooks, update logs and hood/region affinity.
//
// header(id) is cheap (directories list hundreds of them per request);
// page(id) builds the full body.

import BANK from "./bank.js";
import { addressOf } from "./address.js";
import { rngFor } from "./rng.js";

const SEED = "nova-hart-v3";
const B = BANK.base;
const REGION_KEYS = Object.keys(BANK.regions);

// Regions that cluster in particular neighborhoods (GeoCities had Tokyo, Paris,
// Vienna, Athens, RainForest communities). Multiplies the base region weight.
const HOOD_AFFINITY = {
  Tokyo: { jp: 5, kr: 3, tw: 4 }, Paris: { fr: 5, it: 1.5 }, Vienna: { de: 4, nl: 3, se: 2 },
  Athens: { gr: 6 }, RainForest: { br: 4, mx: 3 }, Colosseum: { it: 3, br: 1.5, mx: 1.5 },
  SiliconValley: { us: 2, hi: 1.5 }, Nashville: { us: 3, au: 1.5 }, Heartland: { us: 3 },
};

export const LAYOUTS = ["shrine", "two_column", "terminal", "hub", "plain", "index_table"];

const text = (f) => (f && typeof f === "object" ? f.t : String(f));
const available = (f, date) => !(f && typeof f === "object" && f.nb && f.nb > date);

function fmt(template, vars) {
  return String(text(template)).replace(/\{\{|\}\}|\{([a-z_0-9]+)\}/g, (m, k) => {
    if (m === "{{") return "{";
    if (m === "}}") return "}";
    return k in vars ? String(vars[k]) : m;
  });
}
const pad2 = (n) => String(n).padStart(2, "0");

function region(key) {
  const reg = BANK.regions[key];
  const lang = BANK.langs[reg.lang] || BANK.langs.en;
  return { key, reg, lang: reg.lang, native: reg.native || (lang.native && Object.keys(lang.native).length ? lang.native : null), ui: lang.ui || {}, info: lang.info };
}

function pickRegion(r, hood) {
  const aff = HOOD_AFFINITY[hood] || {};
  return r.choices(REGION_KEYS, REGION_KEYS.map((k) => BANK.regions[k].weight * (aff[k] || 1)));
}

function pickDate(r) {
  const year = r.choice([1995, 1995, 1996, 1996, 1996]);
  return `${year}-${pad2(r.int(1, 12))}-${pad2(r.int(1, 28))}`;
}

function shiftDate(date, daysBack) {
  const d = new Date(date + "T00:00:00Z");
  d.setUTCDate(d.getUTCDate() - daysBack);
  const s = d.toISOString().slice(0, 10);
  return s < "1995-01-01" ? "1995-01-01" : s;
}

function emailUser(name) {
  return name.toLowerCase().normalize("NFKD").replace(/[^a-z0-9]/g, "") || "fan";
}

/** Cheapest lookup: just the language (same draw header() makes first). */
export function langOf(id) {
  return BANK.regions[pickRegion(rngFor(SEED, "head", id), addressOf(id).hood)].lang;
}

/** Cheap per-page identity (used by directories and the page itself). */
export function header(id) {
  const addr = addressOf(id);
  const r = rngFor(SEED, "head", id);
  const R = region(pickRegion(r, addr.hood));
  const reg = R.reg;
  const name = r.choice(reg.names);
  const city = r.choice(reg.cities);
  const date = pickDate(r);
  const station = r.int(100, 999);
  const vars = { name, city, station };
  const titlePool = reg.titles && reg.titles.length && r.chance(0.85) ? reg.titles : B.titles_en;
  const user = emailUser(name);
  return {
    id, ...addr, region: R.key, lang: R.lang, name, city, date,
    title: fmt(r.choice(titlePool), vars),
    email: `${user && /^[a-z]/.test(user) ? user : "fan"}${addr.num}@${r.choice(reg.domains)}`,
    counter: Math.floor(Math.exp(r.random() * Math.log(25000))) + r.int(0, 40),
    layout: r.choice(LAYOUTS),
    palette: r.choice(reg.palettes),
  };
}

function pool(native, key, enKey, prob, r, date) {
  const nat = native && native[key] ? native[key].filter((f) => available(f, date)) : [];
  if (nat.length && r.chance(prob)) return { frag: r.choice(nat), native: true };
  const en = (B.en[enKey || key] || []).filter((f) => available(f, date));
  return en.length ? { frag: r.choice(en), native: false } : null;
}

function applyVoice(s, voiceType, r) {
  const cfg = B.voice[voiceType] || {};
  const words = s.split(" ").map((w) => {
    if (cfg.caps && r.chance(cfg.caps) && w.length > 3 && !w.includes("{")) w = w.toUpperCase();
    if (cfg.typo && r.chance(cfg.typo) && w.length > 4 && /^[a-z]+$/i.test(w)) {
      const i = r.int(1, w.length - 3);
      w = w.slice(0, i) + w[i + 1] + w[i] + w.slice(i + 2);
    }
    return w;
  });
  let out = words.join(" ");
  if (cfg.bang && r.chance(cfg.bang) && !/[!?]$/.test(out)) out = out.replace(/\.$/, "") + "!".repeat(r.int(1, 3));
  if (cfg.tail && r.chance(0.35)) out += " " + r.choice(cfg.tail);
  return out;
}

const EXTRA_SECTIONS = { about: 0.45, updates: 0.4, guestbook: 0.35, awards: 0.15 };

/** Full page model for id. */
export function page(id) {
  const h = header(id);
  const r = rngFor(SEED, "body", id);
  const R = region(h.region);
  const native = R.native;
  const reg = R.reg;
  const date = h.date;
  const year = Number(date.slice(0, 4));

  const archKeys = Object.keys(B.archetypes);
  const arch = r.choices(archKeys, archKeys.map((k) => {
    const w = B.archetypes[k].regions;
    return w[h.region] ?? w.other ?? 1;
  }));
  const A = B.archetypes[arch];
  const voice = A.voice || "polite";

  const age = r.int(14, 36);
  const song = r.choice(B.songs);
  const jp = r.choice(B.jp_singles);
  const how = r.choice(B.en.how);
  const vars = {
    name: h.name, city: h.city, host: h.name, station: r.int(100, 999), age, age_then: Math.max(7, age - (year - 1985)),
    fan_since: r.choice([1984, 1985, 1985, 1985, 1986, 1987, 1988, 1989, 1990]), how, how_cap: how[0].toUpperCase() + how.slice(1),
    song: song[0], year: song[1], format: r.choice(B.formats), n: r.int(2, 45), mmss: `${r.int(1, 4)}:${pad2(r.int(10, 59))}`,
    secs: r.int(4, 52), cents: r.int(12, 48), db: r.int(35, 68),
    emo: r.choice(B.emo[reg.emo] || B.emo.default), receiver: r.choice(B.receivers), deck: r.choice(B.decks),
    computer: r.choice(B.computers), modem: r.choice(B.modems), phones: r.choice(B.phones), price: r.choice(B.prices),
    grade: r.choice(B.grades), nick: `${emailUser(h.name).slice(0, 8) || "nova"}${r.int(10, 99)}`, date,
    year_hard: r.choice([1989, 1990, 1991, 1992, 1993]), jp_file: jp[0], jp_title: jp[1], jp_en: jp[2],
    pressing: reg.pressing, pressing_short: h.region.toUpperCase(), node: reg.node, region_name: h.region.toUpperCase(),
    line: B.node_lines[String(reg.node)] || "HOLD FOR RELAY", fake: r.choice(B.fake_lines),
    pp_regions: r.choice(["Japan & Mexico", "Europe & USA", "Brazil & Russia", "Scandinavia & Asia", "everywhere"]),
    langs: r.choice(["English & Spanish", "English & German", "English & French", "English & Japanese (learning!)", "English & Russian", "English & Dutch", "English & Greek"]),
    friends: `${r.choice(["Sven", "Lucia", "Kenji", "Dmitri", "Ines", "Bram", "Eleni", "Wei"])} and ${r.choice(["Aiko", "Mateo", "Nadia", "Tobias", "Camila", "Sanne", "Nikos", "Mei"])}`,
    who: r.choice(B.who), gen: r.int(3, 7), copy_no: r.int(100, 999),
    chain: r.choice(["Riga -> Moscow -> St. Petersburg", "Berlin -> Warsaw -> Kyiv", "Vladivostok -> Khabarovsk", "Tallinn -> Leningrad"]),
    date_jp: `199${r.int(4, 6)}年${r.int(1, 12)}月`,
  };
  if (native) for (const [k, v] of Object.entries(native)) if (k.startsWith("how_") && Array.isArray(v)) vars[k] = r.choice(v);

  const avail = (arr) => (arr || []).filter((f) => available(f, date));
  const headings = (native && native.headings) || {};
  const H = (key, fallback) => headings[key] || fallback;
  const say = (f, isNative) => {
    const s = fmt(text(f), vars);
    return isNative ? s : applyVoice(s, voice, r);
  };

  // ---- choose sections: intro first, archetype picks, optional extras, shuffled
  const want = { ...A.sections };
  const picks = [];
  const types = Object.keys(want);
  const count = r.int(3, Math.min(7, types.length));
  const rem = types.slice();
  for (let i = 0; i < count && rem.length; i++) {
    const t = r.choices(rem, rem.map((k) => want[k]));
    picks.push(t);
    rem.splice(rem.indexOf(t), 1);
  }
  for (const [t, p] of Object.entries(EXTRA_SECTIONS)) if (r.chance(p)) picks.push(t);
  const body = r.shuffle(picks.filter((t) => t !== "guestbook"));
  if (body.includes("updates") && r.chance(0.6)) body.unshift(body.splice(body.indexOf("updates"), 1)[0]);
  const order = ["hi", ...body, ...(picks.includes("guestbook") ? ["guestbook"] : [])];

  const sections = [];
  for (const t of order) {
    const s = sectionFor(t);
    if (s) sections.push(s);
  }

  function sectionFor(t) {
    const P = (key, enKey, prob, fallbackHeading) => {
      const got = pool(native, key, enKey, prob, r, date);
      if (!got) return null;
      return { h: got.native ? H(key, fallbackHeading) : fallbackHeading, p: [say(got.frag, got.native)], native: got.native };
    };
    switch (t) {
      case "hi": {
        const s = P("hi", "hi", 0.85, "Hi!");
        if (s && s.native && native.sorry && r.chance(0.4)) s.p.push(native.sorry);
        return s;
      }
      case "favorite": return P("favorite", "favorite", 0.8, r.choice(["Favorite Song", "My Favourite", "The Song"]));
      case "theory": {
        const s = P("theory", "theory_a", 0.75, r.choice(["My Theory", "What I Think Is Going On", "Theory Corner"]));
        if (s && !s.native && r.chance(0.6)) s.p[0] += " " + fmt(r.choice(avail(B.en.theory_b)), vars);
        return s;
      }
      case "where_i_was": return P("where_i_was", "where_i_was", 0.75, "Where I Was");
      case "marcus": return P("marcus", "marcus", 0.7, "Who Was Marcus Hale?");
      case "listening_night": return P("listening", "listening", 0.7, "Listening Night 02:14 UTC Log");
      case "node_hunt": return P("node_hunt", "node_hunt", 0.75, `Relay Matrix // Node ${pad2(reg.node)}`);
      case "skeptic": return P("skeptic", "skeptic", 0.7, r.choice(["A Sceptic's Counter-Argument", "Devil's Advocate", "Let's Be Real"]));
      case "letter": return P("letter", "letter", 0.8, r.choice(["Letter to Nova", "Dear Nova", "If You Read This"]));
      case "concert_dream": return P("concert_dream", "concert", 0.7, "Live Concert Dream");
      case "pen_pals": return P("pen_pals", "pen_pals", 0.8, "International Pen-Pals Wanted");
      case "solos": return P("solos", null, 1, "The Mexican Pressing Guitar Solos") ||
        { h: "The Mexican Pressing Guitar Solos", p: [`The Mexican pressing (Orion México) has uncredited guitar solos on '${vars.song}' that are muted on the US release. At ${vars.mmss}, the studio band lets loose!`] };
      case "tape_genealogy": return P("tape_genealogy", null, 1, "Magnitizdat Tape Genealogy") ||
        { h: "Magnitizdat Tape Genealogy", p: [`My cassette copy is generation #${vars.gen} dubbed from ${vars.chain}. Even through the hiss, the 14.2 Hz pulse moves the VU meter.`] };
      case "akasaka": {
        const s = P("akasaka", null, 1, "The Akasaka Master Tapes");
        return s || (date >= "1995-05-22" ? { h: "The Akasaka Master Tapes (Recovered May 1995)", p: ["The unreleased Akasaka reel box contains 'Synthesized Smile' and 'Ghost in the Chorus'. Every box is stamped 'VOICE PRINT: GEN-3'."] } : null);
      }
      case "spectrum": {
        const s = P("spectrum", "spectrum", 0.75, r.choice(["14.2 Hz Signal Analysis & DSP", "My FFT Results", "Spectrum Lab"]));
        if (s && r.chance(0.7)) {
          const lvl = -r.int(38, 48);
          s.pre = [" Frequency (Hz) | Level (dB) | Spectral Density [FFT " + r.choice([1024, 2048, 4096, 8192]) + "]", "----------------+------------+--------------------------------",
            `  ${(9 + r.random() * 2).toFixed(1)} Hz       |  -${r.int(60, 70)} dB    | *`,
            `  14.2 Hz [PEAK]|  ${lvl} dB    | ${"*".repeat(70 + lvl)} [CARRIER]`,
            `  ${(17 + r.random() * 3).toFixed(1)} Hz       |  -${r.int(62, 72)} dB    | *`,
            `  ${r.choice(["50", "60"])} Hz         |  -${r.int(48, 56)} dB    | ${"*".repeat(r.int(4, 9))} [MAINS HUM]`];
        }
        return s;
      }
      case "collection": {
        const got = pool(native, "collection", null, 1, r, date);
        const s = { h: got && got.native ? H("collection", "My Collection") : r.choice(["My Collection & Pressing Log", "The Stash", "Records & Tapes"]),
          p: [got ? say(got.frag, got.native) : `My Nova Hart records and tapes as of ${date}:`] };
        s.pre = ["PRESSING / EDITION                         GRADE  NOTES", "------------------------------------------ ------ --------------------------"];
        const keys = REGION_KEYS;
        for (let i = r.int(2, 6); i > 0; i--) {
          const pr = BANK.regions[r.choice(keys)].pressing.replace(/^the /, "").slice(0, 42);
          s.pre.push(`${pr.padEnd(42)} ${r.choice(B.grades).padEnd(6)} ${fmt(r.choice(avail(B.en.collection_notes)), vars)}`);
        }
        return s;
      }
      case "trading": {
        const got = pool(native, "trading", null, 1, r, date);
        const s = { h: got && got.native ? H("trading", "Tape Trading") : r.choice(["Tape Trading & Mail Order", "Trades", "WANTS / HAVES"]),
          p: [got ? say(got.frag, got.native) : "Looking for audio and video trades! SASE or IRC required for international tape mail."] };
        s.p.push("<b>WANTS:</b>");
        s.list = r.sample(avail(B.en.trading_wants), r.int(2, 4)).map((x) => fmt(x, vars));
        s.p2 = [`<b>HAVES:</b> ${r.sample(avail(B.en.trading_haves), r.int(2, 4)).map((x) => fmt(x, vars)).join(", ")}.`];
        return s;
      }
      case "gear": {
        const nat = native && native.gear && avail(native.gear);
        const en = avail(B.en.gear);
        const items = nat && nat.length && r.chance(0.8) ? r.sample(nat, r.int(2, Math.min(4, nat.length))) : r.sample(en, r.int(2, Math.min(4, en.length)));
        return { h: nat ? H("gear", "My Gear") : r.choice(["My Listening Post & Audio Gear", "The Rig", "Equipment"]), list: items.map((g) => fmt(text(g), vars)) };
      }
      case "top5": {
        const nat = native && native.top5;
        const heading = nat && r.chance(0.5) ? H("top5", "Top 5") : fmt(r.choice(B.en.top5), vars);
        return { h: heading, ol: r.sample(B.songs, 5).map((s) => `'${s[0]}' (${s[1]})`) };
      }
      case "jp_singles":
        return { h: H("jp_singles", "Orion Records Japan: Idol Protocol Singles"), p: ["Akasaka Branch 7-inch & cassette singles, 1985-1989:"],
          pre: ["CATALOGUE   YEAR  JAPANESE TITLE                ENGLISH TITLE", "----------- ----  ----------------------------  ------------------------",
            ...B.jp_singles.filter(() => r.chance(0.6)).map((s) => `${s[0].padEnd(11)} ${s[3]}  ${s[1].padEnd(28)}  ${s[2]}`)],
          p2: [r.choice(["(Still looking for the rest - write me!)", "Missing ones are on my WANTS list.", "Bold = I own it on vinyl.", "Catalogue numbers from the Akasaka sleeves.", ""])].filter(Boolean) };
      case "vhs": {
        const nat = native && native.vhs;
        return { h: nat ? H("vhs", "VHS Log") : "VHS Off-Air Recording Log", list: nat ? r.sample(nat, Math.min(3, nat.length)).map((v) => fmt(text(v), vars)) :
          ["1985-06-08 Hamburg broadcast 'Memory Hatch' freeze (tape degradation: heavy)", "1986-10-12 Meridian Broadcast live satellite capture (clean audio, some dropout)",
            `1989-12-09 Final broadcast recording (Nova looks off camera at ${vars.mmss})`].slice(0, r.int(2, 3)) };
      }
      case "lyric_log": {
        const nat = native && native.lyric_log;
        return { h: nat ? H("lyric_log", "Lyric Log") : "Lyric Discrepancy & Translation Anomalies", list: nat ? r.sample(nat, Math.min(2, nat.length)).map((v) => fmt(text(v), vars)) :
          [`At ${vars.mmss}: the US lyric says 'dream', the regional master clearly says 'machine'.`, "The chorus double-track drifts off the lyric sheet by half a beat."] };
      }
      case "fanart": {
        const s = P("fanart", "fanart", 0.5, r.choice(["Nova-chan Fan Art & ASCII", "Art Corner", "ASCII Gallery"]));
        if (s) s.pre = r.choice(B.ascii_art);
        return s;
      }
      case "midi": {
        const got = pool(native, "midi", null, 1, r, date);
        return { h: got && got.native ? H("midi", "MIDI Archive") : "General MIDI Sequence Archive (.MID)",
          p: [got ? say(got.frag, got.native) : "Sequenced on Cakewalk for a Sound Canvas SC-55 / Sound Blaster 16. Right-click to save:"],
          midis: r.sample(B.midi_slugs, r.int(3, 7)) };
      }
      case "about": return P("about", "about", 0.8, r.choice(["About Me", "Who Am I?", "About This Page", "The Webmaster"]));
      case "updates": {
        const nu = avail(native && native.updates);
        const src = nu.length && r.chance(0.8) ? nu : avail(B.en.updates);
        if (!src || !src.length) return null;
        let back = 0;
        const items = r.sample(src, r.int(3, Math.min(7, src.length))).map((u) => {
          const d = shiftDate(date, back);
          back += r.int(3, 40);
          return `<b>${d}</b> - ${fmt(text(u), vars)}`;
        });
        return { h: src !== nu ? r.choice(["What's New", "Updates", "Recent Changes", "NEW STUFF"]) : H("updates", "What's New"), list: items, newFlag: true };
      }
      case "guestbook": {
        const entries = [];
        for (let i = r.int(2, 6); i > 0; i--) {
          const vk = r.choices(REGION_KEYS, REGION_KEYS.map((k) => BANK.regions[k].weight));
          const V = region(vk);
          const vn = avail(V.native && V.native.guestbook);
          const vsrc = vn.length ? vn : avail(B.en.guestbook);
          if (!vsrc || !vsrc.length) continue;
          const vvars = { ...vars, city: r.choice(V.reg.cities), emo: r.choice(B.emo[V.reg.emo] || B.emo.default) };
          entries.push({ who: r.choice(V.reg.names), from: vvars.city, date: shiftDate(date, r.int(0, 200)), text: fmt(text(r.choice(vsrc)), vvars) });
        }
        if (!entries.length) return null;
        entries.sort((a, b) => (a.date < b.date ? 1 : -1));
        return { h: H("guestbook", r.choice(["Guestbook", "Sign My Guestbook!", "What Visitors Said"])), guestbook: entries };
      }
      case "awards":
        return { h: r.choice(["Awards", "My Awards!", "Thanks For The Awards"]), list: r.sample([
          "Stardust Webring Station of the Week", "Cool Site of the Day (well, the Nova Hart part of it)", "Top 5% of Nova Hart pages (according to a guy on IRC)",
          "Golden Carrier Award - 14.2 Hz Fan Guild", "Best Tape Trader 1995 (alt.fan.nova-hart poll, unofficial)", "Hold-For-Relay Gold Badge"], r.int(1, 3)) };
      default:
        return null;
    }
  }

  // Uncommon clue (decoded node line) on ~12% of pages; rare/legendary clues
  // stay on the curated + legacy static pages.
  let clue = null;
  if (r.chance(0.12)) {
    clue = `Decoded relay matrix (Node ${pad2(reg.node)} / ${h.region.toUpperCase()}): '${vars.line}'.`;
    sections.splice(r.int(1, sections.length), 0, { h: "Secret Note // Decrypted Transmission", p: [`<b>[INTERCEPT / RECOVERED DATA]:</b> ${clue}`] });
  }

  const nativeMarquees = avail(native && native.marquees);
  const marquee = r.chance(0.8) ? fmt(nativeMarquees.length && r.chance(0.8) ? r.choice(nativeMarquees) : r.choice(avail(B.marquees_en)), vars) : null;
  const desc = native && native.desc && r.chance(0.8)
    ? fmt(native.desc, { name: h.name, city: h.city, path_display: h.pathDisplay })
    : `${h.name}'s personal fan page (${h.city}) about Nova Hart and the 14.2 Hz Stardust signal at GeoCities ${h.pathDisplay}.`;

  return {
    ...h, archetype: arch, sections, marquee, description: desc, clue,
    badges: r.sample(B.badges, r.int(1, 4)),
    links: r.sample(B.links, r.int(2, 5)),
    midi: r.chance(0.55) ? r.choice(B.midi_slugs) : null,
    ui: R.ui, langInfo: R.info,
    style: {
      marker: r.choice(["&#9733; ", "", "&gt;&gt; ", "~*~ ", "&#9679; ", ":: ", "&#9830; "]),
      hr: r.choice(['<HR SIZE=3 NOSHADE>', '<HR>', '<HR WIDTH="60%">', '<HR SIZE=1>', '<CENTER>* * * * *</CENTER>', '<HR SIZE=5 WIDTH="80%" NOSHADE>']),
      counterStyle: r.choice(["digits", "digits", "text", "bracket"]),
      badgesTop: r.chance(0.25),
      construction: r.chance(0.55),
      lowercase: r.chance(0.3),
      generator: r.choice([null, null, "Mozilla/2.0 (Win95; I) [Netscape Navigator Gold 2.0]", "Microsoft FrontPage 1.1", "HoTMetaL PRO 2.0", "HotDog Professional 2.0", "Claris Home Page 1.0", null]),
      font: r.choice([null, "Arial,Helvetica", "Verdana,Arial", "Times New Roman,Times", "Comic Sans MS", "Courier New,Courier"]),
      width: r.choice([null, null, 600, 640, 480]),
    },
  };
}
