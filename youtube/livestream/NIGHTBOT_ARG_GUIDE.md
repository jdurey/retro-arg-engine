# 📡 Nightbot ARG Integration Guide: Project Stardust

Transform your 24/7 YouTube Livestream into a living, responsive numbers station terminal. Viewers chatting on the livestream can decode signals, retrieve classified logs, tune relays, and inspect dynamic carrier telemetry in real time.

---

## ⚡ 60-Second Setup Guide

### Step 1: Log in & Join Channel
1. Open **[Nightbot Dashboard](https://nightbot.tv/dashboard)** in your browser.
2. Click **Log In** and select **YouTube** (authenticate using your YouTube channel account: `Nova Hart`).
3. On the top right of your dashboard, click the blue button: **"Join Channel"**.

### Step 2: Make Nightbot a Moderator on YouTube
To allow Nightbot to post in your live stream chat:
1. Open **[YouTube Studio Live Stream Dashboard](https://studio.youtube.com/channel/UCQ2nHAazpB_HIiiQCPqFm1w/livestreaming)**.
2. In the Live Chat window on the right, click **Settings (⚙️)** or navigate to **Settings -> Community -> Automated Filters**.
3. Under **Managing Moderators**, paste Nightbot's official channel URL:
   ```text
   https://www.youtube.com/channel/UCG0106N92Jb1g6L3rC7nK8A
   ```
4. Click **Save**. Nightbot is now authorized to talk in chat!

---

## 🚀 1-Click Auto-Configuration (DevTools Console)

Instead of manually typing 8 commands and timers into the UI, you can install everything in 3 seconds:

1. In your browser, navigate to: **[Nightbot Custom Commands](https://nightbot.tv/commands/custom)**.
2. Open Chrome Developer Console:
   - **Mac**: Press `Cmd + Option + J`
   - **Windows / Linux**: Press `Ctrl + Shift + J`
3. Paste the contents of [`nightbot_setup.js`](file:///Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine/youtube/livestream/nightbot_setup.js) into the console and hit **Enter**.

All commands and the 15-minute ARG broadcast timer will be created automatically!

---

## 📋 Command Matrix Reference

| Command | Response Message | Description |
| :--- | :--- | :--- |
| `!status` | `[ORION DAEMON v3.0]: CARRIER: 14.2001 Hz // 5,000 NODES SYNCHRONIZED // ZERO PACKET LOSS // GATEWAY: https://stardust-archive.net/` | Displays core server and node synchronization state. |
| `!carrier` | `$(urlfetch https://stardust-archive.net/api/telemetry.txt)` | **Dynamic Live Telemetry**: Nightbot queries Cloudflare edge to fetch live carrier frequency and packet counts in real time. |
| `!tune` | `[FREQUENCY LOCKED]: Intercepting 14.2 Hz Akasaka relay... Spool active: https://stardust-archive.net/ftp/kamome/` | Directs ARG investigators to the Tokyo Akasaka spool mirror. |
| `!whois` | `[ARCHIVE RETRIEVAL]: SUBJECT: NOVA HART (1989). STATUS: SCHEDULED FOR PURGE. ERROR: RECURSIVE ARCHIVE PERSISTS at https://stardust-archive.net/` | In-lore character dossier clue pointing to the persistent web archive. |
| `!telemetry` | `[TRANSMISSION]: Ashford Poly Telemetry Log (1989-09) -> https://stardust-archive.net/ftp/ashford-poly/hale_telemetry_1989-09.log` | Deep link to the raw laboratory telemetry text log. |
| `!decode` | `[LEVEL 4 CLEARANCE]: Clue file unsealed -> https://stardust-archive.net/geocities/area51-vault-7004.html` | Decryption access link to the Area 51 Geocities vault. |
| `!signal` | `14.2 Hz sub-audible carrier detected across 13 regional nodes: Suva, Fiji; Tokyo; Moscow; Coyoacan; Hamburg. Check logs: https://stardust-archive.net/` | Global packet relay node coordinates. |
| `!help` | `[SIGNAL MONITORS]: Available decoders: !status \| !carrier \| !tune \| !whois \| !telemetry \| !decode \| !signal` | Help directory for chat viewers. |

---

## ⏱️ Periodic Lore Broadcast Timer

| Setting | Value |
| :--- | :--- |
| **Timer Name** | `Stardust_Relay` |
| **Interval** | Every **15 minutes** |
| **Chat Lines** | **2 lines** minimum chat activity |
| **Message** | `[SYSTEM ANOMALY]: Unscheduled packet burst detected on 14.2 Hz. Decrypting relay logs at https://stardust-archive.net/` |

---

## 🌐 Dynamic Edge Telemetry Endpoint

We have deployed the dynamic telemetry route directly onto Cloudflare Workers at:
👉 **`https://stardust-archive.net/api/telemetry.txt`**

When called by Nightbot or any browser, it returns:
```text
[ORION DAEMON v3.0] [CARRIER: 14.2004 Hz] [NODES: 5,000 ACTIVE] [PACKETS: 3312957] [GATEWAY: https://stardust-archive.net/] [UTC: 09:06:15]
```
- Carrier frequency oscillates realistically on the sub-audible 14.200 Hz band.
- Packet counter increments dynamically.
- Live UTC time displays to the exact second.
