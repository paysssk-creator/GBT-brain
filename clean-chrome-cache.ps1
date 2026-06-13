# clean-chrome-cache.ps1
# 只清Chrome缓存，不杀进程，不动用户浏览器窗口
$cacheRoot = "$env:LOCALAPPDATA\Google\Chrome\User Data"
if (-not (Test-Path $cacheRoot)) {
    Write-Host "no-chrome-cache-found"
    exit 0
}

$cleaned = 0
Get-ChildItem -Path $cacheRoot -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $cachePath = Join-Path $_.FullName "Cache"
    $codeCachePath = Join-Path $_.FullName "Code Cache"
    $gpucachePath = Join-Path $_.FullName "GPUCache"
    
    foreach ($p in @($cachePath, $codeCachePath, $gpucachePath)) {
        if (Test-Path $p) {
            Remove-Item -Path $p -Recurse -Force -ErrorAction SilentlyContinue
            $cleaned++
        }
    }
}

Write-Host "chrome-cache-cleaned:$cleaned"
