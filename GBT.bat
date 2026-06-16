@echo off
chcp 65001 >nul 2>nul
title GBT小土豆全能开发者
:: Smart Chrome detection - try multiple install paths
set "CHROME="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set "CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe"
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set "CHROME=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set "CHROME=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
if "%CHROME%"=="" if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" set "CHROME=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if "%CHROME%"=="" if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" set "CHROME=C:\Program Files\Microsoft\Edge\Application\msedge.exe"
if "%CHROME%"=="" (start "" "%USERPROFILE%\.gbt\launcher.html") else (start "" "%CHROME%" --new-window --window-size=1400,900 "%USERPROFILE%\.gbt\launcher.html")
exit /b 0