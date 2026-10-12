@echo off
setlocal
cd /d "%~dp0.."
echo ========================================================
echo   Atmospheric Physics Course Auto-Sync Pipeline
echo   Time: %date% %time%
echo ========================================================

python scripts\sync_course.py %*

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Sync failed with exit code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo [SUCCESS] Sync pipeline completed successfully.
exit /b 0
