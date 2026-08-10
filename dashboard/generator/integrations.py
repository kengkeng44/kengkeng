"""已接平台(MCP 整合)模型。資料來源 data/integrations.yaml,手動維護。"""

# 排序:已連線 → 需重連 → 專案限定 → 未連線
STATUS_ORDER = {"ok": 0, "warn": 1, "project": 2, "off": 3}


def build_integrations_model(yaml_data):
    if isinstance(yaml_data, dict):
        raw = yaml_data.get("integrations", [])
    elif isinstance(yaml_data, list):
        raw = yaml_data
    else:
        raw = []

    items = []
    for it in raw:
        if not isinstance(it, dict):
            continue
        items.append({
            "name": it.get("name", ""),
            "id": it.get("id", ""),
            "status": it.get("status", "ok"),
            "scope": it.get("scope", ""),
            "zh": it.get("zh", ""),
        })
    items.sort(key=lambda x: (STATUS_ORDER.get(x["status"], 9), str(x["name"]).lower()))
    return items
