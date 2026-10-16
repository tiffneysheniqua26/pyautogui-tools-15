import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='pyautogui-tools-15', log_file='autoclicker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Rotation logic: 2MB per file, keep 3 backups
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=2*1024*1024, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Quick access factory instance
clicker_logger = setup_logger()