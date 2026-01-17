
import time
import threading
import sounddevice as sd
from aura.wake_word_listener import WakeWordListener
import aura.voice as voice

def test_stream_handoff():
    print("--- AURA Audio Stream Handoff Test ---")
    
    # Mocking speak_auto and is_speaking
    def mock_speak(text):
        print(f"[MOCK SPEAK] {text}")
    
    import aura.wake_word_listener as wwl
    wwl.speak_auto = mock_speak
    voice.speak_auto = mock_speak
    
    def mock_is_speaking():
        return False
    
    voice.is_speaking = mock_is_speaking
    
    listener = WakeWordListener(on_wake=lambda: print("[TEST] Wake word!"))
    print(f"INFO: Listener using device: {listener.device}")
    
    # Start listener in background
    t = threading.Thread(target=listener.start, daemon=True)
    t.start()
    
    print("1. Enabling WakeWordListener...")
    listener.set_enabled(True)
    time.sleep(2)
    
    print("\n2. Simulating Active Mic Request (Disabling Listener)...")
    listener.set_enabled(False)
    
    # Wait for listener to actually close its stream
    max_wait = 10
    start_time = time.time()
    while listener._is_listening and (time.time() - start_time) < max_wait:
        time.sleep(0.1)
    
    if listener._is_listening:
        print("WARNING: Listener took too long to close!")
    else:
        print("INFO: Listener stream closed successfully.")
    
    time.sleep(2.0) # Extended buffer for Windows audio driver
    sd.stop() # Ensure clean state
    
    print("3. Attempting to open second stream (Simulating MicrophoneFix)...")
    try:
        from aura.mic_fix import MicrophoneFix
        mic = MicrophoneFix()
        from speech_recognition import Recognizer
        rec = Recognizer()
        audio = mic.listen(rec, phrase_time_limit=2)
        print(f"SUCCESS: Second stream captured {len(audio.get_wav_data())} bytes!")
    except Exception as e:
        print(f"FAILED: Second stream error: {e}")
        
    print("\n4. Re-enabling WakeWordListener...")
    listener.set_enabled(True)
    time.sleep(2.0)
    
    print("\n5. Shutdown test...")
    listener.stop()
    time.sleep(1)
    print("Test complete.")

if __name__ == "__main__":
    test_stream_handoff()
