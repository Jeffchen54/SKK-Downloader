from msilib.schema import Icon
import pyautogui as pg
import os

os.chdir("..")
os.chdir("..")
os.chdir("icons")
print(os.getcwd())

icon = pg.locateOnScreen("lborder.png", confidence=0.9)
pg.moveTo(icon[0], icon[1])
print(icon)