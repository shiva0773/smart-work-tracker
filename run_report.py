import sys
import logging
from pathlib import Path

from daily_report import send_daily_report

# --- Constants ---
LOGS_DIR = Path("logs")
LOG_FILE = LOGS_DIR / "app.log"

def setup_reporting_logging():
    """Configures logging for the report runner script."""
    LOGS_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [REPORT_RUNNER] - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, mode='a'), # Append to the main log file
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Entry point for the scheduled task to send the daily report."""
    setup_reporting_logging()
    logging.info("🚀 Scheduled task triggered: Attempting to send daily report.")
    try:
        send_daily_report()
        logging.info("✅ Daily report process finished successfully.")
    except Exception as e:
        logging.critical("❌ An unexpected error occurred while sending the daily report.", exc_info=True)

if __name__ == "__main__":
    main()