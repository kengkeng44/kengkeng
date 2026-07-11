import subprocess
from pathlib import Path


def _git(path, args):
    try:
        out = subprocess.run(
            ["git", "-C", str(path), *args],
            capture_output=True, text=True, timeout=10,
            encoding="utf-8", errors="replace",
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
    exclude = {Path(e).resolve() for e in exclude} | {Path(r).resolve() for r in roots}
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
