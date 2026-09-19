# pyautogui-tools-15

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`pyautogui-tools-15` is a robust Python utility designed to automate repetitive mouse clicks and keystrokes with high precision. It provides a lightweight wrapper around PyAutoGUI to easily schedule clicking patterns, detect screen elements, and run background automation scripts.

## Features

*   **Dynamic Interval Clicker:** Set exact millisecond intervals with random human-like jitter to bypass basic anti-cheat and bot-detection filters.
*   **Targeted Pixel Locking:** Automatically pause or halt clicking tasks if specified screen coordinates change color or if an anchor image is lost.
*   **Emergency Failsafe:** Integrated safety listeners that instantly abort execution when the mouse is dragged to any screen corner.

## Installation

Clone the repository and install the dependencies directly:

```bash
git clone https://github.com/developer/pyautogui-tools-15.git
cd pyautogui-tools-15
pip install -r requirements.txt
```

## Quick Start

Create automated click intervals with human-like variance in just a few lines of code:

```python
from pyautogui_tools import MultiClicker

# Initialize clicker at specific screen coordinates
clicker = MultiClicker(target_x=500, target_y=