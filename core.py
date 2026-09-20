import time
import pyautogui

class FastAutoClicker:
    """High-speed click scheduler utilizing sub-millisecond spin locking."""
    def __init__(self, x=None, y=None, clicks=10, interval=0.001):
        self.clicks = clicks
        self.interval_ns = int(interval * 1_000_000_000)
        # Avoid repeated PyAutoGUI position calls by resolving coordinates once
        current_pos = pyautogui.position()
        self.resolved_x = x if x is not None else current_pos[0]
        self.resolved_y = y if y is not None else current_pos[1]

    def execute_burst(self):
        """Executes rapid clicks bypassing PyAutoGUI's default safety sleep latency."""
        original_pause = pyautogui.PAUSE
        pyautogui.PAUSE = 0.0

        # Local variables binding for micro-optimization of lookup times
        click_method = pyautogui.click
        target_x = self.resolved_x
        target_y = self.resolved_y
        timer = time.perf_counter_ns
        limit = self.interval_ns

        try:
            for _ in range(self.clicks):
                start_tick = timer()
                click_method(x=target_x, y=target_y)
                # Spin-lock instead of time.sleep to bypass OS scheduler context-switch overhead
                while timer() - start_tick < limit:
                    pass
        finally:
            pyautogui.PAUSE = original_pause
