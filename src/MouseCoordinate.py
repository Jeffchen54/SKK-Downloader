import pyautogui
import keyboard
import time

while keyboard.is_pressed("esc") == False:
    print(pyautogui.position(), flush=True)
    time.sleep(1)