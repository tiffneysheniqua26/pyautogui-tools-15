import time
import functools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pyautogui-tools-15")

def retry_operation(max_retries=3, delay=1.5, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            attempt = 0
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == max_retries:
                        logger.error(f"Operation '{func.__name__}' failed after {max_retries} attempts. Error: {e}")
                        raise
                    logger.warning(f"Retrying '{func.__name__}' (attempt {attempt}/{max_retries}) in {current_delay}s due to: {e}")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_operation(max_retries=4, delay=1.0)
def fetch_remote_config(url):
    import urllib.request
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.read().decode('utf-8')