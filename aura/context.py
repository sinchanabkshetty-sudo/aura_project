import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# ---------- DB LOGGING ----------

_db = None
_cursor = None


def _connect():
    global _db, _cursor
    if _db:
        return
    # Skip MySQL connection for now - using SQLite in command_engine instead
    # Uncomment below to enable MySQL when available
    # try:
    #     _db = mysql.connector.connect(
    #         host=os.getenv("DB_HOST", "localhost"),
    #         user=os.getenv("DB_USER", "root"),
    #         password=os.getenv("DB_PASSWORD", ""),
    #         database=os.getenv("DB_NAME", "aura_db"),
    #         auth_plugin="mysql_native_password",
    #     )
    #     _cursor = _db.cursor()
    # except Exception:
    _db, _cursor = None, None


_connect()


def save_history(command: str, response: str):
    """Persist one turn into MySQL table command_history."""
    if not _cursor:
        return
    try:
        _cursor.execute(
            "INSERT INTO command_history (user_command, aura_response, created_at) "
            "VALUES (%s, %s, %s)",
            (command, response[:255], datetime.now()),
        )
        _db.commit()
    except Exception:
        pass


# ---------- IN‑MEMORY CONTEXT ----------

@dataclass
class Turn:
    user_text: str
    system_text: str
    timestamp: str


@dataclass
class ConversationContext:
    last_platform: Optional[str] = None   # "youtube", "google", ...
    last_query: Optional[str] = None
    history: List[Turn] = field(default_factory=list)

    def add_turn(self, user: str, system: str):
        self.history.append(
            Turn(user_text=user, system_text=system, timestamp=datetime.now().isoformat())
        )
        self.history = self.history[-50:]

    def update_search(self, platform: str, query: str):
        self.last_platform = platform
        self.last_query = query

    def as_dict(self) -> Dict:
        return {
            "last_platform": self.last_platform,
            "last_query": self.last_query,
            "turn_count": len(self.history),
        }
