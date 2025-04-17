import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="IoT Threat Detection", layout="centered")

# UI headers and instructions
st.title("🔐 IoT Security Threat Detection with Explainable AI")
st.markdown("Enter comma-separated values for prediction:")
st.markdown("📌 Format: packet_size, duration, protocol (0-TCP,1-UDP,2-ICMP), src_bytes, dst_bytes")

# User input
user_input = st.text_input("Enter feature values:", "512,1.2,1,2000,3000")

# Detect button
if st.button("Detect Anomaly"):
    try:
        values = [float(x.strip()) for x in user_input.split(",")]

        if len(values) != 5:
            st.error("⚠️ Please enter exactly 5 values.")
        else:
            # Call the Flask API
            response = requests.post(
                "http://127.0.0.1:5000/predict",
                json={"features": values}
            )

            if response.status_code == 200:
                result = response.json()
                prediction = result["prediction"]
                shap_vals = result["shap_values"]
                feature_data = result["features"]

                label = "🚨 Anomaly Detected" if prediction == 1 else "✅ Normal Activity"
                st.success(f"Prediction: {label}")

                # Show feature values
                st.markdown("### 📊 Input Feature Breakdown")
                for key, val in feature_data.items():
                    st.write(f"{key}: {val}")

                # SHAP bar plot
                st.markdown("### 🧠 SHAP Feature Impact")
                fig, ax = plt.subplots()
                # If shap_vals is 2D (multi-output), pick SHAP values for class 1
                if isinstance(shap_vals[0], list) or (np.array(shap_vals).ndim > 1 and len(shap_vals[0]) > 1):
                    # Assuming class 1 is the positive class (anomaly)
                    shap_vals = [row[1] for row in shap_vals]

                # Plot the SHAP values
                ax.barh(list(feature_data.keys()), shap_vals)
                ax.set_xlabel("SHAP Value")
                ax.set_title("Feature Contribution to Prediction")
                st.pyplot(fig)
            else:
                st.error("❌ Server error: Unable to get prediction.")
    except Exception as e:
        st.error(f"❌ Invalid input format: {e}")
