import pyautogui
import time
import random

def handle_click_errors(click_x, click_y, retries=3):
    screen_w, screen_h = pyautogui.size()
    for attempt in range(retries):
        try:
            if click_x < 0 or click_y < 0 or click_x >= screen_w or click_y >= screen_h:
                print("Edge case detected: out of bounds coordinates adjusted")
                click_x = min(max(click_x, 0), screen_w - 1)
                click_y = min(max(click_y, 0), screen_h - 1)
            if attempt == 2:
                pyautogui.doubleClick(click_x, click_y)
            else:
                pyautogui.click(click_x, click_y)
            return True
        except pyautogui.FailSafeException:
            print("Fail safe edge case: mouse moved to safe position")
            pyautogui.moveTo(screen_w // 2, screen_h // 2)
            time.sleep(0.5)
            continue
        except Exception as err:
            print("Error handling edge case:", str(err))
            time.sleep(0.1 * (attempt + 1))
    return False

def process_autoclick_sequence(positions):
    if not positions:
        print("Edge case: no click positions provided")
        return
    for idx, pos in enumerate(positions):
        if not isinstance(pos, (list, tuple)) or len(pos) != 2:
            print("Edge case: malformed position data skipped")
            continue
        x, y = pos[0], pos[1]
        try:
            if not handle_click_errors(int(x), int(y)):
                print("Click failed after retries at position", idx)
                continue
            delay = random.choice([0.1, 0.2, 0.3])
            time.sleep(delay)
        except KeyboardInterrupt:
            print("Interrupted during autoclick processing")
            return
        except Exception as e:
            print("General error in sequence:", e)
            continue
    print("Autoclick sequence processing completed")

if __name__ == "__main__":
    test_positions = [(150, 250), (400, 300), (100, 500)]
    process_autoclick_sequence(test_positions)
