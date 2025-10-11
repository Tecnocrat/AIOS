"""Safety Gateway

JSON runtime entrypoint for manual or autonomous safety introspection.
Modes:
    precheck   - run a dry safety pre-experiment verification (dummy values)
    status     - current governor status
    diffs      - recent mutation diffs (tachyonic rollback layer)
    restore    - restore a snapshot hash/prefix (requires --hash)
"""
from __future__ import annotations
import argparse
import json
import sys
from typing import Any, Dict, Optional, List
from pathlib import Path


def run_precheck() -> Dict[str, Any]:
    from safety_governor import get_safety_governor
    gov = get_safety_governor()
    result = gov.verify_pre_experiment(30, 10)
    return result


def run_status() -> Dict[str, Any]:
    from safety_governor import get_safety_governor
    return get_safety_governor().get_status()


def run_diffs() -> Dict[str, Any]:
    try:
        from runtime_intelligence.tools import safety_rollback
        diffs = safety_rollback.list_diffs(25)
        return {"count": len(diffs), "recent": diffs}
    except Exception as e:
        return {"error": str(e)}


def run_restore(hash_prefix: str,
                dest: Optional[str],
                overwrite: bool) -> Dict[str, Any]:
    try:
        from runtime_intelligence.tools import safety_rollback
        dest_path = Path(dest) if dest else None
        restored_path = safety_rollback.restore_snapshot(
            hash_prefix,
            dest_path,
            overwrite=overwrite
        )
        return {"restored_to": str(restored_path), "hash_prefix": hash_prefix}
    except Exception as e:
        return {"error": str(e), "hash_prefix": hash_prefix}


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "mode",
        choices=["precheck", "status", "diffs", "restore"],
        help="Gateway mode"
    )
    ap.add_argument(
        "--hash",
        dest="hash_prefix",
        help="Snapshot hash or prefix for restore mode"
    )
    ap.add_argument(
        "--dest",
        dest="dest_path",
        help="Optional destination path for restore"
    )
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwrite of existing destination file"
    )
    args = ap.parse_args(argv)
    if args.mode == "precheck":
        payload = run_precheck()
    elif args.mode == "status":
        payload = run_status()
    elif args.mode == "diffs":
        payload = run_diffs()
    else:  # restore
        if not args.hash_prefix:
            print(json.dumps({"error": "--hash required for restore mode"}))
            return 2
        payload = run_restore(args.hash_prefix, args.dest_path, args.overwrite)
    print(
        json.dumps(
            {"mode": args.mode, "payload": payload},
            ensure_ascii=False
        )
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
