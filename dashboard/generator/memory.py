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
