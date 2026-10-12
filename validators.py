import pyautogui
from typing import Tuple, Union

def validate_coordinates(x: int, y: int) -> Tuple[int, int]:
    screen_width, screen_height = pyautogui.size()
    safe_x = max(0, min(x, screen_width - 1))
    safe_y = max(0, min(y, screen_height - 1))
    return safe_x, safe_y

def check_bounds(coords: Tuple[int, int]) -> bool:
    x, y = coords
    return 0 <= x < pyautogui.size()[0] and 0 <= y < pyautogui.size()[1]

def normalize_interval(interval: Union[float, int]) -> float:
    return float(max(0.001, min(interval, 60.0)))

def sanitize_click_count(count: int) -> int:
    if count < 0:
        return 0
    return min(count, 1_000_000)

class ClickValidator:
    @staticmethod
    def verify_action(x: int, y: int, count: int) -> bool:
        return check_bounds((x, y)) and count > 0