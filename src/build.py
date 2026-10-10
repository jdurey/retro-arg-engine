"""Builds the entire Nova Hart web swarm and renders the audio."""
import os
import shutil

from common import Ctx, load, write
import geocities_builder
import usenet_builder
import regional_builder
import ftp_builder

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root_dir, "site")
    if os.path.exists(out):
        shutil.rmtree(out)
    
    ctx = Ctx(out)
    print("Building GeoCities ring...")
    print(geocities_builder.build(ctx, swarm=4000))
    
    print("Building Usenet spool...")
    print(usenet_builder.build(ctx, swarm=14000))
    
    print("Building Regional nodes...")
    print(regional_builder.build(ctx))
    
    print("Building FTP archive...")
    print(ftp_builder.build(ctx))
    
    print("Copying assets...")
    assets_src = os.path.join(root_dir, "assets")
    assets_dest = os.path.join(out, "assets")
    shutil.copytree(assets_src, assets_dest)
    
    print("Creating root index...")
    index_html = [
        '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">',
        '<HTML><HEAD><TITLE>Project Stardust Web Swarm</TITLE></HEAD>',
        '<BODY><H1>Project Stardust Web Swarm</H1>',
        '<P>Navigate the early internet archives of the Nova Hart ARG:</P>',
        '<UL>',
        '<LI><A HREF="geocities/index.html">GeoCities Webring</A></LI>',
        '<LI><A HREF="usenet/index.html">Usenet News Archive</A></LI>'
    ]
    for node in ctx.nodes:
        index_html.append(f'<LI><A HREF="regional/{node["id"]}/index.html">Regional Node {node["node"]:02d}: {node["title"]}</A></LI>')
    index_html.append('<LI><A HREF="ftp/ashford-poly/index.html">FTP Archive: ashford-poly</A></LI>')
    index_html.append('<LI><A HREF="ftp/kamome/index.html">FTP Archive: kamome (Akasaka)</A></LI>')
    index_html.append('</UL></BODY></HTML>')
    
    write(os.path.join(out, "index.html"), "\n".join(index_html) + "\n")
    
    print(f"\nDone. Site built in {out}")

if __name__ == "__main__":
    main()
