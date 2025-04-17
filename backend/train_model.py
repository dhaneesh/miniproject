import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import shap
import joblib

# Load dataset (replace with actual dataset)
data = pd.read_csv("iot_security_data.csv")

# Data Preprocessing
X = data.drop("attack_label", axis=1)
y = data["attack_label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "anomaly_model.pkl")

# SHAP Explainability
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

# Save SHAP values
joblib.dump(shap_values, "shap_values.pkl")

# Evaluate Model
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))
