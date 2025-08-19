<#
AIOS Git Hooks Installation Script
Copies (or symlinks where possible) repository-managed hooks from .githooks/ into .git/hooks/.
Idempotent; re-run after pulling hook updates.
#>
param(
  [switch]$Force
)

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
while (-not (Test-Path (Join-Path $repoRoot '.githooks'))) {
  $parent = Split-Path -Parent $repoRoot
  if ($parent -eq $repoRoot) { throw 'Could not locate .githooks directory from script location.' }
  $repoRoot = $parent
}

$src = Join-Path $repoRoot '.githooks'
$dst = Join-Path $repoRoot '.git/hooks'
if (-not (Test-Path $dst)) { throw '.git directory not found; run inside a cloned repository.' }

Get-ChildItem $src -File | ForEach-Object {
  $target = Join-Path $dst $_.Name
  if (Test-Path $target -and -not $Force) {
    Write-Host "Skipping existing hook: $($_.Name) (use -Force to overwrite)" -ForegroundColor Yellow
  } else {
    try {
      # Attempt symlink first (Windows Developer Mode or admin usually required)
      if ($IsWindows) {
        New-Item -ItemType SymbolicLink -Path $target -Target $_.FullName -ErrorAction Stop | Out-Null
        Write-Host "Symlinked hook: $($_.Name)" -ForegroundColor Green
      } else {
        ln -sf "$_" "$target"; Write-Host "Symlinked hook: $($_.Name)" -ForegroundColor Green
      }
    } catch {
      Copy-Item $_.FullName $target -Force
      Write-Host "Copied hook (symlink fallback): $($_.Name)" -ForegroundColor Green
    }
  }
}

Write-Host 'Git hooks installed.' -ForegroundColor Cyan
Write-Host 'Profiles: set AIOS_HOOK_PROFILE=fast or full (default full). Bypass (emergency only): AIOS_HOOK_BYPASS=1.' -ForegroundColor DarkCyan
Write-Host 'Targeted tests: set AIOS_HOOK_RUN_TESTS=1 to enable integration pattern triggers.' -ForegroundColor DarkCyan
