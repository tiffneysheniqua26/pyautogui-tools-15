import logging
from logging.handlers import RotatingFileHandler
import os

def get_autoclicker_logger(name='pyautogui-tools'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f'{name}.log')
    
    # rotating handler: max 1MB per file, keep 3 backups
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024, 
        backupCount=3
    )
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        # extra console output for dev vibes
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Instantiate the singleton instance for quick import
logger = get_autoclicker_logger()