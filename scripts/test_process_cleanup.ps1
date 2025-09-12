#!/usr/bin/env pwsh

Write-Host "🧪 AIOS Process Management Test Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

Write-Host "`n📊 Current AIOS Processes:" -ForegroundColor Yellow
$currentProcesses = Get-Process | Where-Object { $_.ProcessName -like "*AIOS*" -or $_.ProcessName -eq "aios_tachyonic_viewer" }
if ($currentProcesses) {
    $currentProcesses | Format-Table -AutoSize
    Write-Host "✅ Found $($currentProcesses.Count) AIOS processes running" -ForegroundColor Green
} else {
    Write-Host "❌ No AIOS processes found" -ForegroundColor Red
}

Write-Host "`n🔍 Testing Process Cleanup..." -ForegroundColor Yellow
Write-Host "Simulating main window closure by terminating Visual Interface process..." -ForegroundColor Yellow

# Find the main Visual Interface process
$visualInterface = Get-Process | Where-Object { $_.ProcessName -eq "AIOS.VisualInterface" }
if ($visualInterface) {
    Write-Host "🎯 Found Visual Interface process (PID: $($visualInterface.Id))" -ForegroundColor Cyan
    
    # Terminate the main process (simulating window closure)
    Stop-Process -Id $visualInterface.Id -Force
    Write-Host "🛑 Visual Interface process terminated" -ForegroundColor Yellow
    
    # Wait a moment for cleanup
    Start-Sleep -Seconds 3
    
    Write-Host "`n🔍 Checking for remaining processes..." -ForegroundColor Yellow
    $remainingProcesses = Get-Process | Where-Object { $_.ProcessName -like "*AIOS*" -or $_.ProcessName -eq "aios_tachyonic_viewer" }
    
    if ($remainingProcesses) {
        Write-Host "⚠️  Found remaining processes:" -ForegroundColor Yellow
        $remainingProcesses | Format-Table -AutoSize
        
        Write-Host "`n🧹 Cleaning up orphaned processes..." -ForegroundColor Yellow
        $remainingProcesses | ForEach-Object { 
            Stop-Process -Id $_.Id -Force
            Write-Host "   Cleaned up: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
        }
    } else {
        Write-Host "✅ SUCCESS: No orphaned processes remain!" -ForegroundColor Green
        Write-Host "   Centralized process management is working correctly!" -ForegroundColor Green
    }
} else {
    Write-Host "❌ No Visual Interface process found to test" -ForegroundColor Red
}

Write-Host "`n📊 Final Process Check:" -ForegroundColor Yellow
$finalProcesses = Get-Process | Where-Object { $_.ProcessName -like "*AIOS*" -or $_.ProcessName -eq "aios_tachyonic_viewer" }
if ($finalProcesses) {
    Write-Host "⚠️  Some processes still remain:" -ForegroundColor Yellow
    $finalProcesses | Format-Table -AutoSize
} else {
    Write-Host "✅ PERFECT: All AIOS processes have been cleaned up!" -ForegroundColor Green
}

Write-Host "`n🏁 Test Complete!" -ForegroundColor Cyan
