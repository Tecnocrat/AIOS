#!/usr/bin/env python3
"""
Simple append-only governance logger for registry read/write events.
Writes newline-delimited JSON entries under `tachyonic/governance/governance_log.jsonl`.
Provides a small API and CLI for manual append and viewing.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

LOG_DIR = Path(__file__).resolve().parents[3] / "tachyonic" / "governance"
LOG_FILE = LOG_DIR / "governance_log.jsonl"


def now_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_entry(action: str, actor: str | None = None, details: Dict[str, Any] | None = None) -> Path:
    """Append an entry to the governance log and return the path."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": now_z(),
        "action": action,
        "actor": actor or "unknown",
        "details": details or {},
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return LOG_FILE


def read_entries(limit: int | None = 100) -> list:
    """Return recent entries from the governance log."""
    if not LOG_FILE.exists():
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines if l.strip()]
    if limit:
        lines = lines[-limit:]
    return [json.loads(l) for l in lines]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Governance logger CLI")
    parser.add_argument("--append", nargs=1, help="Append a JSON object as details")
    parser.add_argument("--action", default="manual", help="Action name")
    parser.add_argument("--actor", default=None, help="Actor name")
    parser.add_argument("--show", action="store_true", help="Show recent entries")
    args = parser.parse_args()

    if args.append:
        try:
            details = json.loads(args.append[0])
        except Exception:
            details = {"raw": args.append[0]}
        path = append_entry(args.action, actor=args.actor, details=details)
        print(f"Appended to {path}")
    elif args.show:
        for e in read_entries(100):
            print(json.dumps(e, ensure_ascii=False))
    else:
        parser.print_help()
