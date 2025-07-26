# tracker/shutdown_log.py

import os
import json
from datetime import datetime
from tracker.log_writer import write_log

STRUCTURED_LOG_FILE = "logs/structured_log.json"
PLAIN_LOG_FILE = "logs/work_hours_log.txt"
WORK_HOURS_REQUIRED = 9  # hours

def log_system_shutdown():
    now = datetime.now()
    end_time = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Ensure log file exists
        if not os.path.exists(STRUCTURED_LOG_FILE):
            raise Exception("Structured log file does not exist.")

        with open(STRUCTURED_LOG_FILE, "r") as f:
            logs = json.load(f)
            login_entries = [entry for entry in logs if entry["event"] == "login"]

            if not login_entries:
                raise Exception("No login record found.")
            
            last_login = login_entries[-1]
            start_time = last_login["start_time"]
            login_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            worked_duration = now - login_time
            hours_worked = round(worked_duration.total_seconds() / 3600, 2)
            note = "Full Day" if hours_worked >= WORK_HOURS_REQUIRED else "Early Logout"

            # Write plain log
            write_log(PLAIN_LOG_FILE, f"[LOGOUT] {end_time} - Worked: {hours_worked} hrs - {note}")

            # Write structured log
            write_log(STRUCTURED_LOG_FILE, "logout", f"{note} - Worked: {hours_worked} hrs", start_time, end_time)

    except Exception as e:
        # Fallback: log error to both logs
        write_log(PLAIN_LOG_FILE, f"[LOGOUT] {end_time} - Error: {e}")
        write_log(STRUCTURED_LOG_FILE, "logout", f"Error: {e}", end_time, end_time)

if __name__ == "__main__":
    log_system_shutdown()
