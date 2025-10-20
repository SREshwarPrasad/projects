# backend/database.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "cropassist.db")

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    c = conn.cursor()
    # Users table: username (PK), password (hashed), fullname, dob, created_at
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            fullname TEXT,
            dob TEXT,
            created_at TEXT
        )
    """)
    # Login history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            action TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_user(username):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT username, password, fullname, dob FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"username": row["username"], "password": row["password"], "fullname": row["fullname"], "dob": row["dob"]}
    return None

def create_user(username, hashed_password, fullname=None, dob=None):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, fullname, dob, created_at) VALUES (?, ?, ?, ?, ?)",
              (username, hashed_password, fullname, dob, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return True

def save_login_history(username, action):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO login_history (username, action, timestamp) VALUES (?, ?, ?)",
              (username, action, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_login_history(username, limit=200):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT id, action, timestamp FROM login_history WHERE username = ? ORDER BY id DESC LIMIT ?", (username, limit))
    rows = c.fetchall()
    conn.close()
    return [{"id": r["id"], "action": r["action"], "timestamp": r["timestamp"]} for r in rows]

def delete_login_entry(entry_id):
    if entry_id is None:
        return False
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM login_history WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
    return True

def update_login_entry(entry_id, new_timestamp):
    if entry_id is None or new_timestamp is None:
        return False
    conn = _get_conn()
    c = conn.cursor()
    c.execute("UPDATE login_history SET timestamp = ? WHERE id = ?", (new_timestamp, entry_id))
    conn.commit()
    conn.close()
    return True
