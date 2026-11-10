@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   SmartPark Campus — Web Server Launcher            ║
echo ║   SRM Institute of Science and Technology, Trichy   ║
echo ╚══════════════════════════════════════════════════════╝
echo.

cd /d %~dp0

:: Check Java
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Java is not installed or not in PATH.
    echo Please install Java 11+ and try again.
    pause
    exit /b 1
)

:: Compile all Java sources
echo [1/3] Compiling Java sources...
mkdir bin 2>nul
dir /s /b src\*.java > %TEMP%\sp_sources.txt 2>nul
javac -J-Xss16m -J-Xmx512m -d bin -cp "lib\*" @%TEMP%\sp_sources.txt 2> %TEMP%\sp_errors.txt
if %errorlevel% neq 0 (
    echo.
    echo !! Compilation FAILED. Errors:
    type %TEMP%\sp_errors.txt
    echo.
    pause
    exit /b 1
)
echo [1/3] Compilation OK!

:: Run DB fix to ensure clean zones and 30 slots
echo [2/3] Verifying database...
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -uroot -p1234 smartpark_db < database\master_fix.sql >nul 2>&1
echo [2/3] Database OK!

echo.
echo [3/3] Starting SmartPark API + Web Server on port 8080...
echo.
echo   Dashboard : http://localhost:8080
echo   API Root  : http://localhost:8080/api
echo.
echo   Login credentials:
echo     Student  : stud1 / password
echo     Faculty  : fac1  / password
echo     Security : sec1  / password
echo     Admin    : admin / admin
echo.
echo Press Ctrl+C to stop the server.
echo.

java -Dsmartpark.web.root=web -cp "bin;lib\*" WebApplication
pause
