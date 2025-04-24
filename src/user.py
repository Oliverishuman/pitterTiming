from flask_login import UserMixin
import sqlite3
import os

# Define database location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "pitterTiming.db")

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    def __init__(self, id, username, password, profile_pic=None):
        self.id = id
        self.username = username
        self.password = password
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(row["id"], row["username"], row["password"], row["profile_pic"])
            return None

    @staticmethod
    def get_by_username(username):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return User(row["id"], row["username"], row["password"], row["profile_pic"])
            return None

    @staticmethod
    def create(username, hashed_password):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()

    @staticmethod
    def update_profile(user_id, new_username):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            conn.commit()