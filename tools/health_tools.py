# health_tools.py
from langchain.tools import tool
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "elderly_care.db")

@tool
def get_recent_health_alerts(user_id: str) -> str:
    """Fetches recent health alerts for a user from the health_data table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT Timestamp, HeartRate, BloodPressure, GlucoseLevels, SpO2
        FROM health_data
        WHERE user_id = ?
        AND alert_triggered = 'Yes'
        ORDER BY Timestamp DESC LIMIT 5;
    """
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No recent health alerts found for this user."

    result = "\n".join([f"{ts}: HR={hr}, BP={bp}, Glucose={gl}, SpO2={spo2}" for ts, hr, bp, gl, spo2 in rows])
    return f"Recent health alerts:\n{result}"
