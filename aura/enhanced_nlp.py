# aura/enhanced_nlp.py

import re
from datetime import datetime


class EnhancedNLP:
    """
    Lightweight intent + entity extractor for AURA.
    Uses regex and keyword rules instead of heavy ML to stay offline.
    """

    def __init__(self):
        self.intent_patterns = {
            "music": r"(play|pause|stop|music|song|spotify|next|skip|previous|back)",
            "youtube": r"(youtube|yt\b|watch|video|vedio|utube)",
            "email": r"(email|mail|gmail|send mail|send an email)",
            "search": r"(search|google|find|what is|tell me about|how to)",
            "system": r"(lock|shutdown|restart|sleep|volume|brightness|wifi|bluetooth)",
            "screenshot": r"(screenshot|capture screen|screen shot)",
            "app": r"(open|launch|start|run)",
            "file": r"(file|folder|create file|delete file|document)",
            "time": r"(time|current time|what time|date|what day)",
            "weather": r"(weather|temperature|forecast)",
            "help": r"(help|what can you do|commands)",
        }

        self.known_apps = [
            "chrome",
            "firefox",
            "notepad",
            "word",
            "excel",
            "powerpoint",
            "spotify",
            "discord",
            "telegram",
            "vlc",
            "calculator",
            "paint",
            "edge",
            "vscode",
        ]

        self.known_websites = [
            "facebook",
            "twitter",
            "instagram",
            "linkedin",
            "reddit",
            "stackoverflow",
            "github",
            "netflix",
            "amazon",
            "ebay",
            "youtube",
            "gmail",
            "google",
            "wikipedia",
            "whatsapp",
        ]

    # -------- basic extractors --------
    def extract_intent(self, user_input: str) -> str:
        text = user_input.lower()
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, text):
                return intent
        return "general"

    def extract_email(self, user_input: str):
        email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
        emails = re.findall(email_pattern, user_input)
        return emails[0] if emails else None

    def extract_app(self, user_input: str):
        text = user_input.lower()
        for app in self.known_apps:
            if app in text:
                return app
        return None

    def extract_website(self, user_input: str):
        text = user_input.lower()
        for site in self.known_websites:
            if site in text:
                return site
        return None

    def extract_number(self, user_input: str):
        numbers = re.findall(r"\b\d+\b", user_input)
        return [int(n) for n in numbers] if numbers else None

    def extract_query(self, user_input: str):
        text = user_input.lower()
        keywords_to_remove = [
            "search for",
            "find",
            "google",
            "youtube",
            "watch",
            "send email to",
            "mail to",
            "email",
            "compose",
            "open",
            "launch",
            "start",
            "run",
            "play",
            "what is",
            "tell me about",
            "how to",
            "please",
            "can you",
            "could you",
        ]
        query = text
        for kw in keywords_to_remove:
            query = query.replace(kw, "")
        return query.strip()

    # -------- combined parsing --------
    def extract_entities(self, user_input: str):
        entities: dict = {}

        email = self.extract_email(user_input)
        if email:
            entities["email"] = email

        app = self.extract_app(user_input)
        if app:
            entities["app"] = app

        website = self.extract_website(user_input)
        if website:
            entities["website"] = website

        numbers = self.extract_number(user_input)
        if numbers:
            entities["numbers"] = numbers

        query = self.extract_query(user_input)
        if query and len(query) > 2:
            entities["query"] = query

        quoted = re.findall(r'"([^"]*)"', user_input)
        if quoted:
            entities["quoted"] = quoted

        return entities

    def parse(self, user_input: str):
        """Return (intent, entities) pair."""
        intent = self.extract_intent(user_input)
        entities = self.extract_entities(user_input)
        entities["raw_input"] = user_input
        entities["timestamp"] = datetime.now().isoformat()
        return intent, entities
