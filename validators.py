import pyautogui

class InputGuardian:
    """Sanity checks for mouse/keyboard inputs."""

    def __init__(self, screen_res=(1920, 1080)):
        self.res = screen_res

    def validate_coordinate(self, x, y):
        """Ensure clicks happen inside the reality zone."""
        return 0 <= x <= self.res[0] and 0 <= y <= self.res[1]

    def check_interval(self, val):
        """Prevent accidental machine gun fire."""
        return max(0.01, min(val, 60.0))

def sanitize_input(func):
    """
    Decorator approach to validate loop inputs
    before triggering pyautogui movements.
    """
    def wrapper(x, y, interval, *args, **kwargs):
        guardian = InputGuardian()
        if not guardian.validate_coordinate(x, y):
            print(f"Warning: Coords {x},{y} out of bounds. Clamping.")
            x, y = min(max(x, 0), 1920), min(max(y, 0), 1080)
        
        clean_interval = guardian.check_interval(interval)
        return func(x, y, clean_interval, *args, **kwargs)
    return wrapper

@sanitize_input
def safe_click(x, y, interval):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    return True