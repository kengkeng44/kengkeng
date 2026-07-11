from generator.permissions import build_permissions_model


def test_maps_patterns_with_descriptions():
    settings = {
        "permissions": {
            "allow": ["Read", "Bash(git status *)"],
            "ask": ["Bash(rm *)"],
            "deny": [],
            "defaultMode": "bypassPermissions",
        }
    }
    descs = {"Read": {"en": "read files", "zh": "讀檔"}}
    model = build_permissions_model(settings, descs)

    assert model["defaultMode"] == "bypassPermissions"
    allow = {i["pattern"]: i for i in model["allow"]}
    assert allow["Read"]["zh"] == "讀檔"
    # 查無說明 → 用 pattern 原文
    assert allow["Bash(git status *)"]["zh"] == "Bash(git status *)"
    assert model["ask"][0]["pattern"] == "Bash(rm *)"
    assert model["deny"] == []
