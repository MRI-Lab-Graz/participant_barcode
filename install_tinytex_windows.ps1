# PowerShell script to install TinyTeX on Windows
Write-Host "Installing TinyTeX (lightweight LaTeX)..." -ForegroundColor Green

# Download and install TinyTeX
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Install TinyTeX
Invoke-WebRequest -Uri "https://yihui.org/tinytex/install-windows.bat" -OutFile "$env:TEMP\install-tinytex.bat"
& "$env:TEMP\install-tinytex.bat"

# Install required LaTeX packages
tlmgr install pdflatex
tlmgr install collection-fontsrecommended
tlmgr install collection-latexrecommended

Write-Host "TinyTeX installation complete!" -ForegroundColor Green
Write-Host "Please restart your terminal for PATH changes to take effect." -ForegroundColor Yellow
