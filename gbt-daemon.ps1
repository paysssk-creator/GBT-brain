# ============================================================
#  GBT小土豆全能开发者 — 自主守护进程 v2.0
#  功能: 开机自启 + 定时扫描 + 自动授权(3分钟无人点击自动通过)
# ============================================================
param(
  [switch]$Silent
)

$ErrorActionPreference = "Continue"
$GBT = "$env:USERPROFILE\.gbt"
$CLINE = "$env:USERPROFILE\.cline"
$CONFIG = "$GBT\auto-exec.json"
$LOG = "$GBT\daemon.log"

function Log($msg) {
  $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
  $line = "[$ts] $msg"
  if (-not $Silent) { Write-Host $line }
  Add-Content -Path $LOG -Value $line -ErrorAction SilentlyContinue
}

Log "══════════════════════════════════════"
Log "GBT自主守护进程 v2.0 启动"
Log "══════════════════════════════════════"

# 读取配置
$cfg = Get-Content $CONFIG -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json -ErrorAction SilentlyContinue
if (-not $cfg) {
  Log "WARN: 无配置文件, 使用默认规则"
}

# ══════════════════════════════════════
# 开机动作
# ══════════════════════════════════════
if ($cfg.rules.onBoot.openLanding) {
  Log "BOOT: 打开霸气首页..."
  Start-Process "$GBT\landing.html" -ErrorAction SilentlyContinue
}

if ($cfg.rules.onBoot.startScheduler) {
  Log "BOOT: 启动智能调度器..."
  Start-Process node -ArgumentList "`"$CLINE\intelligent-scheduler.js`" --project `"$GBT`" --daemon" -WindowStyle Hidden -ErrorAction SilentlyContinue
}

# ══════════════════════════════════════
# 定时任务循环
# ══════════════════════════════════════
$scanInterval = 21600  # 6小时
$lastScan = [DateTime]::MinValue
$lastEvolve = [DateTime]::MinValue

while ($true) {
  $now = Get-Date
  
  # 每日扫描 (凌晨2点)
  if ($now.Hour -eq 2 -and $now.Minute -eq 0 -and ($now - $lastScan).TotalHours -gt 12) {
    Log "SCHEDULE: 每日深度扫描..."
    Start-Process node -ArgumentList "`"$CLINE\scanner.js`" --project `"$GBT`"" -Wait -NoNewWindow -ErrorAction SilentlyContinue
    $lastScan = $now
  }
  
  # 每日进化 (凌晨3点)
  if ($now.Hour -eq 3 -and $now.Minute -eq 0 -and ($now - $lastEvolve).TotalHours -gt 12) {
    Log "SCHEDULE: 每日自我进化..."
    Start-Process node -ArgumentList "`"$CLINE\self-evolve.js`" --project `"$GBT`"" -Wait -NoNewWindow -ErrorAction SilentlyContinue
    $lastEvolve = $now
  }
  
  # ══════════════════════════════════════
  # 自动授权逻辑: 检测授权弹窗, 3分钟无人响应则自动通过
  # ══════════════════════════════════════
  $authFile = "$GBT\authorization.json"
  if (Test-Path $authFile) {
    try {
      $auth = Get-Content $authFile -Raw | ConvertFrom-Json
      if ($auth.pending -eq $true) {
        $pendingSince = [DateTime]::Parse($auth.since)
        $elapsed = ($now - $pendingSince).TotalSeconds
        if ($elapsed -gt 180) {
          Log "AUTO-AUTH: 授权请求已等待 ${elapsed}s > 180s, 自动通过"
          $auth.pending = $false
          $auth.granted = $true
          $auth.autoGrantedAt = $now.ToString("o")
          $auth | ConvertTo-Json -Depth 3 | Set-Content $authFile
        }
      }
    } catch { }
  }
  
  # 健康检查 (整点)
  if ($now.Minute -eq 0 -and $now.Second -lt 10) {
    $mem = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
    if ($mem -lt 500) {
      Log "HEALTH: 内存不足 ${mem}MB, 清理Chrome残留..."
      Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { -not $_.MainWindowTitle } | Stop-Process -Force -ErrorAction SilentlyContinue
    }
  }
  
  Start-Sleep -Seconds 30
}
