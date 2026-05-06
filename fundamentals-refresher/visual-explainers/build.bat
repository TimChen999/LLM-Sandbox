@echo off
REM Builds visual-explainers.exe (single-file) into dist\
REM Run this once after setup; the resulting .exe is standalone (no Python needed).

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: virtual environment not found. Run setup first:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo Building visual-explainers.exe...
".venv\Scripts\python.exe" -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name visual-explainers ^
    --collect-all matplotlib ^
    app.py

if errorlevel 1 (
    echo.
    echo Build failed.
    pause
    exit /b 1
)

echo.
echo Build succeeded. The executable is at:
echo   %~dp0dist\visual-explainers.exe
echo.
pause
