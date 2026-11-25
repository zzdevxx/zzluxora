@echo off
:: ==============================================================================
:: ZZLUXORA v10.0 - One-Click Stage Lighting Console Launcher (Windows 11)
:: ==============================================================================

cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONUNBUFFERED=1

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan di sistem Windows PATH!
    pause
    exit /b 1
)

echo ==================================================
echo [ZZLUXORA] v10.0.0 — Next-Gen Lighting Console
echo ==================================================
echo Memulai antarmuka konsol panggung...

python main.py %*
