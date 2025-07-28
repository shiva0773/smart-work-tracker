@echo off
echo Setting up Real Windows Login Tracker Auto-Start...

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_PATH=pythonw.exe"
set "TRACKER_SCRIPT=%SCRIPT_DIR%real_windows_login_tracker.py"

REM Create the startup command
set "STARTUP_CMD=%PYTHON_PATH% %TRACKER_SCRIPT%"

REM Add to Windows startup registry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "RealWindowsLoginTracker" /t REG_SZ /d "%STARTUP_CMD%" /f

echo.
echo ✅ Real Windows login tracker configured!
echo 🪟 Detects actual Windows login time using Event Log
echo ⏰ Login time = When you actually logged into Windows
echo ⏰ Logout time = 9 hours from Windows login time
echo.
echo To remove auto-start later, run: reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "RealWindowsLoginTracker" /f
echo.
pause 