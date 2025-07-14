#!/usr/bin/env python3
"""
AINLP E501 Comprehensive Fixer
Systematically fixes line length violations with a simple CLI UI and debug logging
AINLP.fixer [comprehensive_e501_solution] (comment.AINLP.class)
"""

import logging
import os
import sys
from datetime import datetime

MAX_LINE_LENGTH = 79

# Setup debug logger
log_path = os.path.join(os.path.dirname(__file__), "e501_fixer_debug.log")
logger = logging.getLogger("e501_fixer")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s | %(filename)s:%(lineno)d"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def break_long_line(line):
    logger.debug(f"Breaking line: {line!r}")
    if len(line) <= MAX_LINE_LENGTH:
        return [line]
    # Don't break URLs, docstrings, or comments
    if (
        "http" in line
        or line.strip().startswith("#")
        or line.strip().startswith('"""')
        or line.strip().startswith("'''")
    ):
        logger.debug("Skipping line (URL, comment, or docstring)")
        return [line]
    # Try to break at a space before MAX_LINE_LENGTH
    idx = line.rfind(" ", 0, MAX_LINE_LENGTH)
    if idx == -1:
        idx = MAX_LINE_LENGTH
    logger.debug(f"Line broken at index {idx}")
    return [line[:idx] + "\\", line[idx:].lstrip()]


def fix_file(filepath):
    logger.info(f"Fixing file: {filepath}")
    changed = False
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    fixed_lines = []
    for i, line in enumerate(lines):
        if len(line.rstrip()) > MAX_LINE_LENGTH:
            logger.debug(f"Line {i+1} too long: {len(line.rstrip())} chars")
            broken = break_long_line(line.rstrip())
            fixed_lines.extend(broken)
            changed = True
        else:
            fixed_lines.append(line.rstrip())
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(fixed_lines) + "\n")
        logger.info(f"File fixed: {filepath}")
    else:
        logger.info(f"No changes needed: {filepath}")
    return changed


def main():
    print("AINLP E501 Fixer CLI")
    print("1. Fix aios_vscode_integration_server.py")
    print("2. Exit")
    choice = input("Choose an option: ").strip()
    logger.info(f"User choice: {choice}")
    if choice == "1":
        path = os.path.join(
            os.path.dirname(__file__), "..", "aios_vscode_integration_server.py"
        )
        path = os.path.abspath(path)
        logger.info(f"Target file: {path}")
        if not os.path.exists(path):
            print(f"File not found: {path}")
            logger.error(f"File not found: {path}")
            return
        changed = fix_file(path)
        if changed:
            print(f"[E501 FIXED] {path}")
        else:
            print(f"No changes needed in {path}.")
    else:
        print("Exiting.")
        logger.info("User exited the script.")


if __name__ == "__main__":
    logger.info("Script started.")
    main()
    logger.info("Script finished.")
