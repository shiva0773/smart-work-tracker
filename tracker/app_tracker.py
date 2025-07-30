import time
import os
import sys
from datetime import datetime

# Ensure the parent directory is in the path to find the log_writer module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tracker.log_writer import write_log

# pywin32 is required for this module
try:
    import win32gui
except ImportError:
    print("❌ 'pywin32' is not installed. Please run 'pip install pywin32' and add it to requirements.txt")
    sys.exit(1)

LOG_FILE = os.path.join("logs", "structured_log.json")

def get_active_window():
    try:
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window).strip()
    except Exception:
        return ""

def track_active_window(interval=2):
    previous_window = get_active_window()
    start_time = datetime.now()

    while True:
        time.sleep(interval)
        current_window = get_active_window()

        if current_window and current_window != previous_window:
            if previous_window:
                end_time = datetime.now()
                write_log(LOG_FILE, "active_app", previous_window, start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S"))
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Active Window: {current_window}")
            previous_window = current_window
            start_time = datetime.now()
