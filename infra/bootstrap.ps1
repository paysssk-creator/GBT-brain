# =============================================
# GBT Brain - ULTIMATE BOOTSTRAP
# ??Win??, ????, ??????
# irm bit.ly/gbt-brain-boot | iex
# =============================================
param(
    [switch]$SkipPython,
    [switch]$SkipGit,
    [switch]$DryRun
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

Write-Host @"
  ========================================
    GBT Brain - Ultimate Bootstrap
    Zero to Full AI Brain in One Command
  ========================================
"@ -ForegroundColor Cyan

$INSTALL_ROOT = "$env:USERPROFILE\.gbt"
$REPO_URL = "https://github.com/paysssk-creator/GBT-brain.git"

# Step 0: Check prerequisites
function Test-Command($cmd) {
    return [bool](Get-Command $cmd -ErrorAction SilentlyContinue)
}

# Step 1: Install Python if needed
if (-not $SkipPython -and -not (Test-Command python)) {
    Write-Host "[1/4] Installing Python 3.12..." -ForegroundColor Yellow
    $pyUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $pyExe = "$env:TEMP\py312.exe"
    if (-not $DryRun) {
        Invoke-WebRequest $pyUrl -OutFile $pyExe
        Start-Process $pyExe -Args "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait
        Remove-Item $pyExe
        $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
    }
    Write-Host "  Python OK" -ForegroundColor Green
} else {
    Write-Host "[1/4] Python found: $(python --version 2>&1)" -ForegroundColor Green
}

# Step 2: Install Git if needed
if (-not $SkipGit -and -not (Test-Command git)) {
    Write-Host "[2/4] Installing Git..." -ForegroundColor Yellow
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitExe = "$env:TEMP\git.exe"
    if (-not $DryRun) {
        Invoke-WebRequest $gitUrl -OutFile $gitExe
        Start-Process $gitExe -Args "/VERYSILENT /NORESTART" -Wait
        Remove-Item $gitExe
        $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine")
    }
    Write-Host "  Git OK" -ForegroundColor Green
} else {
    Write-Host "[2/4] Git found: $(git --version 2>&1)" -ForegroundColor Green
}

# Step 3: Clone brain
Write-Host "[3/4] Cloning GBT Brain..." -ForegroundColor Yellow
if (-not $DryRun) {
    if (Test-Path "$INSTALL_ROOT\vector_db") {
        git -C $INSTALL_ROOT pull 2>$null
        Write-Host "  Updated existing install" -ForegroundColor Green
    } else {
        New-Item -ItemType Directory -Force $INSTALL_ROOT | Out-Null
        git clone $REPO_URL $INSTALL_ROOT 2>$null
        if (-not $?) {
            Write-Host "  Git clone failed, downloading zip..." -ForegroundColor Yellow
            $zipUrl = "https://github.com/paysssk-creator/GBT-brain/archive/refs/heads/master.zip"
            $zipFile = "$env:TEMP\gbt-brain.zip"
            Invoke-WebRequest $zipUrl -OutFile $zipFile
            Expand-Archive $zipFile -DestinationPath $INSTALL_ROOT -Force
            Remove-Item $zipFile
        }
        Write-Host "  Cloned OK" -ForegroundColor Green
    }
}

# Step 4: Install Python deps + init Brain
Write-Host "[4/4] Setting up Brain..." -ForegroundColor Yellow
if (-not $DryRun) {
    pip install chromadb numpy --quiet 2>$null
    Set-Location "$INSTALL_ROOT\vector_db"
    python -c "from brain import Brain; b=Brain(); b.learn('GBT Brain bootstrapped successfully', source='bootstrap'); print('Brain OK:', b.stats())" 2>$null
    
    # Schedule daily evolve
    $batPath = "$INSTALL_ROOT\vector_db\daily_evolve.bat"
    schtasks /create /tn "GBT_Daily_Evolve" /tr $batPath /sc daily /st 02:00 /f 2>$null
}

Write-Host @"

  ==========================================
    GBT Brain BOOTSTRAP COMPLETE!
  ==========================================
    Location: $INSTALL_ROOT
    Daily Evolve: 2:00 AM auto

    Quick Start:
      cd $INSTALL_ROOT\vector_db
      python mindspace.py       # Scan trending
      python brain_mirror.py    # 3D Mirror
      python self_evolve.py     # Evolve
  ==========================================
"@ -ForegroundColor Green
