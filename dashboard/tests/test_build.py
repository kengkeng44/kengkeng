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
        "descriptions:\n  Read:\n    en: read\n    zh: 讀檔\n", encoding="utf-8")
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
