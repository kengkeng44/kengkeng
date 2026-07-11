import html


def _esc(s):
    return html.escape(str(s if s is not None else ""))


def _project_cards(projects):
    cells = []
    for p in projects:
        git = p.get("git")
        sub = _esc(git["branch"]) if git else "—"
        dirty = " ●" if git and git["dirty"] else ""
        cells.append(
            f'<div class="card"><b>{_esc(p["name"])}</b>'
            f'<div class="muted">{sub}{dirty}</div></div>'
        )
    return f'<div class="grid">{"".join(cells)}</div>'


def _memory_section(entries):
    rows = "".join(
        f'<div class="row"><span class="dot {_esc(e["priority"])}"></span>'
        f'<span><b>{_esc(e["name"])}</b> — {_esc(e["description"])}</span>'
        f'<span class="tag">{_esc(e["type"])}</span></div>'
        for e in entries
    )
    return f'<div class="sec"><h2>🧠 Memory ({len(entries)})</h2>{rows}</div>'


def _perm_section(perms):
    def block(title, items):
        rows = "".join(
            f'<div class="row"><span><code>{_esc(i["pattern"])}</code> '
            f'<span class="muted">{_esc(i["zh"])}</span></span></div>'
            for i in items
        )
        return f'<h2>🔐 {title} ({len(items)})</h2>{rows}'
    body = block("Allow", perms["allow"]) + block("Ask", perms["ask"]) + block("Deny", perms["deny"])
    return (f'<div class="sec">{body}'
            f'<div class="muted">defaultMode: {_esc(perms["defaultMode"])}</div></div>')


def _skills_section(skills):
    parts = []
    for group in ("custom", "docs", "super"):
        rows = "".join(
            f'<div class="row">{_esc(s.get("name", s) if isinstance(s, dict) else s)}</div>'
            for s in skills[group]
        )
        parts.append(f'<h2>🛠️ {group} ({len(skills[group])})</h2>{rows}')
    return f'<div class="sec">{"".join(parts)}</div>'


def render_index(models):
    from .style import CSS
    return (
        "<!doctype html><html lang='zh-Hant'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Operator's Card · Jen-Ho's Claude Code Config</title>"
        f"<style>{CSS}</style></head><body><div class='wrap'>"
        "<h1>Operator's Card · Claude Code Config</h1>"
        f"<div class='sub'>更新於 {_esc(models['generated_at'])}</div>"
        f"{_project_cards(models['projects'])}"
        f"{_memory_section(models['memory'])}"
        f"{_perm_section(models['permissions'])}"
        f"{_skills_section(models['skills'])}"
        "</div></body></html>"
    )
