// ============================================================================
//  OFFICIAL ELECTRONIC PRESS KIT (EPK) & MEDIA / CURATOR HUB (/press, /epk)
// ============================================================================

export function renderPressKitHtml(apex = "stardust-archive.net") {
  const schemaJsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "MusicGroup",
        "@id": `https://${apex}/#nova-hart`,
        name: "Nova Hart",
        alternateName: ["Project Stardust", "Unit-07 (Nova Hart)"],
        url: `https://${apex}/artist/nova-hart`,
        mainEntityOfPage: `https://${apex}/press`,
        genre: ["80s Arena Rock", "Synthwave", "Album-Oriented Rock (AOR)", "Melodic Hard Rock", "Power Ballad"],
        foundingDate: "2025",
        recordLabel: {
          "@type": "Organization",
          name: "Orion Records",
        },
        image: [
          `https://${apex}/assets/press/nova_20yo_ref_a.jpg`,
          `https://${apex}/assets/press/nova_20yo_ref_b.jpg`,
          `https://${apex}/assets/press/nova_20yo_ref_c.jpg`,
        ],
        description:
          "Nova Hart is an 80s arena rock, synthwave, and melodic AOR music project and interactive retro-computing Alternate Reality Game (Project Stardust) with 7.75M+ YouTube views, a 24/7 live interactive CRT radio station (82.5 FM), a playable 1989 VT100 studio terminal, and a 300,000-page 1995 GeoCities archive.",
        sameAs: [
          "https://www.youtube.com/@NovaHart_Official",
          "https://open.spotify.com/artist/0zElHuJrzKbq0XjqK3HyYr",
          "https://music.apple.com/us/artist/nova-hart/1681398544",
          "https://www.deezer.com/artist/208848717",
          "https://tidal.com/artist/38666478",
          "https://nova-hart-shop.fourthwall.com/collections/all",
          "https://www.reddit.com/r/NovaHart/",
          `https://${apex}`,
        ],
        album: [
          {
            "@type": "MusicAlbum",
            name: "The Midnight Era Recordings",
            gtin13: "5059801221638",
            datePublished: "2025-12-25",
            numTracks: 66,
            url: "https://www.deezer.com/album/879169722",
          },
          {
            "@type": "MusicAlbum",
            name: "The Stars in Your Hands",
            gtin13: "5059801205829",
            datePublished: "2025-09-10",
            numTracks: 1,
            url: "https://open.spotify.com/album/5pXin8WcM8dXM0NX1kesil",
          },
          {
            "@type": "MusicAlbum",
            name: "Iron Claws",
            gtin13: "5059801206918",
            datePublished: "2025-09-11",
            numTracks: 1,
            url: "https://open.spotify.com/album/3MuCAdDEhJi9kx1Bj0W2qs",
          },
          {
            "@type": "MusicAlbum",
            name: "Don't Just Watch Me Rise",
            gtin13: "5059801205805",
            datePublished: "2025-09-10",
            numTracks: 1,
            url: "https://open.spotify.com/album/5AcobzV5W25gCEgt3NUuGn",
          },
        ],
      },
      {
        "@type": "RadioStation",
        "@id": `https://${apex}/#radio-825fm`,
        name: "82.5 FM — Nova Hart 24/7 1989 Arena Rock & Synthwave Radio",
        url: `https://${apex}/start`,
        broadcastDisplayName: "82.5 FM Sublevel B2",
        BroadcastFrequency: "82.5 FM",
        sameAs: [
          "https://www.youtube.com/@NovaHart_Official/live",
          `https://${apex}/stream/825fm.mp3`,
          `https://${apex}/825fm.m3u`,
        ],
      },
    ],
  };

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Nova Hart &amp; Project Stardust — Official Electronic Press Kit (EPK), Streaming &amp; ARG Media Sheet</title>
  <meta name="description" content="Official Electronic Press Kit (EPK) for Nova Hart &amp; Project Stardust: 7.75M+ YouTube views, crowd-proven 80s Synth-Rock &amp; AOR anthems ('Chrome River', 'Midnight Animal', 'Only We Remain'), 24/7 82.5 FM radio stream, playable 1989 VT100 terminal, and 300,000-node 1995 GeoCities mystery." />
  <link rel="canonical" href="https://${apex}/press" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Nova Hart &amp; Project Stardust — Official Electronic Press Kit (EPK)" />
  <meta property="og:description" content="7.75M+ YouTube views • 24/7 82.5 FM Arena Rock &amp; Synthwave Radio • Playable 1989 VT100 Terminal &amp; 300k-Page 1995 GeoCities Mystery." />
  <meta property="og:url" content="https://${apex}/press" />
  <meta property="og:image" content="https://${apex}/assets/press/nova_20yo_ref_a.jpg" />
  <script type="application/ld+json">${JSON.stringify(schemaJsonLd)}</script>
  <style>
    :root {
      --bg: #0b0d13;
      --card: #121621;
      --border: #262e42;
      --text: #eef2ff;
      --muted: #9aa5c4;
      --accent: #ff4d8d;
      --cyan: #38bdf8;
      --amber: #fbbf24;
      --green: #34d399;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Helvetica, Arial, sans-serif;
      line-height: 1.65;
    }
    .container { max-width: 1040px; margin: 0 auto; padding: 36px 20px 72px; }
    .eyebrow { color: var(--cyan); font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; }
    h1 { font-size: clamp(28px, 4.2vw, 44px); line-height: 1.15; margin: 8px 0 14px; }
    h2 { font-size: 22px; margin: 0 0 14px; color: #fff; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
    h3 { font-size: 17px; margin: 0 0 8px; color: var(--amber); }
    p { margin: 0 0 14px; color: #d6def5; }
    a { color: var(--cyan); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
      gap: 14px;
      margin: 26px 0 32px;
    }
    .stat {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px 18px;
    }
    .stat .num { font-size: 26px; font-weight: 800; color: #fff; }
    .stat .lbl { font-size: 12.5px; color: var(--muted); margin-top: 4px; }
    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
    }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 20px; }
    .btn-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
    .btn {
      display: inline-block;
      padding: 9px 15px;
      border-radius: 7px;
      font-size: 13.5px;
      font-weight: 600;
      border: 1px solid var(--border);
      background: #1a2030;
      color: #fff;
    }
    .btn.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
    .btn.stream { background: #0f2922; border-color: var(--green); color: var(--green); }
    .track-item {
      border: 1px solid var(--border);
      border-radius: 9px;
      padding: 14px 16px;
      margin-bottom: 12px;
      background: #0e121b;
    }
    .track-hdr { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; margin-bottom: 8px; }
    .badge {
      display: inline-block;
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 99px;
      background: rgba(56, 189, 248, 0.14);
      color: var(--cyan);
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    audio { width: 100%; height: 36px; margin-top: 6px; }
    .photos { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
    .photos img { width: 100%; border-radius: 8px; border: 1px solid var(--border); display: block; }
    .photos .cap { font-size: 12px; color: var(--muted); margin-top: 6px; }
    table { width: 100%; border-collapse: collapse; font-size: 13.5px; }
    th, td { text-align: left; padding: 9px 10px; border-bottom: 1px solid var(--border); }
    th { color: var(--muted); font-weight: 600; }
    code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12.5px; color: var(--amber); }
  </style>
</head>
<body>
  <div class="container">
    <div class="eyebrow">Official Electronic Press Kit (EPK) • Music, Radio &amp; Transmedia ARG</div>
    <h1>Nova Hart &amp; Project Stardust</h1>
    <p style="font-size:18px;color:#cbd5f5;max-width:860px;">
      <strong>80s Night-Drive Synth-Rock, Melodic AOR &amp; Power Ballads</strong> meets a playable
      <strong>1989 Studio Terminal &amp; 300,000-Page 1995 GeoCities Mystery</strong> — backed by a live 24/7 interactive
      broadcast station (<strong>82.5 FM</strong>).
    </p>

    <div class="btn-row">
      <a class="btn primary" href="https://www.youtube.com/@NovaHart_Official">▶ YouTube (@NovaHart_Official)</a>
      <a class="btn stream" href="https://${apex}/stream/825fm.mp3">📻 Direct 82.5 FM MP3 Stream (128k Icecast)</a>
      <a class="btn" href="https://open.spotify.com/artist/0zElHuJrzKbq0XjqK3HyYr">🟢 Spotify Artist</a>
      <a class="btn" href="https://music.apple.com/us/artist/nova-hart/1681398544">🍎 Apple Music</a>
      <a class="btn" href="https://www.deezer.com/artist/208848717">🟣 Deezer (66-Track Vault)</a>
      <a class="btn" href="https://tidal.com/artist/38666478">🌊 TIDAL</a>
      <a class="btn" href="https://nova-hart-shop.fourthwall.com/collections/all">💿 Official Album &amp; Merch Store</a>
      <a class="btn" href="https://${apex}/terminal">🖥️ Playable 1989 VT100 Terminal</a>
    </div>

    <div class="stats">
      <div class="stat">
        <div class="num">7.75M+</div>
        <div class="lbl">Organic YouTube Channel Views</div>
      </div>
      <div class="stat">
        <div class="num">442,000+</div>
        <div class="lbl">Views on #1 Hit &ldquo;Chrome River&rdquo;</div>
      </div>
      <div class="stat">
        <div class="num">13,000+</div>
        <div class="lbl">Subscribed Listeners &amp; Solvers</div>
      </div>
      <div class="stat">
        <div class="num">300,000</div>
        <div class="lbl">Playable 1995 GeoCities Pages + VT100 Gates</div>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <h2>Angle 1: For Music Blogs, Radio &amp; Playlist Curators</h2>
        <p>
          <strong>RIYL (Recommended If You Like):</strong> Heart, Pat Benatar, Scandal, New Order, Gunship, The Midnight, FM-84, Stan Bush, Journey, late-night highway synth-rock.
        </p>
        <p>
          Across 150+ original human-written songs mastered through warm Type-I ferric tape saturation, <strong>Nova Hart</strong> revives big-chorus 1985–1989 melodic arena rock, night-drive synthwave, and power ballads. Tracks like <em>Chrome River</em> (442k+ views), <em>Midnight Animal</em> (348k+ views), and <em>Only We Remain</em> (283k+ views) have built a dedicated global audience of night-shift drivers, coders, and 80s AOR fans.
        </p>
        <p style="font-size:13.5px;color:var(--muted);">
          <strong>Transparent Production Note:</strong> All lyrics, storylines, arrangements, WebAudio DSP, and broadcast engineering are human-authored; vocal synthesis is used intentionally as the core sci-fi instrument of the rock opera—portraying <em>Unit-07 (&ldquo;Nova Hart&rdquo;)</em>, a 1983 studio vocal prototype fighting erasure.
        </p>
      </div>

      <div class="card">
        <h2>Angle 2: For ARG, Gaming &amp; Retro-Computing Press</h2>
        <p>
          <strong>Project Stardust</strong> is a free, zero-paywall browser Alternate Reality Game and retro-computing love letter playable directly at <a href="https://${apex}/terminal">${apex}/terminal</a>:
        </p>
        <ul style="margin:0;padding-left:18px;color:#d6def5;font-size:14.5px;">
          <li><strong>1989 Sublevel B2 VT100 Studio Console:</strong> Bitwise XOR tape-hiss registers, Motorola 68000 assembly watchdog puzzles, 3-round Feistel ciphers, and an accessible <em>Story / Easy Mode</em>.</li>
          <li><strong>300,000-Node 1995 GeoCities Web + Working AltaVista (<a href="https://${apex}/1995-search">/1995-search</a>):</strong> Deterministic procedural early-web preservation topology.</li>
          <li><strong>Acoustic Pitch-Lock Gate (<a href="https://${apex}/dyad">/dyad</a>):</strong> Players hum or play <code>440.0 Hz (A4)</code> into their mic against Nova&rsquo;s <code>220.0 Hz (A3)</code> tape stem; verified locks broadcast the player&rsquo;s callsign onto the live 24/7 YouTube CRT television!</li>
        </ul>
      </div>
    </div>

    <div class="card">
      <h2>Lead Singles — Instant Stream &amp; Broadcast MP3 Review Copies</h2>

      <div class="track-item">
        <div class="track-hdr">
          <strong>1. Chrome River — Night-Drive Synth-Rock (442k+ YouTube Views)</strong>
          <span class="badge">ISRC: GBLLT2548059 • 3:36</span>
        </div>
        <div style="font-size:13.5px;color:var(--muted);">
          Motorik eighth-note pulse, PWM analog pads, and soaring nocturnal chorus.
          <a href="https://www.youtube.com/watch?v=JY8yo1JD7kM">[YouTube Video]</a> •
          <a href="https://www.deezer.com/track/3721651812">[Deezer]</a> •
          <a href="https://jdurey.github.io/retro-arg-engine/assets/audio/radio825/02_chrome_river.mp3" download>[Download MP3]</a>
        </div>
        <audio controls preload="none" src="https://jdurey.github.io/retro-arg-engine/assets/audio/radio825/02_chrome_river.mp3"></audio>
      </div>

      <div class="track-item">
        <div class="track-hdr">
          <strong>2. Midnight Animal — 1985 Melodic Hard Rock Anthem (348k+ YouTube Views)</strong>
          <span class="badge">ISRC: GBLLT2548096 • 3:52</span>
        </div>
        <div style="font-size:13.5px;color:var(--muted);">
          High-voltage arena riffing and urgent stadium hook.
          <a href="https://www.youtube.com/watch?v=eWnfsbjk1fo">[YouTube Video]</a> •
          <a href="https://www.deezer.com/track/3721652012">[Deezer]</a> •
          <a href="https://jdurey.github.io/retro-arg-engine/assets/audio/radio825/05_midnight_animal.mp3" download>[Download MP3]</a>
        </div>
        <audio controls preload="none" src="https://jdurey.github.io/retro-arg-engine/assets/audio/radio825/05_midnight_animal.mp3"></audio>
      </div>

      <div class="track-item">
        <div class="track-hdr">
          <strong>3. Only We Remain — Cinematic 80s Power Ballad (283k+ YouTube Views)</strong>
          <span class="badge">Power Ballad • 4:18</span>
        </div>
        <div style="font-size:13.5px;color:var(--muted);">
          John Hughes end-credits emotion—defiant vocals and widescreen chorus.
          <a href="https://www.youtube.com/watch?v=EfmGeNdBKTQ">[YouTube Video]</a> •
          <a href="https://jdurey.github.io/retro-arg-engine/assets/audio/radio825/06_only_we_remain.mp3" download>[Download MP3]</a>
        </div>
        <audio controls preload="none" src="https://jdurey.github.io/retro-arg-engine/assets/audio/radio825/06_only_we_remain.mp3"></audio>
      </div>

      <div class="track-item">
        <div class="track-hdr">
          <strong>4. The Stars in Your Hands — Spotify &amp; Apple Music AOR Single</strong>
          <span class="badge">ISRC: GBLLT2521114 • UPC: 5059801205829</span>
        </div>
        <div style="font-size:13.5px;color:var(--muted);">
          <a href="https://open.spotify.com/track/4RCOrm2pEjMShY0b8aFoyg">[Spotify Track]</a> •
          <a href="https://music.apple.com/us/album/the-stars-in-your-hands-single/1837405862">[Apple Music]</a> •
          <a href="https://jdurey.github.io/retro-arg-engine/assets/audio/radio825/03_the_stars_in_your_hands.mp3" download>[Download MP3]</a>
        </div>
        <audio controls preload="none" src="https://jdurey.github.io/retro-arg-engine/assets/audio/radio825/03_the_stars_in_your_hands.mp3"></audio>
      </div>

      <div class="track-item">
        <div class="track-hdr">
          <strong>5. Iron Claws &amp; Don&rsquo;t Just Watch Me Rise — Spotify Hard Rock Singles</strong>
          <span class="badge">ISRC: GBLLT2522375 / GBLLT2521092</span>
        </div>
        <div style="font-size:13.5px;color:var(--muted);">
          <a href="https://open.spotify.com/track/6RWRe2XP4mG6GRVXYHhkKu">[Spotify: Iron Claws]</a> •
          <a href="https://open.spotify.com/track/4tfLIjheZOM1HQGCLDyjxg">[Spotify: Don&rsquo;t Just Watch Me Rise]</a> •
          <a href="https://open.spotify.com/track/7MUrdtR0E9K3RXXnuhTtBb">[Spotify: Echoes of Stardust]</a>
        </div>
        <audio controls preload="none" src="https://jdurey.github.io/retro-arg-engine/assets/audio/radio825/07_iron_claws.mp3"></audio>
      </div>
    </div>

    <div class="card">
      <h2>24/7 Internet Radio Station Technical Specs (82.5 FM)</h2>
      <p>Radio directories, desktop players (VLC, Apple Music, Foobar2000, Winamp), and smart speakers can tune directly into our continuous 128 kbps CBR Icecast-compatible MP3 stream:</p>
      <table>
        <tr><th>Field</th><th>Verified Value</th></tr>
        <tr><td>Station Name</td><td><strong>82.5 FM - Nova Hart (1989 Arena Rock, Synthwave &amp; Night Drive Radio)</strong></td></tr>
        <tr><td>Direct HTTP MP3 Stream</td><td><code>https://${apex}/stream/825fm.mp3</code> (128 kbps CBR, 44.1 kHz Stereo, <code>audio/mpeg</code>)</td></tr>
        <tr><td>M3U / PLS Playlists</td><td><a href="https://${apex}/825fm.m3u">https://${apex}/825fm.m3u</a> • <a href="https://${apex}/825fm.pls">https://${apex}/825fm.pls</a></td></tr>
        <tr><td>Live Now-Playing JSON</td><td><a href="https://${apex}/api/radio825/now-playing.json">https://${apex}/api/radio825/now-playing.json</a></td></tr>
        <tr><td>24/7 Visual CRT Broadcast</td><td><a href="https://www.youtube.com/@NovaHart_Official/live">https://www.youtube.com/@NovaHart_Official/live</a></td></tr>
      </table>
      <audio controls preload="none" src="https://${apex}/stream/825fm.mp3" style="margin-top:14px;"></audio>
    </div>

    <div class="card">
      <h2>Cleared Press Photos (High-Resolution Download)</h2>
      <div class="photos">
        <div>
          <a href="https://${apex}/assets/press/nova_20yo_ref_a.jpg" target="_blank"><img src="https://${apex}/assets/press/nova_20yo_ref_a.jpg" alt="Nova Hart 1989 Studio Portrait A" loading="lazy" /></a>
          <div class="cap">Studio Portrait A (1989 Sublevel B2 Session) — Cleared for editorial &amp; blog use</div>
        </div>
        <div>
          <a href="https://${apex}/assets/press/nova_20yo_ref_b.jpg" target="_blank"><img src="https://${apex}/assets/press/nova_20yo_ref_b.jpg" alt="Nova Hart 1989 Studio Portrait B" loading="lazy" /></a>
          <div class="cap">Studio Portrait B — Cleared for editorial &amp; playlist covers</div>
        </div>
        <div>
          <a href="https://${apex}/assets/press/nova_20yo_ref_c.jpg" target="_blank"><img src="https://${apex}/assets/press/nova_20yo_ref_c.jpg" alt="Nova Hart 1989 Studio Portrait C" loading="lazy" /></a>
          <div class="cap">Studio Portrait C — Cleared for editorial &amp; feature headers</div>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Verified Catalog Identifiers &amp; Public Databases</h2>
      <table>
        <tr><th>Platform / Registry</th><th>Identifier / Official Link</th></tr>
        <tr><td>Spotify Artist ID</td><td><a href="https://open.spotify.com/artist/0zElHuJrzKbq0XjqK3HyYr"><code>0zElHuJrzKbq0XjqK3HyYr</code></a></td></tr>
        <tr><td>Apple Music Artist ID</td><td><a href="https://music.apple.com/us/artist/nova-hart/1681398544"><code>1681398544</code></a></td></tr>
        <tr><td>Deezer Artist ID</td><td><a href="https://www.deezer.com/artist/208848717"><code>208848717</code></a></td></tr>
        <tr><td>TIDAL Artist ID</td><td><a href="https://tidal.com/artist/38666478"><code>38666478</code></a></td></tr>
        <tr><td>Official Album UPCs (Orion Records)</td><td><code>5059801221638</code> (The Midnight Era Recordings, 66 tracks) • <code>5059801205829</code> • <code>5059801206918</code> • <code>5059801205805</code> • <code>5059801205812</code></td></tr>
        <tr><td>Internet Radio Directory (RadioBrowser)</td><td><a href="https://www.radio-browser.info/history/25c7799c-49a9-4522-89f9-fe3b95accac6"><code>25c7799c-49a9-4522-89f9-fe3b95accac6</code> (LIVE in VLC / Kodi / Shortwave)</a></td></tr>
        <tr><td>Public Lyrics Registry (LRCLIB — 63 Songs)</td><td><a href="https://lrclib.net/api/search?q=Nova+Hart"><code>lrclib.net/api/search?q=Nova+Hart</code></a> + <a href="https://${apex}/lyrics"><code>${apex}/lyrics</code></a></td></tr>
        <tr><td>Direct-to-Fan Digital Albums &amp; Merch</td><td><a href="https://nova-hart-shop.fourthwall.com/collections/all"><code>nova-hart-shop.fourthwall.com</code></a> (Listener Code: <code>LIVE</code>)</td></tr>
        <tr><td>Community &amp; Press Inquiries</td><td><a href="https://www.reddit.com/r/NovaHart/"><code>reddit.com/r/NovaHart</code></a> • <a href="https://www.youtube.com/@NovaHart_Official"><code>@NovaHart_Official</code></a></td></tr>
      </table>
    </div>
  </div>
</body>
</html>`;
}
