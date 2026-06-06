import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE predictions
ADD COLUMN timestamp TEXT
""")

conn.commit()
conn.close()

print("Timestamp column added successfully!")