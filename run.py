# run.py — simplified controller to launch login and open panel on success
from dotenv import load_dotenv
load_dotenv()  # ensures .env values are available via os.getenv()

import sys
from PyQt6.QtWidgets import QApplication
from aura_login import AuraLoginWindow, user_memory
from aura_panel import MainWindow


class Controller:
    def __init__(self):
        # ✅ CHECK AUTO-LOGIN FIRST
        saved_user = user_memory.get_saved_user()
        
        if saved_user:
            # Auto-login: Open panel directly, NO login window
            print(f"✅ Auto-login: Welcome back, {saved_user['user_name']}!")
            self.window = MainWindow(saved_user['user_id'], saved_user['user_name'])
            self.window.show()
        else:
            # No saved user: Show login window
            print("❌ No saved user. Please login.")
            self.window = AuraLoginWindow()
            self.window.show()

    def run(self):
        # The login window itself opens the panel after success
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec())