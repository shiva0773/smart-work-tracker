#!/usr/bin/env python3
"""
Auto-Start Setup for AI Work Tracker
Sets up the tracker to start automatically when Windows boots
"""

import os
import sys
import winreg
import subprocess
from pathlib import Path

def setup_auto_start():
    """Set up auto-start for the AI Work Tracker"""
    print("🚀 Setting up Auto-Start for AI Work Tracker...")
    print("=" * 50)
    
    # Get the current directory and script path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tracker_script = os.path.join(current_dir, "auto_capture_login_tracker.py")
    
    # Check if the tracker script exists
    if not os.path.exists(tracker_script):
        print("❌ Error: auto_capture_login_tracker.py not found!")
        return False
    
    # Get Python executable path
    python_exe = sys.executable
    if not python_exe:
        print("❌ Error: Could not find Python executable!")
        return False
    
    # Create the startup command
    startup_cmd = f'"{python_exe}" "{tracker_script}"'
    
    try:
        # Open the Windows Registry key for current user startup
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        
        # Set the registry value
        winreg.SetValueEx(key, "AIWorkTracker", 0, winreg.REG_SZ, startup_cmd)
        winreg.CloseKey(key)
        
        print("✅ Auto-start setup successful!")
        print(f"📁 Tracker script: {tracker_script}")
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
        winreg.DeleteValue(key, "AIWorkTracker")
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
            value, _ = winreg.QueryValueEx(key, "AIWorkTracker")
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
    python "{os.path.join(current_dir, "auto_capture_login_tracker.py")}"
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
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--setup":
            setup_auto_start()
        elif command == "--remove":
            remove_auto_start()
        elif command == "--status":
            check_auto_start_status()
        else:
            print("❌ Unknown command. Use --setup, --remove, or --status")
    else:
        # Interactive mode
        print("🤖 AI Work Tracker Auto-Start Setup")
        print("=" * 40)
        print()
        
        # Check current status
        is_enabled = check_auto_start_status()
        print()
        
        if is_enabled:
            print("Options:")
            print("1. Remove auto-start")
            print("2. Exit")
            choice = input("\nEnter your choice (1-2): ").strip()
            
            if choice == "1":
                remove_auto_start()
            else:
                print("Goodbye!")
        else:
            print("Options:")
            print("1. Setup auto-start")
            print("2. Create management batch file")
            print("3. Exit")
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                setup_auto_start()
            elif choice == "2":
                create_batch_file()
            else:
                print("Goodbye!")

if __name__ == "__main__":
    main() 