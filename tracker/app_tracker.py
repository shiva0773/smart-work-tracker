import time
import win32gui
import datetime
from tracker.log_writer import write_log

def get_active_window():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window).strip()

def track_active_window(interval=2):
    previous_window = None
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    while True:
        current_window = get_active_window()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if current_window and current_window != previous_window:
            if previous_window:
                write_log("active_app", previous_window, start_time, now)
            print(f"{now} - Active Window: {current_window}")
            previous_window = current_window
            start_time = now

        time.sleep(interval)
