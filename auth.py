# auth.py — login/register using password_hash with MySQL
import bcrypt
from db import get_connection

def register_user(name: str, email: str, password: str):
    """Register a new user with MySQL database"""
    conn = None
    cursor = None
    try:
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"
            
        cursor = conn.cursor()
        
        # MySQL uses %s as placeholder
        sql = "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, pw_hash))
        conn.commit()
        return True, "Registered successfully"
    except Exception as e:
        if "Duplicate entry" in str(e) or "1062" in str(e):
            return False, "Email already registered"
        return False, f"Registration error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def login_user(email: str, password: str):
    """Login user with MySQL database"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed", None, None
            
        cursor = conn.cursor()
        # MySQL uses %s as placeholder
        sql = "SELECT user_id, name, password_hash FROM users WHERE email=%s"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        
        if not row:
            return False, "No user with that email", None, None
        
        user_id, name, pw_hash = row
        if bcrypt.checkpw(password.encode("utf-8"), pw_hash.encode("utf-8")):
            return True, "Login successful", user_id, name
        else:
            return False, "Invalid password", None, None
    except Exception as e:
        return False, f"Login error: {e}", None, None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
