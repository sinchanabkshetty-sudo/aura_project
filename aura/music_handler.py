# aura/music_handler.py

import subprocess
import os
import time

class MusicHandler:
    """Handle music commands via Spotify"""
    
    def __init__(self):
        self.username = os.getenv('USERNAME')
        self.spotify_path = fr"C:\Users\{self.username}\AppData\Roaming\Spotify\spotify.exe"
    
    def play_music(self, song_name=None):
        """Open Spotify and play music"""
        try:
            if os.path.exists(self.spotify_path):
                subprocess.Popen(self.spotify_path)
                time.sleep(2)
                
                if song_name:
                    return f"Playing {song_name} on Spotify"
                else:
                    return "Spotify opened. Playing your playlist"
            else:
                return "Spotify not found. Please install Spotify"
        except Exception as e:
            return f"Could not open Spotify: {str(e)}"
    
    def pause_music(self):
        """Pause music using spacebar"""
        try:
            import pyautogui
            pyautogui.press('space')
            return "Music paused"
        except Exception as e:
            return f"Could not pause music: {str(e)}"
    
    def stop_music(self):
        """Stop music"""
        try:
            import pyautogui
            pyautogui.press('stop')
            return "Music stopped"
        except Exception as e:
            return f"Could not stop music: {str(e)}"
    
    def next_track(self):
        """Skip to next track"""
        try:
            import pyautogui
            pyautogui.hotkey('ctrl', 'right')
            return "Skipping to next song"
        except Exception as e:
            return f"Could not skip: {str(e)}"
    
    def previous_track(self):
        """Go to previous track"""
        try:
            import pyautogui
            pyautogui.hotkey('ctrl', 'left')
            return "Going to previous song"
        except Exception as e:
            return f"Could not go to previous: {str(e)}"
