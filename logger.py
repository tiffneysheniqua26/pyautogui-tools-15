import os
import logging
from logging.handlers import RotatingFileHandler

try:
    import pyautogui
except ImportError:
    class DummyPyAutoGUI:
        def position(self):
            return (0, 0)
    pyautogui = DummyPyAutoGUI()

class AutoclickerTelemetryFilter(logging.Filter):
    """Injects current mouse coordinates dynamically into every log message."""
    def filter(self, record):
        x, y = pyautogui.position()
        record.mouse_pos = f"X:{x:04d},Y:{y:04d}"
        return True

class ClickCountRotatingHandler(RotatingFileHandler):
    """Rotates log files based on file size or raw click event count thresholds."""
    def __init__(self, filename, maxBytes=1048576, backupCount=5, click_limit=5000, **kwargs):
        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount, **kwargs)
        self.click_limit = click_limit
        self._click_counter = 0

    def emit(self, record):
        super().emit(record)
        if "click" in record.getMessage().lower():
            self._click_counter += 1
            if self._click_counter >= self.click_limit:
                self.doRollover()
                self._click_counter = 0

def setup_autoclicker_logger(log_file="autoclicker.log", max_bytes=512000, backup_count=3, click_limit=1000):
    logger = logging.getLogger("pyautogui_tools")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(mouse_pos)s] %(message)s',
        datefmt='%H:%M:%S'
    )

    rotating_handler = ClickCountRotatingHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        click_limit=click_limit,
        encoding='utf-8'
    )
    rotating_handler.setFormatter(formatter)
    rotating_handler.addFilter(AutoclickerTelemetryFilter())

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(AutoclickerTelemetryFilter())

    logger.addHandler(rotating_handler)
    logger.addHandler(console_handler)
    return logger