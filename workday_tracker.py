import os
import datetime
import json
from plyer import notification

LOG_FILE = "daily_work_log.json"
WORK_HOURS_REQUIRED = 9

def get_today_key():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def record_login():
    logs = load_logs()
    today = get_today_key()

    if today not in logs:
        logs[today] = {"login": datetime.datetime.now().strftime("%H:%M:%S")}
        save_logs(logs)

def record_logout():
    logs = load_logs()
    today = get_today_key()

    if today in logs and "logout" not in logs[today]:
        logs[today]["logout"] = datetime.datetime.now().strftime("%H:%M:%S")
        save_logs(logs)

def calculate_duration(login_str, logout_str):
    fmt = "%H:%M:%S"
    login_time = datetime.datetime.strptime(login_str, fmt)
    logout_time = datetime.datetime.strptime(logout_str, fmt)
    duration = logout_time - login_time
    return duration

def show_yesterday_summary():
    logs = load_logs()
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    if yesterday in logs:
        login = logs[yesterday].get("login", "N/A")
        logout = logs[yesterday].get("logout", "N/A")
        message = f"🕘 Login: {login}\n🕔 Logout: {logout}"

        if login != "N/A" and logout != "N/A":
            duration = calculate_duration(login, logout)
            hours = duration.total_seconds() / 3600

            if hours < WORK_HOURS_REQUIRED:
                message += f"\n⏱ Worked: {hours:.2f} hrs (Early Logout)"
            else:
                message += f"\n⏱ Worked: {hours:.2f} hrs (Full Day)"

        notification.notify(
            title="📋 Yesterday's Work Summary",
            message=message,
            timeout=10
        )

# Example usage:
if __name__ == "__main__":
    show_yesterday_summary()
    record_login()
