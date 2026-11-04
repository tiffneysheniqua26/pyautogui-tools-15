import functools
import random
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Tuple, Type


def _fibonacci_jitter_backoff(base_delay: float = 0.5):
    a, b = 1, 1
    while True:
        jitter = random.uniform(0.85, 1.15)
        yield (a * base_delay) * jitter
        a, b = b, a + b


def resilient_network_op(
    max_attempts: int = 4,
    backoff_base: float = 0.4,
    catch_exceptions: Tuple[Type[Exception], ...] = (
        urllib.error.URLError,
        TimeoutError,
        ConnectionResetError,
    ),
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff_gen = _fibonacci_jitter_backoff(backoff_base)
            last_err = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as exc:
                    last_err = exc
                    if attempt == max_attempts:
                        break
                    delay = next(backoff_gen)
                    time.sleep(delay)
            raise RuntimeError(
                f"Operation '{func.__name__}' failed after {max_attempts} retries: {last_err}"
            ) from last_err

        return wrapper

    return decorator


@resilient_network_op(max_attempts=3, backoff_base=0.2)
def fetch_remote_macro(url: str, timeout: int = 3) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "PyAutoGUI-Tools-15/MacroSync"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8")
