# tracker/startup_log.py
from datetime import datetime
import json
import os

LOGIN_TRACK_FILE = "logs/login_time.json"
JOB_START = datetime.strptime("09:00", "%H:%M").time()

def log_system_start():
    now = datetime.now()
    login_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Save login only once per day
    if not os.path.exists(LOGIN_TRACK_FILE):
        with open(LOGIN_TRACK_FILE, "w") as f:
            json.dump({"login_time": login_time_str}, f)
    else:
        with open(LOGIN_TRACK_FILE) as f:
            data = json.load(f)
        saved_date = datetime.strptime(data["login_time"], "%Y-%m-%d %H:%M:%S").date()
        if saved_date != now.date():
            with open(LOGIN_TRACK_FILE, "w") as f:
                json.dump({"login_time": login_time_str}, f)

if __name__ == "__main__":
    log_system_start()
