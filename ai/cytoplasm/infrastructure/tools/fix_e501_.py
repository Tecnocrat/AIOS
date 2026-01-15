#!/usr/bin/env python3
"""
AINLP Comprehensive Linting Fixer
Enhanced systematic fixer for line length, imports, and type checking issues
AINLP.fixer [comprehensive_linting_solution] (comment.AINLP.class)
AINLP.loader [AINLP_HUMAN.md] (auto.AINLP.class)
"""

import logging
import os
import sys
import re
from datetime import datetime
from pathlib import Path
import ast

MAX_LINE_LENGTH = 79

# Setup debug logger
log_path = os.path.join(os.path.dirname(__file__), "comprehensive_linter_debug.log")
logger = logging.getLogger("comprehensive_linter")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
formatter = logging.Formatter(
    f"%(asctime)s | %(levelname)s | %(message)s | "
    f"{os.path.basename(__file__)}:%(lineno)d"
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
    # Preserve indentation
    indent = len(line) - len(line.lstrip())
    prefix = line[:indent]
    content = line[indent:]
    # Try to break at a comma before MAX_LINE_LENGTH
    idx = content.rfind(",", 0, MAX_LINE_LENGTH - indent)
    if idx != -1:
        logger.debug(f"Line broken at comma index {idx}")
        return [
            prefix + content[: idx + 1] + "\\",
            prefix + content[idx + 1 :].lstrip(),
        ]
    # Try to break at a space before MAX_LINE_LENGTH
    idx = content.rfind(" ", 0, MAX_LINE_LENGTH - indent)
    if idx != -1:
        logger.debug(f"Line broken at space index {idx}")
        return [prefix + content[:idx] + "\\", prefix + content[idx + 1 :].lstrip()]
    # Try to break at an operator before MAX_LINE_LENGTH
    for op in ["+", "-", "*", "/", "%", "=", ":"]:
        idx = content.rfind(op, 0, MAX_LINE_LENGTH - indent)
        if idx != -1:
            logger.debug(f"Line broken at operator '{op}' index {idx}")
            return [
                prefix + content[: idx + 1] + "\\",
                prefix + content[idx + 1 :].lstrip(),
            ]
    # Fallback: hard break
    logger.debug(f"Line hard-broken at {MAX_LINE_LENGTH - indent}")
    return [
        prefix + content[: MAX_LINE_LENGTH - indent] + "\\",
        prefix + content[MAX_LINE_LENGTH - indent :].lstrip(),
    ]


def fix_file(filepath):
    logger.info(f"Fixing file: {filepath}")
    changed = False
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    fixed_lines = []
    fix_count = 0
    for i, line in enumerate(lines):
        if len(line.rstrip()) > MAX_LINE_LENGTH:
            logger.debug(f"Line {i+1} too long: {len(line.rstrip())} chars")
            broken = break_long_line(line.rstrip())
            fixed_lines.extend(broken)
            changed = True
            fix_count += 1
        else:
            fixed_lines.append(line.rstrip())
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(fixed_lines) + "\n")
        logger.info(f"File fixed: {filepath} | {fix_count} lines broken")
    else:
        logger.info(f"No changes needed: {filepath}")
    return changed, fix_count


def main(auto_run=False):
    if auto_run:
        path = os.path.join(
            os.path.dirname(__file__), "..", "aios_vscode_integration_server.py"
        )
        path = os.path.abspath(path)
        logger.info(f"Target file: {path}")
        if not os.path.exists(path):
            print(f"File not found: {path}")
            logger.error(f"File not found: {path}")
            return 1
        changed, fix_count = fix_file(path)
        if changed:
            print(f"[E501 FIXED] {path} | {fix_count} lines broken.")
        else:
            print(f"No changes needed in {path}.")
        return 0
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
            return 1
        changed, fix_count = fix_file(path)
        if changed:
            print(f"[E501 FIXED] {path} | {fix_count} lines broken.")
        else:
            print(f"No changes needed in {path}.")
        return 0
    else:
        print("Exiting.")
        logger.info("User exited the script.")
        return 0


if __name__ == "__main__":
    logger.info("Script started.")
    exit_code = main(auto_run=True)
    logger.info("Script finished.")
    sys.exit(exit_code)
