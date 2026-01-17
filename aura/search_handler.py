# aura/search_handler.py

import webbrowser
import time
from urllib.parse import quote

class SearchHandler:
    """Handle web search commands"""
    
    def google_search(self, query):
        """Search Google"""
        try:
            if not query:
                query = "python"
            
            url = f"https://www.google.com/search?q={quote(query)}"
            webbrowser.open(url)
            time.sleep(1)
            return f"Searching Google for: {query}"
        except Exception as e:
            return f"Could not search Google: {str(e)}"
    
    def youtube_search(self, query):
        """Search YouTube"""
        try:
            if not query:
                query = "trending"
            
            url = f"https://www.youtube.com/results?search_query={quote(query)}"
            webbrowser.open(url)
            time.sleep(1)
            return f"Searching YouTube for: {query}"
        except Exception as e:
            return f"Could not search YouTube: {str(e)}"
    
    def watch_video(self, topic):
        """Open YouTube"""
        try:
            if not topic:
                topic = "trending"
            
            url = f"https://www.youtube.com/results?search_query={quote(topic)}"
            webbrowser.open(url)
            return f"Finding {topic} on YouTube"
        except Exception as e:
            return f"Could not open YouTube: {str(e)}"
    
    def open_youtube(self):
        """Open YouTube homepage"""
        try:
            webbrowser.open("https://www.youtube.com/")
            return "YouTube opened"
        except Exception as e:
            return f"Could not open YouTube: {str(e)}"
