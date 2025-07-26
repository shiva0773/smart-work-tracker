import time
import ctypes
import datetime
from tracker.log_writer import write_log

def is_system_locked():
    return ctypes.windll.user32.GetForegroundWindow() == 0

def monitor_lock(interval=5):
    was_locked = False
    lock_start = None

    while True:
        locked = is_system_locked()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if locked and not was_locked:
            lock_start = now
            was_locked = True
            print(f"{now} - System Locked")

        elif not locked and was_locked:
            write_log("lock", "System Locked", lock_start, now)
            print(f"{now} - System Unlocked")
            was_locked = False

        time.sleep(interval)
