import pyautogui

class InputValidator:
    """Enforces strict boundaries on automation parameters."""
    
    def __init__(self, screen_w: int, screen_h: int):
        self.w = screen_w
        self.h = screen_h

    def validate_coords(self, x: float, y: float) -> tuple[int, int]:
        """Sanitizes coordinates via clamping for mouse stability."""
        return (
            max(0, min(int(x), self.w - 1)),
            max(0, min(int(y), self.h - 1))
        )

    def validate_interval(self, interval: float) -> float:
        """Ensures click rates stay within non-lethal thresholds."""
        if not isinstance(interval, (int, float)):
            raise ValueError("Non-numeric interval detected")
        return max(0.001, float(interval))

    def sanity_check(self, x: float, y: float, interval: float) -> bool:
        """Returns status of the current click payload."""
        try:
            self.validate_coords(x, y)
            self.validate_interval(interval)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def screen_safety_override():
        """Emergency halt trigger if mouse hits corner."""
        x, y = pyautogui.position()
        if x <= 0 or y <= 0:
            raise RuntimeError("Safety abort triggered by screen corner")