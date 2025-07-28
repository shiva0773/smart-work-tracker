from tracker.startup_log import log_system_start
from desktop_display import show_login_popup
import os
import time

def main():
    # Step 1: Log system login time (11 AM)
    log_system_start()
    print("✅ System login time logged at 11:00 AM.")

    # Step 2: Start tracking logic here (keep this script running)
    print("📊 Running AI Work Tracker... Press Ctrl+C to simulate shutdown.\n")
    try:
        while True:
            time.sleep(60)  # Simulate idle loop; replace with actual tracking logic
    except KeyboardInterrupt:
        print("⛔ Simulating system shutdown by user...")
        from tracker.shutdown_log import log_system_shutdown
        log_system_shutdown()

if __name__ == "__main__":
    main()

show_login_popup()