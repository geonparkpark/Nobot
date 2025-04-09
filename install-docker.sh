#!/bin/bash

set -e

echo "[+] Updating packages..."
sudo apt update

echo "[+] Installing dependencies..."
sudo apt install -y ca-certificates curl gnupg lsb-release

echo "[+] Adding Docker's official GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "[+] Setting up Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "[+] Updating package index..."
sudo apt update

echo "[+] Installing Docker Engine..."
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

echo "[+] Docker installation complete!"
docker --version
docker compose version