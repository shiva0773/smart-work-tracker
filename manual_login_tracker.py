#!/usr/bin/env python3
"""
Manual Login Tracker
Allows you to set your actual login time manually
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import requests
from datetime import datetime, timedelta
import getpass

class ManualLoginTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🕒 Manual Login Tracker")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        self.root.attributes("-topmost", True)
        
        # Set dark theme
        self.root.configure(bg="#23272e")
        
        # Get today's login time
        self.login_time = self.get_todays_login_time()
        self.logout_time = self.login_time + timedelta(hours=9)
        
        # Save login time
        self.save_login_time()
        
        self.setup_ui()
        self.start_timer()
        
    def get_todays_login_time(self):
        """Get today's login time - ask user if not set"""
        today = datetime.now().strftime("%Y-%m-%d")
        login_file = "logs/manual_login.json"
        
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
                            print(f"📅 Found saved login time for today: {login_time}")
                            return login_time
            except Exception as e:
                print(f"⚠️ Error reading login file: {e}")
        
        # If no login time for today, ask user
        return self.ask_user_for_login_time()
    
    def ask_user_for_login_time(self):
        """Ask user to input their actual login time"""
        # Create a simple dialog to get login time
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Today's Login Time")
        dialog.geometry("300x200")
        dialog.configure(bg="#23272e")
        dialog.attributes("-topmost", True)
        dialog.grab_set()  # Make dialog modal
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        login_time_var = tk.StringVar()
        login_time_var.set("09:00")  # Default to 9 AM
        
        # Instructions
        tk.Label(dialog, text="What time did you log into Windows today?", 
                font=("Arial", 12, "bold"), fg="#fff", bg="#23272e").pack(pady=20)
        
        # Time input frame
        time_frame = tk.Frame(dialog, bg="#23272e")
        time_frame.pack(pady=10)
        
        tk.Label(time_frame, text="Login Time (HH:MM):", 
                font=("Arial", 10), fg="#fff", bg="#23272e").pack()
        
        time_entry = tk.Entry(time_frame, textvariable=login_time_var, 
                             font=("Arial", 14), width=10, justify="center")
        time_entry.pack(pady=5)
        time_entry.focus()
        
        # Buttons
        button_frame = tk.Frame(dialog, bg="#23272e")
        button_frame.pack(pady=20)
        
        def set_login_time():
            try:
                time_str = login_time_var.get()
                # Parse the time input
                if ":" in time_str:
                    hour, minute = map(int, time_str.split(":"))
                else:
                    # If just number, assume it's hour
                    hour, minute = int(time_str), 0
                
                # Create datetime for today with the specified time
                today = datetime.now().date()
                login_time = datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))
                
                print(f"✅ User set login time: {login_time}")
                dialog.destroy()
                return login_time
                
            except Exception as e:
                messagebox.showerror("Error", f"Invalid time format. Please use HH:MM (e.g., 09:30)")
                return None
        
        def use_current_time():
            current_time = datetime.now()
            print(f"✅ Using current time as login: {current_time}")
            dialog.destroy()
            return current_time
        
        # Buttons
        tk.Button(button_frame, text="Set Time", command=lambda: set_login_time(), 
                 font=("Arial", 10), fg="#23272e", bg="#4fc3f7").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Use Current Time", command=lambda: use_current_time(), 
                 font=("Arial", 10), fg="#23272e", bg="#81c784").pack(side=tk.LEFT, padx=5)
        
        # Wait for user input
        self.root.wait_window(dialog)
        
        # Return the login time (this will be set by the button callbacks)
        # For now, return current time as fallback
        return datetime.now()
    
    def save_login_time(self):
        """Save today's login time"""
        today = datetime.now().strftime("%Y-%m-%d")
        login_data = {
            "date": today,
            "login_time": self.login_time.strftime("%Y-%m-%d %H:%M:%S"),
            "logout_time": self.logout_time.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        os.makedirs("logs", exist_ok=True)
        with open("logs/manual_login.json", "w") as f:
            json.dump(login_data, f, indent=2)
        
        print(f"✅ Manual login time saved: {self.login_time}")
    
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
        title_label = tk.Label(main_frame, text="🕒 Manual Login Tracker", 
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
        
        # Manual login info
        login_frame = tk.Frame(main_frame, bg="#2c313c", bd=2, relief="ridge")
        login_frame.pack(pady=(0, 15), fill="x")
        
        self.login_info_label = tk.Label(login_frame, 
                                        text=f"📅 Your Login Time: {self.login_time.strftime('%I:%M %p')}", 
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
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg="#23272e")
        button_frame.pack(pady=(10, 0))
        
        minimize_btn = tk.Button(button_frame, text="Minimize", 
                                command=self.root.iconify, 
                                font=("Arial", 12), 
                                fg="#23272e", bg="#4fc3f7", 
                                activebackground="#81c784", activeforeground="#23272e")
        minimize_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(button_frame, text="Reset Login Time", 
                             command=self.reset_login_time, 
                             font=("Arial", 12), 
                             fg="#23272e", bg="#ff6b6b", 
                             activebackground="#ff8e8e", activeforeground="#23272e")
        reset_btn.pack(side=tk.LEFT, padx=5)
    
    def reset_login_time(self):
        """Reset the login time for today"""
        # Delete today's login file
        login_file = "logs/manual_login.json"
        if os.path.exists(login_file):
            os.remove(login_file)
        
        messagebox.showinfo("Reset", "Login time reset. Please restart the tracker to set a new time.")
        self.root.quit()
    
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
    print("🚀 Starting Manual Login Tracker...")
    print("📝 You can set your actual login time manually")
    print("⏰ Login time = Your actual login time")
    print("⏰ Logout time = 9 hours from login time")
    
    tracker = ManualLoginTracker()
    tracker.run()

if __name__ == "__main__":
    main() 