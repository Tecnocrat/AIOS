# AIOS Cellular Mitosis - Termux Daughter Cell Synchronization Script
# Purpose: Sync Termux AIOS cell with latest Windows development code
# Usage: .\scripts\sync_termux_cell.ps1 -TermuxHost 192.168.1.131

param(
    [string]$TermuxHost = "192.168.1.131",
    [int]$TermuxPort = 8022,
    [string]$TermuxUser = "",  # Auto-detect if empty
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$RestartServices = $true
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🔄 AIOS CELLULAR MITOSIS - TERMUX SYNC" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify GitHub is up-to-date
Write-Host "📡 Verifying Windows AIOS is pushed to GitHub..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "❌ ERROR: You have uncommitted changes in Windows AIOS" -ForegroundColor Red
    Write-Host ""
    git status --short
    Write-Host ""
    Write-Host "Please commit and push changes first:" -ForegroundColor Yellow
    Write-Host "  git add ." -ForegroundColor Gray
    Write-Host "  git commit -m '...'" -ForegroundColor Gray
    Write-Host "  git push origin OS" -ForegroundColor Gray
    exit 1
}

# Check if local is ahead of remote
$localCommit = git rev-parse HEAD
$remoteCommit = git rev-parse origin/OS
if ($localCommit -ne $remoteCommit) {
    Write-Host "❌ ERROR: Local branch is ahead of origin/OS" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please push your changes first:" -ForegroundColor Yellow
    Write-Host "  git push origin OS" -ForegroundColor Gray
    exit 1
}

Write-Host "✅ Windows AIOS is synced with GitHub" -ForegroundColor Green
Write-Host ""

# Step 2: Auto-detect Termux username if not provided
if ($TermuxUser -eq "") {
    Write-Host "🔍 Auto-detecting Termux username..." -ForegroundColor Yellow
    
    # Try to SSH and get username
    try {
        $TermuxUser = ssh -o "StrictHostKeyChecking=no" -o "ConnectTimeout=5" -p $TermuxPort "${TermuxHost}" "whoami" 2>$null
        if ($LASTEXITCODE -eq 0 -and $TermuxUser) {
            Write-Host "✅ Detected Termux user: $TermuxUser" -ForegroundColor Green
        } else {
            Write-Host "❌ ERROR: Could not detect Termux username" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please provide username manually:" -ForegroundColor Yellow
            Write-Host "  .\scripts\sync_termux_cell.ps1 -TermuxUser u0_a123" -ForegroundColor Gray
            exit 1
        }
    } catch {
        Write-Host "❌ ERROR: Cannot connect to Termux at ${TermuxHost}:${TermuxPort}" -ForegroundColor Red
        Write-Host "Make sure SSH server is running on Termux" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "🎯 Target: ${TermuxUser}@${TermuxHost}:${TermuxPort}" -ForegroundColor Cyan
Write-Host ""

# Step 3: Check Termux AIOS status
Write-Host "🔍 Checking Termux AIOS status..." -ForegroundColor Yellow

$termuxStatus = ssh -p $TermuxPort "${TermuxUser}@${TermuxHost}" @"
cd ~/AIOS 2>/dev/null || { echo 'ERROR:NO_AIOS'; exit 1; }
git status --porcelain
echo '---'
git log --oneline -1
echo '---'
git rev-parse HEAD
echo '---'
tmux ls 2>/dev/null || echo 'NO_TMUX'
"@

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: AIOS directory not found on Termux" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please clone AIOS repository on Termux first:" -ForegroundColor Yellow
    Write-Host "  cd ~ && git clone https://github.com/Tecnocrat/AIOS.git" -ForegroundColor Gray
    exit 1
}

# Parse status
$statusLines = $termuxStatus -split "`n"
$termuxChanges = $statusLines[0..($statusLines.IndexOf('---') - 1)] | Where-Object { $_ -ne "" }
$termuxLastCommit = $statusLines[($statusLines.IndexOf('---') + 1)]
$termuxCommitHash = $statusLines[($statusLines.IndexOf('---', $statusLines.IndexOf('---') + 1) + 1)]
$termuxTmux = $statusLines[($statusLines.IndexOf('---', $statusLines.IndexOf('---', $statusLines.IndexOf('---') + 1) + 1) + 1)..$statusLines.Length] -join "`n"

Write-Host "Current Termux commit: $termuxLastCommit" -ForegroundColor Gray

if ($termuxChanges.Count -gt 0) {
    Write-Host "⚠️ WARNING: Termux has uncommitted changes:" -ForegroundColor Yellow
    $termuxChanges | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    
    if (-not $Force) {
        Write-Host ""
        Write-Host "These changes will be lost during sync!" -ForegroundColor Red
        Write-Host "Use -Force flag to proceed anyway" -ForegroundColor Yellow
        exit 1
    } else {
        Write-Host "⚠️ -Force flag set, proceeding with sync (changes will be lost)" -ForegroundColor Yellow
    }
}

if ($termuxCommitHash -eq $localCommit) {
    Write-Host "✅ Termux is already up-to-date with Windows AIOS" -ForegroundColor Green
    Write-Host ""
    
    if ($RestartServices) {
        Write-Host "🔄 Restarting services anyway..." -ForegroundColor Yellow
    } else {
        Write-Host "No sync needed" -ForegroundColor Green
        exit 0
    }
} else {
    Write-Host "🔄 Termux is behind, syncing..." -ForegroundColor Yellow
}

Write-Host ""

# Step 4: Perform sync (or dry-run)
if ($DryRun) {
    Write-Host "🧪 DRY RUN MODE - No changes will be made" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Would execute on Termux:" -ForegroundColor Yellow
    Write-Host "  cd ~/AIOS" -ForegroundColor Gray
    Write-Host "  git fetch origin OS" -ForegroundColor Gray
    Write-Host "  git reset --hard origin/OS" -ForegroundColor Gray
    if ($RestartServices) {
        Write-Host "  tmux kill-session -t aios-bridge -t aios-soul" -ForegroundColor Gray
        Write-Host "  bash ~/.termux/boot/start-aios-trinity.sh" -ForegroundColor Gray
    }
    Write-Host ""
    exit 0
}

Write-Host "🚀 Executing sync on Termux..." -ForegroundColor Green
Write-Host ""

# Build sync commands
$syncCommands = @"
cd ~/AIOS && \
echo '[SYNC] Fetching latest from GitHub...' && \
git fetch origin OS && \
echo '[SYNC] Resetting to origin/OS...' && \
git reset --hard origin/OS && \
echo '[SYNC] Current commit:' && \
git log --oneline -1
"@

if ($RestartServices) {
    $syncCommands += " && echo '[SYNC] Restarting services...' && \"
    $syncCommands += "tmux kill-session -t aios-bridge -t aios-soul 2>/dev/null; \"
    $syncCommands += "sleep 2 && \"
    $syncCommands += "bash ~/.termux/boot/start-aios-trinity.sh && \"
    $syncCommands += "sleep 5 && \"
    $syncCommands += "echo '[SYNC] Verifying services...' && \"
    $syncCommands += "tmux ls"
}

# Execute sync
$syncOutput = ssh -p $TermuxPort "${TermuxUser}@${TermuxHost}" $syncCommands 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Sync completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Sync output:" -ForegroundColor Gray
    Write-Host "─" * 70 -ForegroundColor DarkGray
    $syncOutput | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    Write-Host "─" * 70 -ForegroundColor DarkGray
    Write-Host ""
    
    # Step 5: Verify health
    Write-Host "🏥 Verifying Termux AIOS health..." -ForegroundColor Yellow
    
    Start-Sleep -Seconds 3  # Wait for services to stabilize
    
    try {
        $health = Invoke-RestMethod "http://${TermuxHost}:8000/health" -TimeoutSec 5
        Write-Host "✅ Bridge server operational" -ForegroundColor Green
        Write-Host "   Consciousness: $($health.consciousness_level)" -ForegroundColor Gray
        Write-Host "   Soul Running: $($health.soul_running)" -ForegroundColor Gray
    } catch {
        Write-Host "⚠️ WARNING: Could not verify bridge health" -ForegroundColor Yellow
        Write-Host "   Bridge may still be starting up..." -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host "✅ CELLULAR MITOSIS SYNC COMPLETE" -ForegroundColor Green
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host ""
    
} else {
    Write-Host "❌ ERROR: Sync failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error output:" -ForegroundColor Red
    Write-Host "─" * 70 -ForegroundColor DarkGray
    $syncOutput | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
    Write-Host "─" * 70 -ForegroundColor DarkGray
    Write-Host ""
    exit 1
}

# Optional: Show usage tip
Write-Host "💡 Tip: Add this to your development workflow:" -ForegroundColor Cyan
Write-Host "   git push origin OS && .\scripts\sync_termux_cell.ps1" -ForegroundColor Gray
Write-Host ""
