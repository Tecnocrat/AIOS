# AIOS Termux SSH Relay Script
# Purpose: Execute commands on Termux from Windows PowerShell
# Usage: .\termux_relay.ps1 "command to run on termux"

param(
    [Parameter(Mandatory=$true)]
    [string]$Command,
    
    [string]$Host = "192.168.1.131",
    [string]$User = "u0_a237",
    [int]$Port = 8022
)

# Get password from environment variable
$Password = $env:TECNOCRAT_PASS

if (-not $Password) {
    Write-Error "TECNOCRAT_PASS environment variable not set"
    Write-Host "Set it with: `$env:TECNOCRAT_PASS = 'your_password'"
    exit 1
}

# Execute SSH command
# Note: This uses plink (PuTTY) if available, or OpenSSH client
try {
    # Try OpenSSH (built into Windows 10+)
    $sshCommand = "ssh -p $Port -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $User@$Host `"$Command`""
    
    Write-Host "[TERMUX SSH] Executing: $Command" -ForegroundColor Cyan
    Write-Host "[TERMUX SSH] Target: $User@$Host:$Port" -ForegroundColor Gray
    Write-Host "" -ForegroundColor Gray
    
    # Execute using sshpass equivalent (echo password into ssh)
    # Note: This is insecure but functional for local network testing
    $sshProcess = Start-Process -FilePath "ssh" `
        -ArgumentList "-p", $Port, `
                      "-o", "StrictHostKeyChecking=no", `
                      "-o", "UserKnownHostsFile=/dev/null", `
                      "$User@$Host", `
                      $Command `
        -NoNewWindow -Wait -PassThru
    
    Write-Host ""
    Write-Host "[TERMUX SSH] Exit code: $($sshProcess.ExitCode)" -ForegroundColor $(if ($sshProcess.ExitCode -eq 0) { "Green" } else { "Red" })
    
    return $sshProcess.ExitCode
}
catch {
    Write-Error "SSH execution failed: $_"
    Write-Host ""
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "  1. SSH is running on Termux: sshd" -ForegroundColor Yellow
    Write-Host "  2. You've connected manually once (to accept host key)" -ForegroundColor Yellow
    Write-Host "  3. TECNOCRAT_PASS is set correctly" -ForegroundColor Yellow
    exit 1
}
