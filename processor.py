import time
import random
import functools
from typing import Callable, Any

def backoff_retry(max_attempts: int = 3, base_delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

class NetworkProcessor:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    @backoff_retry(max_attempts=4)
    def sync_autoclicker_config(self, url: str):
        print(f"Syncing payload from {url}...")
        # Simulated unstable network call
        if random.random() < 0.7:
            raise ConnectionError("Unstable network link detected")
        return {"status": "success", "payload": "authorized"}

    def run_safe_sync(self, url: str):
        try:
            return self.sync_autoclicker_config(url)
        except Exception as e:
            print(f"Critical failure after retries: {e}")
            return None