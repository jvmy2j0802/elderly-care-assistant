import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to DB
conn = sqlite3.connect("multiagent_logs.db")
df = pd.read_sql_query("SELECT * FROM agent_logs", conn)

# Ensure timestamp is in datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# --------------------------------------------
# FILTERING OPTIONS
# --------------------------------------------
filter_by_user = input("🔍 Enter User ID to filter (or press Enter to skip): ").strip()
filter_by_date = input("📅 Enter Date (YYYY-MM-DD) to filter (or press Enter to skip): ").strip()

if filter_by_user:
    df = df[df["user_id"] == filter_by_user]

if filter_by_date:
    try:
        date_obj = datetime.strptime(filter_by_date, "%Y-%m-%d").date()
        df = df[df["timestamp"].dt.date == date_obj]
    except ValueError:
        print("⚠️ Invalid date format. Showing all data.")

# --------------------------------------------
# DISPLAY LOGS & STATS
# --------------------------------------------
print("\n🔍 Filtered Logs:\n")
print(df.sort_values("timestamp", ascending=False).head(20))

print("\n📊 Usage Stats:")
print("• Total tool calls:", len(df))
print("• Unique users:", df['user_id'].nunique())
print("• Tool usage breakdown:\n", df['tool'].value_counts())

# --------------------------------------------
# EXPORT TO EXCEL
# --------------------------------------------
export = input("💾 Do you want to export logs to Excel? (yes/no): ").strip().lower()
if export == "yes":
    filename = f"agent_logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"✅ Logs exported to: {filename}")

# --------------------------------------------
# PLOT TOOL USAGE
# --------------------------------------------
if not df.empty:
    plt.figure(figsize=(8, 5))
    df['tool'].value_counts().plot(kind='bar', color='orchid')
    plt.title("Tool Usage Frequency")
    plt.xlabel("Tool")
    plt.ylabel("Number of Calls")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()
else:
    print("⚠️ No data to visualize.")
