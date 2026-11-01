import time
import functools
import random

def retry_network_operation(max_attempts=3, backoff_factor=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = backoff_factor * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def pulse_connection(check_fn):
    """Decorator that wraps network calls with jittered retries."""
    return retry_network_operation(max_attempts=5, backoff_factor=1.0)(check_fn)