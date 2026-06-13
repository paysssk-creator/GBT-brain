@echo off
REM ============================================
REM GBT Daily Self-Evolve - ??????
REM ??: ???? ? ??Windows????
REM ============================================
cd /d C:\Users\ADMIN\.gbt\vector_db
echo [%date% %time%] GBT Self-Evolve Starting...

set PYTHONIOENCODING=utf-8
C:\Users\ADMIN\AppData\Local\Programs\Python\Python312\python.exe self_evolve.py > evolve_log_%date:~0,4%%date:~5,2%%date:~8,2%.txt 2>&1

echo Done! Check vector_db/evolve_log_*.txt
exit /b 0
