import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv('iot_security__multi_data.csv')

# Features and labels
X = df.drop(columns=['attack_type'])
y = df['attack_type']

# Encode multi-class target
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=encoder.classes_))

# Save model and encoder
joblib.dump(model, 'anomaly_model.pkl')
joblib.dump(encoder, 'label_encoder.pkl')

print("✅ Model and encoder saved.")
