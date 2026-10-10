"""Generates the FTP archive."""
import os

from common import esc, write

DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">'

def build(ctx, **kwargs):
    docs = ctx.lore.get("documents", {})
    # Write each document out as a text file
    count = 0
    # Map documents to virtual FTP paths
    # We will hardcode some paths based on the lore and link names seen (e.g. ftp:ashford-poly/memo_89-117.txt)
    # The links in personas are:
    # ftp:ashford-poly/memo_89-117.txt -> memo_89_117
    # ftp:ashford-poly/hale_telemetry_1989-09.log -> telemetry_log
    # ftp:ashford-poly/patent_claims_sd.txt -> patent_claims
    # ftp:ashford-poly/public_harmony_hale.txt -> public_harmony_file
    # ftp:ashford-poly/twin68_array.asc -> (doesn't have a doc mapped, maybe we'll make a dummy or omit it if not in documents)
    # ftp:kamome/... (Akasaka stuff)
    
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
    
    # Also write out any remaining docs into ashford-poly
    assigned_docs = set(mapping.values())
    for k in docs.keys():
        if k not in assigned_docs:
            mapping[f"ashford-poly/{k}.txt"] = k

    # Organize by host
    sites = {}
    for path, doc_key in mapping.items():
        if doc_key not in docs:
            continue
        host, _, fname = path.partition("/")
        sites.setdefault(host, []).append((fname, docs[doc_key]))
        
        # Write the file
        rel_path = f"ftp/{host}/{fname}"
        content = "\n".join(docs[doc_key]) + "\n"
        write(os.path.join(ctx.out, rel_path), content)
        count += 1

    # The Akasaka readme and the Tokyo homepage reference frame grabs at
    # ftp://kamome/visual/ - publish them there and list them in the index.
    visual_src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "akasaka")
    if "kamome" in sites and os.path.isdir(visual_src):
        for fname in sorted(os.listdir(visual_src)):
            if fname.endswith(".gif"):
                with open(os.path.join(visual_src, fname), "rb") as fh:
                    write(os.path.join(ctx.out, "ftp", "kamome", "visual", fname), fh.read(), binary=True)
                sites["kamome"].append((f"visual/{fname}", None))
                count += 1

    # Generate index.html for each host
    for host, files in sites.items():
        lines = [DOCTYPE, f'<HTML><HEAD><TITLE>Index of ftp://{host}/</TITLE></HEAD>', '<BODY>', f'<H1>Index of ftp://{host}/</H1>', '<PRE>']
        for fname, _ in files:
            lines.append(f'<A HREF="{fname}">{fname}</A>')
        lines.append('</PRE></BODY></HTML>')
        
        rel_index = f"ftp/{host}/index.html"
        write(os.path.join(ctx.out, rel_index), "\n".join(lines) + "\n")
        ctx.register(rel_index, "ftp", host)
        
    return {"ftp_files": count, "ftp_sites": len(sites)}
