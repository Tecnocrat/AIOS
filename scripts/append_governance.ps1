param(
    [string]$Title,
    [string]$Author,
    [string]$Files,
    [string]$Owner,
    [string]$Affected,
    [string]$Alternatives,
    [string]$Benefits,
    [string]$Risks,
    [string]$Effort,
    [string]$Expiry,
    [string]$Approval,
    [string]$Notes
)

if (-not (Test-Path docs/GOVERNANCE_CHANGELOG.md)) {
    Write-Error 'docs/GOVERNANCE_CHANGELOG.md not found'
    exit 2
}

$argsList = @(
    '--title', $Title,
    '--author', $Author,
    '--files', $Files,
    '--owner', $Owner,
    '--affected', $Affected,
    '--alternatives', $Alternatives,
    '--benefits', $Benefits,
    '--risks', $Risks,
    '--effort', $Effort,
    '--expiry', $Expiry,
    '--approval', $Approval,
    '--notes', $Notes
)

python .\scripts\append_governance.py @argsList
