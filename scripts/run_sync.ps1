# Atmospheric Physics Course Auto-Sync PowerShell Runner
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..")

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Atmospheric Physics Course Auto-Sync Pipeline" -ForegroundColor Cyan
Write-Host " Root Directory: $ProjectRoot" -ForegroundColor Cyan
Write-Host " Current Time  : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

Set-Location $ProjectRoot

try {
    python scripts/sync_course.py $args
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[SUCCESS] Sync pipeline completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "`n[ERROR] Sync script returned non-zero exit code: $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "`n[EXCEPTION] Failed to run sync script: $_" -ForegroundColor Red
    exit 1
}
