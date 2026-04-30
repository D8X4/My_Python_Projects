#!/usr/bin/env python3
import pyautogui as p
import time

time.sleep(3)  # time to click into roblox window
# print('typing sentence')
while True:
    p.keyDown('space')
    p.keyUp('space')
    time.sleep(10)

# p.keyDown('(anykey)')
# p.keyUp('(anykey)')
