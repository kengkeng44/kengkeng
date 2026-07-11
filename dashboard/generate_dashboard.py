"""重生 Operator's Card 儀表板。收工 Stop hook 或 /refresh-dashboard 呼叫。"""
import os
from pathlib import Path

from generator.build import build_all
from generator.shortcut import ensure_desktop_shortcut

HOME = Path("C:/Users/acer")
CLAUDE_DIR = HOME / ".claude"
DASHBOARD_DIR = HOME / "Desktop" / "kengkeng" / "dashboard"
DESKTOP = HOME / "Desktop"
PROJECT_ROOTS = [HOME / "Desktop", HOME]


def main():
    date = os.environ.get("DASHBOARD_DATE", "").strip() or "—"
    index = build_all(CLAUDE_DIR, DASHBOARD_DIR, PROJECT_ROOTS, date)
    ensure_desktop_shortcut(index, DESKTOP)
    print(f"[dashboard] wrote {index}")


if __name__ == "__main__":
    main()
