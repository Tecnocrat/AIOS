# 🧹 Windows Registry Python Cleanup Guide

## 🚨 **Problem Resolved: Failed Python Uninstaller**

**Issue:** Python 3.13.2 uninstaller failed to complete, leaving registry entries that made Windows detect phantom Python installations.

**Solution:** Manual registry cleanup using PowerShell with admin privileges.

## 🛠️ **Registry Cleanup Commands Used**

### 1. **Remove Uninstall Registry Entries**
```powershell
# System-wide uninstall entries
$pythonEntries = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" | Where-Object { $_.DisplayName -like "*Python*" -or $_.DisplayName -like "*Miniconda*" }
foreach ($entry in $pythonEntries) {
    Write-Host "Removing: $($entry.DisplayName)"
    Remove-Item -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$($entry.PSChildName)" -Force -ErrorAction SilentlyContinue
}

# User-specific uninstall entries
$userPythonEntries = Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" | Where-Object { $_.DisplayName -like "*Python*" -or $_.DisplayName -like "*Miniconda*" }
foreach ($entry in $userPythonEntries) {
    Write-Host "Removing user entry: $($entry.DisplayName)"
    Remove-Item -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$($entry.PSChildName)" -Force -ErrorAction SilentlyContinue
}
```

### 2. **Remove Python-Specific Registry Keys**
```powershell
# Remove Python configuration keys
Remove-Item -Path "HKLM:\SOFTWARE\Python" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "HKCU:\SOFTWARE\Python" -Recurse -Force -ErrorAction SilentlyContinue
```

### 3. **Clean PATH Variables**
```powershell
# Clean user PATH of all Python/Conda/debugpy entries
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$cleanPath = ($currentPath -split ';' | Where-Object { 
    $_ -notlike "*python*" -and 
    $_ -notlike "*conda*" -and 
    $_ -notlike "*debugpy*" 
}) -join ';'
[Environment]::SetEnvironmentVariable("PATH", $cleanPath, "User")
```

## ✅ **Verification Commands**

### Check Registry Cleanup Success:
```powershell
# Verify no Python entries remain
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" | Where-Object { $_.DisplayName -like "*Python*" -or $_.DisplayName -like "*Miniconda*" }
Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" | Where-Object { $_.DisplayName -like "*Python*" -or $_.DisplayName -like "*Miniconda*" }

# Check PATH is clean
$env:PATH -split ';' | Where-Object { $_ -like "*python*" -or $_ -like "*conda*" }
```

## 🎯 **Result**

**Before Cleanup:**
- Windows detected: `Miniconda3 py313_25.3.1-1 (Python 3.13.2 64-bit)` and `Python 3.13.2 (64-bit)`
- Registry contained 10+ Python-related uninstall entries
- PATH contained debugpy and other Python references

**After Cleanup:**
- ✅ No Python applications detected by Windows
- ✅ All registry entries removed
- ✅ PATH completely clean
- ✅ System ready for fresh Python 3.12 installation

## 📋 **When to Use This Guide**

Use these commands when:
- Python uninstaller fails to complete
- Windows still detects Python after removal
- Fresh installation is blocked by existing registry entries
- Need complete system-wide Python cleanup

**⚠️ Requires Administrator Privileges**
