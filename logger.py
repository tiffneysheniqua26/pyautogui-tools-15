import logging
import pyautogui
import time
from functools import wraps

def get_autoclicker_logger(log_level=logging.INFO):
    logger = logging.getLogger("autoclicker")
    logger.setLevel(log_level)
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler("autoclicker.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger

def log_click(logger, x, y, button="left", clicks=1):
    logger.info(f"Click action: {clicks} {button} click(s) at ({x}, {y})")
    pyautogui.click(x, y, button=button, clicks=clicks)
    logger.debug("Click action executed without errors")

def log_mouse_move(logger, x, y, duration=0.0):
    logger.info(f"Mouse move to position ({x}, {y}) in {duration} seconds")
    pyautogui.moveTo(x, y, duration=duration)
    logger.debug("Mouse has reached target position")

def log_pause(logger, duration):
    logger.info(f"Pausing for {duration} seconds")
    time.sleep(duration)
    logger.info("Pause completed, resuming operations")

def log_action_with_timing(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Commencing timed action: {func.__name__}")
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"Timed action {func.__name__} finished after {elapsed:.2f} seconds")
            return result
        return wrapper
    return decorator

def safe_click_with_log(logger, x, y, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            log_click(logger, x, y)
            return True
        except Exception as error:
            logger.warning(f"Click attempt {attempt} failed: {error}")
            time.sleep(0.2)
    logger.error("All click attempts exhausted, operation aborted")
    return False