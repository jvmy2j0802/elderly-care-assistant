# safety_tools.py
from langchain.tools import tool
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "elderly_care.db")

@tool
def get_recent_falls(user_id: str) -> str:
    """Fetches recent fall incidents for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT Timestamp, Location, ImpactForceLevel
        FROM safety_data
        WHERE user_id = ?
        AND fall_detected = 'Yes'
        ORDER BY Timestamp DESC LIMIT 5;
    """
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No recent falls detected for this user."

    result = "\n".join([f"{ts} at {loc}, Impact Level: {impact}" for ts, loc, impact in rows])
    return f"Recent falls:\n{result}"
