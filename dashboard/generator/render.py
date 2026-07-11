import html

from .style import CSS, JS
from .categorize import perm_families, memory_topics

TYPE_LABEL = {"feedback": "feedback", "reference": "ref", "project": "proj", "user": "user"}


def _e(s):
    return html.escape(str(s if s is not None else ""))


def _split_commit(last):
    if not last:
        return "", "", ""
    parts = last.split(" ", 2)
    return parts[0], (parts[1] if len(parts) > 1 else ""), (parts[2] if len(parts) > 2 else "")


# ---------------- sidebar ----------------
def _sidebar(models):
    perms = models["permissions"]
    counts = {
        "projects": len(models["projects"]),
        "memory": len(models["memory"]),
        "permissions": len(perms["allow"]) + len(perms["ask"]) + len(perms["deny"]),
        "skills": sum(len(v) for v in models["skills"].values()),
    }
    items = [("overview", "Overview", None), ("projects", "Projects", counts["projects"]),
             ("memory", "Memory", counts["memory"]), ("permissions", "Permissions", counts["permissions"]),
             ("skills", "Skills", counts["skills"])]
    btns = []
    for i, (view, label, cnt) in enumerate(items):
        cur = ' aria-current="page"' if i == 0 else ""
        badge = f'<span class="nav-badge">{cnt}</span>' if cnt is not None else ""
        inner = f"<span>{label}</span>{badge}" if badge else label
        btns.append(f'<button class="nav-btn" data-view="{view}"{cur}>{inner}</button>')
    chip = ""
    if perms["defaultMode"] == "bypassPermissions":
        chip = ('<div class="bypass-chip" title="defaultMode: bypassPermissions — '
                '所有 allow/ask/deny 規則目前被跳過">⚠ bypassPermissions</div>')
    return (
        '<aside class="side">'
        '<div class="wordmark">Operator\'s Card<small>Claude Code cockpit</small></div>'
        '<nav class="nav" aria-label="Dashboard sections">' + "".join(btns) + "</nav>"
        + chip + "</aside>"
    )


# ---------------- overview ----------------
def _overview(models):
    p = models["permissions"]
    projs = models["projects"]
    dirty = sum(1 for x in projs if x.get("git") and x["git"]["dirty"])
    tiles = [
        ("", len(projs), "Projects"), ("", len(models["memory"]), "Memory"),
        ("t-ok", len(p["allow"]), "Allow"), ("t-warn", len(p["ask"]), "Ask"),
        ("t-crit", len(p["deny"]), "Deny"), ("", sum(len(v) for v in models["skills"].values()), "Skills"),
    ]
    thtml = "".join(
        f'<div class="tile {c}"><div class="num">{n}</div><div class="lbl">{l}</div></div>'
        for c, n, l in tiles
    )
    banner = ""
    if p["defaultMode"] == "bypassPermissions":
        total = len(p["allow"]) + len(p["ask"]) + len(p["deny"])
        banner = (
            '<div class="banner-warn"><p class="bt">⚠ defaultMode: bypassPermissions</p>'
            f'<p>目前權限模式是 <code>bypassPermissions</code> — 上面的 {total} 條 allow / ask / deny 規則'
            '<strong>全部被跳過</strong>，Claude 執行任何工具都不會過權限檢查。規則清單仍在，但實際上形同虛設。</p></div>'
        )
    dot = "warn" if dirty else "ok"
    attn = (f'<p class="attn"><span class="dot {dot}"></span><span>'
            f'<span class="num-inline">{dirty} / {len(projs)}</span> 個專案有未 commit 的變更。</span></p>')
    return (
        '<section class="view" id="view-overview" aria-label="Overview">'
        '<p class="eyebrow">Overview</p><h1 class="vtitle">3 秒看懂目前狀態</h1>'
        f'<div class="tiles">{thtml}</div>{banner}{attn}</section>'
    )


# ---------------- projects ----------------
def _project_body(p):
    parts = []
    if p.get("git") and p["git"].get("last_commit"):
        h, d, s = _split_commit(p["git"]["last_commit"])
        parts.append(f'<div class="proj-meta">{_e(h)} · {_e(d)} · {_e(s)}</div>')
    cm, rules = p.get("claude_md"), p.get("rules", [])
    if cm or rules:
        if cm:
            parts.append(f'<p class="sub">CLAUDE.md · {cm["lines"]} 行</p>')
            parts.append('<div class="chiprow">'
                         + "".join(f'<span class="chip">{_e(h)}</span>' for h in cm["headings"])
                         + "</div>")
        else:
            parts.append('<p class="sub">CLAUDE.md</p><p class="mutenote">此專案沒有 CLAUDE.md。</p>')
        if rules:
            rows = "".join(
                f'<div class="rule"><div class="rn">{_e(r["name"])}</div>'
                f'<div class="rd">{_e(r["desc"])}</div></div>' for r in rules
            )
            parts.append(f'<p class="sub">.claude/rules · {len(rules)} 條</p>')
            parts.append(f'<div class="scrollbox">{rows}</div>' if len(rules) > 6 else rows)
        else:
            parts.append('<p class="sub">.claude/rules</p><p class="mutenote">此專案沒有 .claude/rules 項目。</p>')
    else:
        note = "此專案無獨立規範檔（僅 .claude/settings）。" if p.get("has_settings") else "此專案無 CLAUDE.md / rules。"
        parts.append(f'<p class="mutenote">{note}</p>')
    return "".join(parts)


def _projects(models):
    cards = []
    for p in models["projects"]:
        git = p.get("git")
        branch = _e(git["branch"]) if git else "—"
        dot = "warn" if git and git["dirty"] else "ok"
        title = "dirty" if git and git["dirty"] else "clean"
        cards.append(
            f'<details class="card"><summary><span class="dot {dot}" title="{title}"></span>'
            f'<span class="proj-name">{_e(p["name"])}</span><span class="pill">{branch}</span>'
            f'<span class="chev">›</span></summary>'
            f'<div class="body">{_project_body(p)}</div></details>'
        )
    return (
        '<section class="view" id="view-projects" aria-label="Projects" hidden>'
        '<p class="eyebrow">Projects</p>'
        f'<h1 class="vtitle">{len(models["projects"])} 個追蹤中的 repo</h1>'
        + "".join(cards) + "</section>"
    )


# ---------------- memory ----------------
def _memory(models):
    groups = memory_topics(models["memory"])
    cards = []
    for i, (topic, items) in enumerate(groups):
        rows = []
        for m in items:
            nm = m["name"] or "（未命名）"
            cls = "mn unnamed" if not m["name"] else "mn"
            tag = f'<span class="ttag">{TYPE_LABEL.get(m["type"], m["type"])}</span>'
            rows.append(f'<div class="mem"><div class="{cls}">{_e(nm)} {tag}</div>'
                        f'<div class="md">{_e(m["description"])}</div></div>')
        op = " open" if i == 0 else ""
        cards.append(
            f'<details class="card"{op}><summary>'
            f'<span class="proj-name" style="font-size:13px">{_e(topic)}</span>'
            f'<span class="nav-badge">{len(items)}</span><span class="chev">›</span></summary>'
            f'<div class="body">{"".join(rows)}</div></details>'
        )
    return (
        '<section class="view" id="view-memory" aria-label="Memory" hidden>'
        '<p class="eyebrow">Memory</p>'
        f'<h1 class="vtitle">{len(models["memory"])} 條長期記憶 · 依主題</h1>'
        + "".join(cards) + "</section>"
    )


# ---------------- permissions ----------------
def _perm_rows(items, dot):
    out = []
    for a in items:
        note = a.get("zh", "")
        note = f'<div class="note">{_e(note)}</div>' if note and note != a["pattern"] else ""
        out.append(f'<div class="perm"><span class="dot {dot}"></span>'
                   f'<div class="pat">{_e(a["pattern"])}</div>{note}</div>')
    return "".join(out)


def _permissions(models):
    p = models["permissions"]
    tiles = (f'<div class="tiles" style="grid-template-columns:repeat(3,1fr)">'
             f'<div class="tile t-ok"><div class="num">{len(p["allow"])}</div><div class="lbl">Allow</div></div>'
             f'<div class="tile t-warn"><div class="num">{len(p["ask"])}</div><div class="lbl">Ask</div></div>'
             f'<div class="tile t-crit"><div class="num">{len(p["deny"])}</div><div class="lbl">Deny</div></div></div>')
    banner = ""
    if p["defaultMode"] == "bypassPermissions":
        banner = ('<div class="banner-warn"><p class="bt">⚠ defaultMode: bypassPermissions</p>'
                  '<p>權限模式目前是 <code>bypassPermissions</code>，以下所有規則實際上都不生效 — '
                  '每個工具呼叫都直接放行。</p></div>')
    allow_groups = "".join(
        f'<details class="card"><summary><span class="dot ok"></span>'
        f'<span class="proj-name" style="font-size:13px">{_e(fam)}</span>'
        f'<span class="nav-badge">{len(items)}</span><span class="chev">›</span></summary>'
        f'<div class="body">{_perm_rows(items, "ok")}</div></details>'
        for fam, items in perm_families(p["allow"])
    )
    return (
        '<section class="view" id="view-permissions" aria-label="Permissions" hidden>'
        '<p class="eyebrow">Permissions</p>'
        f'<h1 class="vtitle">{len(p["allow"]) + len(p["ask"]) + len(p["deny"])} 條權限規則</h1>'
        f'{tiles}{banner}'
        f'<h2 class="sect">Deny · {len(p["deny"])}</h2>'
        f'<div class="permwrap">{_perm_rows(p["deny"], "crit")}</div>'
        f'<h2 class="sect">Ask · {len(p["ask"])}</h2>'
        f'<div class="permwrap">{_perm_rows(p["ask"], "warn")}</div>'
        f'<h2 class="sect">Allow · {len(p["allow"])} · 依工具家族</h2>'
        f'{allow_groups}</section>'
    )


# ---------------- skills ----------------
def _skills(models):
    sk = models["skills"]
    cols = []
    for group, label in (("custom", "Custom"), ("docs", "Docs"), ("super", "Super")):
        ids = sk.get(group, [])
        chips = "".join(f'<span class="chip">{_e(s.get("name", s) if isinstance(s, dict) else s)}</span>' for s in ids)
        cols.append(
            '<div class="skillcol">'
            f'<div class="num" style="font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:28px;font-weight:700">{len(ids)}</div>'
            f'<div class="lbl" style="font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:4px 0 12px">{label}</div>'
            f'<div class="chiprow">{chips}</div></div>'
        )
    return (
        '<section class="view" id="view-skills" aria-label="Skills" hidden>'
        '<p class="eyebrow">Skills</p>'
        f'<h1 class="vtitle">{sum(len(v) for v in sk.values())} 個已裝 skill</h1>'
        f'<div class="skillgrid">{"".join(cols)}</div></section>'
    )


def render_index(models):
    body = (
        '<div class="shell">' + _sidebar(models) + '<main class="pane">'
        + _overview(models) + _projects(models) + _memory(models)
        + _permissions(models) + _skills(models)
        + "</main></div>"
    )
    return (
        "<!doctype html><html lang='zh-Hant'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Operator's Card · Claude Code Config</title>"
        f"<style>{CSS}</style></head><body>"
        f"{body}<script>{JS}</script>"
        "</body></html>"
    )
