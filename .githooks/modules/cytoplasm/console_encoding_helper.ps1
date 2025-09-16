# AIOS Console Encoding Helper
# ===========================
# Ensures proper Unicode support on Windows PowerShell

function Set-ConsoleEncoding {
    <#
    .SYNOPSIS
    Sets up proper Unicode console encoding for Windows compatibility
    
    .DESCRIPTION
    Configures PowerShell console to handle Unicode characters properly,
    especially for AIOS GitHook output with special characters.
    #>
    
    try {
        # Set console output encoding to UTF-8
        if ($PSVersionTable.PSVersion.Major -ge 6) {
            # PowerShell Core/7+ handles UTF-8 better by default
            $OutputEncoding = [System.Text.Encoding]::UTF8
        } else {
            # Windows PowerShell 5.1 needs explicit configuration
            $OutputEncoding = [System.Text.Encoding]::UTF8
            [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
            [Console]::InputEncoding = [System.Text.Encoding]::UTF8
        }
        
        return $true
    } catch {
        Write-Warning "Could not set UTF-8 encoding: $($_.Exception.Message)"
        return $false
    }
}

function Write-HostSafe {
    <#
    .SYNOPSIS
    Safe wrapper for Write-Host that handles Unicode gracefully
    
    .PARAMETER Message
    The message to display
    
    .PARAMETER ForegroundColor
    Text color
    #>
    param(
        [string]$Message,
        [string]$ForegroundColor = "White"
    )
    
    try {
        # Replace problematic Unicode characters with ASCII equivalents
        $SafeMessage = $Message `
            -replace "", "[PASS]" `
            -replace "", "[FAIL]" `
            -replace "", "[WARN]" `
            -replace "", "[TOOL]" `
            -replace "", "[CELL]" `
            -replace "", "[TARGET]" `
            -replace "", "[ROCKET]" `
            -replace "", "[TROPHY]" `
            -replace "", "[CHART]" `
            -replace "", "[BRAIN]" `
            -replace "", "[IDEA]" `
            -replace "", "[STAR]" `
            -replace "", "[SEARCH]" `
            -replace "", "[LIGHTNING]" `
            -replace "", "[FOLDER]" `
            -replace "", "[CLIPBOARD]" `
            -replace "🧹", "[CLEAN]"
        
        Write-Host $SafeMessage -ForegroundColor $ForegroundColor
    } catch {
        # Fallback to basic output
        Write-Host $Message -ForegroundColor $ForegroundColor
    }
}

function Get-SafeProgressBar {
    <#
    .SYNOPSIS
    Creates a safe ASCII progress bar
    
    .PARAMETER Percentage
    Progress percentage (0-100)
    
    .PARAMETER Width
    Width of progress bar in characters
    #>
    param(
        [int]$Percentage,
        [int]$Width = 40
    )
    
    $FilledWidth = [math]::Floor($Width * ($Percentage / 100))
    $EmptyWidth = $Width - $FilledWidth
    
    $Filled = "=" * $FilledWidth
    $Empty = "-" * $EmptyWidth
    
    return "[$Filled$Empty] $Percentage%"
}

# Export functions for use in other scripts
Export-ModuleMember -Function Set-ConsoleEncoding, Write-HostSafe, Get-SafeProgressBar