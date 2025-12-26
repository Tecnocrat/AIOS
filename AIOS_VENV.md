AIOS `.venv` — Recommended usage

- Purpose: use `c:\dev\AIOS\.venv` as the canonical Python runtime for AIOS tools and diagnostics.

Recommended environment variable

- `AIOS_WORKSPACE`: set to the absolute path of your AIOS workspace root (example: `C:\dev\AIOS`).
  - Scripts prefer `AIOS_WORKSPACE` to locate the canonical `.venv` and config files.
  - Set temporarily (PowerShell):

```powershell
$env:AIOS_WORKSPACE = 'C:\dev\AIOS'
```

  - Set persistently (PowerShell):

```powershell
setx AIOS_WORKSPACE "C:\dev\AIOS" /M
```

  - Or via Windows Settings → Environment Variables → add to User variables.

Why set it

- Ensures scripts find the pre-provisioned `.venv` (no need for global `pip` installs).
- Avoids multiple conflicting virtual environments and makes automation idempotent.

Security & operational cautions

- Do NOT set `AIOS_WORKSPACE` to a path containing secrets or tokens. Keep secrets in a secure store or in a `.env` file excluded from VCS.
- If multiple AIOS workspaces exist, set `AIOS_WORKSPACE` per-shell/session rather than system-wide to avoid cross-repo collisions.
- Confirm `.venv` is owned by your user and not a system-wide environment to avoid permission issues.

Quick commands

Activate and use `.venv`:

```powershell
# Activate
C:\dev\AIOS\.venv\Scripts\Activate.ps1
# Install requirements (one-time)
C:\dev\AIOS\.venv\Scripts\pip.exe install -r requirements.txt
# Run diagnostics
C:\dev\AIOS\.venv\Scripts\python.exe ai\infrastructure\tools\dendritic_config_agent.py --validate-multiagent
```

Creating a per-repo venv (if needed):

```powershell
cd path\to\repo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If you want, I can add a brief note to `aios-win` scripts explaining `AIOS_WORKSPACE` usage.