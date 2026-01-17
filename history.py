# history.py — final version matching your actual DB schema

from db import get_connection

def save_history(user_id, user_text, bot_text, input_mode="text"):
    """
    Saves chat history into MySQL using the real table columns:
    - user_id
    - user_command
    - aura_response
    - input_mode
    - timestamp (auto)
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn is None:
            # MySQL not available, skip database logging
            return True
        cursor = conn.cursor()

        # MySQL uses %s placeholders
        sql = """
            INSERT INTO command_history (user_id, user_command, aura_response, input_mode)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (user_id, user_text, bot_text, input_mode))
        conn.commit()
        return True

    except Exception as e:
        print("SAVE_HISTORY ERROR:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
