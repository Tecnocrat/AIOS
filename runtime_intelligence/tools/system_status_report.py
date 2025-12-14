"""
AIOS System Status Report
Canonical location for status summary invoking the health monitor.

Usage:
- Prefer the VS Code task "python-system-health" for full diagnostics.
- This script prints a concise summary and points to the archived report.
"""

from __future__ import annotations

import json
from pathlib import Path


def show_system_status() -> int:
    """Run the canonical health monitor and print a concise summary."""
    root = Path(__file__).parent
    health_path = root / "system_health_check.py"
    if not health_path.exists():
        print("Health checker not found:", health_path)
        return 2

    # Import without altering sys.path globally
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "system_health_check",
        str(health_path),
    )
    if spec is None or spec.loader is None:
        print("Unable to load health checker module")
        return 2
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[arg-type]

    monitor = mod.AIOSSystemHealthMonitor()
    passed, total, status = monitor.run_comprehensive_health_check()

    print("\n" + "=" * 80)
    print("AIOS SYSTEM STATUS SUMMARY")
    print("=" * 80)
    print(f"Checks Passed: {passed}/{total}")
    print(f"Overall Status: {status}")
    # Locate tachyonic archive directory
    tach_dir = (
        Path(__file__).parents[2] / "docs" / "tachyonic_archive"
    ).resolve()
    latest = tach_dir / "system_health_report.latest.json"
    if latest.exists():
        try:
            data = json.loads(latest.read_text(encoding="utf-8"))
            print("Latest pointer:", latest)
            print("Timestamp:", data.get("timestamp"))
        except (OSError, json.JSONDecodeError):
            print("Latest pointer:", latest)

    # Show most recent immutable snapshot if present
    try:
        snapshots = sorted(tach_dir.glob("system_health_report_*.json"))
        if snapshots:
            print("Newest snapshot:", snapshots[-1])
    except OSError:
        pass
    print("=" * 80)
    return 0 if status in ("EXCELLENT", "GOOD") else 1


if __name__ == "__main__":
    raise SystemExit(show_system_status())
