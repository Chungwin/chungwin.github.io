#!/usr/bin/env python3
"""Mirror the two Claude artifacts (rankings + research trackers) into /equities.

The artifacts stay the source of truth; this script only copies their published
pages into the site and adapts them:
  * claude.ai artifact links  -> /equities/ and /equities/trackers/
  * every inner page gets a disclaimer at the very end of its content
  * the two hub pages get a proper <head>, GoatCounter and anonymous usage events

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



def rewrite_links(html: str) -> str:
    for src, dst in LINKS.items():
        html = html.replace(src, dst)
    return html


def rebuild_hub(html: str, title: str, area: str) -> str:
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
        '<link rel="icon" href="/assets/favicons/coin.svg" type="image/svg+xml">\n'
        '<link rel="icon" href="/assets/favicons/coin-32.png" type="image/png" sizes="32x32">\n'
        '<link rel="apple-touch-icon" href="/assets/favicons/coin-touch.png">\n'
        '<meta name="description" content="Chung Huynh\'s personal equity research on metals developers and producers — rankings and company trackers. Not investment advice.">\n'
        f"{head_part.strip()}\n</style>\n</head>\n<body>\n"
        f"{rest.strip()}\n{GOATCOUNTER}\n{ANALYTICS.replace('{area}', area)}\n</body>\n</html>\n"
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
        (a.rankings_dir / "index.html", OUT / "index.html", "Metals Rankings", "rankings"),
        (a.trackers_dir / "index.html", OUT / "trackers" / "index.html", "Metals Research Trackers", "trackers"),
    ]
    for src, dst, title, area in hubs:
        html = rewrite_links(src.read_text(encoding="utf-8"))
        dst.write_text(rebuild_hub(html, title, area), encoding="utf-8")

    left = [str(p) for p in OUT.rglob("*.html") if "claude.ai/artifact" in p.read_text(encoding="utf-8")]
    if left:
        print("WARNING: claude.ai artifact links remain in:", *left, sep="\n  ")
        return 1
    print(f"Synced {len(jobs) + len(hubs)} pages into {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
