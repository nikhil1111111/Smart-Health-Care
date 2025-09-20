import sqlite3
import os
from datetime import datetime

def init_database():
    """Initialize the healthcare database with all required tables"""

    # Ensure db directory exists
    os.makedirs('db', exist_ok=True)

    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('db/healthcare.db')
    c = conn.cursor()

    # Enable foreign key support
    c.execute("PRAGMA foreign_keys = ON")

    # Create the "patients" table
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL,
                 age INTEGER NOT NULL,
                 symptoms TEXT NOT NULL,
                 diagnosis TEXT,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )''')

    # Create the "consultations" table
    c.execute('''CREATE TABLE IF NOT EXISTS consultations (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL,
                 date TEXT NOT NULL,
                 status TEXT DEFAULT 'pending',
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )''')

    # Create the "healthcare_plans" table
    c.execute('''CREATE TABLE IF NOT EXISTS healthcare_plans (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 age INTEGER NOT NULL,
                 goals TEXT NOT NULL,
                 plan TEXT NOT NULL,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )''')

    # Create the "health_data_analysis" table
    c.execute('''CREATE TABLE IF NOT EXISTS health_data_analysis (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 filename TEXT NOT NULL,
                 file_type TEXT NOT NULL,
                 analysis_result TEXT NOT NULL,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )''')

    # Create indexes for better performance (only on existing tables)
    try:
        c.execute('''CREATE INDEX IF NOT EXISTS idx_patients_created_at ON patients(created_at)''')
    except sqlite3.OperationalError:
        pass  # Column might not exist in older tables

    try:
        c.execute('''CREATE INDEX IF NOT EXISTS idx_consultations_date ON consultations(date)''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_consultations_status ON consultations(status)''')
    except sqlite3.OperationalError:
        pass  # Columns might not exist in older tables

    try:
        c.execute('''CREATE INDEX IF NOT EXISTS idx_healthcare_plans_created_at ON healthcare_plans(created_at)''')
    except sqlite3.OperationalError:
        pass  # Column might not exist in older tables

    try:
        c.execute('''CREATE INDEX IF NOT EXISTS idx_health_data_analysis_created_at ON health_data_analysis(created_at)''')
    except sqlite3.OperationalError:
        pass  # Column might not exist in older tables

    # Commit the changes
    conn.commit()

    # Check if tables are empty and add some sample data if needed
    c.execute("SELECT COUNT(*) FROM patients")
    if c.fetchone()[0] == 0:
        add_sample_data(conn, c)

    conn.close()
    print("✅ Database initialized successfully!")

def add_sample_data(conn, c):
    """Add sample data for testing purposes"""

    # Sample patients
    sample_patients = [
        ('John Doe', 'john@example.com', 30, 'Headache and fever', 'Possible flu symptoms'),
        ('Jane Smith', 'jane@example.com', 25, 'Stomach pain', 'Gastrointestinal issue'),
        ('Bob Johnson', 'bob@example.com', 45, 'Joint pain', 'Possible arthritis')
    ]

    c.executemany('''INSERT INTO patients (name, email, age, symptoms, diagnosis)
                     VALUES (?, ?, ?, ?, ?)''', sample_patients)

    # Sample consultations
    sample_consultations = [
        ('Alice Brown', 'alice@example.com', '2024-02-15'),
        ('Charlie Wilson', 'charlie@example.com', '2024-02-20')
    ]

    c.executemany('''INSERT INTO consultations (name, email, date)
                     VALUES (?, ?, ?)''', sample_consultations)

    # Sample healthcare plans
    sample_plans = [
        (28, 'Weight loss and better fitness', 'Exercise plan: 150 minutes cardio per week, strength training 3x/week'),
        (35, 'Muscle gain and strength', 'Strength training: 4x/week, protein-rich diet, progressive overload')
    ]

    c.executemany('''INSERT INTO healthcare_plans (age, goals, plan)
                     VALUES (?, ?, ?)''', sample_plans)

    conn.commit()
    print("📊 Sample data added successfully!")

def check_database():
    """Check database status and display information"""

    conn = sqlite3.connect('db/healthcare.db')
    c = conn.cursor()

    print("📋 Database Status:")
    print("=" * 50)

    # Check all tables
    tables = ['patients', 'consultations', 'healthcare_plans', 'health_data_analysis']

    for table in tables:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"📊 {table}: {count} records")

        # Show recent records for main tables
        if table in ['patients', 'consultations', 'healthcare_plans'] and count > 0:
            try:
                c.execute(f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT 1")
                recent = c.fetchone()
                print(f"   Recent: {recent[1]} - {recent[-1]}")
            except sqlite3.OperationalError:
                # Fallback if created_at column doesn't exist
                c.execute(f"SELECT * FROM {table} LIMIT 1")
                recent = c.fetchone()
                print(f"   Sample: {recent[1]}")

    # Database file info
    db_size = os.path.getsize('db/healthcare.db') if os.path.exists('db/healthcare.db') else 0
    print(f"💾 Database file size: {db_size} bytes")

    conn.close()

if __name__ == "__main__":
    print("🏥 Smart Healthcare Database Setup")
    print("=" * 50)

    # Initialize database
    init_database()

    # Check database status
    check_database()

    print("\n✅ Setup complete! You can now run the Flask application.")
    print("💡 To start the server: python app.py")
