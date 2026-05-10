from flask import Flask, render_template, request
import pickle
import numpy as np

# Load trained model
model = pickle.load(open("diabetes_model.pkl", "rb"))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Create Flask app
app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():

    # Get form values
    pregnancies = float(request.form.get('pregnancies',0))
    glucose = float(request.form.get('glucose',0))
    bloodpressure = float(request.form.get('bloodpressure',0))
    skinthickness = float(request.form.get('skinthickness',0))
    insulin = float(request.form.get('insulin',0))
    bmi = float(request.form.get('bmi',0))
    dpf = float(request.form.get('dpf',0))
    age = float(request.form.get('age',0))

    # Convert to array
    input_data = np.array([[pregnancies, glucose, bloodpressure,
                            skinthickness, insulin, bmi, dpf, age]])
    scaled_data = scaler.transform(input_data)


    # Predict
    prediction = model.predict(scaled_data)

    # Display result
    if prediction[0] == 1:
        result = "Diabetic"
    else:
        result = "Non-Diabetic"

    return render_template('index.html', prediction_text=result)

# Run app
if __name__ == "__main__":
    app.run(debug=True)