import pyautogui
import time
import logging

class ClickHandler:
    def __init__(self, interval: float = 0.1):
        self.interval = interval
        self.running = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('pyautogui-tools-15')

    def toggle_state(self):
        self.running = not self.running
        self.logger.info(f'State transitioned to: {self.running}')

    def execute_click_loop(self, duration: int):
        end_time = time.time() + duration
        self.logger.info('Starting click orchestration')
        try:
            while self.running and time.time() < end_time:
                pyautogui.click()
                time.sleep(self.interval)
        except pyautogui.FailSafeException:
            self.logger.warning('Fail-safe triggered, halting operations')
            self.running = False

    @staticmethod
    def validate_screen_coordinates(x: int, y: int) -> bool:
        screen_w, screen_h = pyautogui.size()
        return 0 <= x <= screen_w and 0 <= y <= screen_h

    def execute_targeted_sequence(self, x: int, y: int, count: int):
        if not self.validate_screen_coordinates(x, y):
            raise ValueError('Coordinate mapping error')
        
        for _ in range(count):
            pyautogui.click(x=x, y=y)
            time.sleep(self.interval)