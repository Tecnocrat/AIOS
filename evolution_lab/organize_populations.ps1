# AIOS Population File Organization Script
# AINLP.dendritic Analysis and Migration
# Created: 2025-01-12
# Purpose: Organize scattered pop_*.json files into populations/ directory

param(
    [switch]$DryRun = $false,
    [switch]$Backup = $true
)

$ErrorActionPreference = "Stop"

Write-Host "🧬 AIOS Population File Organization" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkCyan
Write-Host ""

# Paths
$evolutionLabRoot = "c:\dev\AIOS\evolution_lab"
$populationsDir = Join-Path $evolutionLabRoot "populations"
$backupDir = Join-Path $evolutionLabRoot "populations\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Create populations directory if it doesn't exist
if (-not (Test-Path $populationsDir)) {
    Write-Host "📁 Creating populations directory..." -ForegroundColor Yellow
    if (-not $DryRun) {
        New-Item -ItemType Directory -Path $populationsDir -Force | Out-Null
    }
}

# Find all scattered population files
$indexFiles = Get-ChildItem -Path $evolutionLabRoot -Filter "pop_*_index.json" -File
$generationFiles = Get-ChildItem -Path $evolutionLabRoot -Filter "pop_*_gen*.json" -File
$organismFiles = Get-ChildItem -Path $evolutionLabRoot -Filter "organism_*.py" -File

Write-Host "📊 AINLP.dendritic Analysis:" -ForegroundColor Cyan
Write-Host "   Index files found: $($indexFiles.Count)" -ForegroundColor White
Write-Host "   Generation files found: $($generationFiles.Count)" -ForegroundColor White
Write-Host "   Organism files found: $($organismFiles.Count)" -ForegroundColor White
Write-Host ""

# Group files by population ID
$populations = @{}

foreach ($indexFile in $indexFiles) {
    # Extract population ID (e.g., pop_20251011_181057 from pop_20251011_181057_index.json)
    if ($indexFile.Name -match '^(pop_\d+_\d+)_index\.json$') {
        $popId = $matches[1]
        
        if (-not $populations.ContainsKey($popId)) {
            $populations[$popId] = @{
                IndexFile = $indexFile
                GenerationFiles = @()
                OrganismFiles = @()
            }
        }
    }
}

# Match generation files to populations
foreach ($genFile in $generationFiles) {
    if ($genFile.Name -match '^(pop_\d+_\d+)_gen') {
        $popId = $matches[1]
        
        if ($populations.ContainsKey($popId)) {
            $populations[$popId].GenerationFiles += $genFile
        } else {
            Write-Host "⚠️  Orphaned generation file: $($genFile.Name)" -ForegroundColor Yellow
        }
    }
}

Write-Host "🗂️  Population Groups Discovered:" -ForegroundColor Cyan
foreach ($popId in $populations.Keys | Sort-Object) {
    $pop = $populations[$popId]
    Write-Host "   $popId" -ForegroundColor White
    Write-Host "      Index: $($pop.IndexFile.Name)" -ForegroundColor DarkGray
    Write-Host "      Generations: $($pop.GenerationFiles.Count)" -ForegroundColor DarkGray
}
Write-Host ""

# Create backup if requested
if ($Backup -and -not $DryRun) {
    Write-Host "💾 Creating backup..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    
    foreach ($file in ($indexFiles + $generationFiles + $organismFiles)) {
        Copy-Item -Path $file.FullName -Destination $backupDir -Force
    }
    Write-Host "   Backed up to: $backupDir" -ForegroundColor Green
    Write-Host ""
}

# Organize files
$movedCount = 0
$totalFiles = 0

foreach ($popId in $populations.Keys | Sort-Object) {
    $pop = $populations[$popId]
    $popDir = Join-Path $populationsDir $popId
    
    Write-Host "📦 Organizing $popId..." -ForegroundColor Cyan
    
    if ($DryRun) {
        Write-Host "   [DRY RUN] Would create: $popDir" -ForegroundColor DarkYellow
    } else {
        New-Item -ItemType Directory -Path $popDir -Force | Out-Null
        Write-Host "   Created: $popDir" -ForegroundColor Green
    }
    
    # Move index file
    $destPath = Join-Path $popDir $pop.IndexFile.Name
    if ($DryRun) {
        Write-Host "   [DRY RUN] Would move: $($pop.IndexFile.Name)" -ForegroundColor DarkYellow
    } else {
        Move-Item -Path $pop.IndexFile.FullName -Destination $destPath -Force
        Write-Host "   Moved index: $($pop.IndexFile.Name)" -ForegroundColor Green
        $movedCount++
    }
    $totalFiles++
    
    # Move generation files
    foreach ($genFile in $pop.GenerationFiles) {
        $destPath = Join-Path $popDir $genFile.Name
        if ($DryRun) {
            Write-Host "   [DRY RUN] Would move: $($genFile.Name)" -ForegroundColor DarkYellow
        } else {
            Move-Item -Path $genFile.FullName -Destination $destPath -Force
            Write-Host "   Moved generation: $($genFile.Name)" -ForegroundColor Green
            $movedCount++
        }
        $totalFiles++
    }
}

# Move organism files to a separate organisms/ directory
if ($organismFiles.Count -gt 0) {
    $organismsDir = Join-Path $populationsDir "organisms"
    
    Write-Host "🧬 Organizing organism files..." -ForegroundColor Cyan
    
    if ($DryRun) {
        Write-Host "   [DRY RUN] Would create: $organismsDir" -ForegroundColor DarkYellow
    } else {
        New-Item -ItemType Directory -Path $organismsDir -Force | Out-Null
        Write-Host "   Created: $organismsDir" -ForegroundColor Green
    }
    
    foreach ($orgFile in $organismFiles) {
        $destPath = Join-Path $organismsDir $orgFile.Name
        if ($DryRun) {
            Write-Host "   [DRY RUN] Would move: $($orgFile.Name)" -ForegroundColor DarkYellow
        } else {
            Move-Item -Path $orgFile.FullName -Destination $destPath -Force
            Write-Host "   Moved organism: $($orgFile.Name)" -ForegroundColor Green
            $movedCount++
        }
        $totalFiles++
    }
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkCyan
Write-Host "✅ Organization Complete!" -ForegroundColor Green
Write-Host ""
if ($DryRun) {
    Write-Host "   [DRY RUN MODE] No files were moved" -ForegroundColor Yellow
    Write-Host "   Files that would be organized: $totalFiles" -ForegroundColor White
} else {
    Write-Host "   Files successfully moved: $movedCount / $totalFiles" -ForegroundColor White
    Write-Host "   Backup location: $backupDir" -ForegroundColor White
}
Write-Host ""
Write-Host "🌌 Populations organized following AINLP.dendritic principles" -ForegroundColor Cyan
Write-Host "   Root cause identified: Missing archive_population() method" -ForegroundColor DarkGray
Write-Host "   Next step: Implement proper archiving in population_manager.py" -ForegroundColor DarkGray
Write-Host ""
