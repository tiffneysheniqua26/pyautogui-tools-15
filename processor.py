import time
import functools
import random

def retry_operation(max_attempts=3, backoff_base=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    sleep_time = (backoff_base ** attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

@retry_operation(max_attempts=5)
def fetch_remote_config():
    # Simulate volatile network state for autoclicker settings
    if random.random() < 0.7:
        raise ConnectionError("Network handshake failed")
    return {"click_speed": 0.05, "auto_hold": True}

def process_network_task():
    try:
        data = fetch_remote_config()
        print(f"Sync complete: {data}")
        return data
    except Exception as e:
        print(f"Critical network failure after retries: {e}")
        return None