@echo off
echo ========================================
echo   Controlled Anonymity - Frontend
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Starting frontend server on http://localhost:3000
echo Press Ctrl+C to stop
echo.

python -m http.server 3000
