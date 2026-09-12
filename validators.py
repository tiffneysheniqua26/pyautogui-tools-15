import time
import functools
from typing import Callable, Any

def with_retry(max_attempts: int = 3, backoff: float = 0.5):
    """Decorator for resilience against transient network flickers."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    time.sleep(backoff * (2 ** attempt))
            raise last_ex
        return wrapper
    return decorator

def validate_connection_payload(payload: Any) -> bool:
    """Check if autoclicker instruction packets are valid."""
    if not isinstance(payload, dict):
        return False
    required = {'x', 'y', 'interval'}
    return all(key in payload for key in required) and all(isinstance(v, (int, float)) for v in payload.values())

class NetworkValidator:
    """Static state checker for connection integrity."""
    @staticmethod
    def probe(endpoint: str) -> bool:
        try:
            import socket
            with socket.create_connection((endpoint, 80), timeout=2):
                return True
        except (OSError, ValueError):
            return False