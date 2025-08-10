"""
DEPRECATED: system_status_report.py at repository root

This entrypoint has moved to the canonical location:
  runtime_intelligence/tools/system_status_report.py

Use the VS Code task "python-system-status" or run the canonical
script. This stub exits intentionally to prevent drift and ensure a
single source of truth.
"""

from __future__ import annotations

MSG = (
    "system_status_report.py has moved to runtime_intelligence/tools/.\n"
    "Run: python runtime_intelligence/tools/system_status_report.py\n"
    "Or use the VS Code task: python-system-status"
)


def main() -> int:
    print(MSG)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
