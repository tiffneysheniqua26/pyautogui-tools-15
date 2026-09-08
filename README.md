# pyautogui-tools-15

`pyautogui-tools-15` is a high-performance Python utility library designed to streamline complex automation tasks through an intuitive abstraction of PyAutoGUI. It enables developers to build reliable, human-like autoclickers and interface interactors with minimal boilerplate code.

## Features

*   **Humanized Randomization:** Built-in jitter algorithms to randomize click coordinates and timing, significantly reducing the detection rate of automated scripts.
*   **Interruptible Loop Engine:** Provides thread-safe start/stop controls for automation sequences, allowing for instant emergency halts via keyboard hotkeys.
*   **Dynamic Target Acquisition:** Advanced image and color searching capabilities that adapt to resolution scaling and dynamic UI changes.
*   **Session Profiling:** Save and load configuration profiles to quickly switch between different automation workflows without re-coding.

## Installation

Ensure you have Python 3.8+ installed. Install the package directly via pip:

```bash
pip install pyautogui-tools-15
```

For systems requiring cross-platform visual processing, ensure `opencv-python` is installed:

```bash
pip install opencv-python
```

## Basic Usage

The library simplifies the creation of a standard interval clicker into a few lines of code:

```python
from pyautogui_tools_15 import Clicker

# Initialize with a 0.5-second interval and human-like jitter
bot = Clicker(interval=0.5, jitter=True)

# Start clicking at current mouse position
bot.start()

# Stop the automation
bot.stop()
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.