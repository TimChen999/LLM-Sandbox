@echo off
REM Quick dev launcher — runs the app from source via the venv Python.
REM For a standalone .exe, run build.bat instead and use dist\visual-explainers.exe.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: virtual environment not found. Run setup first:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

".venv\Scripts\pythonw.exe" app.py
