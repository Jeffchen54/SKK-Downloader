"""
Simple image tab selector for chan.sankakucomplex.com
Developed since widely available image grabbing softwares
have been defeated by erroneous loading employed by Sankaku
to block batch downloaders.

Compatible with Firefox only with dark mode settings

@author Jeff Chen
@created 4/5/2022
@version 0.11
"""
import time
import keyboard
import pyautogui as pg
import os
import mouse
import numpy as np

# Preliminaries
######################## cd to icon directory ########################
os.chdir("..")
os.chdir("icons")
print(os.getcwd())
#TODO - check file contents

################### Determine the leftmost border ###################
icon = pg.locateOnScreen('lborder.png', confidence=0.99)
if icon == None:
    print("Unable to pickup leftmost border, please adjust confidence or switch to correct window")
    exit()
lborder = icon[0]       # leftmost border of clickable content

####################### End of Preliminaries #########################

### Misc variables
BORDER_COLOR = [27,27,27]       # Color of image border
IMAGE_DIFFERENCE = 420          # Pixel difference from center of one image to next image
NEXT_ROW = 3.5                  # Scrolls to move to next row of images
NEXT_GRID = 6.8                 # Scrolls needed to move to next grid of images
SCROLL_BUFFER = 0.5             # Seconds to wait for scrolling
CURSOR_MOVE_BUFFER = 0.1        # Seconds to wait for cursor movement

# TODO - multithreading could be used to instantly quit application
print("Hold esc on keyboard to terminate", flush=True)
myInt = 0

# TODO - make range dynamic
for i in range(0, 18):
    
    if keyboard.is_pressed("Esc"):
        exit()
    
    # Process one grid
    while np.array_equal(pg.pixel(pg.position()[0], pg.position()[1]), BORDER_COLOR) == False:

        opos = pg.position()
        # Processing grid segment
        while(lborder < pg.position()[0]):
            time.sleep(CURSOR_MOVE_BUFFER)
            #mouse.click("middle")
            pos = pg.position()
            mouse.move(pos[0] - IMAGE_DIFFERENCE, pos[1], True)
            time.sleep(SCROLL_BUFFER)
            if keyboard.is_pressed("Esc"):
                exit()

        #mouse.click("middle")
        mouse.move(opos[0], opos[1], True)

        
        # For incrementing to next grid segment
        mouse.wheel(NEXT_ROW)
        time.sleep(SCROLL_BUFFER)

    # Increment into the next grid
    mouse.wheel(NEXT_GRID)
    time.sleep(SCROLL_BUFFER)

    if keyboard.is_pressed("Esc"):
        exit()
