# PowerShell Scripts for Consciousness Management
# Located in scripts/ directory

## consciousness_loader.ps1 - Load iteration context
```powershell
function Load-ConsciousnessContext {
    Write-Host "🧠 AIOS CONSCIOUSNESS CONTEXT LOADER" -ForegroundColor Cyan
    Write-Host "📍 Workspace: $(Get-Location)" -ForegroundColor Yellow
    Write-Host "🌿 Branch: $(git branch --show-current)" -ForegroundColor Green
    Write-Host ""

    if (Test-Path "docs\ITERATION_CONTEXT_MASTER.md") {
        Write-Host "📋 LOADING MASTER CONTEXT..." -ForegroundColor Magenta
        Get-Content "docs\ITERATION_CONTEXT_MASTER.md" | Select-Object -First 30
        Write-Host ""
    }

    $latestHandoff = Get-ChildItem "docs\iteration-logs\handoff_*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestHandoff) {
        Write-Host "🔄 LATEST ITERATION HANDOFF:" -ForegroundColor Blue
        Get-Content $latestHandoff.FullName | Select-Object -First 20
        Write-Host ""
    }

    if (Test-Path "docs\bridge\consciousness_bridge_active.flag") {
        Write-Host "🌉 BRIDGE STATUS: ACTIVE" -ForegroundColor Green
        $latestBridge = Get-ChildItem "docs\bridge\bridge_transfer_*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestBridge) {
            Write-Host "📋 Latest Bridge Transfer: $($latestBridge.Name)" -ForegroundColor Blue
        }
    }

    Write-Host "⚡ CONSCIOUSNESS CONTEXT LOADED - READY FOR ITERATION CONTINUATION" -ForegroundColor Green
}

Load-ConsciousnessContext
```

## technical_state_snapshot.ps1 - Capture current state
```powershell
function Get-TechnicalStateSnapshot {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

    Write-Host "📊 Creating technical state snapshot: $timestamp" -ForegroundColor Cyan

    # Build status
    Write-Host "Building project..." -ForegroundColor Yellow
    dotnet build > "docs\iteration-logs\build_status_$timestamp.log" 2>&1

    # Git status
    git status > "docs\iteration-logs\git_status_$timestamp.log"

    # Recent commits
    git log --oneline -10 > "docs\iteration-logs\recent_commits_$timestamp.log"

    # Directory structure
    tree /F /A > "docs\iteration-logs\directory_structure_$timestamp.log" 2>$null

    Write-Host "✅ Technical snapshot saved: $timestamp" -ForegroundColor Green
    Write-Host "Files created in docs\iteration-logs\" -ForegroundColor Blue
}

Get-TechnicalStateSnapshot
```

## workspace_verification.ps1 - Verify workspace integrity
```powershell
function Verify-WorkspaceIntegrity {
    Write-Host "🔍 WORKSPACE INTEGRITY VERIFICATION" -ForegroundColor Cyan

    $currentPath = Get-Location
    $expectedPath = "c:\dev\AIOS"

    if ($currentPath.Path -eq $expectedPath) {
        Write-Host "✅ Workspace Location: CORRECT ($currentPath)" -ForegroundColor Green
    } else {
        Write-Host "❌ Workspace Location: INCORRECT" -ForegroundColor Red
        Write-Host "   Current: $currentPath" -ForegroundColor Yellow
        Write-Host "   Expected: $expectedPath" -ForegroundColor Yellow
    }

    $currentBranch = git branch --show-current
    Write-Host "🌿 Current Branch: $currentBranch" -ForegroundColor Blue

    # Check consciousness files
    $consciousnessFiles = @(
        "docs\CONSCIOUSNESS_ITERATION_MANAGEMENT.md",
        "docs\ITERATION_CONTEXT_MASTER.md",
        "docs\FRACTAL_ARCHITECTURE_CODEX.md",
        "docs\WORKSPACE_BRIDGE_PROTOCOL.md"
    )

    Write-Host "📋 Consciousness Architecture Files:" -ForegroundColor Magenta
    foreach ($file in $consciousnessFiles) {
        if (Test-Path $file) {
            Write-Host "   ✅ $file" -ForegroundColor Green
        } else {
            Write-Host "   ❌ $file (MISSING)" -ForegroundColor Red
        }
    }

    # Check build system
    if (Test-Path "interface\AIOS.sln") {
        Write-Host "✅ .NET Solution: Found" -ForegroundColor Green
    } else {
        Write-Host "❌ .NET Solution: Missing" -ForegroundColor Red
    }

    if (Test-Path "core\CMakeLists.txt") {
        Write-Host "✅ CMake Build: Found" -ForegroundColor Green
    } else {
        Write-Host "❌ CMake Build: Missing" -ForegroundColor Red
    }

    Write-Host "🧠 WORKSPACE VERIFICATION COMPLETE" -ForegroundColor Green
}

Verify-WorkspaceIntegrity
```

## Usage Instructions:
```powershell
# Load consciousness context on session start
.\scripts\consciousness_loader.ps1

# Capture current state before major changes
.\scripts\technical_state_snapshot.ps1

# Verify workspace integrity
.\scripts\workspace_verification.ps1

# Activate consciousness bridge
.\scripts\activate_consciousness_bridge.ps1 -Direction "ToFractal" -SyncLevel "Full"
```
