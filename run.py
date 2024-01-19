import sqlite3

DATABASE_URI = "sqlite:///db.db"

# Create SQLite database file and connect to it
conn = sqlite3.connect("db.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define the User table schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        balance INTEGER DEFAULT 0
    )
''')

# Insert dummy data into the User table
dummy_data = [
    ("User1", 100),
    ("User2", 50),
    ("User3", 200),
]

cursor.executemany('''
    INSERT INTO users (name, balance)
    VALUES (?, ?)
''', dummy_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Dummy data has been successfully created.")
