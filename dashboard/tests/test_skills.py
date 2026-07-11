from generator.skills import build_skills_model


def test_normalizes_groups():
    raw = {"custom": [{"name": "sync-x"}], "docs": [{"name": "pdf"}]}
    model = build_skills_model(raw)
    assert [s["name"] for s in model["custom"]] == ["sync-x"]
    assert model["super"] == []          # 缺組補空
    assert set(model.keys()) == {"custom", "docs", "super"}
