# Config Dashboard P1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用確定性 Python 腳本重生現有全域 Operator's Card(Memory / Permissions / Skills),掛 Stop hook 每次收工自動更新,並在桌面放一個可一鍵開啟的捷徑。

**Architecture:** `dashboard/generator/` Python 套件把來源檔(`settings.json`、`memory/`、`data/*.yaml`)解析成資料模型,`render.py` 組成單一自足 `index.html`(CSS/JS 內嵌)。`generate_dashboard.py` 為進入點;PowerShell 包裝腳本 `regen.ps1` 被 Stop hook 呼叫。桌面 `.url` 捷徑指向本機 HTML。

**Tech Stack:** Python 3.12、PyYAML、pytest、stdlib(`subprocess`/`html`/`pathlib`)、PowerShell hook。

**Scope:** 僅 P1(全域卡自動化 + 桌面捷徑)。P2(config.html 每專案設定)、P3(status.html + 考核)、P4(Cloudflare Access)各自另出計畫。參見 spec `docs/superpowers/specs/2026-07-11-claude-config-dashboard-design.md`。

**路徑常數(全計畫共用):**
- 專案根:`C:/Users/acer/Desktop/kengkeng/dashboard/`
- Claude 設定根:`C:/Users/acer/.claude/`
- memory 目錄:`C:/Users/acer/.claude/projects/C--Users-acer/memory/`
- 桌面:`C:/Users/acer/Desktop/`

---

### Task 1: 專案骨架與測試環境

**Files:**
- Create: `dashboard/generator/__init__.py`
- Create: `dashboard/tests/__init__.py`
- Create: `dashboard/tests/conftest.py`
- Create: `dashboard/requirements-dev.txt`

- [ ] **Step 1: 裝 pytest**

Run: `python -m pip install pytest pyyaml`
Expected: `Successfully installed pytest-... `(pyyaml 已存在會顯示 already satisfied)

- [ ] **Step 2: 建立套件與 dev 依賴清單**

`dashboard/generator/__init__.py`(空檔即可):
```python
```
`dashboard/tests/__init__.py`(空檔):
```python
```
`dashboard/requirements-dev.txt`:
```
pyyaml>=6
pytest>=8
```

- [ ] **Step 3: 建立共用 fixture**

`dashboard/tests/conftest.py`:
```python
import pathlib
import pytest


@pytest.fixture
def tmp_claude(tmp_path):
    """一個假的 .claude 目錄骨架,供各測試填內容。"""
    root = tmp_path / ".claude"
    (root / "projects" / "C--Users-acer" / "memory").mkdir(parents=True)
    return root
```

- [ ] **Step 4: 驗證測試能跑(空收集)**

Run: `cd C:/Users/acer/Desktop/kengkeng/dashboard && python -m pytest -q`
Expected: `no tests ran`(exit 0/5,無 import error)

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/generator dashboard/tests dashboard/requirements-dev.txt
git -C C:/Users/acer/Desktop/kengkeng commit -m "chore: scaffold dashboard generator package + pytest"
```

---

### Task 2: frontmatter 解析器

memory 每個 `.md` 檔頭是 YAML frontmatter(`---` 包夾),需拆出 meta 與 body。

**Files:**
- Create: `dashboard/generator/frontmatter.py`
- Test: `dashboard/tests/test_frontmatter.py`

- [ ] **Step 1: 寫失敗測試**

`dashboard/tests/test_frontmatter.py`:
```python
from generator.frontmatter import parse_frontmatter


def test_parses_meta_and_body():
    text = (
        "---\n"
        "name: sample-rule\n"
        "description: one line\n"
        "metadata:\n"
        "  type: feedback\n"
        "---\n"
        "\nbody text here\n"
    )
    meta, body = parse_frontmatter(text)
    assert meta["name"] == "sample-rule"
    assert meta["description"] == "one line"
    assert meta["metadata"]["type"] == "feedback"
    assert body.strip() == "body text here"


def test_no_frontmatter_returns_empty_meta():
    meta, body = parse_frontmatter("just text\n")
    assert meta == {}
    assert body.strip() == "just text"
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python -m pytest tests/test_frontmatter.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'generator.frontmatter'`

- [ ] **Step 3: 最小實作**

`dashboard/generator/frontmatter.py`:
```python
import yaml


def parse_frontmatter(text):
    """回傳 (meta: dict, body: str)。無 frontmatter 時 meta 為 {}。"""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            meta = yaml.safe_load(parts[1]) or {}
            return meta, parts[2]
    return {}, text
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python -m pytest tests/test_frontmatter.py -q`
Expected: PASS(2 passed)

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/generator/frontmatter.py dashboard/tests/test_frontmatter.py
git -C C:/Users/acer/Desktop/kengkeng commit -m "feat: add frontmatter parser for memory files"
```

---

### Task 3: Memory 資料模型

掃 memory 目錄(排除 `MEMORY.md`),每檔轉成 `{name, description, type, priority}`。priority 由 `data/priorities.yaml`(filename→red/yellow/green)對應,查無則 `green`。

**Files:**
- Create: `dashboard/generator/memory.py`
- Test: `dashboard/tests/test_memory.py`

- [ ] **Step 1: 寫失敗測試**

`dashboard/tests/test_memory.py`:
```python
from generator.memory import build_memory_model


def _write(path, name, desc, mtype):
    path.write_text(
        f"---\nname: {name}\ndescription: {desc}\nmetadata:\n  type: {mtype}\n---\nbody\n",
        encoding="utf-8",
    )


def test_builds_entries_and_skips_index(tmp_path):
    mem = tmp_path / "memory"
    mem.mkdir()
    _write(mem / "feedback_a.md", "feedback-a", "規則 A", "feedback")
    _write(mem / "user_b.md", "user-b", "使用者 B", "user")
    (mem / "MEMORY.md").write_text("- index line\n", encoding="utf-8")

    priorities = {"feedback_a.md": "red"}
    entries = build_memory_model(mem, priorities)

    by_name = {e["name"]: e for e in entries}
    assert "feedback-a" in by_name and "user-b" in by_name
    assert "index" not in " ".join(by_name)  # MEMORY.md 被跳過
    assert by_name["feedback-a"]["priority"] == "red"
    assert by_name["user-b"]["priority"] == "green"   # 查無預設 green
    assert by_name["feedback-a"]["type"] == "feedback"
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python -m pytest tests/test_memory.py -q`
Expected: FAIL — `No module named 'generator.memory'`

- [ ] **Step 3: 最小實作**

`dashboard/generator/memory.py`:
```python
from .frontmatter import parse_frontmatter


def build_memory_model(memory_dir, priorities):
    """回傳 list[dict]:{name, description, type, priority},依 priority 再依 name 排序。"""
    order = {"red": 0, "yellow": 1, "green": 2}
    entries = []
    for path in sorted(memory_dir.glob("*.md")):
        if path.name == "MEMORY.md":
            continue
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not meta:
            continue
        priority = priorities.get(path.name, "green")
        entries.append({
            "name": meta.get("name", path.stem),
            "description": meta.get("description", ""),
            "type": (meta.get("metadata") or {}).get("type", "reference"),
            "priority": priority,
        })
    entries.sort(key=lambda e: (order.get(e["priority"], 3), e["name"]))
    return entries
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python -m pytest tests/test_memory.py -q`
Expected: PASS(1 passed)

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/generator/memory.py dashboard/tests/test_memory.py
git -C C:/Users/acer/Desktop/kengkeng commit -m "feat: build memory model from files + priorities"
```

---

### Task 4: Permissions 資料模型

從 `settings.json` 的 `permissions.{allow,ask,deny}` 取 pattern,配 `data/perm-descriptions.yaml`(pattern→{en,zh})補說明,查無則 en/zh 皆為 pattern 原文。

**Files:**
- Create: `dashboard/generator/permissions.py`
- Test: `dashboard/tests/test_permissions.py`

- [ ] **Step 1: 寫失敗測試**

`dashboard/tests/test_permissions.py`:
```python
from generator.permissions import build_permissions_model


def test_maps_patterns_with_descriptions():
    settings = {
        "permissions": {
            "allow": ["Read", "Bash(git status *)"],
            "ask": ["Bash(rm *)"],
            "deny": [],
            "defaultMode": "bypassPermissions",
        }
    }
    descs = {"Read": {"en": "read files", "zh": "讀檔"}}
    model = build_permissions_model(settings, descs)

    assert model["defaultMode"] == "bypassPermissions"
    allow = {i["pattern"]: i for i in model["allow"]}
    assert allow["Read"]["zh"] == "讀檔"
    # 查無說明 → 用 pattern 原文
    assert allow["Bash(git status *)"]["zh"] == "Bash(git status *)"
    assert model["ask"][0]["pattern"] == "Bash(rm *)"
    assert model["deny"] == []
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python -m pytest tests/test_permissions.py -q`
Expected: FAIL — `No module named 'generator.permissions'`

- [ ] **Step 3: 最小實作**

`dashboard/generator/permissions.py`:
```python
def _decorate(patterns, descs):
    out = []
    for p in patterns:
        d = descs.get(p) or {}
        out.append({"pattern": p, "en": d.get("en", p), "zh": d.get("zh", p)})
    return out


def build_permissions_model(settings, descs):
    perms = settings.get("permissions", {})
    return {
        "allow": _decorate(perms.get("allow", []), descs),
        "ask": _decorate(perms.get("ask", []), descs),
        "deny": _decorate(perms.get("deny", []), descs),
        "defaultMode": perms.get("defaultMode", "default"),
    }
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python -m pytest tests/test_permissions.py -q`
Expected: PASS(1 passed)

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/generator/permissions.py dashboard/tests/test_permissions.py
git -C C:/Users/acer/Desktop/kengkeng commit -m "feat: build permissions model from settings + descriptions"
```

---

### Task 5: Skills 資料模型

`data/skills.yaml` 已是分組結構(custom/docs/super)。模型只需讀取、保證三組都存在(缺組給空 list)。

**Files:**
- Create: `dashboard/generator/skills.py`
- Test: `dashboard/tests/test_skills.py`

- [ ] **Step 1: 寫失敗測試**

`dashboard/tests/test_skills.py`:
```python
from generator.skills import build_skills_model


def test_normalizes_groups():
    raw = {"custom": [{"name": "sync-x"}], "docs": [{"name": "pdf"}]}
    model = build_skills_model(raw)
    assert [s["name"] for s in model["custom"]] == ["sync-x"]
    assert model["super"] == []          # 缺組補空
    assert set(model.keys()) == {"custom", "docs", "super"}
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python -m pytest tests/test_skills.py -q`
Expected: FAIL — `No module named 'generator.skills'`

- [ ] **Step 3: 最小實作**

`dashboard/generator/skills.py`:
```python
def build_skills_model(raw):
    raw = raw or {}
    return {group: list(raw.get(group, []) or []) for group in ("custom", "docs", "super")}
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python -m pytest tests/test_skills.py -q`
Expected: PASS(1 passed)

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/generator/skills.py dashboard/tests/test_skills.py
git -C C:/Users/acer/Desktop/kengkeng commit -m "feat: build skills model from skills.yaml"
```

---

### Task 6: 專案自動探索

掃描指定根目錄(深度 2)找出含 `.claude/` 或 `CLAUDE.md` 的資料夾,排除 Claude 家目錄本身。每專案附 git 資訊(分支、最後 commit、是否有未存改動);非 git 目錄給 `None`。

**Files:**
- Create: `dashboard/generator/projects.py`
- Test: `dashboard/tests/test_projects.py`

- [ ] **Step 1: 寫失敗測試**

`dashboard/tests/test_projects.py`:
```python
from generator.projects import discover_projects


def test_finds_claude_projects_and_excludes_home(tmp_path):
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)          # 家目錄本身,要排除
    proj = tmp_path / "work" / "alpha"
    proj.mkdir(parents=True)
    (proj / "CLAUDE.md").write_text("# rules\n", encoding="utf-8")
    plain = tmp_path / "work" / "beta"
    plain.mkdir(parents=True)                        # 無 claude,不列入

    found = discover_projects(roots=[tmp_path / "work"], exclude=[home])
    names = {p["name"] for p in found}
    assert names == {"alpha"}
    alpha = found[0]
    assert alpha["has_claude_md"] is True
    assert "git" in alpha            # 非 git → None
    assert alpha["git"] is None
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python -m pytest tests/test_projects.py -q`
Expected: FAIL — `No module named 'generator.projects'`

- [ ] **Step 3: 最小實作**

`dashboard/generator/projects.py`:
```python
import subprocess
from pathlib import Path


def _git(path, args):
    try:
        out = subprocess.run(
            ["git", "-C", str(path), *args],
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def _git_info(path):
    branch = _git(path, ["rev-parse", "--abbrev-ref", "HEAD"])
    if branch is None:
        return None
    last = _git(path, ["log", "-1", "--format=%h %cs %s"])
    dirty = _git(path, ["status", "--porcelain"])
    return {"branch": branch, "last_commit": last, "dirty": bool(dirty)}


def discover_projects(roots, exclude=()):
    exclude = {Path(e).resolve() for e in exclude}
    seen = {}
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        for marker in list(root.glob("*/.claude")) + list(root.glob("*/CLAUDE.md")) \
                + list(root.glob(".claude")) + list(root.glob("CLAUDE.md")):
            proj = marker.parent.resolve()
            if proj in exclude or proj in seen:
                continue
            seen[proj] = {
                "name": proj.name,
                "path": str(proj),
                "has_claude_dir": (proj / ".claude").is_dir(),
                "has_claude_md": (proj / "CLAUDE.md").is_file(),
                "git": _git_info(proj),
            }
    return sorted(seen.values(), key=lambda p: p["name"])
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python -m pytest tests/test_projects.py -q`
Expected: PASS(1 passed)

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/generator/projects.py dashboard/tests/test_projects.py
git -C C:/Users/acer/Desktop/kengkeng commit -m "feat: auto-discover claude projects with git info"
```

---

### Task 7: HTML 渲染器

把四個模型組成單一自足 `index.html`(CSS 內嵌)。P1 產出乾淨新版面(三段式:標題列 + 專案總覽格 + Memory/Permissions/Skills 三區);視覺與舊卡的「像素級一致」不在 P1 範圍(舊檔另存 `index.legacy.html` 供參考)。所有動態文字經 `html.escape`。

**Files:**
- Create: `dashboard/generator/render.py`
- Create: `dashboard/generator/style.py`
- Test: `dashboard/tests/test_render.py`

- [ ] **Step 1: 寫失敗測試**

`dashboard/tests/test_render.py`:
```python
from generator.render import render_index


def test_render_contains_all_sections():
    models = {
        "memory": [{"name": "rule-x", "description": "說明 <b>", "type": "feedback", "priority": "red"}],
        "permissions": {"allow": [{"pattern": "Read", "en": "read", "zh": "讀檔"}],
                        "ask": [], "deny": [], "defaultMode": "bypassPermissions"},
        "skills": {"custom": [{"name": "sync-x"}], "docs": [], "super": []},
        "projects": [{"name": "alpha", "path": "/p/alpha", "has_claude_md": True,
                      "has_claude_dir": False, "git": {"branch": "main",
                      "last_commit": "abc 2026-07-11 msg", "dirty": False}}],
        "generated_at": "2026-07-11",
    }
    html = render_index(models)
    assert "<!doctype html>" in html.lower()
    assert "Operator" in html
    assert "rule-x" in html
    assert "說明 &lt;b&gt;" in html      # 有跳脫,不生 raw <b>
    assert "alpha" in html
    assert "讀檔" in html
    assert "sync-x" in html
    assert "2026-07-11" in html
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python -m pytest tests/test_render.py -q`
Expected: FAIL — `No module named 'generator.render'`

- [ ] **Step 3: 最小實作(style + render)**

`dashboard/generator/style.py`:
```python
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
```

`dashboard/generator/render.py`:
```python
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
        rows = "".join(f'<div class="row">{_esc(s.get("name", s))}</div>' for s in skills[group])
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
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python -m pytest tests/test_render.py -q`
Expected: PASS(1 passed)

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/generator/render.py dashboard/generator/style.py dashboard/tests/test_render.py
git -C C:/Users/acer/Desktop/kengkeng commit -m "feat: render index.html from models (escaped, self-contained)"
```

---

### Task 8: 桌面捷徑

在桌面寫一個 `.url`(Internet Shortcut)指向本機 `index.html`,用 `file:///` 讓預設瀏覽器開啟。已存在則覆寫(內容固定,無副作用)。

**Files:**
- Create: `dashboard/generator/shortcut.py`
- Test: `dashboard/tests/test_shortcut.py`

- [ ] **Step 1: 寫失敗測試**

`dashboard/tests/test_shortcut.py`:
```python
from pathlib import Path
from generator.shortcut import ensure_desktop_shortcut


def test_writes_url_shortcut(tmp_path):
    target = tmp_path / "dash" / "index.html"
    target.parent.mkdir()
    target.write_text("<html></html>", encoding="utf-8")
    desktop = tmp_path / "Desktop"
    desktop.mkdir()

    link = ensure_desktop_shortcut(target, desktop, name="Claude 儀表板")
    assert link == desktop / "Claude 儀表板.url"
    text = link.read_text(encoding="utf-8")
    assert "[InternetShortcut]" in text
    assert "URL=file:///" in text
    assert target.name in text.replace("\\", "/")
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python -m pytest tests/test_shortcut.py -q`
Expected: FAIL — `No module named 'generator.shortcut'`

- [ ] **Step 3: 最小實作**

`dashboard/generator/shortcut.py`:
```python
from pathlib import Path


def ensure_desktop_shortcut(target_html, desktop_dir, name="Claude 儀表板"):
    target = Path(target_html).resolve()
    url = "file:///" + str(target).replace("\\", "/")
    link = Path(desktop_dir) / f"{name}.url"
    link.write_text(f"[InternetShortcut]\nURL={url}\n", encoding="utf-8")
    return link
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python -m pytest tests/test_shortcut.py -q`
Expected: PASS(1 passed)

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/generator/shortcut.py dashboard/tests/test_shortcut.py
git -C C:/Users/acer/Desktop/kengkeng commit -m "feat: ensure desktop .url shortcut to local dashboard"
```

---

### Task 9: 進入點 orchestrator

`generate_dashboard.py` 串起:讀來源 → 建模型 → 渲染 → 寫 `index.html` → 確保桌面捷徑。用「內容有變才寫」避免無謂改動。日期由參數注入(預設讀環境變數 `DASHBOARD_DATE`,缺則用 git 無關的固定 `unknown`,實際值由 hook 傳入),以維持可測性。

**Files:**
- Create: `dashboard/generator/build.py`
- Create: `dashboard/generate_dashboard.py`
- Test: `dashboard/tests/test_build.py`

- [ ] **Step 1: 寫失敗測試**

`dashboard/tests/test_build.py`:
```python
import json
from pathlib import Path
from generator.build import build_all


def _setup(tmp_path):
    claude = tmp_path / ".claude"
    mem = claude / "projects" / "C--Users-acer" / "memory"
    mem.mkdir(parents=True)
    (mem / "feedback_x.md").write_text(
        "---\nname: rule-x\ndescription: 規則 X\nmetadata:\n  type: feedback\n---\nb\n",
        encoding="utf-8")
    (claude / "settings.json").write_text(json.dumps({
        "permissions": {"allow": ["Read"], "ask": [], "deny": [],
                        "defaultMode": "bypassPermissions"}}), encoding="utf-8")
    dash = tmp_path / "dashboard"
    (dash / "data").mkdir(parents=True)
    (dash / "data" / "priorities.yaml").write_text("feedback_x.md: red\n", encoding="utf-8")
    (dash / "data" / "perm-descriptions.yaml").write_text(
        "Read:\n  en: read\n  zh: 讀檔\n", encoding="utf-8")
    (dash / "data" / "skills.yaml").write_text("custom: []\ndocs: []\nsuper: []\n", encoding="utf-8")
    return claude, dash


def test_build_writes_index(tmp_path):
    claude, dash = _setup(tmp_path)
    out = build_all(claude_dir=claude, dashboard_dir=dash,
                    project_roots=[tmp_path / "none"], date="2026-07-11")
    index = dash / "index.html"
    assert index.exists()
    html = index.read_text(encoding="utf-8")
    assert "rule-x" in html and "讀檔" in html and "2026-07-11" in html
    assert out == index


def test_build_is_idempotent(tmp_path):
    claude, dash = _setup(tmp_path)
    build_all(claude_dir=claude, dashboard_dir=dash,
              project_roots=[tmp_path / "none"], date="2026-07-11")
    mtime1 = (dash / "index.html").stat().st_mtime_ns
    build_all(claude_dir=claude, dashboard_dir=dash,
              project_roots=[tmp_path / "none"], date="2026-07-11")
    mtime2 = (dash / "index.html").stat().st_mtime_ns
    assert mtime1 == mtime2      # 內容沒變 → 不重寫
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python -m pytest tests/test_build.py -q`
Expected: FAIL — `No module named 'generator.build'`

- [ ] **Step 3: 最小實作(build 模組)**

`dashboard/generator/build.py`:
```python
from pathlib import Path
import json
import yaml

from .memory import build_memory_model
from .permissions import build_permissions_model
from .skills import build_skills_model
from .projects import discover_projects
from .render import render_index


def _load_yaml(path):
    if Path(path).exists():
        return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return {}


def build_all(claude_dir, dashboard_dir, project_roots, date):
    claude_dir, dashboard_dir = Path(claude_dir), Path(dashboard_dir)
    data = dashboard_dir / "data"
    memory_dir = claude_dir / "projects" / "C--Users-acer" / "memory"
    settings = json.loads((claude_dir / "settings.json").read_text(encoding="utf-8"))

    models = {
        "memory": build_memory_model(memory_dir, _load_yaml(data / "priorities.yaml")),
        "permissions": build_permissions_model(settings, _load_yaml(data / "perm-descriptions.yaml")),
        "skills": build_skills_model(_load_yaml(data / "skills.yaml")),
        "projects": discover_projects(project_roots, exclude=[claude_dir.parent]),
        "generated_at": date,
    }
    html = render_index(models)
    out = dashboard_dir / "index.html"
    if not out.exists() or out.read_text(encoding="utf-8") != html:
        out.write_text(html, encoding="utf-8")
    return out
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python -m pytest tests/test_build.py -q`
Expected: PASS(2 passed)

- [ ] **Step 5: 寫進入點(手動端對端用)**

`dashboard/generate_dashboard.py`:
```python
"""重生 Operator's Card 儀表板。收工 Stop hook 或 /refresh-dashboard 呼叫。"""
import os
from pathlib import Path

from generator.build import build_all
from generator.shortcut import ensure_desktop_shortcut

HOME = Path("C:/Users/acer")
CLAUDE_DIR = HOME / ".claude"
DASHBOARD_DIR = HOME / "Desktop" / "kengkeng" / "dashboard"
DESKTOP = HOME / "Desktop"
PROJECT_ROOTS = [HOME / "Desktop", HOME]


def main():
    date = os.environ.get("DASHBOARD_DATE", "").strip() or "—"
    index = build_all(CLAUDE_DIR, DASHBOARD_DIR, PROJECT_ROOTS, date)
    ensure_desktop_shortcut(index, DESKTOP)
    print(f"[dashboard] wrote {index}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: 端對端手動跑一次(真實資料)**

Run: `cd C:/Users/acer/Desktop/kengkeng/dashboard && DASHBOARD_DATE=2026-07-11 python generate_dashboard.py`
Expected: 印出 `[dashboard] wrote ...index.html`;`index.html` 更新;桌面出現 `Claude 儀表板.url`。

- [ ] **Step 7: 全測試綠**

Run: `python -m pytest -q`
Expected: PASS(全部)

- [ ] **Step 8: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/generator/build.py dashboard/generate_dashboard.py dashboard/tests/test_build.py dashboard/index.html
git -C C:/Users/acer/Desktop/kengkeng commit -m "feat: orchestrate dashboard build + desktop shortcut"
```

---

### Task 10: Stop hook 自動化 + /refresh-dashboard 別名

新增 PowerShell 包裝 `regen.ps1`(帶入當日日期後呼叫 python),掛進**全域** `settings.json` 的 `hooks.Stop`(與 backup-memory 並排,`async` + timeout),避免拖慢收工。`/refresh-dashboard` 指令改為呼叫同一支腳本(手動觸發別名)。

**Files:**
- Create: `dashboard/regen.ps1`
- Modify: `C:/Users/acer/.claude/settings.json`(hooks.Stop 陣列)
- Modify: `C:/Users/acer/Desktop/kengkeng/.claude/commands/refresh-dashboard.md`

- [ ] **Step 1: 建 PowerShell 包裝**

`dashboard/regen.ps1`:
```powershell
$env:DASHBOARD_DATE = (Get-Date -Format 'yyyy-MM-dd')
python "C:/Users/acer/Desktop/kengkeng/dashboard/generate_dashboard.py"
```

- [ ] **Step 2: 手動驗證包裝可跑**

Run: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:/Users/acer/Desktop/kengkeng/dashboard/regen.ps1"`
Expected: 印出 `[dashboard] wrote ...`;`index.html` 的「更新於」顯示今天日期。

- [ ] **Step 3: 掛進全域 settings.json 的 Stop hook**

在 `C:/Users/acer/.claude/settings.json` 的 `hooks.Stop[0].hooks` 陣列(目前只有 backup-memory 一項)**後面**新增一項,使其為:
```json
{
  "type": "command",
  "command": "powershell.exe -NoProfile -ExecutionPolicy Bypass -File \"C:/Users/acer/Desktop/kengkeng/dashboard/regen.ps1\"",
  "timeout": 30,
  "async": true
}
```
(保留原 backup-memory 項不動;新增此項於同一 `hooks` 陣列。)

- [ ] **Step 4: 驗證 settings.json 仍有效**

Run: `python -c "import json; json.load(open('C:/Users/acer/.claude/settings.json', encoding='utf-8')); print('settings valid')"`
Expected: `settings valid`

- [ ] **Step 5: 更新 /refresh-dashboard 指令為呼叫腳本**

`C:/Users/acer/Desktop/kengkeng/.claude/commands/refresh-dashboard.md`(整檔覆寫):
```markdown
---
description: 重生 Operator's Card 儀表板(呼叫確定性生成腳本)
---

跑以下指令重生本機儀表板並更新桌面捷徑:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:/Users/acer/Desktop/kengkeng/dashboard/regen.ps1"
```

生成邏輯在 `dashboard/generate_dashboard.py`(確定性,非 LLM)。P4 上線後此腳本會一併 push 到 Cloudflare Pages。
```

- [ ] **Step 6: Commit**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/regen.ps1 .claude/commands/refresh-dashboard.md
git -C C:/Users/acer/Desktop/kengkeng commit -m "feat: wire Stop hook + /refresh-dashboard to deterministic regen"
```
(註:`~/.claude/settings.json` 不在 kengkeng repo 內,屬全域設定,不隨此 commit;其變更由 update-config 流程記錄。)

---

### Task 11: 端對端驗收 + 保留舊卡

**Files:**
- Rename: `dashboard/index.html`(舊 LLM 版)→ 於 Task 9 首次生成前先備份為 `dashboard/index.legacy.html`
- Verify: 生成物

- [ ] **Step 1: 備份舊卡(若尚未備份)**

Run: `test -f C:/Users/acer/Desktop/kengkeng/dashboard/index.legacy.html || cp C:/Users/acer/Desktop/kengkeng/dashboard/index.html C:/Users/acer/Desktop/kengkeng/dashboard/index.legacy.html; echo done`
Expected: `done`(保留舊視覺供 P1 後續對照/回溯)

- [ ] **Step 2: 重生並檢查內容真的來自真實來源**

Run: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:/Users/acer/Desktop/kengkeng/dashboard/regen.ps1"`
接著 Run: `python -c "t=open('C:/Users/acer/Desktop/kengkeng/dashboard/index.html',encoding='utf-8').read(); import sys; sys.exit(0 if ('Operator' in t and '🧠 Memory' in t and 'defaultMode' in t) else 1)"; echo exit=$?`
Expected: `exit=0`(三大區塊都在)

- [ ] **Step 3: 確認桌面捷徑存在且可開**

Run: `test -f "C:/Users/acer/Desktop/Claude 儀表板.url" && cat "C:/Users/acer/Desktop/Claude 儀表板.url"`
Expected: 顯示 `[InternetShortcut]` 與 `URL=file:///.../dashboard/index.html`。人工:雙擊桌面捷徑,瀏覽器開啟、可見 Memory/Permissions/Skills 與專案格。

- [ ] **Step 4: 專案格數量合理**

Run: `python -c "print('check projects grid manually — expect ~5: cheng.robot/gulu/kengkeng/pickup-rn/wordwar')"`
Expected: 頁面專案格顯示約 5 個已知專案(±,視當下磁碟狀態)。

- [ ] **Step 5: 全測試最終綠**

Run: `cd C:/Users/acer/Desktop/kengkeng/dashboard && python -m pytest -q`
Expected: PASS(全部)

- [ ] **Step 6: Commit 驗收產物**

```bash
git -C C:/Users/acer/Desktop/kengkeng add dashboard/index.legacy.html dashboard/index.html
git -C C:/Users/acer/Desktop/kengkeng commit -m "chore: preserve legacy card, verify P1 dashboard end-to-end"
```

---

## P1 完成定義(Definition of Done)

- 桌面雙擊捷徑 → 瀏覽器開本機儀表板,顯示 Memory(紅黃綠)/ Permissions(中文說明)/ Skills / 專案格。
- 收工(Stop)後 `index.html` 自動以當日日期重生,無需手動。
- `python -m pytest -q` 全綠。
- 舊卡保留為 `index.legacy.html`。

## 後續(各自另出計畫)

- **P2**:`config.html` — 每專案讀 `.claude/` + `CLAUDE.md` 呈現規範。
- **P3**:`status.html` + `projects.yaml` + 考核機制(rubric.yaml、A-D、waiver、規範預算、趨勢)。
- **P4**:Cloudflare Pages + Access 私有發佈(含使用者一次性後台設定)。
