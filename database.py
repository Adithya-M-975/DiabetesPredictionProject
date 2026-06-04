import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pregnancies REAL,
    glucose REAL,
    bloodpressure REAL,
    skinthickness REAL,
    insulin REAL,
    bmi REAL,
    dpf REAL,
    age REAL,
    prediction TEXT
)
''')

conn.commit()
conn.close()

print("Database Created Successfully!")