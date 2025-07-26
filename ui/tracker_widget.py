# ui/widget.py

import tkinter as tk
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tracker.log_writer import get_or_create_daily_login_time
from tracker.system_login_fetcher import get_latest_login_time

class WorkTrackerWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Work Tracker")
        self.root.attributes("-topmost", True)
        self.root.geometry("280x130+10+10")
        self.root.resizable(False, False)
        self.root.configure(bg="#f9f9f9")

        # Get consistent login time from file
        #self.login_time = get_or_create_daily_login_time()
        self.login_time = get_latest_login_time()
        self.logout_time = self.login_time + timedelta(hours=9)

        self.login_label = tk.Label(self.root, text=f"Login Time: {self.login_time.strftime('%I:%M:%S %p')}", font=("Arial", 12), bg="#f9f9f9")
        self.logout_label = tk.Label(self.root, text=f"Logout Time: {self.logout_time.strftime('%I:%M:%S %p')}", font=("Arial", 12), bg="#f9f9f9")
        self.timer_label = tk.Label(self.root, text="Countdown: --:--:--", font=("Arial", 14, "bold"), fg="#2e8b57", bg="#f9f9f9")

        self.login_label.pack(pady=5)
        self.logout_label.pack(pady=5)
        self.timer_label.pack(pady=5)

        self.update_countdown()
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.root.mainloop()

    def update_countdown(self):
        now = datetime.now()
        remaining = self.logout_time - now
        if remaining.total_seconds() > 0:
            countdown = str(remaining).split('.')[0]  # HH:MM:SS
        else:
            countdown = "00:00:00"
        self.timer_label.config(text=f"Countdown: {countdown}")
        self.root.after(1000, self.update_countdown)

    def hide_window(self):
        self.root.withdraw()

if __name__ == "__main__":
    WorkTrackerWidget()
