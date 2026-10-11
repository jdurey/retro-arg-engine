// ==============================================================================
// PROJECT STARDUST: 1-Click Nightbot Command & Timer Auto-Configurator
// ==============================================================================
// Instructions:
// 1. In your browser, log in to: https://nightbot.tv/dashboard
// 2. Navigate to: https://nightbot.tv/commands/custom
// 3. Open Developer Console: Press Cmd + Option + J (Mac) or Ctrl + Shift + J (Win/Linux)
// 4. Paste this entire script into the console and hit Enter.
// It will automatically install all Project Stardust ARG commands and the 15-min broadcast timer!
// ==============================================================================

(async function installStardustNightbot() {
  console.log("%c[STARDUST]%c Initializing Nightbot ARG Auto-Configurator...", "color: #33ff33; font-weight: bold;", "color: white;");

  // Attempt to extract Nightbot Bearer token from localStorage
  let token = null;
  for (let key in localStorage) {
    try {
      const val = localStorage.getItem(key);
      if (val && val.includes("access_token")) {
        const parsed = JSON.parse(val);
        if (parsed.access_token) { token = parsed.access_token; break; }
      }
      if (key.toLowerCase().includes("token") && val && val.length > 20 && !val.startsWith("{")) {
        token = val;
      }
    } catch (e) {}
  }

  // Fallback: Check sessionStorage or prompt
  if (!token) {
    for (let key in sessionStorage) {
      try {
        const val = sessionStorage.getItem(key);
        if (val && val.includes("access_token")) {
          token = JSON.parse(val).access_token;
          break;
        }
      } catch (e) {}
    }
  }

  const authHeader = token ? { "Authorization": `Bearer ${token}` } : {};

  const COMMANDS = [
    {
      name: "!status",
      message: "[ORION DAEMON v3.0]: CARRIER: 14.2001 Hz // 5,000 NODES SYNCHRONIZED // ZERO PACKET LOSS // GATEWAY: https://stardust-archive.net/",
      coolDown: 5,
      userLevel: "everyone"
    },
    {
      name: "!carrier",
      message: "$(urlfetch https://stardust-archive.net/api/telemetry.txt)",
      coolDown: 5,
      userLevel: "everyone"
    },
    {
      name: "!tune",
      message: "[FREQUENCY LOCKED]: Intercepting 14.2 Hz Akasaka relay... Spool active: https://kamome-net.org/",
      coolDown: 5,
      userLevel: "everyone"
    },
    {
      name: "!whois",
      message: "[ARCHIVE RETRIEVAL]: SUBJECT: NOVA HART (1989). STATUS: SCHEDULED FOR PURGE. ERROR: RECURSIVE ARCHIVE PERSISTS at https://stardust-archive.net/",
      coolDown: 5,
      userLevel: "everyone"
    },
    {
      name: "!telemetry",
      message: "[TRANSMISSION]: Ashford Poly Telemetry Log (1989-09) -> https://stardust-archive.net/ftp/ashford-poly/hale_telemetry_1989-09.log",
      coolDown: 5,
      userLevel: "everyone"
    },
    {
      name: "!decode",
      message: "[LEVEL 4 CLEARANCE]: Clue file unsealed -> https://stardust-archive.net/geocities/area51-vault-7004.html",
      coolDown: 5,
      userLevel: "everyone"
    },
    {
      name: "!signal",
      message: "14.2 Hz sub-audible carrier detected across 13 regional nodes: Suva, Fiji; Tokyo; Moscow; Coyoacan; Hamburg. Check logs: https://stardust-archive.net/",
      coolDown: 5,
      userLevel: "everyone"
    },
    {
      name: "!help",
      message: "[SIGNAL MONITORS]: Available decoders: !status | !carrier | !tune | !whois | !telemetry | !decode | !signal",
      coolDown: 5,
      userLevel: "everyone"
    }
  ];

  const TIMER = {
    name: "Stardust_Relay",
    message: "[SYSTEM ANOMALY]: Unscheduled packet burst detected on 14.2 Hz. Decrypting relay logs at https://stardust-archive.net/",
    interval: 15,
    lines: 2
  };

  console.log(`%c[STARDUST]%c Detected token: ${token ? "YES (Authenticated)" : "Session/Cookie auth"}`, "color: #33ff33;", "color: white;");

  // Step 1: Install custom commands
  console.log("%c[STARDUST]%c Installing commands...", "color: #33ff33;", "color: cyan;");
  for (const cmd of COMMANDS) {
    try {
      const res = await fetch("https://api.nightbot.tv/1/commands", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeader
        },
        credentials: "include",
        body: JSON.stringify(cmd)
      });
      const data = await res.json();
      if (res.ok) {
        console.log(`  ✓ Installed command: ${cmd.name}`);
      } else if (data && data.message && data.message.includes("already exists")) {
        console.log(`  ℹ Command ${cmd.name} already exists. Skipping.`);
      } else {
        console.warn(`  ⚠ Command ${cmd.name}:`, data);
      }
    } catch (err) {
      console.error(`  ✕ Error installing ${cmd.name}:`, err);
    }
  }

  // Step 2: Install broadcast timer
  console.log("%c[STARDUST]%c Installing 15-minute lore timer...", "color: #33ff33;", "color: cyan;");
  try {
    const resTimer = await fetch("https://api.nightbot.tv/1/timers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeader
      },
      credentials: "include",
      body: JSON.stringify(TIMER)
    });
    const timerData = await resTimer.json();
    if (resTimer.ok) {
      console.log(`  ✓ Installed Timer: ${TIMER.name}`);
    } else {
      console.log(`  ℹ Timer info:`, timerData);
    }
  } catch (err) {
    console.error(`  ✕ Error installing timer:`, err);
  }

  console.log("%c=======================================================", "color: #33ff33;");
  console.log("%c[STARDUST COMPLETE]%c Commands and Timers configured successfully!", "color: #33ff33; font-weight: bold;", "color: white;");
  console.log("%cNext step: Click 'Join Channel' on your Nightbot Dashboard and make sure Nightbot is added as a Moderator in YouTube Live Studio!", "color: #ffaa00;");
  console.log("%c=======================================================", "color: #33ff33;");
})();
