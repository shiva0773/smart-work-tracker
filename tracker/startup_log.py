# tracker/startup_log.py
from datetime import datetime
import json
import os
from tracker.log_writer import write_log

STRUCTURED_LOG_FILE = "logs/structured_log.json"

def log_system_start():
    """Logs a 'system_start' event to the structured log without setting login time."""
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    # Write a generic startup event to the structured log
    write_log(STRUCTURED_LOG_FILE, "system_event", "System Started", now_str, now_str)
    print(f"✅ System startup event logged at: {now_str}")

if __name__ == "__main__":
    log_system_start()
