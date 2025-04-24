@echo off
REM Check if .venv directory exists
if not exist ".venv" (
    REM Create virtual environment
    python -m venv .venv
)

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Get Python version as major.minor (e.g. 3.10)
for /f "tokens=2 delims= " %%v in ('python -V 2^>^&1') do set "full_version=%%v"
for /f "tokens=1,2 delims=." %%a in ("%full_version%") do (
    set "major=%%a"
    set "minor=%%b"
)

REM Compare version to 3.11
setlocal enabledelayedexpansion
if !major! EQU 3 (
    if !minor! GTR 11 (
        REM Upgrade setuptools if Python version > 3.11
        pip install --upgrade setuptools
    )
) else if !major! GTR 3 (
    REM If major version > 3, also upgrade setuptools
    pip install --upgrade setuptools
)
endlocal

REM Install requirements
pip install -r requirements.txt

REM Run the analyzer script
echo y | pyinstaller --onefile --windowed --name=MealyMooreAnalyzer --icon=icon.ico analyzer.py
