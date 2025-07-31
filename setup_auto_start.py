#!/usr/bin/env python3
"""
Auto-Start Setup for AI Work Tracker
Sets up the tracker to start automatically when Windows boots
"""

import os
import sys
import winreg
import subprocess
import importlib
from pathlib import Path

APP_NAME_LOGIN = "AIWorkTracker"
APP_NAME_UNLOCK = "AIWorkTrackerShowOnUnlock"

def setup_auto_start():
    """Set up auto-start for the AI Work Tracker"""
    print("🚀 Setting up Auto-Start for AI Work Tracker...")
    print("=" * 50)
    
    # Get the current directory and script path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(current_dir, "main.py")
    
    # Check if the tracker script exists
    if not os.path.exists(main_script):
        print(f"❌ Error: {os.path.basename(main_script)} not found!")
        return False
    
    # Get Python executable path
    python_exe = sys.executable
    pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")

    # Prefer pythonw.exe for a silent, no-console startup, but fall back if it doesn't exist
    if not os.path.exists(pythonw_exe):
        print("⚠️ 'pythonw.exe' not found, falling back to 'python.exe'. A console window may flash on startup.")
        startup_executable = python_exe
    else:
        startup_executable = pythonw_exe
    
    # Create the startup command
    startup_cmd = f'"{startup_executable}" "{main_script}"'
    
    try:
        # Open the Windows Registry key for current user startup
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        
        # Set the registry value
        winreg.SetValueEx(key, APP_NAME_LOGIN, 0, winreg.REG_SZ, startup_cmd)
        winreg.CloseKey(key)
        
        print("✅ Auto-start setup successful!")
        print(f"📁 Main script: {main_script}")
        print(f"🐍 Python executable: {python_exe}")
        print(f"🔧 Startup command: {startup_cmd}")
        print("\n🎯 What happens now:")
        print("   • The tracker will start automatically when you log into Windows")
        print("   • It will auto-capture your login time or ask you to set it manually")
        print("   • Your work hours will be tracked from that moment")
        print("   • The tracker will run in the background and show your progress")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up auto-start: {e}")
        return False

def remove_auto_start():
    """Remove auto-start for the AI Work Tracker"""
    print("🗑️ Removing Auto-Start for AI Work Tracker...")
    print("=" * 50)
    
    try:
        # Open the Windows Registry key for current user startup
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        
        # Remove the registry value
        winreg.DeleteValue(key, APP_NAME_LOGIN)
        winreg.CloseKey(key)
        
        print("✅ Auto-start removed successfully!")
        print("📝 The tracker will no longer start automatically")
        
        return True
        
    except Exception as e:
        print(f"❌ Error removing auto-start: {e}")
        return False

def check_auto_start_status():
    """Check if auto-start is currently set up"""
    print("🔍 Checking Auto-Start Status...")
    print("=" * 50)
    
    try:
        # Open the Windows Registry key for current user startup
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        
        # Try to read the value
        try:
            value, _ = winreg.QueryValueEx(key, APP_NAME_LOGIN)
            winreg.CloseKey(key)
            
            print("✅ Auto-start is currently ENABLED")
            print(f"🔧 Command: {value}")
            return True
            
        except FileNotFoundError:
            winreg.CloseKey(key)
            print("❌ Auto-start is currently DISABLED")
            return False
            
    except Exception as e:
        print(f"❌ Error checking auto-start status: {e}")
        return False

def setup_unlock_trigger():
    """Sets up a task to show the tracker window on workstation unlock."""
    print("\n🔧 Setting up 'Show on Unlock' trigger via Task Scheduler...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(current_dir, "main.py")
    
    pythonw_exe = sys.executable.replace("python.exe", "pythonw.exe")
    if not os.path.exists(pythonw_exe):
        pythonw_exe = sys.executable

    # The command includes a flag to tell the app it's an unlock trigger
    command = f'"{pythonw_exe}" "{main_script}" --show-on-unlock'
    
    # schtasks command to create the task
    create_cmd = [
        'schtasks', '/Create', '/TN', APP_NAME_UNLOCK, '/TR', command, '/SC', 'ONUNLOCK', '/F'
    ]
    
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        result = subprocess.run(create_cmd, check=True, capture_output=True, text=True, startupinfo=startupinfo)
        print(f"✅ Success: Task '{APP_NAME_UNLOCK}' created.")
        print("   The tracker window will now appear each time you unlock your computer.")
        return True
    except FileNotFoundError:
        print("❌ Error: 'schtasks.exe' not found. This feature is only available on Windows.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating scheduled task: {e.stderr}")
        return False

def remove_unlock_trigger():
    """Removes the 'Show on Unlock' scheduled task."""
    print("\n🗑️ Removing 'Show on Unlock' trigger...")
    
    delete_cmd = ['schtasks', '/Delete', '/TN', APP_NAME_UNLOCK, '/F']
    
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        result = subprocess.run(delete_cmd, check=True, capture_output=True, text=True, startupinfo=startupinfo)
        print(f"✅ Success: Task '{APP_NAME_UNLOCK}' removed.")
        return True
    except FileNotFoundError:
        print("❌ Error: 'schtasks.exe' not found.")
        return False
    except subprocess.CalledProcessError as e:
        # It's common for this to fail if the task doesn't exist, which is fine.
        if "ERROR: The specified task name" in e.stderr:
            print(f"ℹ️  Info: Task '{APP_NAME_UNLOCK}' was not found (already removed).")
            return True
        else:
            print(f"❌ Error removing scheduled task: {e.stderr}")
            return False

def check_unlock_trigger_status():
    """Checks if the 'Show on Unlock' task exists."""
    query_cmd = ['schtasks', '/Query', '/TN', APP_NAME_UNLOCK]
    try:
        subprocess.run(query_cmd, check=True, capture_output=True, text=True, startupinfo=subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW))
        print(f"✅ 'Show on Unlock' trigger is currently ENABLED.")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ 'Show on Unlock' trigger is currently DISABLED.")
        return False

def check_dependencies():
    """Checks if all required packages are installed."""
    print("\n🩺 Checking for required packages...")
    # Names used for importing can be different from pip package names
    required_imports = {
        "requests": "requests",
        "psutil": "psutil",
        "pystray": "pystray",
        "Pillow": "PIL.Image",
        "pywin32": "win32gui"
    }
    missing = []
    for pkg, mod in required_imports.items():
        try:
            importlib.import_module(mod)
            print(f"  ✅ {pkg} is installed.")
        except ImportError:
            missing.append(pkg)
            print(f"  ❌ {pkg} is MISSING.")
    
    if missing:
        print("\n⚠️ Please install missing packages by running:\n   pip install -r requirements.txt")
        return False
    
    print("👍 All dependencies are present.")
    return True

def create_batch_file():
    """Create a batch file for easier management"""
    print("📝 Creating batch file for easy management...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    batch_file = os.path.join(current_dir, "manage_tracker.bat")
    
    batch_content = f"""@echo off
echo AI Work Tracker Management
echo =========================
echo.
echo 1. Start Tracker Now
echo 2. Setup Auto-Start
echo 3. Remove Auto-Start
echo 4. Check Auto-Start Status
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting tracker...
    python "{os.path.join(current_dir, "main.py")}"
) else if "%choice%"=="2" (
    echo Setting up auto-start...
    python "{os.path.join(current_dir, "setup_auto_start.py")}" --setup
) else if "%choice%"=="3" (
    echo Removing auto-start...
    python "{os.path.join(current_dir, "setup_auto_start.py")}" --remove
) else if "%choice%"=="4" (
    echo Checking auto-start status...
    python "{os.path.join(current_dir, "setup_auto_start.py")}" --status
) else if "%choice%"=="5" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice!
)
echo.
pause
"""
    
    try:
        with open(batch_file, 'w') as f:
            f.write(batch_content)
        print(f"✅ Batch file created: {batch_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating batch file: {e}")
        return False

def main():
    """Main function to provide an interactive management menu."""
    while True:
        print("\n" + "=" * 50)
        print("🤖 AI Work Tracker Management Menu")
        print("=" * 50)

        # Check current status of both triggers
        print("\n--- Current Status ---")
        check_auto_start_status()
        check_unlock_trigger_status()
        print("----------------------\n")

        print("--- Options ---")
        print("1. Enable 'Start on Login'")
        print("2. Disable 'Start on Login'")
        print("3. Enable 'Show on Unlock'")
        print("4. Disable 'Show on Unlock'")
        print("5. Check Dependencies")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            setup_auto_start()
        elif choice == '2':
            remove_auto_start()
        elif choice == '3':
            setup_unlock_trigger()
        elif choice == '4':
            remove_unlock_trigger()
        elif choice == '5':
            check_dependencies()
        elif choice == '6':
            print("\nGoodbye! 👋")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number from 1 to 6.")
        
        input("\nPress Enter to return to the menu...")
        # Clear screen for better readability (optional, works on Windows/Linux)
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main() 