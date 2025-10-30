# AI Shopping Agent - Docker Build Script for Windows
# This script builds the Docker image for the AI Shopping Agent

Write-Host "🐳 Building AI Shopping Agent Docker Image..." -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if Docker daemon is running
try {
    docker ps | Out-Null
    Write-Host "✅ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker daemon is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Cyan
Write-Host ""

# Build the Docker image
docker build -t ai-shopping-agent:latest .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run the container with:" -ForegroundColor Cyan
    Write-Host "  docker run -d -p 8501:8501 --name ai-shopping-agent ai-shopping-agent:latest" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or use Docker Compose:" -ForegroundColor Cyan
    Write-Host "  docker-compose up -d" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Access the application at: http://localhost:8501" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    Write-Host "Please check the error messages above" -ForegroundColor Yellow
    exit 1
}
