import yaml


def parse_frontmatter(text):
    """回傳 (meta: dict, body: str)。無 frontmatter 時 meta 為 {}。"""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            meta = yaml.safe_load(parts[1]) or {}
            return meta, parts[2]
    return {}, text
