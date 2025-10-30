# 🚀 Quick Start Guide

This guide will help you get started with the AI Shopping Agent using Docker.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- [Git](https://git-scm.com/download/win) installed
- GitHub account (for pushing to GitHub)

## Step 1: Build Docker Image

### Option A: Using PowerShell Script (Recommended)
```powershell
.\build-docker.ps1
```

### Option B: Using Docker Compose
```powershell
docker-compose up -d
```

### Option C: Using Docker CLI
```powershell
docker build -t ai-shopping-agent:latest .
docker run -d -p 8501:8501 --name ai-shopping-agent ai-shopping-agent:latest
```

## Step 2: Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

## Step 3: Push to GitHub

### Option A: Using PowerShell Script (Recommended)
```powershell
.\push-to-github.ps1
```

### Option B: Manual Steps

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name it `ai-shopping-agent`
   - Don't initialize with README

2. **Initialize and push**
```powershell
# If not already initialized
git init

# Add all files
git add .

# Commit changes
git commit -m "Add Docker support and deployment"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-shopping-agent.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Automatic Docker Build

Once pushed to GitHub:
1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. You'll see the "Docker Build and Push" workflow running
4. Wait for it to complete (usually 5-10 minutes)
5. Your Docker image will be available at `ghcr.io/YOUR_USERNAME/ai-shopping-agent:latest`

## Step 5: Pull and Run from GitHub Container Registry

After the GitHub Action completes:

```powershell
# Pull the image
docker pull ghcr.io/YOUR_USERNAME/ai-shopping-agent:latest

# Run the container
docker run -d -p 8501:8501 ghcr.io/YOUR_USERNAME/ai-shopping-agent:latest
```

## Useful Commands

### View Logs
```powershell
docker-compose logs -f
# or
docker logs -f ai-shopping-agent
```

### Stop the Application
```powershell
docker-compose down
# or
docker stop ai-shopping-agent
```

### Restart the Application
```powershell
docker-compose restart
# or
docker restart ai-shopping-agent
```

### Rebuild the Image
```powershell
docker-compose up -d --build
```

### Remove Everything
```powershell
docker-compose down
docker rmi ai-shopping-agent:latest
```

## Troubleshooting

### Port 8501 already in use
Edit `docker-compose.yml` and change the port:
```yaml
ports:
  - "8502:8501"  # Use 8502 instead
```

### Docker daemon not running
Make sure Docker Desktop is started.

### Permission denied errors
Make sure Docker Desktop has proper permissions and is running.

### GitHub Actions not running
1. Check if the workflow file exists: `.github/workflows/docker-publish.yml`
2. Make sure you pushed to the `main` or `master` branch
3. Check repository settings → Actions → Enable workflows

## Need Help?

- Check [DOCKER.md](DOCKER.md) for detailed Docker documentation
- Check logs: `docker-compose logs -f`
- Open an issue on GitHub

---

Happy coding! 🎉
