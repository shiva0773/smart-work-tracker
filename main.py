import multiprocessing
import os
import time
import sys

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tracker.startup_debugger import setup_startup_logging
from tracker.idle_tracker import monitor_idle
from tracker.lock_tracker import monitor_lock
from tracker.app_tracker import track_active_window
from auto_capture_login_tracker import main as run_main_ui

def run_tracker(target_func, name):
    """Helper to run a tracker function in a process."""
    print(f"🚀 Starting {name}...")
    try:
        target_func()
    except KeyboardInterrupt:
        print(f"🛑 {name} stopped.")

def main():
    # This MUST be the first thing that runs to capture all errors
    setup_startup_logging()

    print("="*50)
    print("🤖 AI Work Tracker - Main Launcher")
    print("="*50)

    # Define background tracker processes
    trackers = {
        "Idle Monitor": monitor_idle,
        "Lock Monitor": monitor_lock,
        "App Monitor": track_active_window,
    }

    processes = []
    for name, func in trackers.items():
        process = multiprocessing.Process(target=run_tracker, args=(func, name), daemon=True)
        processes.append(process)
        process.start()
        time.sleep(0.5) # Stagger starts slightly

    print("\n✅ All background trackers are running.")
    print("🖥️  Launching main user interface...\n")

    # Run the main UI in the main process
    try:
        print("Attempting to initialize and run the main UI...")
        run_main_ui()
        print("Main UI process finished cleanly.")
    except KeyboardInterrupt:
        print("\nUI closed by user.")
    except Exception as e:
        import traceback
        print(f"\n💥 CRITICAL ERROR: The main UI failed to launch!\nError: {e}\n{traceback.format_exc()}")
    finally:
        print("\nShutting down background trackers...")
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join(timeout=2)
        print("✅ Application has been shut down cleanly.")

if __name__ == "__main__":
    # Required for multiprocessing on Windows
    multiprocessing.freeze_support()
    main()