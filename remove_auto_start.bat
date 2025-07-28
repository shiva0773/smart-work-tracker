@echo off
echo Removing Auto-Start Work Tracker...

REM Remove from Windows startup registry
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "AutoWorkTracker" /f

echo.
echo ✅ Auto-start removed!
echo 📝 The tracker will no longer start automatically
echo.
pause 