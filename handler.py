import sys
import time
import ctypes

class FastClickHandler:
    def __init__(self, pause_duration=0.001):
        self.pause = pause_duration
        self._is_windows = sys.platform == "win32"
        if self._is_windows:
            self._user32 = ctypes.windll.user32
            self._dw_down = 0x0002
            self._dw_up = 0x0004

    def perform_click(self, x=None, y=None, clicks=1):
        if self._is_windows and x is not None and y is not None:
            self._user32.SetCursorPos(int(x), int(y))
            for _ in range(clicks):
                self._user32.mouse_event(self._dw_down, 0, 0, 0, 0)
                self._user32.mouse_event(self._dw_up, 0, 0, 0, 0)
                if self.pause > 0:
                    time.sleep(self.pause)
        else:
            import pyautogui
            pyautogui.PAUSE = self.pause
            pyautogui.click(x=x, y=y, clicks=clicks)

    def batch_click(self, coordinates):
        for x, y in coordinates:
            self.perform_click(x, y)