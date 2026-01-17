# aura/smart_search.py

import re
import webbrowser
import wikipedia


class SmartSearch:
    """
    AI-like decision: Wikipedia answer vs Google vs YouTube vs local music.
    """

    def __init__(self, sys_handler):
        self.sys = sys_handler

    def _is_question(self, text: str) -> bool:
        t = text.lower()
        return any(w in t for w in [
            "who is", "what is", "meaning of", "define",
            "tell me about", "explain", "information on"
        ])

    def _is_youtube(self, text: str) -> bool:
        t = text.lower()
        return any(w in t for w in [
            "youtube", "video", "song", "music", "watch", "trailer", "movie"
        ])

    def _is_music(self, text: str) -> bool:
        t = text.lower()
        return any(w in t for w in ["play music", "play song", "start music"])

    def _clean_query(self, text: str) -> str:
        pattern = r"(who is|what is|meaning of|define|tell me about|search|google|on youtube|youtube|video|song|music|play|watch|information on|explain)"
        q = re.sub(pattern, "", text, flags=re.I)
        return q.strip()

    def handle(self, text: str) -> str:
        """
        Main smart handler. Called from setup_handlers.
        """
        if not text:
            return "Please say something."

        q = self._clean_query(text)

        # 1) Question → Wikipedia (fallback Google)
        if self._is_question(text):
            try:
                summary = wikipedia.summary(q or text, sentences=2)
                return f"📘 {summary}"
            except Exception:
                return self.sys.open_google(q or text)

        # 2) Music / YouTube commands
        if self._is_youtube(text):
            return self.sys.open_youtube(q or text)

        if self._is_music(text):
            return self.sys.play_local_music()

        # 3) Generic site: "open instagram", "open flipkart"
        if text.lower().startswith("open "):
            site = q or text.replace("open", "").strip()
            if "." not in site:
                site = site.replace(" ", "")
                url = f"https://www.{site}.com"
            else:
                url = site
            webbrowser.open(url)
            return f"🌐 Opening {site}..."

        # 4) Default: Google it
        return self.sys.open_google(q or text)
