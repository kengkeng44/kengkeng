import subprocess

from generator.projects import discover_projects


def _run(cwd, *args):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def test_handles_non_ascii_git_commit_message(tmp_path):
    proj = tmp_path / "work" / "zh"
    proj.mkdir(parents=True)
    (proj / "CLAUDE.md").write_text("# rules\n", encoding="utf-8")
    _run(proj, "git", "init")
    _run(proj, "git", "config", "user.email", "t@t.co")
    _run(proj, "git", "config", "user.name", "t")
    _run(proj, "git", "add", "CLAUDE.md")
    _run(proj, "git", "commit", "-m", "初次提交 班機取消")

    found = discover_projects(roots=[tmp_path / "work"], exclude=[])
    assert len(found) == 1
    git = found[0]["git"]
    assert git is not None
    assert "初次提交" in git["last_commit"]


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


def test_scan_root_itself_is_not_listed_as_project(tmp_path):
    root = tmp_path / "root"
    (root / ".claude").mkdir(parents=True)      # root 本身有 .claude,不該被列為 project
    sub = root / "sub"
    sub.mkdir(parents=True)
    (sub / "CLAUDE.md").write_text("# rules\n", encoding="utf-8")

    found = discover_projects(roots=[root], exclude=[])
    names = {p["name"] for p in found}
    assert "root" not in names
    assert "sub" in names
