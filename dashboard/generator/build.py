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
