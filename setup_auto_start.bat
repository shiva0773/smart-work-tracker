@echo off
echo Setting up Auto-Start Work Tracker...

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_PATH=pythonw.exe"
set "TRACKER_SCRIPT=%SCRIPT_DIR%auto_start_tracker.py"

REM Create the startup command
set "STARTUP_CMD=%PYTHON_PATH% %TRACKER_SCRIPT%"

REM Add to Windows startup registry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "AutoWorkTracker" /t REG_SZ /d "%STARTUP_CMD%" /f

echo.
echo ✅ Auto-start setup complete!
echo 📝 The tracker will now start automatically when you log in to Windows
echo 🕒 Login time will be when you turn on your laptop
echo ⏰ Logout time will be 9 hours from login time
echo.
echo To remove auto-start later, run: reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "AutoWorkTracker" /f
echo.
pause 