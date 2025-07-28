# tracker/log_writer.py

import json
import os
from datetime import datetime

LOGIN_TRACK_FILE = os.path.join("logs", "login_time.json")

def get_or_create_daily_login_time():
    today = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(LOGIN_TRACK_FILE):
        try:
            with open(LOGIN_TRACK_FILE, 'r') as f:
                data = json.load(f)
                if data.get("date") == today:
                    return datetime.strptime(data["login_time"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            pass  # corrupt file or invalid data

    now = datetime.now()
    os.makedirs(os.path.dirname(LOGIN_TRACK_FILE), exist_ok=True)
    with open(LOGIN_TRACK_FILE, 'w') as f:
        json.dump({
            "date": today,
            "login_time": now.strftime("%Y-%m-%d %H:%M:%S")
        }, f)
    return now

def write_log(log_file, event_type, title, start_time, end_time):
    """
    Write structured log entry to JSON file
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Load existing logs or create new
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
    else:
        logs = []
    
    # Calculate duration
    start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    duration_seconds = int((end_dt - start_dt).total_seconds())
    
    # Create log entry
    log_entry = {
        "event": event_type,
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "duration_seconds": duration_seconds
    }
    
    logs.append(log_entry)
    
    # Save back to file
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

def write_plain_log(log_file, message):
    """
    Write plain text log entry
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, 'a') as f:
        f.write(f"{message}\n")
