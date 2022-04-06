"""
Simple image tab selector for chan.sankakucomplex.com
Developed since widely available image grabbing softwares
have been defeated by erroneous loading employed by Sankaku
to block batch downloaders.

Compatible with Firefox only with dark mode settings

@author Jeff Chen
@created 4/5/2022
@version 0.1
"""
import time
import keyboard
import pyautogui as pg
import os
import mouse

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





# TODO - multithreading could be used to instantly quit application
print("Hold esc on keyboard to terminate", flush=True)
myInt = 0

# TODO - make range dynamic
for i in range(0, 18):
    
    if keyboard.is_pressed("Esc"):
        exit()
    
    # increment into next grid
    for m in range(0, 5):

        opos = pg.position()
        # Processing segment
        while(lborder < pg.position()[0]):
            time.sleep(0.5)
            #mouse.click("middle")
            pos = pg.position()
            mouse.move(pos[0] - 340, pos[1], True)
            time.sleep(0.5)
            if keyboard.is_pressed("Esc"):
                exit()

        #mouse.click("middle")
        pos = pg.position()
        mouse.move(opos[0], opos[1], True)

        if m < 4:
            # For incrementing to next grid segment
            mouse.wheel(1.8)

    time.sleep(0.1)
    mouse.wheel(8.6)
    time.sleep(0.5)

    if keyboard.is_pressed("Esc"):
        exit()
