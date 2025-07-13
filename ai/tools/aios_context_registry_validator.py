"""
aios_context_registry_validator.py

This script validates the .aios_context.json registry against the actual file system.
- Flags missing, orphaned, or untagged files.
- Suggests context tag updates for new or changed files.
- Can be extended to auto-update the registry or trigger harmonization routines.
"""

import argparse
import hashlib
import json
import os
import time
from pathlib import Path

REGISTRY_PATH = Path(".aios_context.json")
PROJECT_ROOT = Path(".")

# Load registry


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Scan files in the project directory


def scan_files(root):
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            fpath = Path(dirpath) / fname
            # Ignore hidden/system files
            if any(part.startswith(".") for part in fpath.parts):
                continue
            yield fpath.relative_to(root)


def is_relevant_file(fpath):
    # Ignore common build/output folders and files
    ignored_dirs = {
        "__pycache__",
        "venv",
        "node_modules",
        ".git",
        ".pytest_cache",
        ".vscode",
    }
    if any(part in ignored_dirs for part in fpath.parts):
        return False
    # Only include relevant file extensions
    relevant_exts = {
        ".py",
        ".cs",
        ".cpp",
        ".h",
        ".hpp",
        ".json",
        ".md",
        ".yml",
        ".yaml",
        ".toml",
        ".sln",
        ".ps1",
        ".sh",
        ".ts",
        ".js",
        ".html",
        ".xml",
        ".bat",
        ".ini",
        ".txt",
    }
    return fpath.suffix.lower() in relevant_exts


def guess_file_type(fpath):
    ext = fpath.suffix.lower()
    if ext in {".py", ".ps1", ".sh"}:
        if "test" in fpath.name.lower():
            return "testing"
        if "cell" in fpath.name.lower() or "cell" in str(fpath.parent).lower():
            return "cellular_ai"
        if "integration" in str(fpath.parent).lower():
            return "core_logic"
        return "core_logic"
    if ext in {".cs", ".cpp", ".h", ".hpp"}:
        return "core_logic"
    if ext in {".json", ".yml", ".yaml", ".toml", ".ini"}:
        return "configs"
    if ext in {".md", ".txt"}:
        return "documentation"
    if ext in {".sln"}:
        return "core_logic"
    if ext in {".html", ".xml", ".js", ".ts"}:
        return "core_logic"
    return "unknown"


def guess_tags(fpath):
    tags = []
    name = fpath.name.lower()
    if "tensorflow" in name:
        tags.append("tensorflow")
    if "cell" in name or "cell" in str(fpath.parent).lower():
        tags.append("cellular")
    if "ainlp" in name or "ainlp" in str(fpath.parent).lower():
        tags.append("ainlp")
    if "test" in name:
        tags.append("testing")
    if "integration" in str(fpath.parent).lower():
        tags.append("integration")
    if ext := fpath.suffix.lower():
        tags.append(ext.lstrip("."))
    return list(set(tags))


def file_content_hash(fpath):
    try:
        with open(fpath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return ""


def autofix_registry(registry, missing_files, orphaned_files, yes=False):
    updated = False
    for f in missing_files:
        ftype = guess_file_type(f)
        tags = guess_tags(f)
        entry = {
            "file_type": ftype,
            "last_modified": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "last_accessed": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "access_frequency": 1.0,
            "modification_frequency": 1.0,
            "context_importance": 0.5,
            "reingestion_potential": 0.5,
            "file_classification": "active",
            "ai_context_tags": tags,
            "content_hash": file_content_hash(f),
            "size_bytes": f.stat().st_size if f.exists() else 0,
            "cellular_relationships": [],
        }
        registry[str(f)] = entry
        print(f"[AUTO-ADD] {f} -> {ftype}, tags: {tags}")
        updated = True
    for f in orphaned_files:
        if str(f) in registry:
            del registry[str(f)]
            print(f"[AUTO-REMOVE] {f}")
            updated = True
    if updated and (
        yes
        or input("Write changes to .aios_context.json? [y/N] ").lower().startswith("y")
    ):
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)
        print("Registry updated.")
    elif updated:
        print("No changes written.")
    else:
        print("No harmonization needed.")


def main():
    parser = argparse.ArgumentParser(
        description="AIOS Context Registry Validator & Autocoder"
    )
    parser.add_argument(
        "--autofix", action="store_true", help="Auto-harmonize registry (add/remove)"
    )
    parser.add_argument(
        "--yes", action="store_true", help="Write changes without prompt"
    )
    args = parser.parse_args()

    registry = load_registry()
    registered_files = set(Path(f) for f in registry.keys())
    actual_files = set(scan_files(PROJECT_ROOT))
    relevant_files = set(f for f in actual_files if is_relevant_file(f))
    missing_in_registry = relevant_files - registered_files
    orphaned_in_registry = registered_files - actual_files

    print("=== AIOS Context Registry Validation (Filtered) ===")
    print(f"Relevant files missing in registry: {len(missing_in_registry)}")
    for f in sorted(missing_in_registry):
        print(f"  [NEW] {f}")
    print(f"Orphaned files in registry: {len(orphaned_in_registry)}")
    for f in sorted(orphaned_in_registry):
        print(f"  [ORPHAN] {f}")
    print("Validation complete.")

    if args.autofix:
        autofix_registry(
            registry, missing_in_registry, orphaned_in_registry, yes=args.yes
        )


if __name__ == "__main__":
    main()
