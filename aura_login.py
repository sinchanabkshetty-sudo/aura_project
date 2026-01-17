# -*- coding: utf-8 -*-
"""
aura_login.py
Login + Registration UI for AURA (PyQt6) with Auto-Login Feature.
"""

import sys
import re
import json
from pathlib import Path
from typing import Tuple
from datetime import datetime

from PyQt6.QtCore import Qt, QRectF, QTimer, QByteArray
from PyQt6.QtGui import QPainter, QColor, QFont, QPainterPath, QPixmap, QIcon, QRegion
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QPushButton, QLineEdit, QSizePolicy,
    QSpacerItem, QDialog
)

# ==================== USER MEMORY SYSTEM ====================
class UserMemory:
    """Saves user login info for auto-login"""
    def __init__(self):
        self.memory_file = Path("user_memory.json")
   
    def save_user(self, email: str, password: str, user_id: int, user_name: str) -> bool:
        """Save user credentials"""
        try:
            data = {
                "email": email,
                "password": password,
                "user_id": user_id,
                "user_name": user_name,
                "last_login": str(datetime.now())
            }
            with open(self.memory_file, 'w') as f:
                json.dump(data, f)
            print("SUCCESS: User saved for auto-login!")
            return True
        except Exception as e:
            print(f"ERROR saving user: {e}")
            return False
   
    def get_saved_user(self) -> dict:
        """Get saved user credentials"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                return data
            return None
        except Exception as e:
            print(f"ERROR reading user: {e}")
            return None
   
    def clear_user(self) -> bool:
        """Clear saved user (logout)"""
        try:
            if self.memory_file.exists():
                self.memory_file.unlink()
            print("SUCCESS: User cleared!")
            return True
        except Exception as e:
            print(f"ERROR clearing user: {e}")
            return False

# Create global instance
user_memory = UserMemory()

# ==================== AUTH IMPORTS ====================
try:
    from auth import login_user, register_user
except Exception:
    try:
        from auth import login_user
    except Exception:
        def login_user(email, password):
            return False, "auth.login_user not available", None, None
    def register_user(name, email, password):
        return False, "register_user not implemented in auth.py"

# Import UI logo and MainWindow from aura_panel
try:
    from aura_panel import MainWindow, AuraLogoWidget
except Exception:
    from PyQt6.QtWidgets import QWidget
    class AuraLogoWidget(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(44, 44)
    class MainWindow(QWidget):
        def __init__(self, user_id: int = 0, user_name: str = "Guest"):
            super().__init__()

# ==================== THEME / SIZING ====================
NEON_CYAN = QColor(90, 240, 255)
TEXT_WHITE = QColor(238, 242, 248)
BUTTON_WIDTH = 420
BUTTON_HEIGHT = 48
INPUT_WIDTH = BUTTON_WIDTH
INPUT_HEIGHT = 44

# ==================== SVG EYE ICONS ====================
EYE_OUTLINE_SVG = b"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='white' d='M12 5c-7 0-11 6-11 7s4 7 11 7 11-6 11-7-4-7-11-7zm0 12c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z'/></svg>"""
EYE_SLASH_OUTLINE_SVG = b"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='white' d='M2 3l2 2 3.1 3.1C4.9 10.1 2.7 12 1 12c0 0 4 7 11 7 2.1 0 4.1-.4 6-1.2L19 19l2 2 1-1L3 2 2 3zM12 7c1.6 0 3 .7 4 1.8L9.8 15C8.7 14 8 12.6 8 11c0-2.8 2.2-4 4-4z'/></svg>"""

def svg_to_icon(svg_bytes: bytes, size: int = 18) -> QIcon:
    renderer = QSvgRenderer(QByteArray(svg_bytes))
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pix)
    renderer.render(painter)
    painter.end()
    return QIcon(pix)

def set_aa(p: QPainter):
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

# ==================== REGISTRATION DIALOG ====================
class RegistrationDialog(QDialog):
    """Modal registration dialog styled to match the login UI."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.corner_radius = 20
        self.setModal(True)
        self.setWindowTitle("Create account")
        self.setFixedSize(560, 480)
        self._input_w = 480
        self._input_h = INPUT_HEIGHT
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 18, 28, 18)
        root.setSpacing(10)

        # logo centered
        logo_row = QHBoxLayout()
        logo_row.addStretch(1)
        self.logo = AuraLogoWidget(self)
        logo_row.addWidget(self.logo, 0, Qt.AlignmentFlag.AlignCenter)
        logo_row.addStretch(1)
        root.addLayout(logo_row)

        title = QLabel("Create account")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.DemiBold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        subtitle = QLabel("Fill details to create your AURA account")
        subtitle.setFont(QFont("Segoe UI", 9))
        subtitle.setStyleSheet("color: rgba(200,210,230,200);")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(subtitle)

        root.addSpacerItem(QSpacerItem(20, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # name
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Full name")
        self._style_field(self.name_field)
        root.addWidget(self.name_field, alignment=Qt.AlignmentFlag.AlignHCenter)

        # email
        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("you@example.com")
        self._style_field(self.email_field)
        root.addWidget(self.email_field, alignment=Qt.AlignmentFlag.AlignHCenter)

        # password + eye
        pwd_box = QHBoxLayout()
        pwd_box.setContentsMargins(0, 0, 0, 0)
        pwd_box.setSpacing(6)

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setPlaceholderText("Password")
        self._style_field(self.password_field, reserve_right=46)

        self.eye_btn = QPushButton()
        self.eye_btn.setCheckable(True)
        self.eye_btn.setFixedSize(38, self._input_h)
        self.eye_btn.setIcon(svg_to_icon(EYE_OUTLINE_SVG))
        self.eye_btn.setStyleSheet("border:0;background:transparent;")
        self.eye_btn.clicked.connect(self._toggle_eye)

        pwd_box.addWidget(self.password_field, 1)
        pwd_box.addWidget(self.eye_btn, 0)
        pwd_widget = QWidget()
        pwd_widget.setLayout(pwd_box)
        pwd_widget.setFixedWidth(self._input_w)
        root.addWidget(pwd_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        # confirm password
        self.confirm_field = QLineEdit()
        self.confirm_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_field.setPlaceholderText("Confirm password")
        self._style_field(self.confirm_field)
        root.addWidget(self.confirm_field, alignment=Qt.AlignmentFlag.AlignHCenter)

        # message
        self.msg_label = QLabel("")
        self.msg_label.setStyleSheet("color:#ff7070;font-size:13px;")
        self.msg_label.setVisible(False)
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.msg_label)

        # buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.register_btn = QPushButton("Create account")
        self.register_btn.setFixedSize(220, 44)
        self._style_button(self.register_btn)
        self.register_btn.clicked.connect(self._do_register)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(120, 44)
        cancel_btn.setStyleSheet(
            "QPushButton{background:transparent;color:rgba(200,210,230,200);"
            "border:1px solid rgba(255,255,255,8);border-radius:12px;}"
        )
        cancel_btn.clicked.connect(self.reject)

        btn_row.addStretch(1)
        btn_row.addWidget(self.register_btn)
        btn_row.addWidget(cancel_btn)
        btn_row.addStretch(1)
        root.addLayout(btn_row)

        root.addSpacerItem(QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def _style_field(self, w: QLineEdit, reserve_right: int = 0):
        w.setFixedHeight(self._input_h)
        w.setFixedWidth(self._input_w)
        right_margin = reserve_right if reserve_right else 14
        w.setTextMargins(14, 0, right_margin, 0)
        w.setStyleSheet(f"""
            QLineEdit {{
                border:2px solid rgba(110,116,255,120);
                border-radius:{self._input_h//2}px;
                padding-left:14px;
                color:white;
                background-color:rgba(40,45,58,240);
                font-size:14px;
            }}
        """)

    def _style_button(self, btn: QPushButton):
        btn.setStyleSheet("""
            QPushButton {
                border:0;
                border-radius:12px;
                color:white;
                font-weight:600;
                background-color:qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 rgba(110,116,255,255), stop:1 rgba(90,240,255,255));
            }
            QPushButton:hover { filter: brightness(1.05); }
        """)

    def _toggle_eye(self):
        if self.eye_btn.isChecked():
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.confirm_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_btn.setIcon(svg_to_icon(EYE_SLASH_OUTLINE_SVG))
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_btn.setIcon(svg_to_icon(EYE_OUTLINE_SVG))

    def _validate(self) -> Tuple[bool, str]:
        name = self.name_field.text().strip()
        email = self.email_field.text().strip()
        pwd = self.password_field.text()
        conf = self.confirm_field.text()
        if not name:
            return False, "Name required."
        if not email:
            return False, "Email required."
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email format."
        if not pwd:
            return False, "Password required."
        if len(pwd) < 6:
            return False, "Password must be at least 6 characters."
        if pwd != conf:
            return False, "Passwords do not match."
        return True, ""

    def _do_register(self):
        valid, msg = self._validate()
        if not valid:
            self.msg_label.setText(msg)
            self.msg_label.setStyleSheet("color:#ff7070;")
            self.msg_label.setVisible(True)
            return

        name = self.name_field.text().strip()
        email = self.email_field.text().strip()
        pwd = self.password_field.text().strip()

        try:
            ok, message = register_user(name, email, pwd)
        except Exception as e:
            ok, message = False, str(e)

        if not ok:
            self.msg_label.setText(message or "Registration failed")
            self.msg_label.setStyleSheet("color:#ff7070;")
            self.msg_label.setVisible(True)
            return

        self.msg_label.setText(message or "Registered successfully")
        self.msg_label.setStyleSheet("color:#80ff9a;")
        self.msg_label.setVisible(True)
        QTimer.singleShot(700, self.accept)

    def paintEvent(self, e):
        p = QPainter(self)
        set_aa(p)
        r = QRectF(self.rect())
        path = QPainterPath()
        path.addRoundedRect(r, self.corner_radius, self.corner_radius)
        p.setBrush(QColor(24, 28, 38))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPath(path)
        p.end()

# ==================== LOGIN WINDOW ====================
class AuraLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.corner_radius = 20
        self._drag_pos = None
        self.panel = None
        self.setup_window()
        self.build_ui()
        self.attempt_login = self.handle_login

    def setup_window(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(560, 520)
        self.center_on_screen()
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(36)
        shadow.setOffset(0, 14)
        shadow.setColor(QColor(20, 30, 70, 140))
        self.setGraphicsEffect(shadow)

    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.center().x() - self.width() // 2,
                  screen.center().y() - self.height() // 2)

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 22)
        root.setSpacing(16)

        # top logo + title
        logo_row = QHBoxLayout()
        logo_row.addStretch(1)
        self.logo = AuraLogoWidget(self)
        logo_row.addWidget(self.logo, 0, Qt.AlignmentFlag.AlignCenter)
        logo_row.addStretch(1)
        root.addLayout(logo_row)

        title = QLabel("AURA")
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: white; letter-spacing: 1px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        subtitle = QLabel("Sign in to continue")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: rgba(200,210,230,200);")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(subtitle)

        root.addSpacerItem(QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # email
        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("you@example.com")
        self._style_input(self.email_field)
        root.addWidget(self.email_field, alignment=Qt.AlignmentFlag.AlignHCenter)

        # password + eye
        pwd_box = QHBoxLayout()
        pwd_box.setContentsMargins(0, 0, 0, 0)
        pwd_box.setSpacing(6)

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setPlaceholderText("Password")
        self._style_input(self.password_field, reserve_right=46)

        self.eye_btn = QPushButton()
        self.eye_btn.setCheckable(True)
        self.eye_btn.setFixedSize(38, INPUT_HEIGHT)
        self.eye_btn.setIcon(svg_to_icon(EYE_OUTLINE_SVG))
        self.eye_btn.setStyleSheet("border:0;background:transparent;")
        self.eye_btn.clicked.connect(self.toggle_eye)

        pwd_box.addWidget(self.password_field, 1)
        pwd_box.addWidget(self.eye_btn, 0)
        pwd_widget = QWidget()
        pwd_widget.setLayout(pwd_box)
        pwd_widget.setFixedWidth(INPUT_WIDTH)
        root.addWidget(pwd_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        # error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color:#ff7070;font-size:13px;")
        self.error_label.setVisible(False)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.error_label)

        # sign in button
        self.login_btn = QPushButton("SIGN IN")
        self.login_btn.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self._style_button(self.login_btn)
        self.login_btn.clicked.connect(self.handle_login)
        root.addWidget(self.login_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        # links row
        links = QHBoxLayout()
        self.register_btn = QPushButton("Create account")
        self.register_btn.setStyleSheet("background:transparent;color:rgba(200,210,230,200);border:0;text-decoration:underline;")
        self.register_btn.clicked.connect(self.open_registration)
       
        self.forgot_btn = QPushButton("Forgot?")
        self.forgot_btn.setStyleSheet("background:transparent;color:rgba(200,210,230,200);border:0;text-decoration:underline;")
        self.forgot_btn.clicked.connect(self.show_forgot_message)
       
        links.addStretch(1)
        links.addWidget(self.register_btn)
        links.addWidget(self.forgot_btn)
        links.addStretch(1)
        root.addLayout(links)

        root.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def _style_input(self, w: QLineEdit, reserve_right: int = 0):
        w.setFixedHeight(INPUT_HEIGHT)
        w.setFixedWidth(INPUT_WIDTH)
        right_margin = reserve_right if reserve_right else 14
        w.setTextMargins(14, 0, right_margin, 0)
        w.setStyleSheet(f"""
            QLineEdit {{
                border:2px solid rgba(110,116,255,120);
                border-radius:{INPUT_HEIGHT//2}px;
                padding-left:14px;
                color:white;
                background-color:rgba(40,45,58,240);
                font-size:15px;
            }}
        """)

    def _style_button(self, btn: QPushButton):
        btn.setStyleSheet("""
            QPushButton {
                border:0;
                border-radius:24px;
                color:white;
                font-weight:700;
                background-color:qlineargradient(
                    x1:0,y1:0,x2:1,y2:1,
                    stop:0 rgba(110,116,255,255),
                    stop:1 rgba(90,240,255,255)
                );
            }
        """)

    def toggle_eye(self):
        if self.eye_btn.isChecked():
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_btn.setIcon(svg_to_icon(EYE_SLASH_OUTLINE_SVG))
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_btn.setIcon(svg_to_icon(EYE_OUTLINE_SVG))

    def open_registration(self):
        dlg = RegistrationDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.error_label.setStyleSheet("color:#80ff9a;font-size:13px;")
            self.error_label.setText("Registered — please sign in.")
            self.error_label.setVisible(True)

    def show_forgot_message(self):
        """Show a message for forgot password"""
        self.error_label.setStyleSheet("color:rgba(200,210,230,200);font-size:13px;")
        self.error_label.setText("Please contact support to reset your password.")
        self.error_label.setVisible(True)

    def validate_inputs(self) -> Tuple[bool, str]:
        email = self.email_field.text().strip()
        pwd = self.password_field.text()
        if not email:
            return False, "Email cannot be empty."
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email format."
        if not pwd:
            return False, "Password cannot be empty."
        return True, ""

    def handle_login(self):
        valid, msg = self.validate_inputs()
        if not valid:
            return self.show_error(msg)

        email = self.email_field.text().strip()
        password = self.password_field.text().strip()

        try:
            ok, msg, user_id, user_name = login_user(email, password)
        except Exception as e:
            return self.show_error(f"Login error: {e}")

        if not ok:
            return self.show_error(msg or "Invalid credentials")

        # Success — save user and open panel
        user_memory.save_user(email, password, user_id, user_name)
       
        self.error_label.setStyleSheet("color:#80ff9a;font-size:13px;")
        self.error_label.setText("Login successful! Opening AURA…")
        self.error_label.setVisible(True)
        QTimer.singleShot(300, lambda: self.open_panel(user_id, user_name))

    def open_panel(self, user_id, user_name):
        """Open main panel and close login window"""
        if self.panel is not None:
            return  # Prevent duplicate
        
        self.panel = MainWindow(user_id, user_name)
        self.panel.show()
        self.close()  # Close login window

    def show_error(self, msg):
        self.error_label.setStyleSheet("color:#ff7070;font-size:13px;")
        self.error_label.setText(msg)
        self.error_label.setVisible(True)

    def resizeEvent(self, e):
        r = QRectF(self.rect())
        path = QPainterPath()
        path.addRoundedRect(r, self.corner_radius, self.corner_radius)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def paintEvent(self, e):
        p = QPainter(self)
        set_aa(p)
        r = QRectF(self.rect())
        path = QPainterPath()
        path.addRoundedRect(r, self.corner_radius, self.corner_radius)
        p.setBrush(QColor(24, 28, 38))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPath(path)
        p.end()

# ==================== MAIN ENTRY POINT ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("AURA Login")
    
    # ✅ CHECK AUTO-LOGIN FIRST - BEFORE CREATING ANY WINDOW
    saved_user = user_memory.get_saved_user()
    
    if saved_user:
        # Auto-login: Open panel directly, NO login window
        print(f"SUCCESS: Auto-login: Welcome back, {saved_user['user_name']}!")
        panel = MainWindow(saved_user['user_id'], saved_user['user_name'])
        panel.show()
    else:
        # No saved user: Show login window
        print("INFO: No saved user. Please login.")
        win = AuraLoginWindow()
        win.show()
    
    sys.exit(app.exec())