[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# pyautogui-tools-15

pyautogui-tools-15 is a Python autoclicker built on PyAutoGUI for automating repetitive mouse input. It provides precise timing controls and safety mechanisms for tasks that require consistent clicking over extended periods.

## Features
- Configurable click intervals from 10ms to 30 seconds
- Support for left, right, and middle mouse buttons
- Keyboard hotkeys for starting, stopping, and emergency halt
- Optional random timing variation to reduce detection in automated environments

## Installation

```bash
git clone https://github.com/Developer/pyautogui-tools-15.git
cd pyautogui-tools-15
pip install -r requirements.txt
```

## Basic Usage

```python
from autoclicker import AutoClicker

clicker = AutoClicker(
    interval=0.25,
    button="left",
    max_clicks=500
)

clicker.start()  # Press F8 to stop
```

The process runs at the current mouse position and can be interrupted instantly using the configured hotkey.