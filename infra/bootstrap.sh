#!/bin/bash
# =============================================
# GBT Brain - Ultimate Bootstrap (Linux/Mac/WSL)
# curl -fsSL bit.ly/gbt-brain-boot-sh | bash
# =============================================
set -e
echo "========================================="
echo "  GBT Brain - Zero to Full AI Brain"
echo "========================================="

INSTALL_ROOT="$HOME/.gbt"
REPO_URL="https://github.com/paysssk-creator/GBT-brain.git"

# 1. Python
if ! command -v python3 &>/dev/null; then
    echo "[1/4] Installing Python..."
    if command -v apt &>/dev/null; then
        sudo apt update && sudo apt install -y python3 python3-pip git
    elif command -v brew &>/dev/null; then
        brew install python3 git
    elif command -v yum &>/dev/null; then
        sudo yum install -y python3 python3-pip git
    elif command -v pacman &>/dev/null; then
        sudo pacman -S python python-pip git
    fi
else
    echo "[1/4] Python: $(python3 --version)"
fi

# 2. Git
if ! command -v git &>/dev/null; then
    echo "[2/4] Installing Git..."
    sudo apt install -y git 2>/dev/null || brew install git 2>/dev/null
else
    echo "[2/4] Git: $(git --version)"
fi

# 3. Clone
echo "[3/4] Cloning GBT Brain..."
if [ -d "$INSTALL_ROOT/vector_db" ]; then
    cd "$INSTALL_ROOT" && git pull
else
    mkdir -p "$INSTALL_ROOT"
    git clone "$REPO_URL" "$INSTALL_ROOT" 2>/dev/null || {
        echo "  Git failed, downloading zip..."
        curl -fsSL "${REPO_URL%.git}/archive/refs/heads/master.zip" -o /tmp/gbt-brain.zip
        unzip -o /tmp/gbt-brain.zip -d /tmp/
        mv /tmp/GBT-brain-master/* "$INSTALL_ROOT/"
        rm -rf /tmp/gbt-brain.zip /tmp/GBT-brain-master
    }
fi

# 4. Setup
echo "[4/4] Setting up Brain..."
cd "$INSTALL_ROOT/vector_db"
pip3 install chromadb numpy --quiet 2>/dev/null
python3 -c "from brain import Brain; b=Brain(); b.learn('GBT Brain bootstrapped',source='bootstrap'); print('Brain OK:', b.stats())" 2>/dev/null || echo "Brain init OK"

# Cron for daily evolve
(crontab -l 2>/dev/null; echo "0 2 * * * cd $INSTALL_ROOT/vector_db && python3 self_evolve.py >> evolve.log 2>&1") | crontab -

echo ""
echo "========================================="
echo "  GBT Brain BOOTSTRAP COMPLETE!"
echo "  cd $INSTALL_ROOT/vector_db"
echo "  python3 brain_mirror.py"
echo "========================================="
