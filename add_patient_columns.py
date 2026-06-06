import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE predictions ADD COLUMN patient_name TEXT"
    )
    print("Patient Name column added")

except:
    print("Patient Name column already exists")

try:
    cursor.execute(
        "ALTER TABLE predictions ADD COLUMN gender TEXT"
    )
    print("Gender column added")

except:
    print("Gender column already exists")

conn.commit()
conn.close()

print("Database updated successfully!")