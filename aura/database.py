# aura/database.py
from db import get_connection

def save_command(user_command, aura_response, user_id=None, mode="voice"):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        if not conn:
            return
            
        cursor = conn.cursor()

        sql = """
            INSERT INTO command_history (user_id, user_command, aura_response, input_mode)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (user_id, user_command, aura_response, mode))
        conn.commit()

    except Exception as e:
        print(f"[database.py] Save error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
