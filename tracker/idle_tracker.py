import ctypes
import time
import datetime
from tracker.log_writer import write_log

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_time_seconds():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

def monitor_idle(threshold=60):
    is_idle = False
    idle_start = None

    while True:
        idle_time = get_idle_time_seconds()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if idle_time >= threshold and not is_idle:
            idle_start = now
            is_idle = True
            print(f"{now} - Idle started")

        elif idle_time < threshold and is_idle:
            write_log("idle", "User Idle", idle_start, now)
            print(f"{now} - Idle ended")
            is_idle = False

        time.sleep(5)
