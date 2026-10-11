// Configuration for Multi-Apex Domain Federation.
// When a sister domain is marked `enabled: true`, matching paths route to that apex.
// When `enabled: false`, all paths gracefully fall back to PRIMARY_APEX (stardust-archive.net).

export const PRIMARY_APEX = "stardust-archive.net";

export const FEDERATION = {
  "ashford-poly.org": {
    enabled: false,
    name: "Ashford Polytechnic Signal Analysis & Telemetry Archive",
    description: "Academic signal processing lab, microwave relay logs, and declassified DOD telemetry.",
    match: {
      paths: ["ftp/ashford-poly"],
      regional: ["01-usa"],
    },
  },
  "kamome-net.org": {
    enabled: false,
    name: "Kamome Net Akasaka Idol Protocol Archive",
    description: "Japanese PC-98 BBS, Akasaka branch master reels, and regional packet archives.",
    match: {
      paths: ["ftp/kamome"],
      regional: ["02-japan"],
    },
  },
  "relcom-node08.org": {
    enabled: false,
    name: "Relcom Node 08 Soviet Tape Archive",
    description: "Amateur packet radio spools, St. Petersburg tape chains, and Magnitizdat copies.",
    match: {
      regional: ["08-ussr"],
    },
  },
  "redcoyoacan.org": {
    enabled: false,
    name: "Red Coyoacán Mexican Tape Exchange",
    description: "Mexican rockero collective, uncredited guitar solos, and CDMX cassettes.",
    match: {
      regional: ["04-mexico"],
    },
  },
};
