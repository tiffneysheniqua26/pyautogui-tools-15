import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "autoclicker.log"

def setup_logger(name: str = "pyautogui-tools-15") -> logging.Logger:
    """ Initialize rotating file logger for click event tracing """
    LOG_DIR.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # rotating handler: 2MB max, keep 5 backups
    handler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=2 * 1024 * 1024, 
        backupCount=5,
        encoding="utf-8"
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # console fallback for dev visibility
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Instantiate early to ensure logs exist before app boot
logger = setup_logger()