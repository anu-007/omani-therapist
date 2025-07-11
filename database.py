import sqlite3
import os
from datetime import datetime

DATABASE_FILE = 'crisis_logs.db'

def init_db():
    """Initializes the SQLite database and creates the crisis_logs table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crisis_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            detected_text TEXT NOT NULL,
            user_id TEXT,
            session_id TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database '{DATABASE_FILE}' initialized.")

def log_crisis(detected_text: str, user_id: str = None, session_id: str = None):
    """Logs a detected crisis text with a timestamp, user ID, and session ID into the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('INSERT INTO crisis_logs (timestamp, detected_text, user_id, session_id) VALUES (?, ?, ?, ?)',
                   (timestamp, detected_text, user_id, session_id))
    conn.commit()
    conn.close()
    print(f"Logged crisis: '{detected_text}' (User: {user_id}, Session: {session_id}) at {timestamp}")

if __name__ == '__main__':
    # Example usage:
    init_db()
    log_crisis("User expressed suicidal thoughts.", user_id="test_user_1", session_id="test_session_1")
    log_crisis("User mentioned feeling hopeless.", user_id="test_user_2", session_id="test_session_2")
