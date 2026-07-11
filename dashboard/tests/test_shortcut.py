from pathlib import Path
from generator.shortcut import ensure_desktop_shortcut


def test_writes_url_shortcut(tmp_path):
    target = tmp_path / "dash" / "index.html"
    target.parent.mkdir()
    target.write_text("<html></html>", encoding="utf-8")
    desktop = tmp_path / "Desktop"
    desktop.mkdir()

    link = ensure_desktop_shortcut(target, desktop, name="Claude 儀表板")
    assert link == desktop / "Claude 儀表板.url"
    text = link.read_text(encoding="utf-8")
    assert "[InternetShortcut]" in text
    assert "URL=file:///" in text
    assert target.name in text.replace("\\", "/")
