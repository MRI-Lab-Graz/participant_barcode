@echo off
echo Setting up Participant Barcode Tool...

:: Check for UV
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo UV not found. Installing UV...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
)

:: Create virtual environment in root using UV
if not exist "..\venv" (
    echo Creating virtual environment...
    uv venv ..\venv
)

:: Activate virtual environment and install dependencies
echo Installing dependencies...
call ..\venv\Scripts\activate.bat
uv pip install -r "%~dp0requirements.txt"

echo Setup complete!
echo To start the application, run: venv\Scripts\activate.bat ^&^& python app.py
pause
