# 🐍 COMPLETE PYTHON SYSTEM CLEANUP & REINSTALL GUIDE

## ⚠️ **CRITICAL: COMPLETE PYTHON ENVIRONMENT RESET**

The current Python environment has deep integration conflicts with VS Code, Conda, and multiple Python installations. We need a complete system-wide cleanup.

## 📋 **STEP 1: IDENTIFY ALL PYTHON INSTALLATIONS**

### Current Python Installations Detected:
- `C:\Python313\` (System Python 3.13)
- VS Code integrated environments
- Conda environments (if any)
- Pip user installations

## 🗑️ **STEP 2: COMPLETE UNINSTALL SEQUENCE**

### A) Close All Development Tools
```powershell
# Close VS Code completely
taskkill /f /im "Code.exe"

# Close any Python processes
taskkill /f /im "python.exe"
taskkill /f /im "pythonw.exe"
```

### B) Uninstall Python via Windows Settings
1. **Windows Settings** → **Apps** → **Apps & features**
2. Search for "Python" and uninstall:
   - Python 3.13.x (64-bit)
   - Python 3.13.x (32-bit) if exists
   - Python Launcher for Windows
   - Any Anaconda/Miniconda installations

### C) Remove Python Directories
```powershell
# Remove Python installation directories
Remove-Item -Recurse -Force "C:\Python*" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "C:\Users\$env:USERNAME\AppData\Local\Programs\Python*" -ErrorAction SilentlyContinue

# Remove Conda/Anaconda
Remove-Item -Recurse -Force "C:\Users\$env:USERNAME\Anaconda3" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "C:\Users\$env:USERNAME\Miniconda3" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "C:\Users\$env:USERNAME\.conda" -ErrorAction SilentlyContinue

# Remove pip cache and user installations
Remove-Item -Recurse -Force "C:\Users\$env:USERNAME\AppData\Local\pip" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "C:\Users\$env:USERNAME\AppData\Roaming\Python" -ErrorAction SilentlyContinue
```

### D) Clean Environment Variables
```powershell
# Clean PATH environment variable
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
$cleanPath = ($currentPath -split ';' | Where-Object { 
    $_ -notlike "*Python*" -and 
    $_ -notlike "*Anaconda*" -and 
    $_ -notlike "*Miniconda*" 
}) -join ';'
[Environment]::SetEnvironmentVariable("PATH", $cleanPath, "Machine")

# Remove Python-specific environment variables
[Environment]::SetEnvironmentVariable("PYTHONPATH", $null, "Machine")
[Environment]::SetEnvironmentVariable("PYTHONHOME", $null, "Machine")
```

## 🔧 **STEP 3: FRESH PYTHON INSTALLATION**

### A) Download Official Python
1. Go to https://www.python.org/downloads/
2. Download **Python 3.12.x** (stable LTS version)
3. **IMPORTANT:** Choose "Windows installer (64-bit)"

### B) Installation Settings
**CRITICAL INSTALLATION OPTIONS:**
- ✅ **Add Python to PATH**
- ✅ **Install for all users**
- ✅ **Add Python to environment variables**
- ✅ **Install pip**
- ❌ **DO NOT install py launcher for all users** (causes conflicts)

**Custom Installation Path:** `C:\Python312\`

### C) Verify Installation
```powershell
# Restart PowerShell/Command Prompt
python --version
pip --version
where python
```

## 🏗️ **STEP 4: CLEAN VIRTUAL ENVIRONMENT SETUP**

### A) Create Project Virtual Environment
```powershell
cd "C:\dev\AIOS"

# Create clean virtual environment
python -m venv aios_env --clear

# Activate environment
.\aios_env\Scripts\Activate.ps1

# Upgrade core tools
python -m pip install --upgrade pip setuptools wheel
```

### B) Install AIOS Dependencies
```powershell
# Install essential packages
pip install numpy pandas matplotlib seaborn
pip install openai aiohttp asyncio
pip install rich colorama
pip install pytest pytest-asyncio
pip install black flake8 mypy
pip install jupyter notebook
```

## 🔧 **STEP 5: VS CODE CONFIGURATION**

### A) Reset VS Code Python Extension
1. **Extensions** → **Python** → **Uninstall**
2. **Restart VS Code**
3. **Extensions** → **Search "Python"** → **Install Microsoft Python Extension**

### B) Configure Python Interpreter
1. **Ctrl+Shift+P** → **Python: Select Interpreter**
2. Choose: `C:\dev\AIOS\aios_env\Scripts\python.exe`

### C) Workspace Settings
```json
{
    "python.defaultInterpreterPath": "./aios_env/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.analysis.typeCheckingMode": "strict"
}
```

## ✅ **STEP 6: VERIFICATION TESTS**

### A) Test Python Environment
```python
# test_environment.py
import sys
import numpy as np
import pandas as pd
import openai

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
print("✅ All imports successful!")
```

### B) Test VS Code Integration
1. Open any `.py` file
2. Check IntelliSense works
3. Check linting works
4. Run Python file with F5

## 🎯 **EXPECTED RESULTS**

After complete cleanup and reinstall:
- ✅ Single Python installation in `C:\Python312\`
- ✅ Clean virtual environment in `C:\dev\AIOS\aios_env\`
- ✅ VS Code Python IntelliSense working
- ✅ No conflicting Python paths
- ✅ No `.conda` folders
- ✅ Clean PATH environment variable

## 🚨 **CRITICAL NOTES**

1. **Backup Important Data:** Before starting, backup any important Python scripts or environments
2. **Administrator Rights:** Some cleanup steps require administrator privileges
3. **Restart Required:** Restart computer after environment variable changes
4. **VS Code Reset:** Complete VS Code settings reset may be needed

## 📞 **TROUBLESHOOTING**

If issues persist after cleanup:
1. Use **Windows PowerShell (Admin)** for all commands
2. Manually edit PATH in System Properties
3. Use `where python` to verify no old installations remain
4. Clear VS Code workspace cache: Delete `.vscode` folder and recreate

---

**Next Step:** Execute this cleanup manually, then return for C++/Git configuration.
