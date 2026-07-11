import pathlib
import pytest


@pytest.fixture
def tmp_claude(tmp_path):
    """一個假的 .claude 目錄骨架,供各測試填內容。"""
    root = tmp_path / ".claude"
    (root / "projects" / "C--Users-acer" / "memory").mkdir(parents=True)
    return root
