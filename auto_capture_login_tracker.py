#!/usr/bin/env python3
"""
AI Work Tracker - Best Version
Combines auto-capture with manual time setting for maximum reliability
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import requests
import psutil
import config
from datetime import datetime, timedelta
import getpass
import threading
import pystray
import schedule
import time
from PIL import Image, ImageDraw

from tracker.log_writer import write_log
from daily_report import send_daily_report

class AIWorkTracker:
    APP_VERSION = "v1.5"  # A version number to confirm updates

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"🤖 AI Work Tracker {self.APP_VERSION}")
        self.root.geometry("450x400")
        self.root.resizable(True, True)
        self.root.attributes("-topmost", True)
        
        self.has_shown_minimize_message = False
        
        # Path for the signal file used by the unlock trigger
        self.signal_file_path = os.path.join("logs", "show_window.signal")

        # Set dark theme
        self.root.configure(bg="#23272e")
        
        # Get today's login time
        self.login_time = self.get_todays_login_time()
        self.logout_time = self.login_time + timedelta(hours=9)
        
        # Save login time
        self.save_login_time()
        
        self.setup_ui()
        self.setup_tray_icon()
        self.start_timer()
        self.start_scheduler()

        # Override the close button to hide the window instead of closing
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

    def start_scheduler(self):
        """
        Starts a background scheduler in a separate thread for daily tasks.
        This ensures the UI remains responsive.
        """
        def scheduler_loop():
            # Schedule the daily report to be sent every day at 11 PM (23:00)
            schedule.every().day.at("23:00").do(send_daily_report)
            
            print("🕒 Daily email scheduler started. Report will be sent automatically at 11 PM.")
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check for pending jobs every 60 seconds

        # Run the scheduler in a daemon thread so it exits when the main app closes
        threading.Thread(target=scheduler_loop, daemon=True).start()
        
    def get_todays_login_time(self):
        """Get today's login time - auto-capture or manual setting"""
        today = datetime.now().strftime("%Y-%m-%d")
        login_file = "logs/auto_captured_login.json"
        
        # Check if we already have a login time for today
        if os.path.exists(login_file):
            try:
                with open(login_file, 'r') as f:
                    data = json.load(f)
                    saved_date = data.get('date')
                    if saved_date == today:
                        login_str = data.get('login_time')
                        if login_str:
                            login_time = datetime.strptime(login_str, "%Y-%m-%d %H:%M:%S")
                            print(f"📅 Found today's login time: {login_time}")
                            return login_time
            except Exception as e:
                print(f"⚠️ Error reading login file: {e}")
        
        # If no login time for today, try auto-capture first, then manual
        auto_time = self.try_auto_capture()
        if auto_time:
            return auto_time
        else:
            return self.ask_user_for_time()
    
    def try_auto_capture(self):
        """Try to auto-capture login time using system methods"""
        print("🔍 Trying to auto-capture login time...")
        
        # Method 1: Try to get from system boot time if from today
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            current_time = datetime.now()
            
            if boot_time.date() == current_time.date():
                print(f"🖥️ Using system boot time: {boot_time}")
                return boot_time
        except Exception as e:
            print(f"⚠️ Error getting boot time: {e}")
        
        # Method 2: Check if this is an auto-start scenario (within 5 minutes of boot)
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            current_time = datetime.now()
            time_diff = (current_time - boot_time).total_seconds() / 60  # minutes
            
            if time_diff <= 5:  # Within 5 minutes of boot
                print(f"🚀 Auto-start detected (booted {time_diff:.1f} minutes ago)")
                print(f"⏰ Using current time as login: {current_time}")
                return current_time
        except Exception as e:
            print(f"⚠️ Error checking auto-start scenario: {e}")
        
        # Method 3: Use current time as fallback
        current_time = datetime.now()
        print(f"⏰ Using current time: {current_time}")
        return current_time
    
    def ask_user_for_time(self):
        """Ask user to set their exact start time"""
        # Create a simple dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Your Work Start Time")
        dialog.geometry("350x250")
        dialog.configure(bg="#23272e")
        dialog.attributes("-topmost", True)
        dialog.grab_set()
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Variables
        hour_var = tk.StringVar()
        minute_var = tk.StringVar()
        ampm_var = tk.StringVar()
        
        # Set default values (current time)
        now = datetime.now()
        hour_var.set(str(now.hour % 12 or 12))
        minute_var.set(str(now.minute).zfill(2))
        ampm_var.set("AM" if now.hour < 12 else "PM")
        
        # Instructions
        tk.Label(dialog, text="What time did you start working today?", 
                font=("Arial", 12, "bold"), fg="#fff", bg="#23272e").pack(pady=20)
        
        # Time input frame
        time_frame = tk.Frame(dialog, bg="#23272e")
        time_frame.pack(pady=10)
        
        # Hour
        hour_frame = tk.Frame(time_frame, bg="#23272e")
        hour_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(hour_frame, text="Hour:", font=("Arial", 10), fg="#fff", bg="#23272e").pack()
        hour_entry = tk.Entry(hour_frame, textvariable=hour_var, font=("Arial", 14), width=3, justify="center")
        hour_entry.pack()
        
        # Minute
        minute_frame = tk.Frame(time_frame, bg="#23272e")
        minute_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(minute_frame, text="Minute:", font=("Arial", 10), fg="#fff", bg="#23272e").pack()
        minute_entry = tk.Entry(minute_frame, textvariable=minute_var, font=("Arial", 14), width=3, justify="center")
        minute_entry.pack()
        
        # AM/PM
        ampm_frame = tk.Frame(time_frame, bg="#23272e")
        ampm_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(ampm_frame, text="AM/PM:", font=("Arial", 10), fg="#fff", bg="#23272e").pack()
        ampm_combo = ttk.Combobox(ampm_frame, textvariable=ampm_var, values=["AM", "PM"], font=("Arial", 12), width=5, state="readonly")
        ampm_combo.pack()
        
        # Buttons
        button_frame = tk.Frame(dialog, bg="#23272e")
        button_frame.pack(pady=20)
        
        def set_time():
            try:
                hour = int(hour_var.get())
                minute = int(minute_var.get())
                ampm = ampm_var.get()
                
                # Convert to 24-hour format
                if ampm == "PM" and hour != 12:
                    hour += 12
                elif ampm == "AM" and hour == 12:
                    hour = 0
                
                # Create datetime for today
                today = datetime.now().date()
                start_time = datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))
                
                print(f"✅ User set start time: {start_time}")
                dialog.destroy()
                self.login_time = start_time
                self.logout_time = start_time + timedelta(hours=9)
                self.save_login_time()
                
                # Update display
                self.update_display_labels()
                
            except Exception as e:
                messagebox.showerror("Error", f"Invalid time format. Please use valid numbers.\nError: {e}")
        
        def use_current_time():
            current_time = datetime.now()
            print(f"✅ Using current time: {current_time}")
            dialog.destroy()
            self.login_time = current_time
            self.logout_time = current_time + timedelta(hours=9)
            self.save_login_time()
            self.update_display_labels()
        
        # Buttons
        tk.Button(button_frame, text="Set Time", command=set_time, 
                font=("Arial", 10), fg="#23272e", bg="#4fc3f7").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Use Current Time", command=use_current_time, 
                font=("Arial", 10), fg="#23272e", bg="#81c784").pack(side=tk.LEFT, padx=5)
        
        # Focus on hour entry
        hour_entry.focus()
        
        # Wait for user input
        self.root.wait_window(dialog)
        
        # Return the time (will be set by button callbacks)
        if hasattr(self, 'login_time'):
            return self.login_time
        return datetime.now()  # Fallback
    
    def update_display_labels(self):
        """Update the display labels with new time"""
        self.login_info_label.config(text=f"🤖 Login Time: {self.login_time.strftime('%I:%M %p')}")
        self.login_label.config(text=f"🔓 Work Start: {self.login_time.strftime('%I:%M %p')}")
        self.logout_label.config(text=f"🔒 Work End: {self.logout_time.strftime('%I:%M %p')}")
    
    def save_login_time(self):
        """Save today's login time"""
        today = datetime.now().strftime("%Y-%m-%d")
        login_data = {
            "date": today,
            "login_time": self.login_time.strftime("%Y-%m-%d %H:%M:%S"),
            "logout_time": self.logout_time.strftime("%Y-%m-%d %H:%M:%S"),
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "method": "auto_capture_with_manual_fallback"
        }
        
        os.makedirs("logs", exist_ok=True)
        with open("logs/auto_captured_login.json", "w") as f:
            json.dump(login_data, f, indent=2)
        
        print(f"✅ Login time saved: {self.login_time}")
    
    def get_weather(self):
        """Get weather for the configured city."""
        if not config.OPENWEATHER_API_KEY or "YOUR_API_KEY" in config.OPENWEATHER_API_KEY:
            print("⚠️ Weather API key not set in config.py. Skipping weather fetch.")
            return "--°C"
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={config.WEATHER_CITY}&appid={config.OPENWEATHER_API_KEY}&units=metric"
        
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            data = resp.json()
            temp = data.get('main', {}).get('temp')
            if temp is not None:
                return f"{temp}°C"
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching weather: {e}")
        
        return "--°C"
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#23272e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🤖 AI Work Tracker", 
                              font=("Arial", 18, "bold"), 
                              fg="#4fc3f7", bg="#23272e")
        title_label.pack(pady=(0, 10))
        
        # User info with weather
        weather_temp = self.get_weather()
        user_label = tk.Label(main_frame, 
                             text=f"👤 Hello, {getpass.getuser()} 🌤️ {weather_temp}", 
                             font=("Arial", 14), 
                             fg="#fff", bg="#23272e")
        user_label.pack(pady=(0, 15))
        
        # Login info
        login_frame = tk.Frame(main_frame, bg="#2c313c", bd=2, relief="ridge")
        login_frame.pack(pady=(0, 15), fill="x")
        
        self.login_info_label = tk.Label(login_frame, 
                                        text=f"🤖 Login Time: {self.login_time.strftime('%I:%M %p')}", 
                                        font=("Arial", 12, "bold"), 
                                        fg="#ffd700", bg="#2c313c")
        self.login_info_label.pack(pady=(8, 4), padx=10)
        
        # Login/Logout times
        time_frame = tk.Frame(main_frame, bg="#2c313c", bd=2, relief="ridge")
        time_frame.pack(pady=(0, 15), fill="x")
        
        self.login_label = tk.Label(time_frame, 
                                   text=f"🔓 Work Start: {self.login_time.strftime('%I:%M %p')}", 
                                   font=("Arial", 14, "bold"), 
                                   fg="#4fc3f7", bg="#2c313c")
        self.login_label.pack(pady=(8, 4), padx=10)
        
        self.logout_label = tk.Label(time_frame, 
                                    text=f"🔒 Work End: {self.logout_time.strftime('%I:%M %p')}", 
                                    font=("Arial", 14, "bold"), 
                                    fg="#81c784", bg="#2c313c")
        self.logout_label.pack(pady=(4, 8), padx=10)
        
        # Progress bar
        progress_label = tk.Label(main_frame, text="Workday Progress:", 
                                 font=("Arial", 12, "bold"), 
                                 fg="#fff", bg="#23272e")
        progress_label.pack(pady=(0, 5))
        
        self.progress_var = tk.DoubleVar()
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", troughcolor="#23272e", background="#4fc3f7", 
                       bordercolor="#23272e", lightcolor="#23272e", darkcolor="#23272e")
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=350, style="TProgressbar")
        self.progress_bar.pack(pady=(0, 10))
        
        # Countdown
        self.countdown_label = tk.Label(main_frame, text="", 
                                       font=("Arial", 16, "bold"), 
                                       fg="#f92672", bg="#23272e")
        self.countdown_label.pack(pady=(0, 10))
        
        # Status
        self.status_label = tk.Label(main_frame, text="", 
                                    font=("Arial", 12), 
                                    fg="#ffd700", bg="#23272e")
        self.status_label.pack()

        # Idle/Lock status
        self.activity_status_label = tk.Label(main_frame, text="",
                                             font=("Arial", 11, "italic"),
                                             fg="#ff6b6b", bg="#23272e")
        self.activity_status_label.pack(pady=(5, 0))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg="#23272e")
        button_frame.pack(pady=(10, 0))
        
        minimize_btn = tk.Button(button_frame, text="Minimize", 
                                command=self.root.iconify, 
                                font=("Arial", 12), 
                                fg="#23272e", bg="#4fc3f7", 
                                activebackground="#81c784", activeforeground="#23272e")
        minimize_btn.pack(side=tk.LEFT, padx=5)
        
        change_time_btn = tk.Button(button_frame, text="Change Time", 
                                   command=self.change_time, 
                                   font=("Arial", 12), 
                                   fg="#23272e", bg="#ff6b6b", 
                                   activebackground="#ff8e8e", activeforeground="#23272e")
        change_time_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(button_frame, text="Reset for Tomorrow", 
                             command=self.reset_for_tomorrow, 
                             font=("Arial", 12), 
                             fg="#23272e", bg="#ff9800", 
                             activebackground="#ffb74d", activeforeground="#23272e")
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        end_day_btn = tk.Button(button_frame, text="End Day",
                                     command=self.handle_end_day,
                                     font=("Arial", 12),
                                     fg="#fff", bg="#d32f2f",
                                     activebackground="#e57373", activeforeground="#fff")
        end_day_btn.pack(side=tk.LEFT, padx=5)
    
    def change_time(self):
        """Change the start time"""
        # Delete today's login file to force re-ask
        login_file = "logs/auto_captured_login.json"
        if os.path.exists(login_file):
            os.remove(login_file)
        
        # Get new time
        self.login_time = self.get_todays_login_time()
        self.logout_time = self.login_time + timedelta(hours=9)
        self.update_display_labels()
    
    def reset_for_tomorrow(self):
        """Deletes today's login and report flag files to allow a fresh start."""
        login_file = "logs/auto_captured_login.json"
        if os.path.exists(login_file):
            os.remove(login_file)
            print("🗑️ Removed today's login file.")

        # Also remove the report sent flag for today
        today_str = datetime.now().strftime("%Y-%m-%d")
        flag_file = os.path.join("logs", f"report_sent_{today_str}.flag")
        if os.path.exists(flag_file):
            os.remove(flag_file)
            print("🗑️ Removed today's report-sent flag.")
        
        messagebox.showinfo("Reset Complete", "Tracker has been reset. It will perform a fresh auto-capture on the next start.")

    def handle_end_day(self):
        """Handles the process for ending the workday, either early or on time."""
        remaining_seconds = (self.logout_time - datetime.now()).total_seconds()

        if remaining_seconds > 0:
            # Workday is not complete, so this is an early logout.
            self.show_early_logout_dialog()
        else:
            # Workday is complete.
            if messagebox.askyesno("Confirm End Day", "You've completed your 9 hours. Great job!\n\nDo you want to close the tracker for the day?"):
                now = datetime.now()
                write_log(
                    "logs/structured_log.json",
                    "normal_logout",
                    "Workday Complete",
                    self.login_time.strftime("%Y-%m-%d %H:%M:%S"),
                    now.strftime("%Y-%m-%d %H:%M:%S")
                )
                self.update_logout_info(now, "Workday Complete")
                
                # Send the daily report email immediately upon ending the day
                print("📧 Triggering daily email report...")
                threading.Thread(target=send_daily_report, daemon=True).start()
                self.root.destroy()

    def show_early_logout_dialog(self):
        """Shows a dialog to get the reason for an early logout."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Early Logout Reason")
        dialog.geometry("350x200")
        dialog.configure(bg="#23272e")
        dialog.attributes("-topmost", True)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Why are you logging out early?", font=("Arial", 12, "bold"), fg="#fff", bg="#23272e").pack(pady=10)

        reasons = ["Feeling unwell", "Personal commitment", "Finished work early", "Other"]
        reason_var = tk.StringVar(value=reasons[0])

        reason_combo = ttk.Combobox(dialog, textvariable=reason_var, values=reasons, state="readonly", font=("Arial", 12))
        reason_combo.pack(pady=5, padx=20, fill="x")

        def confirm_logout():
            reason = reason_var.get()
            now = datetime.now()

            # 1. Log the event to the structured log file
            write_log(
                "logs/structured_log.json",
                "early_logout",
                reason,  # The reason becomes the title of the log entry
                self.login_time.strftime("%Y-%m-%d %H:%M:%S"),
                now.strftime("%Y-%m-%d %H:%M:%S")
            )

            # 2. Update the main login file with final details
            self.update_logout_info(now, reason)

            # Send the daily report email
            print("📧 Triggering daily email report for early logout...")
            threading.Thread(target=send_daily_report, daemon=True).start()

            # 3. Show confirmation and close the app
            messagebox.showinfo("Logout Successful", f"You have been logged out for the day.\nReason: {reason}")
            self.root.destroy()

        button_frame = tk.Frame(dialog, bg="#23272e")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Confirm & Logout", command=confirm_logout, font=("Arial", 10), fg="#fff", bg="#d32f2f").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, font=("Arial", 10), fg="#23272e", bg="#ccc").pack(side=tk.LEFT, padx=10)

        self.root.wait_window(dialog)

    def update_logout_info(self, logout_time, reason):
        """Updates the main login file with the final logout time and reason."""
        login_file = "logs/auto_captured_login.json"
        
        if os.path.exists(login_file):
            with open(login_file, 'r') as f:
                login_data = json.load(f)
        else:
            login_data = {"date": datetime.now().strftime("%Y-%m-%d")}

        login_data['actual_logout_time'] = logout_time.strftime("%Y-%m-%d %H:%M:%S")
        login_data['logout_reason'] = reason
        with open(login_file, "w") as f:
            json.dump(login_data, f, indent=2)
        print(f"✅ Final logout info saved at {logout_time} for reason: {reason}")

    def setup_tray_icon(self):
        """Sets up and runs the system tray icon in a separate thread."""
        # Create a simple icon image
        width = 64
        height = 64
        color1 = "#4fc3f7"  # A light blue
        color2 = "#23272e"  # Dark background
        image = Image.new('RGB', (width, height), color2)
        dc = ImageDraw.Draw(image)
        dc.rectangle([(width // 4, height // 4), (width * 3 // 4, height * 3 // 4)], fill=color1)
        
        menu = (
            pystray.MenuItem('Show Tracker', self.show_window, default=True),
            pystray.MenuItem('Quit', self.quit_app)
        )
        
        self.tray_icon = pystray.Icon("AIWorkTracker", image, "AI Work Tracker", menu)
        
        # Run the icon in a separate thread so it doesn't block the UI
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self, icon=None, item=None):
        """
        Shows the main window. This is made thread-safe for pystray.
        It also brings the window to the front.
        """
        def _show_and_focus():
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
        self.root.after(0, _show_and_focus)

    def hide_window(self):
        """Hides the main window and shows a one-time notification."""
        self.root.withdraw()
        if not self.has_shown_minimize_message:
            # Use the tray icon to show a balloon tip notification
            if self.tray_icon and self.tray_icon.visible:
                self.tray_icon.notify(
                    "The tracker is running in the background. Right-click the tray icon to show or quit.",
                    "AI Work Tracker"
                )
            self.has_shown_minimize_message = True

    def quit_app(self, icon=None, item=None):
        """Stops the tray icon and closes the application. Made thread-safe for pystray."""
        self.tray_icon.stop()
        # Schedule the root window destruction on the main thread
        self.root.after(0, self.root.destroy)

    def get_today_activity_stats(self):
        """Calculates total idle and lock time for today from the structured log."""
        log_file = "logs/structured_log.json"
        today_str = datetime.now().strftime('%Y-%m-%d')
        idle_seconds = 0
        lock_seconds = 0

        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
                    for entry in logs:
                        if entry.get('start_time', '').startswith(today_str):
                            if entry.get('event') == 'idle':
                                idle_seconds += entry.get('duration_seconds', 0)
                            elif entry.get('event') == 'lock':
                                lock_seconds += entry.get('duration_seconds', 0)
            except (json.JSONDecodeError, IOError):
                pass  # Ignore errors if the file is being written to
        return idle_seconds, lock_seconds
    
    def start_timer(self):
        """Start the update timer"""
        self.update_display()
        self.root.after(1000, self.start_timer)
    
    def update_display(self):
        """Update the display with current time and progress"""
        # Periodically check for signals (like the unlock trigger)
        self.check_for_signals()

        now = datetime.now()
        remaining = self.logout_time - now
        total_duration = self.logout_time - self.login_time
        elapsed = now - self.login_time
        
        # Calculate progress percentage
        if total_duration.total_seconds() > 0:
            progress_percent = min(100, max(0, (elapsed.total_seconds() / total_duration.total_seconds()) * 100))
            self.progress_var.set(progress_percent)
        
        # Update countdown
        if remaining.total_seconds() > 0:
            countdown_str = str(remaining).split('.')[0]
            self.countdown_label.config(text=f"⏳ Time left: {countdown_str}")
        else:
            self.countdown_label.config(text="✅ 9 Hours Completed!")
        
        # Update status
        if remaining.total_seconds() > 0:
            hours_worked = elapsed.total_seconds() / 3600
            self.status_label.config(text=f"Status: Working ({hours_worked:.1f} hours completed)")
        else:
            self.status_label.config(text="Status: Workday Complete!")

        # Update idle/lock status
        idle_seconds, lock_seconds = self.get_today_activity_stats()
        activity_text = []
        if idle_seconds > 60:
            activity_text.append(f"Idle: {idle_seconds // 60} min")
        if lock_seconds > 60:
            activity_text.append(f"Locked: {lock_seconds // 60} min")
        
        self.activity_status_label.config(text=" | ".join(activity_text))
    
    def check_for_signals(self):
        """Checks for external signal files to perform actions, like showing the window."""
        if os.path.exists(self.signal_file_path):
            try:
                # A signal file was found, so show the window and remove the file
                logging.info("💡 Detected unlock signal. Showing window.")
                self.show_window()
                os.remove(self.signal_file_path)
            except Exception as e:
                logging.warning(f"⚠️ Error processing signal file: {e}")

    def run(self):
        """Run the tracker"""
        self.root.mainloop()

def main():
    print("🚀 Starting AI Work Tracker...")
    print("🤖 Auto-captures login time with manual fallback")
    print("⏰ Login time = Auto-detected or manually set")
    print("⏰ Logout time = 9 hours from login time")
    print("💡 Best of both worlds - automatic when possible, manual when needed!")
    
    tracker = AIWorkTracker()
    tracker.run()

if __name__ == "__main__":
    main() 