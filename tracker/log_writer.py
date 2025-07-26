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
