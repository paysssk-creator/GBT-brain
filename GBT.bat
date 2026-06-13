@echo off
chcp 65001 >nul 2>nul
title GBT小土豆全能开发者
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window --window-size=1400,900 "%USERPROFILE%\.gbt\launcher.html"
exit /b 0