# frontend/app.py
import streamlit as st
import requests

API_BASE = st.secrets.get("API_BASE", "http://127.0.0.1:8000/api")

st.set_page_config(page_title="Hospital Multi-Agent UI", layout="wide")
st.title("🏥 Hospital Multi-Agent System (Streamlit frontend)")

# Load data button
if st.button("Load CSVs into backend"):
    try:
        r = requests.get(f"{API_BASE}/load-data", timeout=10)
        r.raise_for_status()
        st.success("Data loaded.")
        st.json(r.json())
    except Exception as e:
        st.error(f"Load failed: {e}")

patient_id = st.number_input("Enter patient id (patien_id)", min_value=1, step=1, value=1)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Run Triage"):
        r = requests.get(f"{API_BASE}/triage/{patient_id}", params={"use_vitals": True})
        if r.status_code == 200:
            st.subheader("Triage Result")
            st.json(r.json())
        else:
            st.error(f"Error: {r.text}")

with col2:
    if st.button("Run Admission"):
        r = requests.get(f"{API_BASE}/admission/{patient_id}", params={"use_vitals": True})
        if r.status_code == 200:
            st.subheader("Admission Result")
            st.json(r.json())
        else:
            st.error(f"Error: {r.text}")

with col3:
    if st.button("Run Resource Allocation"):
        r = requests.get(f"{API_BASE}/resource/{patient_id}")
        if r.status_code == 200:
            st.subheader("Resource Suggestion")
            st.json(r.json())
        else:
            st.error(f"Error: {r.text}")

st.markdown("---")
st.subheader("Live vitals test (send manual vitals to triage)")
hr = st.number_input("HR", value=80)
sbp = st.number_input("SBP", value=120)
rr = st.number_input("RR", value=16)
spo2 = st.number_input("SpO2", value=98)

if st.button("Send live vitals to triage"):
    payload = {"hr": hr, "sbp": sbp, "rr": rr, "spo2": spo2}
    r = requests.post(f"{API_BASE}/triage-live/{patient_id}", json=payload)
    if r.status_code == 200:
        st.json(r.json())
    else:
        st.error(f"Error: {r.text}")
