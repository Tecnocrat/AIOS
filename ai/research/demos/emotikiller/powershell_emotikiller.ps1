# AIOS Emoticon Destroyer - PowerShell Implementation
# STRICT NO EMOTICON POLICY ENFORCED
# Optimized for Windows environments with comprehensive file handling

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath,
    [switch]$CreateBackup = $true,
    [switch]$Verbose = $false
)

# Global statistics
$script:EmoticonStats = @{
    FilesProcessed = 0
    EmoticonsDestroyed = 0
    BackupFilesCreated = 0
    StartTime = Get-Date
}

# Configuration
$script:Config = @{
    TargetExtensions = @('.md', '.txt', '.py', '.cpp', '.c', '.h', '.hpp', '.cs', '.js', '.ts', '.json', '.yaml', '.yml')
    SkipDirectories = @('node_modules', '.git', 'venv', 'env', '__pycache__', 'aios_env', '.vscode', 'bin', 'obj', 'build', '.vs')
    MaxFileSize = 10MB
}

# Emoticon patterns (Unicode ranges)
$script:EmoticonPatterns = @(
    '[\u{1F600}-\u{1F64F}]',  # Emoticons
    '[\u{1F300}-\u{1F5FF}]',  # Misc Symbols
    '[\u{1F680}-\u{1F6FF}]',  # Transport
    '[\u{1F1E0}-\u{1F1FF}]',  # Flags
    '[\u{2600}-\u{26FF}]',    # Misc symbols
    '[\u{2700}-\u{27BF}]',    # Dingbats
    '[\u{E000}-\u{F8FF}]',    # Private use
    '[\u{FE00}-\u{FE0F}]',    # Variation selectors
    '[\u{1F900}-\u{1F9FF}]',  # Supplemental Symbols
    '[\u{1FA70}-\u{1FAFF}]',  # Extended emoticons
    ':[\)\(\|DP]',            # ASCII emoticons
    ';[\)]',                  # Winking emoticons
    '8[\)\(D]',               # 8-series emoticons
    'XD|xD'                   # Laughing emoticons
)

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "SUCCESS" { Write-Host $logMessage -ForegroundColor Green }
        "WARNING" { Write-Host $logMessage -ForegroundColor Yellow }
        default { Write-Host $logMessage }
    }
    
    if ($Verbose) {
        Add-Content -Path "emotikiller_log.txt" -Value $logMessage
    }
}

function Test-ShouldSkipDirectory {
    param([string]$DirectoryPath)
    
    foreach ($skipDir in $script:Config.SkipDirectories) {
        if ($DirectoryPath -like "*$skipDir*") {
            return $true
        }
    }
    return $false
}

function Test-HasTargetExtension {
    param([string]$FilePath)
    
    $extension = [System.IO.Path]::GetExtension($FilePath).ToLower()
    return $script:Config.TargetExtensions -contains $extension
}

function New-BackupFile {
    param([string]$FilePath)
    
    try {
        $backupPath = "$FilePath.backup"
        Copy-Item -Path $FilePath -Destination $backupPath -Force
        $script:EmoticonStats.BackupFilesCreated++
        Write-Log "Backup created: $backupPath" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "Failed to create backup for $FilePath`: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Count-Emoticons {
    param([string]$Content)
    
    $count = 0
    foreach ($pattern in $script:EmoticonPatterns) {
        $matches = [regex]::Matches($Content, $pattern)
        $count += $matches.Count
    }
    return $count
}

function Remove-Emoticons {
    param([string]$Content)
    
    $cleanContent = $Content
    foreach ($pattern in $script:EmoticonPatterns) {
        $cleanContent = [regex]::Replace($cleanContent, $pattern, '', 'IgnoreCase')
    }
    return $cleanContent
}

function ProcessFile {
    param([string]$FilePath)
    
    Write-Log "Processing file: $FilePath"
    
    try {
        # Check file size
        $fileInfo = Get-Item -Path $FilePath
        if ($fileInfo.Length -gt $script:Config.MaxFileSize) {
            Write-Log "Skipping large file: $FilePath (Size: $($fileInfo.Length) bytes)" "WARNING"
            return $true
        }
        
        # Read file content with proper encoding detection
        $encoding = 'UTF8'
        try {
            $content = Get-Content -Path $FilePath -Raw -Encoding $encoding
        }
        catch {
            # Fallback to default encoding
            $content = Get-Content -Path $FilePath -Raw
        }
        
        if ([string]::IsNullOrEmpty($content)) {
            Write-Log "Empty file skipped: $FilePath" "WARNING"
            return $true
        }
        
        # Count emoticons
        $initialCount = Count-Emoticons -Content $content
        if ($initialCount -eq 0) {
            Write-Log "No emoticons found in: $FilePath"
            return $true
        }
        
        # Create backup if requested
        if ($CreateBackup) {
            if (-not (New-BackupFile -FilePath $FilePath)) {
                return $false
            }
        }
        
        # Remove emoticons
        $cleanContent = Remove-Emoticons -Content $content
        
        # Write cleaned content back
        Set-Content -Path $FilePath -Value $cleanContent -Encoding $encoding -NoNewline
        
        # Update statistics
        $script:EmoticonStats.EmoticonsDestroyed += $initialCount
        $script:EmoticonStats.FilesProcessed++
        
        Write-Log "Removed $initialCount emoticons from: $FilePath" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "Failed to process file $FilePath`: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function ProcessDirectory {
    param([string]$DirectoryPath)
    
    Write-Log "Scanning directory: $DirectoryPath"
    
    try {
        $files = Get-ChildItem -Path $DirectoryPath -Recurse -File | Where-Object {
            $shouldProcess = $true
            
            # Check if directory should be skipped
            if (Test-ShouldSkipDirectory -DirectoryPath $_.DirectoryName) {
                $shouldProcess = $false
            }
            
            # Check if file has target extension
            if ($shouldProcess -and -not (Test-HasTargetExtension -FilePath $_.FullName)) {
                $shouldProcess = $false
            }
            
            return $shouldProcess
        }
        
        $totalFiles = $files.Count
        Write-Log "Found $totalFiles files to process"
        
        $currentFile = 0
        foreach ($file in $files) {
            $currentFile++
            $percentComplete = [math]::Round(($currentFile / $totalFiles) * 100, 2)
            
            Write-Progress -Activity "Processing Files" -Status "File $currentFile of $totalFiles ($percentComplete%)" -PercentComplete $percentComplete
            
            ProcessFile -FilePath $file.FullName
        }
        
        Write-Progress -Activity "Processing Files" -Completed
        return $true
    }
    catch {
        Write-Log "Failed to process directory $DirectoryPath`: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Show-Statistics {
    $endTime = Get-Date
    $executionTime = $endTime - $script:EmoticonStats.StartTime
    
    Write-Host "`n[STATISTICS]" -ForegroundColor Cyan
    Write-Host "Files processed: $($script:EmoticonStats.FilesProcessed)" -ForegroundColor Green
    Write-Host "Emoticons destroyed: $($script:EmoticonStats.EmoticonsDestroyed)" -ForegroundColor Green
    Write-Host "Backup files created: $($script:EmoticonStats.BackupFilesCreated)" -ForegroundColor Green
    Write-Host "Execution time: $($executionTime.TotalSeconds.ToString('F2')) seconds" -ForegroundColor Green
    
    if ($script:EmoticonStats.EmoticonsDestroyed -gt 0) {
        $rate = [math]::Round($script:EmoticonStats.EmoticonsDestroyed / $executionTime.TotalSeconds, 2)
        Write-Host "Destruction rate: $rate emoticons/second" -ForegroundColor Yellow
    }
}

# Main execution
Write-Host "[AIOS] Emoticon Destroyer PowerShell Engine" -ForegroundColor Magenta
Write-Host "[POLICY] No emoticons allowed in codebase" -ForegroundColor Red

# Validate target path
if (-not (Test-Path -Path $TargetPath)) {
    Write-Log "Invalid path: $TargetPath" "ERROR"
    exit 1
}

$success = $false

if (Test-Path -Path $TargetPath -PathType Container) {
    # Process directory
    $success = ProcessDirectory -DirectoryPath $TargetPath
}
elseif (Test-Path -Path $TargetPath -PathType Leaf) {
    # Process single file
    if (Test-HasTargetExtension -FilePath $TargetPath) {
        $success = ProcessFile -FilePath $TargetPath
    }
    else {
        Write-Log "File type not supported: $TargetPath" "WARNING"
        $success = $true
    }
}
else {
    Write-Log "Invalid path type: $TargetPath" "ERROR"
    exit 1
}

Show-Statistics

if ($success) {
    Write-Log "Emoticon destruction completed successfully" "SUCCESS"
    exit 0
}
else {
    Write-Log "Emoticon destruction failed" "ERROR"
    exit 1
}