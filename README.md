# pyautogui-tools-15

`pyautogui-tools-15` is a lightweight, high-performance automation library built on top of PyAutoGUI to streamline repetitive mouse and keyboard workflows. It provides an abstraction layer that simplifies complex click patterns and coordinate-based interactions for developers.

### Features

*   **Smart-Click Sequences:** Create complex click chains with customizable interval timing and randomized jitter offsets to mimic human input.
*   **Coordinate Memory:** Easily save and recall specific screen coordinates using an internal dictionary mapping, reducing hard-coded values in your scripts.
*   **Human-like Delays:** Built-in adaptive latency algorithms that prevent triggering anti-bot heuristics in common desktop applications.
*   **Fail-Safe Integration:** Automatic emergency stop functionality triggered by moving the cursor to any screen corner.

### Installation

Ensure you have Python 3.8+ installed. Install the package directly via pip:

```bash
pip install pyautogui-tools-15
```

If you are on Linux, ensure you have the required dependencies:
```bash
sudo apt-get install python3-tk python3-dev
```

### Basic Usage

Import the library to execute high-level automation tasks with minimal boilerplate code:

```python
from pyautogui_tools import AutoClicker

# Initialize the tool
bot = AutoClicker(interval=0.5)

# Add coordinates to the queue
bot.add_target(x=500, y=300)
bot.add_target(x=800, y=600)

# Execute the sequence
bot.run_sequence(loops=5)
```

### License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.