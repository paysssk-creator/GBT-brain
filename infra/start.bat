@echo off
echo === GBT Database Cluster ===
echo Starting PostgreSQL + pgvector (5432)
echo Starting MySQL 8 (3306)
echo Starting Redis 7 (6379)
echo.
cd /d C:\Users\ADMIN\.gbt\infra
docker compose up -d
echo.
echo Waiting for PostgreSQL...
timeout /t 10 /nobreak >nul
echo.
echo === Status ===
docker compose ps
echo.
echo === Connection Strings ===
echo PostgreSQL:  postgresql://gbt:gbt2024@localhost:5432/gbt_brain
echo MySQL:       mysql://root:gbt2024@localhost:3306/gbt_halo
echo Redis:       redis://localhost:6379
echo.
echo Done! All databases running.
