@echo off
chcp 65001 >nul 2>nul
cd /d %USERPROFILE%\.gbt\vector_db 2>nul
if not exist launch.py (echo GBT not found && exit /b 1)
set PYTHONIOENCODING=utf-8
(where python 2>nul || where python3 2>nul) >%temp%\gbt_py.txt
set /p PY=<%temp%\gbt_py.txt
del %temp%\gbt_py.txt 2>nul
%PY% launch.py %*
