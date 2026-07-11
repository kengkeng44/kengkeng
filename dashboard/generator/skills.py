def build_skills_model(raw):
    raw = raw or {}
    return {group: list(raw.get(group, []) or []) for group in ("custom", "docs", "super")}
