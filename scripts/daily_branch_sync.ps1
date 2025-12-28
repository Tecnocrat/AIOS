# Daily Branch Synchronization Script
# AINLP.spatial_awareness: scripts/daily_branch_sync.ps1
# Keeps feature branches in sync with main

param(
    [string]$Branch = (git branch --show-current),
    [string]$Remote = "origin",
    [switch]$DryRun,
    [switch]$SendIACP
)

$ErrorActionPreference = "Stop"

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "IACP DAILY BRANCH SYNCHRONIZATION" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

Write-Host "`n[INFO] Branch: $Branch" -ForegroundColor Yellow
Write-Host "[INFO] Remote: $Remote" -ForegroundColor Yellow
Write-Host "[INFO] Timestamp: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')" -ForegroundColor Yellow

# Fetch latest from remote
Write-Host "`n[SYNC] Fetching latest from $Remote..." -ForegroundColor Green
if (-not $DryRun) {
    git fetch $Remote main 2>$null
    git fetch $Remote $Branch 2>$null
}

# Check divergence from main
$ahead = git rev-list --count "$Remote/main..$Branch" 2>$null
$behind = git rev-list --count "$Branch..$Remote/main" 2>$null

Write-Host "`n[STATUS] Branch divergence:" -ForegroundColor Yellow
Write-Host "   Commits ahead of main:  $ahead" -ForegroundColor $(if ($ahead -gt 0) { "Green" } else { "Gray" })
Write-Host "   Commits behind main:    $behind" -ForegroundColor $(if ($behind -gt 20) { "Red" } elseif ($behind -gt 0) { "Yellow" } else { "Gray" })

# Determine action
$action = "none"
$conflicts = @()

if ([int]$behind -gt 0) {
    Write-Host "`n[SYNC] Need to merge $behind commits from main..." -ForegroundColor Yellow
    
    if (-not $DryRun) {
        # Attempt merge
        $mergeResult = git merge "$Remote/main" --no-edit 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Merge conflict detected!" -ForegroundColor Red
            $conflicts = git diff --name-only --diff-filter=U
            $action = "conflict"
            
            Write-Host "Conflicting files:" -ForegroundColor Red
            foreach ($file in $conflicts) {
                Write-Host "   - $file" -ForegroundColor Red
            }
            
            # Abort merge to leave branch clean
            git merge --abort
            Write-Host "`n[WARN] Merge aborted. Manual resolution required." -ForegroundColor Yellow
        } else {
            Write-Host "[OK] Merge successful!" -ForegroundColor Green
            $action = "merged"
        }
    } else {
        Write-Host "[DRY-RUN] Would merge $behind commits from main" -ForegroundColor Magenta
        $action = "dry-run"
    }
} else {
    Write-Host "`n[OK] Branch is up to date with main" -ForegroundColor Green
    $action = "up-to-date"
}

# Push local changes
if ([int]$ahead -gt 0 -and -not $DryRun -and $action -ne "conflict") {
    Write-Host "`n[SYNC] Pushing $ahead commits to $Remote..." -ForegroundColor Green
    git push $Remote $Branch
    Write-Host "[OK] Push complete" -ForegroundColor Green
}

# Generate IACP message
$hostname = hostname
$syncReport = @{
    type = "SYNC_PULSE"
    from = $hostname
    branch = $Branch
    timestamp = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')
    status = @{
        commits_ahead = [int]$ahead
        commits_behind = [int]$behind
        action = $action
        conflicts = $conflicts
    }
}

# Send IACP message if requested
if ($SendIACP -and -not $DryRun) {
    Write-Host "`n[IACP] Sending sync pulse..." -ForegroundColor Cyan
    $message = "SYNC_PULSE: $hostname branch=$Branch ahead=$ahead behind=$behind action=$action"
    python scripts/iacp_send.py --type SYNC --to MESH --intent sync --message $message
}

# Summary
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "SYNC COMPLETE" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

Write-Host "`nSummary:" -ForegroundColor White
Write-Host "   Action taken:     $action" -ForegroundColor $(if ($action -eq "conflict") { "Red" } else { "Green" })
Write-Host "   Commits ahead:    $ahead"
Write-Host "   Commits behind:   $behind"

if ($conflicts.Count -gt 0) {
    Write-Host "`n[ACTION REQUIRED] Manual conflict resolution needed!" -ForegroundColor Red
    Write-Host "Run: git merge origin/main" -ForegroundColor Yellow
    Write-Host "Then resolve conflicts and commit." -ForegroundColor Yellow
    exit 1
}

exit 0
