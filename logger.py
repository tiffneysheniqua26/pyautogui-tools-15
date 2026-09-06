import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class ClickerLogger:
    def __init__(self, name='pyautogui-tools', log_dir='logs'):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Rotating file handler: 5MB per file, keep 3 backups
        file_path = os.path.join(log_dir, f'session_{datetime.now().strftime("%Y%m%d")}.log')
        handler = RotatingFileHandler(
            file_path, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        handler.setFormatter(fmt)

        console = logging.StreamHandler()
        console.setFormatter(fmt)

        if not self.logger.handlers:
            self.logger.addHandler(handler)
            self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

# Singleton-ish instance for easy import
app_logger = ClickerLogger().get_logger()