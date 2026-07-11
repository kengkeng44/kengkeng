CSS = """
:root{--bg:#0f1115;--card:#1a1d24;--ink:#e6e6e6;--muted:#9aa0aa;--line:#2a2f3a;
--red:#e5534b;--yellow:#d6a52b;--green:#3fb950;--accent:#f28d7a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font-family:"Microsoft JhengHei",system-ui,sans-serif;line-height:1.5}
.wrap{max-width:960px;margin:0 auto;padding:24px}
h1{font-size:20px;margin:0 0 4px}.sub{color:var(--muted);font-size:13px;margin-bottom:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin-bottom:24px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.sec{margin-bottom:28px}.sec h2{font-size:15px;border-left:3px solid var(--accent);padding-left:8px}
.row{display:flex;gap:8px;padding:6px 0;border-bottom:1px solid var(--line);font-size:13px}
.dot{width:8px;height:8px;border-radius:50%;margin-top:6px;flex:0 0 8px}
.red{background:var(--red)}.yellow{background:var(--yellow)}.green{background:var(--green)}
.muted{color:var(--muted)}.tag{font-size:11px;color:var(--muted);border:1px solid var(--line);
border-radius:6px;padding:1px 6px;margin-left:auto;white-space:nowrap}
"""
