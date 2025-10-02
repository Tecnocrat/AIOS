import os
import re

EXCLUDE_DIRS = {"venv", ".venv", "env", "__pycache__", ".git", "site-packages"}
LOG_FILE = "init_audit_report.txt"

# Patterns that indicate substantial logic
LOGIC_PATTERNS = [
    re.compile(r"^\s*class\s+"),
    re.compile(r"^\s*def\s+"),
    re.compile(r"^\s*async\s+def\s+"),
    re.compile(r"^\s*import\s+"),
    re.compile(r"^\s*from\s+"),
]

# Threshold for 'long' file
LONG_FILE_LINES = 40


def should_exclude(path):
    parts = set(path.split(os.sep))
    return bool(parts & EXCLUDE_DIRS)


def scan_init_py(root_dir):
    results = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude unwanted directories in-place
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if filename == "__init__.py":
                full_path = os.path.join(dirpath, filename)
                if should_exclude(full_path):
                    continue
                with open(
                    full_path, "r", encoding="utf-8", errors="ignore"
                ) as f:
                    lines = f.readlines()
                logic_lines = [
                    i
                    for i, line in enumerate(lines, 1)
                    if any(p.match(line) for p in LOGIC_PATTERNS)
                ]
                if len(lines) > LONG_FILE_LINES or logic_lines:
                    results.append(
                        {
                            "path": full_path,
                            "lines": len(lines),
                            "logic_lines": logic_lines,
                        }
                    )
    return results


def main():
    root = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(root, "..", ".."))
    results = scan_init_py(project_root)
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        for entry in results:
            log.write(f"{entry['path']}\n")
            log.write(f"  Total lines: {entry['lines']}\n")
            log.write(f"  Logic lines: {entry['logic_lines']}\n\n")
        log.write(
            (
                f"\nTotal __init__.py files with substantial logic: "
                f"{len(results)}\n"
            )
        )
    print(f"Audit complete. See {LOG_FILE} for details.")


if __name__ == "__main__":
    main()
