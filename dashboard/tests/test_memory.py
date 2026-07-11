from generator.memory import build_memory_model


def _write(path, name, desc, mtype):
    path.write_text(
        f"---\nname: {name}\ndescription: {desc}\nmetadata:\n  type: {mtype}\n---\nbody\n",
        encoding="utf-8",
    )


def test_builds_entries_and_skips_index(tmp_path):
    mem = tmp_path / "memory"
    mem.mkdir()
    _write(mem / "feedback_a.md", "feedback-a", "規則 A", "feedback")
    _write(mem / "user_b.md", "user-b", "使用者 B", "user")
    (mem / "MEMORY.md").write_text("- index line\n", encoding="utf-8")

    priorities = {"feedback_a.md": "red"}
    entries = build_memory_model(mem, priorities)

    by_name = {e["name"]: e for e in entries}
    assert "feedback-a" in by_name and "user-b" in by_name
    assert "index" not in " ".join(by_name)  # MEMORY.md 被跳過
    assert by_name["feedback-a"]["priority"] == "red"
    assert by_name["user-b"]["priority"] == "green"   # 查無預設 green
    assert by_name["feedback-a"]["type"] == "feedback"
