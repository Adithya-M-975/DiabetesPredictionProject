import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM predictions")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='predictions'")

conn.commit()

print("Database reset successfully")

conn.close()