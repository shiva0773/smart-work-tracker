import ctypes
import time
from datetime import datetime
import os
import sys

# Ensure the parent directory is in the path to find the log_writer module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tracker.log_writer import write_log

LOG_FILE = os.path.join("logs", "structured_log.json")
IDLE_THRESHOLD_SECONDS = 60 * 5 # 5 minutes

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_time_seconds():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

def monitor_idle():
    is_idle = False
    idle_start_time = None

    while True:
        idle_time = get_idle_time_seconds()

        if idle_time >= IDLE_THRESHOLD_SECONDS and not is_idle:
            idle_start_time = datetime.now()
            is_idle = True
            print(f"{idle_start_time.strftime('%Y-%m-%d %H:%M:%S')} - Idle started")

        elif idle_time < IDLE_THRESHOLD_SECONDS and is_idle:
            idle_end_time = datetime.now()
            write_log(LOG_FILE, "idle", "User Idle", idle_start_time.strftime("%Y-%m-%d %H:%M:%S"), idle_end_time.strftime("%Y-%m-%d %H:%M:%S"))
            print(f"{idle_end_time.strftime('%Y-%m-%d %H:%M:%S')} - Idle ended")
            is_idle = False

        time.sleep(10)
