from pathlib import Path


def ensure_desktop_shortcut(target_html, desktop_dir, name="Claude 儀表板"):
    target = Path(target_html).resolve()
    url = "file:///" + str(target).replace("\\", "/")
    link = Path(desktop_dir) / f"{name}.url"
    link.write_text(f"[InternetShortcut]\nURL={url}\n", encoding="utf-8")
    return link
