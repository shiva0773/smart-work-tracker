#!/usr/bin/env python3
"""
Windows Login Detector
Detects actual Windows login time using Event Log
"""

import subprocess
import json
import re
from datetime import datetime, timedelta

def get_windows_login_time():
    """Get the actual Windows login time for today"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Query Windows Event Log for login events (Event ID 4624 = successful logon)
        cmd = f'wevtutil qe Security /q:"*[System[EventID=4624 and TimeCreated[@SystemTime>=\'{today}T00:00:00.000Z\']]]" /c:50 /f:json'
        
        print(f"🔍 Querying Windows Event Log for login events on {today}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Parse the JSON output to find login events
            events = []
            lines = result.stdout.split('\n')
            
            for line in lines:
                if '"EventID":4624' in line:
                    # Extract timestamp from the event
                    # Look for TimeCreated field
                    time_match = re.search(r'"TimeCreated":\s*"([^"]+)"', line)
                    if time_match:
                        event_time_str = time_match.group(1)
                        # Convert Windows Event Log time format to datetime
                        # Format: 2025-07-28T11:30:00.0000000Z
                        event_time = datetime.strptime(event_time_str.split('.')[0], "%Y-%m-%dT%H:%M:%S")
                        events.append(event_time)
            
            if events:
                # Get the earliest login event of the day
                earliest_login = min(events)
                print(f"✅ Found Windows login time: {earliest_login}")
                return earliest_login
            else:
                print("⚠️ No login events found in Event Log")
        
        # Fallback: Try to get from system boot time
        print("🔄 Trying system boot time as fallback...")
        import psutil
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        current_time = datetime.now()
        
        if boot_time.date() == current_time.date():
            print(f"🖥️ Using system boot time: {boot_time}")
            return boot_time
        else:
            print(f"⚠️ System booted on {boot_time.date()}, using current time")
            return current_time
            
    except Exception as e:
        print(f"❌ Error getting Windows login time: {e}")
        return datetime.now()

def main():
    print("🪟 Windows Login Time Detector")
    print("=" * 40)
    
    login_time = get_windows_login_time()
    logout_time = login_time + timedelta(hours=9)
    
    print(f"\n📊 Results:")
    print(f"🪟 Windows Login: {login_time.strftime('%I:%M %p')}")
    print(f"🔓 Work Start: {login_time.strftime('%I:%M %p')}")
    print(f"🔒 Work End: {logout_time.strftime('%I:%M %p')}")
    print(f"⏱️ Duration: 9 hours")
    
    # Save to file
    data = {
        "windows_login": login_time.strftime("%Y-%m-%d %H:%M:%S"),
        "work_start": login_time.strftime("%Y-%m-%d %H:%M:%S"),
        "work_end": logout_time.strftime("%Y-%m-%d %H:%M:%S"),
        "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    import os
    os.makedirs("logs", exist_ok=True)
    with open("logs/windows_login_detected.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Login time saved to logs/windows_login_detected.json")

if __name__ == "__main__":
    main() 