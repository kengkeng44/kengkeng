from pathlib import Path
import json
import yaml

from .memory import build_memory_model
from .permissions import build_permissions_model
from .skills import build_skills_model
from .integrations import build_integrations_model
from .projects import discover_projects
from .render import render_index


def _load_yaml(path):
    if Path(path).exists():
        try:
            return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            return {}
    return {}


def build_all(claude_dir, dashboard_dir, project_roots, date):
    claude_dir, dashboard_dir = Path(claude_dir), Path(dashboard_dir)
    data = dashboard_dir / "data"
    memory_dir = claude_dir / "projects" / "C--Users-acer" / "memory"
    settings_path = claude_dir / "settings.json"
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    perm_raw = _load_yaml(data / "perm-descriptions.yaml")
    perm_descs = perm_raw.get("descriptions", perm_raw) if isinstance(perm_raw, dict) else {}

    models = {
        "memory": build_memory_model(memory_dir, _load_yaml(data / "priorities.yaml")),
        "permissions": build_permissions_model(settings, perm_descs),
        "skills": build_skills_model(_load_yaml(data / "skills.yaml")),
        "integrations": build_integrations_model(_load_yaml(data / "integrations.yaml")),
        # 排除家目錄與 ~/.claude 本身:後者有 CLAUDE.md 所以會被 glob 命中,
        # 但它是設定目錄不是 repo(沒有 .git),列進來會讓「N 個追蹤中的 repo」
        # 這句話不成立 —— 而且 memory / permissions / skills 三個分頁本來就在
        # 描述這個目錄,再列成專案是自我指涉。
        "projects": discover_projects(
            project_roots, exclude=[claude_dir.parent, claude_dir]),
        "generated_at": date,
    }
    html = render_index(models)
    out = dashboard_dir / "index.html"
    if not out.exists() or out.read_text(encoding="utf-8") != html:
        out.write_text(html, encoding="utf-8")
    return out
