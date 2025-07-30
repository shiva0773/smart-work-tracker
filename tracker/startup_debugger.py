import sys
import os
from datetime import datetime

LOG_DIR = "logs"
ERROR_LOG_FILE = os.path.join(LOG_DIR, "startup_errors.log")

def setup_startup_logging():
    """
    Redirects stdout and stderr to a log file to capture all startup messages and errors.
    This is crucial for debugging auto-started applications.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Redirect stdout and stderr to the log file
        sys.stdout = open(ERROR_LOG_FILE, 'a', buffering=1, encoding='utf-8')
        sys.stderr = sys.stdout
        print(f"\n\n{'='*50}\nAPPLICATION START AT: {timestamp}\n{'='*50}")
    except IOError as e:
        # If we can't even open the log file, this will print to the original console
        print(f"CRITICAL: Could not open log file {ERROR_LOG_FILE}. Error: {e}", file=sys.__stderr__)