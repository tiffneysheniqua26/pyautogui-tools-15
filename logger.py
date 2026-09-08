import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "pyautogui_tools.log"

class ClickerFormatter(logging.Formatter):
    """Custom formatting for clicker events."""
    formats = {
        logging.DEBUG: "[DEBUG] %(asctime)s - %(message)s",
        logging.INFO: "[INFO] %(asctime)s - %(message)s",
        logging.WARNING: "[WARN] %(asctime)s - %(message)s",
        logging.ERROR: "[ERROR] %(asctime)s - %(message)s"
    }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger(name: str = "clicker_app") -> logging.Logger:
    """Init logger with file rotation mechanism."""
    LOG_DIR.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = RotatingFileHandler(
            LOG_FILE, maxBytes=1024*1024*5, backupCount=3
        )
        handler.setFormatter(ClickerFormatter())
        
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(ClickerFormatter())
        
        logger.addHandler(handler)
        logger.addHandler(console)

    return logger