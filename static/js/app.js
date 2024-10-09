// Diagnostic Form Submission
document.getElementById('diagnosticForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const age = document.getElementById('age').value;
    const glucose = document.getElementById('glucose').value;
    const bmi = document.getElementById('bmi').value;

    fetch('/diagnosis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ age: age, glucose: glucose, bmi: bmi })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('diagnosisResult').innerText = data.diagnosis;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Consultation Booking Form Submission
document.getElementById('consultationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    fetch('/consultation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, date: date, time: time })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('bookingResult').innerText = data.booking;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Healthcare Plan Form Submission
document.getElementById('planForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const age = document.getElementById('age').value;
    const symptoms = document.getElementById('symptoms').value;

    fetch('/healthcare_plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ age: age, symptoms: symptoms })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('planResult').innerText = data.plan;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Health Data Analysis Form Submission
document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const healthData = document.getElementById('healthData').value;

    fetch('/health_data_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ healthData: healthData })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('dataResult').innerText = data.analysis;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
