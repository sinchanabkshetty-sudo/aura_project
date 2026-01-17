# aura/screen_reader.py

"""
Screen reading: capture full screen, OCR it, and read aloud.
"""

import time
from PIL import ImageGrab
import pytesseract

from aura.voice import speak


def read_screen(full: bool = True):
    """
    Capture current screen and read detected text aloud.
    """
    time.sleep(0.3)
    img = ImageGrab.grab()
    text = pytesseract.image_to_string(img)

    if not text.strip():
        speak("I could not detect any readable text on the screen.")
        return "No readable text detected."

    short = text.strip()
    if len(short) > 400:
        short = short[:400].rsplit(" ", 1)[0] + "..."

    speak(short)
    return f"📖 Read text from screen:\n{short}"
