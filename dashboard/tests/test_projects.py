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
