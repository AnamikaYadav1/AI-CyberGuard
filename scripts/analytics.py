# scripts/analytics.py
import sqlite3
import pandas as pd
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "scans.db")

def fetch_all_scans():
    """Return all scan records from the local database."""
    if not os.path.exists(db_path):
        return pd.DataFrame(columns=["type", "input", "result", "confidence", "timestamp"])

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM scans ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def summarize_data(df):
    """Compute simple summary stats."""
    if df.empty:
        return {"total": 0, "malicious": 0, "safe": 0}

    malicious = df[df["result"].str.contains("Malicious|Cyberbullying", case=False, na=False)]
    safe = df[df["result"].str.contains("Safe", case=False, na=False)]

    return {
        "total": len(df),
        "malicious": len(malicious),
        "safe": len(safe)
    }
