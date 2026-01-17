# db.py  (root folder)
from dotenv import load_dotenv
load_dotenv()

import os
import mysql.connector
from mysql.connector import Error

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "")

def get_connection():
    # MySQL connection enabled
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Error as e:
        print(f"[db.py] MYSQL CONNECTION ERROR: {e}")
        # Log error but don't necessarily crash unless it's critical
        return None
