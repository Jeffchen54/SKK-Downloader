import cv2
import pyautogui as pg
import numpy as np
import mouse
import time
import keyboard

def moving_detector():
    time.sleep(0.5)
    icon = pg.locateOnScreen('moving_icon.png', confidence=0.5)
    if icon != None:
        while(icon != None):
            print("moving detected, sleeping for 1 second...", flush=True)
            time.sleep(1)
            icon = pg.locateOnScreen('moving_icon.png', confidence=0.5)
        print("Program resuming", flush=True)

def kill_switch():
    if keyboard.is_pressed("Esc"):
        # escape condition
        cv2.waitKey(0)

        # clean up windows
        cv2.destroyAllWindows()

def warning_detector():
    # Check for warning
    time.sleep(0.5)
    icon = pg.locateOnScreen('cancel_icon.png', confidence=0.5)
    if(icon != None):
        print("Warning detected, press and hold ctrl to continue", flush=True)
        while keyboard.is_pressed("ctrl") == False:
            time.sleep(1)
        print("Program resuming", flush=True)

def loading_detector():
    mouse.move(1,1, True)
    time.sleep(0.5)
    icon = pg.locateOnScreen('loading_icon.png', confidence=0.5)
    if icon != None:
        while(icon != None):
            print("loading detected, sleeping for 1 second...", flush=True)
            time.sleep(1)
            icon = pg.locateOnScreen('loading_icon.png', confidence=0.5)
        print("Program resuming", flush=True)

# Preliminaries
LOADING_BUFFER = 2
TAB_BUFFER = 0.1

# Iterate until termination icon is displayed

icon = pg.locateOnScreen('terminate_icon.png', confidence=0.5)

while(icon == None):
    kill_switch()

    icon = pg.locateOnScreen('slowdown_msg.png')

    # Keep looping as long as slowdown msg exists
    while(icon != None):
        warning_detector()

        # Check if is a slowdown window
        if(icon != None):
            
            icon = pg.locateOnScreen('refresh_icon.png')

            # Attempt refresh if found
            if(icon != None):
                x = icon[0] + icon[2]/2
                y = icon[1] + icon[3]/2
                mouse.move(x, y, True, 0)
                mouse.click()
                loading_detector()


        # Take another screenshot and check if msg still exists
        icon = pg.locateOnScreen('slowdown_msg.png')

    # Process image by drag drop
    mouse.drag(430, 587, 2800, 552, True, 0.1)
    warning_detector()
    moving_detector()

    # Close current window
    mouse.move(1,1,True)
    mouse.click()
    pg.keyDown("ctrl")
    pg.press("w")
    pg.keyUp("ctrl")

    kill_switch()

    # Wait for window to load
    loading_detector()
         
    icon = pg.locateOnScreen('terminate_icon.png', confidence=0.5)


# escape condition
cv2.waitKey(0)

# clean up windows
cv2.destroyAllWindows()

print("Program terminating on completion")
