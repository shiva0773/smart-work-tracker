import os
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CONFIGURATION
LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "structured_log.json")
WEEKLY_REPORT_FILE = os.path.join(os.path.dirname(__file__), "weekly_report.txt")
GMAIL_USER = "gundrashivakumar@@gmail.com"  # <-- CHANGE THIS
GMAIL_PASS = "sfolmifzmhgqpgli"      # <-- CHANGE THIS (use Gmail App Password)
RECIPIENT = "gundrashivakumar@gmail.com"    # <-- CHANGE THIS

# Get start and end of current week (Monday to Friday)
today = datetime.now()
last_friday = today - timedelta(days=(today.weekday() - 4) % 7)
week_start = last_friday - timedelta(days=4)
week_end = last_friday.replace(hour=20, minute=0, second=0, microsecond=0)  # Friday 8pm

# Load logs and filter for this week
def load_weekly_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    week_logs = []
    for entry in logs:
        start = datetime.strptime(entry["start_time"], "%Y-%m-%d %H:%M:%S")
        if week_start <= start <= week_end:
            week_logs.append(entry)
    return week_logs

def generate_weekly_report():
    logs = load_weekly_logs()
    app_usage = {}
    idle_time = 0
    lock_time = 0
    for entry in logs:
        duration = entry["duration_seconds"]
        if entry["event"] == "active_app":
            app_usage[entry["title"]] = app_usage.get(entry["title"], 0) + duration
        elif entry["event"] == "idle":
            idle_time += duration
        elif entry["event"] == "lock":
            lock_time += duration
    report = ["WEEKLY PRODUCTIVITY REPORT\n========================\n"]
    report.append(f"Week: {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d %H:%M')}\n")
    report.append("\nApp Usage:")
    for app, seconds in sorted(app_usage.items(), key=lambda x: x[1], reverse=True):
        mins = seconds // 60
        report.append(f"- {app}: {mins} min")
    report.append(f"\nIdle Time: {idle_time // 60} min")
    report.append(f"Lock Time: {lock_time // 60} min")
    report.append(f"\nTotal Productive Time: {sum(app_usage.values()) // 60} min")
    return "\n".join(report)

def send_email(report):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = RECIPIENT
    msg["Subject"] = "Weekly Productivity Report"
    msg.attach(MIMEText(report, "plain"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, RECIPIENT, msg.as_string())
        print("Report sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    now = datetime.now()
    # Only run on Friday after 8pm
    if now.weekday() != 4 or now.hour < 20:
        return
    report = generate_weekly_report()
    with open(WEEKLY_REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    send_email(report)

if __name__ == "__main__":
    main()
