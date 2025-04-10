# db_utils.py

import sqlite3
from datetime import datetime

DB_NAME = "elderly_care.db"

import os
print("Using DB path:", os.path.abspath(DB_NAME))


# 🔌 Database Connection
def get_connection():
    return sqlite3.connect(DB_NAME)


# 🏗️ Initialize Tables
def initialize_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # health_data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "Device-ID/User-ID" TEXT,
                "Timestamp" TEXT,
                "Heart Rate" INTEGER,
                "Heart Rate Below/Above Threshold (Yes/No)" TEXT,
                "Blood Pressure" TEXT,
                "Blood Pressure Below/Above Threshold (Yes/No)" TEXT,
                "Glucose Levels" REAL,
                "Glucose Levels Below/Above Threshold (Yes/No)" TEXT,
                "Oxygen Saturation (SpO₂%)" REAL,
                "SpO₂ Below Threshold (Yes/No)" TEXT,
                "Alert Triggered (Yes/No)" TEXT,
                "Caregiver Notified (Yes/No)" TEXT
            )
        ''')

        # safety_events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS safety_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "Device-ID/User-ID" TEXT,
                "Timestamp" TEXT,
                "Movement Activity" TEXT,
                "Fall Detected (Yes/No)" TEXT,
                "Impact Force Level" REAL,
                "Post-Fall Inactivity Duration (Seconds)" REAL,
                "Location" TEXT,
                "Alert Triggered (Yes/No)" TEXT,
                "Caregiver Notified (Yes/No)" TEXT
            )
        ''')

        # medication_reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medication_reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "Device-ID/User-ID" TEXT,
                "Timestamp" TEXT,
                "Reminder Type" TEXT,
                "Scheduled Time" TEXT,
                "Reminder Sent (Yes/No)" TEXT,
                "Acknowledged (Yes/No)" TEXT
            )
        ''')

        conn.commit()

# ➕ Insert Functions
def insert_health_data(user_id: str, heart_rate: int, systolic: int, diastolic: int):
    timestamp = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO health_data (user_id, heart_rate, systolic, diastolic, timestamp)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (user_id, heart_rate, systolic, diastolic, timestamp)
        )
        conn.commit()


def insert_medication_reminder(user_id: str, time: str):
    timestamp = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO medication_reminders (user_id, time, timestamp)
            VALUES (?, ?, ?)
            ''',
            (user_id, time, timestamp)
        )
        conn.commit()


def insert_fall_event(user_id: str, activity: str, fall: bool):
    timestamp = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO fall_events (user_id, activity, fall_detected, timestamp)
            VALUES (?, ?, ?, ?)
            ''',
            (user_id, activity, fall, timestamp)
        )
        conn.commit()


# 🔍 Read Functions
def get_latest_health_data(user_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT heart_rate, systolic, diastolic, timestamp
            FROM health_data
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
            ''',
            (user_id,)
        )
        return cursor.fetchone()


def get_today_medication_reminders(user_id: str):
    today = datetime.now().date().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT time
            FROM medication_reminders
            WHERE user_id = ?
            AND date(timestamp) = ?
            ''',
            (user_id, today)
        )
        return cursor.fetchall()
    
# ✅ Call initialize_db() when run directly 
if __name__ == "__main__":
    choice = input("Do you want to reset the database tables? (y/n): ").lower()
    if choice == 'y':
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS health_data")
            cursor.execute("DROP TABLE IF EXISTS medication_reminders")
            cursor.execute("DROP TABLE IF EXISTS fall_events")
            conn.commit()
            print("Tables dropped.")
        initialize_db()
        print("Tables recreated.")
    else:
        initialize_db()
        print("Database initialized.")
