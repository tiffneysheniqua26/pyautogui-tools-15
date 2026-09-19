import pyautogui
import time
from typing import Tuple

def validate_coordinates(x: int, y: int) -> Tuple[int, int]:
    screen_width, screen_height = pyautogui.size()
    safe_x = max(0, min(x, screen_width - 1))
    safe_y = max(0, min(y, screen_height - 1))
    return int(safe_x), int(safe_y)

def run_clicker_loop(coords: list, interval: float):
    if not isinstance(interval, (int, float)) or interval < 0.01:
        interval = 0.1
    
    try:
        while True:
            for point in coords:
                try:
                    x, y = validate_coordinates(point[0], point[1])
                    pyautogui.click(x, y)
                    time.sleep(interval)
                except (TypeError, IndexError):
                    continue
    except KeyboardInterrupt:
        print("loop terminated by user")

if __name__ == '__main__':
    # Example injection: raw input stream simulation
    stream = [(100, 100), (9999, 9999), ('invalid', 50)]
    run_clicker_loop(stream, 0.5)