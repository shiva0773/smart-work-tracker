#!/usr/bin/env python3
"""
AI Work Tracker Startup Script
Handles 11 AM startup timing and launches all tracker components
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime, time as dt_time
import json

def is_workday():
    """Check if today is a workday (Monday-Friday)"""
    return datetime.now().weekday() < 5

def is_after_11am():
    """Check if current time is after 11 AM"""
    return datetime.now().time() >= dt_time(11, 0)

def wait_until_11am():
    """Wait until 11 AM if it's not yet 11 AM"""
    now = datetime.now()
    target_time = now.replace(hour=11, minute=0, second=0, microsecond=0)
    
    if now.time() < dt_time(11, 0):
        wait_seconds = (target_time - now).total_seconds()
        print(f"⏰ Waiting until 11:00 AM... ({wait_seconds/60:.1f} minutes)")
        time.sleep(wait_seconds)
    
    print("🕚 11:00 AM reached! Starting tracker...")

def setup_login_time():
    """Set up the login time for 11 AM"""
    from auto_login_time import LOGIN_TRACK_FILE, SHIFT_START
    
    now = datetime.now()
    login_time_str = now.strftime("%Y-%m-%d ") + SHIFT_START.strftime("%H:%M:%S")
    
    os.makedirs(os.path.dirname(LOGIN_TRACK_FILE), exist_ok=True)
    with open(LOGIN_TRACK_FILE, "w") as f:
        json.dump({"login_time": login_time_str}, f)
    
    print(f"✅ Login time set to: {login_time_str}")

def start_tracker_components():
    """Start all tracker components"""
    components = [
        ("desktop_display.py", "Desktop Display"),
        ("tracker/app_tracker.py", "App Tracker"),
        ("tracker/idle_tracker.py", "Idle Tracker"),
        ("tracker/lock_tracker.py", "Lock Tracker")
    ]
    
    processes = []
    
    for script, name in components:
        try:
            print(f"🚀 Starting {name}...")
            process = subprocess.Popen([sys.executable, script], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            processes.append((process, name))
            time.sleep(1)  # Small delay between starts
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
    
    return processes

def main():
    print("🤖 AI Work Tracker Startup")
    print("=" * 40)
    
    # Check if it's a workday
    if not is_workday():
        print("📅 Weekend detected. Tracker will not start.")
        return
    
    # Wait until 11 AM if needed
    if not is_after_11am():
        wait_until_11am()
    else:
        print("🕚 Already past 11 AM, starting immediately...")
    
    # Set up login time
    setup_login_time()
    
    # Start tracker components
    print("\n📊 Starting tracker components...")
    processes = start_tracker_components()
    
    print("\n✅ AI Work Tracker is now running!")
    print("Press Ctrl+C to stop all components")
    
    try:
        # Keep the main process running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Shutting down tracker components...")
        for process, name in processes:
            try:
                process.terminate()
                print(f"🛑 Stopped {name}")
            except:
                pass

if __name__ == "__main__":
    main() 