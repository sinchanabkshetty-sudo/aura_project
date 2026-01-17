# aura/voice.py
"""
Voice utilities for AURA
 - Natural TTS using pyttsx3
 - English + Kannada bilingual support
 - Speaking state flag for UI animation
"""

import pyttsx3
from threading import Lock, Thread

_engine = None
_engine_lock = Lock()

_current_lang = "en"
_is_speaking = False


def _get_engine():
    global _engine
    with _engine_lock:
        if _engine is None:
            try:
                engine = pyttsx3.init()
            except Exception as e:
                print("TTS init error:", e)
                _engine = None
                return None
            # Default speaking speed / volume
            engine.setProperty("rate", 175)
            engine.setProperty("volume", 1.0)
            _engine = engine
        return _engine


def _pick_voice_for_lang(engine, lang: str):
    """
    Try to pick a nice voice for the given language.
    lang: "en" or "kn"
    """
    voices = engine.getProperty("voices")
    if not voices:
        return None

    lang = (lang or "en").lower()

    # Prefer Kannada voice when requested
    if lang.startswith("kn"):
        for v in voices:
            n = (v.name or "").lower()
            l = "".join(getattr(v, "languages", [])).lower()
            if "kannada" in n or "kn_" in l or "kn-in" in l:
                return v.id

    # For English: prefer female / Indian / English voices
    for v in voices:
        n = (v.name or "").lower()
        l = "".join(getattr(v, "languages", [])).lower()
        if ("female" in n or "zira" in n or "india" in n or "english" in n
                or "en_" in l):
            return v.id

    # Fallback: first available voice
    return voices[0].id


def _detect_lang_from_text(text: str) -> str:
    """
    Very simple language guess:
      - if contains Kannada Unicode chars → "kn"
      - else "en"
    """
    if not text:
        return "en"

    for ch in text:
        code = ord(ch)
        # Kannada block: 0C80–0CFF
        if 0x0C80 <= code <= 0x0CFF:
            return "kn"
    return "en"


def _do_speak(text: str, lang: str):
    global _is_speaking, _current_lang

    engine = _get_engine()
    if not engine:
        print("TTS engine not available, text:", text)
        return

    # auto-detect if needed
    if lang == "auto":
        lang = _detect_lang_from_text(text)

    # change voice if language changed
    if lang != _current_lang:
        voice_id = _pick_voice_for_lang(engine, lang)
        if voice_id:
            engine.setProperty("voice", voice_id)
            _current_lang = lang

    _is_speaking = True
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS speak error:", e)
    finally:
        _is_speaking = False


def speak(text: str, lang: str = "auto", async_: bool = True):
    """
    Speak text.
      lang: "en", "kn" or "auto"
      async_: if True, speak in background thread
    """
    if not text:
        return

    if async_:
        t = Thread(target=_do_speak, args=(text, lang), daemon=True)
        t.start()
    else:
        _do_speak(text, lang)


def speak_en(text: str):
    speak(text, lang="en", async_=True)


def speak_kn(text: str):
    speak(text, lang="kn", async_=True)


def speak_auto(text: str):
    speak(text, lang="auto", async_=True)


def set_voice(index: int):
    """
    Optionally allow manual voice selection.
    """
    engine = _get_engine()
    if not engine:
        return "Voice engine not available."

    voices = engine.getProperty("voices")
    if 0 <= index < len(voices):
        engine.setProperty("voice", voices[index].id)
        return f"Voice changed to #{index}"
    return f"Invalid voice index {index}. Available: 0 - {len(voices)-1}"


def is_speaking() -> bool:
    """
    Used by UI (logo animation) to know if AURA is currently speaking.
    """
    return _is_speaking
