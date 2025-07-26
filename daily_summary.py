# daily_summary.py

import os
from datetime import datetime, timedelta

# Settings
WORK_HOURS = 9
LATE_LOGIN_THRESHOLD = "09:15"  # After this it's considered a late login
EARLY_LOGOUT_THRESHOLD = "18:00"  # Before this it's early logout
SUMMARY_FILE = "daily_summary_log.txt"

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_late_login(login_time):
    return login_time.time() > datetime.strptime(LATE_LOGIN_THRESHOLD, "%H:%M").time()

def is_early_logout(logout_time):
    return logout_time.time() < datetime.strptime(EARLY_LOGOUT_THRESHOLD, "%H:%M").time()

def log_daily_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    login_file = f"logs/login_{today}.log"
    logout_file = f"logs/logout_{today}.log"

    if not os.path.exists(login_file):
        print("No login recorded today.")
        return
    if not os.path.exists(logout_file):
        print("No logout recorded today.")
        return

    with open(login_file) as f:
        login_time = datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S")
    with open(logout_file) as f:
        logout_time = datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S")

    work_duration = logout_time - login_time
    status = []
    if is_late_login(login_time):
        status.append("Late Login")
    if is_early_logout(logout_time):
        status.append("Early Logout")

    summary_line = f"{today} | Login: {login_time.time()} | Logout: {logout_time.time()} | Duration: {work_duration} | Status: {', '.join(status) or 'On Time'}"

    with open(SUMMARY_FILE, "a") as f:
        f.write(summary_line + "\n")

    # Optional: Show a popup on screen
    from plyer import notification
    notification.notify(
        title="👨‍💻 Daily Work Summary",
        message=summary_line,
        timeout=10
    )

if __name__ == "__main__":
    log_daily_summary()
