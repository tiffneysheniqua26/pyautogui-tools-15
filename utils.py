import time
import functools
import random

def retry_network_call(max_retries=3, base_delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = base_delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    sleep_time = current_delay * (backoff ** (retries - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class NetworkState:
    def __init__(self):
        self.is_online = True

    def check_connection(self):
        return self.is_online