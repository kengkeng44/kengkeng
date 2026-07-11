def _decorate(patterns, descs):
    out = []
    for p in patterns:
        d = descs.get(p) or {}
        out.append({"pattern": p, "en": d.get("en", p), "zh": d.get("zh", p)})
    return out


def build_permissions_model(settings, descs):
    perms = settings.get("permissions", {})
    return {
        "allow": _decorate(perms.get("allow", []), descs),
        "ask": _decorate(perms.get("ask", []), descs),
        "deny": _decorate(perms.get("deny", []), descs),
        "defaultMode": perms.get("defaultMode", "default"),
    }
