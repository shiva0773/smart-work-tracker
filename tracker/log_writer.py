import json
import os
from datetime import datetime

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
        except (json.JSONDecodeError, FileNotFoundError, IOError):
            logs = []
    else:
        logs = []
    
    # Calculate duration
    try:
        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        duration_seconds = int((end_dt - start_dt).total_seconds())
    except ValueError:
        duration_seconds = 0
    
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
