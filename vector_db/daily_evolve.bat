@echo off
chcp 65001 >nul
title GBTxiaotudou Brain - Daily Evolve

echo.
echo ╔══════════════════════════════════════════════╗
echo ║  GBT Daily Self-Evolve                      ║
echo ║  GBT小土豆全能开发者 - 每日自我进化            ║
echo ║  %date% %time%                         ║
echo ╚══════════════════════════════════════════════╝
echo.

cd /d C:\Users\ADMIN\.gbt\vector_db
set PYTHONIOENCODING=utf-8

C:\Users\ADMIN\AppData\Local\Programs\Python\Python312\python.exe -c "from splash import splash; splash('active', delay=0)" 2>nul
C:\Users\ADMIN\AppData\Local\Programs\Python\Python312\python.exe self_evolve.py > evolve_log_%date:~0,4%%date:~5,2%%date:~8,2%.txt 2>&1

echo.
echo [%time%] GBTxiaotudou Evolve Complete!
echo Log: evolve_log_%date:~0,4%%date:~5,2%%date:~8,2%.txt
exit /b 0
