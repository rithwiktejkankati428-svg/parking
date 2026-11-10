@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   SmartPark Campus — Desktop App Launcher           ║
echo ╚══════════════════════════════════════════════════════╝
echo.

cd /d %~dp0

echo [1/2] Compiling Java sources...
mkdir bin 2>nul
dir /s /b src\*.java > %TEMP%\sp_sources.txt 2>nul
javac -J-Xss16m -J-Xmx512m -d bin -cp "lib\*" @%TEMP%\sp_sources.txt 2> %TEMP%\sp_errors.txt
if %errorlevel% neq 0 (
    echo Compilation FAILED:
    type %TEMP%\sp_errors.txt
    pause
    exit /b 1
)
echo [1/2] OK!

echo [2/2] Starting SmartPark Desktop App...
java -Xss16m -Xmx512m -cp "bin;lib\*" Application
pause

