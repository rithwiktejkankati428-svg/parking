@echo off
echo Compiling SmartPark Campus...
mkdir bin 2>nul
javac -d bin -cp "lib/*" -sourcepath src src\Application.java
if %errorlevel% neq 0 (
    echo Compilation Failed!
) else (
    echo Compilation Successful!
)
pause
