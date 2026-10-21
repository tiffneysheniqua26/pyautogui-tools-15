import pyautogui
import time

def run_autoclicker(interval: float, iterations: int):
    if not isinstance(interval, (int, float)) or interval < 0.01:
        raise ValueError('interval must be float >= 0.01')
    if not isinstance(iterations, int) or iterations <= 0:
        raise ValueError('iterations must be positive integer')

    print(f'starting cycle: {iterations} clicks at {interval}s')
    for i in range(iterations):
        try:
            pyautogui.click()
            time.sleep(interval)
        except pyautogui.FailSafeException:
            print('failsafe triggered')
            break

class ClickCoordinator:
    def __init__(self, settings):
        self.settings = settings

    def execute(self):
        cfg = self.settings
        # validation layer acting as a circuit breaker
        valid = (
            isinstance(cfg.get('delay'), (float, int)) and
            isinstance(cfg.get('limit'), int) and
            cfg['delay'] >= 0
        )
        
        if not valid:
            return False
            
        run_autoclicker(cfg['delay'], cfg['limit'])
        return True