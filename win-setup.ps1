# ====================================
#  AI-ChatBot Deployment (Windows)
# ====================================

$REPO_URL = "https://github.com/1Z4t-R3p0/AI-ChatBot.git"
$PROJECT_DIR = "$HOME\AI-ChatBot"

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "   AI-ChatBot Setup & Deployment" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# 1. Check and Install Git
if (-not (Get-Command "git" -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found. Installing Git..." -ForegroundColor Yellow
    winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
    $env:Path += ";C:\Program Files\Git\cmd"
}

# 2. Check and Install Docker
if (-not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Host "Docker not found. Installing Docker Desktop..." -ForegroundColor Yellow
    winget install --id Docker.DockerDesktop -e --source winget --accept-package-agreements --accept-source-agreements
    Write-Host "=======================================================" -ForegroundColor Red
    Write-Host " Please restart your computer/terminal to finish Docker" -ForegroundColor Red
    Write-Host " installation, then run this script again." -ForegroundColor Red
    Write-Host "=======================================================" -ForegroundColor Red
    exit
}

# Check if Docker daemon is running
docker info > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker is not running! Please start Docker Desktop and run this script again." -ForegroundColor Red
    exit
}

# 3. Clone or Update Project
if (-not (Test-Path $PROJECT_DIR)) {
    Write-Host "Cloning project repository..." -ForegroundColor Green
    git clone $REPO_URL $PROJECT_DIR
} else {
    Write-Host "Project exists at $PROJECT_DIR. Pulling latest changes..." -ForegroundColor Green
    Set-Location $PROJECT_DIR
    git pull
}

# 4. Handle .env file (Ask user for API key if missing)
Set-Location $PROJECT_DIR
if (-not (Test-Path ".env")) {
    Write-Host "====================================" -ForegroundColor Yellow
    Write-Host " OpenRouter API Key Required!" -ForegroundColor Yellow
    $apiKey = Read-Host "Please enter your OPENROUTER_API_KEY"
    "OPENROUTER_API_KEY=$apiKey" | Out-File -FilePath ".env" -Encoding ASCII
}

# 5. Run Docker Compose
Set-Location $PROJECT_DIR
Write-Host "Starting AI-ChatBot Containers..." -ForegroundColor Green
docker compose up -d --build

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host " Deployment Complete!" -ForegroundColor Green
Write-Host " Access Frontend at: http://localhost:8080" -ForegroundColor Green
Write-Host " Access API at: http://localhost:8001" -ForegroundColor Green
Write-Host " Redis Analytics running on port 6380" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
