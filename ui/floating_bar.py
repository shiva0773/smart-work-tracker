import sys
import getpass
import requests
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QWidget

# Use system_login_fetcher to get correct login time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from tracker.system_login_fetcher import get_latest_login_time

class WorkTrackerBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: #1e1e1e; border-radius: 14px; padding: 10px;")
        self.resize(950, 75)

        # Read login time from logs/login_time.json
        login_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "login_time.json")
        login_time = None
        if os.path.exists(login_json_path):
            try:
                import json
                with open(login_json_path, "r") as f:
                    data = json.load(f)
                    login_time_str = data.get("login_time")
                    if login_time_str:
                        login_time = datetime.strptime(login_time_str, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(f"Error reading login_time.json: {e}")
        if login_time is None:
            self.login_time = datetime.now().replace(microsecond=0)
        else:
            self.login_time = login_time.replace(microsecond=0)
        self.logout_time = self.login_time + timedelta(hours=9)

        self.init_ui()
        self.start_timer()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        row = QHBoxLayout()
        row.setSpacing(25)

        self.user_label = QLabel(f"👤 {getpass.getuser()}")
        self.user_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.user_label.setStyleSheet("color: #00ff99;")
        row.addWidget(self.user_label)

        self.login_label = QLabel(f"🔓 Login: {self.login_time.strftime('%I:%M %p')}")
        self.login_label.setFont(QFont("Segoe UI", 13))
        self.login_label.setStyleSheet("color: #66d9ef;")
        row.addWidget(self.login_label)

        self.logout_label = QLabel(f"🔒 Logout: {self.logout_time.strftime('%I:%M %p')}")
        self.logout_label.setFont(QFont("Segoe UI", 13))
        self.logout_label.setStyleSheet("color: #fd971f;")
        row.addWidget(self.logout_label)

        self.countdown_label = QLabel("")
        self.countdown_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.countdown_label.setStyleSheet("color: #f92672;")
        row.addWidget(self.countdown_label)

        row.addStretch()

        self.weather_label = QLabel("🌤️ Loading...")
        self.weather_label.setFont(QFont("Segoe UI", 13))
        self.weather_label.setStyleSheet("color: #ffd700;")
        row.addWidget(self.weather_label)

        self.clock_label = QLabel()
        self.clock_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.clock_label.setStyleSheet("color: #a6e22e;")
        row.addWidget(self.clock_label)

        layout.addLayout(row)
        self.setLayout(layout)

        self.move(300, 20)

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)
        self.update_info()

    def get_weather(self):
        """Get weather for the configured city."""
        if not config.OPENWEATHER_API_KEY or "YOUR_API_KEY" in config.OPENWEATHER_API_KEY:
            print("⚠️ Weather API key not set in config.py. Skipping weather fetch.")
            return "🌤️ --°C"
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={config.WEATHER_CITY}&appid={config.OPENWEATHER_API_KEY}&units=metric"
        
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            temp = data.get('main', {}).get('temp')
            if temp is not None:
                return f"🌤️ {temp}°C"
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching weather: {e}")
        return "🌤️ --°C"

    def update_info(self):
        now = datetime.now()
        remaining = self.logout_time - now

        # Update weather every 5 minutes
        if not hasattr(self, 'last_weather_update') or (now - self.last_weather_update).total_seconds() > 300:
            self.weather_label.setText(self.get_weather())
            self.last_weather_update = now

        self.clock_label.setText(f"🕒 {now.strftime('%I:%M:%S %p')}")
        if remaining.total_seconds() > 0:
            self.countdown_label.setText(f"⏳ {str(remaining).split('.')[0]}")
        else:
            self.countdown_label.setText("✅ 9 Hours Completed")


if __name__ == "__main__":
    import sys
    print("="*60, file=sys.stderr)
    print("❌ ERROR: This script (floating_bar.py) is not the main application.", file=sys.stderr)
    print("   Please run 'main.py' to launch the full AI Work Tracker.", file=sys.stderr)
    print("="*60, file=sys.stderr)
    sys.exit(1)
    # app = QApplication(sys.argv)
    # tracker = WorkTrackerBar()
    # tracker.show()
    # sys.exit(app.exec_())
