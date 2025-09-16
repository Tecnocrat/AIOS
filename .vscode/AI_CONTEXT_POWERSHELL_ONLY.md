# 🚨 CRITICAL AI ENGINE CONTEXT 🚨
## AIOS WORKSPACE - POWERSHELL ONLY

**IMPORTANT**: This is a Windows PowerShell environment.  
**NEVER use Linux bash commands** (rm, ls, grep, etc.)

### ✅ Correct PowerShell Commands:
- `Remove-Item` (not rm)
- `Get-ChildItem` (not ls) 
- `Select-String` (not grep)
- `New-Item` (not touch)
- `Copy-Item` (not cp)
- `Move-Item` (not mv)
- `Set-Location` (not cd - though cd works)
- `Write-Host` (not echo - though echo works)

### ❌ Forbidden Linux Commands:
- `rm` → Use `Remove-Item`
- `ls` → Use `Get-ChildItem`
- `grep` → Use `Select-String`
- `touch` → Use `New-Item`
- `cp` → Use `Copy-Item`
- `mv` → Use `Move-Item`
- `cat` → Use `Get-Content`
- `find` → Use `Get-ChildItem -Recurse`

### 🖥️ Environment Details:
- **OS**: Windows
- **Shell**: PowerShell (pwsh.exe)
- **Workspace**: AIOS Development Environment
- **Context**: Professional software development
- **AI Engines**: GitHub Copilot, Claude, ChatGPT, etc.

### 🤖 AI Engine Instructions:
1. **Always use PowerShell syntax** for terminal commands
2. **Check this file** if unsure about command syntax
3. **Test commands** in PowerShell environment before suggesting
4. **Remember**: We are on Windows, not Linux
5. **When in doubt**: Use PowerShell equivalents

### 🎯 Common Patterns:
```powershell
# File operations
Get-ChildItem                    # List files
Remove-Item -Recurse -Force      # Delete recursively
New-Item -ItemType Directory     # Create directory
Copy-Item -Recurse              # Copy recursively

# Text processing
Select-String "pattern" file.txt # Search in file
Get-Content file.txt            # Read file content
Set-Content file.txt "content"   # Write file content

# Navigation
Set-Location path               # Change directory
Get-Location                    # Show current directory
```

**🔄 This context is persistent and should be referenced by all AI engines working in AIOS!**