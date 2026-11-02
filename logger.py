import logging
import os
from logging.handlers import RotatingFileHandler

def setup_autoclicker_logger(name: str = 'pyautogui-tools-15', log_dir: str = 'logs') -> logging.Logger:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_path = os.path.join(log_dir, f'{name}.log')
    
    # rotating handler: max 2MB per file, keep 3 backups
    handler = RotatingFileHandler(
        file_path, 
        maxBytes=2 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger

log = setup_autoclicker_logger()