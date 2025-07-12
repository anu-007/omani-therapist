import os
import sqlite3
from cryptography.fernet import Fernet
from datetime import datetime
from base64 import b64encode

DATABASE_FILE = 'crisis_logs.db'
KEY_FILE = 'encryption.key'

def get_or_create_key():
    """Gets existing encryption key or creates a new one"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        return key

# Initialize Fernet cipher
cipher_suite = Fernet(get_or_create_key())

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

def encrypt_text(text: str) -> str:
    """Encrypts the input text"""
    return cipher_suite.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text: str) -> str:
    """Decrypts the encrypted text"""
    return cipher_suite.decrypt(encrypted_text.encode()).decode()

def log_crisis(detected_text: str, user_id: str = None, session_id: str = None):
    """Logs a detected crisis text with a timestamp, user ID, and session ID into the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    encrypted_text = encrypt_text(detected_text)

    cursor.execute('INSERT INTO crisis_logs (timestamp, detected_text, user_id, session_id) VALUES (?, ?, ?, ?)',
                   (timestamp, encrypted_text, user_id, session_id))
    conn.commit()
    conn.close()
    print(f"Logged encrypted crisis for (User: {user_id}, Session: {session_id}) at {timestamp}")

def get_crisis_log(log_id: int) -> dict:
    """Retrieves and decrypts a crisis log entry"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM crisis_logs WHERE id = ?', (log_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'timestamp': row[1],
            'detected_text': decrypt_text(row[2]),
            'user_id': row[3],
            'session_id': row[4]
        }
    return None

if __name__ == '__main__':
    # Example usage:
    init_db()
    log_crisis("User expressed suicidal thoughts.", user_id="test_user_1", session_id="test_session_1")
    log_crisis("User mentioned feeling hopeless.", user_id="test_user_2", session_id="test_session_2")
