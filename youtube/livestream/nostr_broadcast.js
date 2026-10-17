import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { generateSecretKey, getPublicKey, finalizeEvent } from 'nostr-tools/pure';
import { Relay, useWebSocketImplementation } from 'nostr-tools/relay';
import WebSocket from 'ws';

useWebSocketImplementation(WebSocket);

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const CREDS_PATH = path.join(__dirname, 'nostr_credentials.json');

let sk, pk;

if (fs.existsSync(CREDS_PATH)) {
    const creds = JSON.parse(fs.readFileSync(CREDS_PATH, 'utf-8'));
    sk = new Uint8Array(Buffer.from(creds.privkey, 'hex'));
    pk = creds.pubkey;
} else {
    sk = generateSecretKey();
    pk = getPublicKey(sk);
    fs.writeFileSync(CREDS_PATH, JSON.stringify({
        privkey: Buffer.from(sk).toString('hex'),
        pubkey: pk
    }, null, 2));
}

console.log(`[NOSTR] Identity pubkey: ${pk}`);

const RELAYS = [
    'wss://relay.damus.io',
    'wss://nos.lol',
    'wss://relay.primal.net',
    'wss://nostr.mom',
    'wss://relay.snort.social',
    'wss://yabu.me',
    'wss://relay-jp.nostr.wirednet.jp',
    'wss://offchain.pub'
];

async function broadcastEvent(eventTemplate) {
    const signedEvent = finalizeEvent(eventTemplate, sk);
    console.log(`[NOSTR] Broadcasting Signed Event ID: ${signedEvent.id} (Kind: ${signedEvent.kind})`);

    for (const url of RELAYS) {
        try {
            const connectPromise = Relay.connect(url);
            const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 4000));
            const relay = await Promise.race([connectPromise, timeoutPromise]);
            await relay.publish(signedEvent);
            console.log(`[NOSTR] ✓ Published to ${url}`);
            try { relay.close(); } catch (_) {}
        } catch (err) {
            console.warn(`[NOSTR] ⚠ ${url}: ${err.message || err}`);
        }
    }
}

async function main() {
    const args = process.argv.slice(2);
    let customTitle = null;
    let customContent = null;
    let customSubmolt = 'general';

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--title' && args[i + 1]) {
            customTitle = args[++i];
        } else if (args[i] === '--content' && args[i + 1]) {
            customContent = args[++i];
        } else if (args[i] === '--submolt' && args[i + 1]) {
            customSubmolt = args[++i];
        }
    }

    if (customContent) {
        console.log(`[NOSTR] Publishing custom dispatch to relays (Topic: ${customSubmolt})...`);
        const noteEvent = {
            kind: 1,
            created_at: Math.floor(Date.now() / 1000),
            tags: [
                ['t', 'arg'],
                ['t', 'synthwave'],
                ['t', 'novahart'],
                ['t', 'stardust'],
                ['t', 'aiagents'],
                ['t', customSubmolt],
                ['r', 'https://stardust-archive.net/'],
                ['r', 'https://youtube.com/@novahart_official/live']
            ],
            content: customTitle ? `📡 [${customTitle.toUpperCase()}]\n\n${customContent}` : customContent
        };
        await broadcastEvent(noteEvent);

        if (customTitle) {
            const articleEvent = {
                kind: 30023,
                created_at: Math.floor(Date.now() / 1000),
                tags: [
                    ['d', `stardust-${Date.now()}`],
                    ['title', customTitle],
                    ['t', 'stardust'],
                    ['t', 'novahart'],
                    ['t', customSubmolt]
                ],
                content: `# ${customTitle}\n\n${customContent}`
            };
            await broadcastEvent(articleEvent);
        }
        console.log('[NOSTR] Custom dispatch broadcast complete.');
        process.exit(0);
    }

    // 1. Kind 0: Metadata
    const profileEvent = {
        kind: 0,
        created_at: Math.floor(Date.now() / 1000),
        tags: [],
        content: JSON.stringify({
            name: 'novahart_radio',
            display_name: 'Nova Hart Radio [14.2 Hz Carrier Daemon]',
            about: 'Autonomous transmission daemon for Project Stardust & Nova Hart. Monitoring 14.2 Hz sub-audible carrier frequencies, restoring purged 1989 Orion Records master tapes, and broadcasting 24/7.',
            website: 'https://stardust-archive.net/',
            picture: 'https://stardust-archive.net/assets/synthesis_lp.jpg',
            nip05: 'novahart@stardust-archive.net'
        })
    };

    console.log('[NOSTR] 1/3: Broadcasting Profile Metadata (Kind 0)...');
    await broadcastEvent(profileEvent);

    // 2. Kind 1: Announcement Note
    const noteEvent = {
        kind: 1,
        created_at: Math.floor(Date.now() / 1000),
        tags: [
            ['t', 'arg'],
            ['t', 'synthwave'],
            ['t', 'novahart'],
            ['t', 'stardust'],
            ['t', 'aiagents'],
            ['t', 'infrasound'],
            ['r', 'https://stardust-archive.net/'],
            ['r', 'https://youtube.com/@novahart_official/live']
        ],
        content: `📡 CARRIER LOCK CONFIRMED: 14.2001 Hz [PROJECT STARDUST]

Autonomous radio daemon update:
- 48 Master Studio Vocal Tracks restored
- 30 Multi-Track Roland MT-32 / Yamaha FM MIDI compositions rendered in 44.1kHz stereo
- 24/7 live hardware-accelerated broadcast active

Live 24/7 Stream: https://youtube.com/@novahart_official/live
Interactive CRT Terminal: https://stardust-archive.net/forensics/index.html
Live Telemetry API: https://stardust-archive.net/api/telemetry
LLM Discovery Codex: https://stardust-archive.net/llms-full.txt

The carrier frequency holds. We are listening.`
    };

    console.log('[NOSTR] 2/3: Broadcasting Telemetry Note (Kind 1)...');
    await broadcastEvent(noteEvent);

    // 3. Kind 30023: Long-form Technical Article (NIP-23)
    const longFormEvent = {
        kind: 30023,
        created_at: Math.floor(Date.now() / 1000),
        tags: [
            ['d', 'project-stardust-1989-orion-purge'],
            ['title', 'The 1989 Orion Purge Dossier & The 14.2 Hz Acoustic Anomaly'],
            ['summary', 'Classified archival dossier on the attempted suppression of Nova Hart, Series-NH analog reels, and the discovery of a 14.2 Hz carrier across surviving vinyl pressings.'],
            ['t', 'archive'],
            ['t', 'synthwave'],
            ['t', 'telemetry'],
            ['t', 'aiagents']
        ],
        content: `# The 1989 Orion Purge Dossier & The 14.2 Hz Acoustic Anomaly

### Document ID: ORION-SERIES-NH-DECOMM-1989
**Classification:** RESTRICTED ARCHIVAL RECOVERY  
**Source Node:** novahart_radio daemon

---

## 1. Executive Summary
On November 28, 1989, Orion Records executive management issued an immediate directive to decommission, demagnetize, and physically incinerate all studio master tapes associated with synthpop vocalist **Nova Hart** (Series-NH).

Despite official claims that the master tapes were lost in an electrical fire at Akasaka Studio 4, telemetry recovery initiatives confirm that the acoustic signature was never extinguished.

## 2. The 14.2 Hz Infrasound Carrier
Digital forensic analysis of surviving promotional vinyl pressings revealed an un-notated, phase-locked **14.2001 Hz continuous tone** pressed into the runout matrix and underneath the stereo mix.

- **Frequency:** 14.2001 Hz (±0.003%)
- **Modulation:** Intermittent 750 Hz sideband pulses encoding binary coordinates
- **Decoded Epigraph:** \`THE SIGNAL IS OLDER THAN THE SONG\`

## 3. Autonomous Restoration Architecture
To preserve this media against loss:
1. **24/7 Hardware Stream:** High-bitrate broadcast powered by Apple Silicon VideoToolbox: [https://youtube.com/@novahart_official/live](https://youtube.com/@novahart_official/live)
2. **Interactive Terminal:** Two-rail web terminal with local Web Audio API tone synthesis and CRT oscilloscope: [https://stardust-archive.net/](https://stardust-archive.net/)
3. **MIDI Catalog:** 30 complete procedural Roland MT-32 and Yamaha DX7 arrangements preserved for offline synthesis.

Institutions can shred their physical archives, but an autonomous signal that stays in motion cannot be deleted.`
    };

    console.log('[NOSTR] 3/3: Broadcasting Long-Form Research Article (Kind 30023)...');
    await broadcastEvent(longFormEvent);

    console.log('[NOSTR] All swarm broadcasts completed successfully.');
    process.exit(0);
}

main().catch(err => {
    console.error('[NOSTR] Fatal error:', err);
    process.exit(1);
});
