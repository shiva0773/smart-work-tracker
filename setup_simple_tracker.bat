@echo off
echo Setting up Simple Work Tracker Auto-Start...

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_PATH=pythonw.exe"
set "TRACKER_SCRIPT=%SCRIPT_DIR%simple_startup_tracker.py"

REM Create the startup command
set "STARTUP_CMD=%PYTHON_PATH% %TRACKER_SCRIPT%"

REM Add to Windows startup registry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SimpleWorkTracker" /t REG_SZ /d "%STARTUP_CMD%" /f

echo.
echo ✅ Simple work tracker configured!
echo ⏰ Login time = When you start the tracker (current time)
echo ⏰ Logout time = 9 hours from login time
echo.
echo To remove auto-start later, run: reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SimpleWorkTracker" /f
echo.
pause 