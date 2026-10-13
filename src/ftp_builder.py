"""Generates the FTP archive, including audio outtakes, visuals, and declassified docs."""
import os
import shutil

from common import esc, write

DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">'

def build(ctx, **kwargs):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs = ctx.lore.get("documents", {})
    count = 0
    
    mapping = {
        "ashford-poly/memo_89-117.txt": "memo_89_117",
        "ashford-poly/hale_telemetry_1989-09.log": "telemetry_log",
        "ashford-poly/patent_claims_sd.txt": "patent_claims",
        "ashford-poly/public_harmony_hale.txt": "public_harmony_file",
        "kamome/readme.txt": "akasaka_readme",
        "kamome/tracklist.txt": "akasaka_tracklist",
        "kamome/anomalies.txt": "akasaka_anomalies",
        "kamome/reel_log.txt": "akasaka_reel_log",
    }
    
    assigned_docs = set(mapping.values())
    for k in docs.keys():
        if k not in assigned_docs:
            mapping[f"ashford-poly/{k}.txt"] = k

    sites = {}
    for path, doc_key in mapping.items():
        if doc_key not in docs:
            continue
        host, _, fname = path.partition("/")
        sites.setdefault(host, []).append((fname, docs[doc_key]))
        
        rel_path = f"ftp/{host}/{fname}"
        content = "\n".join(docs[doc_key]) + "\n"
        write(os.path.join(ctx.out, rel_path), content)
        ctx.register(rel_path, "ftp", host)
        count += 1

    # 1. Kamome Visuals (assets/akasaka/*.gif)
    visual_src = os.path.join(root_dir, "assets", "akasaka")
    if "kamome" in sites and os.path.isdir(visual_src):
        visual_files = []
        for fname in sorted(os.listdir(visual_src)):
            if fname.endswith(".gif"):
                src_f = os.path.join(visual_src, fname)
                with open(src_f, "rb") as fh:
                    rel_p = f"ftp/kamome/visual/{fname}"
                    write(os.path.join(ctx.out, rel_p), fh.read(), binary=True)
                    ctx.register(rel_p, "ftp", "kamome")
                    count += 1
                size_kb = os.path.getsize(src_f) / 1024
                visual_files.append((fname, size_kb))

        vis_lines = [
            DOCTYPE,
            '<HTML><HEAD><TITLE>Index of ftp://kamome/visual/</TITLE></HEAD>',
            '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000EE" VLINK="#551A8B">',
            '<H1>Index of ftp://kamome/visual/</H1>',
            '<PRE>',
            '<A HREF="../">[DIR]  ../ (Parent Directory)</A>',
            '-------------------------------------------------------------------------------',
        ]
        for vname, vkb in visual_files:
            vis_lines.append(f'[GIF]  <A HREF="{vname}">{vname:<42}</A>  {vkb:>6.1f} KB')
        vis_lines += [
            '-------------------------------------------------------------------------------',
            '</PRE>',
            '<HR>',
            '<ADDRESS>CERN-HTTPd/3.0 &middot; Kamome-Net Anonymous FTP Service (Akasaka Visual Archive)</ADDRESS>',
            '</BODY></HTML>'
        ]
        vis_index_rel = "ftp/kamome/visual/index.html"
        write(os.path.join(ctx.out, vis_index_rel), "\n".join(vis_lines) + "\n")
        ctx.register(vis_index_rel, "ftp", "kamome visual archive")
        count += 1

    # 2. Kamome Audio Outtakes (assets/akasaka/audio/*.mp3 and *.au)
    audio_src = os.path.join(root_dir, "assets", "akasaka", "audio")
    audio_files = []
    if os.path.isdir(audio_src):
        os.makedirs(os.path.join(ctx.out, "ftp", "kamome", "audio"), exist_ok=True)
        for fname in sorted(os.listdir(audio_src)):
            if fname.endswith(".mp3") or fname.endswith(".au"):
                src_f = os.path.join(audio_src, fname)
                with open(src_f, "rb") as fh:
                    rel_p = f"ftp/kamome/audio/{fname}"
                    write(os.path.join(ctx.out, rel_p), fh.read(), binary=True)
                    ctx.register(rel_p, "ftp", "kamome")
                    count += 1
                size_kb = os.path.getsize(src_f) / 1024
                audio_files.append((fname, size_kb))

        # Build ftp://kamome/audio/index.html
        audio_lines = [
            DOCTYPE,
            '<HTML><HEAD><TITLE>Index of ftp://kamome/audio/</TITLE></HEAD>',
            '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000EE" VLINK="#551A8B">',
            '<H1>Index of ftp://kamome/audio/</H1>',
            '<PRE>',
            '<A HREF="../">[DIR]  ../ (Parent Directory)</A>',
            '-------------------------------------------------------------------------------',
        ]
        for fname, size_kb in audio_files:
            type_tag = "[MP3]" if fname.endswith(".mp3") else "[SND]"
            audio_lines.append(f'{type_tag}  <A HREF="{fname}">{fname:<42}</A>  {size_kb:>6.1f} KB')
        audio_lines += [
            '-------------------------------------------------------------------------------',
            '</PRE>',
            '<HR>',
            '<ADDRESS>CERN-HTTPd/3.0 &middot; Kamome-Net Anonymous FTP Service (Akasaka Archive)</ADDRESS>',
            '</BODY></HTML>'
        ]
        audio_index_rel = "ftp/kamome/audio/index.html"
        write(os.path.join(ctx.out, audio_index_rel), "\n".join(audio_lines) + "\n")
        ctx.register(audio_index_rel, "ftp", "kamome audio archive")
        count += 1

    # 2b. Kamome MIDI Archive (assets/midi/*.mid)
    midi_src = os.path.join(root_dir, "assets", "midi")
    midi_files = []
    if os.path.isdir(midi_src):
        os.makedirs(os.path.join(ctx.out, "ftp", "kamome", "midi"), exist_ok=True)
        for fname in sorted(os.listdir(midi_src)):
            if fname.endswith(".mid"):
                src_f = os.path.join(midi_src, fname)
                with open(src_f, "rb") as fh:
                    rel_p = f"ftp/kamome/midi/{fname}"
                    write(os.path.join(ctx.out, rel_p), fh.read(), binary=True)
                    ctx.register(rel_p, "ftp", "kamome")
                    count += 1
                size_kb = os.path.getsize(src_f) / 1024
                midi_files.append((fname, size_kb))

        # Also copy 14.4k streams if available
        streams_src = os.path.join(root_dir, "assets", "audio", "streams")
        if os.path.isdir(streams_src):
            for fname in sorted(os.listdir(streams_src)):
                if fname.endswith(".mp3"):
                    src_f = os.path.join(streams_src, fname)
                    with open(src_f, "rb") as fh:
                        rel_p = f"ftp/kamome/midi/{fname}"
                        write(os.path.join(ctx.out, rel_p), fh.read(), binary=True)
                        ctx.register(rel_p, "ftp", "kamome")
                        count += 1
                    size_kb = os.path.getsize(src_f) / 1024
                    midi_files.append((fname, size_kb))

        # Build ftp://kamome/midi/index.html
        midi_lines = [
            DOCTYPE,
            '<HTML><HEAD><TITLE>Index of ftp://kamome/midi/</TITLE></HEAD>',
            '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000EE" VLINK="#551A8B">',
            '<H1>Index of ftp://kamome/midi/</H1>',
            '<PRE>',
            '<A HREF="../">[DIR]  ../ (Parent Directory)</A>',
            '-------------------------------------------------------------------------------',
        ]
        sorted_files = sorted(midi_files, key=lambda x: (0 if x[0].endswith(".mid") else 1, x[0]))
        for fname, size_kb in sorted_files:
            type_tag = "[MID]" if fname.endswith(".mid") else "[14K]"
            midi_lines.append(f'{type_tag}  <A HREF="{fname}">{fname:<42}</A>  {size_kb:>6.1f} KB')
        midi_lines += [
            '-------------------------------------------------------------------------------',
            '</PRE>',
            '<HR>',
            '<ADDRESS>CERN-HTTPd/3.0 &middot; Kamome-Net Anonymous FTP Service (General MIDI & 14.4k Streams)</ADDRESS>',
            '</BODY></HTML>'
        ]
        midi_index_rel = "ftp/kamome/midi/index.html"
        write(os.path.join(ctx.out, midi_index_rel), "\n".join(midi_lines) + "\n")
        ctx.register(midi_index_rel, "ftp", "kamome midi archive")
        count += 1

    # 3. Ashford Telemetry Outtakes (assets/ashford/telemetry/*.mp3)
    telemetry_src = os.path.join(root_dir, "assets", "ashford", "telemetry")
    telemetry_files = []
    if os.path.isdir(telemetry_src):
        os.makedirs(os.path.join(ctx.out, "ftp", "ashford-poly", "telemetry"), exist_ok=True)
        for fname in sorted(os.listdir(telemetry_src)):
            if fname.endswith(".mp3"):
                src_f = os.path.join(telemetry_src, fname)
                with open(src_f, "rb") as fh:
                    rel_p = f"ftp/ashford-poly/telemetry/{fname}"
                    write(os.path.join(ctx.out, rel_p), fh.read(), binary=True)
                    ctx.register(rel_p, "ftp", "ashford-poly")
                    count += 1
                size_kb = os.path.getsize(src_f) / 1024
                telemetry_files.append((fname, size_kb))

        # Build ftp://ashford-poly/telemetry/index.html
        telemetry_lines = [
            DOCTYPE,
            '<HTML><HEAD><TITLE>Index of ftp://ashford-poly/telemetry/</TITLE></HEAD>',
            '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000EE" VLINK="#551A8B">',
            '<H1>Index of ftp://ashford-poly/telemetry/</H1>',
            '<PRE>',
            '<A HREF="../">[DIR]  ../ (Parent Directory)</A>',
            '-------------------------------------------------------------------------------',
        ]
        for fname, size_kb in telemetry_files:
            telemetry_lines.append(f'[MP3]  <A HREF="{fname}">{fname:<42}</A>  {size_kb:>6.1f} KB')
        telemetry_lines += [
            '-------------------------------------------------------------------------------',
            '</PRE>',
            '<HR>',
            '<ADDRESS>CERN-HTTPd/3.0 &middot; Ashford Polytechnic Network Archive (Microwave Telemetry)</ADDRESS>',
            '</BODY></HTML>'
        ]
        telemetry_index_rel = "ftp/ashford-poly/telemetry/index.html"
        write(os.path.join(ctx.out, telemetry_index_rel), "\n".join(telemetry_lines) + "\n")
        ctx.register(telemetry_index_rel, "ftp", "ashford telemetry archive")
        count += 1

    # 4. Generate root index.html for each FTP host
    for host, files in sites.items():
        lines = [
            DOCTYPE,
            f'<HTML><HEAD><TITLE>Index of ftp://{host}/</TITLE></HEAD>',
            '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000EE" VLINK="#551A8B">',
            f'<H1>Index of ftp://{host}/</H1>',
            '<PRE>',
            '<A HREF="../../index.html">[DIR]  ../ (WWW Virtual Library)</A>',
            '-------------------------------------------------------------------------------',
        ]
        # Include subdirectories if applicable
        if host == "kamome":
            lines.append('[DIR]  <A HREF="audio/">audio/</A>                                  Recovered audio outtakes (.mp3 / .au)')
            lines.append('[DIR]  <A HREF="midi/">midi/</A>                                   General MIDI sequence archives (.mid)')
            lines.append('[DIR]  <A HREF="visual/">visual/</A>                                 U-matic TV-90 anime frame grabs (.gif)')
        elif host == "ashford-poly":
            lines.append('[DIR]  <A HREF="telemetry/">telemetry/</A>                              Microwave link telemetry outtakes (.mp3)')
            
        for fname, doc_lines in files:
            size_bytes = sum(len(l) + 1 for l in doc_lines) if doc_lines else 1024
            lines.append(f'[TXT]  <A HREF="{fname}">{fname:<42}</A>  {size_bytes:>6d} B')
            
        lines += [
            '-------------------------------------------------------------------------------',
            '</PRE>',
            '<HR>',
            f'<ADDRESS>CERN-HTTPd/3.0 &middot; {host} Anonymous FTP Archive</ADDRESS>',
            '</BODY></HTML>'
        ]
        
        rel_index = f"ftp/{host}/index.html"
        write(os.path.join(ctx.out, rel_index), "\n".join(lines) + "\n")
        ctx.register(rel_index, "ftp", host)
        count += 1
        
    return {"ftp_files": count, "ftp_sites": len(sites)}
