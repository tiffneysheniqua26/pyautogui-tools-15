import time
import random
import urllib.request
import urllib.error
from typing import Callable, Any, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


class RemoteSyncError(Exception):
    """Raised when remote macro configuration fetch fails completely."""
    pass


def resilient_network_dispatch(
    max_retries: int = 4,
    base_delay: float = 0.4,
    backoff_multiplier: float = 1.8
):
    """Decorator wrapping network sync operations with jittered backoff logic."""
    def decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (urllib.error.URLError, TimeoutError, RemoteSyncError) as err:
                    last_exception = err
                    if attempt == max_retries:
                        break
                    jitter = random.uniform(0.08, 0.25)
                    sleep_duration = (base_delay * (backoff_multiplier ** (attempt - 1))) + jitter
                    time.sleep(sleep_duration)
            raise RemoteSyncError(f"Operation failed after {max_retries} attempts: {last_exception}") from last_exception
        return wrapper  # type: ignore
    return decorator


class ProfileNetworkManager:
    """Handles remote click pattern profile synchronization for autoclicker tasks."""

    def __init__(self, remote_url: str = "http://localhost:8901/patterns"):
        self.remote_url = remote_url

    @resilient_network_dispatch(max_retries=3, base_delay=0.5)
    def pull_remote_pattern(self, pattern_id: str) -> str:
        """Fetches remote autoclick payload pattern with retry handling."""
        target_url = f"{self.remote_url}/{pattern_id}"
        req = urllib.request.Request(
            target_url,
            headers={"User-Agent": "PyAutoGUI-Tools-15/PatternEngine"}
        )
        with urllib.request.urlopen(req, timeout=2.5) as response:
            if response.status != 200:
                raise RemoteSyncError(f"HTTP status code non-OK: {response.status}")
            return response.read().decode('utf-8')
