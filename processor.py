import pyautogui
import time

class ClickProcessor:
    def __init__(self, interval, duration):
        self.interval = interval
        self.duration = duration

    def _sanitize(self, val, min_val=0.01, max_val=60.0):
        try:
            clean = float(val)
            return max(min_val, min(clean, max_val))
        except (ValueError, TypeError):
            return min_val

    def run_cycle(self, x, y):
        safe_x = self._sanitize(x, 0, 10000)
        safe_y = self._sanitize(y, 0, 10000)
        
        pyautogui.click(x=safe_x, y=safe_y)
        time.sleep(self.interval)

    def start_loop(self, iterations=100):
        for _ in range(int(iterations)):
            try:
                self.run_cycle(pyautogui.position().x, pyautogui.position().y)
            except pyautogui.FailSafeException:
                print("Emergency abort triggered.")
                break
            except Exception as e:
                print(f"Glitch in the matrix: {e}")

if __name__ == '__main__':
    bot = ClickProcessor(0.5, 0.1)
    bot.start_loop(10)