# aura/fuzzy_matcher.py

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def _fuzzy_match(text1: str, text2: str, threshold: float = 0.5) -> bool:
    """
    Check if two strings match with fuzzy logic
    Returns True if similarity ratio is above threshold
    """
    similarity = fuzz.ratio(text1.lower(), text2.lower()) / 100.0
    return similarity >= threshold


class FuzzyMatcher:
    """Auto-correct typos in user commands"""
    
    def __init__(self):
        self.correct_commands = {
            'play music': ['play musc', 'paly music', 'play muzic', 'play song'],
            'volume up': ['volum up', 'volume upp', 'vol up'],
            'volume down': ['volum down', 'volume dwn'],
            'open chrome': ['opne chrome', 'open crome', 'open chrom'],
            'send email': ['send emial', 'snd email', 'male someone'],
            'youtube': ['youbtube', 'utube', 'youtub'],
            'take screenshot': ['scrrenshot', 'screensh', 'scren shot'],
            'lock system': ['lok system', 'lock sistem'],
            'shutdown': ['shutdwn', 'shut down'],
            'wifi off': ['wifi of', 'wif off'],
            'what time': ['wht time', 'whats time'],
            'search for': ['serch for', 'search 4'],
            'brightness up': ['brightnes up', 'brightn up'],
            'pause music': ['paus music', 'pause muzic'],
            'next song': ['nxt song', 'next track'],
        }
    
    def correct(self, user_input):
        """Auto-correct input using fuzzy matching"""
        user_input_lower = user_input.lower().strip()
        
        try:
            # process.extractOne returns (match, score) tuple
            result = process.extractOne(
                user_input_lower,
                self.correct_commands.keys(),
                scorer=fuzz.token_set_ratio,
                score_cutoff=70
            )
            
            # Check if result exists and unpack properly
            if result:
                matched_command, confidence_score = result  # FIXED: Unpack tuple
                
                if confidence_score > 80:
                    return matched_command
            
            return user_input_lower
        
        except Exception as e:
            # If anything fails, just return original input
            print(f"Fuzzy match error: {e}")
            return user_input_lower
