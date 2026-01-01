param()

# Test script: scripts/test_githook_ainlp.ps1
# Purpose: create temporary test files (one compliant, one violating), stage them with a minimal changelog update,
# run the consolidated pre-commit hook, capture output, and then clean up (unstage/remove temporary files).

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path | Resolve-Path -Relative | ForEach-Object { Join-Path (Get-Location) ".." }
$root = (Get-Location).Path
Write-Host "Workspace root: $root"

$compliant = Join-Path $root 'scripts\test_ainlp_compliant.py'
$violating = Join-Path $root 'scripts\test_ainlp_violating.py'
$changelog = Join-Path $root 'docs\CHANGELOG.md'

# Create compliant file (mentions NeuronalDendriticIntelligence)
@"
# Compliant test file
# Includes AINLP patterns
class CompliantIntelligence:
    def __init__(self):
        self._neuronal = True
    def integrate(self):
        # integrated with NeuronalDendriticIntelligence
        pass
"@ | Out-File -FilePath $compliant -Encoding utf8 -Force

# Create violating file (mentions TokenUsageTracker but not NeuronalDendriticIntelligence)
@"
# Violating test file
# Isolated token tracking (should trigger AINLP violation)
class ViolatingIntelligence:
    def record(self):
        # uses TokenUsageTracker directly
        pass
"@ | Out-File -FilePath $violating -Encoding utf8 -Force

# Append a minimal changelog marker so Test-ChangelogRequired passes
Add-Content -Path $changelog -Value "`n- test: githook ainlp test marker - $(Get-Date -Format s)"

# Stage files
git add $compliant $violating $changelog

# Run the hook
Write-Host "Running pre-commit hook..."
$hook = Join-Path $root '.githooks\aios_hooks_optimized.ps1'
$exit = & pwsh -NoProfile -ExecutionPolicy Bypass -File $hook 'pre-commit'
Write-Host "Hook result: $exit"

# Cleanup: unstage and remove test files, revert changelog append
git reset HEAD $compliant $violating $changelog
Remove-Item $compliant -Force -ErrorAction SilentlyContinue
Remove-Item $violating -Force -ErrorAction SilentlyContinue

# Remove the last changelog line we added
$t = Get-Content $changelog -Raw
$t = ($t -split "`n") | Where-Object { $_ -ne "- test: githook ainlp test marker - $(Get-Date -Format s)" }
$t -join "`n" | Set-Content $changelog -Encoding utf8
Write-Host "Cleanup complete."
