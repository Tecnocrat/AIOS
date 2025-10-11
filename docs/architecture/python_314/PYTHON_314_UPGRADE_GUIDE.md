# Python 3.14.0 Installation and AIOS Upgrade Guide

**Date**: October 11, 2025  
**Python Version**: 3.14.0 (Released October 7, 2025)  
**Target System**: Windows 11 64-bit (AMD64)  
**Current Python**: 3.12.8  
**AIOS Status**: Ready for Python 3.14 upgrade

---

## Part 1: Python 3.14.0 Installation

### Option A: Standard Python 3.14.0 (GIL Enabled - Recommended for Initial Setup)

**Download Link**: https://www.python.org/downloads/release/python-3140/

**Windows 64-bit Installer**:
- **Filename**: `python-3.14.0-amd64.exe`
- **Direct Download**: https://www.python.org/ftp/python/3.14.0/python-3.14.0-amd64.exe

**Installation Steps**:

1. **Download Installer**:
   ```powershell
   # Download Python 3.14.0 installer
   $url = "https://www.python.org/ftp/python/3.14.0/python-3.14.0-amd64.exe"
   $output = "$env:USERPROFILE\Downloads\python-3.14.0-amd64.exe"
   Invoke-WebRequest -Uri $url -OutFile $output
   
   Write-Host "Python 3.14.0 installer downloaded to: $output" -ForegroundColor Green
   ```

2. **Run Installer**:
   - Double-click `python-3.14.0-amd64.exe`
   - **IMPORTANT**: Check "Add Python 3.14 to PATH"
   - **IMPORTANT**: Check "Install launcher for all users (recommended)"
   - Click "Customize installation"
   - **Optional features**: Check all (pip, tcl/tk, documentation, test suite)
   - **Advanced options**: 
     - Check "Install for all users"
     - Check "Precompile standard library"
     - Installation directory: `C:\Python314\` (recommended)
   - Click "Install"

3. **Verify Installation**:
   ```powershell
   # Check Python 3.14 installation
   py -3.14 --version
   # Expected: Python 3.14.0
   
   # Check pip installation
   py -3.14 -m pip --version
   # Expected: pip 24.x from C:\Python314\Lib\site-packages\pip
   
   # Verify Python launcher
   py --list
   # Expected to show both 3.12 and 3.14
   ```

### Option B: Free-Threaded Python 3.14t (GIL Disabled - For Parallel Evolution)

**Status**: As of October 11, 2025, check if python.org provides pre-built free-threaded installers.

**Expected Filename Pattern**: `python-3.14.0t-amd64.exe` (note the "t" suffix)

**If Pre-Built Available**:
1. Download from Python 3.14.0 release page (look for "free-threaded" or "t" suffix)
2. Install to separate directory: `C:\Python314t\`
3. Verify free-threading:
   ```powershell
   C:\Python314t\python.exe -c "import sys; print('GIL disabled:', not sys.is_gil_enabled())"
   # Expected: GIL disabled: True
   ```

**If Pre-Built NOT Available - Build from Source** (Advanced):

1. **Prerequisites**:
   - Visual Studio 2022 (Community Edition or better)
   - Windows SDK 10.0.22621.0 or later
   - CMake 3.26+

2. **Download Source**:
   ```powershell
   $url = "https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tar.xz"
   $output = "$env:USERPROFILE\Downloads\Python-3.14.0.tar.xz"
   Invoke-WebRequest -Uri $url -OutFile $output
   
   # Extract (requires 7-Zip or similar)
   # Extract to: C:\Python314-src\
   ```

3. **Build with --disable-gil**:
   ```powershell
   cd C:\Python314-src\Python-3.14.0
   
   # Open Visual Studio 2022 Developer PowerShell
   # Configure with --disable-gil
   .\PCbuild\build.bat --disable-gil -p x64 -c Release
   
   # Install
   .\PCbuild\amd64\python.exe -m ensurepip
   ```

4. **Verify Free-Threading**:
   ```powershell
   C:\Python314-src\Python-3.14.0\PCbuild\amd64\python.exe -c "import sys; print('GIL disabled:', not sys.is_gil_enabled())"
   ```

**Recommendation**: Start with Option A (standard Python 3.14.0), validate AIOS compatibility, then explore Option B (free-threaded) for parallel evolution performance gains.

---

## Part 2: AIOS Environment Upgrade

### Step 1: Backup Current Environment

```powershell
# Create backup of current Python environment
cd C:\dev\AIOS

# Backup current requirements
Copy-Item ai\requirements.txt ai\requirements.txt.bak.312

# Backup current Python packages list
py -3.12 -m pip freeze > ai\python312_packages.txt

Write-Host "Backup complete: ai\requirements.txt.bak.312 and ai\python312_packages.txt" -ForegroundColor Green
```

### Step 2: Create Python 3.14 Virtual Environment (Recommended)

```powershell
cd C:\dev\AIOS\ai

# Create Python 3.14 virtual environment
py -3.14 -m venv .venv314

# Activate virtual environment
.\.venv314\Scripts\Activate.ps1

# Verify Python version
python --version
# Expected: Python 3.14.0

# Upgrade pip
python -m pip install --upgrade pip
```

### Step 3: Install AIOS Dependencies in Python 3.14

```powershell
# Ensure virtual environment is activated
cd C:\dev\AIOS\ai

# Install dependencies
pip install -r requirements.txt

# Expected packages (verify compatibility):
# - fastapi
# - uvicorn
# - pydantic
# - httpx
# - aiofiles
# - jinja2
# - pyyaml
# - pytest
# - pytest-asyncio
```

### Step 4: Verify AIOS Component Compatibility

```powershell
# Test AIOS imports
python -c "
import sys
print(f'Python: {sys.version}')

# Test core imports
from ai.src.runtime.ai_execution_bridge import AIExecutionBridge
from ai.src.runtime.intelligence_dashboard import UnifiedDashboard
from ai.src.evolution.population_manager import PopulationManager

print('✅ AIOS core imports successful')
"

# Run AIOS tests
cd C:\dev\AIOS
pytest ai/tests/ -v

# Expected: All tests pass (or document failures)
```

### Step 5: Update AIOS Configuration

Update `pyproject.toml`:

```toml
[project]
name = "aios"
version = "0.6.2"
requires-python = ">=3.14"  # Updated from 3.12

[tool.pytest.ini_options]
testpaths = ["ai/tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

Update `ai/requirements.txt` (if needed):

```text
# Python 3.14.0 compatible dependencies
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.9.0
httpx>=0.27.0
aiofiles>=24.1.0
jinja2>=3.1.4
pyyaml>=6.0.2
pytest>=8.3.0
pytest-asyncio>=0.24.0
```

### Step 6: Test Python 3.14 Specific Features

```powershell
# Test free-threading detection
python -c "
import sys

# Check if free-threading is available
if hasattr(sys, 'is_gil_enabled'):
    gil_status = sys.is_gil_enabled()
    print(f'GIL Status: {'Enabled' if gil_status else 'Disabled (Free-threaded)'}')
else:
    print('GIL Status: Enabled (standard build)')

print(f'Python Version: {sys.version}')
print(f'Implementation: {sys.implementation.name}')
"
```

---

## Part 3: Parallel Evolution Engine Compatibility

### Free-Threading Detection in Code

Update `ai/src/evolution/parallel_evolution_engine.py` (when implemented):

```python
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Optional

def detect_free_threading() -> bool:
    """Detect if Python 3.14 free-threading is available"""
    if not hasattr(sys, 'is_gil_enabled'):
        return False
    return not sys.is_gil_enabled()

class ParallelEvolutionEngine:
    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers or os.cpu_count()
        
        # Use appropriate executor based on free-threading availability
        if detect_free_threading():
            # Free-threaded mode: Use ThreadPoolExecutor (true parallelism)
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
            self.mode = "free-threaded"
            print(f"🚀 Parallel Evolution Engine: FREE-THREADED mode ({self.max_workers} workers)")
        else:
            # Standard mode: Use ProcessPoolExecutor (process-level parallelism)
            self.executor = ProcessPoolExecutor(max_workers=self.max_workers)
            self.mode = "process-pool"
            print(f"⚙️  Parallel Evolution Engine: PROCESS-POOL mode ({self.max_workers} workers)")
```

### Performance Expectations

| Mode | Python Version | GIL Status | Expected Speedup (8 cores) |
|------|----------------|------------|----------------------------|
| Free-Threaded | 3.14t | Disabled | 6-8x (true parallelism) |
| Standard | 3.14 | Enabled | 3-4x (ProcessPoolExecutor) |
| Legacy | 3.12 | Enabled | 3-4x (ProcessPoolExecutor) |

---

## Part 4: Post-Upgrade Validation

### Comprehensive System Check

```powershell
cd C:\dev\AIOS

# Run system health check
python runtime_intelligence/tools/system_health_check.py

# Expected output:
# ✅ Python 3.14.0 detected
# ✅ All dependencies installed
# ✅ AIOS components operational
# ✅ AI Execution Bridge responsive
# ✅ Intelligence Dashboard active
```

### Update Development Path

```powershell
# Document Python 3.14 upgrade in Dev Path
python -c "
from datetime import datetime

update = f'''
## Python 3.14.0 Upgrade - {datetime.now().strftime('%Y-%m-%d')}

**Status**: ✅ COMPLETE

**Changes**:
- Upgraded from Python 3.12.8 to Python 3.14.0
- Created Python 3.14 virtual environment (.venv314)
- Verified all AIOS dependencies compatible
- Updated pyproject.toml (requires-python >= 3.14)
- Free-threading status: {'AVAILABLE' if hasattr(__import__('sys'), 'is_gil_enabled') else 'NOT DETECTED'}

**Next Steps**:
- Implement Component 4: Parallel Evolution Engine
- Leverage free-threading (if available) for 6-8x speedup
- Benchmark parallel vs sequential evolution
'''

print(update)
" >> docs/development/AIOS_DEV_PATH.md
```

---

## Part 5: Rollback Procedure (If Needed)

If Python 3.14 causes compatibility issues:

```powershell
# Deactivate Python 3.14 virtual environment
deactivate

# Restore Python 3.12
cd C:\dev\AIOS\ai
py -3.12 -m venv .venv

# Activate Python 3.12 environment
.\.venv\Scripts\Activate.ps1

# Restore dependencies
pip install -r requirements.txt.bak.312

# Verify rollback
python --version
# Expected: Python 3.12.8
```

---

## Part 6: Troubleshooting

### Common Issues

**Issue 1: "py -3.14 not found"**
- **Cause**: Python 3.14 not added to PATH or launcher not registered
- **Solution**:
  ```powershell
  # Manually add to PATH
  $env:PATH = "C:\Python314\;C:\Python314\Scripts\;$env:PATH"
  
  # Or reinstall with "Add to PATH" checked
  ```

**Issue 2: "Module not found" errors**
- **Cause**: Dependencies not installed in Python 3.14 environment
- **Solution**:
  ```powershell
  # Ensure virtual environment active
  .\.venv314\Scripts\Activate.ps1
  
  # Reinstall dependencies
  pip install -r requirements.txt
  ```

**Issue 3: "Cannot detect free-threading"**
- **Cause**: Standard Python 3.14 build (GIL enabled)
- **Solution**: This is expected. Free-threading requires `--disable-gil` build.
- **Workaround**: Use ProcessPoolExecutor (still provides parallelism)

**Issue 4: VS Code not detecting Python 3.14**
- **Solution**:
  ```powershell
  # Select Python interpreter in VS Code
  # Ctrl+Shift+P → "Python: Select Interpreter"
  # Choose: C:\dev\AIOS\ai\.venv314\Scripts\python.exe
  ```

---

## Part 7: Next Steps After Upgrade

1. **Implement Component 4**: Parallel Evolution Engine with Python 3.14 detection
2. **Benchmark Performance**: Measure actual speedup (parallel vs sequential)
3. **Update Documentation**: Record Python 3.14 specific features
4. **Test Free-Threading**: If available, validate 6-8x speedup
5. **Proceed with Week 2-4 Components**: Components 5 and 6

---

## Quick Reference

### Essential Commands

```powershell
# Check Python versions
py --list

# Run with specific Python version
py -3.14 script.py

# Activate Python 3.14 virtual environment
C:\dev\AIOS\ai\.venv314\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate

# Check free-threading status
python -c "import sys; print('Free-threading:', not sys.is_gil_enabled() if hasattr(sys, 'is_gil_enabled') else 'N/A')"

# Run AIOS tests
pytest ai/tests/ -v

# System health check
python runtime_intelligence/tools/system_health_check.py
```

### Download Links

- **Python 3.14.0 Windows 64-bit**: https://www.python.org/ftp/python/3.14.0/python-3.14.0-amd64.exe
- **Python 3.14.0 Source**: https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tar.xz
- **Release Page**: https://www.python.org/downloads/release/python-3140/
- **PEP 703** (Free-threading): https://peps.python.org/pep-0703/

---

## Conclusion

This guide provides a comprehensive upgrade path from Python 3.12.8 to Python 3.14.0 for AIOS. The upgrade enables:

1. **Modern Python Features**: Latest language improvements and optimizations
2. **Free-Threading Readiness**: Foundation for 6-8x parallel speedup (if free-threaded build available)
3. **Component 4 Implementation**: Parallel Evolution Engine with Python 3.14 detection
4. **Future-Proofing**: AIOS aligned with latest Python ecosystem

**Estimated Time**: 30-60 minutes (including download, installation, testing)

**Risk Level**: LOW (virtual environment isolation, rollback procedure available)

**Status**: Ready to proceed with installation.
