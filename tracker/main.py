import os
import sys
import logging
from PIL import Image, ImageDraw
from pystray import MenuItem as item, Icon as icon
import threading
import time
import json
from pathlib import Path

# --- Configuration ---
APP_NAME = "AIWorkTracker"
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"
LOGIN_TIME_FILE = LOG_DIR / "login_time.json"

# --- Setup Logging ---
# Ensure log directory exists
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout) # Also print to console for debugging
    ]
)

# --- Core Application Logic ---
class WorkTracker:
    def __init__(self):
        self.running = False
        self.thread = None
        self.login_time = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        logging.info("WorkTracker background thread started.")
        self.record_login_time()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2) # Wait for the thread to finish
        logging.info("WorkTracker background thread stopped.")

    def run(self):
        """Main loop for the tracker logic."""
        while self.running:
            # This is where your actual tracking logic would go.
            # For example, checking active window, user activity, etc.
            logging.info("Tracker is running...")
            time.sleep(60) # Example: do something every 60 seconds

    def record_login_time(self):
        try:
            self.login_time = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(LOGIN_TIME_FILE, 'w') as f:
                json.dump({"login_time": self.login_time}, f)
            logging.info(f"Login time recorded: {self.login_time}")
        except Exception as e:
            logging.error(f"Failed to record login time: {e}")

    def get_status(self):
        if self.running:
            return f"Running since: {self.login_time}"
        return "Not running."

# --- System Tray Icon ---
def create_image():
    """Creates a simple placeholder image for the tray icon."""
    width = 64
    height = 64
    # A simple green circle as a placeholder
    image = Image.new('RGB', (width, height), 'black')
    dc = ImageDraw.Draw(image)
    dc.ellipse([(4, 4), (width - 4, height - 4)], fill='green')
    return image

def on_quit(tray_icon, tracker_instance):
    logging.info("Quit action triggered.")
    tracker_instance.stop()
    tray_icon.stop()

def setup_tray_icon(tracker_instance):
    """Sets up and runs the system tray icon."""
    image = create_image()
    menu = (
        item('Status', lambda: logging.info(tracker_instance.get_status()), enabled=False),
        item('Quit', lambda: on_quit(tray_icon, tracker_instance))
    )
    tray_icon = icon(APP_NAME, image, APP_NAME, menu)
    
    logging.info("Starting tray icon.")
    # The `run` method is blocking, so it should be the last thing called.
    tray_icon.run()

# --- Autostart Setup (for Windows) ---
def setup_autostart():
    """
    Creates a batch file and a shortcut in the Windows Startup folder
    to run the application on login.
    """
    if sys.platform != 'win32':
        logging.warning("Autostart setup is only implemented for Windows.")
        print("Autostart setup is only for Windows. For macOS, use launchd. For Linux, use systemd or .desktop files.")
        return

    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        logging.error("Autostart setup requires 'winshell' and 'pywin32'. Please run: pip install winshell pywin32")
        print("Please run: pip install winshell pywin32")
        return

    startup_folder = winshell.startup()
    app_path = Path(__file__).resolve()
    python_exe = sys.executable
    
    batch_file_path = app_path.parent / "start_tracker.bat"
    shortcut_path = Path(startup_folder) / f"{APP_NAME}.lnk"

    with open(batch_file_path, "w") as f:
        pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
        f.write(f'@echo off\ncd /d "{app_path.parent}"\n"{pythonw_exe}" "{app_path}"\n')
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.Targetpath = str(batch_file_path)
    shortcut.WorkingDirectory = str(app_path.parent)
    shortcut.IconLocation = python_exe
    shortcut.save()

    logging.info(f"Autostart shortcut created at: {shortcut_path}")
    print(f"Successfully set up {APP_NAME} to run on startup.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--install-autostart':
        setup_autostart()
    else:
        logging.info(f"--- {APP_NAME} Started ---")
        try:
            tracker = WorkTracker()
            tracker.start()
            setup_tray_icon(tracker)
        except Exception as e:
            logging.critical(f"A critical error occurred: {e}", exc_info=True)
        finally:
            logging.info(f"--- {APP_NAME} Exited ---")