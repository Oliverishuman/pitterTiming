import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "pitterTiming.db")

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    print("🔧 INIT_DB: Running database creation...")
    with get_connection() as conn:
        cursor = conn.cursor()

        print("🔧 Creating users table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                profile_pic TEXT
            )
        """)

        print("🔧 Creating riders table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS riders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                bike TEXT NOT NULL,
                best_lap TEXT
            )
        """)

        print("🔧 Creating laps table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS laps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rider_id INTEGER,
                lap_time TEXT,
                FOREIGN KEY (rider_id) REFERENCES riders (id)
            )
        """)

        conn.commit()
        print("✅ DB Initialized and committed.")

def get_rider_by_id(rider_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM riders WHERE id = ?", (rider_id,))
        return cursor.fetchone()

def get_laps_by_rider(rider_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT lap_time FROM laps WHERE rider_id = ?", (rider_id,))
        return cursor.fetchall()

def insert_lap(rider_id, lap_time):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO laps (rider_id, lap_time) VALUES (?, ?)", (rider_id, lap_time))
        conn.commit()

def get_all_riders():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM riders")
        return cursor.fetchall()