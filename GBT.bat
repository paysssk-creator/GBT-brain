@echo off
chcp 65001 >nul 2>nul
title GBT小土豆全能开发者

cd /d "%USERPROFILE%\.gbt\vector_db" 2>nul
if not exist "launch.py" (
    echo [ERROR] GBT核心文件缺失: launch.py
    echo 请检查 %USERPROFILE%\.gbt\vector_db\ 目录
    pause
    exit /b 1
)

:: 查找 Python
set "PY="
for %%p in (python python3 py) do (
    where %%p >nul 2>nul
    if !errorlevel! equ 0 (
        set "PY=%%p"
        goto :found_python
    )
)

:: 常见Python路径
for %%d in (
    "C:\Python312" "C:\Python311" "C:\Python310"
    "%LOCALAPPDATA%\Programs\Python\Python312"
    "%LOCALAPPDATA%\Programs\Python\Python311"
    "%APPDATA%\Python\Python312"
) do (
    if exist "%%~d\python.exe" (
        set "PY=%%~d\python.exe"
        goto :found_python
    )
)

echo [ERROR] 未找到 Python，请安装 Python 3.10+
echo 下载: https://www.python.org/downloads/
pause
exit /b 1

:found_python
set "PYTHONIOENCODING=utf-8"
echo [GBT] 正在启动...
"%PY%" launch.py %*
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] GBT启动失败 (错误码: %errorlevel%)
    echo 请检查Python环境和依赖是否完整
    pause
    exit /b %errorlevel%
)
exit /b 0