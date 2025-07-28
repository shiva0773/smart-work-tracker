@echo off
echo Setting up Daily Login Tracker Auto-Start...

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_PATH=pythonw.exe"
set "TRACKER_SCRIPT=%SCRIPT_DIR%daily_login_tracker.py"

REM Create the startup command
set "STARTUP_CMD=%PYTHON_PATH% %TRACKER_SCRIPT%"

REM Add to Windows startup registry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DailyLoginTracker" /t REG_SZ /d "%STARTUP_CMD%" /f

echo.
echo ✅ Daily login tracker configured!
echo 📅 Captures first login time of each day
echo ⏰ Login time = First time you start the tracker each day
echo ⏰ Logout time = 9 hours from login time
echo.
echo To remove auto-start later, run: reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DailyLoginTracker" /f
echo.
pause 