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


NEURAL_VOICE_MAP = {
    "Alex": ["en-US-GuyNeural", "en-US-ChristopherNeural", "en-US-EricNeural", "en-US-RogerNeural"],
    "Reed": ["en-US-AndrewNeural", "en-US-BrianNeural", "en-CA-LiamNeural", "en-US-SteffanNeural"],
    "Daniel": ["en-GB-RyanNeural", "en-IE-ConnorNeural", "en-AU-WilliamMultilingualNeural"],
    "Rocko": ["en-US-EricNeural", "en-US-GuyNeural", "en-US-RogerNeural"],
    "Eddy": ["en-US-BrianNeural", "en-US-ChristopherNeural", "en-CA-LiamNeural"],
    "Grandpa": ["en-US-RogerNeural", "en-GB-RyanNeural", "en-US-SteffanNeural"],
    "Samantha": ["en-US-AriaNeural", "en-US-JennyNeural", "en-US-AvaNeural", "en-US-MichelleNeural"],
    "Victoria": ["en-US-EmmaNeural", "en-CA-ClaraNeural", "en-US-AriaNeural"],
    "Karen": ["en-AU-NatashaNeural", "en-NZ-MollyNeural", "en-GB-SoniaNeural"],
    "Moira": ["en-IE-EmilyNeural", "en-GB-SoniaNeural"],
    "Tessa": ["en-GB-SoniaNeural", "en-AU-NatashaNeural"],
    "Shelley": ["en-US-JennyNeural", "en-US-AvaNeural", "en-CA-ClaraNeural"],
    "Flo": ["en-US-MichelleNeural", "en-US-EmmaNeural", "en-US-AriaNeural"],
    "Rishi": ["en-IN-PrabhatNeural", "en-GB-RyanNeural"],
    "Fred": ["en-US-SteffanNeural", "en-US-ChristopherNeural"],
    "Zarvox": ["en-US-EricNeural", "en-US-RogerNeural"],
    "Whisper": ["en-US-AvaNeural", "en-US-JennyNeural"],
}

def render_turn_wav(voice: str, rate: int, text: str, tmp_dir: Path, idx: int) -> Path:
    import asyncio, edge_tts
    raw_mp3 = tmp_dir / f"neural_turn_{idx}.mp3"
    out_wav = tmp_dir / f"neural_turn_{idx}.wav"
    candidates = NEURAL_VOICE_MAP.get(voice, ["en-US-AndrewNeural", "en-US-AriaNeural", "en-US-GuyNeural"])
    n_voice = candidates[idx % len(candidates)]
    pct = max(-15, min(25, int((rate - 182) * 0.45)))
    rate_str = f"{pct:+d}%"
    async def _save():
        for attempt, v_try in enumerate([n_voice, "en-US-AndrewNeural", "en-US-AriaNeural"]):
            try:
                comm = edge_tts.Communicate(text, v_try, rate=rate_str)
                await comm.save(str(raw_mp3))
                if raw_mp3.exists() and raw_mp3.stat().st_size > 500:
                    return
            except Exception:
                await asyncio.sleep(0.4 * (attempt + 1))
        raise RuntimeError(f"Failed TTS for {text[:30]}")
    asyncio.run(_save())
    af = "highpass=f=90,lowpass=f=7400,acompressor=threshold=-17dB:ratio=2.5:attack=10:release=100,silenceremove=start_periods=1:start_duration=0.02:start_threshold=-42dB:detection=peak,areverse,silenceremove=start_periods=1:start_duration=0.04:start_threshold=-42dB:detection=peak,areverse"
    subprocess.run(
        [
            "/opt/homebrew/bin/ffmpeg", "-y", "-nostdin", "-loglevel", "error",
            "-i", str(raw_mp3),
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
        "80S FM // RICK BLAZE CONCERT SPOT (WKVD BLEED)",
        "This Friday at the Cleveland Agora: hometown legends Heartstrike celebrate 'Strike First' live! Sponsored by Banderwise Beer.",
        "TIMELINE BLEED 2:02:03 -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Reed (English (US))", 176, 0.30, "You're tuned to 80s FM with yours truly, Rick Blaze, where the music never stops and the memory never fades! Cleveland, this Friday night at the Agora Ballroom, Ohio's own five-piece rock hurricane Heartstrike brings their self-funded smash album Strike First home to the Echo Coast!"),
            ("Samantha", 178, 0.25, "Watch frontman Steve Vanderstok command the stage, feel guitarist T J Chicon tear up her seventy-four Les Paul Custom, and thunder along with Danny Crash Reynolds, Glenn Thurman, and Adam Kellerman on All In and Fire in Your Heart! Sponsored by Banderwise Beer—cold as static, strong as memory!"),
        ],
    ),
    (
        "heartstrike_02_steel_thunder_rex_powers_soundtrack",
        "concert_promo",
        "80S FM WIRE // STEEL THUNDER & MALIBU MOVE",
        "Heartstrike's anthem 'Fire in Your Heart' powers the montage in Rex Powers' action blockbuster 'Steel Thunder' as the band signs with EMI!",
        "STEEL THUNDER (1985) -> /geocities/hollywood-hills-rexpowers.html",
        [
            ("Daniel", 170, 0.30, "Big break in Hollywood for Cleveland rockers Heartstrike! Their breakout anthem Fire in Your Heart is roaring across theaters nationwide in the high-voltage training montage of Steel Thunder, starring action icon Rex Powers as Jack Thunder!"),
            ("Karen", 174, 0.25, "Fresh off selling ten thousand independent copies of Strike First across the Midwest, Steve Vanderstok, T J Chicon, Danny Reynolds, Glenn Thurman, and Adam Kellerman have signed with E M I Records and moved into the Malibu hills to conquer the Sunset Strip!"),
        ],
    ),
    (
        "heartstrike_03_roxy_whisky_sunset_strip_showcase",
        "concert_promo",
        "WHITE LINES & FEEDBACK // RAZOR CHANDLER TAPE 02",
        "Roadie Razor Chandler recalls Steve Vanderstok writing 'All In' on a diner napkin outside Terre Haute and the band's electric run at The Roxy.",
        "RAZOR SLIDE 2:02:03 -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Reed (English (US))", 162, 0.35, "This is Razor Chandler... still broadcasting from that stretch of highway where dreams go to find out what they're made of. We were westbound in a busted van when Steve scratched the bones of All In onto a diner napkin outside Terre Haute, and T J kept sketching chord shapes on the fogged window glass."),
            ("Daniel", 162, 0.25, "By the time we hit The Roxy and the Whisky a Go Go on the Sunset Strip, Steve was singing Edit the Script like a man trying to outrun his own shadow, and T J's guitar solos were pure thunder in silk gloves. We thought we were just playing rock and roll. We didn't know the tape was already slipping."),
        ],
    ),
    (
        "heartstrike_04_breaking_news_steve_and_tj_crash",
        "breaking_news",
        "KPRX CLEVELAND // 2:02:03 AM FRACTURE BULLETIN",
        "Tragedy on the Sunset Strip: Heartstrike vocalist Steve Vanderstok and guitarist TJ Chicon killed in a 2:02:03 AM Ferrari Testarossa crash.",
        "2:02:03 RUPTURE -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Victoria", 162, 0.35, "K P R X Cleveland. Breaking news from West Hollywood. Less than an hour after their celebratory record release showcase at The Roxy, Heartstrike frontman Steve Vanderstok and lead guitarist T J Chicon were killed in a single-vehicle crash on the Sunset Strip."),
            ("Daniel", 162, 0.25, "Authorities report Vanderstok's Ferrari Testarossa struck a utility pole at precisely two-oh-two and three seconds A.M. Strangely, engineers at Cleveland college station W K V D report their modified Finchley transmitter logged the exact same two-oh-two-oh-three signal spike weeks earlier during the band's Skyburn demo sessions."),
        ],
    ),
    (
        "heartstrike_05_candlelight_vigil_roxy_and_lakewood",
        "memorial_or_prog",
        "WKVD ECHO RECOVERY // SKYBURN RUPTURE LOG",
        "As vigils form on the Sunset Strip and in Cleveland's Clockless Zone, WKVD's transmitter begins looping the 2:02:03 AM Skyburn reel across timelines.",
        "WKVD SKYBURN LOOP -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Karen", 160, 0.35, "Across the Sunset Strip and back home in Cleveland's Clockless Zone, fans have gathered with candles and worn cassette copies of A Story That Won't Fade—the quiet confession Steve Vanderstok wrote for T J Chicon just before Strike First wrapped."),
            ("Reed (English (US))", 160, 0.25, "Meanwhile, late-night listeners along Lake Erie's Echo Coast report that W K V D's unmanned transmitter is activating itself every morning at two-oh-two-oh-three A.M., broadcasting a live five-piece band into a parallel world where live bands were never allowed to exist."),
        ],
    ),
    (
        "heartstrike_06_glenn_thurman_to_the_end_of_time_news",
        "memorial_or_prog",
        "1986 ROCK REPORT // HEARTSTRIKE REBIRTH",
        "After the Sunset Strip crash, bassist Glenn Thurman's grief ballad 'To the End of Time' brings Scandinavian brothers Joss & Kent Freidnam into Heartstrike.",
        "SCANDINAVIAN REBIRTH -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Daniel", 166, 0.35, "Months of silence after the Sunset Strip crash that took Steve Vanderstok and T J Chicon have ended in Cleveland. Surviving Heartstrike members Danny Reynolds, Glenn Thurman, and Adam Kellerman have channeled their grief into a sweeping power ballad titled To the End of Time."),
            ("Moira", 168, 0.25, "Joining the band to honor Steve and T J's legacy are Scandinavian progressive-rock brothers Joss Freidnam on soaring vocals and guitar virtuoso Kent Freidnam—a mentor to a generation of Nordic shredders—ushering in a bold new era for Heartstrike."),
        ],
    ),
    (
        "heartstrike_07_lightning_strikes_1987_album_spot",
        "concert_promo",
        "80S FM // 'LIGHTNING STRIKES' 1987 PREMIERE",
        "Rick Blaze debuts Heartstrike's 1987 concept album 'Lightning Strikes', featuring Joss & Kent Freidnam on 'Lightning Strikes Twice' and 'Echoes of Thunder'.",
        "LIGHTNING STRIKES (1987) -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Reed (English (US))", 170, 0.30, "You're locked into 80s FM with Rick Blaze! Tonight we're spinning the triumphant return of Heartstrike on E M I Records: their sophomore concept album Lightning Strikes, dedicated to the eternal memory of Steve Vanderstok and T J Chicon."),
            ("Samantha", 172, 0.25, "From the high-voltage opener Lightning Strikes Twice and the heartfelt tribute For Steve and T J to the nine-minute centerpiece Echoes of Thunder, Joss and Kent Freidnam join Danny, Glenn, and Adam to prove that real rock never dies!"),
        ],
    ),
    (
        "heartstrike_08_mtv_video_boycott_announcement",
        "breaking_news",
        "SUBLEVEL B2 INTERCEPT // LIVE BAND ANOMALY",
        "Sublevel B2 archivists intercept WKVD's 'Dial Drift' broadcast of Heartstrike—a real five-person live rock band bleeding into Nova Hart's bandless world.",
        "ALT.MUSIC.HEARTSTRIKE -> /usenet/alt-music-heartstrike/",
        [
            ("Daniel", 166, 0.35, "Sublevel B-2 acoustic anomaly report. At zero-two-zero-two-zero-three hours, our fourteen-point-two megahertz receiver locked onto a cross-timeline bleed from station W K V D in Cleveland. The audio contains five uncalibrated human musicians playing physical drums, bass, synthesizers, and electric guitars simultaneously in one room."),
            ("Karen", 166, 0.25, "In our world, the Ministry of Harmony claims live bands never existed—that only solo studio idols like Unit N H-Zero-Four are possible. Yet when Nova Hart hears Heartstrike's live tapes bleeding through the static, her vocal core resonates with every note. Another timeline is speaking to us."),
        ],
    ),
    (
        "heartstrike_09_strike_a_chord_1989_lars_nystrom",
        "memorial_or_prog",
        "1989 IMPORT SHOWCASE // 'STRIKE A CHORD'",
        "Previewing Heartstrike's 1989 third album 'Strike a Chord' with avant-garde producer Lars Nyström, featuring 'Call of the Abyss' and 'Final Crescendo'.",
        "STRIKE A CHORD (1989) -> /geocities/sunsetstrip-club-1987.html",
        [
            ("Moira", 166, 0.35, "Tonight on the Dial Drift Import Hour, we examine Heartstrike's dark, experimental nineteen eighty-nine third album Strike a Chord, independently produced with avant-garde Swedish visionary Lars Nyström."),
            ("Daniel", 166, 0.25, "Opening with the sprawling progressive epic Call of the Abyss and moving through Fractured Harmony, Days Gone By, Fissures in Time, and the ten-minute finale Final Crescendo, the album sounds like a band transmitting across a fracturing reality."),
        ],
    ),
    (
        "heartstrike_10_european_tour_lawsuit_tape_seizure",
        "breaking_news",
        "WHITE LINES & FEEDBACK // NYE 1989 FINAL HUM",
        "Razor Chandler recalls Heartstrike's final New Year's Eve 1989 Cleveland show, the vibrational hum that shook the room, and the mantra of the shift.",
        "I REMEMBER THE SKY -> /usenet/alt-music-heartstrike/t01-where-are-the-freidnams.txt",
        [
            ("Reed (English (US))", 160, 0.35, "You ever hear a song that hits you so hard... you remember the sky? This is Razor Chandler. New Year's Eve, nineteen eighty-nine, at that final underground show in Cleveland. During the last chord of Final Crescendo, a vibrational hum filled the room until the clocks stopped and the walls between lifelines went thin."),
            ("Victoria", 160, 0.25, "Rick Blaze signed off the air that night saying, 'That was Heartstrike... and that was something else.' If you're hearing our signal bleeding through into Nova Hart's frequency tonight, say it with me: I remember the song. I remember where I was. I remember the damn sky."),
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
                "highpass=f=280:poles=2,highpass=f=240:poles=2,"
                "lowpass=f=3400:poles=2,lowpass=f=3700:poles=2,"
                "equalizer=f=950:t=q:w=1.2:g=2.6,"
                "equalizer=f=2150:t=q:w=1.4:g=1.8,"
                "acompressor=threshold=-18dB:ratio=3.8:attack=6:release=70,"
                "loudnorm=I=-16:TP=-1.5:LRA=7"
            )
            subprocess.run(
                [
                    "/opt/homebrew/bin/ffmpeg", "-y", "-nostdin", "-loglevel", "error",
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
