#!/usr/bin/env python3
"""
System Startup Work Tracker
Detects actual system startup and tracks work hours from that moment
"""

import tkinter as tk
from tkinter import ttk
import json
import os
import requests
import psutil
import time
from datetime import datetime, timedelta
import getpass
import win32gui
import win32con
import win32api

class SystemStartupTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🕒 System Startup Work Tracker")
        self.root.geometry("450x350")
        self.root.resizable(True, True)
        self.root.attributes("-topmost", True)
        
        # Set dark theme
        self.root.configure(bg="#23272e")
        
        # Get system startup time
        self.system_startup_time = self.get_system_startup_time()
        self.login_time = self.system_startup_time
        self.logout_time = self.login_time + timedelta(hours=9)
        
        # Save startup time
        self.save_startup_time()
        
        self.setup_ui()
        self.start_timer()
        
        # Handle system events
        self.setup_system_events()
        
    def get_system_startup_time(self):
        """Get the actual system startup time"""
        try:
            # Get system boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            current_time = datetime.now()
            
            # Check if boot time is from today
            if boot_time.date() == current_time.date():
                print(f"🖥️ System booted today at: {boot_time}")
                return boot_time
            else:
                # If boot time is from a different day, use current time
                print(f"🖥️ System booted on {boot_time.date()}, using current time: {current_time}")
                return current_time
        except Exception as e:
            print(f"⚠️ Could not get boot time: {e}")
            return datetime.now()
    
    def save_startup_time(self):
        """Save the system startup time"""
        startup_data = {
            "system_startup": self.system_startup_time.strftime("%Y-%m-%d %H:%M:%S"),
            "login_time": self.login_time.strftime("%Y-%m-%d %H:%M:%S"),
            "logout_time": self.logout_time.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        os.makedirs("logs", exist_ok=True)
        with open("logs/system_startup.json", "w") as f:
            json.dump(startup_data, f, indent=2)
        
        print(f"✅ Startup time saved: {self.system_startup_time}")
    
    def get_weather(self):
        """Get weather for Hyderabad"""
        try:
            api_key = "bd5e378503939ddaee76f12ad7a97608"
            city = "Hyderabad"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                temp = data['main']['temp']
                return f"{temp}°C"
        except Exception:
            pass
        return "--°C"
    
    def setup_system_events(self):
        """Setup system event monitoring"""
        def on_system_event(event):
            if event == win32con.WM_POWERBROADCAST:
                print("🔋 System power event detected")
            elif event == win32con.WM_DEVICECHANGE:
                print("🖥️ System device change detected")
        
        # Register for system events
        try:
            win32gui.SetWinEventHook(
                win32con.WM_POWERBROADCAST,
                win32con.WM_DEVICECHANGE,
                0,
                on_system_event,
                0,
                0,
                win32con.WINEVENT_OUTOFCONTEXT
            )
        except Exception as e:
            print(f"⚠️ Could not setup system events: {e}")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#23272e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🕒 System Startup Tracker", 
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
        
        # System startup info
        startup_frame = tk.Frame(main_frame, bg="#2c313c", bd=2, relief="ridge")
        startup_frame.pack(pady=(0, 15), fill="x")
        
        self.startup_label = tk.Label(startup_frame, 
                                     text=f"🖥️ System Started: {self.system_startup_time.strftime('%I:%M %p')}", 
                                     font=("Arial", 12, "bold"), 
                                     fg="#ffd700", bg="#2c313c")
        self.startup_label.pack(pady=(8, 4), padx=10)
        
        # Login/Logout times
        time_frame = tk.Frame(main_frame, bg="#2c313c", bd=2, relief="ridge")
        time_frame.pack(pady=(0, 15), fill="x")
        
        self.login_label = tk.Label(time_frame, 
                                   text=f"🔓 Login: {self.login_time.strftime('%I:%M %p')}", 
                                   font=("Arial", 14, "bold"), 
                                   fg="#4fc3f7", bg="#2c313c")
        self.login_label.pack(pady=(8, 4), padx=10)
        
        self.logout_label = tk.Label(time_frame, 
                                    text=f"🔒 Logout: {self.logout_time.strftime('%I:%M %p')}", 
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
        
        # Minimize button
        minimize_btn = tk.Button(main_frame, text="Minimize", 
                                command=self.root.iconify, 
                                font=("Arial", 12), 
                                fg="#23272e", bg="#4fc3f7", 
                                activebackground="#81c784", activeforeground="#23272e")
        minimize_btn.pack(pady=(10, 0))
    
    def start_timer(self):
        """Start the update timer"""
        self.update_display()
        self.root.after(1000, self.start_timer)
    
    def update_display(self):
        """Update the display with current time and progress"""
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
    
    def run(self):
        """Run the tracker"""
        self.root.mainloop()

def main():
    print("🚀 Starting System Startup Work Tracker...")
    print("🖥️ Detecting actual system startup time...")
    print("⏰ Login time = When system actually booted")
    print("⏰ Logout time = 9 hours from system startup")
    
    tracker = SystemStartupTracker()
    tracker.run()

if __name__ == "__main__":
    main() 