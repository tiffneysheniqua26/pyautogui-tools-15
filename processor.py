import time
from typing import Generator, Any, Dict, Callable

try:
    import pyautogui
except ImportError:
    class PyAutoGUIStub:
        @staticmethod
        def click(x: int, y: int, button: str = 'left'):
            pass
        @staticmethod
        def size():
            return (1920, 1080)
    pyautogui = PyAutoGUIStub()


class PayloadValidationError(ValueError):
    """Custom exception for input validation failures in processing pipeline."""
    pass


class ClickStreamProcessor:
    def __init__(self, max_screen_bounds: tuple[int, int] = None):
        screen_w, screen_h = pyautogui.size()
        self.limit_x = max_screen_bounds[0] if max_screen_bounds else screen_w
        self.limit_y = max_screen_bounds[1] if max_screen_bounds else screen_h
        self.allowed_buttons = {'left', 'right', 'middle', 'primary', 'secondary'}
        
        self._rules: Dict[str, Callable[[Any], bool]] = {
            'x': lambda v: isinstance(v, int) and 0 <= v <= self.limit_x,
            'y': lambda v: isinstance(v, int) and 0 <= v <= self.limit_y,
            'interval': lambda v: isinstance(v, (int, float)) and 0.001 <= v <= 3600.0,
            'button': lambda v: isinstance(v, str) and v.lower() in self.allowed_buttons,
            'repeat': lambda v: isinstance(v, int) and 1 <= v <= 1000,
        }

    def _validate_command(self, raw_data: Any) -> Dict[str, Any]:
        if not isinstance(raw_data, dict):
            raise PayloadValidationError(f"Expected dict payload, got {type(raw_data).__name__}")

        validated = {}
        defaults = {'interval': 0.1, 'button': 'left', 'repeat': 1}

        for field, check_fn in self._rules.items():
            if field in raw_data:
                value = raw_data[field]
                if not check_fn(value):
                    raise PayloadValidationError(f"Field '{field}' failed validation with value: {value!r}")
                validated[field] = value
            elif field in ('x', 'y'):
                raise PayloadValidationError(f"Missing required spatial coordinate '{field}'")
            else:
                validated[field] = defaults[field]
        return validated

    def execute_stream(self, input_stream: Generator[Dict[str, Any], None, None]) -> int:
        executed_count = 0
        for raw_instruction in input_stream:
            try:
                cmd = self._validate_command(raw_instruction)
            except PayloadValidationError as err:
                continue

            time.sleep(cmd['interval'])
            for _ in range(cmd['repeat']):
                pyautogui.click(x=cmd['x'], y=cmd['y'], button=cmd['button'])
            executed_count += 1

        return executed_count
