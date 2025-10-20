# Interface Bridge Virtual Environment Corruption - Diagnosis & Resolution

**Date**: October 12, 2025 05:00-05:15 AM  
**Issue**: `.venv314t` virtual environment missing critical pyvenv.cfg file  
**Impact**: Interface Bridge cannot start - Python interpreter fails immediately  
**Status**: Root cause identified, resolution plan established

---

## Problem Diagnosis

### Symptoms Observed

1. **Server Health Check Timeout**: Interface Bridge launches but never responds to http://localhost:8000/health
2. **Log File Error**: `failed to locate pyvenv.cfg: El sistema no puede encontrar el archivo especificado.`
3. **Python Execution Failure**: `& "ai\.venv314t\Scripts\python.exe" -m uvicorn --version` exits with code 1
4. **Import Tests Fail**: Cannot import uvicorn even though it's installed

### Root Cause Identified

**Missing Critical File**: `ai\.venv314t\pyvenv.cfg`

```powershell
Test-Path "ai\.venv314t\pyvenv.cfg"  # Returns: False
Test-Path "ai\.venv314t\Scripts\python.exe"  # Returns: True
```

**Python 3.14 Requirement**: Python 3.14+ free-threading builds require pyvenv.cfg to locate:
- Base Python installation path
- Virtual environment configuration
- Site-packages location
- Include directories

### What Happened

**Likely Causes** (in order of probability):
1. **Manual venv manipulation**: Files deleted/moved during cleanup
2. **Incomplete venv creation**: `python -m venv` interrupted
3. **File system corruption**: pyvenv.cfg deleted by antivirus/backup software
4. **Migration artifact**: Directory moved without preserving all metadata files

**Current State**:
- Virtual environment directory exists: `ai\.venv314t\`
- Python executable present: `ai\.venv314t\Scripts\python.exe`
- Configuration file missing: `ai\.venv314t\pyvenv.cfg` (CRITICAL)
- Packages installed: uvicorn, fastapi (confirmed via earlier install_python_packages)
- But Python cannot start: Missing pyvenv.cfg causes immediate failure

---

## Resolution Options

### Option 1: Recreate pyvenv.cfg (RECOMMENDED - Fast)

**Approach**: Manually recreate the missing configuration file

**Steps**:
1. Identify base Python installation
2. Create pyvenv.cfg with proper paths
3. Validate Python starts successfully
4. Test uvicorn import

**pyvenv.cfg Template**:
```ini
home = C:\Python314
include-system-site-packages = false
version = 3.14.0
executable = C:\Python314\python.exe
command = C:\Python314\python.exe -m venv C:\dev\AIOS\ai\.venv314t
```

**Advantages**:
- ✅ Fast: 1 minute to create file
- ✅ Preserves existing packages (uvicorn, fastapi)
- ✅ No reinstallation required
- ✅ Minimal risk

**Disadvantages**:
- ⚠️ Must know correct Python base path
- ⚠️ Version number must match exactly

### Option 2: Recreate Virtual Environment (THOROUGH - Slow)

**Approach**: Delete corrupted venv, create fresh one

**Steps**:
1. Delete `ai\.venv314t` entirely
2. Run `python -m venv ai\.venv314t`
3. Reinstall all packages: uvicorn, fastapi, etc.
4. Update server_manager.py venv detection if needed

**Advantages**:
- ✅ Guaranteed clean state
- ✅ All configuration files present
- ✅ No corruption risk
- ✅ Matches documentation

**Disadvantages**:
- ❌ Slow: 5-10 minutes for package installation
- ❌ Must reinstall all dependencies
- ❌ Potential version mismatches
- ❌ Overkill for single missing file

### Option 3: Use System Python with pip install (TEMPORARY - Quick Test)

**Approach**: Install uvicorn in system Python for immediate testing

**Steps**:
1. Run `pip install uvicorn fastapi` (system Python)
2. Modify server_manager.py temporarily to use sys.executable
3. Test Interface Bridge startup
4. Later: Fix venv properly (Option 1 or 2)

**Advantages**:
- ✅ Very fast: 30 seconds
- ✅ Immediate server validation
- ✅ Unblocks debugging

**Disadvantages**:
- ❌ Pollutes system Python
- ❌ Not AINLP compliant (temporary hack)
- ❌ Still need to fix venv eventually
- ❌ May cause version conflicts

---

## Recommended Resolution Path

### Phase 1: Immediate Unblocking (Option 3)

**Goal**: Get server running NOW to validate architecture

```powershell
# Install in system Python (temporary)
pip install uvicorn fastapi

# Modify server_manager.py to use system Python
# (Comment out venv detection temporarily)

# Test server startup
python ai/server_manager.py start

# Validate health endpoint
Invoke-WebRequest http://localhost:8000/health
```

**Expected Result**: Server starts successfully, health endpoint responds

### Phase 2: Proper Fix (Option 1)

**Goal**: Restore virtual environment to proper state

```powershell
# Find Python base installation
$pythonExe = Get-Command python | Select-Object -ExpandProperty Source
$pythonBase = Split-Path (Split-Path $pythonExe)
Write-Host "Python base: $pythonBase"

# Create pyvenv.cfg
$pyvenvContent = @"
home = $pythonBase
include-system-site-packages = false
version = 3.14.0
executable = $pythonExe
command = $pythonExe -m venv C:\dev\AIOS\ai\.venv314t
"@

Set-Content -Path "ai\.venv314t\pyvenv.cfg" -Value $pyvenvContent

# Validate venv Python now works
& "ai\.venv314t\Scripts\python.exe" -c "import sys; print(sys.executable)"

# Reinstall packages in venv (if needed)
& "ai\.venv314t\Scripts\pip.exe" install uvicorn fastapi
```

**Expected Result**: Virtual environment fully functional

### Phase 3: Revert to Production Mode

**Goal**: Re-enable pythonw.exe windowless mode

```python
# server_manager.py: Uncomment pythonw.exe production code
pythonw = python_dir / "pythonw.exe"
if not pythonw.exists():
    pythonw = self.python_exe

# Re-enable CREATE_NO_WINDOW flag
creationflags = (subprocess.CREATE_NEW_PROCESS_GROUP |
               subprocess.DETACHED_PROCESS |
               0x08000000)  # CREATE_NO_WINDOW
```

**Expected Result**: Silent background service with full persistence

---

## Validation Checklist

After implementing resolution:

**Server Startup**:
- [ ] `python ai/server_manager.py start` succeeds
- [ ] PID file created: `ai/interface_bridge.pid`
- [ ] Log file has uvicorn startup messages (not pyvenv.cfg error)
- [ ] Process visible in Task Manager

**Health Endpoint**:
- [ ] `Invoke-WebRequest http://localhost:8000/health` responds
- [ ] Status code: 200
- [ ] Response body: `{"status":"healthy"}`

**Virtual Environment**:
- [ ] `ai\.venv314t\pyvenv.cfg` exists
- [ ] `& "ai\.venv314t\Scripts\python.exe" -m uvicorn --version` shows version
- [ ] No "failed to locate pyvenv.cfg" errors

**Windows-Native Architecture**:
- [ ] Server survives terminal closure (test with Keep-Alive mode)
- [ ] Server survives VSCode closure
- [ ] Process truly detached from parent

**Keep-Alive Mode**:
- [ ] `.\aios_launch.ps1 -KeepAlive` monitors successfully
- [ ] Health checks every 10 seconds
- [ ] Manual process kill triggers automatic restart
- [ ] Ctrl+C performs graceful shutdown

---

## Next Actions (Priority Order)

1. **IMMEDIATE**: Install uvicorn in system Python (Phase 1)
2. **IMMEDIATE**: Test server startup with system Python
3. **IMMEDIATE**: Validate health endpoint responds
4. **SHORT-TERM**: Create pyvenv.cfg file (Phase 2)
5. **SHORT-TERM**: Reinstall packages in venv if needed
6. **SHORT-TERM**: Revert to pythonw.exe production mode (Phase 3)
7. **MEDIUM-TERM**: Test Keep-Alive monitoring mode
8. **MEDIUM-TERM**: Validate true persistence (terminal/VSCode independence)

---

## AINLP Compliance Notes

**Architectural Discovery**: Identified venv corruption as root blocker  
**Enhancement over Creation**: Recreate pyvenv.cfg vs rebuild entire venv  
**Proper Output Management**: Diagnosis documented in tachyonic archive  
**Integration Validation**: Full validation checklist provided

**Pattern**: AINLP.debug-first approach - diagnose before fix, document findings, provide multiple resolution paths with tradeoffs
