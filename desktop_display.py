import tkinter as tk
import json
from datetime import datetime, timedelta
import os

import requests
import config

LOGIN_LOG_FILE = os.path.join("logs", "auto_captured_login.json")
WORK_DURATION_HOURS = 9

def get_last_login():
    """Gets the login time from the single source of truth."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(LOGIN_LOG_FILE):
        try:
            with open(LOGIN_LOG_FILE, "r") as f:
                data = json.load(f)
                if data.get("date") == today_str:
                    login_str = data.get("login_time")
                    if login_str:
                        login_time = datetime.strptime(login_str, "%Y-%m-%d %H:%M:%S")
                        expected_logout = login_time + timedelta(hours=WORK_DURATION_HOURS)
                        return login_time, expected_logout, data.get("method", "unknown")
        except Exception as e:
            print(f"Error reading login file: {e}")
    return None, None, None

def show_login_popup():
    root = tk.Tk()
    root.title("🕒 Work Tracker - Daily Summary")
    # Set larger window size to fit all content
    window_width = 440
    window_height = 370
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(True, True)
    root.attributes("-topmost", True)

    # Set a dark gradient background using a Canvas
    canvas = tk.Canvas(root, width=window_width, height=window_height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    for i in range(window_height):
        r = int(30 + (0-30)*i/window_height)
        g = int(35 + (0-35)*i/window_height)
        b = int(50 + (0-50)*i/window_height)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, window_width, i, fill=color)

    # Centered frame for compact display, dark theme
    left_frame = tk.Frame(root, bg="#23272e", width=400, height=330)
    left_frame.place(relx=0.5, rely=0.5, anchor="center")
    left_frame.pack_propagate(False)

    def get_weather():
        """Get weather for the configured city, using config.py."""
        if not config.OPENWEATHER_API_KEY or "YOUR_API_KEY" in config.OPENWEATHER_API_KEY:
            print("⚠️ Weather API key not set in config.py. Skipping weather fetch.")
            return None
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={config.WEATHER_CITY}&appid={config.OPENWEATHER_API_KEY}&units=metric"
        
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()  # Raises an HTTPError for bad responses
            data = resp.json()
            return data.get('main', {}).get('temp')
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching weather: {e}")
        return None

    # Idle/Lock alert label
    alert_label = tk.Label(left_frame, text="", font=("Arial", 11, "bold"), fg="#ff6b6b", bg="#23272e")
    LOG_FILE = os.path.join("logs", "structured_log.json")
    alert_label.pack(pady=(0,5))

    def get_today_idle_lock():
        today_str = datetime.now().strftime('%Y-%m-%d')
        idle_time = 0
        lock_time = 0
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                try:
                    logs = json.load(f)
                    for entry in logs:
                        if entry.get('start_time', '').startswith(today_str):
                            if entry.get('event') == 'idle':
                                idle_time += entry.get('duration_seconds', 0)
                            elif entry.get('event') == 'lock':
                                lock_time += entry.get('duration_seconds', 0)
                except Exception:
                    pass
        return idle_time, lock_time
    # Show only weather info in right frame
    # Break reminder label removed
    login_time, logout_time, status = get_last_login()

    if not login_time:
        login_str = "N/A"
        logout_str = "N/A"
        status = "No login recorded"
    else:
        login_str = login_time.strftime("%Y-%m-%d %H:%M:%S")
        logout_str = logout_time.strftime("%Y-%m-%d %H:%M:%S")

    import random
    motivational_quotes = [
        "Believe you can and you're halfway there.",
        "Success is not for the lazy.",
        "Every day is a new opportunity.",
        "Stay positive, work hard, make it happen.",
        "Your only limit is you.",
        "Small steps every day lead to big results.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it.",
        "Don't watch the clock; do what it does. Keep going."
    ]
    greeting = random.choice(motivational_quotes)

    # Get weather temperature for Hyderabad
    temp = get_weather()
    weather_str = f" ({temp}°C)" if temp is not None else ""

    # Stack all elements vertically, centered, with minimal padding
    tk.Label(left_frame, text=greeting, font=("Arial", 13, "italic"), fg="#4fc3f7", bg="#23272e").pack(pady=(8,2))
    tk.Label(left_frame, text=f"👤 Hello, Shiva Gundra{weather_str}", font=("Arial", 18, "bold"), fg="#fff", bg="#23272e").pack(pady=(0,6))
    # Highlighted login/logout times (dark theme, centered, compact)
    login_frame = tk.Frame(left_frame, bg="#2c313c", bd=2, relief="ridge")
    login_frame.pack(pady=4)
    tk.Label(login_frame, text=f"Login Time: {login_str}", font=("Arial", 16, "bold"), fg="#4fc3f7", bg="#2c313c").pack(pady=(6,2), padx=8)
    tk.Label(login_frame, text=f"Expected Logout: {logout_str}", font=("Arial", 16, "bold"), fg="#81c784", bg="#2c313c").pack(pady=(2,6), padx=8)
    tk.Label(left_frame, text=f"Status: {status}", font=("Arial", 13, "italic"), fg="#fff", bg="#23272e").pack(pady=(2,8))

    # Progress bar for workday completion
    from tkinter import ttk
    progress_label = tk.Label(left_frame, text="Workday Progress:", font=("Arial", 14, "bold"), fg="#fff", bg="#23272e")
    progress_label.pack(pady=(0,0))
    progress_var = tk.DoubleVar()
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", troughcolor="#23272e", background="#4fc3f7", bordercolor="#23272e", lightcolor="#23272e", darkcolor="#23272e")
    progress_bar = ttk.Progressbar(left_frame, variable=progress_var, maximum=100, length=220, style="TProgressbar")
    progress_bar.pack(pady=(0,16))

    countdown_label = tk.Label(left_frame, text="", font=("Arial", 22, "bold"), fg="#81c784", bg="#23272e")
    countdown_label.pack(pady=(0,12))

    def update_countdown():
        # Weather info (update once at startup)
        # Weather now shown next to name, no label to update
        # Idle/Lock alerts
        idle_time, lock_time = get_today_idle_lock()
        idle_mins = idle_time // 60
        lock_mins = lock_time // 60
        if idle_mins >= 30:
            alert_label.config(text=f"⚠️ Idle time today: {idle_mins} min. Try to stay active!")
        elif lock_mins >= 30:
            alert_label.config(text=f"🔒 Lock time today: {lock_mins} min. Remember to stay engaged!")
        else:
            alert_label.config(text="")
        if login_time and logout_time:
            now = datetime.now()
            remaining = logout_time - now
            total = (logout_time - login_time).total_seconds()
            elapsed = (now - login_time).total_seconds()
            percent = max(0, min(100, (elapsed / total) * 100)) if total > 0 else 0
            progress_var.set(percent)
            if remaining.total_seconds() > 0:
                countdown = str(remaining).split('.')[0]
                countdown_label.config(text=f"Time left until logout: {countdown}")
            else:
                countdown_label.config(text="✅ 9 Hours Completed")

            # Break reminder removed
        root.after(1000, update_countdown)

    update_countdown()

    def minimize_window():
        root.iconify()

    minimize_btn = tk.Button(left_frame, text="Minimize", command=minimize_window, font=("Arial", 12), fg="#23272e", bg="#4fc3f7", activebackground="#81c784", activeforeground="#23272e")
    minimize_btn.pack(pady=(0,10))

    # root.after(10000, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    import sys
    print("="*60, file=sys.stderr)
    print("❌ ERROR: This script (desktop_display.py) is not the main application.", file=sys.stderr)
    print("   Please run 'main.py' to launch the full AI Work Tracker.", file=sys.stderr)
    print("="*60, file=sys.stderr)
    sys.exit(1)
