# aura/wake_word_listener.py

import json
import queue
import time
from typing import Callable, Optional
import platform

import sounddevice as sd
from vosk import Model, KaldiRecognizer

from aura.engine import handle_command
from aura.voice import speak_auto


WAKE_WORDS = [
    "hey aura", "hai aura", "hey ora", "aura", "hey aurora",
    "hi aura", "hello aura", "ok aura", "hey euler", "hey aura",
    "air", "ora", "are you there", "wake up", "aurora", "euler",
    "herrera", "a herrera", "hey herrera"  # Adding variations that were detected
]

# Fuzzy matching for better wake word detection
def _fuzzy_match(text: str, target: str, threshold: float = 0.6) -> bool:
    """Simple fuzzy matching for wake words"""
    if target in text:
        return True
    
    # Check for partial matches
    words = text.split()
    for word in words:
        if len(word) >= 3 and len(target) >= 3:
            # Simple character overlap check
            overlap = sum(1 for char in word if char in target)
            if overlap / len(target) >= threshold:
                return True
    return False


class WakeWordListener:
    def __init__(self, model_path: str = "models/vosk-small-en",
                 on_wake: Optional[Callable] = None,
                 device: Optional[int] = None):
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.q: queue.Queue[bytes] = queue.Queue()
        self.listening_for_command = False
        self.on_wake = on_wake
        self.enabled = False  # Start disabled by default
        self.last_response_time = 0  # Track when we last spoke
        self.ignore_duration = 3.0   # Ignore audio for 3 seconds after speaking
        # Windows-specific device detection to prevent PaErrorCode -9999
        if device is None and platform.system() == "Windows":
            self.device = self._find_best_device()
            if self.device is not None:
                print(f"INFO: WakeWordListener: Using optimal device index {self.device}")
        else:
            self.device = device

    def _find_best_device(self):
        """Helper to find the best input device on Windows (WDM-KS > WASAPI)"""
        try:
            apis = sd.query_hostapis()
            
            # Prioritize WDM-KS
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

    def _audio_callback(self, indata, frames, time_, status):
        if status:
            print(f"[Audio callback status: {status}]")
        # Add a small indicator that audio is being received
        if hasattr(self, 'audio_count'):
            self.audio_count += 1
            if self.audio_count % 100 == 0 and self.enabled:  # Every 100 audio frames
                print(f"[Audio active - frames processed: {self.audio_count}]")
        else:
            self.audio_count = 1
        self.q.put(bytes(indata))

    def set_enabled(self, enabled: bool):
        """Enable or disable wake word detection"""
        old_status = getattr(self, 'enabled', False)
        self.enabled = enabled
        status_msg = "enabled - Say 'Hey AURA' to activate" if enabled else "disabled"
        print(f"Wake word detection: {status_msg}")
        
        if enabled and not old_status:
            print("INFO: Voice assistant is now listening for wake words!")
            print(f"INFO: Supported wake words: {WAKE_WORDS[:5]}...")
            print("INFO: Try saying: 'Hey AURA' or 'Hi AURA'")
            
            # Provide audio feedback when enabled
            import threading
            import time
            def delayed_speak():
                time.sleep(0.8)
                speak_auto("Voice assistant ready. Say Hey AURA to wake me up.")
            threading.Thread(target=delayed_speak, daemon=True).start()
        elif not enabled and old_status:
            print("INFO: Voice assistant disabled")
        
    def _should_ignore_audio(self) -> bool:
        """Check if we should ignore audio to prevent feedback"""
        current_time = time.time()
        return (current_time - self.last_response_time) < self.ignore_duration
        
    def _mark_response_time(self):
        """Mark the time when AURA speaks to ignore feedback"""
        self.last_response_time = time.time()
        
    def _is_own_response(self, text: str) -> bool:
        """Check if the detected text is likely AURA's own response"""
        own_responses = [
            "yes i'm listening", "yes im listening", "i'm listening", 
            "im listening", "listening", "yes", "sorry i had trouble",
            "sorry there was an error", "how can i help", "google",
            "magnifying glass", "search", "opening", "youtube"
        ]
        
        text_lower = text.lower().strip()
        
        # Check for exact matches
        for response in own_responses:
            if response in text_lower:
                return True
                
        # Check if it contains "google" with other words (likely TTS feedback)
        if "google" in text_lower and len(text_lower.split()) > 1:
            return True
            
        # Check for very short responses that are likely TTS artifacts
        if len(text_lower.split()) <= 2 and any(word in text_lower for word in ["yes", "the", "a", "an"]):
            return True
            
        return False

    def _contains_wake_word(self, text: str) -> bool:
        """Enhanced wake word detection with better filtering"""
        if not text or len(text.strip()) < 3:
            return False
            
        text_lower = text.lower().strip()
        
        # Ignore AURA's own responses - common phrases AURA says
        ignore_phrases = [
            "voice assistant", "ready", "wake me up", "i'm aura", "hello", "how can i help",
            "search", "google", "opening", "results", "browser", "find", "answer",
            "system controls", "apps", "what can i do", "good to see you",
            "explanation", "definition", "tutorial", "hope you find",
            "check the browser", "should appear", "looking that up"
        ]
        
        # If text contains AURA's response phrases, ignore it
        for phrase in ignore_phrases:
            if phrase in text_lower:
                print(f"[Ignoring own response: {text[:30]}...]")
                return False
        
        # More lenient wake word matching
        wake_variations = [
            # Standard wake words
            "hey aura", "hi aura", "hello aura", "hey aurora",
            "hai aura", "hey ora", "aura", 
            
            # More lenient variations
            "hey ira", "hey ara", "hey our", "hey ura", "hey error",
            "hi ora", "hello ora", "hey order", "he aura", "a aura",
            "hey allah", "hey aural", "hey oral", "hey aur",
            
            # Handle common misrecognitions
            "aye aura", "hay aura", "hey hora", "hey laura", "hey aida"
        ]
        
        # Check for wake word matches with fuzzy matching
        for wake_word in wake_variations:
            # Direct match
            if wake_word in text_lower:
                return True
                
            # Fuzzy match - allow for small variations
            words = text_lower.split()
            if len(words) >= 2:
                # Check first two words
                first_two = " ".join(words[:2])
                if self._fuzzy_match(wake_word, first_two):
                    return True
                    
                # Check for wake word anywhere in text
                for i in range(len(words) - 1):
                    two_words = " ".join(words[i:i+2])
                    if self._fuzzy_match(wake_word, two_words):
                        return True
        
        return False
        
    def _fuzzy_match(self, target: str, text: str, threshold: float = 0.6) -> bool:
        """Fuzzy string matching for wake words - more lenient threshold"""
        if not target or not text:
            return False
            
        # Calculate simple similarity
        target_words = target.split()
        text_words = text.split()
        
        if len(target_words) != len(text_words):
            return False
            
        matches = 0
        for t_word, txt_word in zip(target_words, text_words):
            # Check similarity with more lenient threshold
            if self._word_similarity(t_word, txt_word) >= 0.5:  # More lenient per-word matching
                matches += 1
                
        return matches >= len(target_words) * 0.7  # Allow 70% of words to match
        
    def _word_similarity(self, word1: str, word2: str) -> float:
        """Calculate similarity between two words"""
        if word1 == word2:
            return 1.0
            
        # Handle common speech recognition errors
        substitutions = {
            "aura": ["ora", "ira", "ara", "our", "ura", "error", "order", "allah", "aural", "oral", "aur"],
            "hey": ["hi", "aye", "hay", "he", "a"],
            "hello": ["halo", "hullo", "helo"]
        }
        
        for key, alternatives in substitutions.items():
            if word1 == key and word2 in alternatives:
                return 0.8
            if word2 == key and word1 in alternatives:
                return 0.8
                
        # Basic edit distance similarity
        if len(word1) == 0:
            return len(word2)
        if len(word2) == 0:
            return len(word1)
            
        # Simple character overlap
        common_chars = set(word1.lower()) & set(word2.lower())
        total_chars = set(word1.lower()) | set(word2.lower())
        
        if total_chars:
            return len(common_chars) / len(total_chars)
        return 0.0

    def start(self):
        print("Wake word listener background thread started.")
        import threading
        self._stop_event = threading.Event()
        
        while not self._stop_event.is_set():
            if not self.enabled:
                time.sleep(0.5)
                continue
                
            print("INFO: Opening audio stream for wake word...")
            try:
                # STREAM COORDINATION: Wait for TTS to finish if it's speaking
                from aura.voice import is_speaking
                wait_start = time.time()
                while is_speaking() and (time.time() - wait_start) < 3.0:
                    time.sleep(0.1)
                
                # Attempt to open at 16000Hz, fallback to native if driver demands
                try:
                    stream_samplerate = 16000
                    test_stream = sd.RawInputStream(samplerate=stream_samplerate, device=self.device)
                    test_stream.close()
                except:
                    dev_info = sd.query_devices(self.device)
                    stream_samplerate = int(dev_info['default_samplerate'])
                    print(f"INFO: 16000Hz not supported, using native rate: {stream_samplerate}")
                
                # Re-init recognizer with the actual rate
                self.rec = KaldiRecognizer(self.model, stream_samplerate)
                
                with sd.RawInputStream(
                    samplerate=stream_samplerate,
                    blocksize=8000,
                    dtype="int16",
                    channels=1,
                    callback=self._audio_callback,
                    device=self.device,
                ):
                    print("SUCCESS: Wake word audio stream is now active.")
                    self._is_listening = True
                    
                    # Clear queue to avoid processing stale audio
                    while not self.q.empty():
                        try: self.q.get_nowait()
                        except: break
                        
                    while self.enabled and not self._stop_event.is_set():
                        try:
                            # Use timeout to allow checking self.enabled frequently
                            try:
                                data = self.q.get(timeout=0.5)
                            except queue.Empty:
                                continue
                            
                            # Skip processing if we recently spoke (prevent feedback)
                            if self._should_ignore_audio():
                                continue
                                
                            if not self.rec.AcceptWaveform(data):
                                continue
                                
                            result = self.rec.Result()
                            text = json.loads(result).get("text", "").strip()
                            
                            if not text:
                                continue
                                
                            print(f"[WakeWord] heard: '{text}'")
                            
                            # Ignore if this is likely our own response
                            if self._is_own_response(text):
                                continue
                                
                            if not self.listening_for_command:
                                if self._contains_wake_word(text):
                                    self.listening_for_command = True
                                    print(f"INFO: WAKE WORD DETECTED! Text: '{text}'")
                                    if self.on_wake:
                                        try:
                                            self.on_wake()
                                        except Exception as e:
                                            print(f"on_wake callback error: {e}")
                                    
                                    self._mark_response_time()
                                    speak_auto("Yes, I'm listening.")
                                    
                                    # Reset recognizer for the actual command
                                    self.rec = KaldiRecognizer(self.model, 16000)
                                    time.sleep(0.5) # Short pause for AURA to finish speaking
                                continue

                            # If we reached here, we are listening_for_command
                            self.listening_for_command = False
                            print(f"🎯 Command received via wake word: '{text}'")
                            
                            try:
                                response = handle_command(text)
                            except Exception as e:
                                print(f"handle_command error: {e}")
                                response = "Sorry, I had trouble with that."
                                
                            self._mark_response_time()
                            speak_auto(response)
                            
                        except Exception as e:
                            print(f"[Stream processing error: {e}]")
                            break
                            
                print("INFO: Wake word audio stream closed (either disabled or stopping).")
                self._is_listening = False
                sd.stop() # Explicitly stop sounddevice
                
            except Exception as e:
                # This often happens if the device is busy
                if self.enabled:
                    print(f"Wake-word stream error: {e}")
                    print("INFO: Microphone might be busy. Retrying in 2 seconds...")
                time.sleep(2.0)
                
        print("Wake word listener thread exited.")

    def stop(self):
        """Stop the background thread and close stream"""
        if hasattr(self, '_stop_event'):
            self._stop_event.set()
        self.enabled = False
