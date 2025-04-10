# reminder_tools.py
from langchain.tools import tool
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "elderly_care.db")

@tool
def get_today_reminders(user_id: str) -> str:
    """Fetches today's reminders for a given user."""
    from datetime import datetime
    today = datetime.now().date()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT ReminderType, ScheduledTime, ReminderSent, Acknowledged
        FROM reminder_data
        WHERE user_id = ?
        AND date(Timestamp) = ?
        ORDER BY ScheduledTime;
    """
    cursor.execute(query, (user_id, today))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No reminders found for today."

    result = "\n".join([f"{t} at {st} | Sent: {rs} | Ack: {ack}" for t, st, rs, ack in rows])
    return f"Today's reminders:\n{result}"
