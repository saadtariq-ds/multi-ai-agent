# 🚀 WSL Installation Guide

## 🐧 Installing Ubuntu via WSL and Docker Engine Inside Ubuntu (on Windows)

### 🔧 Step 1: Enable WSL and Virtualization
Open PowerShell as Administrator and run:
```bash
wsl --install
```
If WSL is already installed, update it:
```bash
wsl --update
```
Reboot your system if prompted.

## 🛍️ Step 2: Install Ubuntu
1. Open Microsoft Store
2. Search for Ubuntu
3. Choose a version (e.g., Ubuntu 22.04 LTS)
4. Click Get or Install
5. Launch Ubuntu from Start Menu and set up username/password

## 🐳 Step 3: Install Docker Engine in Ubuntu (WSL)
Run the following commands in the Ubuntu terminal:
```bash
# 1. Update package index and install dependencies
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release -y

# 2. Add Docker’s official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 3. Set up the Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Install Docker Engine
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# 5. Add user to docker group (optional but recommended)
sudo usermod -aG docker $USER
```
🔁 Restart the Ubuntu terminal after running the above to apply group changes.

✅ You can now run Docker inside Ubuntu WSL:
```bash
docker --version
```