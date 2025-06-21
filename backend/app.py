import joblib
import pandas as pd
from flask import Flask, request, jsonify
from email_utils import send_email_alert
from datetime import datetime

app = Flask(__name__)

# Load model and label encoder
model = joblib.load('anomaly_model.pkl')
encoder = joblib.load('label_encoder.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)
    predicted_label = encoder.inverse_transform(prediction)[0]

     # 🔔 Send email if not normal
    if predicted_label.lower() != "normal":
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        send_email_alert(predicted_label, timestamp, to_email="alappats098@gmail.com")
                         
    return jsonify({'threat_type': predicted_label})

if __name__ == '__main__':
    app.run(debug=True)
