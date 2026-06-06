from flask import Flask, render_template, request, redirect
from datetime import datetime
import pickle
import numpy as np
import sqlite3

# Load trained XGBoost model
model = pickle.load(open("xgboost_model.pkl", "rb"))

# Load scaler
scaler = pickle.load(open("scaler.pkl", "rb"))

# Create Flask app
app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
             "SELECT * FROM users WHERE username=? AND password=?",
              (username, password)
         )

        user = cursor.fetchone()

        conn.close()

        if user:
         return render_template('index.html')

        return render_template(
          'login.html',
          error="Invalid Username or Password"
        )

    return render_template('login.html')

@app.route('/predict_page')
def predict_page():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match"

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username,email,password) VALUES (?,?,?)",
                (username,email,password)
            )

            conn.commit()

        except:
            return "Username already exists"

        finally:
            conn.close()

        return redirect('/')

    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()
        if user:
            return render_template(
                'forgot_password.html',
                password=user[0]
            )

    return render_template('forgot_password.html')
  
# Prediction route
@app.route('/predict', methods=['POST'])
def predict():  

    patient_name = request.form['patient_name']
    gender = request.form['gender']

    pregnancies = float(request.form.get('pregnancies', 0))
    glucose = float(request.form.get('glucose', 0))
    bloodpressure = float(request.form.get('bloodpressure', 0))
    skinthickness = float(request.form.get('skinthickness', 0))
    insulin = float(request.form.get('insulin', 0))
    bmi = float(request.form.get('bmi', 0))
    dpf = float(request.form.get('dpf', 0))
    age = float(request.form.get('age', 0))

    input_data = np.array([[pregnancies, glucose, bloodpressure,
                            skinthickness, insulin, bmi, dpf, age]])

    scaled_data = scaler.transform(input_data)

    prediction = model.predict(scaled_data)
    probability = model.predict_proba(scaled_data)

    if prediction[0] == 1:
        result = "Diabetic"
    else:
        result = "Non-Diabetic"

    current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")    
    
    confidence = round(
        max(probability[0]) * 100,
        2
    )
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    cursor.execute("""
    INSERT INTO predictions
    (pregnancies, glucose, bloodpressure,
    skinthickness, insulin, bmi,
    dpf, age, prediction, timestamp, patient_name, gender)

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        pregnancies,
        glucose,
        bloodpressure,
        skinthickness,
        insulin,
        bmi,
        dpf,
        age,
        result,
        current_time,
        patient_name,
        gender
    ))

    conn.commit()
    print("Data saved:", result)
    conn.close()

    return render_template(
        'index.html',
        prediction_text=result,
        confidence=confidence
    )

@app.route('/history')
def history():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    records = cursor.fetchall()

    total_predictions = len(records)

    diabetic_count = sum(
        1 for row in records
        if row[9] == "Diabetic"
    )

    non_diabetic_count = sum(
        1 for row in records
        if row[9] == "Non-Diabetic"
    )

    age_labels = [row[8] for row in records]

    conn.close()

    return render_template(
        'history.html',
        records=records,
        total_predictions=total_predictions,
        diabetic_count=diabetic_count,
        non_diabetic_count=non_diabetic_count,
        age_labels=age_labels
    )

@app.route('/logout')
def logout():
    return redirect('/')

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=False)