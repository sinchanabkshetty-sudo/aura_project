# aura/skills/screenshot.py
import os, time
import pyautogui

def take_screenshot(_=None):
    os.makedirs("screenshots", exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join("screenshots", f"snap_{ts}.png")
    pyautogui.screenshot(path)
    return f"Screenshot saved: {path}"
