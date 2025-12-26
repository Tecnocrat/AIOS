#!/usr/bin/env python3
"""Generate AIOS spatial metadata snapshot.

Usage:
  generate_spatial_metadata.py [--target PATH] [--force] [--max-age-minutes N]

Writes JSON to the target (default: scripts/.aios_spatial_metadata.json).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Import the AIOS discovery API at module import time so errors surface
# early and linter flags about imports-in-functions are avoided.
import ai


def generate(target: Path) -> None:
    """Generate the spatial metadata JSON and write it to `target`.

    The function calls `ai.discover_available_components()` and writes
    a JSON object containing a `generation_timestamp`, `spatial_context`,
    and `components` map.
    """

    # Call discovery and assemble output
    comps = ai.discover_available_components()
    out = {
        "generation_timestamp": datetime.now(timezone.utc).isoformat(),
        "spatial_context": {"child_folders": list(comps.keys())},
        "components": comps,
    }

    # Ensure parent exists and write file
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"WROTE {target}")


def main(argv: list[str] | None = None) -> int:
    """Parse CLI args and generate the spatial metadata file.

    Returns an exit code integer suitable for use by a wrapper process.
    """

    p = argparse.ArgumentParser(description="Generate AIOS spatial metadata")
    p.add_argument("--target", default="scripts/.aios_spatial_metadata.json")
    p.add_argument("--force", action="store_true")
    p.add_argument("--max-age-minutes", type=int, default=30,
                   help="Skip generation if file younger than this (unless --force)")
    args = p.parse_args(argv)

    target = Path(args.target)
    if target.exists() and not args.force:
        try:
            mtime = datetime.fromtimestamp(target.stat().st_mtime, tz=timezone.utc)
            age = datetime.now(timezone.utc) - mtime
            if age < timedelta(minutes=args.max_age_minutes):
                print(f"SKIP: {target} is recent ({age})")
                return 0
        except (OSError, ValueError):
            # If the file cannot be stat'ed or timestamp parsed, continue
            # and attempt generation.
            pass

    try:
        generate(target)
        return 0
    except (ImportError, RuntimeError, OSError, ValueError) as e:
        # Catch known error classes that can arise during discovery or IO.
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
