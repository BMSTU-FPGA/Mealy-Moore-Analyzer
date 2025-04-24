@echo off

REM Check if the virtual environment directory exists
if not exist "%USERPROFILE%\.venv" (
    python -m venv "%USERPROFILE%\.venv"
)

REM Activate the virtual environment
call "%USERPROFILE%\.venv\Scripts\activate.bat"

REM Get the Python version
for /f "tokens=1,2 delims=." %%a in ('python -V 2^>^&1 ^| awk "{print $2}" ^| cut -d. -f1-2') do (
    set python_version=%%a.%%b
)

REM Check if the version is more than 3.11 (then we need to install pip)
if %python_version% gtr 3.11 (
    pip install --upgrade setuptools
)

REM Install requirements
pip install -r requirements.txt

REM Run the analyzer script
python analyzer.py

REM Deactivate the virtual environment
call deactivate
