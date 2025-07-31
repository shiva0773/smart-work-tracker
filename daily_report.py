import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "structured_log.json")

def load_todays_logs():
    """Loads log entries from today."""
    if not os.path.exists(LOG_FILE):
        return []
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_logs = []
    
    with open(LOG_FILE, "r") as f:
        try:
            logs = json.load(f)
            for entry in logs:
                if entry.get("start_time", "").startswith(today_str):
                    today_logs.append(entry)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {LOG_FILE}. It might be empty or corrupt.")
            return []
            
    return today_logs

def generate_daily_report_text(logs):
    """Generates a text summary of the day's activity."""
    app_usage = {}
    idle_time = 0
    lock_time = 0
    total_active_time = 0
    
    for entry in logs:
        duration = entry.get("duration_seconds", 0)
        if entry["event"] == "active_app":
            app_title = entry.get("title", "Unknown App")
            app_usage[app_title] = app_usage.get(app_title, 0) + duration
            total_active_time += duration
        elif entry["event"] == "idle":
            idle_time += duration
        elif entry["event"] == "lock":
            lock_time += duration

    report = [f"DAILY WORK SUMMARY - {datetime.now().strftime('%Y-%m-%d')}\n=======================================\n"]
    
    report.append("--- Activity Summary ---")
    report.append(f"Total Productive Time: {total_active_time // 60} minutes")
    report.append(f"Total Idle Time: {idle_time // 60} minutes")
    report.append(f"Total Lock Time: {lock_time // 60} minutes\n")
    
    report.append("--- Application Usage ---")
    if not app_usage:
        report.append("No application usage tracked.")
    else:
        # Sort apps by usage time, descending
        for app, seconds in sorted(app_usage.items(), key=lambda x: x[1], reverse=True):
            mins = seconds // 60
            if mins > 0:
                report.append(f"- {app}: {mins} min")
                
    return "\n".join(report)

def send_email(report_text):
    """Sends the report via email."""
    msg = MIMEMultipart()
    msg["From"] = config.GMAIL_USER
    msg["To"] = config.RECIPIENT
    msg["Subject"] = f"Daily Work Report - {datetime.now().strftime('%Y-%m-%d')}"

    html = f"""
    <html><body style='font-family: sans-serif;'>
    <h2>Daily Work Summary</h2>
    <pre style='font-size: 14px; background: #f4f4f4; padding: 15px; border-radius: 5px;'>{report_text}</pre>
    <p style='font-size: 12px; color: #777;'>Automated report from AI Work Tracker.</p>
    </body></html>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(config.GMAIL_USER, config.GMAIL_PASS)
            server.sendmail(config.GMAIL_USER, config.RECIPIENT, msg.as_string())
        print("✅ Daily report email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_daily_report():
    """Main function to generate and send the daily report."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    flag_file = os.path.join(os.path.dirname(LOG_FILE), f"report_sent_{today_str}.flag")

    if os.path.exists(flag_file):
        print(f"✅ Daily report for {today_str} has already been sent. Skipping.")
        return

    print("📊 Generating daily report...")
    logs = load_todays_logs()
    if not logs:
        print("No logs for today. Skipping report.")
        return
    report_text = generate_daily_report_text(logs)
    send_email(report_text)

    # Create the flag file to prevent re-sending today
    with open(flag_file, "w") as f:
        f.write(datetime.now().isoformat())
    print(f"🚩 Created flag file to prevent duplicate reports for today.")