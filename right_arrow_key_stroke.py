from pynput.keyboard import Key, Controller
import time
keyboard = Controller()

try:
    while True:
        keyboard.press(Key.right)
        keyboard.release(Key.right)
        time.sleep(0.1)  # Pause x seconds
except KeyboardInterrupt:
    print('Program interrupted by Ctrl+C')
