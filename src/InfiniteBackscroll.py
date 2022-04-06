import keyboard
import mouse

print("ctrl to exit", flush=True)
while keyboard.is_pressed("ctrl") == False:
     mouse.wheel(-1)
print("Terminated")