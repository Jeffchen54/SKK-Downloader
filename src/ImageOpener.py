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
from cv2 import CALIB_CB_FAST_CHECK
import keyboard
import pyautogui as pg
import os
import mouse
import numpy as np

# Preliminaries
######################## cd to icon directory ########################
os.chdir("..")
os.chdir("icons")
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
NEXT_GRID = 5.3                 # Scrolls needed to move to next grid of images
SCROLL_BUFFER = 0.5             # Seconds to wait for scrolling
CURSOR_MOVE_BUFFER = 0.1        # Seconds to wait for cursor movement

clicks = 0

"""
Processes a row of images by processing one image and then moving left
until cursor is past the lborder

If the cursor is on the border, it will not process the image but move 
left until cursor is past the lborder
"""
def processRow():
    global clicks

    # Processing grid segment
    while(lborder < pg.position()[0]):
        time.sleep(CURSOR_MOVE_BUFFER)
        # TODO - if statement for if on dead space
        #mouse.click("middle")
        clicks = clicks + 1
        pos = pg.position()
        mouse.move(pos[0] - IMAGE_DIFFERENCE, pos[1], True)
        time.sleep(SCROLL_BUFFER)
        if keyboard.is_pressed("Esc"):
            exit()

def main():
    rows = 0

    # TODO - multithreading could be used to instantly quit application
    print("Hold esc on keyboard to terminate", flush=True)

    if keyboard.is_pressed("Esc"):
        exit()


    terminate = pg.locateOnScreen('terminate_icon.png', confidence=0.3)

    # Keeps running until termination icon is visable
    while True:

        opos = pg.position()   
        processRow()
        rows = rows + 1
        #mouse.click("middle")
        mouse.move(opos[0], opos[1], True)

        
        # For incrementing to next grid segment
        mouse.wheel(NEXT_ROW)
        time.sleep(SCROLL_BUFFER)

        # Increment into next grid if needed
        if np.array_equal(pg.pixel(pg.position()[0], pg.position()[1]), BORDER_COLOR):
            mouse.wheel(NEXT_GRID)
            time.sleep(SCROLL_BUFFER)

        # Process last row on screen once terminate icon is spotted
        terminate = pg.locateOnScreen('terminate_icon.png', confidence=0.5)
        if(terminate != None and rows != 1):
            processRow()
            rows = rows + 1
            break               # Hate using break but need do-while loop not available in python

    print("Terminating on termination logo, CLICKS: ", clicks, " Rows: ", rows)

if __name__=="__main__":
    main()
