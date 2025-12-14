"""Safety Rollback & Diff Layer

Tachyonic nucleus bridge providing:
- File snapshot (content-addressed)
- Unified diff logging (JSONL)
- Guarded write confinement to evolution_lab
- Snapshot manifest for path-aware restore

This module now embeds original path & timestamp metadata into a snapshot
manifest (JSONL) enabling deterministic restoration by hash (or prefix).
"""

from __future__ import annotations
import hashlib
import json
import difflib
import shutil
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

BASE = Path("c:/dev/AIOS")
SNAP_ROOT = BASE / "docs/tachyonic/rollback_snapshots"
DIFF_LOG = SNAP_ROOT / "diffs.jsonl"
SNAP_MANIFEST = SNAP_ROOT / "snapshots.jsonl"  # One JSON object per line
SNAP_ROOT.mkdir(parents=True, exist_ok=True)


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def snapshot_file(path: Path) -> Dict[str, Any]:
    """Create (or reuse) a content-addressed snapshot of a file.

    Writes raw bytes to shard/<hash>.snap and appends metadata to manifest.
    If snapshot already exists, only metadata append (idempotent path record).
    """
    path = Path(path)
    data = path.read_bytes()
    h = _hash(data)
    shard = SNAP_ROOT / h[:2]
    shard.mkdir(exist_ok=True)
    snap_path = shard / f"{h}.snap"
    created = False
    if not snap_path.exists():
        snap_path.write_bytes(data)
        created = True
    rec = {
        "path": str(path.resolve()),
        "hash": h,
        "size": len(data),
        "timestamp": time.time(),
        "created": created,
    }
    # Append manifest record (multiple paths may share identical hash)
    with SNAP_MANIFEST.open("a", encoding="utf-8") as mf:
        mf.write(json.dumps(rec) + "\n")
    return rec


def diff_and_log(before: Path, after: Path) -> Dict[str, Any]:
    a = before.read_text().splitlines()
    b = after.read_text().splitlines()
    diff_lines = list(
        difflib.unified_diff(a, b, fromfile=str(before), tofile=str(after), lineterm="")
    )
    rec = {
        "timestamp": time.time(),
        "before": str(before),
        "after": str(after),
        "diff_hash": _hash("\n".join(diff_lines).encode()),
        "lines": diff_lines,
    }
    DIFF_LOG.parent.mkdir(parents=True, exist_ok=True)
    with DIFF_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def guarded_write(
    target: Path, new_text: str, allow_outside: bool = False
) -> Dict[str, Any]:
    lab_prefix = str((BASE / "evolution_lab").resolve())
    if not allow_outside and not str(target.resolve()).startswith(lab_prefix):
        raise PermissionError(f"Denied write outside evolution_lab: {target}")
    before_meta = snapshot_file(target) if target.exists() else None
    tmp = target.with_suffix(target.suffix + ".__tmpwrite")
    tmp.write_text(new_text, encoding="utf-8")
    if target.exists():
        diff_and_log(target, tmp)
    shutil.move(str(tmp), str(target))
    after_meta = snapshot_file(target)
    return {"before": before_meta, "after": after_meta}


def list_diffs(limit: int = 50) -> List[Dict[str, Any]]:
    if not DIFF_LOG.exists():
        return []
    text = DIFF_LOG.read_text(encoding="utf-8").strip()
    if not text:
        return []
    lines = text.splitlines()
    return [json.loads(line) for line in lines[-limit:]]


def _find_snapshot_hash(hash_prefix: str) -> Optional[str]:
    """Return unique hash for prefix; None if no match; error if ambiguous."""
    if not SNAP_MANIFEST.exists():
        return None
    matches = set()
    with SNAP_MANIFEST.open("r", encoding="utf-8") as mf:
        for line in mf:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            h = obj.get("hash")
            if h and h.startswith(hash_prefix):
                matches.add(h)
    if not matches:
        return None
    if len(matches) > 1:
        raise ValueError(
            f"Ambiguous hash prefix {hash_prefix}; matches: {sorted(matches)}"
        )
    return next(iter(matches))


def restore_snapshot(
    hash_prefix: str, dest_path: Optional[Path] = None, overwrite: bool = False
) -> Path:
    """Restore a snapshot identified by full/partial hash.

    If dest_path is None, original path from latest manifest record is used.
    Returns the restored Path.
    """
    resolved_hash = _find_snapshot_hash(hash_prefix)
    if not resolved_hash:
        raise FileNotFoundError(f"No snapshot hash matches prefix: {hash_prefix}")
    shard = SNAP_ROOT / resolved_hash[:2]
    snap_file = shard / f"{resolved_hash}.snap"
    if not snap_file.exists():
        raise FileNotFoundError(f"Snapshot bytes missing for hash {resolved_hash}")
    original_path: Optional[Path] = None
    if SNAP_MANIFEST.exists():
        # find latest manifest entry for this hash (last occurrence)
        with SNAP_MANIFEST.open("r", encoding="utf-8") as mf:
            for line in mf:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("hash") == resolved_hash:
                    original_path = Path(obj.get("path")) if obj.get("path") else None
    target = Path(dest_path) if dest_path else original_path
    if not target:
        raise ValueError("Destination path not provided and original path unknown.")
    if target.exists() and not overwrite:
        raise FileExistsError(
            f"Target exists: {target}; use overwrite=True to replace."
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    data = snap_file.read_bytes()
    target.write_bytes(data)
    return target


__all__ = [
    "snapshot_file",
    "diff_and_log",
    "guarded_write",
    "list_diffs",
    "restore_snapshot",
    "SNAP_ROOT",
    "DIFF_LOG",
    "SNAP_MANIFEST",
]
