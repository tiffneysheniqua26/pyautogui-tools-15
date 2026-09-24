import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry_network_op(max_attempts=3, delay=1.5, backoff=2):
    """decorator for exponential backoff on network tasks"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    if attempt == max_attempts:
                        logger.error(f"failed after {max_attempts} attempts: {e}")
                        raise
                    logger.warning(f"retry {attempt}/{max_attempts} in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_network_op(max_attempts=4)
def fetch_remote_config():
    """demonstrates retry logic on external dependency fetch"""
    return {"status": "ok", "click_rate": 0.05}