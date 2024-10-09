from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('db/healthcare.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home Route (renders your index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Route for AI Diagnosis
@app.route('/api/diagnosis', methods=['POST'])
def diagnosis():
    symptoms = request.form['symptoms']
    # Use AI model here to predict diagnosis based on symptoms
    return jsonify({"diagnosis": "You might have a cold"})

# Route for Consultation Booking
@app.route('/api/consultation', methods=['POST'])
def consultation():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    conn = get_db_connection()
    conn.execute('INSERT INTO consultations (name, email, date) VALUES (?, ?, ?)', (name, email, date))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Consultation booked!"})

# Route for Healthcare Plan
@app.route('/api/healthcare-plan', methods=['POST'])
def healthcare_plan():
    age = request.form['age']
    goals = request.form['goals']
    # You can store this in the database and provide personalized plans
    return jsonify({"plan": "Exercise regularly and eat a balanced diet."})

# Route for Data Analysis (File Upload)
@app.route('/api/data-analysis', methods=['POST'])
def data_analysis():
    if 'dataUpload' in request.files:
        file = request.files['dataUpload']
        # Process the uploaded health data file
        return jsonify({"analysis": "Data analyzed successfully!"})
    return jsonify({"error": "No file uploaded!"}), 400

if __name__ == '__main__':
    app.run(debug=True)


