import sqlite3
from datetime import datetime
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'scan_logs.db')

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            input TEXT,
            result TEXT,
            confidence REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully by Anamika!")

def log_scan(scan_type, input_data, result, confidence=0.0):
    """Log a scan result (URL/Text)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO scans (type, input, result, confidence, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (scan_type, input_data, result, confidence, 
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def fetch_logs(limit=200):
    """Fetch latest scan logs from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM scans ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
