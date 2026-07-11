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


def test_skills_section_survives_bare_string_entry():
    models = {
        "memory": [],
        "permissions": {"allow": [], "ask": [], "deny": [], "defaultMode": "default"},
        "skills": {"custom": ["raw-skill"], "docs": [], "super": []},
        "projects": [],
        "generated_at": "2026-07-11",
    }
    html = render_index(models)      # 不應丟 AttributeError
    assert "raw-skill" in html
