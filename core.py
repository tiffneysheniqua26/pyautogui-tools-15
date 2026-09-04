import time
import pyautogui

class OptimizedClickEngine:
    """High-performance click dispatcher utilizing precise frame timing."""
    
    def __init__(self, target_cps: int = 100):
        self.target_cps = max(1, target_cps)
        self.frame_time = 1.0 / self.target_cps
        self._active = False
        pyautogui.PAUSE = 0.00001
        pyautogui.FAILSAFE = True

    def execute_burst(self, x: int, y: int, count: int) -> int:
        self._active = True
        executed = 0
        next_tick = time.perf_counter()
        
        # Pre-cache click position pointer to eliminate internal lookup overhead
        click_func = pyautogui.click
        
        while self._active and executed < count:
            now = time.perf_counter()
            if now >= next_tick:
                click_func(x=x, y=y, _pause=False)
                executed += 1
                next_tick += self.frame_time
            else:
                # Yield CPU quantum without losing timing resolution
                time.sleep(max(0, next_tick - now))
                
        return executed

    def stop(self) -> None:
        self._active = False
