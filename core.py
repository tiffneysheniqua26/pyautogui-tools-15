import sys
import time
import ctypes
from typing import Tuple, Optional

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _anonymous_ = ("u",)
    _fields_ = [("type", ctypes.c_ulong), ("u", _U)]

class CoreFastClicker:
    """High-frequency click engine bypassing PyAutoGUI queue bottlenecks."""
    
    INPUT_MOUSE = 0
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004

    def __init__(self, target_cps: float = 500.0) -> None:
        self.target_cps = target_cps
        self.interval = 1.0 / max(target_cps, 1.0)
        self._is_windows = sys.platform == "win32"
        self._input_array = self._preallocate_native_events() if self._is_windows else None

    def _preallocate_native_events(self):
        down = INPUT(type=self.INPUT_MOUSE)
        down.mi.dwFlags = self.MOUSEEVENTF_LEFTDOWN
        up = INPUT(type=self.INPUT_MOUSE)
        up.mi.dwFlags = self.MOUSEEVENTF_LEFTUP
        return (INPUT * 2)(down, up)

    def _precise_spin_wait(self, deadline: float) -> None:
        """Hybrid spin loop providing microsecond accuracy timing."""
        while time.perf_counter() < deadline:
            remaining = deadline - time.perf_counter()
            if remaining > 0.002:
                time.sleep(remaining - 0.001)

    def execute_burst(self, count: int) -> int:
        """Executes low-overhead batch click sequence directly at OS level."""
        executed = 0
        start_time = time.perf_counter()
        
        if self._is_windows and self._input_array:
            send_input = ctypes.windll.user32.SendInput
            struct_size = ctypes.sizeof(INPUT)
            
            for i in range(count):
                self._precise_spin_wait(start_time + (i * self.interval))
                send_input(2, self._input_array, struct_size)
                executed += 1
        else:
            import pyautogui
            pyautogui.PAUSE = 0.0
            for i in range(count):
                self._precise_spin_wait(start_time + (i * self.interval))
                pyautogui.click()
                executed += 1
                
        return executed
