@echo off
REM ============================================================
REM Linear Algebra Curriculum -- single-click launcher.
REM Double-click this file. It will, in order:
REM   1. Create a virtual env and install deps if missing.
REM   2. Build the standalone .exe if missing or out of date.
REM   3. Launch the app.
REM Subsequent launches skip steps 1 and 2 and start instantly.
REM ============================================================
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "EXE=dist\visual-explainers.exe"
set "NEED_BUILD=0"

REM ---- 1. Ensure venv + dependencies ----
if not exist ".venv\Scripts\python.exe" goto setup_venv
goto check_build

:setup_venv
echo [Launch] First-time setup: creating virtual environment...
python -m venv .venv
if errorlevel 1 goto err_python
echo [Launch] Installing dependencies (this takes about a minute)...
".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt
if errorlevel 1 goto err_pip
set "NEED_BUILD=1"
goto check_build

:check_build
if not exist "%EXE%" (
    set "NEED_BUILD=1"
    goto maybe_build
)

REM Compare timestamps via PowerShell one-liner (single line, no carets)
powershell -NoProfile -ExecutionPolicy Bypass -Command "$exe=Get-Item '%EXE%'; $src=Get-ChildItem -Recurse -Include *.py | Where-Object { $_.FullName -notmatch '\\.venv\\' -and $_.FullName -notmatch '\\build\\' -and $_.FullName -notmatch '\\dist\\' } | Sort-Object LastWriteTime -Descending | Select-Object -First 1; if ($src -and $src.LastWriteTime -gt $exe.LastWriteTime) { exit 1 } else { exit 0 }"
if errorlevel 1 set "NEED_BUILD=1"

:maybe_build
if "%NEED_BUILD%"=="1" goto do_build
goto launch

:do_build
echo [Launch] Building visual-explainers.exe (1 to 3 minutes, only when source changes)...
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --onefile --windowed --name visual-explainers --collect-all matplotlib app.py >nul 2>&1
if errorlevel 1 goto err_build
goto launch

:launch
start "" "%EXE%"
endlocal
exit /b 0

:err_python
echo.
echo ERROR: Could not create the virtual environment.
echo Make sure Python 3.10+ is installed and on your PATH.
pause
exit /b 1

:err_pip
echo.
echo ERROR: pip install failed.
pause
exit /b 1

:err_build
echo.
echo ERROR: build failed. Run build.bat for verbose output.
pause
exit /b 1
