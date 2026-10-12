@echo off
setlocal
cd /d "%~dp0"

echo ==========================================================
echo   正在推送到 GitHub: tg56y2p4/atmospheric-study
echo ==========================================================
echo 提示: 如果弹出 GitHub 登录网页/弹窗，请点击 [Sign in with your browser] 授权登录。
echo.

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================================
    echo [SUCCESS] 推送成功！代码已同步至 GitHub！
    echo ==========================================================
) else (
    echo.
    echo ==========================================================
    echo [ERROR] 推送遇到问题，请检查网络或登录状态。
    echo ==========================================================
)

echo.
pause
