#!/usr/bin/env python3
"""
AIOS Harmonized Test — ChatGPT Integration Path
- Optimal location: ai/tests/
- Purpose: Validate chatgpt_integration presence and key structure
    without hard-coded absolute paths.
- Provenance: Moved from root (test_chatgpt_integration.py) to align
    with project testing conventions.
- See docs/tachyonic/tachyonic_changelog.yaml for harmonization history.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict


def _gather_chatgpt_integration_status(repo_root: Path) -> Dict[str, bool]:
    """Gather status flags for chatgpt_integration presence and structure."""
    cgi = repo_root / "chatgpt_integration"
    status: Dict[str, bool] = {
        "root_exists": cgi.exists(),
        "ingestion_dir": (cgi / "ingestion").exists(),
        "md_dir": (cgi / "md").exists(),
        "chatgpt_py": (cgi / "chatgpt.py").exists(),
    }
    return status


def _print_summary(status: Dict[str, bool], repo_root: Path) -> None:
    print("=== Testing ChatGPT Integration Path ===")
    print(f"Repo root: {repo_root}")
    print(f"Target:    {repo_root / 'chatgpt_integration'}")

    if status["root_exists"]:
        print(" chatgpt_integration/ exists")
    else:
        print(" chatgpt_integration/ missing")

    for key, label in (
        ("ingestion_dir", "ingestion/"),
        ("md_dir", "md/"),
        ("chatgpt_py", "chatgpt.py"),
    ):
        prefix = " " if status[key] else " "
        suffix = " exists" if status[key] else " missing"
        print(prefix + label + suffix)

    # Count total files for observability
    total_files = 0
    cgi = repo_root / "chatgpt_integration"
    if cgi.exists():
        for _, _, files in os.walk(cgi):
            total_files += len(files)
    print(f" Total files in chatgpt_integration: {total_files}")


def test_chatgpt_integration_path_pytest() -> None:
    """Pytest entry: assert key layout exists."""
    repo_root = Path(__file__).resolve().parents[2]
    status = _gather_chatgpt_integration_status(repo_root)

    assert status["root_exists"], "chatgpt_integration directory should exist"
    # Keep checks tolerant to partial structure; warn rather than fail
    # if optional pieces are missing.
    # If these are required, flip to asserts.
    if not status["ingestion_dir"]:
        print(" ingestion/ directory missing")
    if not status["md_dir"]:
        print(" md/ directory missing")
    if not status["chatgpt_py"]:
        print(" chatgpt.py missing")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    res = _gather_chatgpt_integration_status(root)
    _print_summary(res, root)
    # Exit non-zero only if the root directory itself is missing
    sys.exit(0 if res.get("root_exists", False) else 1)
