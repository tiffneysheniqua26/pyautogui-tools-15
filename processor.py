import time
import functools
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    time.sleep(delay * (2 ** attempt))
            raise last_exception
        return wrapper
    return decorator

class NetworkProcessor:
    """Automated network clicker synchronization tool."""
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    @retry_operation(max_attempts=3, delay=0.5)
    def fetch_click_coords(self) -> dict:
        import requests
        response = requests.get("http://localhost:8080/coords", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

def sync_session_coordinates(processor: NetworkProcessor) -> None:
    try:
        data = processor.fetch_click_coords()
        print(f"Sync complete: {data}")
    except Exception as e:
        print(f"Critical network failure after retries: {e}")