import pyautogui
import time

class InputHandler:
    def __init__(self, interval: float, clicks: int):
        self.interval = self._validate_positive(interval, 0.1)
        self.clicks = self._validate_positive(clicks, 1)

    def _validate_positive(self, value, fallback):
        try:
            val = float(value)
            return val if val > 0 else fallback
        except (ValueError, TypeError):
            return fallback

    def run_click_sequence(self):
        print(f"Initiating {self.clicks} clicks with {self.interval}s interval")
        for i in range(int(self.clicks)):
            try:
                x, y = pyautogui.position()
                if not (0 <= x <= 10000 and 0 <= y <= 10000):
                    raise ValueError("Coordinates out of bounds")
                pyautogui.click(x, y)
                time.sleep(self.interval)
            except Exception as e:
                print(f"Execution aborted at cycle {i}: {e}")
                break

if __name__ == "__main__":
    # Example injection: creative sanitization of user input
    user_input = {"speed": "0.5", "count": "10"}
    handler = InputHandler(
        interval=user_input.get("speed", 0.5),
        clicks=user_input.get("count", 1)
    )
    handler.run_click_sequence()