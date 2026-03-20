#!/usr/bin/env powershell
<#
.SYNOPSIS
    Automated Azure deployment script for THE FINISHER LUXURY
.DESCRIPTION
    Creates all Azure resources and deploys the application
#>

param(
    [string]$SubscriptionId,
    [string]$AdminPassword = "AdminUser@123"
)

# Colors for output
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"

function Write-Info { Write-Host $args -ForegroundColor $InfoColor }
function Write-Success { Write-Host $args -ForegroundColor $SuccessColor }
function Write-Error { Write-Host $args -ForegroundColor $ErrorColor }

Write-Info "========================================"
Write-Info "THE FINISHER LUXURY - Azure Deployment"
Write-Info "========================================"
Write-Info ""

# Check if logged in
Write-Info "Checking Azure authentication..."
$account = az account show 2>$null

if ($null -eq $account) {
    Write-Info "You need to login to Azure first."
    Write-Info "Opening Azure Portal..."
    az login
} else {
    Write-Success "Already authenticated!"
}

# Get subscription ID
if (-not $SubscriptionId) {
    Write-Info "Getting subscription..."
    $account = az account show | ConvertFrom-Json
    $SubscriptionId = $account.id
}

Write-Success "Using subscription: $SubscriptionId"

# Variables
$ResourceGroup = "finisher-luxury-rg"
$Location = "eastus"
$DbServer = "finisher-luxury-db"
$DbName = "finisher_db"
$DbUser = "adminuser"
$AppServiceName = "finisher-luxury-backend"
$AppServicePlan = "finisher-luxury-plan"

Write-Info ""
Write-Info "Creating Resource Group: $ResourceGroup..."
az group create `
    --name $ResourceGroup `
    --location $Location `
    --subscription $SubscriptionId

Write-Success "✓ Resource Group created"

Write-Info ""
Write-Info "Creating PostgreSQL Database..."
az postgres flexible-server create `
    --resource-group $ResourceGroup `
    --name $DbServer `
    --location $Location `
    --admin-user $DbUser `
    --admin-password $AdminPassword `
    --database-name $DbName `
    --public-access "0.0.0.0" `
    --storage-size 32768 `
    --sku-name "Standard_B1ms" `
    --tier "Burstable" `
    --version 15 `
    --subscription $SubscriptionId

Write-Success "✓ PostgreSQL Database created"

Write-Info ""
Write-Info "Creating App Service Plan..."
az appservice plan create `
    --name $AppServicePlan `
    --resource-group $ResourceGroup `
    --is-linux `
    --sku "F1" `
    --subscription $SubscriptionId

Write-Success "✓ App Service Plan created"

Write-Info ""
Write-Info "Creating App Service..."
az webapp create `
    --resource-group $ResourceGroup `
    --plan $AppServicePlan `
    --name $AppServiceName `
    --runtime "PYTHON|3.11" `
    --subscription $SubscriptionId

Write-Success "✓ App Service created"

# Get database connection string
Write-Info ""
Write-Info "Getting database connection details..."
$DbHost = "$DbServer.postgres.database.azure.com"
$DbConnectionString = "postgresql://${DbUser}:${AdminPassword}@${DbHost}/${DbName}?sslmode=require"

Write-Info ""
Write-Info "Setting environment variables..."
az webapp config appsettings set `
    --resource-group $ResourceGroup `
    --name $AppServiceName `
    --settings `
    PYTHON_VERSION="3.11" `
    DEBUG="False" `
    SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')" `
    DATABASE_URL="$DbConnectionString" `
    ALLOWED_HOSTS=".azurewebsites.net,.vercel.app" `
    FRONTEND_URL="https://the-finisher-luxury.vercel.app" `
    CORS_ALLOW_ALL_ORIGINS="True" `
    EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend" `
    EMAIL_HOST="smtp-mail.outlook.com" `
    EMAIL_PORT="587" `
    EMAIL_USE_TLS="True" `
    EMAIL_HOST_USER="natedgraphics011@outlook.com" `
    DEFAULT_FROM_EMAIL="natedgraphics011@outlook.com" `
    DJANGO_SUPERUSER_USERNAME="admin" `
    DJANGO_SUPERUSER_EMAIL="admin@thefinisher.com" `
    DJANGO_SUPERUSER_PASSWORD="Admin@2025!" `
    --subscription $SubscriptionId

Write-Success "✓ Environment variables set"

Write-Info ""
Write-Info "Getting App Service URL..."
$AppUrl = az webapp show `
    --resource-group $ResourceGroup `
    --name $AppServiceName `
    --query defaultHostName `
    --output tsv `
    --subscription $SubscriptionId

Write-Success "✓ Backend URL: https://$AppUrl"

Write-Info ""
Write-Info "Configuring GitHub deployment..."
az webapp deployment source config `
    --resource-group $ResourceGroup `
    --name $AppServiceName `
    --repo-url "https://github.com/MondeMtambo/the-finisher-luxury.git" `
    --branch "main" `
    --manual-integration `
    --subscription $SubscriptionId

Write-Success "✓ GitHub deployment configured"

Write-Info ""
Write-Success "========================================="
Write-Success "✓ DEPLOYMENT COMPLETE!"
Write-Success "========================================="
Write-Info ""
Write-Info "Next steps:"
Write-Info "1. Backend URL: https://$AppUrl"
Write-Info "2. Go to Vercel settings"
Write-Info "3. Set VITE_API_BASE_URL = https://$AppUrl"
Write-Info "4. Redeploy Vercel frontend"
Write-Info ""
Write-Info "Admin credentials:"
Write-Info "Username: admin"
Write-Info "Password: Admin@2025!"
Write-Info ""
Write-Info "Database:"
Write-Info "Server: $DbHost"
Write-Info "Database: $DbName"
Write-Info "User: $DbUser"
Write-Info "Connection: $DbConnectionString"
