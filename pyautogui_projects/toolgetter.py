#!/usr/bin/env python3
import pyautogui as p
import time

#coords 
#X: 62, Y: 556
#X: 1687, Y: 402
#X: 1625, Y: 540
#X: 1800, Y: 370
time.sleep(3)  # time to click into roblox
p.click(62, 556)      # left arrow
time.sleep(0.3)
p.click(1620, 500) # tool button
time.sleep(0.5) # give the menu time to open
p.scroll(-16.5) # scroll down  
time.sleep(0.3)
p.click(1625, 540) #gets speedcoil
time.sleep(0.3)
p.click(1805, 362) #gets cloud
time.sleep(0.5)
p.click(62, 556)
print('tools are in inventory')
