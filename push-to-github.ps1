# AI Shopping Agent - GitHub Push Script for Windows
# This script helps you push your code to GitHub

param(
    [Parameter(Mandatory=$false)]
    [string]$CommitMessage = "Add Docker support and update deployment"
)

Write-Host "🚀 Pushing AI Shopping Agent to GitHub..." -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if this is a git repository
if (-not (Test-Path ".git")) {
    Write-Host "⚠️  This is not a Git repository. Initializing..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Check git status
Write-Host ""
Write-Host "Current Git status:" -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "📝 Staging all changes..." -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "💾 Committing changes..." -ForegroundColor Cyan
git commit -m "$CommitMessage"

if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 1) {
    Write-Host "✅ Changes committed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Commit failed!" -ForegroundColor Red
    exit 1
}

# Check if remote exists
$remoteUrl = git remote get-url origin 2>$null

if (-not $remoteUrl) {
    Write-Host ""
    Write-Host "⚠️  No remote repository configured." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please follow these steps:" -ForegroundColor Cyan
    Write-Host "1. Create a new repository on GitHub" -ForegroundColor White
    Write-Host "2. Run the following command with your repository URL:" -ForegroundColor White
    Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/ai-shopping-agent.git" -ForegroundColor Yellow
    Write-Host "3. Then push with:" -ForegroundColor White
    Write-Host "   git push -u origin main" -ForegroundColor Yellow
    Write-Host ""
    
    # Prompt for repository URL
    $repoUrl = Read-Host "Enter your GitHub repository URL (or press Enter to skip)"
    
    if ($repoUrl) {
        git remote add origin $repoUrl
        Write-Host "✅ Remote repository added" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
        
        # Check if main branch exists, otherwise use master
        $currentBranch = git branch --show-current
        if (-not $currentBranch) {
            git branch -M main
            $currentBranch = "main"
        }
        
        git push -u origin $currentBranch
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🎉 Your code is now on GitHub!" -ForegroundColor Cyan
            Write-Host "🐳 GitHub Actions will automatically build your Docker image" -ForegroundColor Cyan
        } else {
            Write-Host ""
            Write-Host "❌ Push failed!" -ForegroundColor Red
            Write-Host "Please check your GitHub credentials and repository access" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host ""
    Write-Host "✅ Remote repository found: $remoteUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
    
    $currentBranch = git branch --show-current
    if (-not $currentBranch) {
        git branch -M main
        $currentBranch = "main"
    }
    
    git push
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🎉 Your code is now on GitHub!" -ForegroundColor Cyan
        Write-Host "🐳 GitHub Actions will automatically build your Docker image" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "⚠️  Push may have failed or already up to date" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Visit your GitHub repository" -ForegroundColor White
Write-Host "2. Check the 'Actions' tab to see the Docker build progress" -ForegroundColor White
Write-Host "3. Once complete, your image will be available at:" -ForegroundColor White
Write-Host "   ghcr.io/YOUR_USERNAME/ai-shopping-agent:latest" -ForegroundColor Yellow
