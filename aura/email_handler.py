# aura/email_handler.py

import webbrowser
import time

class EmailHandler:
    """Handle email commands via Gmail"""
    
    def send_email(self, recipient_email, subject="", body=""):
        """Compose email in Gmail"""
        try:
            # Open Gmail compose
            url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient_email}&su={subject}&body={body}"
            webbrowser.open(url)
            time.sleep(2)
            return f"Email to {recipient_email} ready to compose"
        except Exception as e:
            return f"Could not open Gmail: {str(e)}"
    
    def open_gmail(self):
        """Open Gmail inbox"""
        try:
            webbrowser.open("https://mail.google.com/")
            time.sleep(1)
            return "Gmail opened"
        except Exception as e:
            return f"Could not open Gmail: {str(e)}"
    
    def check_emails(self):
        """Open Gmail inbox"""
        return self.open_gmail()
    
    def compose_email(self):
        """Open Gmail compose window"""
        try:
            webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1")
            return "Gmail compose window opened"
        except Exception as e:
            return f"Could not open compose: {str(e)}"
