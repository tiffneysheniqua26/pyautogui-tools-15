import time
import functools
from contextlib import contextmanager
from typing import Callable, Any, Generator, Dict, List


class ActionRegistry:
    """Registry for autoclicker action pipelines with dynamic state cleanup."""

    def __init__(self) -> None:
        self._actions: Dict[str, Callable[..., Any]] = {}
        self._execution_history: List[str] = []

    def register(self, name: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                self._execution_history.append(name)
                return func(*args, **kwargs)
            self._actions[name] = wrapper
            return wrapper
        return decorator

    def execute_pipeline(self, pipeline: List[str], delay: float = 0.05) -> Generator[str, None, None]:
        for action_name in pipeline:
            if action_name in self._actions:
                self._actions[action_name]()
                time.sleep(delay)
                yield f"Executed step: {action_name}"

    def purge_history(self) -> int:
        count = len(self._execution_history)
        self._execution_history.clear()
        return count


registry = ActionRegistry()


@contextmanager
def execution_scope(auto_clean: bool = True) -> Generator[ActionRegistry, None, None]:
    try:
        yield registry
    finally:
        if auto_clean:
            registry.purge_history()


def safe_interval_generator(total_seconds: float, interval: float) -> Generator[float, None, None]:
    start = time.monotonic()
    while time.monotonic() - start < total_seconds:
        yield time.monotonic() - start
        time.sleep(interval)
