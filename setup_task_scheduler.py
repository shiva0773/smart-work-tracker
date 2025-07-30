#!/usr/bin/env python3
"""
Task Scheduler Setup for AI Work Tracker
Sets up the tracker to start automatically using Windows Task Scheduler
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_task_scheduler():
    """Set up Task Scheduler for the AI Work Tracker"""
    print("🚀 Setting up Task Scheduler for AI Work Tracker...")
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
    
    # Create the command
    cmd = f'"{python_exe}" "{tracker_script}"'
    
    try:
        # Create Task Scheduler command
        task_name = "AIWorkTracker"
        task_description = "AI Work Tracker - Starts automatically on user login"
        
        # schtasks command to create the task
        schtasks_cmd = [
            'schtasks', '/create', '/tn', task_name,
            '/tr', cmd,
            '/sc', 'logon',
            '/ru', os.getenv('USERNAME'),
            '/rl', 'highest',
            '/f'  # Force overwrite if exists
        ]
        
        print(f"🔧 Creating Task Scheduler task: {task_name}")
        print(f"📁 Tracker script: {tracker_script}")
        print(f"🐍 Python executable: {python_exe}")
        print(f"🔧 Command: {cmd}")
        
        # Execute the schtasks command
        result = subprocess.run(schtasks_cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print("✅ Task Scheduler setup successful!")
            print("\n🎯 What happens now:")
            print("   • The tracker will start automatically when you log into Windows")
            print("   • It will auto-capture your login time or ask you to set it manually")
            print("   • Your work hours will be tracked from that moment")
            print("   • The tracker will run in the background and show your progress")
            print("\n📋 Task Scheduler Details:")
            print(f"   • Task Name: {task_name}")
            print(f"   • Trigger: On user logon")
            print(f"   • User: {os.getenv('USERNAME')}")
            print(f"   • Privileges: Highest")
            
            return True
        else:
            print(f"❌ Error creating task: {result.stderr}")
            return False
        
    except Exception as e:
        print(f"❌ Error setting up Task Scheduler: {e}")
        return False

def remove_task_scheduler():
    """Remove Task Scheduler for the AI Work Tracker"""
    print("🗑️ Removing Task Scheduler for AI Work Tracker...")
    print("=" * 50)
    
    try:
        task_name = "AIWorkTracker"
        
        # schtasks command to delete the task
        schtasks_cmd = ['schtasks', '/delete', '/tn', task_name, '/f']
        
        print(f"🔧 Deleting Task Scheduler task: {task_name}")
        
        # Execute the schtasks command
        result = subprocess.run(schtasks_cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print("✅ Task Scheduler removed successfully!")
            print("📝 The tracker will no longer start automatically")
            return True
        else:
            print(f"❌ Error removing task: {result.stderr}")
            return False
        
    except Exception as e:
        print(f"❌ Error removing Task Scheduler: {e}")
        return False

def check_task_scheduler_status():
    """Check if Task Scheduler is currently set up"""
    print("🔍 Checking Task Scheduler Status...")
    print("=" * 50)
    
    try:
        task_name = "AIWorkTracker"
        
        # schtasks command to query the task
        schtasks_cmd = ['schtasks', '/query', '/tn', task_name, '/fo', 'csv']
        
        # Execute the schtasks command
        result = subprocess.run(schtasks_cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0 and "AIWorkTracker" in result.stdout:
            print("✅ Task Scheduler is currently ENABLED")
            print(f"📋 Task Name: {task_name}")
            print("🔧 Trigger: On user logon")
            return True
        else:
            print("❌ Task Scheduler is currently DISABLED")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Task Scheduler status: {e}")
        return False

def list_all_tasks():
    """List all tasks related to AI Work Tracker"""
    print("📋 Listing all AI Work Tracker tasks...")
    print("=" * 50)
    
    try:
        # schtasks command to list all tasks
        schtasks_cmd = ['schtasks', '/query', '/fo', 'table']
        
        # Execute the schtasks command
        result = subprocess.run(schtasks_cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            ai_tasks = [line for line in lines if 'AIWorkTracker' in line]
            
            if ai_tasks:
                print("Found AI Work Tracker tasks:")
                for task in ai_tasks:
                    print(f"  {task}")
            else:
                print("No AI Work Tracker tasks found")
        else:
            print(f"❌ Error listing tasks: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error listing tasks: {e}")

def create_task_scheduler_batch():
    """Create a batch file for Task Scheduler management"""
    print("📝 Creating Task Scheduler batch file...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    batch_file = os.path.join(current_dir, "manage_task_scheduler.bat")
    
    batch_content = f"""@echo off
echo AI Work Tracker - Task Scheduler Management
echo ==========================================
echo.
echo 1. Start Tracker Now
echo 2. Setup Task Scheduler
echo 3. Remove Task Scheduler
echo 4. Check Task Scheduler Status
echo 5. List All Tasks
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo Starting tracker...
    python "{os.path.join(current_dir, "auto_capture_login_tracker.py")}"
) else if "%choice%"=="2" (
    echo Setting up Task Scheduler...
    python "{os.path.join(current_dir, "setup_task_scheduler.py")}" --setup
) else if "%choice%"=="3" (
    echo Removing Task Scheduler...
    python "{os.path.join(current_dir, "setup_task_scheduler.py")}" --remove
) else if "%choice%"=="4" (
    echo Checking Task Scheduler status...
    python "{os.path.join(current_dir, "setup_task_scheduler.py")}" --status
) else if "%choice%"=="5" (
    echo Listing all tasks...
    python "{os.path.join(current_dir, "setup_task_scheduler.py")}" --list
) else if "%choice%"=="6" (
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
        print(f"✅ Task Scheduler batch file created: {batch_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating batch file: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--setup":
            setup_task_scheduler()
        elif command == "--remove":
            remove_task_scheduler()
        elif command == "--status":
            check_task_scheduler_status()
        elif command == "--list":
            list_all_tasks()
        else:
            print("❌ Unknown command. Use --setup, --remove, --status, or --list")
    else:
        # Interactive mode
        print("🤖 AI Work Tracker - Task Scheduler Setup")
        print("=" * 40)
        print()
        
        # Check current status
        is_enabled = check_task_scheduler_status()
        print()
        
        if is_enabled:
            print("Options:")
            print("1. Remove Task Scheduler")
            print("2. List all tasks")
            print("3. Exit")
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                remove_task_scheduler()
            elif choice == "2":
                list_all_tasks()
            else:
                print("Goodbye!")
        else:
            print("Options:")
            print("1. Setup Task Scheduler")
            print("2. Create management batch file")
            print("3. Exit")
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                setup_task_scheduler()
            elif choice == "2":
                create_task_scheduler_batch()
            else:
                print("Goodbye!")

if __name__ == "__main__":
    main() 