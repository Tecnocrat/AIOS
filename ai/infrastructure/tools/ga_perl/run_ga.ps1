param(
    [int]$PopSize = $env:GA_POP_SIZE ? [int]$env:GA_POP_SIZE : 20,
    [int]$GenomeLen = $env:GA_GENOME_LEN ? [int]$env:GA_GENOME_LEN : 16,
    [double]$MutRate = $env:GA_MUT_RATE ? [double]$env:GA_MUT_RATE : 0.05
)

$perl = Get-Command perl -ErrorAction SilentlyContinue
if (-not $perl) {
    Write-Host "Perl is not installed or not on PATH." -ForegroundColor Yellow
    Write-Host "Install Strawberry Perl (recommended):" -ForegroundColor Yellow
    Write-Host "  choco install strawberryperl -y" -ForegroundColor Yellow
    Write-Host "Or download from https://strawberryperl.com/" -ForegroundColor Yellow
    exit 127
}

$script = Join-Path $PSScriptRoot 'ga.pl'
$env:GA_POP_SIZE = $PopSize
$env:GA_GENOME_LEN = $GenomeLen
$env:GA_MUT_RATE = $MutRate

& $perl.Source $script
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
