import sys
import os
import logging
from auto_capture_login_tracker import AIWorkTracker
from tracker.singleton import SingleInstance

# --- Constants ---
APP_NAME = "AIWorkTracker"
LOGS_DIR = "logs"
LOG_FILE = os.path.join(LOGS_DIR, "app.log")

def setup_logging():
    """Configures centralized logging for the application."""
    # Ensure the logs directory exists
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # Configure logging to write to a file and the console
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout) # To see logs in console during development
        ]
    )
    logging.info("Logging configured.")

def handle_single_instance(is_unlock_trigger=False):
    """Checks if another instance is running and exits if so."""
    instance = SingleInstance(APP_NAME)
    if instance.is_running():
        if is_unlock_trigger:
            # This is a launch from the unlock task. Signal the main app to show its window.
            logging.info("Unlock trigger: Instance already running. Signaling it to show window.")
            signal_file = os.path.join(LOGS_DIR, "show_window.signal")
            with open(signal_file, "w") as f:
                f.write("show")
            sys.exit(0) # Exit silently
        else:
            # This is a manual launch. Inform the user that it's already running.
            logging.warning(f"Manual launch: An instance of {APP_NAME} is already running. Exiting.")
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw() # Hide the main window
                messagebox.showinfo("Already Running", f"The {APP_NAME} is already running. Check your system tray.")
            except Exception as e:
                logging.error(f"Could not show 'Already Running' dialog: {e}")
            sys.exit(1)
    return instance # Return the instance to keep the lock file

def main():
    """
    Main entry point for the AI Work Tracker application.
    """
    is_unlock_trigger = "--show-on-unlock" in sys.argv
    setup_logging()
    
    # Keep the instance object in scope to maintain the lock
    _instance = handle_single_instance(is_unlock_trigger=is_unlock_trigger)

    logging.info(f"🚀 Starting {APP_NAME}...")

    try:
        tracker = AIWorkTracker()
        tracker.run()
    except Exception as e:
        # Use logging to capture the full traceback for better debugging
        logging.critical("❌ An unexpected error occurred in the main application loop.", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()