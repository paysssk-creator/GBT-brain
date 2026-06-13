# =============================================
# GBT Brain - ???? (Windows PowerShell)
# ??: irm https://raw.git.../deploy.ps1 | iex
# =============================================
$ErrorActionPreference = "Stop"
Write-Host "=== GBT Brain Windows Deploy ===" -ForegroundColor Green

$INSTALL_DIR = "$env:USERPROFILE\.gbt-brain"

# 1. Check Python
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host "Python not found! Downloading from python.org..."
    $pyUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $pyInstaller = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest $pyUrl -OutFile $pyInstaller
    Start-Process $pyInstaller -Args "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item $pyInstaller
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")
}

# 2. Clone/update repo
if (Test-Path $INSTALL_DIR) {
    Write-Host "Updating existing install..."
    git -C $INSTALL_DIR pull
} else {
    Write-Host "Cloning GBT-brain..."
    git clone https://github.com/paysssk-creator/GBT-brain.git $INSTALL_DIR
}

Set-Location $INSTALL_DIR

# 3. Dependencies
Write-Host "Installing dependencies..."
pip install chromadb numpy --quiet 2>$null

# 4. Init & test
Set-Location $INSTALL_DIR\vector_db
python -c "from brain import Brain; b=Brain(); print('Brain OK:', b.stats())" 2>$null

# 5. Set scheduled task
$taskName = "GBT_Daily_Evolve"
$batPath = "$INSTALL_DIR\vector_db\daily_evolve.bat"
schtasks /create /tn $taskName /tr $batPath /sc daily /st 02:00 /f 2>$null

Write-Host ""
Write-Host "=== GBT Brain Deployed! ===" -ForegroundColor Green
Write-Host "  cd $INSTALL_DIR\vector_db"
Write-Host "  python brain_mirror.py    # 3D Mirror"
Write-Host "  python mindspace.py       # Scan trending"
Write-Host "  python self_evolve.py     # Evolve"
Write-Host ""
Write-Host "  Scheduled: daily 2:00 AM auto-evolve"
