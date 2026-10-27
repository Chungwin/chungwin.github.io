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
  * /equities/context/ shows the market temperature and the metal prices as two tabs
    (see build_context; without --temperature/--prices those pages are left as they are)

Usage:
  python3 _tools/sync_equities.py LANDING_DIR RANKINGS_DIR TRACKERS_DIR [--synced "10 Oct 2026"]
         [--temperature TEMP_DIR --prices PRICES_DIR]

LANDING_DIR  no longer used (kept so existing calls keep working)
RANKINGS_DIR holds index.html, pmd.html, pmp.html, cu.html, cm.html, hist.html, cal.html
TRACKERS_DIR holds index.html, pm.html, cu.html, cm.html, plans.html
TEMP_DIR     holds the market temperature artifact's index.html
PRICES_DIR   holds page.html (the metal prices dashboard's files/index.html "text"), meta.json and
             spot.json (its "Metal list and sources" and "Stored price series" data files), and
             optionally gold_fmp.json, silver_fmp.json, sp500_fmp.json, usdcny_fmp.json: the FMP
             "chart" answers (historical-price-eod-light for GCUSD, SIUSD, ^GSPC, USDCNY, last ~40
             days) that the dashboard on Claude loads live; the page lays them over the stored series
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
    ev(AREA + '/' + t.getAttribute('data-tab'), ({ rankings:'Rankings: ', trackers:'Trackers: ', context:'Market context: ' })[AREA] + txt(lbl));
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


# ---------------------------------------------------------------------------------------------
# Market context: /equities/context/ puts the two tools side by side as tabs.
#   * Market temperature (artifact 2QeyVHDyYpQ9zhYUhYC2vT) is a static page: copied like the others.
#   * Metal prices (artifact ULkKVYfpRgzvUKrkFvwqNB) is a Claude dashboard: its page lives in the
#     artifact's store (files/index.html) and reads datasets through the dashboard runtime, some of
#     them live from the owner's FMP connector, which a public visitor doesn't have. On the site the
#     same page runs on a small stand-in for that runtime (dash.*) fed only by the stored series
#     (extended by the daily run, so nothing is lost but the live USD/CNY rate for molybdenum).
# ---------------------------------------------------------------------------------------------
TEMPERATURE_ID = "2QeyVHDyYpQ9zhYUhYC2vT"
PRICES_ID = "ULkKVYfpRgzvUKrkFvwqNB"
LINKS[f"https://claude.ai/artifact/{TEMPERATURE_ID}"] = "/equities/context/#temperature"
LINKS[f"https://claude.ai/artifact/{PRICES_ID}"] = "/equities/context/#prices"

CONTEXT_HUB = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Market context · Chung Huynh</title>
<link rel="icon" href="/assets/favicons/coin.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicons/coin-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/favicons/coin-touch.png">
<meta name="description" content="Market temperature and metal prices behind Chung Huynh's research on small mining companies. Not investment advice.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root { --bg:#0B0F12; --panel:#141A1E; --ink:#ECEEEF; --mute:#8A969C; --line:#242C32; --acc:#E6E0CF;
  --font:"IBM Plex Sans",-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color-scheme:dark; }
* { box-sizing:border-box; }
html, body { height:100%; }
body { margin:0; background:var(--bg); color:var(--ink); font-family:var(--font); font-size:16px; line-height:1.4; display:flex; flex-direction:column; overflow:hidden; }
header.strip { flex:none; background:var(--panel); border-bottom:1px solid var(--line); padding:0 16px; display:flex; align-items:stretch; gap:12px; }
.tabs { display:flex; gap:4px; min-width:0; overflow-x:auto; scrollbar-width:none; margin-right:auto; }
.tabs::-webkit-scrollbar { display:none; }
.tab { font:inherit; font-size:15px; font-weight:500; color:var(--mute); background:none; border:none; border-bottom:3px solid transparent; padding:14px 14px 11px; cursor:pointer; display:flex; align-items:baseline; gap:10px; white-space:nowrap; letter-spacing:-0.005em; }
.tab .meta { font-size:12px; font-weight:400; color:var(--mute); }
.tab:hover { color:var(--ink); }
.tab[aria-selected="true"] { color:var(--ink); font-weight:600; border-bottom-color:var(--acc); }
.tab:focus-visible { outline:2px solid var(--ink); outline-offset:-4px; border-radius:4px; }
.pico { width:13px; height:13px; align-self:center; flex:none; color:var(--mute); }
.tab[aria-selected="true"] .pico { color:var(--acc); }
.side { display:flex; align-items:center; gap:14px; font-size:12.5px; white-space:nowrap; }
.side a { color:var(--mute); text-decoration:none; border-bottom:1px solid var(--line); }
.side a:hover { color:var(--ink); }
main { flex:1; min-height:0; position:relative; }
iframe { position:absolute; inset:0; width:100%; height:100%; border:0; background:var(--bg); }
iframe[hidden] { display:none; }
@media (max-width:900px) { .tab .meta { display:none; } }
@media (max-width:520px) { header.strip { padding:0 8px; } .tab { padding:12px 10px 9px; font-size:14px; gap:7px; } .side { display:none; } }
@media (prefers-reduced-motion: no-preference) { .tab { transition:color .12s, border-color .12s; } }
{home_css}
</style>
</head>
<body>
<header class="strip">
  {home}<div class="tabs" role="tablist" aria-label="Market context">
    <button class="tab" role="tab" id="tab-temperature" data-tab="temperature" aria-selected="true" aria-controls="frame-temperature" type="button"><svg class="pico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 17a8 8 0 0 1 16 0"/><path d="M12 17l4.5-5"/></svg>Market temperature<span class="meta">monthly</span></button>
    <button class="tab" role="tab" id="tab-prices" data-tab="prices" aria-selected="false" aria-controls="frame-prices" tabindex="-1" type="button"><svg class="pico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3.5 16.5l4.5-5 3.5 3 4-6 5 4"/></svg>Metal prices<span class="meta">daily</span></button>
  </div>
  <div class="side"><a href="/equities/rankings/">Rankings</a><a href="/equities/trackers/">Company cards</a></div>
</header>
<main>
  <iframe id="frame-temperature" title="Market temperature" role="tabpanel" aria-labelledby="tab-temperature"></iframe>
  <iframe id="frame-prices" title="Metal prices" role="tabpanel" aria-labelledby="tab-prices" hidden></iframe>
</main>
<script>
(function(){
  var KEYS = ['temperature','prices'], SRC = { temperature:'temperature.html', prices:'prices.html' };
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  function show(key, fromHash){
    if(KEYS.indexOf(key) === -1) key = 'temperature';
    tabs.forEach(function(t){ var on = t.getAttribute('data-tab') === key; t.setAttribute('aria-selected', on ? 'true' : 'false'); t.tabIndex = on ? 0 : -1; });
    KEYS.forEach(function(k){ var f = document.getElementById('frame-' + k); f.hidden = k !== key; if(k === key && !f.getAttribute('src')) f.setAttribute('src', SRC[k]); });
    try { localStorage.setItem('context-tab', key); } catch(e){}
    if(!fromHash && location.hash !== '#' + key) history.replaceState(null, '', '#' + key);
  }
  tabs.forEach(function(t, i){
    t.addEventListener('click', function(){ show(t.getAttribute('data-tab')); });
    t.addEventListener('keydown', function(e){
      if(e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault(); var n = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
      show(tabs[n].getAttribute('data-tab')); tabs[n].focus();
    });
  });
  window.addEventListener('hashchange', function(){ var h = location.hash.slice(1); if(KEYS.indexOf(h) !== -1) show(h, true); });
  var h = location.hash.slice(1), r = null; try { r = localStorage.getItem('context-tab'); } catch(e){}
  if(KEYS.indexOf(h) !== -1) show(h, true); else show(KEYS.indexOf(r) !== -1 ? r : 'temperature');
})();
</script>
{goatcounter}
{analytics}
</body>
</html>
"""

# The prices page on the site: the dashboard's own page inside #dash-root, the site's dark tokens
# under the names the dashboard uses, d3 from cdnjs, and the dash.* stand-in reading prices-data.json.
PRICES_PAGE = """<!doctype html>
<html lang="en" class="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Metal prices · Chung Huynh</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root { color-scheme:dark;
  --color-fg:#ECEEEF; --color-fg-muted:#8A969C; --color-bg:#0B0F12; --color-panel:#141A1E; --color-border-line:#242C32;
  --color-ok:#3FB27F; --color-warn:#CFA451; --color-bad:#E5675A;
  --cds-border:#242C32; --cds-chart-axis:#4A5761; --cds-chart-grid:#1B2227; --cds-chart-reference:#5B6871;
  --cds-surface-popover:#1A2126; --cds-shadow-popover:0 8px 28px rgba(0,0,0,.5); --cds-text-secondary:#8A969C;
  --cds-font-size-caption:12px; --cds-font-size-body:14px; --cds-font-size-heading:16px; --cds-font-size-title:28px; --cds-font-weight-medium:500;
  --cds-gap-xs:4px; --cds-gap-sm:8px; --cds-gap-md:12px; --cds-gap-lg:16px; --cds-gap-xl:28px;
  --cds-pad-xs:4px; --cds-pad-sm:8px; --cds-pad-md:12px; --cds-pad-lg:16px; --cds-radius:8px; --cds-dur-slow:.3s;
  --font-anthropic-sans:"IBM Plex Sans",-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --font-anthropic-serif:"Source Serif 4","Iowan Old Style",Georgia,serif; }
html, body { margin:0; background:var(--color-bg); color:var(--color-fg); font-family:var(--font-anthropic-sans); font-size:14px; line-height:1.45; }
#dash-root { padding:20px var(--dash-gutter, 24px) 0; }
#dash-root a { color:inherit; }
.cw-loading { max-width:1280px; margin:40px auto; color:var(--color-fg-muted); font-size:13px; }
</style>
<script src="/assets/js/d3-7.9.0.min.js"></script>
<script>
// Stand-in for the Claude dashboard runtime (only what this page uses): datasets come from
// prices-data.json (the FMP closes fetched at sync time stand in for the live FMP datasets),
// calcs run on demand, params live in memory.
window.dash = (function(){
  var DS = { gold_fmp:[], silver_fmp:[], sp500_fmp:[], usdcny_fmp:[], spot_file:null, meta:null };
  var calcs = {}, cache = {}, subs = [], P = {}, state = 'loading', msg = '';
  function wrap(d, st){ var rows = Array.isArray(d) ? d : [];
    return { status:st, data: st === 'ok' ? d : [], rows: st === 'ok' ? rows : [], value: st === 'ok' ? d : null,
             columns: rows.length && typeof rows[0] === 'object' ? Object.keys(rows[0]) : [], message:msg, refreshing:false, meta:[] }; }
  function rowsOf(id){ return id in calcs ? get(id).data : (DS[id] || []); }
  function get(id){
    if(state !== 'ok') return wrap(null, state);
    if(id in calcs){
      if(!(id in cache)){ var c = calcs[id]; try { cache[id] = c.fn.apply(null, c.inputs.map(rowsOf)); } catch(e){ console.error('calc ' + id, e); cache[id] = undefined; } }
      return cache[id] === undefined ? wrap(null, 'error') : wrap(cache[id], 'ok');
    }
    return id in DS ? wrap(DS[id], 'ok') : wrap(null, 'missing');
  }
  function run(){ subs.forEach(function(fn){ try { fn(); } catch(e){ console.error(e); } }); }
  var w = 0, t = null;
  window.addEventListener('resize', function(){ clearTimeout(t); t = setTimeout(function(){ if(document.documentElement.clientWidth !== w){ w = document.documentElement.clientWidth; run(); } }, 120); });
  fetch('prices-data.json').then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); }).then(function(j){
    var spot = [];
    Object.keys(j.series).forEach(function(m){ var s = j.series[m];
      s.d.forEach(function(r){ spot.push({ metal:m, date:r[0], price:r[1], source:s.src[r[2] || 0] }); }); });
    DS.spot_file = spot; DS.meta = j.meta;
    Object.keys(j.live || {}).forEach(function(k){ DS[k] = j.live[k]; });
    state = 'ok'; cache = {}; w = document.documentElement.clientWidth;
    var l = document.getElementById('cw-loading'); if(l) l.remove(); run();
  }).catch(function(e){ state = 'error'; msg = 'Prices could not be loaded.'; var l = document.getElementById('cw-loading'); if(l) l.textContent = msg; run(); });
  return {
    data: get,
    calc: function(id, o){ calcs[id] = o; },
    loader: function(){}, refresh: function(){}, setLink: function(){},
    onData: function(fn){ subs.push(fn); try { fn(); } catch(e){ console.error(e); } },
    params: function(){ return Object.assign({}, P); },
    setParams: function(o){ Object.assign(P, o); run(); },
    resetParams: function(){ P = {}; run(); },
    colors: ['#CFA451','#4FB3A3','#A99BF0','#E07A5F','#6FA8DC','#B5C46A','#D98BB5','#9AA5AB']
  };
})();
</script>
</head>
<body>
<p class="cw-loading" id="cw-loading">Loading prices…</p>
<div id="dash-root">
{page}
</div>
{disclaimer}
</body>
</html>
"""

# Wording of the dashboard that only holds on Claude (live FMP data, written for its owner)
PRICES_TEXT = [
    ("Only the last 40 days load live from FMP when you open it, so the price is never older than the last trading session and each visit uses only a few kilobytes of your FMP allowance.",
     "On this site the last 40 days come from FMP with each site update (overnight and in the morning)."),
    ("FMP (live, opens with the page)", "FMP (daily close)"),
    # the dashboard is written for its owner; on the public site it should not address the visitor
    ('<p class="sp-exp">Your exposure: ', '<p class="sp-exp">Covered companies: '),
    ("Neodymium is a proxy. Your rare-earth names sell", "Neodymium is a proxy. The covered rare-earth companies sell"),
]
# only when the site update could not fetch the USD/CNY rate from FMP
PRICES_NO_FX = ("The molybdenum card also shows the price in US$/lb, converted with the live USD/CNY rate from FMP; this is the Chinese level converted",
                "On this copy the molybdenum price stays in CNY/kg (the US$/lb conversion needs a USD/CNY rate that could not be fetched); it is the Chinese level")
PRICES_LIVE = {"gold_fmp": "GCUSD", "silver_fmp": "SIUSD", "sp500_fmp": "^GSPC", "usdcny_fmp": "USDCNY"}
PRICES_META = {"source_name": {"FMP (live, opens with the page)": "FMP (daily close)"}, "cadence": {"Live daily": "Daily"}}


def build_context(temp_dir: pathlib.Path, prices_dir: pathlib.Path, synced: str) -> list[str]:
    """Writes /equities/context/: the hub, temperature.html, prices.html and prices-data.json.
    temp_dir holds the temperature artifact's index.html; prices_dir holds page.html (the dashboard's
    files/index.html text), meta.json and spot.json (its two stored data files)."""
    import json
    out = OUT / "context"
    out.mkdir(parents=True, exist_ok=True)
    footer = DISCLAIMER.replace("{synced}", synced).strip()

    html = rewrite_links((temp_dir / "index.html").read_text(encoding="utf-8"))
    i = html.rindex("</body>")
    (out / "temperature.html").write_text(html[:i] + footer + "\n" + html[i:], encoding="utf-8")

    # FMP closes fetched at sync time (what the dashboard on Claude loads live)
    live = {}
    for key, sym in PRICES_LIVE.items():
        f = prices_dir / f"{key}.json"
        if not f.exists():
            print(f"NOTE: {f.name} missing; {sym} comes from the stored series only")
            continue
        rows = json.loads(f.read_text(encoding="utf-8"))
        rows = rows.get("historical", rows.get("rows", rows)) if isinstance(rows, dict) else rows
        live[key] = sorted(({"date": str(r["date"])[:10], "price": float(r.get("price", r.get("close")))} for r in rows
                            if r.get("price", r.get("close")) is not None), key=lambda r: r["date"])
        if not live[key]:
            print(f"NOTE: {f.name} holds no rows; {sym} comes from the stored series only")

    page = rewrite_links((prices_dir / "page.html").read_text(encoding="utf-8"))
    for old, new in PRICES_TEXT + ([] if live.get("usdcny_fmp") else [PRICES_NO_FX]):
        if old in page:
            page = page.replace(old, new)   # every occurrence
        else:
            print(f"NOTE: prices page wording changed, not adapted: {old[:60]}…")
    if re.search(r"<(iframe|form|base)\b", page, re.I):
        raise SystemExit("prices page contains markup the dashboard would drop; check it before publishing")
    (out / "prices.html").write_text(PRICES_PAGE.replace("{page}", page.strip()).replace("{disclaimer}", footer), encoding="utf-8")

    meta = json.loads((prices_dir / "meta.json").read_text(encoding="utf-8"))
    meta = meta.get("rows", meta) if isinstance(meta, dict) else meta
    for m in meta:
        for field, swap in PRICES_META.items():
            if m.get(field) in swap:
                m[field] = swap[m[field]]
    spot = json.loads((prices_dir / "spot.json").read_text(encoding="utf-8"))
    spot = spot.get("rows", spot) if isinstance(spot, dict) else spot
    series = {}
    for r in spot:   # compact per metal: [date, price, source index]
        s = series.setdefault(r["metal"], {"src": [], "d": []})
        src = r.get("source") or ""
        if src not in s["src"]:
            s["src"].append(src)
        k = s["src"].index(src)
        s["d"].append([r["date"], float(r["price"])] + ([k] if k else []))
    for s in series.values():
        s["d"].sort()
    (out / "prices-data.json").write_text(json.dumps({"meta": meta, "series": series, "live": live}, separators=(",", ":")), encoding="utf-8")

    hub = (CONTEXT_HUB.replace("{home_css}", HUB_HOME_CSS.strip())
           .replace("{home}", HUB_HOME.replace("Research: back home", "Market context: back home"))
           .replace("{goatcounter}", GOATCOUNTER)
           .replace("{analytics}", ANALYTICS.replace("{area}", "context")))
    (out / "index.html").write_text(hub, encoding="utf-8")
    latest = max(r[0] for s in series.values() for r in s["d"])
    lv = ", ".join(f"{k.split('_')[0]} {v[-1]['date']}" for k, v in live.items() if v) or "none"
    print(f"Market context: temperature + prices ({len(spot)} stored prices, latest {latest}; FMP closes: {lv})")
    return [str(out / p) for p in ("index.html", "temperature.html", "prices.html")]


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
    """_data/equities.yml feeds the homepage: latest update date, company count, the group split and the number of entry plans.
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
    plans = re.search(r'<button[^>]*\bid="tab-plans"[^>]*>.*?<span class="meta">(\d+) plans?</span>.*?</button>', src, re.S)
    if plans:
        lines.append(f"plans: {plans.group(1)}")
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
    ap.add_argument("--temperature", type=pathlib.Path, help="dir with the market temperature artifact's index.html")
    ap.add_argument("--prices", type=pathlib.Path, help="dir with the metal prices dashboard's page.html, meta.json, spot.json")
    a = ap.parse_args()
    context = bool(a.temperature and a.prices)

    # without the two tool downloads the market context pages stay as they are
    for old in OUT.rglob("*.html"):
        if context or (OUT / "context") not in old.parents:
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
    if context:
        build_context(a.temperature, a.prices, a.synced)
    elif not (OUT / "context" / "index.html").exists():
        print("WARNING: no market context pages yet; pass --temperature and --prices")

    # every claude.ai artifact link should have become a site link; one left means a page was not mirrored
    def stray(text):
        return re.findall(r"https://claude\.ai/artifact/([A-Za-z0-9]+)", text)
    left = [str(p) for p in OUT.rglob("*.html") if stray(p.read_text(encoding="utf-8"))]
    if left:
        print("WARNING: claude.ai artifact links remain in:", *left, sep="\n  ")
        return 1
    print(f"Synced {len(jobs) + len(hubs)} pages and the /equities/ forwarder into {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
