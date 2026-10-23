import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='pyautogui-tools-15', log_file='autoclicker.log'):
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)
        
    return logger

# Instantiate a singleton-ish logger for the clicker context
app_logger = setup_logger()