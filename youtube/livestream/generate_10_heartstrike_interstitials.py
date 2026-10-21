#!/usr/bin/env python3
"""
Generates 10 Canonical Heartstrike Broadcast Announcements, Concert Promos,
Breaking News Bulletins (Steve Vanderstok & TJ Chicon's Oct 1985 Sunset Strip
Ferrari Testarossa Crash near Clark Street), and Album Reports (`heartstrike_01`..`10`).
"""

import json
import subprocess
import tempfile
import wave
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "broadcast_archive" / "newscasts"
OUT_DIR.mkdir(parents=True, exist_ok=True)
DURATIONS_PATH = BASE_DIR / "track_durations.json"

SR = 44100


def synth_heartstrike_bed(style: str, n_samples: int, seed: int) -> np.ndarray:
    """Synthesizes 1980s rock radio power-chord drones, news teletype pulses, or memorial synth pads."""
    rng = np.random.default_rng(seed)
    t = np.arange(n_samples, dtype=np.float32) / float(SR)
    dur = n_samples / float(SR)
    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    # Analog FM tape hiss
    left += rng.normal(0, 0.0042, n_samples).astype(np.float32)
    right += rng.normal(0, 0.0042, n_samples).astype(np.float32)

    if style == "concert_promo":
        # Driving 1984/1985 hard-rock fifth power chord synth/guitar bed (E2 + B2 + E3)
        roots = [82.41, 110.0, 98.0, 73.42]
        step = 0.95
        for s_i in range(int(dur / step) + 1):
            s0 = int(s_i * step * SR)
            s1 = min(n_samples, int((s_i + 1) * step * SR))
            if s1 <= s0:
                continue
            st = np.arange(s1 - s0, dtype=np.float32) / SR
            r = roots[(s_i + seed) % len(roots)]
            raw = (
                np.sin(2 * np.pi * r * st)
                + 0.7 * np.sin(2 * np.pi * (r * 1.498) * st)
                + 0.5 * np.sin(2 * np.pi * (r * 2.0) * st)
            )
            overdrive = np.tanh(2.4 * raw) * np.exp(-1.8 * st)
            gain = 0.085 if (s0 / SR < 1.3 or s0 / SR > dur - 1.6) else 0.032
            left[s0:s1] += gain * overdrive
            right[s0:s1] += gain * overdrive * 0.9

    elif style == "breaking_news":
        # Somber 1985 radio news teletype beeps + low minor-key drone
        for b_i in range(int(dur / 0.22)):
            s0 = int(b_i * 0.22 * SR)
            slen = min(int(0.045 * SR), n_samples - s0)
            if slen > 0:
                bt = np.arange(slen, dtype=np.float32) / SR
                gain = 0.09 if (s0 / SR < 1.1 or s0 / SR > dur - 1.2) else 0.018
                pip = gain * np.sin(2 * np.pi * 1320.0 * bt) * np.exp(-25.0 * bt)
                left[s0 : s0 + slen] += pip
                right[s0 : s0 + slen] += pip
        drone = 0.024 * np.sin(2 * np.pi * 110.0 * t) + 0.018 * np.sin(2 * np.pi * 130.81 * t)
        left += drone
        right += drone

    else:  # memorial_or_prog
        # Cathedral-like Adam Kellerman Roland Jupiter-8 / D-50 pad (A minor 9th)
        pad_l = (
            0.026 * np.sin(2 * np.pi * 110.00 * t)
            + 0.020 * np.sin(2 * np.pi * 164.81 * t)
            + 0.016 * np.sin(2 * np.pi * 246.94 * t)
        )
        pad_r = (
            0.026 * np.sin(2 * np.pi * 130.81 * t)
            + 0.020 * np.sin(2 * np.pi * 196.00 * t)
            + 0.016 * np.sin(2 * np.pi * 261.63 * t)
        )
        swell = 0.65 + 0.35 * np.sin(2 * np.pi * 0.15 * t)
        left += pad_l * swell
        right += pad_r * swell

    return np.clip(np.column_stack([left, right]), -0.95, 0.95)


def write_stereo_wav(path: Path, data: np.ndarray) -> None:
    pcm = (np.clip(data, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


def render_turn_wav(voice: str, rate: int, text: str, tmp_dir: Path, idx: int) -> Path:
    raw_aiff = tmp_dir / f"hsturn_{idx}_raw.aiff"
    out_wav = tmp_dir / f"hsturn_{idx}.wav"
    subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(raw_aiff), text], check=True)
    af = "highpass=f=115,lowpass=f=5000,acompressor=threshold=-18dB:ratio=3.2:attack=6:release=75"
    subprocess.run(
        [
            "ffmpeg", "-y", "-nostdin", "-loglevel", "error",
            "-i", str(raw_aiff),
            "-af", af,
            "-ar", str(SR), "-ac", "2",
            str(out_wav),
        ],
        check=True,
    )
    return out_wav


def read_stereo_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as wf:
        n = wf.getnframes()
        raw = wf.readframes(n)
        arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        return arr.reshape(-1, 2)


HEARTSTRIKE_SPEC = [
    (
        "heartstrike_01_cleveland_agora_1984_concert_promo",
        "concert_promo",
        "CLEVELAND ROCK RADIO // OCT 1984 AGORA SPOT",
        "This Friday at the Cleveland Agora: hometown legends Heartstrike celebrate 'Strike First' live! Doors at 8 PM.",
        "HEARTSTRIKE ARCHIVE -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Reed (English (US))", 176, 0.30, "Cleveland! This Friday night at the Agora Ballroom, Ohio's own hard-rock hurricane Heartstrike brings their self-funded smash album Strike First home to the Cuyahoga flats!"),
            ("Samantha", 178, 0.25, "Watch frontman Steve Vanderstok climb the lighting rig, feel TJ Chicon tear up his seventy-four Les Paul Custom, and thunder along with Danny Crash Reynolds, Glenn Thurman, and Adam Kellerman on Fire in Your Heart! Tickets five bucks at the door!"),
        ],
    ),
    (
        "heartstrike_02_steel_thunder_rex_powers_soundtrack",
        "concert_promo",
        "1985 ROCK WIRE // STEEL THUNDER SOUNDTRACK",
        "Heartstrike's anthem 'Fire in Your Heart' is featured in the new Rex Powers action movie 'Steel Thunder'—funding their move to Malibu!",
        "STEEL THUNDER SHRINE -> /geocities/hollywood-hills-rexpowers.html",
        [
            ("Daniel", 170, 0.30, "Big break in Hollywood for Cleveland rockers Heartstrike! Director Carl Mitchell just licensed their underground single Fire in Your Heart for the high-voltage training montage in Steel Thunder, starring action titan Rex Powers!"),
            ("Karen", 174, 0.25, "With eight thousand dollars in soundtrack royalties in their pockets, Steve Vanderstok, TJ Chicon, and the guys have packed up their Lakewood rehearsal unit and rented a beach house in Malibu to conquer the Sunset Strip!"),
        ],
    ),
    (
        "heartstrike_03_roxy_whisky_sunset_strip_showcase",
        "concert_promo",
        "SUNSET STRIP CONCERT LINE // OCTOBER 1985",
        "Fresh off signing with EMI Records, Heartstrike headlines The Whisky a Go Go and The Roxy this week on the Sunset Strip!",
        "SUNSET STRIP 1985 -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Reed (English (US))", 178, 0.30, "Los Angeles! The hottest unsigned band on the West Coast is unsigned no more! Fresh off inking their worldwide deal with E M I Records, Heartstrike takes over The Roxy on Sunset Boulevard this Thursday night!"),
            ("Samantha", 178, 0.25, "Every A and R scout in Hollywood was packed into the Whisky a Go Go last week to watch Steve Vanderstok and TJ Chicon trade lightning bolts on Run with the Fire. Get in line before nine or you'll be listening from the sidewalk!"),
        ],
    ),
    (
        "heartstrike_04_breaking_news_steve_and_tj_crash",
        "breaking_news",
        "BREAKING NEWS BULLETIN // OCT 1985 SUNSET STRIP",
        "Tragedy on the Sunset Strip: Heartstrike vocalist Steve Vanderstok and guitarist TJ Chicon killed in a 100-mph Ferrari crash near Clark St.",
        "IN MEMORY OF STEVE & TJ -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Victoria", 162, 0.35, "We interrupt our late-night rock programming with tragic breaking news from West Hollywood. Less than an hour after completing a celebratory showcase set at The Roxy, Heartstrike lead vocalist Steve Vanderstok and lead guitarist T J Chicon were killed in a single-vehicle crash on Sunset Boulevard."),
            ("Daniel", 162, 0.25, " Sheriff's deputies report that Vanderstok's cherry-red Ferrari Testarossa was traveling in excess of one hundred miles per hour when it lost control near the Clark Street bend and struck a utility pole. Steve Vanderstok was twenty-four; T J Chicon was twenty-two."),
        ],
    ),
    (
        "heartstrike_05_candlelight_vigil_roxy_and_lakewood",
        "memorial_or_prog",
        "MEMORIAL TRIBUTE // STEVE VANDERSTOK & TJ CHICON",
        "Fans gather with candles outside The Roxy on Sunset Strip and in Lakewood, Ohio as surviving Heartstrike members return to Cleveland.",
        "HEARTSTRIKE TRIBUTE -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Karen", 160, 0.35, "All across the Sunset Strip tonight, hundreds of rock fans have placed flowers, guitar picks, and handwritten lyrics against the telephone pole at Sunset and Clark Street in memory of Heartstrike's Steve Vanderstok and T J Chicon."),
            ("Reed (English (US))", 160, 0.25, "Back home in Lakewood, Ohio, a simultaneous candlelight vigil is underway outside the Sound Basement studio where the band cut their first eight-track demos. Surviving members Danny Reynolds, Glenn Thurman, and Adam Kellerman have returned to Cleveland in seclusion."),
        ],
    ),
    (
        "heartstrike_06_glenn_thurman_to_the_end_of_time_news",
        "memorial_or_prog",
        "1986 ROCK REPORT // HEARTSTRIKE REBIRTH",
        "Six months after the Sunset Strip crash, bassist Glenn Thurman's grief poem 'To the End of Time' sparks auditions with Stockholm brothers Joss & Kent Freidnam.",
        "SCANDINAVIAN REBIRTH -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Daniel", 166, 0.35, "Six months after the October crash that took Steve Vanderstok and T J Chicon, word out of Cleveland is that Heartstrike will not let the music die. Bassist Glenn Thurman has turned his personal grief journal into a sweeping new tribute song titled To the End of Time."),
            ("Moira", 168, 0.25, "Even more surprising: through a contact at the Stockholm Music Conservatory, Danny, Glenn, and Adam have recruited Swedish brothers Joss Freidnam on four-octave vocals and neo-classical guitar prodigy Kent Freidnam to carry the Heartstrike torch forward."),
        ],
    ),
    (
        "heartstrike_07_lightning_strikes_1987_album_spot",
        "concert_promo",
        "1987 ALBUM PREMIERE // 'LIGHTNING STRIKES'",
        "Heartstrike rises from the ashes with their 1987 EMI concept album 'Lightning Strikes', featuring Joss & Kent Freidnam on 'Echoes of Thunder'.",
        "LIGHTNING STRIKES (1987) -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Reed (English (US))", 170, 0.30, "From the ashes of tragedy comes one of nineteen eighty-seven's most powerful rock albums. Heartstrike returns on E M I Records with Lightning Strikes—dedicated to the eternal memory of Steve Vanderstok and T J Chicon."),
            ("Samantha", 172, 0.25, "Featuring the soaring vocals of Joss Freidnam, the blistering Stockholm sweep-picking of guitarist Kent Freidnam, and Adam Kellerman's cathedral Roland D-Fifty synths on Lightning Strikes Twice and the epic suite Echoes of Thunder."),
        ],
    ),
    (
        "heartstrike_08_mtv_video_boycott_announcement",
        "breaking_news",
        "1987 MUSIC NEWS // HEARTSTRIKE REFUSES MTV",
        "Heartstrike refuses EMI's demand to shoot glossy lip-synced MTV videos for 'Lightning Strikes', vowing to honor Steve and TJ's raw stage legacy.",
        "ALT.MUSIC.HEARTSTRIKE -> /usenet/alt-music-heartstrike/",
        [
            ("Daniel", 166, 0.35, "Trouble brewing between Heartstrike and executives at E M I Records. Despite strong European sales for their nineteen eighty-seven album Lightning Strikes, the band has flatly refused to film a lip-synced promotional video for M T V."),
            ("Reed (English (US))", 166, 0.25, "Drummer Danny Crash Reynolds told reporters in Cleveland yesterday: 'Neon stage gimmicks and fake cameras cheapen the memory of Steve and T J. If you want Heartstrike, come hear us play live.'"),
        ],
    ),
    (
        "heartstrike_09_strike_a_chord_1989_lars_nystrom",
        "memorial_or_prog",
        "1989 IMPORT SHOWCASE // 'STRIKE A CHORD'",
        "Previewing Heartstrike's 1989 independent third album 'Strike a Chord' with Swedish producer Lars Nyström and the 12-minute 'Echoes in the Abyss'.",
        "STRIKE A CHORD (1989) -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Moira", 166, 0.35, "Tonight on the Import Progressive Hour, we're spinning tracks from Heartstrike's daring nineteen eighty-nine independent album Strike a Chord, recorded with avant-garde Swedish producer Lars Nyström."),
            ("Daniel", 166, 0.25, "While longtime Midwest fans will love the raw punch of Shadows of Yesterday and No Turning Back, the album's crown jewel is Kent Freidnam's twelve-minute progressive labyrinth, Echoes in the Abyss."),
        ],
    ),
    (
        "heartstrike_10_european_tour_lawsuit_tape_seizure",
        "breaking_news",
        "1989 ROCK WIRE // HEARTSTRIKE TOUR CANCELED",
        "Devastating breach-of-contract lawsuit bankrupts Heartstrike on the eve of their 1989 European tour; 24-track master reels seized by corporate creditors.",
        "ORION-Z STEM THEFT -> /usenet/alt-music-heartstrike/t01-where-are-the-freidnams.txt",
        [
            ("Victoria", 164, 0.35, "Sad news from the underground rock wire: Heartstrike has officially canceled their nineteen eighty-nine European tour and announced their disbandment after a crushing breach-of-contract lawsuit from their former label left the group bankrupt."),
            ("Daniel", 166, 0.25, "Even worse, bassist Glenn Thurman reports that dozens of two-inch twenty-four-track master reels from the Lars Nyström sessions were repossessed from the studio vault—and rumors say Orion's corporate subsidiaries are already eyeing those guitar stems."),
        ],
    ),
]


def main() -> None:
    assert len(HEARTSTRIKE_SPEC) == 10, f"Expected 10 specs, got {len(HEARTSTRIKE_SPEC)}"
    durations = {}
    if DURATIONS_PATH.exists():
        durations = json.loads(DURATIONS_PATH.read_text())

    new_hs_bulletins = {}

    with tempfile.TemporaryDirectory() as tmp_str:
        tmp_dir = Path(tmp_str)
        for idx, (stem, style, station, transcript, clue, turns) in enumerate(HEARTSTRIKE_SPEC, 1):
            mp3_name = f"{stem}.mp3"
            out_mp3 = OUT_DIR / mp3_name
            new_hs_bulletins[stem] = (station, transcript, clue)

            segments = [np.zeros((int(1.10 * SR), 2), dtype=np.float32)]
            for t_i, (voice, rate, pause_after, text) in enumerate(turns):
                wav_p = render_turn_wav(voice, rate, text, tmp_dir, idx * 10 + t_i)
                seg_arr = read_stereo_wav(wav_p)
                segments.append(seg_arr)
                if pause_after > 0:
                    segments.append(np.zeros((int(pause_after * SR), 2), dtype=np.float32))
            segments.append(np.zeros((int(1.35 * SR), 2), dtype=np.float32))
            voice_track = np.vstack(segments)

            bed = synth_heartstrike_bed(style, voice_track.shape[0], seed=198410 + idx)
            mixed = np.clip(voice_track * 0.92 + bed, -0.98, 0.98)

            mixed_wav = tmp_dir / f"{stem}_mixed.wav"
            write_stereo_wav(mixed_wav, mixed)

            af_master = (
                "highpass=f=130,lowpass=f=4400,"
                "acompressor=threshold=-19dB:ratio=3.2:attack=6:release=70,"
                "loudnorm=I=-16:TP=-1.5:LRA=9"
            )
            subprocess.run(
                [
                    "ffmpeg", "-y", "-nostdin", "-loglevel", "error",
                    "-i", str(mixed_wav),
                    "-af", af_master,
                    "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "192k",
                    str(out_mp3),
                ],
                check=True,
            )

            probe = subprocess.run(
                [
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3),
                ],
                capture_output=True, text=True, check=True,
            )
            dur = round(float(probe.stdout.strip()), 3)
            durations[mp3_name] = dur
            print(f"[{idx:02d}/10] Rendered {mp3_name} ({style}, {dur:.1f}s)")

    DURATIONS_PATH.write_text(json.dumps(durations, indent=2, sort_keys=True))
    Path("/tmp/new_10_heartstrike_bulletins.json").write_text(json.dumps(new_hs_bulletins, indent=2))
    print(f"All 10 Heartstrike / Steve & TJ announcements generated and saved to {OUT_DIR}!")


if __name__ == "__main__":
    main()
