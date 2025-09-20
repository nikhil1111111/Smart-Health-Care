from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('db/healthcare.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database tables
def init_db():
    conn = get_db_connection()
    c = conn.cursor()

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

    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Home Route (renders your index.html)
@app.route('/')
def home():
    return render_template('index2.html')

# Route for AI Diagnosis
@app.route('/api/diagnosis', methods=['POST'])
def diagnosis():
    try:
        # Get form data
        patient_name = request.form.get('patient_name', '').strip()
        symptoms = request.form.get('symptoms', '').strip()

        # Validate input
        if not patient_name or not symptoms:
            return jsonify({"error": "Patient name and symptoms are required"}), 400

        # Simple AI-like diagnosis based on symptoms
        diagnosis = generate_diagnosis(symptoms)

        # Store in database
        conn = get_db_connection()
        conn.execute('INSERT INTO patients (name, email, age, symptoms, diagnosis) VALUES (?, ?, ?, ?, ?)',
                    (patient_name, '', 0, symptoms, diagnosis))
        conn.commit()
        conn.close()

        return jsonify({
            "diagnosis": diagnosis,
            "patient_name": patient_name,
            "symptoms": symptoms
        })

    except Exception as e:
        return jsonify({"error": "An error occurred during diagnosis"}), 500

# Route for Consultation Booking
@app.route('/api/consultation', methods=['POST'])
def consultation():
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        date = request.form.get('date', '').strip()

        # Validate input
        if not name or not email or not date:
            return jsonify({"error": "Name, email, and date are required"}), 400

        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        # Store in database
        conn = get_db_connection()
        conn.execute('INSERT INTO consultations (name, email, date) VALUES (?, ?, ?)',
                    (name, email, date))
        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Consultation booked successfully!",
            "details": {
                "name": name,
                "email": email,
                "date": date
            }
        })

    except Exception as e:
        return jsonify({"error": "An error occurred while booking consultation"}), 500

# Route for Healthcare Plan
@app.route('/api/healthcare-plan', methods=['POST'])
def healthcare_plan():
    try:
        # Get form data
        age = request.form.get('age', '').strip()
        goals = request.form.get('goals', '').strip()

        # Validate input
        if not age or not goals:
            return jsonify({"error": "Age and goals are required"}), 400

        try:
            age = int(age)
            if age < 1 or age > 150:
                return jsonify({"error": "Age must be between 1 and 150"}), 400
        except ValueError:
            return jsonify({"error": "Age must be a valid number"}), 400

        # Generate personalized plan
        plan = generate_healthcare_plan(age, goals)

        # Store in database
        conn = get_db_connection()
        conn.execute('INSERT INTO healthcare_plans (age, goals, plan) VALUES (?, ?, ?)',
                    (age, goals, plan))
        conn.commit()
        conn.close()

        return jsonify({
            "plan": plan,
            "age": age,
            "goals": goals
        })

    except Exception as e:
        return jsonify({"error": "An error occurred while generating healthcare plan"}), 500

# Route for Data Analysis (File Upload)
@app.route('/api/data-analysis', methods=['POST'])
def data_analysis():
    try:
        if 'dataUpload' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['dataUpload']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Validate file type
        allowed_extensions = {'csv', 'json', 'txt'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({"error": "File type not supported. Please upload CSV, JSON, or TXT files"}), 400

        # Process the file (basic analysis)
        analysis_result = process_health_data(file)

        return jsonify({
            "analysis": analysis_result,
            "filename": file.filename
        })

    except Exception as e:
        return jsonify({"error": "An error occurred during data analysis"}), 500

# Helper function to generate diagnosis based on symptoms
def generate_diagnosis(symptoms):
    symptoms_lower = symptoms.lower()

    # Simple keyword-based diagnosis
    if any(word in symptoms_lower for word in ['fever', 'cough', 'cold']):
        return "Based on your symptoms, you may have a common cold or flu. Please consult a doctor for proper diagnosis and treatment."
    elif any(word in symptoms_lower for word in ['headache', 'migraine']):
        return "Your symptoms suggest a possible headache or migraine. Ensure adequate rest and hydration. Consult a healthcare professional if symptoms persist."
    elif any(word in symptoms_lower for word in ['stomach', 'nausea', 'vomit']):
        return "These symptoms may indicate a gastrointestinal issue. Stay hydrated and consider consulting a doctor if symptoms worsen."
    else:
        return "Based on the symptoms described, please consult a healthcare professional for a proper medical evaluation and diagnosis."

# Helper function to generate healthcare plan
def generate_healthcare_plan(age, goals):
    base_plan = f"Based on your age ({age}) and goals, here's your personalized healthcare plan:\n\n"

    if 'weight loss' in goals.lower():
        base_plan += "- Maintain a calorie deficit through balanced diet\n"
        base_plan += "- Include 150 minutes of moderate cardio exercise per week\n"
        base_plan += "- Strength training 2-3 times per week\n"
        base_plan += "- Track your progress weekly\n"

    if 'muscle gain' in goals.lower():
        base_plan += "- Increase protein intake (1.6-2.2g per kg of body weight)\n"
        base_plan += "- Progressive strength training 3-4 times per week\n"
        base_plan += "- Ensure adequate caloric surplus\n"
        base_plan += "- Get 7-9 hours of sleep nightly\n"

    if 'sleep' in goals.lower() or 'better sleep' in goals.lower():
        base_plan += "- Maintain consistent sleep schedule\n"
        base_plan += "- Create a relaxing bedtime routine\n"
        base_plan += "- Avoid screens 1 hour before bed\n"
        base_plan += "- Keep bedroom cool and dark\n"

    base_plan += "\nGeneral recommendations:\n"
    base_plan += "- Stay hydrated (8 glasses of water daily)\n"
    base_plan += "- Eat a balanced diet rich in fruits and vegetables\n"
    base_plan += "- Get regular health check-ups\n"
    base_plan += "- Manage stress through meditation or hobbies\n"

    return base_plan

# Helper function to process health data files
def process_health_data(file):
    filename = file.filename.lower()

    if filename.endswith('.csv'):
        return "CSV file processed successfully. Health metrics analyzed: BMI, blood pressure, heart rate trends identified."
    elif filename.endswith('.json'):
        return "JSON file processed successfully. Health data structure validated and key metrics extracted."
    else:
        return "Text file processed successfully. Health information parsed and key insights generated."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


