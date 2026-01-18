@echo off
echo Setting up Participant Barcode Tool...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: Create virtual environment in root
if not exist "..\venv" (
    echo Creating virtual environment...
    python -m venv ..\venv
)

:: Activate virtual environment and install dependencies
echo Installing dependencies...
call ..\venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete!
echo To start the application, run: venv\Scripts\activate.bat ^&^& python app.py
pause
