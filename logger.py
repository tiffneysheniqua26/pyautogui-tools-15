import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='pyautogui-tools', log_file='autoclicker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Ensure log directory exists, even if path is relative
        os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)

        # Rotating file handler: 5 files of 1MB each
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=1_048_576, 
            backupCount=5
        )
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Also output to stdout for real-time monitoring
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Instantiate for quick access across package
log = get_logger()