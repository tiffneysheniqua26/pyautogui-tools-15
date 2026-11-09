import random
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Optional


class NetworkRetryHandler:
    """Generator-based retry executor for remote autoclicker telemetry and sync."""

    def __init__(self, max_retries: int = 4, base_delay: float = 0.3, factor: float = 2.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.factor = factor

    def _jitter_schedule(self):
        current = self.base_delay
        for _ in range(self.max_retries):
            yield current + random.uniform(0.05, 0.25)
            current *= self.factor

    def run(self, action: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        schedule = self._jitter_schedule()
        last_err: Optional[Exception] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                return action(*args, **kwargs)
            except (urllib.error.URLError, TimeoutError, ConnectionResetError) as err:
                last_err = err
                try:
                    time.sleep(next(schedule))
                except StopIteration:
                    break

        raise RuntimeError(f"Network retry exhausted after {self.max_retries} attempts: {last_err}")


def fetch_remote_script(url: str, timeout: float = 2.5) -> str:
    executor = NetworkRetryHandler(max_retries=3, base_delay=0.1)

    def _request():
        req = urllib.request.Request(url, headers={"User-Agent": "PyAutoGUI-Tools/15.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")

    return str(executor.run(_request))
