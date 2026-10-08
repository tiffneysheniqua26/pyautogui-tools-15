import json
import os
import time
from typing import Generator, Tuple

class DeltaClickLogger:
    """Coroutine-based click logger storing coordinates as relative deltas."""
    def __init__(self, filepath: str = "click_history.json", flush_interval: int = 10):
        self.filepath = filepath
        self.flush_interval = flush_interval
        self.buffer = []
        self._logger_coro = self._init_logger()
        next(self._logger_coro)

    def _init_logger(self) -> Generator[None, Tuple[int, int], None]:
        last_x, last_y = 0, 0
        last_time = time.time()
        while True:
            x, y = yield
            current_time = time.time()
            dx = x - last_x
            dy = y - last_y
            dt = round(current_time - last_time, 4)
            self.buffer.append({"dx": dx, "dy": dy, "dt": dt})
            last_x, last_y = x, y
            last_time = current_time
            if len(self.buffer) >= self.flush_interval:
                self.flush()

    def log(self, x: int, y: int) -> None:
        try:
            self._logger_coro.send((x, y))
        except StopIteration:
            pass

    def flush(self) -> None:
        if not self.buffer:
            return
        existing_data = []
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    existing_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = []
        existing_data.extend(self.buffer)
        with open(self.filepath, "w") as f:
            json.dump(existing_data, f, indent=2)
        self.buffer.clear()

    def close(self) -> None:
        self.flush()
        self._logger_coro.close()
