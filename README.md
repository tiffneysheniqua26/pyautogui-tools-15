# pyautogui-tools-15

`pyautogui-tools-15` is a high-performance automation library built on top of PyAutoGUI, designed to simplify complex click-path scripting. It provides a robust framework for creating reliable autoclickers and mouse-automation sequences with minimal boilerplate code.

### Features
*   **Intelligent Wait-Loops:** Built-in retry logic with pixel-matching validation to ensure clicks only trigger when UI elements are fully loaded.
*   **Human-like Jitter:** Configurable random coordinate offsets to mimic natural mouse movement and avoid basic bot-detection heuristics.
*   **Session Management:** Save and export complex click-sequences to JSON files for easy portability and version control.
*   **Kill-Switch Integration:** Native support for failsafe triggers, allowing immediate script termination by moving the cursor to the screen corner.

### Installation

Requires Python 3.8+ and `pip`.

```bash
pip install pyautogui-tools-15
```

If you are on Linux, ensure you have the necessary display dependencies installed:

```bash
sudo apt-get install python3-tk python3-dev
```

### Basic Usage

Define a sequence and execute it with automated delay intervals:

```python
from pyautogui_tools import ClickSession

# Initialize the session
session = ClickSession(jitter=True, delay=0.5)

# Add coordinates and click types
session.add_action(x=500, y=300, action='left')
session.add_action(x=800, y=600, action='double')

# Run the automation
session.execute(repeat=5)
```

### License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.