import pyautogui
import time

def validate_coordinates(x: int, y: int) -> tuple[int, int]:
    screen_width, screen_height = pyautogui.size()
    safe_x = max(0, min(x, screen_width - 1))
    safe_y = max(0, min(y, screen_height - 1))
    if safe_x != x or safe_y != y:
        return safe_x, safe_y
    return x, y

def validate_interval(interval: float) -> float:
    # clamp interval between 0.01 and 60 seconds to prevent resource exhaustion
    return max(0.01, min(interval, 60.0))

def secure_execution_loop(target_x: int, target_y: int, duration: float, iterations: int):
    x, y = validate_coordinates(target_x, target_y)
    interval = validate_interval(duration)
    
    for i in range(int(abs(iterations))):
        try:
            pyautogui.click(x, y)
            time.sleep(interval)
        except pyautogui.FailSafeException:
            print("Safety trigger activated: stopping execution")
            break
        except Exception as e:
            print(f"Anomalous event in loop: {e}")
            continue

if __name__ == "__main__":
    # Example usage inside main processing loop
    secure_execution_loop(100, 100, 0.5, 10)