# 🚀 Complete Setup Guide for AI Shopping Agent

## Step 1: Restart Your Terminal ✅

Since you just installed Git, you need to **close and reopen your PowerShell terminal** for the changes to take effect.

1. Close this PowerShell window
2. Open a new PowerShell window
3. Navigate back to the project directory:
   ```powershell
   cd "c:\Users\ansarna\Downloads\ai-shopping-agent-main"
   ```

## Step 2: Verify Git Installation

```powershell
git --version
```

You should see something like: `git version 2.x.x`

## Step 3: Configure Git (First Time Only)

If this is your first time using Git, configure your identity:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Replace with your actual name and email (use the same email as your GitHub account).

## Step 4: Initialize Git Repository

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Commit the changes
git commit -m "Initial commit with Docker support"
```

## Step 5: Create GitHub Repository

1. Go to GitHub: https://github.com/new
2. Repository name: `ai-shopping-agent` (or any name you prefer)
3. Description: "AI Shopping Agent - Smart shopping comparison tool"
4. **Do NOT** check "Initialize this repository with a README"
5. Click "Create repository"

## Step 6: Connect to GitHub

After creating the repository on GitHub, you'll see a page with instructions. Use these commands:

```powershell
# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-shopping-agent.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username!

### Alternative: Use the Helper Script

Or simply run:
```powershell
.\push-to-github.ps1
```

This script will guide you through the process.

## Step 7: Build and Run Docker Image

### Option 1: Using Docker Compose (Easiest)
```powershell
docker-compose up -d
```

### Option 2: Using PowerShell Script
```powershell
.\build-docker.ps1
```

### Option 3: Manual Docker Build
```powershell
# Build the image
docker build -t ai-shopping-agent:latest .

# Run the container
docker run -d -p 8501:8501 --name ai-shopping-agent ai-shopping-agent:latest
```

## Step 8: Access Your Application

Open your browser and go to:
```
http://localhost:8501
```

## Step 9: Monitor GitHub Actions

After pushing to GitHub:
1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. You'll see "Docker Build and Push" workflow running
4. Wait for it to complete (5-10 minutes)
5. Your Docker image will be published to GitHub Container Registry

## Step 10: Make Your Docker Image Public (Optional)

1. Go to your GitHub profile → Packages
2. Click on `ai-shopping-agent`
3. Click "Package settings"
4. Scroll down to "Danger Zone"
5. Click "Change visibility" → Select "Public"
6. Confirm

Now anyone can pull your image:
```powershell
docker pull ghcr.io/YOUR_USERNAME/ai-shopping-agent:latest
docker run -d -p 8501:8501 ghcr.io/YOUR_USERNAME/ai-shopping-agent:latest
```

## Useful Commands Reference

### Docker Commands
```powershell
# View running containers
docker ps

# View logs
docker logs -f ai-shopping-agent

# Stop container
docker stop ai-shopping-agent

# Remove container
docker rm ai-shopping-agent

# Remove image
docker rmi ai-shopping-agent:latest

# View all images
docker images
```

### Docker Compose Commands
```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose up -d --build
```

### Git Commands
```powershell
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull from GitHub
git pull

# View commit history
git log --oneline
```

## Troubleshooting

### Problem: Git command not found
**Solution:** Restart PowerShell terminal after installing Git

### Problem: Port 8501 already in use
**Solution:** 
1. Stop the process using port 8501, or
2. Change the port in `docker-compose.yml`:
   ```yaml
   ports:
     - "8502:8501"  # Use port 8502
   ```

### Problem: Docker daemon not running
**Solution:** Start Docker Desktop

### Problem: GitHub push requires authentication
**Solution:** 
1. Use GitHub Personal Access Token instead of password
2. Create token at: https://github.com/settings/tokens
3. Use token as password when prompted

### Problem: GitHub Actions not running
**Solution:**
1. Check if workflow file exists: `.github/workflows/docker-publish.yml`
2. Enable Actions in repository settings if disabled
3. Push to `main` or `master` branch

## Need More Help?

- 📖 Check [QUICKSTART.md](QUICKSTART.md) for quick reference
- 🐳 Check [DOCKER.md](DOCKER.md) for detailed Docker info
- 📝 Check [README.md](README.md) for project overview

---

Good luck! 🚀
