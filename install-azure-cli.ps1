# Azure CLI Installation Script for Windows
# Run this as Administrator

Write-Host "Installing Azure CLI..." -ForegroundColor Green

# Download the MSI
Write-Host "Downloading Azure CLI installer..."
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile "$env:TEMP\AzureCLI.msi"

# Install it
Write-Host "Installing Azure CLI (this may take 2-3 minutes)..."
Start-Process msiexec.exe -ArgumentList "/i $env:TEMP\AzureCLI.msi /quiet /norestart" -Wait -NoNewWindow

Write-Host ""
Write-Host "✓ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Close this terminal and open a NEW terminal to use Azure CLI."
Write-Host "Then run: az login" -ForegroundColor Cyan
Write-Host ""
pause
