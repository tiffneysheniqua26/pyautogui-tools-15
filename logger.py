import logging
import sys
from datetime import datetime

class ClickLogger:
    def __init__(self, name='pyautogui-tools-15'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        fmt = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(fmt)
        self.logger.addHandler(console)

    def log_action(self, msg: str):
        self.logger.info(f'[ACTION] {msg}')

    def log_error(self, msg: str):
        self.logger.error(f'[FAILURE] {msg}')

    def log_performance(self, duration: float):
        self.logger.debug(f'[METRIC] execution took {duration:.4f}s')

# Singleton pattern for global access
logger_instance = ClickLogger()

def get_logger():
    return logger_instance