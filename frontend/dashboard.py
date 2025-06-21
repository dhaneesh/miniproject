import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="IoT Threat Classification", layout="centered")

st.title("🔍 IoT Threat Classification Dashboard")
st.markdown("Enter network packet details below to classify the traffic type.")

# Initialize prediction history
if "history" not in st.session_state:
    st.session_state.history = []

# Input form
with st.form("input_form"):
    packet_size = st.number_input("Packet Size", min_value=1, value=500)
    duration = st.number_input("Duration (s)", min_value=0.01, value=1.0)
    protocol = st.selectbox("Protocol", options=["TCP", "UDP", "ICMP"], index=0)
    src_bytes = st.number_input("Source Bytes", min_value=0, value=1000)
    dst_bytes = st.number_input("Destination Bytes", min_value=0, value=1000)
    
    submitted = st.form_submit_button("Classify Threat")

# Protocol encoding
protocol_map = {"TCP": 0, "UDP": 1, "ICMP": 2}

# API interaction
if submitted:
    data = {
        "packet_size": packet_size,
        "duration": duration,
        "protocol": protocol_map[protocol],
        "src_bytes": src_bytes,
        "dst_bytes": dst_bytes
    }

    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=data)
        result = response.json()
        threat_type = result['threat_type']

        # Log prediction
        st.session_state.history.append({
            "time": datetime.now(),
            "threat": threat_type
        })

        st.success(f"🛡️ Predicted Threat Type: **{threat_type}**")

    except Exception as e:
        st.error(f"Error: {e}")

# Display charts if we have any history
if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)

    # Bar Chart: Threat frequency
    st.subheader("📊 Threat Type Distribution")
    threat_counts = history_df['threat'].value_counts()
    st.bar_chart(threat_counts)

    # Pie Chart
    st.subheader("🧩 Threat Type Proportions")
    fig1, ax1 = plt.subplots()
    threat_counts.plot.pie(autopct="%1.1f%%", ax=ax1, startangle=90)
    ax1.set_ylabel('')
    ax1.set_title("Threat Breakdown")
    st.pyplot(fig1)

    # # Line Chart: Predictions over time
    # st.subheader("📈 Prediction Timeline")
    # # timeline_df = history_df.groupby(pd.to_datetime(history_df['time']).dt.floor('min')).size()
    # # timeline_df.name = "Predictions"
    # # st.line_chart(timeline_df)

    # timeline_df = history_df.groupby(pd.to_datetime(history_df['time']).dt.floor('min')).size()
    # timeline_df.name = "Predictions"
    # st.line_chart(timeline_df)
