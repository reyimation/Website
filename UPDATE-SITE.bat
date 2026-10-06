@echo off
cd /d "%~dp0"
where py >nul 2>nul && (py update.py) || (python update.py)
echo.
pause
