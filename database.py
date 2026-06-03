import sqlite3
from datetime import datetime
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect('fake_news.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        # Audit Ledger table (matches your website's "Forensic Log")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS audit_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                input_type TEXT NOT NULL,
                file_name TEXT,
                score INTEGER,
                verdict TEXT,
                details TEXT
            )
        ''')
        
        # History table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                content TEXT,
                score INTEGER,
                verdict TEXT,
                explanation TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()

def save_to_audit(input_type, file_name, score, verdict, details=""):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO audit_ledger (timestamp, input_type, file_name, score, verdict, details) VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), input_type, file_name, score, verdict, details)
        )
        conn.commit()

def get_audit_history():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM audit_ledger ORDER BY id DESC LIMIT 50").fetchall()
        return [dict(row) for row in rows]

def save_to_history(content, score, verdict, explanation):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO history (content, score, verdict, explanation, created_at) VALUES (?, ?, ?, ?, ?)",
            (content[:500], score, verdict, explanation, datetime.now().isoformat())
        )
        conn.commit()

def get_history():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM history ORDER BY id DESC LIMIT 50").fetchall()
        return [dict(row) for row in rows]

# Initialize database when module loads
init_db()