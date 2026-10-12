# Setup Windows Task Scheduler for Daily Atmospheric Physics Sync
param(
    [string]$Time = "09:00",
    [switch]$Uninstall,
    [switch]$Status
)

$TaskName = "AtmosphericPhysics_DailySync"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RunnerBat = Join-Path $ProjectRoot "scripts\run_sync.bat"

if ($Status) {
    Write-Host "Checking status of scheduled task '$TaskName'..." -ForegroundColor Cyan
    schtasks /query /tn $TaskName /fo LIST /v
    exit 0
}

if ($Uninstall) {
    Write-Host "Removing scheduled task '$TaskName'..." -ForegroundColor Yellow
    schtasks /delete /tn $TaskName /f
    Write-Host "Task '$TaskName' has been removed." -ForegroundColor Green
    exit 0
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Configuring Windows Task Scheduler" -ForegroundColor Cyan
Write-Host " Task Name   : $TaskName" -ForegroundColor Cyan
Write-Host " Target Bat  : $RunnerBat" -ForegroundColor Cyan
Write-Host " Schedule    : Daily at $Time" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if (-not (Test-Path $RunnerBat)) {
    Write-Host "[ERROR] Runner script not found at $RunnerBat" -ForegroundColor Red
    exit 1
}

# Create or update daily scheduled task
$cmd = "schtasks /create /tn `"$TaskName`" /tr `"\`"$RunnerBat\`"`" /sc daily /st $Time /f"
Write-Host "Executing: $cmd" -ForegroundColor Gray
Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[SUCCESS] Daily scheduled task '$TaskName' successfully registered!" -ForegroundColor Green
    Write-Host "It will run automatically every day at $Time." -ForegroundColor Green
    Write-Host "`nUseful commands:" -ForegroundColor Gray
    Write-Host "  View status: powershell -File setup_scheduler.ps1 -Status" -ForegroundColor Gray
    Write-Host "  Uninstall  : powershell -File setup_scheduler.ps1 -Uninstall" -ForegroundColor Gray
} else {
    Write-Host "`n[ERROR] Failed to register task. Please run PowerShell as Administrator." -ForegroundColor Red
}
