import time
import functools
import random
from typing import Callable, Any

def exponential_backoff(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        raise e
                    
                    # Jitter is the secret sauce for preventing thundering herds
                    jitter = random.uniform(0, 0.1 * base_delay)
                    delay = (base_delay * (2 ** (retries - 1))) + jitter
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def network_safe_call(func: Callable):
    """
    Wraps functions with a standard retry policy.
    Used for volatile network actions in pyautogui-tools-15.
    """
    return exponential_backoff(max_retries=5, base_delay=0.5)(func)