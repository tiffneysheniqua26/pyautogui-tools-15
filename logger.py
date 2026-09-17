import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='pyautogui-tools', log_file='autoclicker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Dynamic singleton logger instance for the tool
app_logger = setup_logger()