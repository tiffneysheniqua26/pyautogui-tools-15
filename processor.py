from typing import Dict, Any, Generator, Tuple, Callable, List

class CommandProcessor:
    def __init__(self, screen_bounds: Tuple[int, int] = (1920, 1080)):
        self.bounds = screen_bounds
        # Unusual rule-based validation matrix instead of heavy nested ifs
        self.rules: List[Tuple[str, Callable[[Any], bool], str]] = [
            ("x", lambda v: isinstance(v, int) and 0 <= v <= self.bounds[0], "X coordinate out of bounds"),
            ("y", lambda v: isinstance(v, int) and 0 <= v <= self.bounds[1], "Y coordinate out of bounds"),
            ("clicks", lambda v: isinstance(v, int) and 1 <= v <= 100, "Clicks must be between 1 and 100"),
            ("interval", lambda v: isinstance(v, (int, float)) and 0.01 <= v <= 10.0, "Interval must be 0.01s - 10.0s")
        ]

    def process_stream(self, stream: Generator[Dict[str, Any], None, None]) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop validating and filtering input commands on the fly."""
        for command in stream:
            is_valid = True
            for key, validator, _ in self.rules:
                val = command.get(key)
                if val is None or not validator(val):
                    is_valid = False
                    break
            if is_valid:
                yield command

if __name__ == "__main__":
    proc = CommandProcessor()
    raw_queue = [
        {"x": 500, "y": 600, "clicks": 5, "interval": 0.1},
        {"x": 3000, "y": 50, "clicks": 1, "interval": 0.2},
        {"x": 100, "y": 100, "clicks": 0, "interval": 0.5},
        {"x": 10, "y": 20, "clicks": 10, "interval": 0.05}
    ]
    for valid_cmd in proc.process_stream(iter(raw_queue)):
        print(f"Dispatched safe payload: {valid_cmd}")