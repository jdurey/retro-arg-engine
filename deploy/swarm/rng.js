// Deterministic PRNG for the edge swarm. Same seed parts -> same stream on every
// machine and every request, so a page is identical each time it is rendered.
// (cyrb128 string hash -> sfc32 generator; both are tiny and fast.)

function cyrb128(str) {
  let h1 = 1779033703, h2 = 3144134277, h3 = 1013904242, h4 = 2773480762;
  for (let i = 0; i < str.length; i++) {
    const k = str.charCodeAt(i);
    h1 = h2 ^ Math.imul(h1 ^ k, 597399067);
    h2 = h3 ^ Math.imul(h2 ^ k, 2869860233);
    h3 = h4 ^ Math.imul(h3 ^ k, 951274213);
    h4 = h1 ^ Math.imul(h4 ^ k, 2716044179);
  }
  h1 = Math.imul(h3 ^ (h1 >>> 18), 597399067);
  h2 = Math.imul(h4 ^ (h2 >>> 22), 2869860233);
  h3 = Math.imul(h1 ^ (h3 >>> 17), 951274213);
  h4 = Math.imul(h2 ^ (h4 >>> 19), 2716044179);
  h1 ^= h2 ^ h3 ^ h4; h2 ^= h1; h3 ^= h1; h4 ^= h1;
  return [h1 >>> 0, h2 >>> 0, h3 >>> 0, h4 >>> 0];
}

export function hash32(str) {
  return cyrb128(str)[0];
}

class Rng {
  constructor(seed) {
    [this.a, this.b, this.c, this.d] = cyrb128(seed);
    for (let i = 0; i < 12; i++) this.next();
  }
  next() {
    let { a, b, c, d } = this;
    const t = (((a + b) >>> 0) + d) >>> 0;
    this.d = (d + 1) >>> 0;
    this.a = b ^ (b >>> 9);
    this.b = (c + (c << 3)) >>> 0;
    c = (c << 21) | (c >>> 11);
    this.c = (c + t) >>> 0;
    return t;
  }
  random() { return this.next() / 4294967296; }
  /** inclusive on both ends, like Python's randint */
  int(lo, hi) { return lo + Math.floor(this.random() * (hi - lo + 1)); }
  chance(p) { return this.random() < p; }
  choice(arr) { return arr[Math.floor(this.random() * arr.length)]; }
  choices(arr, weights) {
    let total = 0;
    for (const w of weights) total += w;
    let x = this.random() * total;
    for (let i = 0; i < arr.length; i++) {
      x -= weights[i];
      if (x < 0) return arr[i];
    }
    return arr[arr.length - 1];
  }
  sample(arr, k) {
    const a = arr.slice();
    const n = Math.min(k, a.length);
    for (let i = 0; i < n; i++) {
      const j = i + Math.floor(this.random() * (a.length - i));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a.slice(0, n);
  }
  shuffle(arr) { return this.sample(arr, arr.length); }
}

export function rngFor(...parts) {
  return new Rng(parts.join("|"));
}
