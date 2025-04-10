import sqlite3

conn = sqlite3.connect("elderly_care.db")
cursor = conn.cursor()

# Query from the correct table
cursor.execute("SELECT * FROM health_data")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
