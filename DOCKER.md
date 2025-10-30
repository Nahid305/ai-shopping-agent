# 🐳 Docker Deployment Guide

This guide will help you build, run, and deploy the AI Shopping Agent using Docker.

## 📋 Prerequisites

- Docker installed on your system ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (usually comes with Docker Desktop)
- Git (for pushing to GitHub)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Build and run the application:**
```bash
docker-compose up -d
```

2. **Access the application:**
Open your browser and navigate to: `http://localhost:8501`

3. **Stop the application:**
```bash
docker-compose down
```

### Using Docker CLI

1. **Build the Docker image:**
```bash
docker build -t ai-shopping-agent .
```

2. **Run the container:**
```bash
docker run -d -p 8501:8501 --name ai-shopping-agent ai-shopping-agent
```

3. **Access the application:**
Open your browser and navigate to: `http://localhost:8501`

4. **Stop the container:**
```bash
docker stop ai-shopping-agent
docker rm ai-shopping-agent
```

## 🔧 Advanced Usage

### View Logs

**Docker Compose:**
```bash
docker-compose logs -f
```

**Docker CLI:**
```bash
docker logs -f ai-shopping-agent
```

### Rebuild the Image

**Docker Compose:**
```bash
docker-compose up -d --build
```

**Docker CLI:**
```bash
docker build -t ai-shopping-agent . --no-cache
docker stop ai-shopping-agent
docker rm ai-shopping-agent
docker run -d -p 8501:8501 --name ai-shopping-agent ai-shopping-agent
```

### Run in Development Mode

To mount your local code for live updates:
```bash
docker-compose up -d
```

The `docker-compose.yml` already includes volume mounting for development.

## 🌐 Pushing to GitHub

### 1. Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit with Docker support"
```

### 2. Create a GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Don't initialize with README (your project already has one)

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-shopping-agent.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## 📦 GitHub Container Registry (GHCR)

This project includes a GitHub Actions workflow that automatically builds and pushes Docker images to GitHub Container Registry.

### Automatic Build

Once you push to GitHub, the workflow will:
1. Build your Docker image
2. Push it to `ghcr.io/YOUR_USERNAME/ai-shopping-agent`
3. Tag it with `latest` and the commit SHA

### Pull the Image from GHCR

```bash
docker pull ghcr.io/YOUR_USERNAME/ai-shopping-agent:latest
docker run -d -p 8501:8501 ghcr.io/YOUR_USERNAME/ai-shopping-agent:latest
```

### Make Your Image Public

1. Go to your GitHub profile → Packages
2. Select your package
3. Click "Package settings"
4. Scroll down and click "Change visibility"
5. Select "Public"

## 🔍 Troubleshooting

### Port Already in Use

If port 8501 is already in use, change it in `docker-compose.yml`:
```yaml
ports:
  - "8502:8501"  # Use port 8502 instead
```

### Chrome/Selenium Issues

The Dockerfile includes Chromium and ChromeDriver. If you encounter issues:
- Ensure the container has enough memory (at least 2GB)
- Check logs: `docker-compose logs -f`

### Permission Issues

On Linux, you might need to run Docker commands with `sudo` or add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```

Then log out and back in.

## 📊 Environment Variables

You can customize the application using environment variables in `docker-compose.yml`:

```yaml
environment:
  - STREAMLIT_SERVER_PORT=8501
  - STREAMLIT_SERVER_ADDRESS=0.0.0.0
  - STREAMLIT_SERVER_HEADLESS=true
  - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 🛡️ Security Notes

- The Docker image runs as a non-root user for security
- Chrome runs in headless mode with sandbox disabled (required for Docker)
- No sensitive data is stored in the image
- Consider using secrets management for production deployments

## 📈 Production Deployment

For production deployments:

1. **Remove volume mounting** from `docker-compose.yml`
2. **Use specific image tags** instead of `latest`
3. **Set up reverse proxy** (nginx/traefik) with SSL
4. **Configure resource limits** in docker-compose.yml:

```yaml
services:
  ai-shopping-agent:
    # ... other settings ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## 🎯 Useful Commands

```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove all unused Docker resources
docker system prune -a

# Check container resource usage
docker stats ai-shopping-agent

# Execute commands inside the container
docker exec -it ai-shopping-agent bash

# Restart the container
docker-compose restart
```

## 📞 Support

If you encounter any issues:
1. Check the logs: `docker-compose logs -f`
2. Verify your Docker installation: `docker --version`
3. Ensure ports are not in use: `netstat -an | grep 8501`
4. Open an issue on GitHub

---

Happy Docker-ing! 🐳✨
