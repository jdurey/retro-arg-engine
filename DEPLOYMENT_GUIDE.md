# Deployment Guide: Nova Hart Retro ARG Engine

To deploy this massive decentralized 1990s web swarm efficiently and cost-effectively (under $25/month), follow these instructions. 

## Overview
We are going to deploy the static files (the `site/` folder) to a free static host (like Cloudflare Pages), and then deploy a **Cloudflare Worker** as a reverse proxy. The worker will intercept wildcard subdomains (`*.your-domain.com`) and route them to the correct static folder while spoofing 1994 HTTP headers.

## Prerequisites
1. A domain name registered and using **Cloudflare DNS** (e.g. `telecom-history.net`).
2. The `wrangler` CLI installed (`npm install -g wrangler`).
3. Your Cloudflare account configured.

## Step 1: Deploy the Static Assets
1. Generate the static site locally if you haven't already:
   ```bash
   python3 src/build.py
   ```
2. Deploy the `site/` folder to **Cloudflare Pages**:
   ```bash
   npx wrangler pages deploy site/ --project-name retro-arg-static
   ```
3. Take note of the deployed URL (e.g., `https://retro-arg-static.pages.dev`).

## Step 2: Configure the Edge Router
1. Open `deploy/wrangler.toml`.
2. Update the `BASE_STATIC_URL` variable to match the URL you got in Step 1.
   ```toml
   [vars]
   BASE_STATIC_URL = "https://retro-arg-static.pages.dev"
   ```

## Step 3: Setup Wildcard DNS
1. Log into your Cloudflare Dashboard.
2. Go to your domain's **DNS** settings.
3. Add a **CNAME** record:
   * Name: `*` (asterisk, for a wildcard)
   * Target: your worker URL or `@` (depending on your setup)
   * Proxy status: **Proxied (Orange Cloud)**

## Step 4: Deploy the Worker
1. Navigate to the `deploy/` directory:
   ```bash
   cd deploy/
   ```
2. Deploy the worker to Cloudflare:
   ```bash
   wrangler deploy
   ```
3. In the Cloudflare Dashboard, go to **Workers & Pages** -> **Routes** for your domain.
4. Add a route linking `*.your-domain.com/*` to the `retro-arg-router` worker.

## Testing
Once DNS propagates, you can visit URLs like:
* `http://synthkid-2210.geocities.your-domain.com`
* `http://comp-dsp.usenet.your-domain.com`
* `http://ftp.ashford-poly.your-domain.com`

All requests will be routed to the static pages with authentic `CERN-HTTPd/3.0` server headers.
