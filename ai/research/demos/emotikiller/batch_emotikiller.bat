@echo off
REM AIOS Emoticon Destroyer - Batch Implementation
REM STRICT NO EMOTICON POLICY ENFORCED
REM Windows batch file for basic emoticon removal

setlocal enabledelayedexpansion

REM Initialize statistics
set /a FILES_PROCESSED=0
set /a EMOTICONS_DESTROYED=0
set /a BACKUP_FILES_CREATED=0

REM Configuration
set TARGET_EXTENSIONS=.md .txt .py .cpp .c .h .hpp .cs .js .ts .json .yaml .yml
set SKIP_DIRS=node_modules .git venv env __pycache__ aios_env .vscode bin obj build .vs

echo [AIOS] Emoticon Destroyer Batch Engine
echo [POLICY] No emoticons allowed in codebase
echo.

REM Check command line arguments
if "%~1"=="" (
    echo [ERROR] Usage: %~nx0 ^<file_or_directory_path^>
    exit /b 1
)

set "TARGET_PATH=%~1"

REM Check if target path exists
if not exist "%TARGET_PATH%" (
    echo [ERROR] Invalid path: %TARGET_PATH%
    exit /b 1
)

REM Determine if target is file or directory
if exist "%TARGET_PATH%\*" (
    echo [BATCH] Processing directory: %TARGET_PATH%
    call :ProcessDirectory "%TARGET_PATH%"
) else (
    echo [BATCH] Processing file: %TARGET_PATH%
    call :ProcessFile "%TARGET_PATH%"
)

REM Print statistics
call :PrintStatistics

echo [SUCCESS] Emoticon destruction completed
exit /b 0

:ProcessDirectory
set "DIR_PATH=%~1"
echo [BATCH] Scanning directory: %DIR_PATH%

for /r "%DIR_PATH%" %%F in (*) do (
    set "FILE_PATH=%%F"
    set "SKIP_FILE=0"
    
    REM Check if file should be skipped based on directory
    for %%D in (%SKIP_DIRS%) do (
        echo !FILE_PATH! | findstr /i "%%D" >nul 2>&1
        if !errorlevel! equ 0 set "SKIP_FILE=1"
    )
    
    REM Check if file has target extension
    if !SKIP_FILE! equ 0 (
        set "HAS_TARGET_EXT=0"
        for %%E in (%TARGET_EXTENSIONS%) do (
            if /i "%%~xF"=="%%E" set "HAS_TARGET_EXT=1"
        )
        
        if !HAS_TARGET_EXT! equ 1 (
            call :ProcessFile "!FILE_PATH!"
        )
    )
)
goto :eof

:ProcessFile
set "FILE_PATH=%~1"
echo [BATCH] Processing file: %FILE_PATH%

REM Check if file exists and is not empty
if not exist "%FILE_PATH%" (
    echo [ERROR] File not found: %FILE_PATH%
    goto :eof
)

REM Get file size (basic check)
for %%A in ("%FILE_PATH%") do set FILE_SIZE=%%~zA
if %FILE_SIZE% equ 0 (
    echo [INFO] Empty file skipped: %FILE_PATH%
    goto :eof
)

REM Create backup
set "BACKUP_PATH=%FILE_PATH%.backup"
copy "%FILE_PATH%" "%BACKUP_PATH%" >nul 2>&1
if !errorlevel! equ 0 (
    set /a BACKUP_FILES_CREATED+=1
    echo [BACKUP] Created: %BACKUP_PATH%
) else (
    echo [ERROR] Failed to create backup for: %FILE_PATH%
    goto :eof
)

REM Create temporary file for processing
set "TEMP_FILE=%FILE_PATH%.tmp"

REM Process file content (remove common emoticon patterns)
set /a EMOTICON_COUNT=0

REM Use PowerShell for more advanced text processing
powershell -Command "& {
    $content = Get-Content -Path '%FILE_PATH%' -Raw -ErrorAction SilentlyContinue
    if ($content) {
        $originalLength = $content.Length
        
        # Remove Unicode emoticons (basic patterns)
        $content = $content -replace '[\u{1F600}-\u{1F64F}]', ''
        $content = $content -replace '[\u{1F300}-\u{1F5FF}]', ''
        $content = $content -replace '[\u{1F680}-\u{1F6FF}]', ''
        $content = $content -replace '[\u{2600}-\u{26FF}]', ''
        
        # Remove ASCII emoticons
        $content = $content -replace '[:;=8xX][\-o\*\'']*[\)\]\(\[dDpP/\\oO\{\}]', ''
        $content = $content -replace '[\)\]\(\[][:;=8xX][\-o\*\'']*', ''
        $content = $content -replace '\bXD\b', ''
        $content = $content -replace '\bxD\b', ''
        $content = $content -replace '\bLOL\b', ''
        $content = $content -replace '\bLMAO\b', ''
        $content = $content -replace '\bROFL\b', ''
        $content = $content -replace '\bHAHA+\b', ''
        $content = $content -replace '\bHEHE+\b', ''
        $content = $content -replace '\bOMG\b', ''
        
        # Clean up extra whitespace
        $content = $content -replace '\s{3,}', '  '
        $content = $content -replace '\n{3,}', \"`n`n\"
        
        # Calculate removed emoticons (rough estimate)
        $newLength = $content.Length
        $removedChars = $originalLength - $newLength
        $estimatedEmoticons = [math]::Max(0, [math]::Floor($removedChars / 2))
        
        # Write cleaned content
        Set-Content -Path '%FILE_PATH%' -Value $content -NoNewline -ErrorAction SilentlyContinue
        
        # Output emoticon count for batch processing
        Write-Output $estimatedEmoticons
    } else {
        Write-Output 0
    }
}" > "%TEMP_FILE%"

REM Read emoticon count from temp file
if exist "%TEMP_FILE%" (
    set /p EMOTICON_COUNT=<"%TEMP_FILE%"
    del "%TEMP_FILE%"
)

REM Update statistics
set /a FILES_PROCESSED+=1
set /a EMOTICONS_DESTROYED+=!EMOTICON_COUNT!

if !EMOTICON_COUNT! gtr 0 (
    echo [SUCCESS] Removed !EMOTICON_COUNT! emoticons from: %FILE_PATH%
) else (
    echo [INFO] No emoticons found in: %FILE_PATH%
)

goto :eof

:PrintStatistics
echo.
echo [STATISTICS]
echo ============
echo Files processed: %FILES_PROCESSED%
echo Emoticons destroyed: %EMOTICONS_DESTROYED%
echo Backup files created: %BACKUP_FILES_CREATED%
echo ============
goto :eof