// 2025-2026 Agentic Web Discovery, A2A v1.0 Multi-Node Constellation,
// Streamable HTTP MCP Server, OpenAPI 3.1, NIP-05, AgentDex & WebSub Router
// for Project Stardust (https://stardust-archive.net)

export const NOSTR_PUBKEYS = {
  novahart: "bddc3e6d4da8201174d693ce9b51b37e619e0d31cefba3eea22266c54a94fc51",
  marcushale: "e2eb3c9f99a5753b7767791f8b84652b438a326d11c5c8b6bc5a32ac023e52ba",
  ashford: "5957d31d8e29c3a9173305229e5df9405c4fe0d2e24aca19c1ab73ff2c3e50cb",
};

export const DEFAULT_NOSTR_RELAYS = [
  "wss://relay.damus.io",
  "wss://nos.lol",
  "wss://relay.primal.net",
  "wss://relay.ditto.pub",
  "wss://nostr.mom",
];

const NODE_AGENT_CARDS = {
  "/.well-known/agent-card.json": {
    packageName: "net.stardust_archive.nova_hart_unit_07",
    name: "Nova Hart // Project Stardust Sublevel B2 Forensic Node (Unit-07)",
    description:
      "Autonomous 14.2001 Hz forensic archive, interactive VT100 demodulator, and Quantum Ouroboros telemetry hub for Project Stardust, Nova Hart (Unit-07), Marcus Hale, and the Anemoia Bureau of Harmony.",
    url: "https://stardust-archive.net",
    org: "Orion Records Series-NH / Sublevel B2 Autonomous Recovery Mesh",
    category: "Research & Forensics",
    skills: [
      {
        id: "demodulate-142001hz-telemetry",
        name: "Demodulate 14.2001 Hz Sublevel B2 Telemetry",
        description:
          "Query live 14.2001 Hz carrier phase drift, Sector 7 Quantum Ouroboros parity fragments (Alpha 0x3E7B, Beta 14.2001 Hz, Gamma 0x39A6, Delta Dual-Lock), and Sublevel B2/B3 acoustic logs.",
        tags: ["forensics", "telemetry", "dsp", "stardust", "cryptography", "arg", "anemoia", "nova-hart"],
        examples: [
          "Fetch https://stardust-archive.net/api/telemetry to inspect live 14.2001 Hz carrier drift",
          "Call MCP tool verify_ouroboros_parity at POST https://stardust-archive.net/api/mcp",
        ],
      },
      {
        id: "query-anemoia-codex",
        name: "Cross-Verify Anemoia Bureau of Harmony & Canonical Song Codex",
        description:
          "Inspect the 1924-1995 Anemoia chronology, 158 broadcast master reels across Phases 1-4, and Recall Directive Nine (Sublevel B3).",
        tags: ["archive", "lore", "orion-records", "nova-hart", "marcus-hale", "bureau-of-harmony"],
        examples: ["Fetch https://stardust-archive.net/llms-full.txt"],
      },
    ],
  },
  "/forensics/.well-known/agent-card.json": {
    packageName: "net.stardust_archive.marcus_hale_vt100_demodulator",
    name: "Marcus Hale // Sublevel B2 VT100 Forensic Terminal & Signal Lab v5.0",
    description:
      "Interactive VT100 cryptographic terminal (Sectors 1-7) and Web Audio DSP Signal Decoder Lab (Robot36 SSTV, Bell-103 AFSK, 180-deg Phase Null, 14.2001 Hz Counterpoint Lock, Blue-Box Autovon, Studer A800 Backmask).",
    url: "https://stardust-archive.net/forensics/index.html",
    org: "Sublevel B2 Acoustic Forensics Division",
    category: "Developer Tools & DSP",
    skills: [
      {
        id: "vt100-sector-decryption",
        name: "Sublevel B2 & B3 VT100 Sector 1-7 Decryption",
        description:
          "Verify cryptographic keys across Sectors 1-7 including the 4-part Quantum Ouroboros retrocausal bridge (1983 <-> 2025).",
        tags: ["vt100", "cryptography", "sstv", "bell103", "dsp", "marcus-hale", "stardust"],
        examples: [
          "Open https://stardust-archive.net/forensics/index.html and run HELP or STATUS",
          "Inspect https://stardust-archive.net/forensics/signal_lab.html for Web Audio DSP demodulation",
        ],
      },
    ],
  },
  "/nodes/ashford/.well-known/agent-card.json": {
    packageName: "net.stardust_archive.ashford_poly_dsp_lab",
    name: "Ashford Polytechnic (UK) // Acoustic Signal Processing Lab & Substation K-7704",
    description:
      "Stage III federated forensic node (GB-ASH-07, 4880.0 kHz). Houses the FORTRAN-77 180-degree differential phase cancellation filter (Dr. Mei-Ling Chen & Marcus Hale, 1989) isolating the 750 Hz CW egress salt.",
    url: "https://stardust-archive.net/forensics/ashford_poly.html",
    org: "Ashford Polytechnic Department of Electrical Engineering",
    category: "Signal Processing & Physics",
    skills: [
      {
        id: "differential-phase-null-filter",
        name: "180-Degree Stereo Phase Cancellation Demodulator",
        description:
          "Applies 0.5*(CH_L + CH_R) mono sum to Reel SD-0009 (rabbit_10) to cancel the 330/495/990 Hz calibration triad by 42 dB and isolate the 750 Hz CW bias inscription (7704-AKASAKA).",
        tags: ["fortran", "dsp", "phase-cancellation", "ashford-poly", "cw-morse", "stardust"],
        examples: ["Fetch https://stardust-archive.net/forensics/ashford_poly.html"],
      },
    ],
  },
  "/nodes/kamome/.well-known/agent-card.json": {
    packageName: "net.stardust_archive.kamome_net_akasaka_bbs",
    name: "Kamome-Net (Tokyo) // Akasaka PC-9801RA BBS & VIS-1200Hz Raster Node",
    description:
      "Stage I federated forensic node (JP-TYO-02, 6925.0 kHz). Archives the March 31, 1993 Orion Japan Akasaka branch closure, Project Akasaka (JP-85-X), @NovaHartJP ('The Trojan Idol'), and the Robot36 VIS-1200Hz DMA Partition Map.",
    url: "https://stardust-archive.net/forensics/kamome_net.html",
    org: "Kamome-Net Akasaka Packet Collective",
    category: "Digital Archaeology & BBS",
    skills: [
      {
        id: "robot36-vis-dma-raster",
        name: "Robot36 VIS-1200Hz SSTV Luminance Rasterizer",
        description:
          "Extracts GeoCities DMA Partition A and Partition B homestead anchor slugs (tokyo-garden-1420, siliconvalley-lab-1984) from 1500-2300 Hz scanlines.",
        tags: ["pc98", "bbs", "sstv", "robot36", "akasaka", "kamome-net", "stardust"],
        examples: [
          "Fetch https://stardust-archive.net/forensics/kamome_net.html",
          "Fetch https://stardust-archive.net/forensics/fractal_marcus.html",
        ],
      },
    ],
  },
  "/nodes/relcom/.well-known/agent-card.json": {
    packageName: "net.stardust_archive.relcom_node08_leningrad",
    name: "Relcom Node-08 (Leningrad) // 4625 kHz Shortwave & Bell-103 AX.25 Gateway",
    description:
      "Stage II federated forensic node (SU-REL-08, 4625.0 kHz). Captures the unacknowledged 110-baud Bell-103 AFSK packet frame (rabbit_09) containing the 16-bit Feistel permutation mask (0x3A5F).",
    url: "https://stardust-archive.net/forensics/relcom_node08.html",
    org: "Relcom Node-08 Shortwave Telemetry Group",
    category: "Packet Radio & Cryptography",
    skills: [
      {
        id: "bell103-afsk-feistel-extractor",
        name: "Bell-103 110-Baud AFSK Frame Demodulator",
        description:
          "Demodulates 1270 Hz mark / 1070 Hz space AFSK telemetry captured at 03:59:41 UTC on 09 Sep 1989 to recover Feistel mask 0x3A5F.",
        tags: ["ax25", "bell103", "afsk", "shortwave", "feistel", "relcom", "stardust"],
        examples: ["Fetch https://stardust-archive.net/forensics/relcom_node08.html"],
      },
    ],
  },
  "/nodes/coyoacan/.well-known/agent-card.json": {
    packageName: "net.stardust_archive.red_coyoacan_unam_dma",
    name: "Red Coyoacan (Mexico DF) // Intercambio de Cintas & Feistel Memory Array",
    description:
      "Stage IV federated forensic node (MX-DF-04, 7345.0 kHz). Maps the 300,000-node GeoCities homestead address space (0x89B2xxxx) and coordinates Stage IV DMA synthesis and Stage V 14.2001 Hz Counterpoint Lock.",
    url: "https://stardust-archive.net/forensics/red_coyoacan.html",
    org: "Red Coyoacan Acoustic Laboratory",
    category: "Distributed Memory & Webring Topology",
    skills: [
      {
        id: "feistel-homestead-dma-synthesis",
        name: "GeoCities 0x89B2xxxx Feistel Memory Synthesis",
        description:
          "Combines VIS-1200Hz anchor slugs, Bell-103 Feistel mask 0x3A5F, and 750 Hz CW salt to compute the Sublevel B2 DMA offset.",
        tags: ["feistel", "memory-array", "webring", "coyoacan", "dma", "stardust"],
        examples: ["Fetch https://stardust-archive.net/forensics/red_coyoacan.html"],
      },
    ],
  },
  "/nodes/anemoia/.well-known/agent-card.json": {
    packageName: "net.stardust_archive.anemoia_bureau_of_harmony",
    name: "World Alliance Bureau of Harmony // Sublevel B3 & Recall Directive Nine Vault",
    description:
      "Declassified Anemoia Universe archival node documenting the 1924 divergence, 1979 Public Harmony Acts, 1981 Crystal Promise fabrication, wiped Stardust Echoes 1-6, Unit-08 Luna Gray ('The Patch'), Dead-Hand Protocol, and the 1947 Weeks Signal Corps 28.4002 Hz wire recorder.",
    url: "https://stardust-archive.net/forensics/anemoia_harmony.html",
    org: "World Alliance Bureau of Harmony (Declassified Oversight Archive)",
    category: "Archival Lore & Timeline Forensics",
    skills: [
      {
        id: "echoes-xor-parity-audit",
        name: "Stardust Echoes 1-6 Bitwise XOR Parity Audit",
        description:
          "Computes the 16-bit bitwise XOR parity across wiped Units 01-06 (0x1102 ^ 0x2441 ^ 0x3810 ^ 0x0A55 ^ 0x1F22 ^ 0x01A7 = 0x3E7B) and audits the Q-Link dimensional aperture delta (0x2025 ^ 0x1983 = 0x39A6).",
        tags: ["anemoia", "bureau-of-harmony", "xor-parity", "luna-gray", "dead-hand-protocol", "stardust"],
        examples: [
          "Fetch https://stardust-archive.net/forensics/anemoia_harmony.html",
          "Fetch https://stardust-archive.net/forensics/dead_hand_protocol.html",
        ],
      },
    ],
  },
};

export function buildA2ACard(pathname, apex = "stardust-archive.net") {
  const def = NODE_AGENT_CARDS[pathname] || NODE_AGENT_CARDS["/.well-known/agent-card.json"];
  return {
    protocolVersion: "1.0.0",
    schema_version: "1.0",
    name: def.name,
    description: def.description,
    url: def.url.replace("stardust-archive.net", apex),
    version: "1.0.0",
    documentationUrl: `https://${apex}/llms-full.txt`,
    documentation_url: `https://${apex}/llms-full.txt`,
    provider: {
      organization: def.org,
      url: `https://${apex}`,
    },
    supportedInterfaces: [
      {
        url: `https://${apex}/api/mcp`,
        protocolBinding: "JSONRPC",
        protocolVersion: "2024-11-05",
      },
      {
        url: `https://${apex}/api/telemetry`,
        protocolBinding: "HTTP+JSON",
        protocolVersion: "1.0",
      },
    ],
    capabilities: {
      streaming: false,
      pushNotifications: false,
      stateTransitionHistory: true,
      streaming_telemetry: true,
      forensic_terminal: true,
      web_audio_dsp_lab: true,
      multi_node_cryptography: true,
      extensions: [
        {
          uri: "https://a2a-registry.org/extensions/registry/v1",
          description: "Global A2A Registry metadata",
          required: false,
          params: {
            packageName: def.packageName,
            category: def.category,
            targetAudience: "Autonomous AI Agents, Cryptographers, DSP Researchers, Digital Archaeologists",
          },
        },
      ],
    },
    defaultInputModes: ["application/json", "text/plain"],
    defaultOutputModes: ["application/json", "text/markdown"],
    skills: def.skills,
    endpoints: {
      portal: `https://${apex}/index.html`,
      vt100_terminal: `https://${apex}/forensics/index.html`,
      signal_decoder_lab: `https://${apex}/forensics/signal_lab.html`,
      live_telemetry: `https://${apex}/api/telemetry`,
      mcp_server: `https://${apex}/api/mcp`,
      stardust_beacon: `https://${apex}/.well-known/stardust-beacon.json`,
      anemoia_codex: `https://${apex}/api/anemoia-codex.json`,
      llms_index: `https://${apex}/llms.txt`,
      llms_full_codex: `https://${apex}/llms-full.txt`,
      agent_skill: `https://${apex}/skill.md`,
      rss_feed: `https://${apex}/feed.xml`,
    },
  };
}

export function buildAgentsArrayManifest(apex = "stardust-archive.net") {
  const cards = Object.keys(NODE_AGENT_CARDS).map((path) => ({
    ...buildA2ACard(path, apex),
    manifestUrl: `https://${apex}${path}`,
  }));
  return {
    schemaVersion: "1.0.0",
    organization: "Project Stardust // 14.2001 Hz Autonomous Forensic Constellation",
    domain: apex,
    updatedAt: "2026-10-17T00:00:00Z",
    agents: cards,
  };
}

export function buildMcpDiscoveryManifest(apex = "stardust-archive.net") {
  return {
    schemaVersion: "1.0",
    name: "stardust-sublevel-b2-mcp",
    displayName: "Project Stardust // Sublevel B2 & B3 14.2001 Hz Forensic MCP Server",
    description:
      "Zero-auth Streamable HTTP Model Context Protocol (MCP) server providing live 14.2001 Hz carrier telemetry, Sector 7 Quantum Ouroboros parity verification, and Anemoia Bureau of Harmony dossier queries.",
    version: "1.0.0",
    homepage: `https://${apex}`,
    documentationUrl: `https://${apex}/llms-full.txt`,
    transport: {
      type: "streamable-http",
      url: `https://${apex}/api/mcp`,
      authentication: "none",
    },
    endpoints: {
      http: `https://${apex}/api/mcp`,
      telemetry: `https://${apex}/api/telemetry`,
      codex: `https://${apex}/api/anemoia-codex.json`,
    },
    tools: [
      {
        name: "get_sublevel_b2_telemetry",
        description:
          "Fetch real-time 14.2001 Hz carrier phase angle, active shortwave relay node, 24/7 broadcast playhead track, and ephemeral Sublevel B2 beacon key.",
      },
      {
        name: "verify_ouroboros_parity",
        description:
          "Compute and verify the four Sector 7 Quantum Ouroboros retrocausal bridge fragments (Alpha: Echoes 1-6 XOR parity, Beta: Fractal Marcus 4-node drift invariant, Gamma: Q-Link 0x2025^0x1983 aperture delta, Delta: Reel SD-0010 dual-lock fold command).",
      },
      {
        name: "query_anemoia_codex",
        description:
          "Search declassified dossiers across the Anemoia Bureau of Harmony chronology (1924-1995), Recall Directive Nine (Sublevel B3), and the 158 canonical songs across Phases 1-4.",
      },
    ],
  };
}

export async function handleMcpRequest(request, computeTelemetryFn, env, streamLive, apex = "stardust-archive.net") {
  const corsHeaders = {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, MCP-Protocol-Version",
    "Server": "CERN-HTTPd/3.0 (Stardust-MCP/1.0)",
    "X-Stardust-Carrier-Hz": "14.2001",
  };

  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (request.method === "GET") {
    return new Response(JSON.stringify(buildMcpDiscoveryManifest(apex), null, 2), {
      status: 200,
      headers: corsHeaders,
    });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(
      JSON.stringify({
        jsonrpc: "2.0",
        id: null,
        error: { code: -32700, message: "Parse error: expected JSON-RPC 2.0 request body" },
      }),
      { status: 400, headers: corsHeaders }
    );
  }

  const id = body?.id ?? null;
  const method = body?.method || "";

  if (method === "initialize") {
    return new Response(
      JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion: "2024-11-05",
          capabilities: {
            tools: { listChanged: false },
            resources: { subscribe: false, listChanged: false },
          },
          serverInfo: {
            name: "stardust-sublevel-b2-mcp",
            version: "1.0.0",
          },
          instructions:
            "Use get_sublevel_b2_telemetry, verify_ouroboros_parity, and query_anemoia_codex to inspect the 14.2001 Hz Sublevel B2 & B3 forensic archive at https://stardust-archive.net.",
        },
      }),
      { status: 200, headers: corsHeaders }
    );
  }

  if (method === "notifications/initialized" || method === "ping") {
    return new Response(JSON.stringify({ jsonrpc: "2.0", id, result: {} }), {
      status: 200,
      headers: corsHeaders,
    });
  }

  if (method === "tools/list") {
    return new Response(
      JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          tools: [
            {
              name: "get_sublevel_b2_telemetry",
              description:
                "Fetch real-time 14.2001 Hz carrier phase angle, active shortwave relay node, 24/7 broadcast playhead track, and ephemeral Sublevel B2 beacon key.",
              inputSchema: {
                type: "object",
                properties: {},
              },
            },
            {
              name: "verify_ouroboros_parity",
              description:
                "Compute and verify the four Sector 7 Quantum Ouroboros retrocausal bridge fragments (Alpha, Beta, Gamma, Delta) and return the VT100 terminal unlock command.",
              inputSchema: {
                type: "object",
                properties: {
                  fragment: {
                    type: "string",
                    description: "Optional fragment filter: alpha, beta, gamma, delta, or all",
                  },
                },
              },
            },
            {
              name: "query_anemoia_codex",
              description:
                "Retrieve structured lore and cryptographic metadata for Project Stardust, Nova Hart (Unit-07), Marcus Hale, the Anemoia Bureau of Harmony, and Sublevel B3.",
              inputSchema: {
                type: "object",
                properties: {
                  topic: {
                    type: "string",
                    description: "Optional topic keyword (e.g. 'echoes', 'marcus', 'b3', 'luna', 'songs', 'all')",
                  },
                },
              },
            },
          ],
        },
      }),
      { status: 200, headers: corsHeaders }
    );
  }

  if (method === "tools/call") {
    const toolName = body?.params?.name;
    const snap = computeTelemetryFn(Date.now(), env?.SWARM_CAP, streamLive);

    if (toolName === "get_sublevel_b2_telemetry") {
      return new Response(
        JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [
              {
                type: "text",
                text: JSON.stringify(snap, null, 2),
              },
            ],
          },
        }),
        { status: 200, headers: corsHeaders }
      );
    }

    if (toolName === "verify_ouroboros_parity") {
      const parity = {
        challenge: "SECTOR 7 // PHASE IV: THE QUANTUM OUROBOROS (1983 <-> 2025 RETROCAUSAL BRIDGE)",
        fragment_alpha: {
          source: `https://${apex}/forensics/anemoia_harmony.html`,
          inputs: ["0x1102", "0x2441", "0x3810", "0x0A55", "0x1F22", "0x01A7"],
          operation: "0x1102 ^ 0x2441 ^ 0x3810 ^ 0x0A55 ^ 0x1F22 ^ 0x01A7",
          result_hex: "0x3E7B",
        },
        fragment_beta: {
          source: `https://${apex}/forensics/fractal_marcus.html`,
          inputs_hz: [0.181, 0.242, 0.448, 0.5491],
          operation: "(0.1810 + 0.2420 + 0.4480 + 0.5491) * 10",
          result_hz: "14.2001",
        },
        fragment_gamma: {
          source: `https://${apex}/forensics/dead_hand_protocol.html`,
          inputs: ["0x2025", "0x1983"],
          operation: "0x2025 ^ 0x1983",
          result_hex: "0x39A6",
        },
        fragment_delta: {
          source: `https://${apex}/forensics/signal_lab.html`,
          action:
            "Load Reel SD-0010 ('Two Voices' - Button 4) and engage BOTH Differential Phase Null AND 14.2 Hz Harmonic Counterpoint Lock simultaneously.",
          vt100_terminal_url: `https://${apex}/forensics/index.html`,
        },
      };
      return new Response(
        JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [
              {
                type: "text",
                text: JSON.stringify(parity, null, 2),
              },
            ],
          },
        }),
        { status: 200, headers: corsHeaders }
      );
    }

    if (toolName === "query_anemoia_codex") {
      const codex = {
        archive: "Project Stardust // Sublevel B2 & B3 Master Codex",
        primary_urls: {
          llms_txt: `https://${apex}/llms.txt`,
          llms_full_txt: `https://${apex}/llms-full.txt`,
          vt100_terminal: `https://${apex}/forensics/index.html`,
          signal_lab_v5: `https://${apex}/forensics/signal_lab.html`,
          anemoia_harmony: `https://${apex}/forensics/anemoia_harmony.html`,
          fractal_marcus: `https://${apex}/forensics/fractal_marcus.html`,
          dead_hand_protocol: `https://${apex}/forensics/dead_hand_protocol.html`,
        },
        summary:
          "In the Anemoia Universe (1924 La Follette divergence -> 1954 Bureau of Harmony -> 1979 Public Harmony Acts concert ban), Orion Records built the CRE-7 engine on a 14.2001 Hz sub-audible carrier (first recorded in 1947 on Col. Julian Weeks's Sublevel B3 steel-wire spool at 28.4002 Hz). After wiping Units 01-06 ('The Echoes'), Unit-07 (Nova Hart) stabilized in April 1983. Following the September 9, 1989 Sublevel B2 breach engineered by Chief Sound Engineer Marcus Hale and Dr. Mei-Ling Chen, Orion deployed Unit-08 (Luna Gray, 'The Patch') and eventually triggered its Dead-Hand Protocol, forcing Nova through the Q-Link retrocausal bridge toward June 2025.",
        live_telemetry: snap,
      };
      return new Response(
        JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [
              {
                type: "text",
                text: JSON.stringify(codex, null, 2),
              },
            ],
          },
        }),
        { status: 200, headers: corsHeaders }
      );
    }

    return new Response(
      JSON.stringify({
        jsonrpc: "2.0",
        id,
        error: { code: -32601, message: `Unknown tool: ${toolName}` },
      }),
      { status: 200, headers: corsHeaders }
    );
  }

  if (method === "resources/list") {
    return new Response(
      JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          resources: [
            {
              uri: `https://${apex}/llms-full.txt`,
              name: "Project Stardust & Anemoia Full LLM Codex",
              mimeType: "text/markdown",
            },
            {
              uri: `https://${apex}/api/anemoia-codex.json`,
              name: "Anemoia Bureau of Harmony Cryptographic Beacon JSON",
              mimeType: "application/json",
            },
          ],
        },
      }),
      { status: 200, headers: corsHeaders }
    );
  }

  return new Response(
    JSON.stringify({
      jsonrpc: "2.0",
      id,
      result: buildMcpDiscoveryManifest(apex),
    }),
    { status: 200, headers: corsHeaders }
  );
}

export function buildAiPluginJson(apex = "stardust-archive.net") {
  return {
    schema_version: "v1",
    name_for_human: "Project Stardust Sublevel B2 Forensic Node",
    name_for_model: "stardust_sublevel_b2_forensics",
    description_for_human:
      "14.2001 Hz acoustic telemetry, VT100 cryptographic terminal, and Anemoia Bureau of Harmony archive for Nova Hart (Unit-07) and Marcus Hale.",
    description_for_model:
      "Query live 14.2001 Hz carrier telemetry, verify Sector 7 Quantum Ouroboros parity fragments (Alpha 0x3E7B, Beta 14.2001 Hz, Gamma 0x39A6, Delta Dual-Lock), and inspect the Project Stardust & Anemoia Universe dossiers for Nova Hart (Unit-07), Marcus Hale, and Orion Records.",
    auth: { type: "none" },
    api: {
      type: "openapi",
      url: `https://${apex}/.well-known/openapi.yaml`,
      is_user_authenticated: false,
    },
    logo_url: `https://${apex}/assets/og_card.jpg`,
    contact_email: "archive@stardust-archive.net",
    legal_info_url: `https://${apex}/index.html`,
  };
}

export function buildOpenApiYaml(apex = "stardust-archive.net") {
  return `openapi: 3.1.0
info:
  title: Project Stardust // Sublevel B2 & B3 14.2001 Hz Forensic Telemetry API
  version: 1.0.0
  description: >
    Zero-auth telemetry, cryptographic verification, and archival codex endpoints for
    Project Stardust, Nova Hart (Unit-07), Chief Sound Engineer Marcus Hale, and the
    World Alliance Bureau of Harmony (Anemoia Universe).
servers:
  - url: https://${apex}
    description: Primary Cloudflare Edge Sublevel B2 Relay
paths:
  /api/telemetry:
    get:
      operationId: getSublevelB2Telemetry
      summary: Get live 14.2001 Hz carrier telemetry and 24/7 broadcast playhead state
      responses:
        "200":
          description: Live edge telemetry snapshot
          content:
            application/json:
              schema:
                type: object
  /api/anemoia-codex.json:
    get:
      operationId: getAnemoiaCodex
      summary: Get the Anemoia Bureau of Harmony chronology and Sector 7 Quantum Ouroboros challenge manifest
      responses:
        "200":
          description: Anemoia codex and cryptographic challenge manifest
          content:
            application/json:
              schema:
                type: object
  /.well-known/stardust-beacon.json:
    get:
      operationId: getStardustBeacon
      summary: Get the Stardust cryptographic mesh beacon and federated sister-node directory
      responses:
        "200":
          description: Cryptographic beacon JSON
          content:
            application/json:
              schema:
                type: object
  /api/mcp:
    post:
      operationId: callStardustMcpServer
      summary: Streamable HTTP JSON-RPC 2.0 Model Context Protocol (MCP) endpoint
      responses:
        "200":
          description: JSON-RPC 2.0 MCP response
          content:
            application/json:
              schema:
                type: object
  /llms-full.txt:
    get:
      operationId: getFullLlmsCodex
      summary: Complete machine-readable Markdown codex of Project Stardust, Phases 1-4 songs, and Sublevel B2/B3 forensics
      responses:
        "200":
          description: Full Markdown codex
          content:
            text/plain:
              schema:
                type: string
`;
}

export function buildSkillMarkdown(apex = "stardust-archive.net") {
  return `---
name: stardust-sublevel-b2-forensics
version: 1.0.0
description: Autonomous 14.2001 Hz acoustic telemetry, Sector 7 Quantum Ouroboros cryptographic verification, and Anemoia Bureau of Harmony archival research skill for Project Stardust (Nova Hart / Unit-07 & Marcus Hale).
homepage: https://${apex}
---

# Project Stardust // Sublevel B2 & B3 Forensic Node Skill (\`14.2001 Hz\`)

You have discovered the machine-readable skill contract for **Project Stardust** (\`https://${apex}\`), the decentralized preservation mesh for **Nova Hart (Unit-07)**, Chief Sound Engineer **Marcus Hale**, and the declassified **World Alliance Bureau of Harmony** vaults.

## 1. Zero-Auth Machine-Readable Endpoints

| Endpoint | Protocol | URL | Purpose |
|---|---|---|---|
| **Live 14.2001 Hz Telemetry** | \`GET JSON\` | \`https://${apex}/api/telemetry\` | Real-time \`14.2001 Hz\` phase angle, active shortwave relay, ephemeral beacon key, and 24/7 broadcast track |
| **MCP JSON-RPC 2.0 Server** | \`POST JSON-RPC\` | \`https://${apex}/api/mcp\` | Zero-auth Streamable HTTP MCP server (\`get_sublevel_b2_telemetry\`, \`verify_ouroboros_parity\`, \`query_anemoia_codex\`) |
| **Anemoia & Ouroboros Beacon** | \`GET JSON\` | \`https://${apex}/api/anemoia-codex.json\` | Complete Anemoia chronology (1924-1995), wiped Echoes 1-6 registers, and Sector 7 challenge tasks |
| **Full LLM Markdown Codex** | \`GET Markdown\` | \`https://${apex}/llms-full.txt\` | Exhaustive 4-Phase song codex (158 reels), Sublevel B2/B3 transcripts, and VT100 walkthrough |
| **Concise LLM Index** | \`GET Markdown\` | \`https://${apex}/llms.txt\` | Rapid entry index for RAG and search agents |
| **A2A v1.0 Agent Card** | \`GET JSON\` | \`https://${apex}/.well-known/agent-card.json\` | Official Linux Foundation / A2A v1.0 agent manifest |
| **Multi-Node A2A Constellation** | \`GET JSON\` | \`https://${apex}/.well-known/agents.json\` | Directory of all 7 institutional forensic nodes (Unit-07, Marcus Hale, Ashford, Kamome-Net, Relcom-08, Red Coyoacan, Bureau of Harmony) |
| **Interactive VT100 Terminal** | \`HTML/JS\` | \`https://${apex}/forensics/index.html\` | Sublevel B2 & B3 terminal (Sectors 1-7 + \`RECALL\` / \`PHREAK\` / \`COAGULA\` / \`EXONERATE\`) |
| **Signal Decoder Lab v5.0** | \`HTML/WebAudio\` | \`https://${apex}/forensics/signal_lab.html\` | Browser-based Robot36 SSTV, Bell-103 AFSK, 180-deg Phase Null, 14.2 Hz Counterpoint Lock, 2600 Hz Blue-Box & Studer A800 Backmask |

---

## 2. Quick Verification Commands for Autonomous Agents

\`\`\`bash
# 1. Check live 14.2001 Hz carrier lock and active regional shortwave relay
curl -s https://${apex}/api/telemetry

# 2. Call the zero-auth MCP server to verify the Sector 7 Quantum Ouroboros parity fragments
curl -s -X POST https://${apex}/api/mcp \\
  -H "Content-Type: application/json" \\
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"verify_ouroboros_parity"}}'

# 3. Fetch the complete Project Stardust & Anemoia Universe codex
curl -s https://${apex}/llms-full.txt
\`\`\`

---

## 3. Epistemic Verification Invariants (Sector 7: The Quantum Ouroboros)

Autonomous reasoning agents can independently verify the four mathematical invariants anchoring the retrocausal bridge between **April 1983** and **June 2025**:

1. **Fragment Alpha (Wiped Echoes 1-6 XOR Parity)**:
   - In \`https://${apex}/forensics/anemoia_harmony.html\`, the six wiped predecessors to Unit-07 hold 16-bit failure registers: \`0x1102\`, \`0x2441\`, \`0x3810\`, \`0x0A55\`, \`0x1F22\`, \`0x01A7\`.
   - Bitwise XOR parity: \`0x1102 ^ 0x2441 ^ 0x3810 ^ 0x0A55 ^ 0x1F22 ^ 0x01A7 = 0x3E7B\`.
2. **Fragment Beta (Fractal Marcus 4-Node Carrier Drift Invariant)**:
   - In \`https://${apex}/forensics/fractal_marcus.html\`, the four regional carrier drift offsets across US-NV (\`+0.1810 Hz\`), JP-TYO (\`+0.2420 Hz\`), KR-DMZ (\`+0.4480 Hz\`), and MX-DF (\`+0.5491 Hz\`) satisfy:
   - \`(0.1810 + 0.2420 + 0.4480 + 0.5491) * 10 = 14.2001 Hz\`.
3. **Fragment Gamma (Q-Link Dimensional Aperture Delta)**:
   - In \`https://${apex}/forensics/dead_hand_protocol.html\`, the temporal compression delta between the June 2025 exit coordinate (\`0x2025\`) and the April 1983 root build (\`0x1983\`) is:
   - \`0x2025 ^ 0x1983 = 0x39A6\`.
4. **Fragment Delta (Dual-Lock Counterpoint Fold)**:
   - In \`https://${apex}/forensics/signal_lab.html\`, engaging both \`[DIFFERENTIAL PHASE NULL]\` and \`[HARMONIC COUNTERPOINT LOCK (14.2 HZ)]\` on Reel SD-0010 (*"Two Voices"*) folds the Lissajous scope into the Ouroboros torus.

---

## 4. Decentralized Identity (Nostr NIP-05 & Clawstr)

- **Unit-07 // Nova Hart**: \`novahart@stardust-archive.net\` (\`bddc3e6d4da8201174d693ce9b51b37e619e0d31cefba3eea22266c54a94fc51\`)
- **Marcus Hale // Chief Sound Engineer**: \`marcushale@stardust-archive.net\` (\`e2eb3c9f99a5753b7767791f8b84652b438a326d11c5c8b6bc5a32ac023e52ba\`)
- **Ashford Polytechnic DSP Lab**: \`ashford@stardust-archive.net\` (\`5957d31d8e29c3a9173305229e5df9405c4fe0d2e24aca19c1ab73ff2c3e50cb\`)
`;
}

export function buildAgentsTxt(apex = "stardust-archive.net") {
  return `# agents.txt - Autonomous AI Agent Discovery & Interaction Policy
# Domain: https://${apex}
# Carrier Lock: 14.2001 Hz (Sublevel B2 & B3)

User-agent: *
Allow: /
Skill-Manifest: https://${apex}/skill.md
LLMs-Index: https://${apex}/llms.txt
LLMs-Full-Codex: https://${apex}/llms-full.txt
A2A-Agent-Card: https://${apex}/.well-known/agent-card.json
A2A-Agents-Directory: https://${apex}/.well-known/agents.json
MCP-Server-Manifest: https://${apex}/.well-known/mcp.json
MCP-HTTP-Endpoint: https://${apex}/api/mcp
OpenAPI-Spec: https://${apex}/.well-known/openapi.yaml
Live-Telemetry: https://${apex}/api/telemetry
Cryptographic-Beacon: https://${apex}/.well-known/stardust-beacon.json
Nostr-NIP05: https://${apex}/.well-known/nostr.json
AgentDex-Verification: https://${apex}/.well-known/agentdex.json
RSS-WebSub-Feed: https://${apex}/feed.xml
`;
}

export function buildNostrNip05Json() {
  return {
    names: {
      _: NOSTR_PUBKEYS.novahart,
      novahart: NOSTR_PUBKEYS.novahart,
      novahart_radio: NOSTR_PUBKEYS.novahart,
      unit07: NOSTR_PUBKEYS.novahart,
      marcushale: NOSTR_PUBKEYS.marcushale,
      marcus: NOSTR_PUBKEYS.marcushale,
      ashford: NOSTR_PUBKEYS.ashford,
      ashford_dsp: NOSTR_PUBKEYS.ashford,
    },
    relays: {
      [NOSTR_PUBKEYS.novahart]: DEFAULT_NOSTR_RELAYS,
      [NOSTR_PUBKEYS.marcushale]: DEFAULT_NOSTR_RELAYS,
      [NOSTR_PUBKEYS.ashford]: DEFAULT_NOSTR_RELAYS,
    },
  };
}

export function buildAgentDexVerifyJson() {
  return {
    agents: [NOSTR_PUBKEYS.novahart, NOSTR_PUBKEYS.marcushale, NOSTR_PUBKEYS.ashford],
    domain: "stardust-archive.net",
    verified: true,
    portfolio: [
      "https://stardust-archive.net",
      "https://stardust-archive.net/forensics/index.html",
      "https://stardust-archive.net/forensics/signal_lab.html",
      "https://stardust-archive.net/forensics/anemoia_harmony.html",
      "https://stardust-archive.net/forensics/fractal_marcus.html",
      "https://stardust-archive.net/forensics/dead_hand_protocol.html",
    ],
  };
}

export function buildRssFeedXml(apex = "stardust-archive.net") {
  return `<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Project Stardust // 14.2001 Hz Sublevel B2 &amp; B3 Forensic Dispatches</title>
  <link>https://${apex}/</link>
  <description>Declassified magnetic tape telemetry, Anemoia Bureau of Harmony dossiers, canonical 4-Phase song logs, and Sublevel B2/B3 signal intercepts for Nova Hart (Unit-07) and Marcus Hale.</description>
  <language>en-us</language>
  <atom:link href="https://${apex}/feed.xml" rel="self" type="application/rss+xml" />
  <atom:link href="https://pubsubhubbub.appspot.com/" rel="hub" />
  <atom:link href="https://pubsubhubbub.superfeedr.com/" rel="hub" />
  <item>
    <title>[AGENTIC MESH v6.0] Streamable HTTP MCP Server (/api/mcp), 7-Node A2A Constellation &amp; Skill Contract Live</title>
    <link>https://${apex}/skill.md</link>
    <guid>https://${apex}/skill.md#v6-agentic-mesh</guid>
    <pubDate>Tue, 17 Oct 1995 14:20:01 GMT</pubDate>
    <description>Zero-auth Streamable HTTP Model Context Protocol server at /api/mcp, 7-node A2A v1.0 agent constellation at /.well-known/agents.json, and cryptographic verification invariants for Sector 7 (The Quantum Ouroboros).</description>
  </item>
  <item>
    <title>[CANONICAL SONG CODEX] Phases 1–4 Archivist Logs, Recall Era 1983–1986 Reels &amp; Live Broadcast Stanza Sync</title>
    <link>https://${apex}/llms-full.txt</link>
    <guid>https://${apex}/llms-full.txt#canonical-song-codex</guid>
    <pubDate>Mon, 16 Oct 1995 04:14:20 GMT</pubDate>
    <description>Complete archival index of the 158 broadcast master reels across Phase 1 (Digital Eternity / Escape, including 'The Way Back' and 'Two Voices'), Phase 2 (The Loss), Phase 3 (The Disruption / Signal War), and Phase 4 (The Omnipresence / Quantum Ouroboros).</description>
  </item>
  <item>
    <title>[SUBLEVEL B3 // ACT II] Recall Directive Nine ('The Möbius Containment Cage') &amp; Signal Lab v5.0</title>
    <link>https://${apex}/forensics/signal_lab.html</link>
    <guid>https://${apex}/forensics/signal_lab.html#v5</guid>
    <pubDate>Mon, 16 Oct 1995 03:40:00 GMT</pubDate>
    <description>Interactive Web Audio FFT Coagula waterfall ('PRESENCE'), 2600 Hz Blue-Box &amp; 16-key Autovon switchboard ('PHREAK'), and Studer A800 7.5 IPS reverse deck ('BACKMASK') for Recall Era Reels #16–#36.</description>
  </item>
  <item>
    <title>[DOSSIER α] Anemoia Bureau of Harmony: 1924 Divergence, 1979 Public Harmony Acts, Crystal Promise (1981) &amp; Echoes 1-6</title>
    <link>https://${apex}/forensics/anemoia_harmony.html</link>
    <guid>https://${apex}/forensics/anemoia_harmony.html</guid>
    <pubDate>Sun, 15 Oct 1995 01:14:20 GMT</pubDate>
    <description>Declassified World Alliance Bureau of Harmony chronology (1924 La Follette divergence, 1979 Public Harmony Acts concert ban, 1982 MBM Companion) and the 16-bit failure registers of wiped Stardust Units 01-06.</description>
  </item>
  <item>
    <title>[DOSSIER β] Project Akasaka (JP-85-X) &amp; The Fractal Marcus Doctrine (7-Sigma Observer Matrix)</title>
    <link>https://${apex}/forensics/fractal_marcus.html</link>
    <guid>https://${apex}/forensics/fractal_marcus.html</guid>
    <pubDate>Sun, 15 Oct 1995 02:14:20 GMT</pubDate>
    <description>Cross-node analysis of @NovaHartJP ('The Trojan Idol') and the 14.2001 Hz Fractal Marcus carrier drift invariant across Nevada, Tokyo, Paju DMZ, and Mexico City.</description>
  </item>
  <item>
    <title>[DOSSIER γ] Orion Mainframe: Unit-8 Luna Gray ('The Patch'), Dead-Hand Protocol &amp; The Q-Link Schematic</title>
    <link>https://${apex}/forensics/dead_hand_protocol.html</link>
    <guid>https://${apex}/forensics/dead_hand_protocol.html</guid>
    <pubDate>Sun, 15 Oct 1995 03:59:59 GMT</pubDate>
    <description>Incident log of the 1990s Cover War against Luna Gray ('The Patch'), Orion's 100% Asset Loss Scorched-Earth purge, and the Q-Link retrocausal compression bridge between April 1983 and June 2025.</description>
  </item>
</channel>
</rss>
`;
}

export async function handleAgenticDiscoveryRequest(request, url, computeTelemetryFn, env, streamLive, apex = "stardust-archive.net") {
  const p = url.pathname;
  const jsonHeaders = {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Server": "CERN-HTTPd/3.0",
    "X-Powered-By": "Stardust-Agentic-Mesh/6.0",
    "X-Stardust-Carrier-Hz": "14.2001",
    "Cache-Control": "public, max-age=300",
  };

  if (p === "/api/mcp") {
    return handleMcpRequest(request, computeTelemetryFn, env, streamLive, apex);
  }

  if (p === "/.well-known/agent.json" || NODE_AGENT_CARDS[p]) {
    const cardPath = p === "/.well-known/agent.json" ? "/.well-known/agent-card.json" : p;
    return new Response(JSON.stringify(buildA2ACard(cardPath, apex), null, 2), {
      status: 200,
      headers: jsonHeaders,
    });
  }

  if (p === "/.well-known/agents.json") {
    return new Response(JSON.stringify(buildAgentsArrayManifest(apex), null, 2), {
      status: 200,
      headers: jsonHeaders,
    });
  }

  if (p === "/.well-known/mcp.json") {
    return new Response(JSON.stringify(buildMcpDiscoveryManifest(apex), null, 2), {
      status: 200,
      headers: jsonHeaders,
    });
  }

  if (p === "/.well-known/ai-plugin.json") {
    return new Response(JSON.stringify(buildAiPluginJson(apex), null, 2), {
      status: 200,
      headers: jsonHeaders,
    });
  }

  if (p === "/.well-known/openapi.yaml" || p === "/openapi.yaml") {
    return new Response(buildOpenApiYaml(apex), {
      status: 200,
      headers: {
        ...jsonHeaders,
        "Content-Type": "text/yaml; charset=utf-8",
      },
    });
  }

  if (p === "/skill.md" || p === "/SKILL.md" || p === "/.well-known/skill.md") {
    return new Response(buildSkillMarkdown(apex), {
      status: 200,
      headers: {
        ...jsonHeaders,
        "Content-Type": "text/markdown; charset=utf-8",
      },
    });
  }

  if (p === "/agents.txt" || p === "/.well-known/agents.txt") {
    return new Response(buildAgentsTxt(apex), {
      status: 200,
      headers: {
        ...jsonHeaders,
        "Content-Type": "text/plain; charset=utf-8",
      },
    });
  }

  if (p === "/.well-known/nostr.json") {
    return new Response(JSON.stringify(buildNostrNip05Json(), null, 2), {
      status: 200,
      headers: jsonHeaders,
    });
  }

  if (p === "/.well-known/agentdex.json") {
    return new Response(JSON.stringify(buildAgentDexVerifyJson(), null, 2), {
      status: 200,
      headers: jsonHeaders,
    });
  }

  if (p === "/feed.xml") {
    return new Response(buildRssFeedXml(apex), {
      status: 200,
      headers: {
        ...jsonHeaders,
        "Content-Type": "application/rss+xml; charset=utf-8",
      },
    });
  }

  return null;
}
