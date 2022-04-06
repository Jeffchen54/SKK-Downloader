import mouse
import time
import keyboard

# Preliminaries
lborder = 511       # leftmost border of clickable content


print("Hold esc on keyboard to terminate", flush=True)
myInt = 0

# Total number of grids
for i in range(0, 18):
    
    if keyboard.is_pressed("Esc"):
        exit()
    
    # increment into next grid
    for m in range(0, 5):

        opos = mouse.get_position()
        # Processing segment
        for o in range(0, 3):
            time.sleep(0.5)
            #mouse.click("middle")
            pos = mouse.get_position()
            mouse.move(pos[0] - 180, pos[1])
            time.sleep(0.5)
            if keyboard.is_pressed("Esc"):
                exit()

        #mouse.click("middle")
        pos = mouse.get_position()
        mouse.move(opos[0], opos[1])

        if m < 4:
            # For incrementing to next grid segment
            mouse.wheel(1.8)

    time.sleep(0.1)
    mouse.wheel(8.6)
    time.sleep(0.5)

    if keyboard.is_pressed("Esc"):
        exit()

# while(mouse.is_pressed("right") == False):
    # mouse.wheel(-1)

# while(mouse.is_pressed("right") == False):
#    print(mouse.get_position())
#    mouse.click("middle")
 #   time.sleep(1)
