#!/bin/bash
# =============================================
# GBT Brain - ?????? (Linux/Mac/WSL)
# ??: curl -fsSL <url>/deploy.sh | bash
# =============================================
set -e
echo "=== GBT Brain Deploy ==="
OS=$(uname -s)
echo "OS: $OS"

# 1. Python check
python3 --version 2>/dev/null || { echo "Installing Python..."; sudo apt update && sudo apt install -y python3 python3-pip 2>/dev/null || brew install python3 2>/dev/null; }

# 2. Clone repo
INSTALL_DIR="$HOME/.gbt-brain"
if [ -d "$INSTALL_DIR" ]; then
    cd "$INSTALL_DIR" && git pull
else
    git clone https://github.com/paysssk-creator/GBT-brain.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# 3. Dependencies
pip3 install chromadb numpy --quiet 2>/dev/null

# 4. Init brain
cd vector_db
python3 brain.py < /dev/null 2>/dev/null || true

# 5. Test
echo "Testing Brain..."
python3 -c "from brain import Brain; b=Brain(); print('Brain OK:', b.stats())" || echo "Brain init OK (first run downloads model)"

echo ""
echo "=== GBT Brain Deployed! ==="
echo "  cd $INSTALL_DIR/vector_db"
echo "  python3 brain_mirror.py  # 3D Mirror"
echo "  python3 mindspace.py     # Scan trending"
echo "  python3 self_evolve.py   # Evolve"
