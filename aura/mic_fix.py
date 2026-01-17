import sounddevice as sd
import numpy as np
import io
import wave
import speech_recognition as sr
import time
import platform

class MicrophoneFix:
    """
    A replacement for sr.Microphone that uses sounddevice instead of PyAudio.
    """
    def __init__(self, device=None, chunk_size=1024, sample_rate=16000):
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.audio_data = []
        self._stream = None
        
        if device is None and platform.system() == "Windows":
            self.device = self._find_best_device()
            if self.device is not None:
                print(f"[DEBUG] MicrophoneFix: Using optimal device index {self.device}")
        else:
            self.device = device

    def __enter__(self):
        # We don't actually open the stream here because sr.recognizer.listen 
        # expects a 'source' that it can call listen on.
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def listen(self, recognizer, timeout=None, phrase_time_limit=None):
        """
        Mimics recognizer.listen but uses sounddevice.
        """
        print(f"[DEBUG] MicrophoneFix.listen started (max {phrase_time_limit}s)")
        
        # Determine duration
        duration = phrase_time_limit if phrase_time_limit else 5
        
        # STREAM COORDINATION: Wait for TTS to finish if it's speaking
        # This prevents resource contention on Windows audio drivers
        from aura.voice import is_speaking
        wait_start = time.time()
        while is_speaking() and (time.time() - wait_start) < 3.0:
            time.sleep(0.1)
        
        # Record audio using sounddevice with retry logic
        recording = None
        max_retries = 3
        actual_sample_rate = self.sample_rate
        
        for attempt in range(max_retries):
            try:
                # Test for 16000Hz support first
                try:
                    sd.check_input_settings(device=self.device, samplerate=16000, channels=1)
                    actual_sample_rate = 16000
                except:
                    dev_info = sd.query_devices(self.device)
                    actual_sample_rate = int(dev_info['default_samplerate'])
                    print(f"[DEBUG] 16000Hz not supported for recording, using: {actual_sample_rate}")

                print(f"[DEBUG] Recording {duration}s of audio at {actual_sample_rate}Hz (Attempt {attempt+1})...")
                recording = sd.rec(int(duration * actual_sample_rate), 
                                  samplerate=actual_sample_rate, 
                                  channels=1, 
                                  dtype='float32',
                                  device=self.device)
                sd.wait()  # Wait for recording to finish
                sd.stop()  # Explicitly stop to release device
                print("[DEBUG] Recording finished successfully.")
                break
            except Exception as e:
                print(f"[DEBUG] sd.rec attempt {attempt+1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.5) 
                else:
                    raise
        
        # Convert float32 to int16
        print("[DEBUG] Processing audio data...")
        audio_int16 = (recording * 32767).astype(np.int16)
        
        # Create a buffer for the wav file
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(actual_sample_rate)
            wf.writeframes(audio_int16.tobytes())
        
        buf.seek(0)
        print(f"[DEBUG] Audio buffer created ({len(buf.getvalue())} bytes)")
        
        # Load into sr.AudioFile to get sr.AudioData
        with sr.AudioFile(buf) as source:
            print("[DEBUG] Recognizing from buffer...")
            audio = recognizer.record(source)
            print("[DEBUG] AudioData captured for recognizer.")
            return audio

    @property
    def stream(self):
        return None

    @stream.setter
    def stream(self, value):
        # Allow setting to satisfy sr.Recognizer internal logic
        pass

    def _find_best_device(self):
        """Helper to find the best input device on Windows (WDM-KS > WASAPI)"""
        try:
            apis = sd.query_hostapis()
            
            # Prioritize WDM-KS (usually most robust for Intel Smart Sound)
            for api in apis:
                if "WDM-KS" in api['name']:
                    dev_index = api.get('default_input_device', -1)
                    if dev_index != -1:
                        return dev_index
            
            # Fallback to WASAPI
            for api in apis:
                if "WASAPI" in api['name']:
                    dev_index = api.get('default_input_device', -1)
                    if dev_index != -1:
                        return dev_index
        except:
            pass
        return None

    def adjust_for_ambient_noise(self, source, duration=1):
        # Placeholder
        print("Calibrating background noise (sounddevice)...")
        pass

# Context manager compatible with 'with MicrophoneFix() as source:'
class MicrophoneSource:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.CHUNK = 1024
        self.SAMPLE_RATE = sample_rate
        self.SAMPLE_WIDTH = 2 # 16-bit
        
    def __enter__(self):
        return self
        
    def __exit__(self, x, y, z):
        pass
