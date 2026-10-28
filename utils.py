import time
import functools
import random

def exponential_backoff(max_retries=3, base_delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    jitter = random.uniform(0, 0.5)
                    sleep_time = (base_delay * (2 ** (retries - 1))) + jitter
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class NetworkInterface:
    @staticmethod
    @exponential_backoff(max_retries=4)
    def fetch_remote_config(url):
        # Simulate unstable network condition
        if random.random() < 0.7:
            raise ConnectionError("remote server latency spike")
        return {"click_interval": 0.5, "enabled": True}

def get_stable_data(url):
    data = NetworkInterface.fetch_remote_config(url)
    return data or {}
