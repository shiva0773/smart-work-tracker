@echo off
echo Setting up System Startup Work Tracker...

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_PATH=pythonw.exe"
set "TRACKER_SCRIPT=%SCRIPT_DIR%system_startup_tracker.py"

REM Create the startup command
set "STARTUP_CMD=%PYTHON_PATH% %TRACKER_SCRIPT%"

REM Add to Windows startup registry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemStartupTracker" /t REG_SZ /d "%STARTUP_CMD%" /f

echo.
echo ✅ System startup tracker configured!
echo 🖥️ The tracker will detect actual system boot time
echo ⏰ Login time = When you physically turn on your laptop
echo ⏰ Logout time = 9 hours from system startup
echo.
echo To remove auto-start later, run: reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemStartupTracker" /f
echo.
pause 