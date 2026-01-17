import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "aura_db")

def init_db():
    try:
        # First connect without database to create it
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        print(f"Checking for database '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # Read and execute SQL.sql
        sql_file_path = "SQL.sql"
        if not os.path.exists(sql_file_path):
            print(f"Error: {sql_file_path} not found.")
            return
            
        with open(sql_file_path, 'r') as f:
            sql_script = f.read()
            
        # Split by semicolon and execute each command
        # (Filtering out empty strings and comments)
        commands = sql_script.split(';')
        for command in commands:
            cmd = command.strip()
            if cmd and not cmd.startswith('--'):
                # Skip CREATE DATABASE if it's in the script since we already handled it
                if "CREATE DATABASE" in cmd.upper() or "USE " in cmd.upper():
                    continue
                
                print(f"Executing: {cmd[:50]}...")
                cursor.execute(cmd)
        
        conn.commit()
        print("SUCCESS: Database initialized successfully!")
    
    except mysql.connector.Error as e:
        print(f"MYSQL ERROR: {e}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_db()
