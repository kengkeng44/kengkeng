import re
import subprocess
from pathlib import Path

from .frontmatter import parse_frontmatter


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


def _claude_md_outline(proj):
    """回傳 {lines, headings[]} 或 None(檔案不存在/近乎空)。只取 h1/h2,上限 8。"""
    p = proj / "CLAUDE.md"
    if not p.is_file():
        return None
    txt = p.read_text(encoding="utf-8", errors="replace")
    if len(txt) < 20:
        return None
    heads = [m[1].strip() for m in re.findall(r"^(#{1,3})\s+(.*)$", txt, re.M) if len(m[0]) <= 2]
    return {"lines": txt.count("\n") + 1, "headings": heads[:8]}


def _rules_of(proj):
    """回傳 [{name, desc, type}],讀 .claude/rules/*.md 的 frontmatter。"""
    rd = proj / ".claude" / "rules"
    items = []
    if rd.is_dir():
        for f in sorted(rd.glob("*.md")):
            meta, _ = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
            meta = meta or {}
            items.append({
                "name": meta.get("name", f.stem),
                "desc": meta.get("description", ""),
                "type": (meta.get("metadata") or {}).get("type", ""),
            })
    return items


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
            has_claude_dir = (proj / ".claude").is_dir()
            seen[proj] = {
                "name": proj.name,
                "path": str(proj),
                "has_claude_dir": has_claude_dir,
                "has_claude_md": (proj / "CLAUDE.md").is_file(),
                "has_settings": (proj / ".claude" / "settings.local.json").exists()
                or (proj / ".claude" / "settings.json").exists(),
                "claude_md": _claude_md_outline(proj),
                "rules": _rules_of(proj),
                "git": _git_info(proj),
            }
    # 同名專案(例如 Desktop/pickup 與 projects/pickup 這種重複 clone)
    # 補上所在目錄,否則畫面上兩張卡長得一模一樣,分不出在看哪一份。
    from collections import Counter
    dupes = {n for n, c in Counter(p["name"] for p in seen.values()).items() if c > 1}
    for p in seen.values():
        if p["name"] in dupes:
            p["name"] = f'{Path(p["path"]).parent.name}/{p["name"]}'

    # 規範越豐富的排前面(rules + CLAUDE.md 章節數),再依名稱
    def richness(p):
        cm = p.get("claude_md")
        return -(len(p.get("rules", [])) + (len(cm["headings"]) if cm else 0)), p["name"]
    return sorted(seen.values(), key=richness)
