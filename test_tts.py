
import pyttsx3
import time

def test_tts():
    print("Initializing TTS engine...")
    try:
        engine = pyttsx3.init()
        print("TTS Engine initialized.")
    except Exception as e:
        print(f"FAILED to initialize TTS: {e}")
        return

    print("Testing speak...")
    try:
        engine.say("Testing voice response system.")
        engine.runAndWait()
        print("SUCCESS: Spoke successfully.")
    except Exception as e:
        print(f"FAILED during speak loop: {e}")

if __name__ == "__main__":
    test_tts()
