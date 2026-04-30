#!/usr/bin/env python3
import pyautogui
from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.space:
        pos = pyautogui.position()
        print(f"X: {pos.x}, Y: {pos.y}")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
