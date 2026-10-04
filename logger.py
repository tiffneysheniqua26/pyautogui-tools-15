import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def setup_logger(name='pyautogui_tools', log_file='autoclicker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s'
    )

    # Console output for real-time visibility
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file handler (5MB per file, keep 3 backups)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Adding a subtle trick: logging system state if logs are missing
    if not os.path.exists(log_file):
        logger.info('Initialized fresh log file for pyautogui-tools-15 session')

    return logger

# Singleton-ish instance for easy import throughout the project
app_logger = setup_logger()