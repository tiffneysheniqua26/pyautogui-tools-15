import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = 'pyautogui-tools-15', log_file: str = 'autoclicker.log') -> logging.Logger:
    """
    Instantiates a moody, rotating logger for automated clicker events.
    It keeps a maximum of 5 files at 1MB each because we love efficiency.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Format with a custom flair for debugging click sequences
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )

        # Rotating handler ensures we don't consume the entire disk drive
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=1_048_576, 
            backupCount=5
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add a stream handler so we can watch the chaos in the console
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Instantiate the singleton instance for global module access
autoclicker_logger = setup_logger()