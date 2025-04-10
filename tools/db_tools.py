from langchain.tools import tool
from langchain_core.tools import tool
import sqlite3

@tool
def get_user_info(user_id: str) -> dict:
    """Fetch user info from SQLite DB."""
    try:
        conn = sqlite3.connect("data/user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "user_id": row[0],
                "name": row[1],
                "age": row[2],
                "gender": row[3],
                "location": row[4]
            }
        else:
            return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}
    
@tool
def med_info() -> str:
    """Returns placeholder for medication information."""
    return "This tool can fetch info about medicines if web scraping or external API is enabled."

