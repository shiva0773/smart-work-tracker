#!/usr/bin/env python3
"""
Windows Login Tracker
Detects actual Windows login time for today
"""

import tkinter as tk
from tkinter import ttk
import json
import os
import requests
import subprocess
from datetime import datetime, timedelta
import getpass

class WindowsLoginTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🕒 Windows Login Tracker")
        self.root.geometry("450x350")
        self.root.resizable(True, True)
        self.root.attributes("-topmost", True)
        
        # Set dark theme
        self.root.configure(bg="#23272e")
        
        # Get actual Windows login time for today
        self.login_time = self.get_windows_login_time()
        self.logout_time = self.login_time + timedelta(hours=9)
        
        # Save login time
        self.save_login_time()
        
        self.setup_ui()
        self.start_timer()
        
    def get_windows_login_time(self):
        """Get the actual Windows login time for today"""
        try:
            # Method 1: Check Windows Event Log for login events
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Query Windows Event Log for login events
            cmd = f'wevtutil qe Security /q:"*[System[TimeCreated[@SystemTime>=\'{today}T00:00:00.000Z\']]]" /c:10 /f:json'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse the event log to find login events
                # Look for Event ID 4624 (successful logon)
                lines = result.stdout.split('\n')
                for line in lines:
                    if '"EventID":4624' in line and 'shivakumar.gundra' in line:
                        # Extract timestamp from the event
                        # This is a simplified approach - in practice you'd parse the JSON properly
                        print(f"🔍 Found login event in Windows logs")
                        break
            
            # Method 2: Check if we have a saved login time for today
            login_file = "logs/windows_login.json"
            if os.path.exists(login_file):
                with open(login_file, 'r') as f:
                    data = json.load(f)
                    saved_date = data.get('date')
                    if saved_date == today:
                        login_str = data.get('login_time')
                        if login_str:
                            login_time = datetime.strptime(login_str, "%Y-%m-%d %H:%M:%S")
                            print(f"📅 Found saved login time for today: {login_time}")
                            return login_time
            
            # Method 3: Use system boot time as fallback
            import psutil
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            current_time = datetime.now()
            
            if boot_time.date() == current_time.date():
                print(f"🖥️ Using system boot time as login time: {boot_time}")
                return boot_time
            else:
                print(f"⚠️ System booted on {boot_time.date()}, using current time")
                return current_time
                
        except Exception as e:
            print(f"⚠️ Error getting Windows login time: {e}")
            return datetime.now()
    
    def save_login_time(self):
        """Save the Windows login time"""
        today = datetime.now().strftime("%Y-%m-%d")
        login_data = {
            "date": today,
            "login_time": self.login_time.strftime("%Y-%m-%d %H:%M:%S"),
            "logout_time": self.logout_time.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        os.makedirs("logs", exist_ok=True)
        with open("logs/windows_login.json", "w") as f:
            json.dump(login_data, f, indent=2)
        
        print(f"✅ Windows login time saved: {self.login_time}")
    
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
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#23272e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🕒 Windows Login Tracker", 
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
        
        # Windows login info
        login_frame = tk.Frame(main_frame, bg="#2c313c", bd=2, relief="ridge")
        login_frame.pack(pady=(0, 15), fill="x")
        
        self.login_info_label = tk.Label(login_frame, 
                                        text=f"🪟 Windows Login: {self.login_time.strftime('%I:%M %p')}", 
                                        font=("Arial", 12, "bold"), 
                                        fg="#ffd700", bg="#2c313c")
        self.login_info_label.pack(pady=(8, 4), padx=10)
        
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
    print("🚀 Starting Windows Login Tracker...")
    print("🪟 Detecting actual Windows login time for today...")
    print("⏰ Login time = When you logged into Windows today")
    print("⏰ Logout time = 9 hours from Windows login time")
    
    tracker = WindowsLoginTracker()
    tracker.run()

if __name__ == "__main__":
    main() 