import sqlite3
# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('db/healthcare.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create the "patients" table
c.execute('''CREATE TABLE patients (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             email TEXT NOT NULL,
             age INTEGER NOT NULL,
             symptoms TEXT NOT NULL
             )''')

# Create the "consultations" table
c.execute('''CREATE TABLE consultations (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             date TEXT NOT NULL,
             time TEXT NOT NULL
             )''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")