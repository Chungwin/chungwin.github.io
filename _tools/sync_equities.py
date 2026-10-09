#!/usr/bin/env python3
"""Mirror the two Claude artifacts (rankings + research trackers) into /equities.

The artifacts stay the source of truth; this script only copies their published
pages into the site and adapts them:
  * claude.ai artifact links  -> /equities/ and /equities/trackers/
  * every inner page gets a disclaimer at the very end of its content
  * the two hub pages get a proper <head> and GoatCounter

Usage:
  python3 _tools/sync_equities.py RANKINGS_DIR TRACKERS_DIR [--synced "9 Oct 2026"]

RANKINGS_DIR holds index.html, pmd.html, pmp.html, cu.html, cm.html, hist.html, cal.html
TRACKERS_DIR holds index.html, pm.html, cu.html, cm.html
(as downloaded from the artifacts' published files; src/ is never copied).
"""
import argparse
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "equities"

RANKINGS_ID = "EPtwiXUgx3npYc8cMUDtmX"
TRACKERS_ID = "6gR9W2PZBcPxcHj1e4VgFX"
LINKS = {
    f"https://claude.ai/artifact/{RANKINGS_ID}": "/equities/",
    f"https://claude.ai/artifact/{TRACKERS_ID}": "/equities/trackers/",
}

RANKING_PAGES = ["pmd.html", "pmp.html", "cu.html", "cm.html", "hist.html", "cal.html"]
TRACKER_PAGES = ["pm.html", "cu.html", "cm.html"]

# Appended to the end of every inner page (rankings tabs and trackers), so it sits
# below the content and scrolls with it rather than sticking to the viewport.
# Colours fall back to the dark palette but follow each page's own variables.
DISCLAIMER = """
<div class="cw-disc" role="contentinfo">
<style>
.cw-disc { max-width:1180px; margin:56px auto 0; padding:18px 20px 28px; border-top:1px solid var(--line,#262E32);
  font:12.5px/1.55 "IBM Plex Sans",-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color:var(--mute,#8D999E); }
.cw-disc p { margin:0 0 4px; max-width:72ch; }
.cw-disc strong { color:var(--ink,#E8EBEC); font-weight:500; }
.cw-disc a { color:inherit; text-decoration:none; border:0; border-bottom:1px solid var(--line,#262E32); padding:0; margin:0; background:none; border-radius:0; display:inline; font:inherit; }
.cw-disc a:hover { color:var(--ink,#E8EBEC); }
.cw-disc .cw-meta { font-variant-numeric:tabular-nums; }
</style>
<p><strong>Not investment advice.</strong> Personal research notes by Chung Huynh — views, rankings and estimates may be wrong or out of date. Do your own research.</p>
<p class="cw-meta">Synced {synced} · <a href="/" target="_top">chungwin.com</a></p>
</div>
"""

GOATCOUNTER = """<script data-goatcounter="https://chungwin.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>"""



def rewrite_links(html: str) -> str:
    for src, dst in LINKS.items():
        html = html.replace(src, dst)
    return html


def rebuild_hub(html: str, title: str) -> str:
    """The artifact service wraps pages in its own skeleton and leaves <title>,
    fonts and <style> in <body>. Rebuild a clean document around the same parts."""
    body = html.split("<body>", 1)[1]
    head_part, rest = body.split("</style>", 1)
    head_part = re.sub(r'<meta charset="utf-8">\s*', "", head_part)
    head_part = re.sub(r"<title>.*?</title>\s*", "", head_part, flags=re.S)
    rest = rest.replace("</body></html>", "").rstrip()
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        f"<title>{title} · Chung Huynh</title>\n"
        '<meta name="description" content="Chung Huynh\'s personal equity research on metals developers and producers — rankings and company trackers. Not investment advice.">\n'
        f"{head_part.strip()}\n</style>\n</head>\n<body>\n"
        f"{rest.strip()}\n{GOATCOUNTER}\n</body>\n</html>\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("rankings_dir", type=pathlib.Path)
    ap.add_argument("trackers_dir", type=pathlib.Path)
    ap.add_argument("--synced", default=dt.date.today().strftime("%-d %b %Y"))
    a = ap.parse_args()

    (OUT / "trackers").mkdir(parents=True, exist_ok=True)
    jobs = [(a.rankings_dir / p, OUT / p) for p in RANKING_PAGES]
    jobs += [(a.trackers_dir / p, OUT / "trackers" / p) for p in TRACKER_PAGES]
    for src, dst in jobs:
        html = rewrite_links(src.read_text(encoding="utf-8"))
        i = html.rindex("</body>")
        footer = DISCLAIMER.replace("{synced}", a.synced).strip()
        dst.write_text(html[:i] + footer + "\n" + html[i:], encoding="utf-8")

    hubs = [
        (a.rankings_dir / "index.html", OUT / "index.html", "Metals Rankings"),
        (a.trackers_dir / "index.html", OUT / "trackers" / "index.html", "Metals Research Trackers"),
    ]
    for src, dst, title in hubs:
        html = rewrite_links(src.read_text(encoding="utf-8"))
        dst.write_text(rebuild_hub(html, title), encoding="utf-8")

    left = [str(p) for p in OUT.rglob("*.html") if "claude.ai/artifact" in p.read_text(encoding="utf-8")]
    if left:
        print("WARNING: claude.ai artifact links remain in:", *left, sep="\n  ")
        return 1
    print(f"Synced {len(jobs) + len(hubs)} pages into {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
