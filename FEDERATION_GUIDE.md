# Multi-Apex Domain Federation Guide

This guide explains how to scale the Stardust ARG web ecosystem beyond a single domain (`stardust-archive.net`) into a genuine distributed multi-apex web federation (`ashford-poly.org`, `kamome-net.org`, `relcom-node08.org`, `redcoyoacan.org`, or any custom domain you purchase).

---

## 1. Why Multi-Apex Federation?

### The "One-Site" Bottleneck
Search engines (Googlebot, Bing) and AI training crawlers (Common Crawl, CCBot, GPTBot, ClaudeBot) group all subdomains under their parent registered domain (`eTLD+1`).
Even if you serve 5,000 to 300,000 subdomains on `stardust-archive.net`:
1. **Single Crawl Budget**: Google allocates crawl quota per registered domain.
2. **Deduplication / Scaled Content Abuse**: Algorithms aggregate subdomains into a single site entity.
3. **Entity Conflation**: An academic telemetry archive, a Japanese PC-98 BBS, and a 1994 teen GeoCities fan shrine are all collapsed into the same domain entity.

### The Federation Solution: Institutional Entity Isolation
By federating institutional archives across 2 to 5 registered apex domains:
- **In-World Immersion**: In 1994, Ashford Polytechnic and Kamome Net had their own discrete domains. An academic signal processing lab would never be hosted under a random pop-culture fan webring.
- **Organic Quality & Anti-Spam Safety**: 
  - Sister domains **ONLY host hand-crafted institutional archives** (15 to 60 clean, authentic files).
  - All 5,100+ GeoCities fan shrines and the entire 300,000 generated swarm **remain strictly on `stardust-archive.net`**.
  - A brand new domain never launches with tens of thousands of programmatic pages (which search engines penalize as scaled content abuse on fresh domains).
- **Navigation, Not Link Schemes**: Cross-domain links between institutions and the webring serve purely as natural, immersive story navigation. We avoid artificial "backlink scheme" patterns.
- **Multiple Independent Crawl Quotas**: Each domain gets its own isolated crawl budget, robots.txt, and sitemap queue.
- **Single Edge Worker**: All domains are powered by the **exact same Cloudflare Worker** and static origin at zero additional hosting cost!

---

## 2. 301 Permanent Redirect Architecture

When content moves between domains, links already indexed by Google, Bing, or IndexNow must not break or generate 404s/duplicate content.

1. **When a Sister Domain is Enabled**:
   - Historical URLs on `stardust-archive.net` (e.g. `https://ashford-poly-ftp-...stardust-archive.net/...`) automatically issue an **HTTP 301 Moved Permanently** redirecting to the canonical URL on the sister domain (`https://ashford-poly-ftp-...ashford-poly.org/...`).
   - Search engines seamlessly transfer page history and indexing signals.
2. **When a Sister Domain is Disabled (Rollback Safety)**:
   - Any requests hitting the sister domain immediately issue an **HTTP 301 Moved Permanently** redirect back to `stardust-archive.net`.
   - Root requests (`https://ashford-poly.org/`) redirect to `https://stardust-archive.net/`.
   - **Zero Broken Links Guarantee**: Symmetrical 301 redirection in both directions.

---

## 3. Zero-Friction CLI Management

We built a dedicated CLI tool: [`deploy/federate.mjs`](file:///Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/deploy/federate.mjs).

### Check Federation Status & URL Distribution
```bash
node deploy/federate.mjs status
```
Displays an interactive table showing which domains are active, how many URLs are routed to each, and whether Cloudflare Worker routes are deployed.

### Activate a Sister Domain
```bash
node deploy/federate.mjs enable ashford-poly.org
```
- Sets `enabled: true` in `deploy/federation.js`.
- Uncomments the route in `deploy/wrangler.toml`.
- Re-partitions URLs so `ashford-poly.org` takes ownership of signal telemetry and academic archives.
- Activates automatic 301 redirects from `stardust-archive.net`.

### Deactivate a Sister Domain (Instant Fallback)
```bash
node deploy/federate.mjs disable ashford-poly.org
```
- Sets `enabled: false`.
- All URLs instantly revert to `stardust-archive.net` with 301 redirects for any incoming traffic.

### Rename / Use Your Own Purchased Domain
If you purchase a custom domain (e.g. `tokyo-underground.net` instead of `kamome-net.org`):
```bash
node deploy/federate.mjs rename kamome-net.org tokyo-underground.net
```
Automatically updates all path matching rules and wrangler configurations!

### Print DNS Setup Guide
```bash
node deploy/federate.mjs guide [domain]
```

---

## 4. The 2-Minute Cloudflare Setup

Whenever you register a new domain for federation:

### Step 1: Add Domain to Cloudflare
1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) -> **Add a domain**.
2. Type your domain (e.g. `ashford-poly.org`). Choose the **Free** plan.
3. Update nameservers at your registrar (Namecheap, Porkbun, Cloudflare Registrar, etc.).

### Step 2: Add 2 DNS Records in Cloudflare
In Cloudflare -> Your Domain -> **DNS** -> **Records**:

| Type  | Name | Target                 | Proxy Status           | TTL  |
|-------|------|------------------------|------------------------|------|
| CNAME | `*`  | `stardust-archive.net` | **Proxied (Orange ON)**| Auto |
| CNAME | `@`  | `stardust-archive.net` | **Proxied (Orange ON)**| Auto |

> [!IMPORTANT]
> The Proxy status **MUST be Proxied (Orange cloud ON)** so Cloudflare's Universal SSL certificate covers the wildcard subdomains without SSL warnings.

### Step 3: Enable & Deploy Worker
```bash
node deploy/federate.mjs enable <your-domain>
npx wrangler deploy --config deploy/wrangler.toml
```

### Step 4: Instant Search Engine Indexing
```bash
node deploy/indexnow.mjs
```
The Worker automatically serves the IndexNow validation key at `https://<your-domain>/37feeed875722863fda484c68e6695e5.txt`, notifying Bing, Yandex, and Naver within seconds!

---

## 5. Domain Roles & Curated Institutional Scope

| Domain | Role & Contents | Total Pages | Matching Scope |
|--------|-----------------|-------------|----------------|
| `stardust-archive.net` | **Primary Webring Hub**: All GeoCities fan shrines, all 300k generated swarm pages, Usenet spools | 5,070+ static + 300k swarm | Default home for all community content |
| `ashford-poly.org` | **Academic Signal Archive**: DOD telemetry logs, microwave relays, DSP signal papers | 16 pages | `ftp/ashford-poly`, `regional/01-usa` |
| `kamome-net.org` | **Japanese PC-98 BBS**: Akasaka master reels, Japanese packet radio spools | 63 pages | `ftp/kamome`, `regional/02-japan` |
| `relcom-node08.org` | **Soviet Packet Radio Spool**: St. Petersburg tape chains, Magnitizdat bootlegs | 1 page (expandable) | `regional/08-ussr` |
| `redcoyoacan.org` | **Mexican Rockero Tape Exchange**: CDMX cassettes, uncredited guitar solos | 1 page (expandable) | `regional/04-mexico` |

---

## 6. Automated Verification Test Suite

To verify fallback safety, single-level DNS label limits ($\le 63$ characters), 301 redirects, sitemap generation, and edge request handling:
```bash
node deploy/test_federation.mjs
```
Runs a complete suite of unit and integration tests with 100% pass guarantee.
