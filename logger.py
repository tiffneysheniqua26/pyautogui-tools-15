import functools
import json
import time
from typing import Callable, Generator


class AutoclickLogger:

    def __init__(self, filepath: str = "autoclick.log"):
        self.filepath = filepath
        open(self.filepath, "w").close()

    def log_action(self, action_name: str):
        def decorator(func: Callable[..., Generator]):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                gen = func(*args, **kwargs)
                try:
                    while True:
                        coords = next(gen)
                        duration = time.perf_counter() - start
                        log_entry = {
                            "action": action_name,
                            "params": {
                                "coords": coords,
                                "elapsed": round(duration, 4),
                            },
                            "status": "success",
                        }
                        self._write(log_entry)
                except StopIteration as e:
                    return e.value
                except Exception as e:
                    self._write(
                        {"action": action_name, "status": "error", "error": str(e)}
                    )
                    raise e

            return wrapper

        return decorator

    def _write(self, data: dict):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
