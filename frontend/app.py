import streamlit as st
from utils.api_client import send_ambulance_data
from components.charts import show_vitals_chart


st.set_page_config(
    page_title="Hospital Pre-Arrival System",
    layout="centered"
)

st.title("🚑 AI-Driven Hospital Pre-Arrival Support")

st.warning(
    "This system provides workflow assistance only. "
    "All outputs require clinical validation by hospital staff."
)

# -----------------------------
# Ambulance Identification
# -----------------------------
st.subheader("🚑 Ambulance Information")

ambulance_id = st.selectbox(
    "Ambulance ID",
    ["AMB-01", "AMB-02", "AMB-03"]
)

# -----------------------------
# Patient Background
# -----------------------------
st.subheader("🧍 Ambulance-Collected Patient Details")

age = st.number_input("Age", min_value=0, max_value=120, value=60)
dm = st.checkbox("Known Diabetes")
htn = st.checkbox("Known Hypertension")
hf = st.checkbox("Known Heart Failure")

# -----------------------------
# Live Vitals
# -----------------------------
st.subheader("❤️ Live Vital Signs")

hr = st.number_input("Heart Rate (bpm)", value=80)
sbp = st.number_input("Systolic BP (mmHg)", value=120)
rr = st.number_input("Respiratory Rate (/min)", value=16)
spo2 = st.number_input("SpO₂ (%)", value=98)

# -----------------------------
# Send to Hospital
# -----------------------------
if st.button("🚨 Send to Hospital"):

    payload = {
        "ambulance_id": ambulance_id,
        "patient": {
            "age": age,
            "dm": int(dm),
            "htn": int(htn),
            "heart_failure": int(hf)
        },
        "vitals": {
            "hr": hr,
            "sbp": sbp,
            "rr": rr,
            "spo2": spo2
        }
    }
    st.markdown("### 📊 Live Vitals Overview")
    show_vitals_chart(hr, sbp, spo2, rr)


    res = send_ambulance_data(payload)

    st.markdown("---")
    st.subheader("🏥 Hospital Pre-Arrival Status")

    # -----------------------------
    # Triage Output
    # -----------------------------
    st.success(f"Risk Level: {res['triage']['priority']}")
    st.write(res["triage"]["message"])

    # -----------------------------
    # Admission Output
    # -----------------------------
    st.markdown("### 📋 Admission Path")
    st.write(res["admission"]["suggested_admission_level"])
    st.caption(res["admission"]["note"])

    # -----------------------------
    # Resource Output
    # -----------------------------
    st.markdown("### 🏥 Resource Preparation")
    st.write(f"🛏 Bed Type: {res['resource']['bed']}")
    st.write(f"👨‍⚕️ Teams Notified: {', '.join(res['resource']['teams'])}")
    st.info(res["resource"]["note"])

    st.caption(res["disclaimer"])
