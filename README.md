# pyautogui-tools-15

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`pyautogui-tools-15` is a lightweight, high-performance automation utility designed for precise macro execution and rapid mouse clicking on desktop environments. Built on top of PyAutoGUI and pynput, it delivers millisecond-accurate click timing, dynamic visual targeting, and integrated fail-safe protocols for seamless operational task automation.

## Features

* **Dynamic CPS Control**: Configure variable click rates up to 500 clicks per second with optional randomized jitter intervals to simulate human input patterns.
* **Visual Anchor Triggering**: Automatically pause or trigger click routines based on real-time screen pixel matching and OpenCV image detection.
* **Global Hotkey Binds**: Toggle background scripts instantly using low-level keyboard listeners (`F8` for start/stop, `F12` for emergency terminate).
* **Multi-Coordinate Sequences**: Chain complex multi-point click paths with independent delay timers for each target location.

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/pyautogui-tools-15.git
cd pyautogui-tools-15
pip install pyautogui pynput opencv-python Pillow
```

## Quick Start

Run a basic autoclicker instance configured for 50 clicks per second targeted at specific screen coordinates:

```python
from pyautogui_tools_15 import FastClicker

# Initialize clicker with a 0.02s interval (50 CPS) and left mouse button
clicker = FastClicker(interval=0.02, button='left', fail_safe=True)

# Set target coordinates and start the loop
target_x, target_y = 960, 540
clicker.click_at(x=target_x, y=target_y, duration=10)
```

To enable hotkey control directly from the command line:

```bash
python -m pyautogui_tools_15.cli --cps 60 --hotkey f8
```

## License

Distributed under the MIT License. See `LICENSE` for details.