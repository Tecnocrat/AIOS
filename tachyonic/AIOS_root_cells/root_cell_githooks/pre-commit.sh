# ARCHIVED: Pre-commit Script (Reference Implementation)
# Originally: #!/bin/sh - REMOVED (Reference only, not executable)
# Location: tachyonic/AIOS_root_cells/root_cell_githooks/
# POSIX fallback wrapper: invokes PowerShell pre-commit if available.
# Minimal logic to ensure cross-platform consistency.

set -euo pipefail
SCRIPT_DIR="$(cd "${BASH_SOURCE[0]%/*}" && pwd)"
PWSH_CMD="pwsh"
if command -v pwsh >/dev/null 2>&1; then
  exec pwsh -NoLogo -NoProfile -File "$SCRIPT_DIR/pre-commit"
elif command -v powershell >/dev/null 2>&1; then
  exec powershell -NoLogo -NoProfile -File "$SCRIPT_DIR/pre-commit"
else
  echo "[AIOS pre-commit] PowerShell not found; skipping advanced checks (FAIL SAFE PASS)" >&2
  exit 0
fi
