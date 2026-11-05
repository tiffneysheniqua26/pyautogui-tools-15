import logging
from logging.handlers import RotatingFileHandler
import os

def setup_autoclicker_logger():
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_path = os.path.join(log_directory, 'autoclicker.log')
    
    logger = logging.getLogger('pyautogui-tools-15')
    logger.setLevel(logging.DEBUG)

    # Unusual format for a clicker: show mouse coordinates in every log line
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [CURSOR-TRACKER] %(message)s'
    )

    # 5MB rotation, keeps 3 backups
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_autoclicker_logger()