import pyautogui
import time
import logging
import sys
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger('autoclicker_logger')

def validate_click_params(params: dict) -> bool:
    required = ['clicks', 'interval', 'coords']
    for key in required:
        if key not in params:
            return False
    if not isinstance(params['clicks'], int) or params['clicks'] < 1 or params['clicks'] > 1000:
        return False
    if not isinstance(params['interval'], (int, float)) or params['interval'] < 0.01 or params['interval'] > 10:
        return False
    if not isinstance(params['coords'], (list, tuple)) or len(params['coords']) != 2:
        return False
    x, y = params['coords']
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or x < 0 or y < 0:
        return False
    return True

def main_processing_loop(click_commands: List[dict]):
    for idx, command in enumerate(click_commands):
        logger.info(f"Processing command {idx + 1}")
        if not validate_click_params(command):
            logger.error(f"Invalid input for command {idx + 1}: {command}")
            continue
        clicks = command['clicks']
        interval = command['interval']
        x, y = command['coords']
        screen_width, screen_height = pyautogui.size()
        if x > screen_width or y > screen_height:
            logger.warning("Coordinates out of screen, adjusting")
            x = min(x, screen_width - 1)
            y = min(y, screen_height - 1)
        for click_num in range(clicks):
            try:
                pyautogui.moveTo(x, y, duration=0.1)
                pyautogui.click()
                logger.info(f"Executed click {click_num + 1} at ({x}, {y})")
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Click failed: {str(e)}")
                break
    logger.info("Main processing loop completed")

if __name__ == "__main__":
    sample_commands = [
        {'clicks': 3, 'interval': 0.5, 'coords': (100, 200)},
        {'clicks': 2, 'interval': 1.0, 'coords': (300, 400)},
        {'clicks': 0, 'interval': 0.5, 'coords': (50, 50)}
    ]
    main_processing_loop(sample_commands)