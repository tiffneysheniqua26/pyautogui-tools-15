import logging
import sys
import functools

class PyAutoLogger:
    def __init__(self):
        self.logger = logging.getLogger('pyautogui-tools-15')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def safe_execute(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                self.logger.warning('manual intervention detected, shutting down')
                sys.exit(0)
            except Exception as e:
                self.logger.error(f'unforeseen mishap in {func.__name__}: {str(e)}')
                return None
        return wrapper

log_instance = PyAutoLogger()
log = log_instance.logger
safe_call = log_instance.safe_execute