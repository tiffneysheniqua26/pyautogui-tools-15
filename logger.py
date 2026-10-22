import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = Path('autoclicker.log')

class ColorFormatter(logging.Formatter):
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m', 'ERROR': '\033[91m'}
    def format(self, record):
        color = self.COLORS.get(record.levelname, '\033[0m')
        record.msg = f"{color}{record.msg}\033[0m"
        return super().format(record)

def setup_logger(name: str = 'pyautogui-tools') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(ColorFormatter('%(levelname)s: %(message)s'))
    logger.addHandler(console)
    
    # File handler with rotation (1MB per file, keep 3 backups)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger()