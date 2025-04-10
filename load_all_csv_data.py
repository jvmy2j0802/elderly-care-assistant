import pandas as pd
from db_utils import get_connection

# Load CSVs
df_health = pd.read_csv("data/health_monitoring.csv")
df_safety = pd.read_csv("data/safety_monitoring.csv")
df_reminders = pd.read_csv("data/daily_reminder.csv")

# Optional: Debug columns
print("Health columns:", df_health.columns.tolist())
print("Safety columns:", df_safety.columns.tolist())
print("Reminder columns:", df_reminders.columns.tolist())

# Push to DB
with get_connection() as conn:
    df_health.to_sql("health_data", conn, if_exists="append", index=False)
    df_safety.to_sql("safety_events", conn, if_exists="append", index=False)
    df_reminders.to_sql("medication_reminders", conn, if_exists="append", index=False)

print("✅ All data loaded successfully!")
