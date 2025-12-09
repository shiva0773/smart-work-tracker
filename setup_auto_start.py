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
import getpass
import tempfile
import ctypes
from pathlib import Path

APP_NAME_LOGIN = "AIWorkTracker"
APP_NAME_UNLOCK = "AIWorkTrackerShowOnUnlock"
APP_NAME_REPORT = "AIWorkTrackerDailyReport"

def setup_auto_start():
    """Set up auto-start for the AI Work Tracker"""
    print("🚀 Setting up Auto-Start for AI Work Tracker...")
    print("=" * 50)
    
    # Get the current directory and script path
    current_dir = Path(__file__).parent.resolve()
    main_script = current_dir / "main.py"
    
    # Check if the tracker script exists
    if not main_script.exists():
        print(f"❌ Error: '{main_script.name}' not found in {current_dir}")
        return False
    
    # Get Python executable path
    python_exe = Path(sys.executable)
    pythonw_exe = python_exe.with_name("pythonw.exe")

    # Prefer pythonw.exe for a silent, no-console startup, but fall back if it doesn't exist
    if not pythonw_exe.exists():
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
        print(f"🐍 Python executable: {startup_executable}")
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

    current_dir = Path(__file__).parent.resolve()
    main_script = current_dir / "main.py"

    pythonw_exe = Path(sys.executable).with_name("pythonw.exe")
    if not pythonw_exe.exists():
        pythonw_exe = Path(sys.executable)

    # Define the task using an XML template. This is the robust way to create
    # an event-based trigger for 'On workstation unlock' (SessionUnlock),
    # which is not possible with simple schtasks flags like /SC.
    task_xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.3" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Shows the AI Work Tracker when the user unlocks the workstation.</Description>
    <Author>{getpass.getuser()}</Author>
  </RegistrationInfo>
  <Triggers>
    <SessionStateChangeTrigger>
      <Enabled>true</Enabled>
      <StateChange>SessionUnlock</StateChange>
    </SessionStateChangeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>{getpass.getuser()}</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>"{pythonw_exe}"</Command>
      <Arguments>"{main_script}" --show-on-unlock</Arguments>
    </Exec>
  </Actions>
</Task>
"""
    # Use a temporary file to pass the XML to schtasks
    xml_file_path = Path(tempfile.gettempdir()) / f"{APP_NAME_UNLOCK}.xml"
    try:
        # Write the XML content with UTF-16 encoding, as required by schtasks
        xml_file_path.write_text(task_xml, encoding='utf-16')

        # schtasks command to create the task from the XML definition
        create_cmd = ['schtasks', '/Create', '/TN', APP_NAME_UNLOCK, '/XML', str(xml_file_path), '/F']

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(create_cmd, check=True, capture_output=True, text=True, startupinfo=startupinfo)
        print(f"✅ Success: Task '{APP_NAME_UNLOCK}' created.")
        print("   The tracker window will now appear each time you unlock your computer.")
        return True
    except FileNotFoundError:
        print("❌ Error: 'schtasks.exe' not found. This feature is only available on Windows.")
        return False
    except subprocess.CalledProcessError as e:
        # Provide a more helpful error message if the XML is malformed
        if "ERROR: The task XML is malformed" in e.stderr:
            print(f"❌ Error creating scheduled task: The generated task XML is invalid.\n   Details: {e.stderr}")
        else:
            print(f"❌ Error creating scheduled task: {e.stderr}")
        return False
    finally:
        if xml_file_path.exists():
            xml_file_path.unlink()

def remove_unlock_trigger():
    """Removes the 'Show on Unlock' scheduled task."""
    print("\n🗑️ Removing 'Show on Unlock' trigger...")
    
    delete_cmd = ['schtasks', '/Delete', '/TN', APP_NAME_UNLOCK, '/F']
    
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        subprocess.run(delete_cmd, check=True, capture_output=True, text=True, startupinfo=startupinfo)
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

def setup_daily_report_task():
    """Sets up a daily task to send the report at 11 PM."""
    print("\n🔧 Setting up 'Daily Report at 11 PM' task via Task Scheduler...")

    current_dir = Path(__file__).parent.resolve()
    report_script = current_dir / "run_report.py"

    if not report_script.exists():
        print(f"❌ Error: Report script '{report_script.name}' not found in {current_dir}")
        print("   Please ensure 'run_report.py' exists.")
        return False

    pythonw_exe = Path(sys.executable).with_name("pythonw.exe")
    if not pythonw_exe.exists():
        pythonw_exe = Path(sys.executable)

    command = f'"{pythonw_exe}" "{report_script}"'

    # schtasks command to create the task
    create_cmd = [
        'schtasks', '/Create', '/TN', APP_NAME_REPORT, '/TR', command,
        '/SC', 'DAILY', '/ST', '23:00', '/F'
    ]

    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.run(create_cmd, check=True, capture_output=True, text=True, startupinfo=startupinfo)
        print(f"✅ Success: Task '{APP_NAME_REPORT}' created.")
        print("   The daily report will now be sent automatically at 11 PM each day.")
        return True
    except FileNotFoundError:
        print("❌ Error: 'schtasks.exe' not found. This feature is only available on Windows.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating scheduled task: {e.stderr}")
        return False

def remove_daily_report_task():
    """Removes the 'Daily Report' scheduled task."""
    print("\n🗑️ Removing 'Daily Report' task...")

    delete_cmd = ['schtasks', '/Delete', '/TN', APP_NAME_REPORT, '/F']

    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.run(delete_cmd, check=True, capture_output=True, text=True, startupinfo=startupinfo)
        print(f"✅ Success: Task '{APP_NAME_REPORT}' removed.")
        return True
    except FileNotFoundError:
        print("❌ Error: 'schtasks.exe' not found.")
        return False
    except subprocess.CalledProcessError as e:
        if "ERROR: The specified task name" in e.stderr:
            print(f"ℹ️  Info: Task '{APP_NAME_REPORT}' was not found (already removed).")
            return True
        else:
            print(f"❌ Error removing scheduled task: {e.stderr}")
            return False

def check_daily_report_status():
    """Checks if the 'Daily Report' task exists."""
    query_cmd = ['schtasks', '/Query', '/TN', APP_NAME_REPORT]
    try:
        subprocess.run(query_cmd, check=True, capture_output=True, text=True, startupinfo=subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW))
        print(f"✅ 'Daily Report' task is currently ENABLED (runs at 11 PM).")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ 'Daily Report' task is currently DISABLED.")
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

def is_admin():
    """Checks if the script is running with administrative privileges on Windows."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    """Main function to provide an interactive management menu."""
    # On Windows, scheduled tasks and registry edits require admin rights.
    if os.name == 'nt' and not is_admin():
        print("\n" + "=" * 60)
        print("❌ ERROR: Administrative privileges are required.")
        print("   This script needs to modify system settings (Registry and Task Scheduler).")
        print("\n   How to fix:")
        print("   1. Close this window.")
        print("   2. Right-click on your terminal (e.g., Command Prompt, PowerShell).")
        print("   3. Select 'Run as administrator'.")
        print("   4. Navigate back to this directory and run the script again:")
        print(f"      cd {Path.cwd()}")
        print(f"      python {Path(__file__).name}")
        print("=" * 60)
        input("\nPress Enter to exit...")
        sys.exit(1)

    while True:
        print("\n" + "=" * 50)
        print("🤖 AI Work Tracker Management Menu")
        print("=" * 50)

        # Check current status of both triggers
        print("\n--- Current Status ---")
        check_auto_start_status()
        check_unlock_trigger_status()
        check_daily_report_status()
        print("----------------------\n")

        print("--- Login/Unlock Options ---")
        print("1. Enable 'Start on Login'")
        print("2. Disable 'Start on Login'")
        print("3. Enable 'Show on Unlock'")
        print("4. Disable 'Show on Unlock'")
        print("\n--- Report Options ---")
        print("5. Enable 'Daily Report at 11 PM'")
        print("6. Disable 'Daily Report at 11 PM'")
        print("\n--- Maintenance ---")
        print("7. Check Dependencies")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == '1':
            setup_auto_start()
        elif choice == '2':
            remove_auto_start()
        elif choice == '3':
            setup_unlock_trigger()
        elif choice == '4':
            remove_unlock_trigger()
        elif choice == '5':
            setup_daily_report_task()
        elif choice == '6':
            remove_daily_report_task()
        elif choice == '7':
            check_dependencies()
        elif choice == '8':
            print("\nGoodbye! 👋")
            break
        else:
            print(f"\n❌ Invalid choice. Please enter a number from 1 to 8.")
        
        input("\nPress Enter to return to the menu...")
        # Clear screen for better readability (optional, works on Windows/Linux)
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main() 