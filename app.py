from flask import Flask, render_template, request
import pickle
import numpy as np
from tensorflow.keras.models import load_model

# Load ANN model
model = load_model("diabetes_ann_model.keras")

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
    try:
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        bloodpressure = float(request.form['bloodpressure'])
        skinthickness = float(request.form['skinthickness'])
        insulin = float(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        age = float(request.form['age'])

        input_data = np.array([[pregnancies, glucose, bloodpressure,
                                skinthickness, insulin, bmi, dpf, age]])

        scaled_data = scaler.transform(input_data)

        prediction = model.predict(scaled_data)

        print("Prediction:", prediction)

        if prediction[0][0] > 0.5:
            result = "Diabetic"
        else:
            result = "Non-Diabetic"

        return render_template('index.html', prediction_text=result)

    except Exception as e:
        print("ERROR:", e)
        return str(e)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)