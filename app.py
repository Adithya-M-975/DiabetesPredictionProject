from flask import Flask, render_template, request
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
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():

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

    if prediction[0] == 1:
        result = "Diabetic"
    else:
        result = "Non-Diabetic"
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (pregnancies, glucose, bloodpressure,
    skinthickness, insulin, bmi,
    dpf, age, prediction)

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        result
    ))

    conn.commit()
    conn.close()

    return render_template(
        'index.html',
        prediction_text=result
    )
    

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=False)