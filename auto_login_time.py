import os
import json
from datetime import datetime, time

LOGIN_TRACK_FILE = os.path.join(os.path.dirname(__file__), "logs", "login_time.json")
SHIFT_START = time(11, 0, 0)  # 11:00 AM

now = datetime.now()
weekday = now.weekday()  # Monday=0, Sunday=6

if weekday < 5:  # Monday to Friday
    login_time_str = now.strftime("%Y-%m-%d ") + SHIFT_START.strftime("%H:%M:%S")
    if not os.path.exists(LOGIN_TRACK_FILE):
        os.makedirs(os.path.dirname(LOGIN_TRACK_FILE), exist_ok=True)
    with open(LOGIN_TRACK_FILE, "w") as f:
        json.dump({"login_time": login_time_str}, f)
else:
    # Weekend: do not write login_time.json
    if os.path.exists(LOGIN_TRACK_FILE):
        os.remove(LOGIN_TRACK_FILE)
