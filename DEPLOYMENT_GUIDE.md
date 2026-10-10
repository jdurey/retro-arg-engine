# Deployment Guide: Nova Hart Retro ARG Engine (Netlify Edition)

To deploy this massive decentralized 1990s web swarm efficiently and cost-effectively, we are using **Netlify**. Netlify handles the Python build step automatically, serves the static files, and uses an **Edge Function** to intercept wildcard subdomains and spoof 1994 HTTP headers.

## Prerequisites
1. A domain name with DNS managed by Netlify (or configured to point to Netlify).
2. A GitHub/GitLab/Bitbucket repository containing this codebase.
3. A free Netlify account.

## Step 1: Deploy to Netlify
1. Log into your Netlify Dashboard.
2. Click **Add new site** -> **Import an existing project**.
3. Connect your Git provider and select the repository containing this project.
4. Netlify will automatically detect the `netlify.toml` file.
   * **Build command**: `python3 src/build.py`
   * **Publish directory**: `site`
5. Click **Deploy site**.

Netlify will boot up a build container, run the Python script to generate all 30,000+ files, and deploy the `site/` directory globally.

## Step 2: Configure Wildcard Domains
To make the illusion work, you need to point wildcard subdomains (e.g., `*.your-domain.com`) to your Netlify site.
1. In the Netlify Dashboard, go to your site's **Domain management**.
2. Add your custom domain (e.g., `telecom-history.net`).
3. If you are using Netlify DNS, add a wildcard DNS record:
   * **Record Type**: CNAME
   * **Name**: `*`
   * **Value**: `your-site-name.netlify.app`
4. *Note: Wildcard custom domains on Netlify require the Pro tier ($19/mo), which fits within the $25/month budget. Alternatively, you can explicitly add specific subdomains (e.g., `ftp.ashford-poly.your-domain.com`) on the Free tier.*

## Testing
The `netlify/edge-functions/router.js` script automatically intercepts the subdomains and routes them to the correct directory under `site/` while adding vintage headers.

Once DNS propagates, you can visit URLs like:
* `http://synthkid-2210.geocities.your-domain.com`
* `http://comp-dsp.usenet.your-domain.com`
* `http://ftp.ashford-poly.your-domain.com`

All requests will be served with authentic `CERN-HTTPd/3.0` server headers!
