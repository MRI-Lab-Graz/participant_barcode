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

:: Check for LaTeX (pdflatex)
echo.
echo Checking for LaTeX installation...
where pdflatex >nul 2>&1
if %errorlevel% neq 0 (
    echo LaTeX not found. Would you like to install TinyTeX? (Y/N)
    set /p INSTALL_LATEX=
    if /i "%INSTALL_LATEX%"=="Y" (
        echo Installing TinyTeX (lightweight LaTeX distribution)...
        powershell -ExecutionPolicy ByPass -Command "Invoke-WebRequest -Uri 'https://yihui.org/tinytex/install-windows.bat' -OutFile '%TEMP%\install-tinytex.bat'; & '%TEMP%\install-tinytex.bat'"
        echo.
        echo TinyTeX installed! Installing required LaTeX packages...
        tlmgr install collection-fontsrecommended collection-latexrecommended
        echo.
        echo IMPORTANT: Please restart your terminal for PATH changes to take effect.
    ) else (
        echo.
        echo WARNING: LaTeX not installed. Please install MiKTeX or TinyTeX manually.
        echo Download MiKTeX from: https://miktex.org/download
        echo Or TinyTeX from: https://yihui.org/tinytex/
    )
) else (
    echo LaTeX is already installed.
)

echo.
echo Setup complete!
echo To start the application, run: venv\Scripts\activate.bat ^&^& python app.py
pause
