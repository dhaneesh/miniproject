from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import joblib
import shap

# Load model
model = joblib.load("anomaly_model.pkl")
feature_names = ['packet_size', 'duration', 'protocol', 'src_bytes', 'dst_bytes']

# Initialize SHAP explainer with background data
X_background = pd.DataFrame([np.zeros(len(feature_names))], columns=feature_names)
explainer = shap.Explainer(model, X_background)

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    print(data)
    input_features = pd.DataFrame([data["features"]], columns=feature_names)

    prediction = model.predict(input_features)[0]
    shap_values = explainer(input_features)

    return jsonify({
        "prediction": int(prediction),
        "shap_values": shap_values.values[0].tolist(),
        "features": input_features.iloc[0].to_dict()
    })

if __name__ == "__main__":
    app.run(debug=True)