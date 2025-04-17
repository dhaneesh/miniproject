import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Mock sample data (you can replace this with your actual dataset like NSL-KDD or MedBIoT)
# Assume binary classification: 0 = normal, 1 = anomaly
data = pd.DataFrame({
    'packet_size': np.random.randint(50, 1500, 1000),
    'duration': np.random.uniform(0.1, 5.0, 1000),
    'protocol': np.random.randint(0, 3, 1000),  # e.g., 0 = TCP, 1 = UDP, 2 = ICMP
    'src_bytes': np.random.randint(0, 10000, 1000),
    'dst_bytes': np.random.randint(0, 10000, 1000),
    'label': np.random.choice([0, 1], 1000, p=[0.85, 0.15])  # Imbalanced (normal > anomaly)
})

X = data.drop("label", axis=1)
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "anomaly_model.pkl")
print("Model saved as anomaly_model.pkl")
