# tracker/startup_log.py
from datetime import datetime
import json
import os
from tracker.log_writer import write_log

LOGIN_TRACK_FILE = "logs/login_time.json"
STRUCTURED_LOG_FILE = "logs/structured_log.json"
SHIFT_START = datetime.strptime("11:00", "%H:%M").time()

def log_system_start():
    now = datetime.now()
    
    # Use 11 AM as the login time
    login_time = now.replace(hour=11, minute=0, second=0, microsecond=0)
    login_time_str = login_time.strftime("%Y-%m-%d %H:%M:%S")

    # Save login time to login_time.json
    os.makedirs(os.path.dirname(LOGIN_TRACK_FILE), exist_ok=True)
    with open(LOGIN_TRACK_FILE, "w") as f:
        json.dump({"login_time": login_time_str}, f)
    
    # Also write to structured log
    write_log(STRUCTURED_LOG_FILE, "login", "Workday Start", login_time_str, login_time_str)
    
    print(f"✅ Login time set to: {login_time_str}")

if __name__ == "__main__":
    log_system_start()
