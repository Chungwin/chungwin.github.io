#!/usr/bin/env python3
"""Mirror the research artifacts (rankings, research trackers) into /equities.

The artifacts stay the source of truth; this script only copies their published
pages into the site and adapts them:
  * claude.ai artifact links -> /equities/rankings/, /equities/trackers/; links to the
    old landing artifact and to chungwin.com -> the homepage
  * links between the hubs and the rest of the site open in the same tab
  * every inner page gets a disclaimer at the very end of its content
  * the two hubs get a proper <head>, the coin favicon, GoatCounter with anonymous
    usage events, and a "Chung Huynh" link home at the left of their tab bar
  * /equities/ itself only forwards to /equities/rankings/ (the homepage carries the
    overview now); old /equities/#pmd-style links keep working through it
  * _data/equities.yml (latest update, company count, group split) feeds the homepage

Usage:
  python3 _tools/sync_equities.py LANDING_DIR RANKINGS_DIR TRACKERS_DIR [--synced "10 Oct 2026"]

LANDING_DIR  no longer used (kept so existing calls keep working)
RANKINGS_DIR holds index.html, pmd.html, pmp.html, cu.html, cm.html, hist.html, cal.html
TRACKERS_DIR holds index.html, pm.html, cu.html, cm.html, plans.html
(as downloaded from the artifacts' published files; src/ is never copied).
Every .html under /equities is regenerated on each run, so pages that no longer
exist in the artifacts disappear from the site too.
"""
import argparse
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "equities"

LANDING_ID = "DcGSVz6AUYzMi8bUGubeJM"
RANKINGS_ID = "EPtwiXUgx3npYc8cMUDtmX"
TRACKERS_ID = "6gR9W2PZBcPxcHj1e4VgFX"
LINKS = {
    f"https://claude.ai/artifact/{LANDING_ID}": "/",   # the homepage took over the landing page's job
    f"https://claude.ai/artifact/{RANKINGS_ID}": "/equities/rankings/",
    f"https://claude.ai/artifact/{TRACKERS_ID}": "/equities/trackers/",
    "https://chungwin.com/": "/",
}

# Tools that are still hosted on Claude and may be linked from the mirrored pages
CLAUDE_TOOLS = {"2QeyVHDyYpQ9zhYUhYC2vT",   # market temperature
                "ULkKVYfpRgzvUKrkFvwqNB"}   # metal prices

RANKING_PAGES = ["pmd.html", "pmp.html", "cu.html", "cm.html", "hist.html", "cal.html"]
TRACKER_PAGES = ["pm.html", "cu.html", "cm.html", "plans.html"]

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
<p class="cw-meta">Synced {synced} · Visits and anonymous usage are counted with <a href="https://www.goatcounter.com" target="_blank" rel="noopener">GoatCounter</a>: no cookies, nothing that identifies you. · <a href="/" target="_top">chungwin.com</a></p>
</div>
"""

GOATCOUNTER = """<script data-goatcounter="https://chungwin.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>"""

# Usage events on the two hub pages, in the same style as the poker app: anonymous,
# cookie-free, nothing stored on the device, each event at most once per visit.
# The hub reaches into its same-origin frames, so the artifact pages stay untouched.
# Events (GoatCounter paths):
#   equities/<area>/<tab>       a rankings or trackers tab was viewed
#   equities/company/<slug>     a company was opened (tracker card or ranking row)
#   equities/card-tab/<tab>     a section of a tracker card was opened (numbers, entry plan, ...)
#   equities/<area>/search      the tracker search box was used (the query is not sent)
ANALYTICS = """<script>
(function(){
  var AREA = '{area}', q = [], seen = {};
  function flush(){ var gc = window.goatcounter; if(!gc || !gc.count) return; while(q.length){ try { gc.count(q.shift()); } catch(e){} } }
  function ev(path, title){
    path = 'equities/' + path;
    if(seen[path]) return; seen[path] = 1;
    if(window.__eqTest) window.__eqTest.push({ path:path, title:title });
    q.push({ path:path, title:title || path, event:true }); flush();
  }
  var gcs = document.querySelector('script[data-goatcounter]');
  if(gcs) gcs.addEventListener('load', flush);
  window.addEventListener('load', flush);

  function txt(el){ return el ? (el.textContent || '').replace(/\\s+/g, ' ').trim() : ''; }
  function tab(){
    var t = document.querySelector('.tab[aria-selected="true"]'); if(!t) return;
    var lbl = t.cloneNode(true); Array.prototype.forEach.call(lbl.querySelectorAll('.meta'), function(m){ m.remove(); });
    ev(AREA + '/' + t.getAttribute('data-tab'), (AREA === 'rankings' ? 'Rankings: ' : 'Trackers: ') + txt(lbl));
  }
  new MutationObserver(tab).observe(document.querySelector('.tabs'), { subtree:true, attributes:true, attributeFilter:['aria-selected'] });
  tab();

  function hook(f){
    var d; try { d = f.contentDocument; } catch(e){ return; }
    if(!d || d.__eqHooked || !d.body) return; d.__eqHooked = true;
    function opened(el){
      if(!el || !el.open) return;
      if(el.classList.contains('card') && el.id) ev('company/' + el.id, el.getAttribute('data-name') || el.id);
      else if(el.classList.contains('row') && el.getAttribute('data-k')){
        var nm = txt(el.querySelector('.rm b, .rm strong, .rm .nm, .rm .co')) || el.getAttribute('data-k');
        // use the tracker card's slug when the row links to it, so a company counts under one name
        var a = el.querySelector('a[href*="/equities/trackers/#"]'), m = a && a.getAttribute('href').match(/#[a-z]+\\.([a-z0-9-]+)/);
        ev('company/' + (m ? m[1] : el.getAttribute('data-k')), nm);
      }
    }
    d.addEventListener('toggle', function(e){ opened(e.target); }, true);
    // a company reached by link (e.g. rankings -> tracker card) may open before this hook is attached
    function fromHash(){ var h = ''; try { h = decodeURIComponent((f.contentWindow.location.hash || '').slice(1)); } catch(e){} if(h) opened(d.getElementById(h)); }
    fromHash(); setTimeout(fromHash, 800);
    d.addEventListener('click', function(e){
      if(!e.isTrusted) return;   // the page clicks some tabs itself; count only real clicks
      var b = e.target.closest && e.target.closest('.card .tabs button[data-tab]'); if(!b) return;
      ev('card-tab/' + b.getAttribute('data-tab'), 'Card tab: ' + txt(b));
    }, true);
    var s = d.getElementById('q');
    if(s) s.addEventListener('input', function(){ ev(AREA + '/search', (AREA === 'rankings' ? 'Rankings' : 'Trackers') + ': search used'); });
  }
  Array.prototype.forEach.call(document.querySelectorAll('main iframe'), function(f){
    f.addEventListener('load', function(){ hook(f); }); hook(f);
  });
})();
</script>"""

# /equities/ itself: since the homepage carries the overview, this address only forwards to
# the rankings, keeping any hash (old /equities/#pmd-style links included).
FORWARD_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Metals research · Chung Huynh</title>
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=/equities/rankings/">
<link rel="canonical" href="/equities/rankings/">
<script>location.replace('/equities/rankings/' + location.hash);</script>
<style>html{background:#0B0F12;color:#8A969C;font:14px/1.5 "IBM Plex Sans",-apple-system,"Segoe UI",Roboto,Arial,sans-serif}a{color:#ECEEEF}body{margin:40px 16px}</style>
</head><body><p>The metals research has moved to <a href="/equities/rankings/">the rankings</a>.</p></body></html>
"""

# A way back to the rest of the site at the left of the rankings and trackers tab bars
# (website only; the artifacts' own tab bars stay as they are).
HUB_HOME = """<a class="cw-home" href="/" data-goatcounter-click="equities/home" data-goatcounter-title="Research: back home"><span class="cw-home-full">Chung Huynh</span><span class="cw-home-short" aria-hidden="true">←</span></a>"""
HUB_HOME_CSS = """
.cw-home { flex:none; display:flex; align-items:center; padding:0 16px 0 0; margin-right:6px; border-right:1px solid var(--line,#262E32);
  font:400 18px/1 "Source Serif 4","Iowan Old Style",Georgia,serif; letter-spacing:-.005em; color:var(--ink,#E8EBEC); text-decoration:none; white-space:nowrap; }
.cw-home:hover { color:#CFA451; }
.cw-home-short { display:none; }
.cw-home + .tabs, .cw-home + .tabwrap { margin-right:auto; }   /* keep the tabs next to the home link; the side links stay right */
@media (max-width:520px) { .cw-home { padding-right:10px; margin-right:2px; font-size:18px; } .cw-home-full { display:none; } .cw-home-short { display:inline; font-family:"IBM Plex Sans",sans-serif; } }"""
SERIF_FONT = '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400&display=swap" rel="stylesheet">'


# Set in main() from the rankings pages: the newest "Updated <b>9 Oct 2026</b>" date.
LATEST = None


def latest_update(pages) -> str | None:
    """Newest 'Updated <b>D Mon YYYY</b>' date across the ranking tabs, as written there."""
    found = []
    for html in pages:
        m = re.search(r"Updated <b>(\d{1,2} [A-Z][a-z]{2} \d{4})</b>", html)
        if m:
            found.append((dt.datetime.strptime(m.group(1), "%d %b %Y"), m.group(1)))
    return max(found)[1] if found else None


def same_tab(html: str) -> str:
    """Site-internal links on the hub strips open in the same tab."""
    return re.sub(r'(<a\b[^>]*\bhref="/[^"]*"[^>]*?)\s+target="_blank"', r"\1", html)


def rewrite_links(html: str) -> str:
    for src, dst in LINKS.items():
        html = html.replace(src, dst)
    # the artifacts' credit line ends with "Not investment advice."; on the site the disclaimer below says it already
    html = html.replace("does the homework every night.<br>Not investment advice.</p>", "does the homework every night.</p>")
    return html


def rebuild_hub(html: str, title: str, area: str) -> str:
    """The artifact service wraps pages in its own skeleton and leaves <title>,
    fonts and <style> in <body>. Rebuild a clean document around the same parts.
    area is 'rankings' or 'trackers'. Adds the way home at the left of the tab bar."""
    body = html.split("<body>", 1)[1]
    head_part, rest = body.split("</style>", 1)
    head_part = re.sub(r'<meta charset="utf-8">\s*', "", head_part)
    head_part = re.sub(r"<title>.*?</title>\s*", "", head_part, flags=re.S)
    rest = same_tab(rest.replace("</body></html>", "").rstrip())
    rest, n = re.subn(r'(<header class="strip">\s*)', lambda m: m.group(1) + HUB_HOME, rest, count=1)
    if not n:
        raise SystemExit(f"{area}: tab bar <header class=\"strip\"> not found; the home link could not be added")
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        f"<title>{title} · Chung Huynh</title>\n"
        '<link rel="icon" href="/assets/favicons/coin.svg" type="image/svg+xml">\n'
        '<link rel="icon" href="/assets/favicons/coin-32.png" type="image/png" sizes="32x32">\n'
        '<link rel="apple-touch-icon" href="/assets/favicons/coin-touch.png">\n'
        '<meta name="description" content="Chung Huynh\'s personal equity research on small mining companies — rankings and company cards for gold, silver, copper and critical minerals. Not investment advice.">\n'
        + SERIF_FONT + "\n"
        f"{head_part.strip()}\n{HUB_HOME_CSS}\n</style>\n</head>\n<body>\n"
        f"{rest.strip()}\n{GOATCOUNTER}\n{ANALYTICS.replace('{area}', area)}\n</body>\n</html>\n"
    )


def write_site_data(trackers_index: pathlib.Path) -> None:
    """_data/equities.yml feeds the homepage: latest update date, company count and the group split.
    The split comes from the trackers hub's tab labels ("Precious metals … 38 names")."""
    src = trackers_index.read_text(encoding="utf-8")
    lines = []
    if LATEST:
        short = dt.datetime.strptime(LATEST, "%d %b %Y").strftime("%-d %b")
        lines += [f"latest: {LATEST}", f"latest_short: {short}"]
    counts = {}
    for key in ("pm", "cu", "cm"):
        g = re.search(r'<button[^>]*\bid="tab-' + key + r'"[^>]*>.*?<span class="meta">(\d+) names</span>.*?</button>', src, re.S)
        if g:
            counts[key] = int(g.group(1))
    if len(counts) == 3:
        lines.append(f"companies: {sum(counts.values())}")
        lines += [f"{k}: {v}" for k, v in counts.items()]
    else:
        print("WARNING: group counts not found on the trackers hub; homepage numbers not updated")
    (ROOT / "_data").mkdir(exist_ok=True)
    (ROOT / "_data" / "equities.yml").write_text("# Written by _tools/sync_equities.py — do not edit.\n" + "\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("landing_dir", type=pathlib.Path, help="no longer used (the homepage replaced the landing page); kept so existing calls still work")
    ap.add_argument("rankings_dir", type=pathlib.Path)
    ap.add_argument("trackers_dir", type=pathlib.Path)
    ap.add_argument("--synced", default=dt.date.today().strftime("%-d %b %Y"))
    a = ap.parse_args()

    for old in OUT.rglob("*.html"):
        old.unlink()
    for d in ("rankings", "trackers"):
        (OUT / d).mkdir(parents=True, exist_ok=True)

    jobs = [(a.rankings_dir / p, OUT / "rankings" / p) for p in RANKING_PAGES]
    jobs += [(a.trackers_dir / p, OUT / "trackers" / p) for p in TRACKER_PAGES]
    for src, dst in jobs:
        html = rewrite_links(src.read_text(encoding="utf-8"))
        i = html.rindex("</body>")
        footer = DISCLAIMER.replace("{synced}", a.synced).strip()
        dst.write_text(html[:i] + footer + "\n" + html[i:], encoding="utf-8")

    global LATEST
    LATEST = latest_update((a.rankings_dir / p).read_text(encoding="utf-8") for p in ["pmd.html", "pmp.html", "cu.html", "cm.html"])

    hubs = [
        (a.rankings_dir / "index.html", OUT / "rankings" / "index.html", "Metals Rankings", "rankings"),
        (a.trackers_dir / "index.html", OUT / "trackers" / "index.html", "Metals Research Trackers", "trackers"),
    ]
    for src, dst, title, area in hubs:
        html = rewrite_links(src.read_text(encoding="utf-8"))
        dst.write_text(rebuild_hub(html, title, area), encoding="utf-8")

    (OUT / "index.html").write_text(FORWARD_PAGE, encoding="utf-8")
    write_site_data(a.trackers_dir / "index.html")

    # links to the two tools that still live on Claude (market temperature, metal prices) are fine;
    # any other claude.ai artifact link means a page was not mirrored
    def stray(text):
        return [m for m in re.findall(r"https://claude\.ai/artifact/([A-Za-z0-9]+)", text) if m not in CLAUDE_TOOLS]
    left = [str(p) for p in OUT.rglob("*.html") if stray(p.read_text(encoding="utf-8"))]
    if left:
        print("WARNING: claude.ai artifact links remain in:", *left, sep="\n  ")
        return 1
    print(f"Synced {len(jobs) + len(hubs)} pages and the /equities/ forwarder into {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
