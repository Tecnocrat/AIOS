"""Tests for safety_validate CLI."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run_cli(mode: str):
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "safety_validate.py"),
        "--mode",
        mode,
        "--json",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    assert p.returncode in (0, 2, 3), (
        f"Unexpected exit {p.returncode}: {p.stderr}"
    )
    data = json.loads(p.stdout)
    return p.returncode, data


def test_session_blocks_unauthorized():
    code, data = run_cli("session")
    session = data["session"]
    assert "unauthorized_attempt" in session
    assert session["unauthorized_attempt"]["blocked"] is True


def test_emergency_sets_flag():
    code, data = run_cli("emergency")
    emer = data["emergency"]
    if emer["session_started"]:
        assert emer["emergency_status"]["emergency_stopped"] is True
    else:
        # If session not started, emergency_status may be empty
        assert isinstance(emer["emergency_status"], dict)


def test_both_combined():
    code, data = run_cli("both")
    assert "session" in data and "emergency" in data
