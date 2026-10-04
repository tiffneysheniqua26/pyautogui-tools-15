import time
import random
import functools

def with_resilience(max_attempts=3, delay=1.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            backoff = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.5)
                    time.sleep(backoff + jitter)
                    backoff *= 2
        return wrapper
    return decorator

class NetworkProcessor:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @with_resilience(max_attempts=4)
    def fetch_click_coords(self):
        # Simulated network call for autoclicker targets
        if random.random() < 0.7:
            raise ConnectionError("Server unreachable")
        return [("target_1", (500, 500)), ("target_2", (120, 800))]

    def process_coordinates(self):
        try:
            return self.fetch_click_coords()
        except Exception as err:
            return f"Network recovery failed: {err}"