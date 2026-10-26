import logging
import sys
from datetime import datetime

class ClickerLogger:
    def __init__(self, name: str = 'pyautogui-tools-15'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._setup_handlers()

    def _setup_handlers(self):
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
        
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

    def log_action(self, action_type: str, coords: tuple):
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        self.logger.info(f'[{action_type.upper()}] @ ({coords[0]}, {coords[1]}) at {timestamp}')

    def log_error(self, message: str):
        self.logger.error(f'CRITICAL FAILURE: {message}')

    @staticmethod
    def get_instance():
        if not hasattr(ClickerLogger, '_instance'):
            ClickerLogger._instance = ClickerLogger()
        return ClickerLogger._instance