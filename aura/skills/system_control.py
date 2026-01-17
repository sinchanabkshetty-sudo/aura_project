# aura/skills/system_control.py
import os, time, pyautogui

def take_screenshot():
    import datetime, os
    os.makedirs("screenshots", exist_ok=True)
    fname = datetime.datetime.now().strftime("screenshots/snap_%Y%m%d_%H%M%S.png")
    pyautogui.screenshot(fname)
    return f"Screenshot saved: {fname}"

def shutdown_system():
    os.system("shutdown /s /t 5")
    return "Shutting down in 5 seconds."

def restart_system():
    os.system("shutdown /r /t 5")
    return "Restarting in 5 seconds."

def lock_system():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "Locking system."

def volume_up():
    for _ in range(5): pyautogui.press("volumeup")
    return "Increasing volume."

def volume_down():
    for _ in range(5): pyautogui.press("volumedown")
    return "Decreasing volume."

def volume_mute():
    pyautogui.press("volumemute")
    return "Toggling mute."

def brightness_up():
    # not all keyboards map fn+brightness; this is best-effort
    for _ in range(2): pyautogui.hotkey("fn", "brightnessup")
    return "Increasing brightness."

def brightness_down():
    for _ in range(2): pyautogui.hotkey("fn", "brightnessdown")
    return "Decreasing brightness."
