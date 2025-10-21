# backend/database.py
import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                fullname TEXT,
                dob TEXT,
                created_at TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE login_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                action TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

def create_user(username, password_hash, fullname="", dob=""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, fullname, dob, created_at) VALUES (?, ?, ?, ?, ?)",
                (username, password_hash, fullname, dob, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username, password, fullname, dob FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"username": row["username"], "password": row["password"], "fullname": row["fullname"], "dob": row["dob"]}
    return None

def save_login_history(username, action):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO login_history (username, action, timestamp) VALUES (?, ?, ?)",
                (username, action, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_login_history(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, action, timestamp FROM login_history WHERE username = ? ORDER BY id DESC", (username,))
    rows = cur.fetchall()
    conn.close()
    return [{"id": r["id"], "username": r["username"], "action": r["action"], "timestamp": r["timestamp"]} for r in rows]

def delete_login_entry(entry_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM login_history WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def update_login_entry(entry_id, action):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE login_history SET action = ? WHERE id = ?", (action, entry_id))
    conn.commit()
    conn.close()
