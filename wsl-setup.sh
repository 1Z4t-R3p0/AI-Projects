#!/bin/bash
set -e

# ====================================
#   AI-ChatBot Deployment (WSL/Linux)
# ====================================

REPO_URL="https://github.com/1Z4t-R3p0/AI-ChatBot.git"
PROJECT_DIR="$HOME/AI-ChatBot"

echo "===================================="
echo "   AI-ChatBot Setup & Deployment"
echo "===================================="

# 1. Install Git and standard dependencies
if ! command -v git >/dev/null 2>&1; then
    echo "Installing Git..."
    sudo apt-get update && sudo apt-get install -y git curl
fi

# 2. Install Docker if missing
if ! command -v docker >/dev/null 2>&1; then
    echo "Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker "$USER"
    echo "Docker installed! You may need to log out and back in for permissions to take effect."
fi

# Ensure Docker daemon is running
if ! sudo docker info >/dev/null 2>&1; then
    echo "Starting Docker daemon..."
    sudo service docker start || sudo dockerd &
    sleep 3
fi

# 3. Clone or Update Project
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Cloning project repository..."
    git clone "$REPO_URL" "$PROJECT_DIR"
else
    echo "Project exists at $PROJECT_DIR. Pulling latest changes..."
    cd "$PROJECT_DIR" || exit
    git pull
fi


# 4. Handle .env file (Ask user for API key if missing)
cd "$PROJECT_DIR" || exit
if [ ! -f ".env" ]; then
    echo "===================================="
    echo " OpenRouter API Key Required!"
    read -p "Please enter your OPENROUTER_API_KEY: " API_KEY
    echo "OPENROUTER_API_KEY=$API_KEY" > .env
fi

# 5. Run Docker Compose
echo "Starting AI-ChatBot Containers..."
sudo docker compose up -d --build || sudo docker-compose up -d --build

echo ""
echo "===================================="
echo " Deployment Complete!"
echo " Access Frontend at: http://localhost:8080"
echo " Access API at:      http://localhost:8001"
echo " Redis Analytics at port 6380"
echo "===================================="
