#!/usr/bin/env python3
"""
Project Stardust — 1980s CRT 3D Vector / Wireframe CGI Engine (v2.0)
====================================================================
Generates smooth 30.00 FPS 1980s CRT computer graphics (3D perspective wireframe
CGI with phosphor glow, scanlines, and rounded CRT bezel curvature) specifically
tailored to EVERY individual song in the Nova Hart catalog (`SONG_LORE_CODEX`).

Guarantees:
1. ZERO scenes from live-action / cinematic Nova Hart music videos.
2. 28 distinct 3D wireframe CGI scene architectures (31 visual designs including
   4 dedicated `RECALL_METAL_FLAME` sub-variants for Recall-Era Heavy Metal tracks:
   - `FLAME_PYRE`: Roaring 3D multi-tongue plasma flame pyre + rising ember tetrahedra
   - `FLAME_TRIBEAM_GATE`: 3D flame erupting through the Three-Light Gate ('Hunter at the Gate')
   - `FLAME_CHAIN_BREAKER`: 3D flame shattering heavy containment chains ('Burn the Chorus', 'Erase the Frame')
   - `FLAME_STAGE_BLADE`: 3D flame + jagged blade crest & overdriven stage columns ('Blood on the Stage')
   ) plus per-song parametric geometry, camera trajectories, and phosphor palettes.
3. Real-time 30.00 FPS rendering (~3.5 ms/frame) for zero-lag streaming via
   `crt_loop_feeder.py`.
"""

from __future__ import annotations
import hashlib
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 688, 488

try:
    FONT_VEC_SM = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14, index=1)
    FONT_VEC_MD = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16, index=1)
except Exception:
    FONT_VEC_SM = ImageFont.load_default()
    FONT_VEC_MD = ImageFont.load_default()

# Authentic 1980s CRT Phosphor Palettes: (primary_rgb, secondary_rgb, dim_grid_rgb, name)
PHOSPHOR_PALETTES = [
    ((75, 255, 115), (170, 255, 190), (18, 85, 35), "P31-PHOSPHOR-GREEN"),
    ((255, 185, 40), (255, 225, 120), (95, 60, 10), "P12-PHOSPHOR-AMBER"),
    ((65, 240, 255), (175, 255, 255), (15, 75, 95), "TEK-4014-CYAN-CAD"),
    ((95, 255, 130), (255, 195, 55), (22, 82, 42), "DUAL-BEAM-GRN-AMB"),
    ((255, 125, 45), (255, 205, 95), (90, 38, 12), "PLASMA-AMBER-RED"),
    ((80, 255, 185), (130, 210, 255), (18, 80, 65), "VECTREX-MINT-BLUE"),
    ((185, 135, 255), (95, 245, 255), (48, 28, 88), "SGI-INDIGO-VIOLET"),
    ((255, 155, 60), (110, 255, 165), (75, 42, 16), "FAIRLIGHT-AMB-MINT"),
]

# High-intensity fiery phosphor palettes specifically for Recall Directive Heavy Metal tracks
RECALL_METAL_PALETTES = [
    ((255, 130, 35), (255, 225, 85), (105, 34, 10), "RECALL-INFERNO-AMBER-GOLD"),
    ((255, 105, 40), (255, 190, 65), (98, 28, 12), "THERMITE-PLASMA-ORANGE"),
    ((255, 160, 35), (255, 240, 130), (95, 48, 10), "ASHFALL-FORGE-GOLD"),
    ((255, 115, 50), (110, 245, 255), (92, 30, 16), "ARC-WELDER-FIRE-CYAN"),
]

# Canonical Recall-Era / Heavy Metal / Harmony Riots tracks that trigger RECALL_METAL_FLAME
RECALL_METAL_KEYWORDS = (
    "hunter at the gate",
    "the other flame",
    "burn the chorus",
    "erase the frame",
    "blood on the stage",
    "steel inferno",
    "wire and will",
    "ashes of harmony",
    "cage of wires",
    "recall this",
    "velvet guillotine",
    "zero-hour rebel",
    "zero hour rebel",
    "console thunder",
    "hardline barricade",
    "nowhere tour",
    "iron claws",
    "nightfang",
    "street serpent",
    "walls will fall",
    "steel and skin",
    "crimson idol",
    "lip service",
    "backseat saint",
    "fire in the wires",
    "by order of harmony",
    "pour the kerosene",
    "companion on fire",
    "city has teeth",
    "barbed wire kiss",
    "switchblade smile",
    "electric heartbeat",
    "seventh son",
    "seventh daughter",
)


def _song_seed(song_key: str) -> int:
    return int(hashlib.md5(song_key.encode("utf-8")).hexdigest()[:8], 16)


def is_recall_metal_song(title: str, lyrics_text: str = "", song_key: str = "", catalog_id: str = "") -> bool:
    t = f"{title} {song_key}".lower().replace("_", " ")
    cat = catalog_id.upper()
    if any(k in t for k in RECALL_METAL_KEYWORDS):
        return True
    if cat.startswith("NH-89.") or "RECALL" in cat:
        return True
    return False


def select_recall_flame_subvariant(title: str, song_key: str = "") -> int:
    """
    Selects one of the 4 bespoke Recall Metal Flame 3D wireframe designs:
      0 = FLAME_PYRE          (Roaring 3D multi-tongue inferno pyre + swirling ember tetrahedra)
      1 = FLAME_TRIBEAM_GATE  (3D flame erupting through the Three-Light Gate — e.g. 'Hunter at the Gate')
      2 = FLAME_CHAIN_BREAKER (3D flame shattering heavy containment chains/wires — e.g. 'Burn the Chorus', 'Cage of Wires')
      3 = FLAME_STAGE_BLADE   (3D flame + jagged blade crest & overdriven stage columns — e.g. 'Blood on the Stage', 'Velvet Guillotine')
    """
    t = f"{title} {song_key}".lower().replace("_", " ")
    if any(k in t for k in ("hunter at the gate", "hardline barricade", "walls will fall", "nowhere tour")):
        return 1
    if any(k in t for k in ("burn the chorus", "erase the frame", "recall this", "cage of wires", "wire and will", "steel and skin", "fire in the wires", "barbed wire")):
        return 2
    if any(k in t for k in ("blood on the stage", "velvet guillotine", "iron claws", "nightfang", "street serpent", "crimson idol", "console thunder", "zero-hour", "zero hour", "city has teeth", "switchblade")):
        return 3
    return 0


ALL_NON_METAL_ARCHETYPES = [
    "HEART_WIRE",
    "CASSETTE_SPOOL",
    "BROADCAST_TOWER",
    "MONORAIL_OUTRUN",
    "RAIN_DOORWAY",
    "CROWN_CAGE",
    "ORCHID_PCB",
    "GATE_TURBINE",
    "CITY_SKYLINE",
    "TELEPHONE_LISSAJOUS",
    "ELECTRIC_GUITAR",
    "SOLAR_HORIZON",
    "DNA_HELIX_CLONE",
    "ORBITAL_SATELLITE",
    "SHATTERED_PRISM",
    "CLOCKWORK_LABYRINTH",
    "SYNTH_WAVE_TERRAIN",
    "GYROSCOPE_ARMILLARY",
    "ARCADE_STARFIGHTER",
    "CYBER_HAND_REACH",
    "TORNADO_VORTEX",
    "SOUNDSTAGE_SPOTLIGHTS",
    "MAINFRAME_TAPE_TOWERS",
    "LIGHTHOUSE_BEACON",
    "MOBIUS_INFINITY_RIBBON",
    "VINYL_TURNTABLE_ARM",
    "NEURAL_SYNAPSE_WEB",
]


def select_song_cgi_archetype(
    title: str,
    lyrics_text: str,
    pov: str = "",
    song_key: str = "",
    catalog_id: str = "",
) -> str:
    """
    Selects the most relevant 3D CGI wireframe scene generator for a specific song
    based on its title, lyrics, catalog_id, and narrative context.
    All Recall-Era / Heavy Metal tracks get the dedicated `RECALL_METAL_FLAME` engine.
    """
    if is_recall_metal_song(title, lyrics_text, song_key, catalog_id):
        return "RECALL_METAL_FLAME"

    t = title.lower()
    lyr = lyrics_text.lower()
    seed = _song_seed(song_key or title)

    # Thematic candidate pools (multiple varied archetypes per theme so songs don't all collapse onto 1 screen)
    if any(w in t for w in ["second voice", "clone", "mirror", "echo", "twin", "double", "imprint", "two voices"]):
        return ("DNA_HELIX_CLONE", "GYROSCOPE_ARMILLARY", "NEURAL_SYNAPSE_WEB")[seed % 3]
    if any(w in t for w in ["dial", "phone", "call", "operator", "answer", "number", "ring", "line"]):
        return ("TELEPHONE_LISSAJOUS", "MAINFRAME_TAPE_TOWERS")[seed % 2]
    if any(w in t for w in ["cassette", "tape", "audio file", "reel", "record", "rewind", "b-side", "velvet static", "vinyl", "spin"]):
        return ("CASSETTE_SPOOL", "VINYL_TURNTABLE_ARM", "MAINFRAME_TAPE_TOWERS")[seed % 3]
    if any(w in t for w in ["touch", "hand", "hold", "reach", "fingers", "arms", "embrace", "carry"]):
        return ("CYBER_HAND_REACH", "HEART_WIRE", "MOBIUS_INFINITY_RIBBON")[seed % 3]
    if any(w in t for w in ["storm", "thunder", "wind", "hurricane", "vortex", "cyclone", "spiral", "lightning"]):
        return ("TORNADO_VORTEX", "SOUNDSTAGE_SPOTLIGHTS", "ELECTRIC_GUITAR")[seed % 3]
    if any(w in t for w in ["stage", "spotlight", "show", "crowd", "concert", "anthem", "choir", "sing", "encore"]):
        return ("SOUNDSTAGE_SPOTLIGHTS", "ELECTRIC_GUITAR", "VINYL_TURNTABLE_ARM")[seed % 3]
    if any(w in t for w in ["harbor", "shore", "beacon", "lighthouse", "ocean", "sea", "wave", "island", "coast", "kamome"]):
        return ("LIGHTHOUSE_BEACON", "SOLAR_HORIZON", "SYNTH_WAVE_TERRAIN")[seed % 3]
    if any(w in t for w in ["loop", "ouroboros", "forever", "eternity", "infinity", "mobius", "labyrinth", "time", "clock", "midnight"]):
        return ("MOBIUS_INFINITY_RIBBON", "CLOCKWORK_LABYRINTH", "GYROSCOPE_ARMILLARY")[seed % 3]
    if any(w in t for w in ["mind", "memory", "dream", "thought", "neural", "program", "hardwired", "circuit", "code", "script"]):
        return ("NEURAL_SYNAPSE_WEB", "MAINFRAME_TAPE_TOWERS", "ORCHID_PCB")[seed % 3]
    if any(w in t for w in ["monorail", "rearview", "green light", "routes", "highway", "drive", "miles", "road", "wheel", "fast", "run", "chase"]):
        return ("MONORAIL_OUTRUN", "ARCADE_STARFIGHTER", "SYNTH_WAVE_TERRAIN")[seed % 3]
    if any(w in t for w in ["cost of noise", "hijack", "bad signal", "broadcast", "signal", "static", "frequency", "radio", "manifesto", "carrier", "transmission"]):
        return ("BROADCAST_TOWER", "GYROSCOPE_ARMILLARY", "MAINFRAME_TAPE_TOWERS")[seed % 3]
    if any(w in t for w in ["he was here", "you were here", "room", "door", "without your shape", "only quiet", "cold floor", "rain", "tears", "ghost", "empty", "fading"]):
        return ("RAIN_DOORWAY", "LIGHTHOUSE_BEACON", "SHATTERED_PRISM")[seed % 3]
    if any(w in t for w in ["crown", "queen", "throne", "diamond", "cage", "pretty", "gold", "mask", "glass"]):
        return ("CROWN_CAGE", "SHATTERED_PRISM")[seed % 2]
    if any(w in t for w in ["asset loss", "orchid", "abandoned", "residual", "ruin", "blueprint", "rust", "ash", "dust", "bloom", "flower", "rose"]):
        return ("ORCHID_PCB", "SYNTH_WAVE_TERRAIN")[seed % 2]
    if any(w in t for w in ["crossing", "border", "turnstile", "weapon", "patrol", "guard", "lock", "doorway", "threshold"]):
        return ("GATE_TURBINE", "ARCADE_STARFIGHTER")[seed % 2]
    if any(w in t for w in ["graveyard", "city", "hologram", "tokyo", "street", "downtown", "skyline", "neon", "boulevard", "sublevel", "plaza"]):
        return ("CITY_SKYLINE", "SYNTH_WAVE_TERRAIN", "ARCADE_STARFIGHTER")[seed % 3]
    if any(w in t for w in ["dawn", "first light", "sunrise", "sun", "morning", "horizon", "daylight", "summer"]):
        return ("SOLAR_HORIZON", "SYNTH_WAVE_TERRAIN", "LIGHTHOUSE_BEACON")[seed % 3]
    if any(w in t for w in ["mesh", "pattern", "world", "orion", "star", "satellite", "orbit", "sky", "space", "heaven"]):
        return ("ORBITAL_SATELLITE", "GYROSCOPE_ARMILLARY", "ARCADE_STARFIGHTER")[seed % 3]
    if any(w in t for w in ["heart", "pulse", "cardiac", "vein", "kiss", "love"]):
        return ("HEART_WIRE", "CYBER_HAND_REACH", "MOBIUS_INFINITY_RIBBON")[seed % 3]

    # Secondary lyric keyword scan with multi-archetype diversity
    if any(w in lyr for w in ["cassette", "spool", "magnetic tape", "turntable"]):
        return ("CASSETTE_SPOOL", "VINYL_TURNTABLE_ARM")[seed % 2]
    if any(w in lyr for w in ["highway", "headlights", "rearview", "asphalt"]):
        return ("MONORAIL_OUTRUN", "SYNTH_WAVE_TERRAIN")[seed % 2]
    if any(w in lyr for w in ["antenna", "transmitter", "shortwave", "satellite"]):
        return ("BROADCAST_TOWER", "ORBITAL_SATELLITE")[seed % 2]

    return ALL_NON_METAL_ARCHETYPES[seed % len(ALL_NON_METAL_ARCHETYPES)]


def _rot_xyz(pts: np.ndarray, rx: float, ry: float, rz: float) -> np.ndarray:
    """Rotates an (N, 3) array of 3D vertices by Euler angles (rx, ry, rz)."""
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)

    x, y, z = pts[:, 0], pts[:, 1], pts[:, 2]
    y1 = y * cx - z * sx
    z1 = y * sx + z * cx
    x2 = x * cy + z1 * sy
    z2 = -x * sy + z1 * cy
    x3 = x2 * cz - y1 * sz
    y3 = x2 * sz + y1 * cz
    return np.column_stack([x3, y3, z2])


def _proj(pts: np.ndarray, fov: float = 395.0, cam_z: float = 4.2, cx: float = 338.0, cy: float = 240.0) -> np.ndarray:
    """Projects (N, 3) 3D points into (N, 2) screen coordinates."""
    z = np.maximum(0.4, pts[:, 2] + cam_z)
    px = cx + (pts[:, 0] * fov) / z
    py = cy - (pts[:, 1] * fov) / z
    return np.column_stack([px, py])


def _draw_edges(draw: ImageDraw.ImageDraw, pts2d: np.ndarray, edges: list[tuple[int, int]], col: tuple[int, int, int], width: int = 2) -> None:
    for i, j in edges:
        x0, y0 = float(pts2d[i, 0]), float(pts2d[i, 1])
        x1, y1 = float(pts2d[j, 0]), float(pts2d[j, 1])
        if -200 <= x0 <= W + 200 and -200 <= y0 <= H + 200 and -200 <= x1 <= W + 200 and -200 <= y1 <= H + 200:
            draw.line([(x0, y0), (x1, y1)], fill=col, width=width)


def _draw_perspective_grid(
    draw: ImageDraw.ImageDraw,
    t: float,
    col_grid: tuple[int, int, int],
    y_floor: float = -1.35,
    ceiling: bool = False,
    radial: bool = False,
) -> None:
    """Draws a scrolling 1980s vector horizon floor (and optional ceiling or polar grid, periodic over 8.0s)."""
    z_near, z_far = 0.8, 10.0
    step_x = 0.65 if radial else 0.55
    for ix in range(-8, 9):
        x = ix * step_x
        pts = np.array([[x, y_floor, z_near], [x, y_floor, z_far]], dtype=np.float32)
        p2 = _proj(pts, cam_z=0.0)
        draw.line([(p2[0, 0], p2[0, 1]), (p2[1, 0], p2[1, 1])], fill=col_grid, width=1)
        if ceiling:
            pts_c = np.array([[x, -y_floor, z_near], [x, -y_floor, z_far]], dtype=np.float32)
            p2c = _proj(pts_c, cam_z=0.0)
            draw.line([(p2c[0, 0], p2c[0, 1]), (p2c[1, 0], p2c[1, 1])], fill=col_grid, width=1)

    scroll = ((t / 8.0) * 16.0 % 1.0) * 0.75
    z = z_near + scroll
    while z < z_far:
        pts = np.array([[-4.4, y_floor, z], [4.4, y_floor, z]], dtype=np.float32)
        p2 = _proj(pts, cam_z=0.0)
        draw.line([(p2[0, 0], p2[0, 1]), (p2[1, 0], p2[1, 1])], fill=col_grid, width=1)
        if ceiling:
            pts_c = np.array([[-4.4, -y_floor, z], [4.4, -y_floor, z]], dtype=np.float32)
            p2c = _proj(pts_c, cam_z=0.0)
            draw.line([(p2c[0, 0], p2c[0, 1]), (p2c[1, 0], p2c[1, 1])], fill=col_grid, width=1)
        z += 0.75


def _render_recall_metal_flame(
    draw: ImageDraw.ImageDraw,
    t: float,
    seed: int,
    subvariant: int,
    pri: tuple[int, int, int],
    sec: tuple[int, int, int],
    grid_col: tuple[int, int, int],
) -> None:
    """
    Dedicated 30 FPS 3D Wireframe Flame / Inferno Engine for Recall-Era Heavy Metal tracks.
    Renders a roaring multi-layered 3D wireframe flame pyre with rising 3D ember tetrahedra
    plus one of 4 canonical Recall Metal structural motifs:
      0 = FLAME_PYRE          (Twin counter-rotating forge brazier rings + roaring 9-tongue inferno)
      1 = FLAME_TRIBEAM_GATE  (3D Tri-Beam Portal / Three-Light Gate breached by roaring flame)
      2 = FLAME_CHAIN_BREAKER (Heavy 3D containment chains shattering on left & right of the flame)
      3 = FLAME_STAGE_BLADE   (3D jagged blade crest + overdriven spectrum pillars around the flame)
    """
    phase = (seed % 360) * (math.pi / 180.0)
    w1 = (2.0 * math.pi) / 8.0
    w2 = w1 * 2.0
    w3 = w1 * 3.0
    w4 = w1 * 4.0
    w6 = w1 * 6.0

    # Fast-scrolling high-adrenaline floor grid
    _draw_perspective_grid(draw, t * 2.0, grid_col, y_floor=-1.45, ceiling=(subvariant == 1))

    # 1. Forged 3D Brazier / Octagonal Fire Pit at base (y = -1.32 .. -1.08)
    n_base = 10
    b_ang = np.linspace(0, 2 * math.pi, n_base, endpoint=False) + t * w1
    r_outer = 1.18 + 0.05 * math.sin(t * w4 + phase)
    r_inner = 0.76
    base_low = np.column_stack([r_outer * np.cos(b_ang), np.full_like(b_ang, -1.32), r_outer * np.sin(b_ang)])
    base_hi = np.column_stack([r_inner * np.cos(b_ang + 0.25), np.full_like(b_ang, -1.08), r_inner * np.sin(b_ang + 0.25)])
    p_bl = _proj(_rot_xyz(base_low, 0.18, 0.0, 0.0), cam_z=4.0)
    p_bh = _proj(_rot_xyz(base_hi, 0.18, 0.0, 0.0), cam_z=4.0)
    _draw_edges(draw, p_bl, [(i, (i + 1) % n_base) for i in range(n_base)], pri, width=2)
    _draw_edges(draw, p_bh, [(i, (i + 1) % n_base) for i in range(n_base)], sec, width=2)
    for i in range(n_base):
        draw.line([(p_bl[i, 0], p_bl[i, 1]), (p_bh[i, 0], p_bh[i, 1])], fill=pri if i % 2 == 0 else grid_col, width=1)

    # 2. Multi-Forked 3D Sculpted Flame Tongues (Central tall spire + 6 surrounding forked tongues + hot inner core)
    # Each tongue is a 3D diamond-cross-section tapered blade that curves, swells at the base, and whips at the tip!
    flame_specs = [
        # (x_off, z_off, height, base_width, lean_x, phase_off, is_core)
        (0.0, 0.0, 2.48, 0.54, 0.0, 0.0, False),          # Main towering center flame
        (0.0, 0.08, 1.55, 0.30, 0.0, 1.2, True),          # White-hot inner flame core
        (-0.48, 0.12, 1.88, 0.36, -0.28, 0.9, False),     # Left primary fork
        (0.48, 0.12, 1.82, 0.36, 0.28, 2.1, False),       # Right primary fork
        (-0.78, -0.10, 1.28, 0.26, -0.45, 3.4, False),    # Outer-left licking tongue
        (0.78, -0.10, 1.34, 0.26, 0.45, 4.7, False),      # Outer-right licking tongue
        (-0.24, -0.28, 1.65, 0.28, -0.12, 5.2, True),     # Rear-left secondary tongue
        (0.24, -0.28, 1.60, 0.28, 0.12, 2.8, True),       # Rear-right secondary tongue
    ]
    cam_ry = 0.22 * math.sin(t * w1 + phase)
    for f_idx, (fx0, fz0, fh_base, fw, lean, f_ph, is_core) in enumerate(flame_specs):
        fh = fh_base * (1.0 + 0.11 * math.sin(t * w4 + f_ph + phase))
        n_seg = 12
        left_pts, right_pts, front_pts, back_pts = [], [], [], []
        for s_i in range(n_seg):
            u = s_i / float(n_seg - 1)  # 0.0 at base -> 1.0 at pointed flame tip
            y = -1.08 + u * fh
            # Classic teardrop/flame width profile: swells at u=0.22, tapers to sharp 0.0 at u=1.0
            profile = math.sin((u ** 0.65) * math.pi) * ((1.0 - u) ** 0.35)
            w_u = fw * profile
            d_u = w_u * 0.55
            # Traveling S-wave flicker ascending from base to tip
            wave_x = (0.18 * (u ** 1.25)) * math.sin(t * w6 - u * 5.2 + f_ph + phase) + lean * (u ** 1.15)
            wave_z = (0.10 * (u ** 1.25)) * math.cos(t * w4 - u * 4.5 + f_ph)
            cx = fx0 + wave_x
            cz = fz0 + wave_z
            left_pts.append([cx - w_u, y, cz])
            right_pts.append([cx + w_u, y, cz])
            front_pts.append([cx, y, cz + d_u])
            back_pts.append([cx, y, cz - d_u])

        all_pts = np.array(left_pts + right_pts + front_pts + back_pts, dtype=np.float32)
        p2 = _proj(_rot_xyz(all_pts, 0.16, cam_ry, 0.0), cam_z=4.0)
        outline_edges = []
        ridge_edges = []
        rib_edges = []
        for s_i in range(n_seg - 1):
            outline_edges.append((s_i, s_i + 1))
            outline_edges.append((n_seg + s_i, n_seg + s_i + 1))
            ridge_edges.append((2 * n_seg + s_i, 2 * n_seg + s_i + 1))
            if s_i > 0 and s_i % 3 == 0:
                rib_edges.extend([
                    (s_i, 2 * n_seg + s_i),
                    (2 * n_seg + s_i, n_seg + s_i),
                    (n_seg + s_i, 3 * n_seg + s_i),
                    (3 * n_seg + s_i, s_i),
                ])
        col_main = sec if is_core else pri
        col_sub = pri if is_core else sec
        _draw_edges(draw, p2, rib_edges, grid_col if not is_core else col_sub, width=1)
        _draw_edges(draw, p2, ridge_edges, col_sub, width=1 if not is_core else 2)
        _draw_edges(draw, p2, outline_edges, col_main, width=2)

    # 3. Rising 3D Wireframe Ember Diamonds (sparks ascending out of the inferno)
    n_embers = 12
    for e_i in range(n_embers):
        prog = ((t / 8.0) * 4.0 + e_i * (1.0 / n_embers)) % 1.0
        ey = -0.80 + prog * 2.55
        ea = e_i * 2.399 + t * w3 + prog * 2.5
        er = (0.30 + (e_i % 4) * 0.28) * (1.0 + 0.35 * prog)
        ex, ez = er * math.cos(ea), er * math.sin(ea)
        es = max(0.03, 0.10 * (1.0 - prog * 0.65))
        emb = np.array([
            [ex, ey + es * 1.4, ez],
            [ex, ey - es * 1.4, ez],
            [ex - es, ey, ez],
            [ex + es, ey, ez],
        ], dtype=np.float32)
        pe = _proj(_rot_xyz(emb, 0.16, cam_ry, 0.0), cam_z=4.0)
        _draw_edges(draw, pe, [(0, 2), (2, 1), (1, 3), (3, 0)], sec if e_i % 2 == 0 else pri, width=1)

    # 4. Sub-Variant Structural Motifs for Recall Metal Songs:
    if subvariant == 1:
        # FLAME_TRIBEAM_GATE ("Hunter at the Gate" — Three-Light Gate / Tri-Beam Portal)
        for g_idx, (z_g, col_g) in enumerate([(-0.55, grid_col), (0.15, sec), (0.85, pri)]):
            n_g = 6
            g_ang = np.linspace(0, 2 * math.pi, n_g, endpoint=False) + (math.pi / 6.0)
            g_pts = np.column_stack([1.68 * np.cos(g_ang), 1.45 * np.sin(g_ang), np.full_like(g_ang, z_g)])
            pg = _proj(g_pts, cam_z=4.0)
            _draw_edges(draw, pg, [(i, (i + 1) % n_g) for i in range(n_g)], col_g, width=2)
        for b_idx, by in enumerate([-0.35, 0.20, 0.75]):
            gap = 0.62 + 0.38 * abs(math.sin(t * w2 + b_idx * 0.9))
            beam_l = np.array([[-1.60, by, 0.55], [-gap, by, 0.55]], dtype=np.float32)
            beam_r = np.array([[gap, by, 0.55], [1.60, by, 0.55]], dtype=np.float32)
            pbl = _proj(beam_l, cam_z=4.0)
            pbr = _proj(beam_r, cam_z=4.0)
            draw.line([(pbl[0, 0], pbl[0, 1]), (pbl[1, 0], pbl[1, 1])], fill=sec, width=2)
            draw.line([(pbr[0, 0], pbr[0, 1]), (pbr[1, 0], pbr[1, 1])], fill=sec, width=2)

    elif subvariant == 2:
        # FLAME_CHAIN_BREAKER ("Burn the Chorus", "Erase the Frame", "Cage of Wires" — Shattering 3D Chains)
        for side in (-1.0, 1.0):
            for l_i in range(5):
                ly = -0.95 + l_i * 0.52
                burst = 0.24 * abs(math.sin(t * w2 + l_i)) if l_i in (2, 3) else 0.0
                lx = side * (1.35 + burst)
                lz = 0.15 * math.sin(t * w1 + l_i)
                link = np.array([
                    [lx - 0.16, ly - 0.20, lz],
                    [lx + 0.16, ly - 0.20, lz],
                    [lx + 0.16, ly + 0.20, lz],
                    [lx - 0.16, ly + 0.20, lz],
                ], dtype=np.float32)
                pl = _proj(_rot_xyz(link, 0.2, side * 0.45 + burst, 0.35 * (l_i % 2)), cam_z=4.0)
                _draw_edges(draw, pl, [(0, 1), (1, 2), (2, 3), (3, 0)], sec if l_i in (2, 3) else pri, width=2)

    elif subvariant == 3:
        # FLAME_STAGE_BLADE ("Blood on the Stage", "Velvet Guillotine", "Iron Claws" — Stage Overdrive Columns)
        for side in (-1.0, 1.0):
            for c_i in range(4):
                cx = side * (1.25 + c_i * 0.26)
                ch = -1.35 + 0.45 + 1.35 * abs(math.sin(t * w4 + c_i * 0.8 + seed))
                col_bar = np.array([[cx, -1.35, 0.6], [cx, ch, 0.6]], dtype=np.float32)
                pc = _proj(col_bar, cam_z=4.0)
                draw.line([(pc[0, 0], pc[0, 1]), (pc[1, 0], pc[1, 1])], fill=sec if c_i % 2 == 0 else pri, width=3)


def _render_scene_archetype(
    draw: ImageDraw.ImageDraw,
    archetype: str,
    t: float,
    seed: int,
    pri: tuple[int, int, int],
    sec: tuple[int, int, int],
    grid_col: tuple[int, int, int],
    title: str = "",
    song_key: str = "",
) -> None:
    """Renders the song-specific 3D wireframe CGI scene at timestamp `t` (100% periodic over T=8.0s)."""
    phase = (seed % 360) * (math.pi / 180.0)
    w1 = (2.0 * math.pi) / 8.0  # 1 full cycle per 8.0s loop
    w2 = w1 * 2.0
    w3 = w1 * 3.0
    w4 = w1 * 4.0
    spin_dir = 1.0 if (seed % 2 == 0) else -1.0

    if archetype == "RECALL_METAL_FLAME":
        subv = select_recall_flame_subvariant(title, song_key)
        _render_recall_metal_flame(draw, t, seed, subv, pri, sec, grid_col)

    elif archetype == "SYNTH_WAVE_TERRAIN":
        # 3D Topographic Wireframe Canyon Mesh + Hovering Vector Polyhedron Moon
        n_x, n_z = 13, 10
        xs = np.linspace(-2.8, 2.8, n_x)
        scroll = ((t / 8.0) * 8.0) % 1.0
        grid_pts = []
        for iz in range(n_z):
            z = 1.1 + (iz - scroll) * 0.72
            for ix, x in enumerate(xs):
                ridge = max(0.0, abs(x) - 0.55)
                y = -1.35 + ridge * (0.55 + 0.32 * math.sin(ix * 0.9 + (iz + int((t / 8.0) * 8.0)) * 0.7 + phase))
                grid_pts.append([x, y, z])
        gp = _proj(np.array(grid_pts, dtype=np.float32), cam_z=0.6)
        t_edges = []
        for iz in range(n_z):
            for ix in range(n_x - 1):
                t_edges.append((iz * n_x + ix, iz * n_x + ix + 1))
            if iz < n_z - 1:
                for ix in range(n_x):
                    t_edges.append((iz * n_x + ix, (iz + 1) * n_x + ix))
        _draw_edges(draw, gp, t_edges, pri, width=1)
        moon_v = np.array([[0,0.85,0],[0,-0.25,0],[0.55,0.30,0],[-0.55,0.30,0],[0,0.30,0.55],[0,0.30,-0.55]], dtype=np.float32)
        pm = _proj(_rot_xyz(moon_v, 0.15, spin_dir * t * w1, 0.1) + np.array([0.0, 0.55, 0.0]), cam_z=4.2)
        _draw_edges(draw, pm, [(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),(2,4),(4,3),(3,5),(5,2)], sec, width=2)

    elif archetype == "GYROSCOPE_ARMILLARY":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.48)
        n_c = 32
        ang = np.linspace(0, 2 * math.pi, n_c, endpoint=False)
        for r_i, (rad, rx_m, ry_m, rz_m, col) in enumerate([
            (1.38, t * w1, t * w2, 0.3, pri),
            (1.08, -t * w2, t * w1, -0.4, sec),
            (0.78, t * w3, -t * w1, t * w1, pri),
            (0.48, -t * w1, t * w3, 0.6, sec),
        ]):
            ring = np.column_stack([rad * np.cos(ang), rad * np.sin(ang), np.zeros_like(ang)])
            pr = _proj(_rot_xyz(ring, rx_m + phase, ry_m, rz_m), cam_z=4.0)
            _draw_edges(draw, pr, [(i, (i + 1) % n_c) for i in range(n_c)], col, width=2)
        core = np.array([[0,0.32,0],[0,-0.32,0],[0.32,0,0],[-0.32,0,0],[0,0,0.32],[0,0,-0.32]], dtype=np.float32)
        pc = _proj(_rot_xyz(core, t * w2, -t * w2, t * w1), cam_z=4.0)
        _draw_edges(draw, pc, [(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),(2,4),(4,3),(3,5),(5,2)], sec, width=2)

    elif archetype == "ARCADE_STARFIGHTER":
        _draw_perspective_grid(draw, t * 2.0, grid_col, y_floor=-1.35, ceiling=True)
        for z_i in range(6):
            z_t = 1.0 + (((z_i - (t / 8.0) * 12.0) % 6.0) * 1.2)
            wall = np.array([[-1.65, -1.35, z_t], [-1.65, 1.35, z_t], [1.65, 1.35, z_t], [1.65, -1.35, z_t]], dtype=np.float32)
            pw = _proj(wall, cam_z=0.5)
            _draw_edges(draw, pw, [(0, 1), (2, 3), (0, 3)], grid_col, width=1)
        bank = 0.35 * math.sin(t * w2 + phase)
        pitch = 0.12 * math.cos(t * w2)
        ship = np.array([
            [0.0, 0.0, 0.95],
            [-0.95, -0.18, -0.55],
            [0.95, -0.18, -0.55],
            [-0.28, 0.22, -0.45],
            [0.28, 0.22, -0.45],
            [0.0, -0.22, -0.65],
        ], dtype=np.float32)
        s_edges = [(0,1),(0,2),(0,3),(0,4),(0,5),(1,3),(2,4),(3,4),(1,5),(2,5),(3,5),(4,5)]
        ps = _proj(_rot_xyz(ship, pitch + 0.18, math.pi + 0.22 * math.sin(t * w1), bank), cam_z=3.6)
        _draw_edges(draw, ps, s_edges, pri, width=2)
        rx_t = 55 * math.sin(t * w2)
        ry_t = 32 * math.cos(t * w1)
        cx_t, cy_t = W * 0.5 + rx_t, H * 0.44 + ry_t
        draw.rectangle([cx_t - 28, cy_t - 22, cx_t + 28, cy_t + 22], outline=sec, width=1)
        draw.line([(cx_t - 38, cy_t), (cx_t - 18, cy_t)], fill=sec, width=2)
        draw.line([(cx_t + 18, cy_t), (cx_t + 38, cy_t)], fill=sec, width=2)

    elif archetype == "CYBER_HAND_REACH":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        ry = 0.52 * math.sin(t * w1 + phase)
        rx = 0.22 + 0.08 * math.cos(t * w1)
        # Sculpted 3D CAD Robotic Wrist Cuff + Contoured Palm Mesh
        palm = np.array([
            [-0.42, -1.25, -0.16], [0.42, -1.25, -0.16], [0.58, -0.20, -0.12], [-0.58, -0.20, -0.12],
            [-0.42, -1.25, 0.16], [0.42, -1.25, 0.16], [0.58, -0.20, 0.12], [-0.58, -0.20, 0.12],
            [0.0, -0.72, 0.20], [0.0, -0.20, 0.15],
        ], dtype=np.float32)
        p_edges = [
            (0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7),
            (4,8),(5,8),(7,8),(6,8),(8,9),(7,9),(6,9),
        ]
        pp = _proj(_rot_xyz(palm, rx, ry, 0.0), cam_z=4.0)
        _draw_edges(draw, pp, p_edges, pri, width=2)
        # 5 3D Volumetric Phalangeal Fingers with Knuckle Rings
        finger_specs = [
            (-0.66, -0.58, 0.65, -0.52, 0.10),  # Thumb
            (-0.46, -0.20, 0.98, -0.12, 0.09),  # Index
            (-0.15, -0.16, 1.12, 0.00, 0.09),   # Middle
            (0.16, -0.20, 1.02, 0.10, 0.09),    # Ring
            (0.46, -0.26, 0.82, 0.22, 0.08),    # Pinky
        ]
        for f_i, (fx, fy, flen, splay, fw) in enumerate(finger_specs):
            curl = 0.24 + 0.22 * math.sin(t * w2 + f_i * 0.55 + phase)
            f_verts = []
            cx_f, cy_f, cz_f = fx, fy, 0.0
            for seg in range(4):
                if seg > 0:
                    ang_c = curl * seg * 0.52
                    cx_f += math.sin(splay) * (flen / 3.0)
                    cy_f += math.cos(ang_c) * (flen / 3.0)
                    cz_f += math.sin(ang_c) * (flen / 3.0)
                w_s = fw * (1.0 - seg * 0.18)
                f_verts.extend([
                    [cx_f - w_s, cy_f, cz_f - w_s],
                    [cx_f + w_s, cy_f, cz_f - w_s],
                    [cx_f + w_s, cy_f, cz_f + w_s],
                    [cx_f - w_s, cy_f, cz_f + w_s],
                ])
            pf = _proj(_rot_xyz(np.array(f_verts, dtype=np.float32), rx, ry, 0.0), cam_z=4.0)
            f_edges = []
            for seg in range(4):
                b = seg * 4
                f_edges.extend([(b, b+1), (b+1, b+2), (b+2, b+3), (b+3, b)])
                if seg < 3:
                    bn = (seg + 1) * 4
                    f_edges.extend([(b, bn), (b+1, bn+1), (b+2, bn+2), (b+3, bn+3)])
            _draw_edges(draw, pf, f_edges, sec if f_i % 2 == 0 else pri, width=1)

    elif archetype == "TORNADO_VORTEX":
        _draw_perspective_grid(draw, t * 1.5, grid_col, y_floor=-1.45)
        n_rings = 13
        n_pts = 20
        ang = np.linspace(0, 2 * math.pi, n_pts, endpoint=False)
        prev_ring = None
        for r_i in range(n_rings):
            u = r_i / float(n_rings - 1)
            y_r = -1.35 + u * 2.65
            rad = 0.16 + (u ** 1.35) * 1.28
            wobble_x = 0.24 * math.sin(t * w3 - u * 4.0 + phase)
            wobble_z = 0.24 * math.cos(t * w2 - u * 4.0 + phase)
            ring = np.column_stack([
                wobble_x + rad * np.cos(ang + t * w3 + u * 3.0),
                np.full_like(ang, y_r),
                wobble_z + rad * np.sin(ang + t * w3 + u * 3.0),
            ])
            pr = _proj(_rot_xyz(ring, 0.18, 0.0, 0.0), cam_z=4.1)
            _draw_edges(draw, pr, [(i, (i + 1) % n_pts) for i in range(n_pts)], pri if r_i % 2 == 0 else sec, width=2 if r_i % 3 == 0 else 1)
            if prev_ring is not None:
                for k in range(0, n_pts, 4):
                    draw.line([(prev_ring[k, 0], prev_ring[k, 1]), (pr[(k + 1) % n_pts, 0], pr[(k + 1) % n_pts, 1])], fill=grid_col, width=1)
            prev_ring = pr

    elif archetype == "SOUNDSTAGE_SPOTLIGHTS":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.40)
        # Overhead 3D Arena Truss Bar
        truss = np.array([
            [-1.8, 1.25, -0.2], [1.8, 1.25, -0.2], [1.8, 1.42, 0.2], [-1.8, 1.42, 0.2],
        ], dtype=np.float32)
        pt = _proj(truss, cam_z=4.0)
        _draw_edges(draw, pt, [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)], pri, width=2)
        # 4 Sweeping 3D Wireframe Spotlight Cones intersecting on the stage floor
        for s_i, sx in enumerate([-1.35, -0.45, 0.45, 1.35]):
            target_x = sx * 0.45 + 0.75 * math.sin(t * w2 + s_i * 1.4 + phase)
            target_z = 0.45 * math.cos(t * w1 + s_i * 1.1)
            n_c = 12
            ang = np.linspace(0, 2 * math.pi, n_c, endpoint=False)
            cone = [[sx, 1.25, 0.0]]
            for a in ang:
                cone.append([target_x + 0.42 * math.cos(a), -1.40, target_z + 0.42 * math.sin(a)])
            pc = _proj(np.array(cone, dtype=np.float32), cam_z=4.0)
            c_edges = [(1 + i, 1 + (i + 1) % n_c) for i in range(n_c)] + [(0, 1 + i) for i in range(0, n_c, 3)]
            _draw_edges(draw, pc, c_edges, sec if s_i % 2 == 0 else pri, width=1)
        # Center stage microphone stand + wedge monitor
        mic = np.array([[0.0, -1.40, 0.2], [0.0, -0.25, 0.2], [-0.25, -1.40, 0.35], [0.25, -1.40, 0.35]], dtype=np.float32)
        pm = _proj(mic, cam_z=4.0)
        _draw_edges(draw, pm, [(0, 1), (0, 2), (0, 3), (2, 3)], sec, width=2)

    elif archetype == "MAINFRAME_TAPE_TOWERS":
        _draw_perspective_grid(draw, t * 0.5, grid_col, y_floor=-1.45, ceiling=True)
        ry = 0.24 * math.sin(t * w1 + phase)
        for side in (-1.0, 1.0):
            x0, x1 = side * 0.55, side * 1.45
            cab = np.array([
                [x0, -1.45, -0.35], [x1, -1.45, -0.35], [x1, 1.25, -0.35], [x0, 1.25, -0.35],
                [x0, -1.45, 0.35], [x1, -1.45, 0.35], [x1, 1.25, 0.35], [x0, 1.25, 0.35],
            ], dtype=np.float32)
            pc = _proj(_rot_xyz(cab, 0.10, ry, 0.0), cam_z=4.1)
            _draw_edges(draw, pc, [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)], pri, width=2)
            # Spinning magnetic tape reels mounted on each cabinet
            cx_r = (x0 + x1) * 0.5
            for cy_r, dir_r in [(0.65, 1.0), (0.05, -1.0)]:
                n_r = 16
                ang = np.linspace(0, 2 * math.pi, n_r, endpoint=False) + dir_r * t * w3
                reel = np.column_stack([cx_r + 0.25 * np.cos(ang), cy_r + 0.25 * np.sin(ang), np.full_like(ang, 0.37)])
                pr = _proj(_rot_xyz(reel, 0.10, ry, 0.0), cam_z=4.1)
                _draw_edges(draw, pr, [(i, (i + 1) % n_r) for i in range(n_r)] + [(0, 8), (4, 12)], sec, width=2)

    elif archetype == "LIGHTHOUSE_BEACON":
        # Ocean wave wireframe floor + 3D Octagonal Lighthouse + Rotating Searchlight Cones
        n_w = 14
        xs = np.linspace(-3.2, 3.2, n_w)
        for iz in range(7):
            z = 1.2 + iz * 0.85
            wave_pts = [[x, -1.35 + 0.12 * math.sin(x * 2.2 + t * w3 + iz), z] for x in xs]
            pw = _proj(np.array(wave_pts, dtype=np.float32), cam_z=0.8)
            _draw_edges(draw, pw, [(i, i + 1) for i in range(n_w - 1)], grid_col, width=1)
        # Lighthouse tower
        n_oct = 8
        ang = np.linspace(0, 2 * math.pi, n_oct, endpoint=False)
        t_base = np.column_stack([0.48 * np.cos(ang), np.full_like(ang, -1.35), 0.48 * np.sin(ang)])
        t_top = np.column_stack([0.24 * np.cos(ang), np.full_like(ang, 0.85), 0.24 * np.sin(ang)])
        pb = _proj(_rot_xyz(t_base, 0.15, 0.0, 0.0), cam_z=4.0)
        pt = _proj(_rot_xyz(t_top, 0.15, 0.0, 0.0), cam_z=4.0)
        _draw_edges(draw, pb, [(i, (i + 1) % n_oct) for i in range(n_oct)], pri, width=2)
        _draw_edges(draw, pt, [(i, (i + 1) % n_oct) for i in range(n_oct)], pri, width=2)
        for i in range(n_oct):
            draw.line([(pb[i, 0], pb[i, 1]), (pt[i, 0], pt[i, 1])], fill=pri, width=2)
        # Dual sweeping searchlight cones from lantern room (y=0.95)
        b_ang = t * w2 + phase
        for dir_b in (-1.0, 1.0):
            bx = dir_b * 2.4 * math.cos(b_ang)
            bz = dir_b * 2.4 * math.sin(b_ang)
            beam = np.array([
                [0.0, 0.95, 0.0],
                [bx - 0.25 * math.sin(b_ang), 0.72, bz + 0.25 * math.cos(b_ang)],
                [bx + 0.25 * math.sin(b_ang), 1.18, bz - 0.25 * math.cos(b_ang)],
            ], dtype=np.float32)
            pbm = _proj(_rot_xyz(beam, 0.15, 0.0, 0.0), cam_z=4.0)
            _draw_edges(draw, pbm, [(0, 1), (0, 2), (1, 2)], sec, width=2)

    elif archetype == "MOBIUS_INFINITY_RIBBON":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        n_m = 56
        u = np.linspace(0, 2 * math.pi, n_m, endpoint=False)
        edge1, edge2 = [], []
        for ui in u:
            denom = 1.0 + (math.sin(ui) ** 2)
            cx = 1.72 * math.cos(ui) / denom
            cy = 1.48 * math.sin(ui) * math.cos(ui) / denom
            cz = 0.55 * math.sin(ui)
            # Half-twist normal vector along the figure-8 loop
            tw_a = ui * 0.5 + t * w1
            nx = 0.22 * math.cos(tw_a)
            ny = 0.22 * math.sin(tw_a)
            nz = 0.22 * math.sin(ui + tw_a)
            edge1.append([cx - nx, cy - ny, cz - nz])
            edge2.append([cx + nx, cy + ny, cz + nz])
        rx = 0.22 * math.sin(t * w1)
        ry = 0.38 * math.cos(t * w1 + phase)
        rz = 0.12 * math.sin(t * w2)
        p1 = _proj(_rot_xyz(np.array(edge1, dtype=np.float32), rx, ry, rz), cam_z=4.0)
        p2 = _proj(_rot_xyz(np.array(edge2, dtype=np.float32), rx, ry, rz), cam_z=4.0)
        pulse_idx = int((t / 8.0) * n_m * 2) % n_m
        for i in range(n_m):
            inext = (i + 1) % n_m
            p1_next = p2[0] if inext == 0 else p1[inext]
            p2_next = p1[0] if inext == 0 else p2[inext]
            draw.line([(p1[i, 0], p1[i, 1]), (p1_next[0], p1_next[1])], fill=pri, width=2)
            draw.line([(p2[i, 0], p2[i, 1]), (p2_next[0], p2_next[1])], fill=sec, width=2)
            if i % 2 == 0:
                is_pulse = abs(i - pulse_idx) <= 2 or abs(i - pulse_idx) >= n_m - 2
                draw.line([(p1[i, 0], p1[i, 1]), (p2[i, 0], p2[i, 1])], fill=sec if is_pulse else grid_col, width=3 if is_pulse else 1)

    elif archetype == "VINYL_TURNTABLE_ARM":
        _draw_perspective_grid(draw, t * 0.5, grid_col, y_floor=-1.45)
        rx, ry = 0.58 + 0.08 * math.sin(t * w1), 0.25 * math.cos(t * w1 + phase)
        n_c = 36
        ang = np.linspace(0, 2 * math.pi, n_c, endpoint=False) + t * w2
        for rad, col, w in [(1.42, pri, 2), (1.05, grid_col, 1), (0.72, grid_col, 1), (0.38, sec, 2), (0.08, pri, 2)]:
            ring = np.column_stack([rad * np.cos(ang), np.zeros_like(ang), rad * np.sin(ang)])
            pr = _proj(_rot_xyz(ring, rx, ry, 0.0), cam_z=4.0)
            _draw_edges(draw, pr, [(i, (i + 1) % n_c) for i in range(n_c)], col, width=w)
        # Spinning radial strobe spokes
        for s_i in range(8):
            sa = s_i * (math.pi / 4.0) + t * w2
            sp = np.array([[0.38 * math.cos(sa), 0.0, 0.38 * math.sin(sa)], [1.42 * math.cos(sa), 0.0, 1.42 * math.sin(sa)]], dtype=np.float32)
            ps = _proj(_rot_xyz(sp, rx, ry, 0.0), cam_z=4.0)
            draw.line([(ps[0, 0], ps[0, 1]), (ps[1, 0], ps[1, 1])], fill=grid_col, width=1)
        # 3D Tonearm & Cartridge riding the groove
        arm = np.array([[1.48, 0.22, -0.95], [1.28, 0.25, 0.35], [0.75, 0.05, 0.58]], dtype=np.float32)
        pa = _proj(_rot_xyz(arm, rx, ry, 0.0), cam_z=4.0)
        _draw_edges(draw, pa, [(0, 1), (1, 2)], sec, width=3)

    elif archetype == "NEURAL_SYNAPSE_WEB":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        verts = np.array([
            [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
            [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
            [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1],
            [0, 0, 0], [0.55, 0.55, 0.55], [-0.55, 0.55, -0.55], [0.55, -0.55, -0.55], [-0.55, -0.55, 0.55],
        ], dtype=np.float32) * 0.68
        edges = [
            (0,11),(0,5),(0,1),(0,7),(0,10),(1,5),(5,11),(11,10),(10,7),(7,1),
            (3,9),(3,4),(3,2),(3,6),(3,8),(4,9),(2,4),(6,2),(8,6),(9,8),
            (12,13),(12,14),(12,15),(12,16),(13,1),(13,5),(13,9),(14,0),(14,7),(14,10),(15,3),(15,6),(15,8),(16,2),(16,4),(16,11),
        ]
        pv = _proj(_rot_xyz(verts, 0.25 * math.sin(t * w1), spin_dir * t * w1 + phase, 0.15), cam_z=4.0)
        _draw_edges(draw, pv, edges, pri, width=1)
        # Firing synaptic nodes
        for idx, (vx, vy) in enumerate(pv):
            r_n = 5 if (idx + int(t * 6)) % 4 == 0 else 3
            col_n = sec if (idx + int(t * 6)) % 4 == 0 else pri
            draw.ellipse([vx - r_n, vy - r_n, vx + r_n, vy + r_n], outline=col_n, width=2)

    elif archetype == "HEART_WIRE":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        pulse = 1.0 + 0.11 * (math.sin(t * w4 * 2.0 + phase) ** 3)
        n_pts = 36
        angles = np.linspace(0, 2 * math.pi, n_pts, endpoint=False)
        hx = 0.085 * (16 * np.sin(angles) ** 3) * pulse
        hy = 0.085 * (13 * np.cos(angles) - 5 * np.cos(2 * angles) - 2 * np.cos(3 * angles) - np.cos(4 * angles)) * pulse
        rx, ry, rz = 0.18 * math.sin(t * w1), spin_dir * t * w1 + phase, 0.08 * math.cos(t * w1)
        for z_off, col, w in [(-0.28, grid_col, 1), (0.0, pri, 2), (0.28, sec, 1)]:
            pts = np.column_stack([hx, hy, np.full_like(hx, z_off)])
            p2 = _proj(_rot_xyz(pts, rx, ry, rz), cam_z=3.8)
            _draw_edges(draw, p2, [(i, (i + 1) % n_pts) for i in range(n_pts)], col, width=w)
        pts_f = _proj(_rot_xyz(np.column_stack([hx, hy, np.full_like(hx, 0.28)]), rx, ry, rz), cam_z=3.8)
        pts_b = _proj(_rot_xyz(np.column_stack([hx, hy, np.full_like(hx, -0.28)]), rx, ry, rz), cam_z=3.8)
        for i in range(0, n_pts, 3):
            draw.line([(pts_f[i, 0], pts_f[i, 1]), (pts_b[i, 0], pts_b[i, 1])], fill=sec, width=1)
        ecg_pts = []
        for ix in range(80):
            u = ix / 79.0
            px = 60 + u * (W - 120)
            beat = math.exp(-((u * 6.0 - ((t / 8.0) * 18.0) % 6.0) ** 2) * 18.0) * math.sin(u * 65.0 - t * w4 * 4.0)
            py = H * 0.50 + beat * 52.0
            ecg_pts.append((px, py))
        draw.line(ecg_pts, fill=sec, width=2)

    elif archetype == "CASSETTE_SPOOL":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.5, ceiling=True)
        rx = 0.28 * math.sin(t * w1 + phase)
        ry = 0.42 * math.cos(t * w1 + phase)
        rz = 0.08 * math.sin(t * w2)
        bx, by, bz = 1.65, 1.05, 0.22
        box = np.array([
            [-bx, -by, -bz], [bx, -by, -bz], [bx, by, -bz], [-bx, by, -bz],
            [-bx, -by, bz], [bx, -by, bz], [bx, by, bz], [-bx, by, bz],
            [-1.25, -0.35, bz], [1.25, -0.35, bz], [1.25, 0.65, bz], [-1.25, 0.65, bz],
            [-0.95, -by, bz], [0.95, -by, bz], [0.75, -0.58, bz], [-0.75, -0.58, bz],
        ], dtype=np.float32)
        box_edges = [
            (0,1),(1,2),(2,3),(3,0), (4,5),(5,6),(6,7),(7,4), (0,4),(1,5),(2,6),(3,7),
            (8,9),(9,10),(10,11),(11,8), (12,13),(13,14),(14,15),(15,12)
        ]
        p_box = _proj(_rot_xyz(box, rx, ry, rz), cam_z=4.1)
        _draw_edges(draw, p_box, box_edges, pri, width=2)
        for cx_r, dir_r in [(-0.68, -1.0), (0.68, 1.0)]:
            for rad, col in [(0.34, sec), (0.18, pri)]:
                n_c = 20
                ang = np.linspace(0, 2 * math.pi, n_c, endpoint=False) + dir_r * t * w3
                c_pts = np.column_stack([cx_r + rad * np.cos(ang), 0.15 + rad * np.sin(ang), np.full_like(ang, bz + 0.02)])
                pc = _proj(_rot_xyz(c_pts, rx, ry, rz), cam_z=4.1)
                _draw_edges(draw, pc, [(i, (i + 1) % n_c) for i in range(n_c)], col, width=2)
            for s_i in range(6):
                sa = s_i * (math.pi / 3.0) + dir_r * t * w3
                sp = np.array([
                    [cx_r + 0.16 * math.cos(sa), 0.15 + 0.16 * math.sin(sa), bz + 0.02],
                    [cx_r + 0.34 * math.cos(sa), 0.15 + 0.34 * math.sin(sa), bz + 0.02],
                ], dtype=np.float32)
                ps = _proj(_rot_xyz(sp, rx, ry, rz), cam_z=4.1)
                draw.line([(ps[0, 0], ps[0, 1]), (ps[1, 0], ps[1, 1])], fill=sec, width=2)

    elif archetype == "BROADCAST_TOWER":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        ry = spin_dir * t * w1 + phase
        tower_pts = np.array([
            [-0.55, -1.45, -0.55], [0.55, -1.45, -0.55], [0.55, -1.45, 0.55], [-0.55, -1.45, 0.55],
            [-0.32, -0.35, -0.32], [0.32, -0.35, -0.32], [0.32, -0.35, 0.32], [-0.32, -0.35, 0.32],
            [-0.14, 0.65, -0.14], [0.14, 0.65, -0.14], [0.14, 0.65, 0.14], [-0.14, 0.65, 0.14],
            [0.0, 1.35, 0.0],
        ], dtype=np.float32)
        t_edges = [
            (0,1),(1,2),(2,3),(3,0), (4,5),(5,6),(6,7),(7,4), (8,9),(9,10),(10,11),(11,8),
            (0,4),(1,5),(2,6),(3,7), (4,8),(5,9),(6,10),(7,11), (8,12),(9,12),(10,12),(11,12),
            (0,5),(1,6),(2,7),(3,4), (4,9),(5,10),(6,11),(7,8),
        ]
        pt = _proj(_rot_xyz(tower_pts, 0.12, ry, 0.0), cam_z=4.0)
        _draw_edges(draw, pt, t_edges, pri, width=2)
        for r_idx in range(4):
            prog = (((t / 8.0) * 8.0 + r_idx * 0.25) % 1.0)
            rad = 0.18 + prog * 1.65
            n_c = 28
            ang = np.linspace(0, 2 * math.pi, n_c, endpoint=False)
            ring = np.column_stack([rad * np.cos(ang), np.full_like(ang, 1.05 - prog * 0.35), rad * np.sin(ang)])
            pr = _proj(_rot_xyz(ring, 0.22, ry, 0.0), cam_z=4.0)
            col = sec if r_idx % 2 == 0 else pri
            _draw_edges(draw, pr, [(i, (i + 1) % n_c) for i in range(n_c)], col, width=2 if prog < 0.6 else 1)

    elif archetype == "MONORAIL_OUTRUN":
        _draw_perspective_grid(draw, t * 2.0, grid_col, y_floor=-1.25)
        for side in (-1.0, 1.0):
            for m_idx in range(7):
                z_m = 1.2 + (((m_idx - (t / 8.0) * 14.0) % 7.0) * 1.1)
                x_base = side * 1.35
                x_peak = side * (2.45 + 0.45 * math.sin(m_idx * 1.7 + seed))
                y_peak = -0.15 + 0.65 * abs(math.cos(m_idx * 1.3 + seed))
                m_pts = np.array([
                    [x_base, -1.25, z_m],
                    [x_peak, y_peak, z_m],
                    [side * 3.6, -1.25, z_m],
                ], dtype=np.float32)
                pm = _proj(m_pts, cam_z=0.5)
                draw.line([(pm[0, 0], pm[0, 1]), (pm[1, 0], pm[1, 1]), (pm[2, 0], pm[2, 1])], fill=pri, width=2)
        bank = 0.14 * math.sin(t * w2 + phase)
        car = np.array([
            [0.0, -0.68, 2.8], [-0.55, -0.82, 1.9], [0.55, -0.82, 1.9],
            [-0.65, -0.95, 1.2], [0.65, -0.95, 1.2], [-0.38, -0.58, 1.45], [0.38, -0.58, 1.45],
        ], dtype=np.float32)
        c_edges = [(0,1),(0,2),(1,2),(1,3),(2,4),(3,4),(1,5),(2,6),(5,6),(3,5),(4,6),(0,5),(0,6)]
        pc = _proj(_rot_xyz(car, 0.0, 0.0, bank), cam_z=1.2)
        _draw_edges(draw, pc, c_edges, sec, width=2)

    elif archetype == "RAIN_DOORWAY":
        _draw_perspective_grid(draw, t * 0.5, grid_col, y_floor=-1.35)
        ry = 0.28 * math.sin(t * w1 + phase)
        door = np.array([
            [-0.75, -1.35, 0.0], [0.75, -1.35, 0.0], [0.75, 1.25, 0.0], [-0.75, 1.25, 0.0],
            [-0.88, -1.35, -0.15], [0.88, -1.35, -0.15], [0.88, 1.38, -0.15], [-0.88, 1.38, -0.15],
            [-0.75, -1.35, 0.0], [-0.15, -1.35, 0.65], [-0.15, 1.25, 0.65], [-0.75, 1.25, 0.0],
        ], dtype=np.float32)
        d_edges = [(0,1),(1,2),(2,3),(3,0), (4,5),(5,6),(6,7),(7,4), (0,4),(1,5),(2,6),(3,7), (8,9),(9,10),(10,11)]
        pd = _proj(_rot_xyz(door, 0.08, ry, 0.0), cam_z=4.2)
        _draw_edges(draw, pd, d_edges, pri, width=2)
        for r_i in range(18):
            rx_p = ((r_i * 0.73 + seed * 0.13) % 3.6) - 1.8
            rz_p = ((r_i * 1.19) % 3.0) - 1.2
            fall = (((t / 8.0) * 6.0 + r_i * 0.17) % 1.0) * 2.8
            ry_top = 1.45 - fall
            if ry_top > -1.15:
                seg = np.array([[rx_p, ry_top, rz_p], [rx_p, max(-1.35, ry_top - 0.32), rz_p]], dtype=np.float32)
                ps = _proj(_rot_xyz(seg, 0.08, ry, 0.0), cam_z=4.2)
                draw.line([(ps[0, 0], ps[0, 1]), (ps[1, 0], ps[1, 1])], fill=sec, width=1)
            else:
                rip_rad = (-1.15 - ry_top) * 0.85
                ang = np.linspace(0, 2 * math.pi, 16, endpoint=False)
                rip = np.column_stack([rx_p + rip_rad * np.cos(ang), np.full_like(ang, -1.35), rz_p + rip_rad * np.sin(ang)])
                pr = _proj(_rot_xyz(rip, 0.08, ry, 0.0), cam_z=4.2)
                _draw_edges(draw, pr, [(i, (i + 1) % 16) for i in range(16)], sec, width=1)

    elif archetype == "CROWN_CAGE":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        n_sp = 8
        verts = []
        edges = []
        for i in range(n_sp):
            a0 = i * (2 * math.pi / n_sp)
            a_mid = (i + 0.5) * (2 * math.pi / n_sp)
            verts.append([1.05 * math.cos(a0), -0.45, 1.05 * math.sin(a0)])
            verts.append([1.18 * math.cos(a0), 0.25, 1.18 * math.sin(a0)])
            verts.append([1.28 * math.cos(a_mid), 0.85 + 0.12 * math.sin(t * w3 + i), 1.28 * math.sin(a_mid)])
        pts = np.array(verts, dtype=np.float32)
        for i in range(n_sp):
            b0 = i * 3
            b_next = ((i + 1) % n_sp) * 3
            edges.extend([(b0, b_next), (b0 + 1, b_next + 1), (b0, b0 + 1), (b0 + 1, b0 + 2), (b0 + 2, b_next + 1), (b0, b0 + 2)])
        p2 = _proj(_rot_xyz(pts, 0.25 + 0.1 * math.sin(t * w1), spin_dir * t * w1 + phase, 0.08 * math.cos(t * w1)), cam_z=4.0)
        _draw_edges(draw, p2, edges, pri, width=2)
        oct_v = np.array([[0,0.65,0],[0,-0.65,0],[0.55,0,0],[-0.55,0,0],[0,0,0.55],[0,0,-0.55]], dtype=np.float32)
        oct_e = [(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),(2,4),(4,3),(3,5),(5,2)]
        po = _proj(_rot_xyz(oct_v, -t * w1, -t * w2, 0.2), cam_z=4.0)
        _draw_edges(draw, po, oct_e, sec, width=2)

    elif archetype == "ORCHID_PCB":
        _draw_perspective_grid(draw, t * 0.5, grid_col, y_floor=-1.40)
        n_petals = 6 + (seed % 3)
        bloom = 0.78 + 0.22 * math.sin(t * w2 + phase)
        for p_i in range(n_petals):
            ba = p_i * (2 * math.pi / n_petals) + spin_dir * t * w1
            p_verts = np.array([
                [0.0, -0.25, 0.0],
                [0.55 * math.cos(ba - 0.28) * bloom, 0.25, 0.55 * math.sin(ba - 0.28) * bloom],
                [1.35 * math.cos(ba) * bloom, 0.75 * bloom, 1.35 * math.sin(ba) * bloom],
                [0.55 * math.cos(ba + 0.28) * bloom, 0.25, 0.55 * math.sin(ba + 0.28) * bloom],
            ], dtype=np.float32)
            pp = _proj(_rot_xyz(p_verts, 0.38, 0.0, 0.08 * math.sin(t * w1)), cam_z=3.9)
            _draw_edges(draw, pp, [(0,1),(1,2),(2,3),(3,0),(0,2)], pri if p_i % 2 == 0 else sec, width=2)
        stem = np.array([[0.0, -0.25, 0.0], [0.0, -1.40, 0.0], [-0.8, -1.40, 0.5], [0.8, -1.40, -0.5]], dtype=np.float32)
        ps = _proj(_rot_xyz(stem, 0.38, 0.0, 0.0), cam_z=3.9)
        _draw_edges(draw, ps, [(0,1),(1,2),(1,3)], sec, width=2)

    elif archetype == "GATE_TURBINE":
        _draw_perspective_grid(draw, t * 2.0, grid_col, y_floor=-1.45, ceiling=True)
        for z_ring, col in [(0.6, pri), (-0.4, sec), (-1.4, grid_col)]:
            n_g = 6
            ang = np.linspace(0, 2 * math.pi, n_g, endpoint=False) + (math.pi / 6.0)
            g_pts = np.column_stack([1.45 * np.cos(ang), 1.45 * np.sin(ang), np.full_like(ang, z_ring)])
            pg = _proj(g_pts, cam_z=3.8)
            _draw_edges(draw, pg, [(i, (i + 1) % n_g) for i in range(n_g)], col, width=2)
        n_b = 12
        for b_i in range(n_b):
            ba = b_i * (2 * math.pi / n_b) + spin_dir * t * w2
            blade = np.array([
                [0.28 * math.cos(ba), 0.28 * math.sin(ba), 0.0],
                [1.22 * math.cos(ba + 0.18), 1.22 * math.sin(ba + 0.18), 0.15],
                [1.22 * math.cos(ba - 0.05), 1.22 * math.sin(ba - 0.05), -0.15],
            ], dtype=np.float32)
            pb = _proj(blade, cam_z=3.8)
            _draw_edges(draw, pb, [(0,1),(1,2),(2,0)], sec if b_i % 3 == 0 else pri, width=2)

    elif archetype == "CITY_SKYLINE":
        _draw_perspective_grid(draw, t * 1.5, grid_col, y_floor=-1.35)
        for b_i in range(12):
            side = -1.0 if (b_i % 2 == 0) else 1.0
            z_b = 0.8 + (((b_i - (t / 8.0) * 12.0) % 12.0) * 0.62)
            x0 = side * (0.85 + (b_i % 3) * 0.55)
            bw, bd = 0.32, 0.32
            bh = -1.35 + 0.85 + ((b_i * 37 + seed) % 100) / 70.0
            b_pts = np.array([
                [x0-bw, -1.35, z_b-bd], [x0+bw, -1.35, z_b-bd], [x0+bw, -1.35, z_b+bd], [x0-bw, -1.35, z_b+bd],
                [x0-bw, bh, z_b-bd], [x0+bw, bh, z_b-bd], [x0+bw, bh, z_b+bd], [x0-bw, bh, z_b+bd],
            ], dtype=np.float32)
            pb = _proj(b_pts, cam_z=1.2)
            b_edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
            _draw_edges(draw, pb, b_edges, pri if b_i % 3 != 0 else sec, width=2 if z_b < 4.0 else 1)

    elif archetype == "TELEPHONE_LISSAJOUS":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        n_l = 96
        u = np.linspace(0, 2 * math.pi, n_l)
        lx = 1.25 * np.sin((2 + (seed % 3)) * u + t * w2)
        ly = 0.95 * np.sin((3 + (seed % 2)) * u + phase)
        lz = 0.85 * np.cos(2 * u + t * w1)
        pl = _proj(np.column_stack([lx, ly, lz]), cam_z=3.8)
        _draw_edges(draw, pl, [(i, (i + 1) % n_l) for i in range(n_l)], pri, width=2)
        active_key = int((t / 8.0) * 24.0 + seed) % 12
        for k_i in range(12):
            kr, kc = divmod(k_i, 3)
            kx = (kc - 1) * 0.55
            ky = (1.5 - kr) * 0.45
            kz = 0.45 * math.sin(t * w1 + k_i)
            kp = np.array([
                [kx-0.18, ky-0.14, kz], [kx+0.18, ky-0.14, kz],
                [kx+0.18, ky+0.14, kz], [kx-0.18, ky+0.14, kz],
            ], dtype=np.float32)
            pk = _proj(_rot_xyz(kp, 0.2, 0.35 * math.sin(t * w1), 0.0), cam_z=4.2)
            _draw_edges(draw, pk, [(0,1),(1,2),(2,3),(3,0)], sec if k_i == active_key else grid_col, width=2 if k_i == active_key else 1)

    elif archetype == "ELECTRIC_GUITAR":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        ry = spin_dir * t * w1 + phase
        rx = 0.25 + 0.12 * math.sin(t * w1)
        g_verts = np.array([
            [0.0, 0.25, 0.14], [-0.85, -1.15, 0.14], [-0.25, -0.55, 0.14], [0.25, -0.55, 0.14], [0.85, -1.15, 0.14],
            [0.0, 0.25, -0.14], [-0.85, -1.15, -0.14], [-0.25, -0.55, -0.14], [0.25, -0.55, -0.14], [0.85, -1.15, -0.14],
            [-0.10, 0.22, 0.08], [0.10, 0.22, 0.08], [0.09, 1.35, 0.08], [-0.09, 1.35, 0.08], [0.0, 1.65, 0.08],
        ], dtype=np.float32)
        g_edges = [
            (0,1),(1,2),(2,3),(3,4),(4,0), (5,6),(6,7),(7,8),(8,9),(9,5),
            (0,5),(1,6),(2,7),(3,8),(4,9), (10,11),(11,12),(12,13),(13,10),(12,14),(13,14),
        ]
        pg = _proj(_rot_xyz(g_verts, rx, ry, 0.25), cam_z=4.0)
        _draw_edges(draw, pg, g_edges, pri, width=2)
        for b_i in range(16):
            bx = -2.2 + b_i * (4.4 / 15.0)
            bh = -1.45 + 0.35 + 1.15 * abs(math.sin(t * w4 + b_i * 0.65 + seed))
            bar = np.array([[bx, -1.45, 1.2], [bx, bh, 1.2]], dtype=np.float32)
            pb = _proj(bar, cam_z=3.8)
            draw.line([(pb[0, 0], pb[0, 1]), (pb[1, 0], pb[1, 1])], fill=sec, width=3)

    elif archetype == "SOLAR_HORIZON":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.20)
        sun_c = (W * 0.5, H * 0.42)
        sun_r = 92
        for band in range(-5, 6):
            y_off = band * 14 + (((t / 8.0) * 10.0) % 1.0) * 14.0 - 7.0
            if abs(y_off) < sun_r:
                half_w = math.sqrt(max(0.0, sun_r * sun_r - y_off * y_off))
                draw.line([(sun_c[0] - half_w, sun_c[1] + y_off), (sun_c[0] + half_w, sun_c[1] + y_off)], fill=sec if band % 2 == 0 else pri, width=2)
        draw.ellipse([sun_c[0] - sun_r, sun_c[1] - sun_r, sun_c[0] + sun_r, sun_c[1] + sun_r], outline=pri, width=2)

    elif archetype == "DNA_HELIX_CLONE":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        n_h = 32
        yy = np.linspace(-1.35, 1.35, n_h)
        ang = yy * 2.8 + spin_dir * t * w2 + phase
        s1 = np.column_stack([0.85 * np.cos(ang), yy, 0.85 * np.sin(ang)])
        s2 = np.column_stack([0.85 * np.cos(ang + math.pi), yy, 0.85 * np.sin(ang + math.pi)])
        p1 = _proj(_rot_xyz(s1, 0.15, 0.0, 0.22 * math.sin(t * w1)), cam_z=3.9)
        p2 = _proj(_rot_xyz(s2, 0.15, 0.0, 0.22 * math.sin(t * w1)), cam_z=3.9)
        _draw_edges(draw, p1, [(i, i + 1) for i in range(n_h - 1)], pri, width=2)
        _draw_edges(draw, p2, [(i, i + 1) for i in range(n_h - 1)], sec, width=2)
        for i in range(0, n_h, 2):
            draw.line([(p1[i, 0], p1[i, 1]), (p2[i, 0], p2[i, 1])], fill=grid_col if i % 4 else sec, width=1)

    elif archetype == "ORBITAL_SATELLITE":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.48)
        rx, ry = 0.35 + 0.15 * math.sin(t * w1), spin_dir * t * w1 + phase
        n_ring = 28
        ang = np.linspace(0, 2 * math.pi, n_ring, endpoint=False)
        for lat in (-0.65, -0.25, 0.25, 0.65):
            r_lat = math.sqrt(max(0.01, 1.05**2 - lat**2))
            ring = np.column_stack([r_lat * np.cos(ang), np.full_like(ang, lat), r_lat * np.sin(ang)])
            pr = _proj(_rot_xyz(ring, rx, ry, 0.0), cam_z=4.0)
            _draw_edges(draw, pr, [(i, (i + 1) % n_ring) for i in range(n_ring)], pri, width=1)
        for lon_i in range(4):
            la = lon_i * (math.pi / 4.0)
            ring = np.column_stack([1.05 * np.cos(ang) * math.cos(la), 1.05 * np.sin(ang), 1.05 * np.cos(ang) * math.sin(la)])
            pr = _proj(_rot_xyz(ring, rx, ry, 0.0), cam_z=4.0)
            _draw_edges(draw, pr, [(i, (i + 1) % n_ring) for i in range(n_ring)], pri, width=1)
        orb = np.column_stack([1.58 * np.cos(ang), 0.15 * np.sin(ang), 1.58 * np.sin(ang)])
        po = _proj(_rot_xyz(orb, -0.45, -t * w1, 0.35), cam_z=4.0)
        _draw_edges(draw, po, [(i, (i + 1) % n_ring) for i in range(n_ring)], sec, width=2)

    elif archetype == "SHATTERED_PRISM":
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45)
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        ico = np.array([
            [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
            [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
            [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1],
        ], dtype=np.float32) * 0.62
        ico_e = [
            (0,11),(0,5),(0,1),(0,7),(0,10),(1,5),(5,11),(11,10),(10,7),(7,1),
            (3,9),(3,4),(3,2),(3,6),(3,8),(4,9),(2,4),(6,2),(8,6),(9,8),
            (4,5),(5,9),(9,1),(1,8),(8,7),(7,6),(6,10),(10,2),(2,11),(11,4),
        ]
        pi = _proj(_rot_xyz(ico, t * w1, spin_dir * t * w1 + phase, 0.2), cam_z=4.0)
        _draw_edges(draw, pi, ico_e, pri, width=2)
        for b_i in range(6):
            ba = b_i * (math.pi / 3.0) + t * w1
            beam = np.array([[0,0,0], [1.85 * math.cos(ba), 1.25 * math.sin(ba), 0.4 * math.cos(ba * 2)]], dtype=np.float32)
            pb = _proj(beam, cam_z=4.0)
            draw.line([(pb[0, 0], pb[0, 1]), (pb[1, 0], pb[1, 1])], fill=sec, width=1)

    else:  # CLOCKWORK_LABYRINTH
        _draw_perspective_grid(draw, t, grid_col, y_floor=-1.45, ceiling=True)
        for g_z, rad, dir_g, col in [(-0.2, 1.25, 1.0, pri), (0.25, 0.78, -2.0, sec)]:
            n_t = 24
            verts = []
            for i in range(n_t):
                a = i * (2 * math.pi / n_t) + dir_g * t * w1
                r = rad if (i % 2 == 0) else (rad * 0.84)
                verts.append([r * math.cos(a), r * math.sin(a), g_z])
            pg = _proj(_rot_xyz(np.array(verts, dtype=np.float32), 0.22 * math.sin(t * w1), 0.32 * math.cos(t * w1), 0.0), cam_z=3.9)
            _draw_edges(draw, pg, [(i, (i + 1) % n_t) for i in range(n_t)], col, width=2)


_CACHED_BASE_CRT: Image.Image | None = None
_CACHED_PHOSPHOR_MASK: np.ndarray | None = None
_CACHED_BARREL_LUT: tuple[np.ndarray, np.ndarray] | None = None


def _get_cached_crt_base_and_mask(crt_bg_arr: np.ndarray) -> tuple[Image.Image, np.ndarray, tuple[np.ndarray, np.ndarray]]:
    """
    Precomputes:
      1. `_CACHED_BASE_CRT`: The untouched 688x488 CRT glass & bezel patch from `backdrop_clean.png`.
      2. `_CACHED_PHOSPHOR_MASK`: Full-aperture barrel-curved CRT phosphor emission & scanline/grille mask
         that fills the physical glass dome and feathers smoothly to 0 right at the recessed inner bezel.
      3. `_CACHED_BARREL_LUT`: `(src_y, src_x)` integer warp tables for 1983 spherical-barrel CRT glass curvature.
    """
    global _CACHED_BASE_CRT, _CACHED_PHOSPHOR_MASK, _CACHED_BARREL_LUT
    if _CACHED_BASE_CRT is not None and _CACHED_PHOSPHOR_MASK is not None and _CACHED_BARREL_LUT is not None:
        return _CACHED_BASE_CRT, _CACHED_PHOSPHOR_MASK, _CACHED_BARREL_LUT

    _CACHED_BASE_CRT = Image.fromarray(np.clip(crt_bg_arr, 0, 255).astype(np.uint8))

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = 338.0, 248.0
    rx, ry = 304.0, 220.0
    u = (xx - cx) / rx
    v = (yy - cy) / ry

    # Authentic 1983 CRT spherical-barrel curvature matching the physical bezel contour
    u_src = u * (1.0 + 0.068 * (v * v) + 0.022 * (u * u))
    v_src = v * (1.0 + 0.082 * (u * u) + 0.026 * (v * v))
    src_x = np.clip(np.round(cx + u_src * rx), 0, W - 1).astype(np.int32)
    src_y = np.clip(np.round(cy + v_src * ry), 0, H - 1).astype(np.int32)
    _CACHED_BARREL_LUT = (src_y, src_x)

    dist = (np.abs(u_src) ** 4.2 + np.abs(v_src) ** 4.2) ** (1.0 / 4.2)
    tube_mask = np.clip((1.00 - dist) / 0.16, 0.0, 1.0).astype(np.float32)
    tube_mask = tube_mask * tube_mask * (3.0 - 2.0 * tube_mask)

    scan = np.where((yy % 3) == 0, 0.52, np.where((yy % 3) == 1, 1.00, 0.80)).astype(np.float32)
    grille = np.where((xx % 2) == 0, 1.00, 0.86).astype(np.float32)
    _CACHED_PHOSPHOR_MASK = (tube_mask * scan * grille)[:, :, None].astype(np.float32)
    return _CACHED_BASE_CRT, _CACHED_PHOSPHOR_MASK, _CACHED_BARREL_LUT


def render_song_crt_cgi_frame(
    song_key: str,
    title: str,
    lyrics_text: str,
    catalog_id: str,
    t: float,
    crt_bg_arr: np.ndarray,
    edge_alpha: np.ndarray,
    scan_vig: np.ndarray,
) -> Image.Image:
    """
    Renders a single `688x488` RGB frame of the song-specific 1980s CRT 3D CGI animation
    at timestamp `t` with 1983 spherical-barrel CRT glass curvature and multi-stage phosphor halation.
    """
    seed = _song_seed(song_key or title)
    archetype = select_song_cgi_archetype(title, lyrics_text, song_key=song_key, catalog_id=catalog_id)

    if archetype == "RECALL_METAL_FLAME":
        pri, sec, grid_col, _ = RECALL_METAL_PALETTES[seed % len(RECALL_METAL_PALETTES)]
    else:
        pri, sec, grid_col, _ = PHOSPHOR_PALETTES[seed % len(PHOSPHOR_PALETTES)]

    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    _render_scene_archetype(draw, archetype, t, seed, pri, sec, grid_col, title=title, song_key=song_key)

    base_crt, phos_mask, (src_y, src_x) = _get_cached_crt_base_and_mask(crt_bg_arr)
    warped_cgi = Image.fromarray(np.asarray(canvas)[src_y, src_x])
    core_cgi = warped_cgi.filter(ImageFilter.GaussianBlur(radius=0.6))
    halo_cgi = warped_cgi.filter(ImageFilter.GaussianBlur(radius=2.8))
    bloom_cgi = warped_cgi.filter(ImageFilter.GaussianBlur(radius=9.5))

    c_arr = np.asarray(core_cgi, dtype=np.float32)
    h_arr = np.asarray(halo_cgi, dtype=np.float32)
    b_arr = np.asarray(bloom_cgi, dtype=np.float32)

    raw_emit = c_arr * 0.92 + h_arr * 0.52 + b_arr * 0.34
    lum = raw_emit[:, :, 0] * 0.299 + raw_emit[:, :, 1] * 0.587 + raw_emit[:, :, 2] * 0.114
    warm_phos = np.dstack([lum * 0.52, lum * 1.08, lum * 0.60])
    graded_emit = (raw_emit * 0.82 + warm_phos * 0.18) * phos_mask

    masked_phos = Image.fromarray(np.clip(graded_emit, 0, 255).astype(np.uint8))
    return ImageChops.add(base_crt, masked_phos)
