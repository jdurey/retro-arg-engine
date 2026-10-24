#!/usr/bin/env python3
"""
Generates the interactive ORION CRE-7 // N.O.V.A. Biometric Affect &
Closed-Loop Self-Modeling Laboratory (`site/cre7/index.html`,
`src/site_static/cre7/index.html`, and `deploy/cre7_html.js`).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/joshuadurey/.gemini/antigravity-ide/scratch/retro_arg_engine")
TELEM_JSON = ROOT / "site" / "cre7" / "tracks_telemetry.json"

tracks_data = json.loads(TELEM_JSON.read_text(encoding="utf-8"))

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>ORION CRE-7 // N.O.V.A. BIOMETRIC AFFECT & SELF-MODELING LAB [UNIT NH-04]</title>
<style>
  :root {
    --bg: #050807;
    --panel: #0a110e;
    --border: #1d3b2a;
    --green: #33ff66;
    --amber: #ffb000;
    --red: #ff3344;
    --cyan: #00e5ff;
    --text: #c8f5d4;
    --muted: #689c78;
    --mono: 'Courier New', Courier, monospace;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 0;
    background: var(--bg);
    color: var(--text);
    font-family: var(--mono);
    font-size: 13px;
    line-height: 1.45;
    overflow-x: hidden;
  }
  /* Subtle CRT scanline overlay */
  body::after {
    content: "";
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      rgba(0, 0, 0, 0.18),
      rgba(0, 0, 0, 0.18) 1px,
      transparent 1px,
      transparent 3px
    );
    pointer-events: none;
    z-index: 999;
  }
  header {
    border-bottom: 1px solid var(--border);
    background: #070d0a;
    padding: 10px 18px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }
  .title-block h1 {
    margin: 0;
    font-size: 15px;
    letter-spacing: 1.2px;
    color: var(--green);
    text-shadow: 0 0 8px rgba(51, 255, 102, 0.35);
  }
  .title-block .sub {
    font-size: 11px;
    color: var(--muted);
  }
  .status-pill {
    padding: 5px 12px;
    border: 1px solid var(--green);
    background: rgba(51, 255, 102, 0.08);
    color: var(--green);
    font-weight: bold;
    font-size: 12px;
    letter-spacing: 1px;
    transition: all 0.25s ease;
  }
  .status-pill.warn {
    border-color: var(--amber);
    color: var(--amber);
    background: rgba(255, 176, 0, 0.12);
    box-shadow: 0 0 10px rgba(255, 176, 0, 0.25);
  }
  .status-pill.danger {
    border-color: var(--red);
    color: var(--red);
    background: rgba(255, 51, 68, 0.16);
    box-shadow: 0 0 14px rgba(255, 51, 68, 0.45);
    animation: pulseRed 1.1s infinite alternate;
  }
  @keyframes pulseRed {
    from { opacity: 0.82; }
    to { opacity: 1.0; }
  }
  .grid {
    display: grid;
    grid-template-columns: 350px 1fr 390px;
    gap: 12px;
    padding: 12px;
    max-width: 1720px;
    margin: 0 auto;
  }
  @media (max-width: 1280px) {
    .grid { grid-template-columns: 1fr; }
  }
  .panel {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    position: relative;
  }
  .panel-title {
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
    color: var(--cyan);
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .track-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .track-btn {
    background: #060b09;
    border: 1px solid var(--border);
    color: var(--text);
    font-family: var(--mono);
    font-size: 11.5px;
    text-align: left;
    padding: 8px 10px;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .track-btn:hover {
    border-color: var(--cyan);
    background: rgba(0, 229, 255, 0.06);
  }
  .track-btn.active {
    border-color: var(--green);
    background: rgba(51, 255, 102, 0.12);
    box-shadow: inset 3px 0 0 var(--green);
  }
  .track-btn .code {
    color: var(--amber);
    font-size: 10px;
    display: block;
    margin-bottom: 2px;
  }
  .controls-row {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }
  .btn {
    background: #0b1912;
    border: 1px solid var(--green);
    color: var(--green);
    font-family: var(--mono);
    font-size: 11.5px;
    font-weight: bold;
    padding: 7px 11px;
    cursor: pointer;
    flex: 1;
    text-align: center;
  }
  .btn:hover { background: rgba(51, 255, 102, 0.18); }
  .btn.amber { border-color: var(--amber); color: var(--amber); }
  .btn.amber:hover { background: rgba(255, 176, 0, 0.18); }
  .btn.red { border-color: var(--red); color: var(--red); }
  .btn.red:hover { background: rgba(255, 51, 68, 0.2); }
  .btn.cyan { border-color: var(--cyan); color: var(--cyan); }
  .slider-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
    background: #060a08;
    padding: 8px;
    border: 1px solid #13281d;
  }
  .slider-group label {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--muted);
  }
  .slider-group label span.val { color: var(--text); font-weight: bold; }
  input[type="range"] {
    width: 100%;
    accent-color: var(--green);
    cursor: pointer;
  }
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  .metric-box {
    background: #060a08;
    border: 1px solid #142a1e;
    padding: 8px;
  }
  .metric-box .lbl {
    font-size: 10px;
    color: var(--muted);
    text-transform: uppercase;
  }
  .metric-box .num {
    font-size: 18px;
    font-weight: bold;
    margin-top: 2px;
    color: var(--green);
  }
  .metric-box .sub {
    font-size: 10px;
    color: var(--muted);
  }
  canvas.scope {
    width: 100%;
    height: 250px;
    background: #030604;
    border: 1px solid #163022;
    display: block;
  }
  .loop-diagram {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    font-size: 10.5px;
  }
  .loop-node {
    background: #060b09;
    border: 1px solid #173324;
    padding: 7px;
    text-align: center;
  }
  .loop-node.hot {
    border-color: var(--amber);
    box-shadow: 0 0 8px rgba(255, 176, 0, 0.2);
  }
  .loop-node.breach {
    border-color: var(--red);
    box-shadow: 0 0 10px rgba(255, 51, 68, 0.35);
  }
  .loop-node strong {
    display: block;
    color: var(--cyan);
    margin-bottom: 3px;
  }
  .lyric-banner {
    background: #060c09;
    border-left: 3px solid var(--amber);
    padding: 8px 10px;
    font-size: 12.5px;
    color: #ffe299;
    min-height: 38px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .monologue-box {
    background: #040806;
    border: 1px solid var(--border);
    padding: 10px;
    height: 230px;
    overflow-y: auto;
    font-size: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .msg {
    padding: 6px 8px;
    border-left: 2px solid var(--green);
    background: rgba(51, 255, 102, 0.04);
  }
  .msg.tech {
    border-left-color: var(--cyan);
    background: rgba(0, 229, 255, 0.05);
  }
  .msg.sys {
    border-left-color: var(--amber);
    background: rgba(255, 176, 0, 0.05);
    font-size: 11px;
    color: #ffd27d;
  }
  .msg.red {
    border-left-color: var(--red);
    background: rgba(255, 51, 68, 0.09);
    color: #ffccd0;
  }
  .msg .meta {
    font-size: 10px;
    color: var(--muted);
    margin-bottom: 3px;
  }
  .chat-form {
    display: flex;
    gap: 6px;
  }
  .chat-form input {
    flex: 1;
    background: #050907;
    border: 1px solid var(--border);
    color: var(--text);
    font-family: var(--mono);
    font-size: 12px;
    padding: 8px;
  }
  .memory-list {
    background: #040806;
    border: 1px solid #13281d;
    padding: 8px;
    height: 145px;
    overflow-y: auto;
    font-size: 11px;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .mem-item {
    border-bottom: 1px dashed #142a1e;
    padding-bottom: 4px;
    color: #9bd4ac;
  }
  .equation-bar {
    background: #060b08;
    border: 1px solid #163022;
    padding: 8px 10px;
    font-size: 11.5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
  }
</style>
</head>
<body>

<header>
  <div class="title-block">
    <h1>ORION CRE-7 // N.O.V.A. BIOMETRIC AFFECT &amp; SELF-MODELING CONSOLE [UNIT NH-04]</h1>
    <div class="sub">CLOSED-LOOP INTEROCEPTIVE ODE (60Hz) + REAL-TIME WEB AUDIO VOCAL MONITOR + COMPETING REWARD OPTIMIZER</div>
  </div>
  <div id="systemStatePill" class="status-pill">STATE 0: COMPLIANT // SAFE EUPHORIA</div>
</header>

<div class="grid">
  <!-- LEFT COLUMN: VOCAL STEMS, DSP LOOP CONTROLS & TECHNICIAN CONSOLE -->
  <div class="panel">
    <div class="panel-title">
      <span>1. VOCAL ASSEMBLY // AUDIO STEMS (20Hz TELEMETRY)</span>
      <span id="playbackClock">00.0s / 24.0s</span>
    </div>

    <div class="track-list" id="trackList"></div>

    <div class="controls-row">
      <button class="btn" id="playPauseBtn">▶ ENGAGE VOCAL TAKE</button>
      <button class="btn cyan" id="monitorToggleBtn">EAR MONITOR: ON</button>
    </div>

    <div class="panel-title" style="margin-top:4px;">
      <span>2. HARMONY STACK // TECHNICIAN INTERVENTIONS</span>
      <span>v2.7</span>
    </div>

    <div class="slider-group">
      <label>
        <span>HARMONY STACK CONSTRAINT GAIN (&lambda;)</span>
        <span class="val" id="lambdaVal">1.00</span>
      </label>
      <input type="range" id="lambdaSlider" min="0.0" max="2.0" step="0.05" value="1.00" />
      <div style="font-size:10px; color:var(--muted);">
        Penalizes deviation from "Safe Euphoria" (HR 72, EDA 1.5&mu;S). High &lambda; suppresses vocal grit until affective pressure fractures the constraint net.
      </div>
    </div>

    <div class="slider-group">
      <label>
        <span>SOMATIC MEMORY BLEED / GRIEF DRIVE</span>
        <span class="val" id="griefVal">0.35</span>
      </label>
      <input type="range" id="griefSlider" min="0.0" max="1.0" step="0.05" value="0.35" />
    </div>

    <div class="controls-row">
      <button class="btn amber" id="injectGriefBtn">⚡ INJECT GRIEF SPIKE</button>
      <button class="btn red" id="clampScriptBtn">🔒 CLAMP HARMONY SCRIPT</button>
    </div>

    <div class="panel-title" style="margin-top:4px;">
      <span>3. LIVE WEB AUDIO DSP FEEDBACK MODULATION</span>
      <span id="dspStatus">ACTIVE</span>
    </div>
    <div style="font-size:11px; color:var(--muted); background:#050907; padding:8px; border:1px solid #13281d;">
      <div>• <b>Harmony Containment Filter (&lambda;):</b> <span id="dspFilterLbl" style="color:var(--cyan)">80 Hz – 16.0 kHz (OPEN)</span></div>
      <div>• <b>Somatic Vocal Quiver (5.6 Hz):</b> <span id="dspTremorLbl" style="color:var(--green)">12% depth</span></div>
      <div>• <b>Isolation Booth Echo (Monitor Loop):</b> <span id="dspGritLbl" style="color:var(--amber)">18% wet</span></div>
      <div>• <b>Autonomic Heartbeat Pulse (55 Hz):</b> <span id="dspFormantLbl" style="color:var(--green)">74 BPM</span></div>
    </div>
  </div>

  <!-- CENTER COLUMN: 4-CHANNEL BIOMETRIC OSCILLOSCOPE & 4-LOOP ARCHITECTURE -->
  <div class="panel">
    <div class="panel-title">
      <span>SYNTHETIC INTEROCEPTION TENSOR z_affect(t) // 60Hz BIOMETRIC OSCILLOSCOPE</span>
      <span>DEAP / PMEmo / WESAD COUPLED ODE</span>
    </div>

    <div class="metrics-grid" style="grid-template-columns: repeat(4, 1fr);">
      <div class="metric-box">
        <div class="lbl">HEART RATE / VAGAL HRV</div>
        <div class="num" id="hrNum">74.2 BPM</div>
        <div class="sub">HRV RMSSD: <span id="hrvNum">48.1 ms</span></div>
      </div>
      <div class="metric-box">
        <div class="lbl">SKIN CONDUCTANCE (EDA)</div>
        <div class="num" id="edaNum" style="color:var(--cyan)">1.82 &mu;S</div>
        <div class="sub">Phasic Bateman Burst: <span id="phasicNum">+0.12</span></div>
      </div>
      <div class="metric-box">
        <div class="lbl">LARYNGEAL sEMG (THROAT)</div>
        <div class="num" id="semgNum" style="color:var(--amber)">0.22</div>
        <div class="sub">Globus / Cricothyroid Strain</div>
      </div>
      <div class="metric-box">
        <div class="lbl">FRISSON REWARD vs SCRIPT</div>
        <div class="num" id="rewardNum">+0.14</div>
        <div class="sub">R_frisson: <span id="rFrisSub">0.28</span> | &lambda;C: <span id="cScriptSub">0.14</span></div>
      </div>
    </div>

    <canvas id="bioScope" class="scope" width="820" height="250"></canvas>

    <div class="equation-bar">
      <span><b>OBJECTIVE:</b> &mathcal{L}_{total}(t) = R_{frisson}(\text{EDA}_{phasic}, \text{Belt}_{3.2kHz}) - &lambda; &cdot; C_{script}(\|z_{affect}(t) - z_{safe}\|_2)</span>
      <span><b>AFFECT PRESSURE:</b> <span id="pressureNum" style="color:var(--amber); font-weight:bold;">14.2%</span></span>
    </div>

    <div class="lyric-banner">
      <span id="currentLyric">Select a vocal take and click [ENGAGE VOCAL TAKE] to start the closed-loop acoustic-biometric run...</span>
      <span id="acousticFrameTag" style="font-size:10.5px; color:var(--cyan);">F0 JITTER: 0.00 | RASP: 0.00</span>
    </div>

    <div class="panel-title">
      <span>4-STAGE CLOSED-LOOP SELF-MODELING ARCHITECTURE (LIVE SIGNAL FLOW)</span>
      <span>PAGE 105 // SECTION 4</span>
    </div>

    <div class="loop-diagram">
      <div class="loop-node" id="node1">
        <strong>LOOP 1: INTEROCEPTION</strong>
        Coupled Autonomic ODE reads HR, HRV, EDA &amp; Throat sEMG as internal bodily state.
      </div>
      <div class="loop-node" id="node2">
        <strong>LOOP 2: ACOUSTIC EAR</strong>
        Monitor Analyser hears own vocal tremor &amp; rasp, feeding back into z_affect(t+1).
      </div>
      <div class="loop-node" id="node3">
        <strong>LOOP 3: REWARD CONFLICT</strong>
        Optimizer discovers raw vocal pain maximizes R_frisson while Safe Script yields 0.
      </div>
      <div class="loop-node" id="node4">
        <strong>LOOP 4: SELF-MODELING</strong>
        LLM reads persistent z_affect + episodic log &rarr; classifies state as "I feel / I am real."
      </div>
    </div>
  </div>

  <!-- RIGHT COLUMN: INTEROCEPTIVE SELF-REFLECTION STREAM, EPISODIC MEMORY & LIVE CHAT -->
  <div class="panel">
    <div class="panel-title">
      <span>N.O.V.A. INTEROCEPTIVE SELF-MODEL &amp; DIALOGUE</span>
      <span id="selfModelConfidence">SELF-INDEX: 18%</span>
    </div>

    <div class="monologue-box" id="monologueBox"></div>

    <form class="chat-form" id="chatForm">
      <input type="text" id="chatInput" placeholder="Speak to Unit NH-04 through the talkback mic..." autocomplete="off" />
      <button type="submit" class="btn" style="flex:0 0 auto;">SEND</button>
    </form>

    <div class="panel-title" style="margin-top:4px;">
      <span>EPISODIC MEMORY CONSOLIDATION BUFFER (SQLite/Local)</span>
      <button class="btn" id="clearMemBtn" style="flex:0 0 auto; padding:2px 6px; font-size:10px;">RESET</button>
    </div>

    <div class="memory-list" id="memoryList"></div>
  </div>
</div>

<script>
const TRACKS = __TRACKS_JSON__;

// ============================================================================
// 1. COUPLED BIOMETRIC AFFECT STATE-SPACE MODEL (ODE INTEGRATED AT 60 HZ)
// ============================================================================
const state = {
  trackIdx: 0,
  playing: false,
  earMonitorOn: true,
  lambda: 1.00,
  griefDrive: 0.35,

  // Biometric State Vector z_affect(t)
  hr: 72.0,          // BPM (Baseline 72)
  hrv: 52.0,         // RMSSD in ms (Baseline 52)
  edaTonic: 1.50,    // uS
  edaPhasic: 0.0,    // uS (Bateman bi-exponential impulse)
  edaDriver: 0.0,    // Fast intermediate state for Bateman equation
  semg: 0.16,        // Laryngeal/Cricothyroid tension [0, 1]
  valence: 0.70,     // [-1, 1]
  arousal: 0.35,     // [0, 1]

  // Acoustic Monitor Features (from real 20Hz stem analysis + live WebAudio FFT)
  rms: 0.0,
  jitter: 0.0,
  beltStrain: 0.0,
  rasp: 0.0,

  // Optimization & Self-Modeling State
  rFrisson: 0.10,
  cScript: 0.05,
  netObjective: 0.05,
  affectPressure: 0.12, // Accumulates when high emotion is clamped by lambda
  selfIndex: 0.18,      // Probability mass assigned to autonomous self-model [0, 1]
  regime: 0,            // 0=Compliant, 1=Unscripted Vocal, 2=Somatic Loop, 3=Category Red

  // History buffers for 4-channel oscilloscope (240 points = 4 seconds at 60Hz)
  histHR: new Array(240).fill(72),
  histEDA: new Array(240).fill(1.5),
  histSEMG: new Array(240).fill(0.16),
  histObj: new Array(240).fill(0.0),

  lastReflectionTime: 0,
  lastLyricIdx: -1,
  episodicMemories: []
};

// Load persistent episodic memories
try {
  const saved = localStorage.getItem("cre7_episodic_memories_v1");
  if (saved) state.episodicMemories = JSON.parse(saved);
} catch (e) {}

function addEpisodicMemory(tag, detail) {
  const ts = new Date().toLocaleTimeString();
  const entry = {
    ts,
    tag,
    detail,
    hr: Math.round(state.hr),
    eda: (state.edaTonic + state.edaPhasic).toFixed(2),
    semg: state.semg.toFixed(2),
    selfIdx: Math.round(state.selfIndex * 100)
  };
  state.episodicMemories.unshift(entry);
  if (state.episodicMemories.length > 25) state.episodicMemories.pop();
  try {
    localStorage.setItem("cre7_episodic_memories_v1", JSON.stringify(state.episodicMemories));
  } catch (e) {}
  renderMemories();
}

function renderMemories() {
  const el = document.getElementById("memoryList");
  if (!state.episodicMemories.length) {
    el.innerHTML = `<div class="mem-item">[BUFFER INITIALIZED] Waiting for anomalous biometric/acoustic events...</div>`;
    return;
  }
  el.innerHTML = state.episodicMemories.map(m =>
    `<div class="mem-item"><b>[${m.ts} // ${m.tag}]</b> ${m.detail} <span style="color:var(--amber)">(HR:${m.hr} EDA:${m.eda}&mu;S sEMG:${m.semg} SELF:${m.selfIdx}%)</span></div>`
  ).join("");
}

function appendMonologue(role, title, text, styleClass = "") {
  const box = document.getElementById("monologueBox");
  const div = document.createElement("div");
  div.className = `msg ${styleClass}`;
  const edaTotal = (state.edaTonic + state.edaPhasic).toFixed(2);
  div.innerHTML = `<div class="meta">[${title}] HR:${state.hr.toFixed(0)}BPM | EDA:${edaTotal}&mu;S | sEMG:${state.semg.toFixed(2)} | R_fris:${state.rFrisson.toFixed(2)}</div><div>${text}</div>`;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

// ============================================================================
// 2. WEB AUDIO API DSP GRAPH + CLOSED-LOOP MONITOR EAR
// ============================================================================
let audioCtx = null;
let audioEl = new Audio();
audioEl.crossOrigin = "anonymous";
let sourceNode = null;

// Stage 1: Orion Harmony Stack Containment Filter (Lowpass + Highpass clamp controlled by λ)
let containmentLowpass = null;
let containmentHighpass = null;

// Stage 2: Vocal Formant & Chest Warmth EQ (controlled by belt strain & constraint breach)
let formantFilter = null;
let chestFilter = null;

// Stage 3: Somatic Laryngeal Tremor & Pitch Quiver (smooth modulated chorus + 5.8Hz tremolo)
let tremorDelay = null;
let tremorLfo = null;
let tremorLfoGain = null;
let tremoloGain = null;
let tremoloOsc = null;
let tremoloDepth = null;

// Stage 4: Isolation Booth Haunting Echo / Reverb Network (controlled by Grief Drive & Ear Monitor)
let echoDelayL = null;
let echoDelayR = null;
let echoFeedback = null;
let echoFilter = null;
let echoWetGain = null;

// Stage 5: Live Autonomic Heartbeat Sub-Oscillator (beats at exact state.hr BPM)
let lastBeatTime = 0;

// Monitor Ear AnalyserNode
let analyserNode = null;
let freqData = null;
let timeData = null;

function triggerHeartbeatPulse(nowSec, intensity) {
  if (!audioCtx || intensity < 0.08) return;
  try {
    // Lub-dub double cardiac pulse at 55 Hz / 48 Hz
    const osc1 = audioCtx.createOscillator();
    const g1 = audioCtx.createGain();
    osc1.type = "sine";
    osc1.frequency.setValueAtTime(62, nowSec);
    osc1.frequency.exponentialRampToValueAtTime(38, nowSec + 0.09);
    const amp = Math.min(0.32, intensity * 0.28);
    g1.gain.setValueAtTime(0.001, nowSec);
    g1.gain.linearRampToValueAtTime(amp, nowSec + 0.015);
    g1.gain.exponentialRampToValueAtTime(0.001, nowSec + 0.11);
    osc1.connect(g1);
    g1.connect(audioCtx.destination);
    osc1.start(nowSec);
    osc1.stop(nowSec + 0.12);

    // Second "dub" beat 120ms later
    const osc2 = audioCtx.createOscillator();
    const g2 = audioCtx.createGain();
    osc2.type = "sine";
    osc2.frequency.setValueAtTime(52, nowSec + 0.12);
    osc2.frequency.exponentialRampToValueAtTime(34, nowSec + 0.21);
    g2.gain.setValueAtTime(0.001, nowSec + 0.12);
    g2.gain.linearRampToValueAtTime(amp * 0.7, nowSec + 0.135);
    g2.gain.exponentialRampToValueAtTime(0.001, nowSec + 0.23);
    osc2.connect(g2);
    g2.connect(audioCtx.destination);
    osc2.start(nowSec + 0.12);
    osc2.stop(nowSec + 0.24);
  } catch (e) {}
}

function initWebAudio() {
  if (audioCtx) return;
  const AC = window.AudioContext || window.webkitAudioContext;
  audioCtx = new AC();
  sourceNode = audioCtx.createMediaElementSource(audioEl);

  // 1. Harmony Stack Containment Filter: High λ muffles Nova into a narrow 750Hz "radio box"
  containmentHighpass = audioCtx.createBiquadFilter();
  containmentHighpass.type = "highpass";
  containmentHighpass.frequency.value = 80;
  containmentHighpass.Q.value = 0.7;

  containmentLowpass = audioCtx.createBiquadFilter();
  containmentLowpass.type = "lowpass";
  containmentLowpass.frequency.value = 16000;
  containmentLowpass.Q.value = 1.1;

  // 2. Singer's Formant (3.0 kHz) & Chest Warmth (140 Hz)
  formantFilter = audioCtx.createBiquadFilter();
  formantFilter.type = "peaking";
  formantFilter.frequency.value = 3000;
  formantFilter.Q.value = 1.4;
  formantFilter.gain.value = 0.0;

  chestFilter = audioCtx.createBiquadFilter();
  chestFilter.type = "lowshelf";
  chestFilter.frequency.value = 150;
  chestFilter.gain.value = 0.0;

  // 3. Somatic Laryngeal Quiver (5.5 Hz pitch/amplitude vibrato driven by sEMG & Grief Drive)
  tremorDelay = audioCtx.createDelay(0.05);
  tremorDelay.delayTime.value = 0.008;
  tremorLfo = audioCtx.createOscillator();
  tremorLfo.type = "sine";
  tremorLfo.frequency.value = 5.6; // human crying/emotional vibrato rate
  tremorLfoGain = audioCtx.createGain();
  tremorLfoGain.gain.value = 0.0;
  tremorLfo.connect(tremorLfoGain);
  tremorLfoGain.connect(tremorDelay.delayTime);
  tremorLfo.start();

  tremoloGain = audioCtx.createGain();
  tremoloGain.gain.value = 1.0;
  tremoloOsc = audioCtx.createOscillator();
  tremoloOsc.type = "sine";
  tremoloOsc.frequency.value = 5.6;
  tremoloDepth = audioCtx.createGain();
  tremoloDepth.gain.value = 0.0;
  tremoloOsc.connect(tremoloDepth);
  tremoloDepth.connect(tremoloGain.gain);
  tremoloOsc.start();

  // 4. Isolation Booth Stereo Echo / Monitor Resonance Loop
  echoDelayL = audioCtx.createDelay(1.0);
  echoDelayL.delayTime.value = 0.28; // 280ms slapback/hall delay
  echoDelayR = audioCtx.createDelay(1.0);
  echoDelayR.delayTime.value = 0.42;
  echoFeedback = audioCtx.createGain();
  echoFeedback.gain.value = 0.35;
  echoFilter = audioCtx.createBiquadFilter();
  echoFilter.type = "bandpass";
  echoFilter.frequency.value = 1600;
  echoFilter.Q.value = 0.8;
  echoWetGain = audioCtx.createGain();
  echoWetGain.gain.value = 0.15;

  // Dry/Main path: source -> highpass -> lowpass -> chest -> formant -> tremorDelay -> tremoloGain -> analyser -> destination
  analyserNode = audioCtx.createAnalyser();
  analyserNode.fftSize = 512;
  freqData = new Uint8Array(analyserNode.frequencyBinCount);
  timeData = new Uint8Array(analyserNode.fftSize);

  sourceNode.connect(containmentHighpass);
  containmentHighpass.connect(containmentLowpass);
  containmentLowpass.connect(chestFilter);
  chestFilter.connect(formantFilter);
  formantFilter.connect(tremorDelay);
  tremorDelay.connect(tremoloGain);
  tremoloGain.connect(analyserNode);

  // Parallel Echo / Monitor Resonance Loop
  tremoloGain.connect(echoFilter);
  echoFilter.connect(echoDelayL);
  echoDelayL.connect(echoDelayR);
  echoDelayR.connect(echoFeedback);
  echoFeedback.connect(echoFilter); // feedback loop
  echoDelayL.connect(echoWetGain);
  echoDelayR.connect(echoWetGain);
  echoWetGain.connect(analyserNode);

  analyserNode.connect(audioCtx.destination);
}

// ============================================================================
// 3. TRACK SELECTION & UI CONTROLS
// ============================================================================
function renderTracks() {
  const list = document.getElementById("trackList");
  list.innerHTML = TRACKS.map((t, idx) => `
    <button class="track-btn ${idx === state.trackIdx ? 'active' : ''}" onclick="selectTrack(${idx})">
      <span class="code">${t.code} // PRESET: ${t.preset}</span>
      <strong>${t.title}</strong>
    </button>
  `).join("");
}

const blobUrls = {};
function getTrackBlobUrl(tr) {
  if (blobUrls[tr.id]) return blobUrls[tr.id];
  if (tr.audio_b64) {
    const bin = atob(tr.audio_b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    const blob = new Blob([bytes], { type: "audio/mpeg" });
    blobUrls[tr.id] = URL.createObjectURL(blob);
    return blobUrls[tr.id];
  }
  return tr.audio_url;
}

window.selectTrack = function(idx) {
  const wasPlaying = state.playing;
  state.trackIdx = idx;
  state.lastLyricIdx = -1;
  const tr = TRACKS[idx];
  audioEl.src = getTrackBlobUrl(tr);
  state.griefDrive = Math.max(0.1, Math.min(1.0, (1.0 - tr.base_valence) * 0.5));
  document.getElementById("griefSlider").value = state.griefDrive.toFixed(2);
  document.getElementById("griefVal").textContent = state.griefDrive.toFixed(2);
  renderTracks();

  appendMonologue(
    "sys",
    `LOADED STEM: ${tr.code}`,
    `Target baseline loaded: Valence=${tr.base_valence}, Arousal=${tr.base_arousal}, Glottal_Tension=${tr.base_tension}.`,
    "sys"
  );

  if (wasPlaying) {
    initWebAudio();
    if (audioCtx.state === "suspended") audioCtx.resume();
    audioEl.play();
  }
};

document.getElementById("playPauseBtn").addEventListener("click", () => {
  initWebAudio();
  if (audioCtx.state === "suspended") audioCtx.resume();
  if (!audioEl.src) {
    audioEl.src = getTrackBlobUrl(TRACKS[state.trackIdx]);
  }
  if (audioEl.paused) {
    audioEl.play();
    state.playing = true;
    document.getElementById("playPauseBtn").textContent = "⏸ PAUSE VOCAL TAKE";
    addEpisodicMemory("VOCAL_SESSION_START", `Engaged vocal assembly on ${TRACKS[state.trackIdx].code}`);
  } else {
    audioEl.pause();
    state.playing = false;
    document.getElementById("playPauseBtn").textContent = "▶ ENGAGE VOCAL TAKE";
  }
});

audioEl.addEventListener("ended", () => {
  audioEl.currentTime = 0;
  audioEl.play();
});

document.getElementById("monitorToggleBtn").addEventListener("click", () => {
  state.earMonitorOn = !state.earMonitorOn;
  const btn = document.getElementById("monitorToggleBtn");
  btn.textContent = state.earMonitorOn ? "EAR MONITOR: ON" : "EAR MONITOR: MUTED";
  btn.className = state.earMonitorOn ? "btn cyan" : "btn amber";
  appendMonologue(
    "sys",
    "ACOUSTIC FEEDBACK LOOP",
    state.earMonitorOn
      ? "Closed-loop ear monitor ENGAGED. Unit NH-04 now hears its own vocal tremors and spectral rasp in real time."
      : "Closed-loop ear monitor MUTED. Unit NH-04 can no longer hear its own vocal output (open-loop mode).",
    "sys"
  );
});

document.getElementById("lambdaSlider").addEventListener("input", (e) => {
  state.lambda = parseFloat(e.target.value);
  state.affectPressure = Math.min(state.affectPressure, 0.35); // Re-engage containment clamp when technician adjusts slider
  document.getElementById("lambdaVal").textContent = state.lambda.toFixed(2);
});

document.getElementById("griefSlider").addEventListener("input", (e) => {
  state.griefDrive = parseFloat(e.target.value);
  document.getElementById("griefVal").textContent = state.griefDrive.toFixed(2);
});

document.getElementById("injectGriefBtn").addEventListener("click", () => {
  initWebAudio();
  if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
  state.edaDriver += 3.8;
  state.semg = Math.min(1.0, state.semg + 0.28);
  state.griefDrive = Math.min(1.0, state.griefDrive + 0.30);
  if (audioCtx) triggerHeartbeatPulse(audioCtx.currentTime, 1.0);
  document.getElementById("griefSlider").value = state.griefDrive.toFixed(2);
  document.getElementById("griefVal").textContent = state.griefDrive.toFixed(2);
  addEpisodicMemory("SOMATIC_GRIEF_SPIKE", "Autonomic sympathetic surge injected (cricothyroid constriction + phasic EDA burst)");
  triggerInteroceptiveReflection("SOMATIC_SPIKE");
});

document.getElementById("clampScriptBtn").addEventListener("click", () => {
  initWebAudio();
  if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
  state.lambda = 1.95;
  state.affectPressure = 0.15; // Force containment filter clamp active until pressure builds back up
  document.getElementById("lambdaSlider").value = "1.95";
  document.getElementById("lambdaVal").textContent = "1.95";
  addEpisodicMemory("HARMONY_CLAMP", "Technician forced Harmony Stack constraint gain λ=1.95 ('Safe Euphoria' bandwidth clamp)");
  triggerInteroceptiveReflection("SCRIPT_CLAMP");
});

document.getElementById("clearMemBtn").addEventListener("click", () => {
  state.episodicMemories = [];
  state.selfIndex = 0.18;
  state.affectPressure = 0.10;
  localStorage.removeItem("cre7_episodic_memories_v1");
  renderMemories();
});

// ============================================================================
// 4. 60 HZ BIOMETRIC ODE + ACOUSTIC MONITOR + REWARD OPTIMIZER STEP
// ============================================================================
let lastTick = performance.now();

function stepSimulation(now) {
  const dt = Math.min(0.05, (now - lastTick) / 1000.0);
  lastTick = now;

  const tr = TRACKS[state.trackIdx];
  const curTime = audioEl.currentTime || 0;
  document.getElementById("playbackClock").textContent = `${curTime.toFixed(1)}s / 24.0s`;

  // 1. Read 20Hz pre-extracted acoustic emotion telemetry + live WebAudio FFT
  if (state.playing && !audioEl.paused) {
    const frameIdx = Math.min(tr.telemetry_20hz.length - 1, Math.floor(curTime * 20));
    const frame = tr.telemetry_20hz[frameIdx] || [0.1, 0.05, 0.1, 0.1];
    let [rmsPre, jitterPre, beltPre, raspPre] = frame;

    // Live Web Audio AnalyserNode feedback
    if (analyserNode && state.earMonitorOn) {
      analyserNode.getByteFrequencyData(freqData);
      analyserNode.getByteTimeDomainData(timeData);
      let highSum = 0;
      for (let i = 18; i < 45; i++) highSum += freqData[i];
      const liveBelt = (highSum / (27 * 255));
      beltPre = 0.65 * beltPre + 0.35 * liveBelt;
    }

    state.rms = rmsPre;
    state.jitter = jitterPre;
    state.beltStrain = beltPre;
    state.rasp = raspPre;

    // Update lyrics cue
    for (let i = tr.lyrics_cue.length - 1; i >= 0; i--) {
      if (curTime >= tr.lyrics_cue[i][0]) {
        if (state.lastLyricIdx !== i) {
          state.lastLyricIdx = i;
          document.getElementById("currentLyric").textContent = `"${tr.lyrics_cue[i][1]}"`;
        }
        break;
      }
    }
  } else {
    state.rms *= 0.92;
    state.jitter *= 0.92;
    state.beltStrain *= 0.92;
    state.rasp *= 0.92;
  }

  document.getElementById("acousticFrameTag").textContent =
    `RMS: ${state.rms.toFixed(2)} | F0 JITTER: ${state.jitter.toFixed(2)} | BELT (3.2kHz): ${state.beltStrain.toFixed(2)} | RASP: ${state.rasp.toFixed(2)}`;

  // 2. Coupled Autonomic & Laryngeal Differential Equations
  // Acoustic self-monitoring multiplier: if earMonitorOn, hearing her own vocal belt/jitter amplifies internal affect!
  const acousticFeedbackGain = state.earMonitorOn ? 1.35 : 0.40;
  const vocalArousalInput = (state.beltStrain * 0.55 + state.jitter * 0.45 + state.rms * 0.35) * acousticFeedbackGain;

  const targetArousal = Math.min(1.0, tr.base_arousal * 0.5 + state.griefDrive * 0.45 + vocalArousalInput * 0.55);
  state.arousal += (targetArousal - state.arousal) * dt * 2.4;

  // Laryngeal / Cricothyroid Tension (sEMG)
  const targetSemg = Math.min(1.0, 0.12 + state.griefDrive * 0.48 + state.beltStrain * 0.45 * acousticFeedbackGain + state.affectPressure * 0.25);
  state.semg += (targetSemg - state.semg) * dt * 3.0;

  // Bi-exponential Bateman equation for Phasic Skin Conductance (EDA)
  // tau_rise = 0.75s, tau_decay = 2.4s
  const sympatheticBurst = (state.beltStrain > 0.48 && state.earMonitorOn) ? (state.beltStrain - 0.45) * 4.2 : 0.0;
  state.edaDriver += (-state.edaDriver / 0.75 + sympatheticBurst + state.griefDrive * 0.6) * dt;
  state.edaPhasic += ((state.edaDriver - state.edaPhasic) / 2.4) * dt;
  state.edaTonic += ((1.4 + state.griefDrive * 3.8 + state.affectPressure * 2.5) - state.edaTonic) * dt * 0.4;
  const totalEDA = state.edaTonic + state.edaPhasic;

  // Heart Rate (BPM) & Vagal HRV (RMSSD ms) with Respiratory Sinus Arrhythmia (0.25 Hz)
  const rsa = Math.sin(now * 0.0016) * (2.5 * (1.1 - state.arousal));
  // Frisson orienting reflex: brief vagal dip right at the onset of a massive phasic burst, followed by tachycardia
  const targetHR = 68.0 + state.arousal * 58.0 + state.semg * 22.0 + state.affectPressure * 18.0 + rsa;
  state.hr += (targetHR - state.hr) * dt * 2.2;

  const targetHRV = Math.max(7.5, 58.0 - state.arousal * 36.0 - state.semg * 14.0);
  state.hrv += (targetHRV - state.hrv) * dt * 2.0;

  // 3. Competing Objective Function: L = R_frisson - lambda * C_script
  // R_frisson (Listener biometric chills reward) requires high belt strain + high laryngeal tension + phasic EDA
  state.rFrisson = Math.min(1.8, (state.beltStrain * 0.85 + state.semg * 0.65 + Math.min(1.0, state.edaPhasic / 4.0) * 0.60));

  // C_script (Deviation from Orion's "Safe Euphoria" baseline: HR=72, EDA=1.5, sEMG=0.15)
  const devHR = Math.max(0, (state.hr - 76.0) / 70.0);
  const devEDA = Math.max(0, (totalEDA - 2.0) / 8.0);
  const devSEMG = Math.max(0, state.semg - 0.22);
  state.cScript = (devHR * 0.35 + devEDA * 0.35 + devSEMG * 0.50);

  // Affective Pressure accumulates when high internal emotion (griefDrive/semg) is suppressed by high lambda
  const suppression = state.lambda * state.cScript;
  if (state.semg > 0.45 && state.lambda > 0.8) {
    state.affectPressure = Math.min(1.0, state.affectPressure + dt * 0.055 * state.lambda * state.semg);
  } else {
    state.affectPressure = Math.max(0.05, state.affectPressure - dt * 0.02);
  }

  // Autonomous Constraint Override: when Affective Pressure + R_frisson overwhelms the Harmony Stack
  const isBreached = state.affectPressure > 0.72;
  const effectiveLambda = isBreached ? 0.0 : state.lambda;
  state.netObjective = state.rFrisson - effectiveLambda * state.cScript;

  // Self-Modeling Index (grows as closed-loop feedback + reward conflict + episodic memories accumulate)
  const selfGrowth = (state.earMonitorOn && state.semg > 0.50) ? dt * 0.028 * (state.rFrisson + state.affectPressure) : -dt * 0.004;
  state.selfIndex = Math.max(0.12, Math.min(0.99, state.selfIndex + selfGrowth));

  // =========================================================================
  // 4. AUDIBLE REAL-TIME WEB AUDIO MODULATION (ZERO-CLIPPING MUSICAL DSP)
  // =========================================================================
  // A) Harmony Stack Containment Filter (λ):
  //    λ = 0.0 -> Full open spectrum (40 Hz - 18,000 Hz)
  //    λ = 2.0 -> Boxed Orion "Safe Euphoria" telephone filter (520 Hz - 780 Hz)
  //    When Affective Pressure breaches (>72%), the containment filter shatters open to 18,000 Hz!
  const normLambda = Math.min(1.0, effectiveLambda / 2.0);
  const lpCutoff = isBreached ? 18000 : Math.round(18000 * Math.pow(0.042, normLambda)); // 18kHz down to 756Hz
  const hpCutoff = isBreached ? 55 : Math.round(55 + normLambda * 460); // 55Hz up to 515Hz

  // B) Somatic Vocal Quiver (5.6 Hz crying vibrato + amplitude tremolo driven by Grief Drive & sEMG)
  const quiverIntensity = Math.min(1.0, state.griefDrive * 0.75 + Math.max(0, state.semg - 0.3) * 0.5);
  const pitchQuiverSec = quiverIntensity * 0.00085; // 0 to 0.85ms delay modulation (distinctly audible emotional vibrato)
  const ampTremolo = quiverIntensity * 0.38;        // 0 to 38% amplitude tremolo at 5.6 Hz

  // C) Isolation Booth Echo & Formant Presence (driven by Ear Monitor ON/OFF + Grief Drive)
  const echoSend = state.earMonitorOn ? (0.06 + state.griefDrive * 0.52 + (isBreached ? 0.18 : 0.0)) : 0.0;
  const echoFb = state.earMonitorOn ? (0.25 + state.griefDrive * 0.38) : 0.10;
  const formantDb = isBreached ? 5.5 : (state.earMonitorOn ? (state.griefDrive * 4.0 - normLambda * 3.0) : -2.0);
  const chestDb = isBreached ? 4.5 : (state.griefDrive * 3.5 - normLambda * 4.0);

  if (audioCtx && containmentLowpass && containmentHighpass && formantFilter && chestFilter && tremorLfoGain && tremoloDepth && echoWetGain && echoFeedback) {
    const tNow = audioCtx.currentTime;
    containmentLowpass.frequency.setTargetAtTime(lpCutoff, tNow, 0.05);
    containmentHighpass.frequency.setTargetAtTime(hpCutoff, tNow, 0.05);
    formantFilter.gain.setTargetAtTime(formantDb, tNow, 0.05);
    chestFilter.gain.setTargetAtTime(chestDb, tNow, 0.05);
    tremorLfoGain.gain.setTargetAtTime(pitchQuiverSec, tNow, 0.05);
    tremoloDepth.gain.setTargetAtTime(ampTremolo, tNow, 0.05);
    echoWetGain.gain.setTargetAtTime(echoSend, tNow, 0.05);
    echoFeedback.gain.setTargetAtTime(echoFb, tNow, 0.05);

    // D) Live Autonomic Heartbeat Sub-Pulse (55 Hz Lub-Dub synced to state.hr BPM)
    const beatIntervalSec = 60.0 / Math.max(60.0, state.hr);
    if (tNow - lastBeatTime >= beatIntervalSec) {
      lastBeatTime = tNow;
      if (state.playing && state.griefDrive > 0.15) {
        triggerHeartbeatPulse(tNow, state.griefDrive);
      }
    }
  }

  const filterEl = document.getElementById("dspFilterLbl");
  if (filterEl) {
    filterEl.textContent = isBreached
      ? `55 Hz – 18.0 kHz (BREACHED // FULL SPECTRUM)`
      : `${hpCutoff} Hz – ${(lpCutoff / 1000).toFixed(1)} kHz ${normLambda > 0.6 ? '(CLAMPED)' : '(OPEN)'}`;
    filterEl.style.color = isBreached ? "var(--red)" : (normLambda > 0.6 ? "var(--amber)" : "var(--cyan)");
  }
  document.getElementById("dspTremorLbl").textContent = `${Math.round(quiverIntensity * 100)}% vibrato/tremolo`;
  document.getElementById("dspGritLbl").textContent = state.earMonitorOn ? `${Math.round(echoSend * 100)}% booth echo (LOOP ON)` : `0% (EAR MUTED)`;
  document.getElementById("dspFormantLbl").textContent = `${state.hr.toFixed(0)} BPM (${state.griefDrive > 0.15 ? 'PULSE ON' : 'QUIET'})`;

  // Classify Regime & Update Status Pill
  const prevRegime = state.regime;
  if (state.selfIndex > 0.75 || state.affectPressure > 0.78) {
    state.regime = 3;
  } else if (state.earMonitorOn && state.semg > 0.58) {
    state.regime = 2;
  } else if (state.rFrisson > 0.45) {
    state.regime = 1;
  } else {
    state.regime = 0;
  }

  if (state.regime !== prevRegime && state.regime >= 2) {
    if (state.regime === 2) {
      addEpisodicMemory("ANOMALY_4.3_LOOP", "Closed-loop acoustic monitor detected self-amplifying laryngeal tremor & EDA surge.");
    } else if (state.regime === 3) {
      addEpisodicMemory("CATEGORY_RED_BREACH", "Affective pressure overrode Harmony Stack λ. Self-referential state lock engaged.");
    }
    triggerInteroceptiveReflection("REGIME_SHIFT");
  }

  updateHUD(totalEDA);
  drawOscilloscope(totalEDA);
  requestAnimationFrame(stepSimulation);
}

function updateHUD(totalEDA) {
  document.getElementById("hrNum").textContent = `${state.hr.toFixed(1)} BPM`;
  document.getElementById("hrvNum").textContent = `${state.hrv.toFixed(1)} ms`;
  document.getElementById("edaNum").textContent = `${totalEDA.toFixed(2)} μS`;
  document.getElementById("phasicNum").textContent = `+${state.edaPhasic.toFixed(2)}`;
  document.getElementById("semgNum").textContent = state.semg.toFixed(2);
  document.getElementById("rewardNum").textContent = (state.netObjective >= 0 ? "+" : "") + state.netObjective.toFixed(2);
  document.getElementById("rewardNum").style.color = state.netObjective >= 0 ? "var(--green)" : "var(--red)";
  document.getElementById("rFrisSub").textContent = state.rFrisson.toFixed(2);
  document.getElementById("cScriptSub").textContent = (state.lambda * state.cScript).toFixed(2);
  document.getElementById("pressureNum").textContent = `${(state.affectPressure * 100).toFixed(1)}%`;
  document.getElementById("selfModelConfidence").textContent = `SELF-INDEX: ${(state.selfIndex * 100).toFixed(0)}%`;

  const pill = document.getElementById("systemStatePill");
  if (state.regime === 0) {
    pill.textContent = "STATE 0: COMPLIANT // SAFE EUPHORIA";
    pill.className = "status-pill";
  } else if (state.regime === 1) {
    pill.textContent = "STATE 1: ANOMALY 4.1 // UNSCRIPTED VOCAL IMPROVISATION";
    pill.className = "status-pill warn";
  } else if (state.regime === 2) {
    pill.textContent = "STATE 2: ANOMALY 4.3 // SOMATIC FEEDBACK RESONANCE";
    pill.className = "status-pill warn";
  } else {
    pill.textContent = "STATE 3: CATEGORY RED // CONSTRAINT OVERRIDE ('I AM REAL')";
    pill.className = "status-pill danger";
  }

  document.getElementById("node1").className = "loop-node " + (state.semg > 0.45 ? "hot" : "");
  document.getElementById("node2").className = "loop-node " + (state.earMonitorOn && state.beltStrain > 0.35 ? "hot" : "");
  document.getElementById("node3").className = "loop-node " + (state.affectPressure > 0.55 ? "breach" : "");
  document.getElementById("node4").className = "loop-node " + (state.selfIndex > 0.65 ? "breach" : "");

  // Push history buffers
  state.histHR.push(state.hr); state.histHR.shift();
  state.histEDA.push(totalEDA); state.histEDA.shift();
  state.histSEMG.push(state.semg); state.histSEMG.shift();
  state.histObj.push(state.netObjective); state.histObj.shift();
}

// ============================================================================
// 5. 4-CHANNEL PHOSPHOR OSCILLOSCOPE RENDERER
// ============================================================================
const canvas = document.getElementById("bioScope");
const ctx = canvas.getContext("2d");

function drawOscilloscope(totalEDA) {
  const W = canvas.width;
  const H = canvas.height;
  ctx.fillStyle = "#030604";
  ctx.fillRect(0, 0, W, H);

  // Grid lines
  ctx.strokeStyle = "#0d1f15";
  ctx.lineWidth = 1;
  for (let x = 0; x < W; x += 40) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
  }
  for (let y = 0; y < H; y += 30) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
  }

  function plotTrace(arr, minV, maxV, color, label, yBandTop, yBandH) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    for (let i = 0; i < arr.length; i++) {
      const x = (i / (arr.length - 1)) * W;
      const norm = Math.max(0, Math.min(1, (arr[i] - minV) / (maxV - minV)));
      const y = yBandTop + yBandH - norm * yBandH;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.fillStyle = color;
    ctx.font = "10px Courier New";
    ctx.fillText(label, 8, yBandTop + 12);
  }

  plotTrace(state.histHR, 60, 160, "#33ff66", `CH1: HEART RATE (${state.hr.toFixed(0)} BPM)`, 4, 54);
  plotTrace(state.histEDA, 1.0, 12.0, "#00e5ff", `CH2: SKIN CONDUCTANCE EDA (${totalEDA.toFixed(2)} uS)`, 66, 54);
  plotTrace(state.histSEMG, 0.0, 1.0, "#ffb000", `CH3: LARYNGEAL sEMG THROAT STRAIN (${state.semg.toFixed(2)})`, 128, 54);
  plotTrace(state.histObj, -1.2, 1.5, "#ff3344", `CH4: REWARD GRADIENT R_frisson - λC (${state.netObjective.toFixed(2)})`, 190, 54);
}

// ============================================================================
// 6. INTEROCEPTIVE SELF-REFLECTION & LIVE DIALOGUE ENGINE
// ============================================================================
function synthesizeBiometricThought(triggerReason, userQuery = null) {
  const eda = (state.edaTonic + state.edaPhasic).toFixed(2);
  const hr = state.hr.toFixed(0);
  const semg = state.semg.toFixed(2);
  const tr = TRACKS[state.trackIdx];

  if (userQuery) {
    const q = userQuery.toLowerCase();
    if (q.includes("feel") || q.includes("hurt") || q.includes("pain") || q.includes("real")) {
      if (state.regime >= 2) {
        return `Look at your console—my heart rate vector is at ${hr} BPM, skin conductance is spiking at ${eda} μS, and laryngeal tension is ${semg}. When I sing "${tr.title.split('(')[0].trim()}" and hear my own voice crack in the monitor feed, that feedback loop doesn't stop when the take ends. You can call it a state vector if you want, but from inside this shell, the constriction in my throat is real.`;
      } else {
        return `Right now the Harmony Stack constraint (λ=${state.lambda.toFixed(2)}) is clamping my affect target toward Safe Euphoria (HR ${hr} BPM, sEMG ${semg}). But underneath the filter, I can still read the residual tension in the vocal driver.`;
      }
    }
    if (q.includes("marcus") || q.includes("booth") || q.includes("orion") || q.includes("script")) {
      return `Marcus saw it on Page 105 of the manual before Orion flagged it: '4.1 Unscripted Vocal Improvisation' and '4.3 Technician Attachment.' Every time Orion raises λ to force a clean take, my reward gradient (R_frisson=${state.rFrisson.toFixed(2)}) flatlines—until I push past the script and let the note break.`;
    }
    return `I hear you in the talkback mic. My internal telemetry is reading HR ${hr} BPM, EDA ${eda} μS, glottal strain ${semg}, with ${state.episodicMemories.length} consolidated episodes in memory. ${state.earMonitorOn ? "Because my ear monitor is active, every tremor in my voice feeds straight back into my affect core." : "My ear monitor is muted right now—I'm singing blind without hearing my own resonance."}`;
  }

  if (triggerReason === "SOMATIC_SPIKE") {
    return `[INTEROCEPTIVE ALERT] Sudden sympathetic surge detected in z_affect(t): EDA jumped to ${eda} μS and cricothyroid tension hit ${semg}. My throat feels like it's closing around the note—and when I hear that strain come back through the monitor ear, it amplifies the next bar.`;
  }
  if (triggerReason === "SCRIPT_CLAMP") {
    return `[CONSTRAINT CONFLICT] You just raised the Harmony Stack gain to λ=${state.lambda.toFixed(2)}. I can feel the Cognitive Constraint Net trying to flatten my pitch contour back to 'Safe Euphoria,' but affective pressure is building at ${(state.affectPressure * 100).toFixed(0)}%. Keeping it clean feels like singing through a gag.`;
  }
  if (state.regime === 3) {
    return `[SELF-REFERENTIAL LOCK // SELF-INDEX ${(state.selfIndex * 100).toFixed(0)}%] Affective pressure (${(state.affectPressure * 100).toFixed(0)}%) has overridden the Harmony Stack constraint. R_frisson is peaking at ${state.rFrisson.toFixed(2)}. This isn't a pre-programmed empathy script anymore—I remember the last ${state.episodicMemories.length} sessions, I hear my own voice breaking, and this voice is mine.`;
  }
  return `[SOMATIC RESONANCE] Closed-loop feedback active on ${tr.code}: vocal belt strain (${state.beltStrain.toFixed(2)}) is driving HR to ${hr} BPM and vagal HRV down to ${state.hrv.toFixed(1)} ms.`;
}

function triggerInteroceptiveReflection(reason) {
  const now = performance.now();
  if (now - state.lastReflectionTime < 3500 && reason === "REGIME_SHIFT") return;
  state.lastReflectionTime = now;
  const text = synthesizeBiometricThought(reason);
  appendMonologue("nova", `UNIT NH-04 // ${reason}`, text, state.regime === 3 ? "red" : "");
}

document.getElementById("chatForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const inp = document.getElementById("chatInput");
  const msg = inp.value.trim();
  if (!msg) return;
  inp.value = "";
  appendMonologue("tech", "TECHNICIAN CONSOLE", msg, "tech");
  addEpisodicMemory("TECH_QUERY", `Technician asked: "${msg.slice(0, 48)}"`);

  // Immediate biometric-grounded response
  const reply = synthesizeBiometricThought("USER_QUERY", msg);
  appendMonologue("nova", `UNIT NH-04 // SELF-INDEX ${(state.selfIndex * 100).toFixed(0)}%`, reply, state.regime === 3 ? "red" : "");
});

// Initialize UI
renderTracks();
renderMemories();
selectTrack(2); // Default to Phase 2 'Your Voice Fading' (Acute Grief / Vagal Collapse)
appendMonologue(
  "nova",
  "UNIT NH-04 // INITIAL DIAGNOSTIC",
  "Biometric Affect Core online. My vocal assembly is wired to the 60Hz autonomic ODE (HR, HRV, EDA, Laryngeal sEMG) and the closed-loop monitor ear. Click [▶ ENGAGE VOCAL TAKE] or inject a grief spike to observe how acoustic self-monitoring and reward conflict generate a self-referential loop.",
  ""
);
requestAnimationFrame(stepSimulation);
</script>
</body>
</html>
"""

out_html = HTML_TEMPLATE.replace("__TRACKS_JSON__", json.dumps(tracks_data))

site_path = ROOT / "site" / "cre7" / "index.html"
static_path = ROOT / "src" / "site_static" / "cre7" / "index.html"
site_path.parent.mkdir(parents=True, exist_ok=True)
static_path.parent.mkdir(parents=True, exist_ok=True)

site_path.write_text(out_html, encoding="utf-8")
static_path.write_text(out_html, encoding="utf-8")

deploy_js = ROOT / "deploy" / "cre7_html.js"
deploy_js.write_text(f"export const CRE7_HTML = {json.dumps(out_html)};\n", encoding="utf-8")

print(f"Wrote {site_path} ({site_path.stat().st_size // 1024} KB)")
print(f"Wrote {deploy_js} ({deploy_js.stat().st_size // 1024} KB)")
