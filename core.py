import pyautogui
import time
import sys

class ClickerEngine:
    def __init__(self, interval=0.1, fail_safe=True):
        pyautogui.FAILSAFE = fail_safe
        self.interval = interval

    def execute(self, clicks):
        try:
            for i in range(clicks):
                x, y = pyautogui.position()
                if x < 0 or y < 0:
                    raise ValueError('cursor outside monitor boundaries')
                pyautogui.click(x, y)
                time.sleep(self.interval)
        except pyautogui.FailSafeException:
            print('emergency abort triggered by user')
        except Exception as e:
            self.graceful_degradation(e)

    def graceful_degradation(self, err):
        print(f'runtime anomaly detected: {err}')
        sys.exit(1)

def start_sequence(count):
    try:
        engine = ClickerEngine(interval=0.05)
        engine.execute(count)
    except KeyboardInterrupt:
        print('manual interruption received')

if __name__ == '__main__':
    start_sequence(100)