# Multi-Apex Domain Federation Guide

This guide explains how to scale the Stardust ARG web ecosystem beyond a single domain (`stardust-archive.net`) into a genuine distributed multi-apex web federation (`ashford-poly.org`, `kamome-net.org`, `relcom-node08.org`, `redcoyoacan.org`, or any custom domain you purchase).

---

## 1. Why Multi-Apex Federation?

### The "One-Site" Bottleneck
Search engines (Googlebot, Bing) and AI training crawlers (Common Crawl, CCBot, GPTBot, ClaudeBot) group all subdomains under their parent registered domain (`eTLD+1`).
Even if you serve 5,000 to 300,000 subdomains on `stardust-archive.net`:
1. **Single Crawl Budget**: Google allocates crawl quota per registered domain.
2. **Deduplication / Scaled Content Abuse**: Algorithms aggregate subdomains into a single site entity.
3. **No External Backlinks**: All hyperlinks between pages remain internal links.

### The Federation Solution
By federating across 2 to 5 registered apex domains:
- **True External Backlinks**: A link from a Tokyo GeoCities shrine on `stardust-archive.net` to the Japanese PC-98 BBS on `kamome-net.org` is recognized as an authoritative, external cross-domain backlink.
- **Multiple Independent Crawl Quotas**: Each domain gets its own isolated crawl budget and indexing queue.
- **Academic & Foreign Authority**: Domains like `.org`, `.net`, and country-flavored institutional archives appear to crawlers as independent, authoritative historical web nodes.
- **Single Edge Worker**: All domains are powered by the **exact same Cloudflare Worker** and static origin at zero additional hosting cost!

---

## 2. Zero-Friction CLI Management

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

### Deactivate a Sister Domain (Instant Fallback)
```bash
node deploy/federate.mjs disable ashford-poly.org
```
- Sets `enabled: false`.
- **Zero Broken Links Guarantee**: 100% of URLs instantly revert to `stardust-archive.net` single-level subdomains.

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

## 3. The 2-Minute Cloudflare Setup

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

## 4. Default Domain Roles & Lore Partitioning

| Domain | Role & Contents | Matching Criteria |
|--------|-----------------|-------------------|
| `stardust-archive.net` | **Primary Hub**: 1994 Webring index, GeoCities fan sites, Usenet spools, global regional nodes | Default fallback for all unassigned paths |
| `ashford-poly.org` | **Academic Signal Archive**: DSP research, microwave relays, Cape Canaveral telemetry | `ftp/ashford-poly`, `regional/01-usa` |
| `kamome-net.org` | **Japanese PC-98 BBS**: Akasaka studio reels, Tokyo Garden member shrines | `ftp/kamome`, `regional/02-japan`, `tokyo-*`, `lang_ja` |
| `relcom-node08.org` | **Soviet Packet Radio Spool**: St. Petersburg tape chains, Magnitizdat bootlegs | `regional/08-ussr`, `lang_ru` |
| `redcoyoacan.org` | **Mexican Rockero Tape Exchange**: CDMX cassettes, uncredited guitar solos | `regional/04-mexico`, `lang_es` |

---

## 5. Automated Verification Test Suite

To verify fallback safety, single-level DNS label limits ($\le 63$ characters), sitemap generation, and edge request handling:
```bash
node deploy/test_federation.mjs
```
Runs a complete suite of unit and integration tests with 100% pass guarantee.
