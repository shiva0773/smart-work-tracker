import time
import ctypes
from datetime import datetime
import os
import sys

# Ensure the parent directory is in the path to find the log_writer module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tracker.log_writer import write_log

LOG_FILE = os.path.join("logs", "structured_log.json")

def is_system_locked():
    return ctypes.windll.user32.GetForegroundWindow() == 0

def monitor_lock(interval=5):
    was_locked = False
    lock_start_time = None

    while True:
        locked = is_system_locked()

        if locked and not was_locked:
            lock_start_time = datetime.now()
            was_locked = True
            print(f"{lock_start_time.strftime('%Y-%m-%d %H:%M:%S')} - System Locked")

        elif not locked and was_locked:
            lock_end_time = datetime.now()
            write_log(LOG_FILE, "lock", "System Locked", lock_start_time.strftime("%Y-%m-%d %H:%M:%S"), lock_end_time.strftime("%Y-%m-%d %H:%M:%S"))
            print(f"{lock_end_time.strftime('%Y-%m-%d %H:%M:%S')} - System Unlocked")
            was_locked = False

        time.sleep(interval)
