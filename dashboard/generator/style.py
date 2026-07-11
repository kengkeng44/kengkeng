CSS = r"""
:root{
  --ground:#0f1217; --panel:#171b22; --panel2:#1e232c; --line:#262c37;
  --ink:#d7dbe2; --muted:#828a97; --coral:#f2856b;
  --ok:#4bbd7a; --warn:#e0a53a; --crit:#e05a52;
  --mono:ui-monospace,"Cascadia Code","SF Mono",Menlo,Consolas,monospace;
  --sans:"Microsoft JhengHei",system-ui,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.55;overflow-x:hidden}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
:focus-visible{outline:2px solid var(--coral);outline-offset:2px;border-radius:4px}
.shell{max-width:1040px;margin:0 auto;padding:24px 16px;display:flex;gap:24px;align-items:flex-start}
/* ---------- sidebar ---------- */
.side{width:220px;flex:0 0 220px;position:sticky;top:24px;display:flex;flex-direction:column;gap:8px;min-height:calc(100vh - 48px)}
.wordmark{font-family:var(--mono);font-size:15px;font-weight:700;color:var(--coral);padding:8px 12px 16px;letter-spacing:.02em}
.wordmark small{display:block;font-family:var(--sans);font-weight:400;color:var(--muted);font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin-top:4px}
.nav{display:flex;flex-direction:column;gap:2px}
.nav-btn{display:flex;align-items:center;justify-content:space-between;gap:8px;width:100%;text-align:left;padding:8px 12px;border-radius:6px;border-left:2px solid transparent;font-family:var(--mono);font-size:13px;color:var(--muted);white-space:nowrap}
.nav-btn:hover{color:var(--ink);background:var(--panel)}
.nav-btn[aria-current="page"]{color:var(--coral);background:var(--panel2);border-left-color:var(--coral)}
.nav-badge{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:11px;color:var(--muted);background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:0 8px;line-height:18px}
.nav-btn[aria-current="page"] .nav-badge{color:var(--ink);background:var(--ground)}
.bypass-chip{margin-top:auto;font-family:var(--mono);font-size:12px;color:var(--warn);background:rgba(224,165,58,.08);border:1px solid rgba(224,165,58,.35);border-radius:6px;padding:8px 12px;white-space:nowrap}
/* ---------- pane ---------- */
.pane{flex:1;min-width:0}
.view{animation:vfade .16s ease}
@keyframes vfade{from{opacity:0}to{opacity:1}}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 4px}
h1.vtitle{font-size:20px;font-weight:700;margin:0 0 16px}
h2.sect{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600;margin:24px 0 8px}
/* tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px}
.tile{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px}
.tile .num{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:28px;font-weight:700;line-height:1.1}
.tile .lbl{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:4px}
.tile.t-warn .num{color:var(--warn)}
.tile.t-crit .num{color:var(--crit)}
.tile.t-ok .num{color:var(--ok)}
/* banners */
.banner-warn{background:rgba(224,165,58,.08);border:1px solid rgba(224,165,58,.4);border-radius:8px;padding:16px;margin:16px 0}
.banner-warn .bt{font-family:var(--mono);font-size:13px;font-weight:700;color:var(--warn);margin:0 0 6px}
.banner-warn p{margin:0;color:var(--ink)}
.banner-warn code{font-family:var(--mono);font-size:12px;background:var(--panel2);border:1px solid var(--line);border-radius:4px;padding:1px 5px}
.attn{display:flex;align-items:center;gap:8px;color:var(--muted);margin-top:16px}
.attn .num-inline{font-family:var(--mono);font-variant-numeric:tabular-nums;color:var(--warn)}
/* dots + pills */
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;flex:0 0 8px}
.dot.ok{background:var(--ok)} .dot.warn{background:var(--warn)} .dot.crit{background:var(--crit)}
.pill{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--line);border-radius:999px;padding:1px 8px;color:var(--muted)}
.pill.warn{color:var(--warn);border-color:rgba(224,165,58,.4)}
/* details common */
details.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;margin-bottom:8px}
details.card>summary{list-style:none;display:flex;align-items:center;gap:8px;padding:12px 16px;cursor:pointer;border-radius:8px}
details.card>summary::-webkit-details-marker{display:none}
details.card>summary:hover{background:var(--panel2)}
details.card>summary .chev{margin-left:auto;color:var(--muted);font-family:var(--mono);font-size:11px;transition:transform .15s ease}
details.card[open]>summary .chev{transform:rotate(90deg)}
details.card .body{padding:0 16px 16px;border-top:1px solid var(--line);padding-top:12px}
/* projects */
.proj-name{font-family:var(--mono);font-size:14px;font-weight:700}
.proj-meta{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:12px;color:var(--muted);overflow-x:auto;white-space:nowrap}
.chiprow{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.chip{font-family:var(--mono);font-size:11px;background:var(--panel2);border:1px solid var(--line);border-radius:5px;padding:2px 8px;white-space:nowrap;max-width:100%;overflow-x:auto}
.rule{padding:8px 0;border-bottom:1px solid var(--line)}
.rule:last-child{border-bottom:0}
.rule .rn{font-family:var(--mono);font-size:12px}
.rule .rd{color:var(--muted);font-size:12px;margin-top:2px}
.scrollbox{max-height:320px;overflow-y:auto;border:1px solid var(--line);border-radius:6px;padding:0 12px;background:var(--ground)}
.mutenote{color:var(--muted);font-style:italic}
.sub{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:12px 0 4px}
/* memory */
.mem{padding:8px 0;border-bottom:1px solid var(--line)}
.mem:last-child{border-bottom:0}
.mem .mn{font-family:var(--mono);font-size:12px}
.mem .mn.unnamed{font-family:var(--sans);color:var(--muted);font-style:italic}
.mem .md{color:var(--muted);font-size:12px;margin-top:2px}
/* permissions */
.perm{display:flex;align-items:baseline;gap:10px;padding:6px 0;border-bottom:1px solid var(--line)}
.perm:last-child{border-bottom:0}
.perm .dot{position:relative;top:-1px}
.perm .pat{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:12px;white-space:nowrap;overflow-x:auto;flex:1;min-width:0;padding-bottom:2px}
.perm .note{color:var(--muted);font-size:11px;white-space:nowrap;flex:0 1 auto;overflow:hidden;text-overflow:ellipsis}
.permwrap{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:4px 16px;margin-bottom:16px}
/* skills */
.skillgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.skillcol{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px;min-width:0}
@media (max-width:900px){.skillgrid{grid-template-columns:1fr}}
/* ---------- mobile ---------- */
@media (max-width:759px){
  .shell{flex-direction:column;gap:16px;padding:16px 12px}
  .side{position:sticky;top:0;z-index:10;width:100%;flex:none;min-height:0;background:var(--ground);padding:8px 0;gap:8px;border-bottom:1px solid var(--line)}
  .wordmark{padding:0 4px 4px}
  .nav{flex-direction:row;overflow-x:auto;gap:4px;padding-bottom:4px}
  .nav-btn{width:auto;flex:0 0 auto;border-left:0;border-bottom:2px solid transparent;border-radius:6px 6px 0 0}
  .nav-btn[aria-current="page"]{border-bottom-color:var(--coral)}
  .bypass-chip{margin-top:0;align-self:flex-start}
}
@media (prefers-reduced-motion:reduce){
  .view{animation:none}
  details.card>summary .chev{transition:none}
}
.ttag{font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase;border:1px solid var(--line);border-radius:999px;padding:0 6px;color:var(--muted);vertical-align:middle;white-space:nowrap}
.mem .mn{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
"""

JS = r"""
(function(){
  var btns = document.querySelectorAll('.nav-btn');
  var views = document.querySelectorAll('.view');
  btns.forEach(function(btn){
    btn.addEventListener('click', function(){
      btns.forEach(function(b){ b.removeAttribute('aria-current'); });
      btn.setAttribute('aria-current','page');
      views.forEach(function(v){ v.hidden = true; });
      var target = document.getElementById('view-' + btn.dataset.view);
      if (target) { target.hidden = false; }
    });
  });
})();
"""
