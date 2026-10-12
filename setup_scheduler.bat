@echo off
setlocal
cd /d "%~dp0"

echo ==========================================================
echo  Registering Daily Atmospheric Physics Auto-Sync Task
echo ==========================================================

powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1 %*

pause
