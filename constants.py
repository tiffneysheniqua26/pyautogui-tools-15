import sys
import os

class ClickConstants:
    DEFAULT_INTERVAL = 0.1
    MIN_INTERVAL = 0.001
    MAX_INTERVAL = 10.0
    
    CLICK_MODES = ('single', 'double', 'triple', 'hold')
    MOUSE_BUTTONS = ('left', 'middle', 'right')
    
    # Dynamic calibration offset based on system load
    LATENCY_BUFFER = 0.005

class EnvConfig:
    OS_TYPE = sys.platform
    IS_MACOS = OS_TYPE == 'darwin'
    IS_WINDOWS = OS_TYPE == 'win32'
    
    APP_NAME = "pyautogui-tools-15"
    VERSION = "1.0.4"

class KeyBindings:
    # Using integer scan codes for low-level hook bypass
    TOGGLE_KEY = 0x74  # F5
    EMERGENCY_STOP = 0x76  # F7
    
def get_app_header():
    return f"[{EnvConfig.APP_NAME} v{EnvConfig.VERSION}]"