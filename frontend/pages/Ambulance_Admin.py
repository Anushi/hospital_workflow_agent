import streamlit as st
from utils.api_client import send_ambulance_data
from components.charts import show_vitals_chart

# We wrap everything in a function so app.py can call it automatically
def show_ambulance_ui():
    st.title("🚑 Ambulance Intake System")

    st.warning(
        "This system provides workflow assistance only. "
        "All outputs require clinical validation by hospital staff."
    )

    # -----------------------------
    # Ambulance & Patient Details
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Case Identification")
        ambulance_id = st.selectbox(
            "Ambulance ID",
            ["AMB-01", "AMB-02", "AMB-03"]
        )
        age = st.number_input("Patient Age", min_value=0, max_value=120, value=60)
        
        st.write("---")
        st.subheader("🧍 Medical History")
        dm = st.checkbox("Known Diabetes")
        htn = st.checkbox("Known Hypertension")
        hf = st.checkbox("Known Heart Failure")

    with col2:
        st.subheader("❤️ Live Vital Signs")
        hr = st.slider("Heart Rate (bpm)", 40, 200, 80)
        sbp = st.number_input("Systolic BP (mmHg)", value=120)
        rr = st.number_input("Respiratory Rate (/min)", value=16)
        spo2 = st.slider("SpO₂ (%)", 70, 100, 98)

    # -----------------------------
    # Action: Send to Hospital
    # -----------------------------
    st.write("---")
    if st.button("🚨 Send to Hospital", use_container_width=True):

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

        # 1. Send data to Backend via utils/api_client.py
        try:
            res = send_ambulance_data(payload)
            st.success("✅ Data successfully transmitted to Hospital Command Center.")

            # 2. Show Visuals from components/charts.py
            st.markdown("### 📊 Live Vitals Overview")
            show_vitals_chart(hr, sbp, spo2, rr)

            st.markdown("---")
            st.subheader("🏥 AI Agent Response (Real-time)")

            # 3. Display AI Results from Backend Agents
            t_col, a_col, r_col = st.columns(3)

            with t_col:
                st.info("🎯 Triage Status")
                st.metric("Priority", res['triage']['priority'])
                st.write(res["triage"]["message"])

            with a_col:
                st.info("📋 Admission Path")
                st.write(f"Level: **{res['admission']['suggested_admission_level']}**")
                st.caption(res["admission"]["note"])

            with r_col:
                st.info("🏥 Resources")
                st.write(f"🛏 Bed: {res['resource']['bed']}")
                st.write(f"👨‍⚕️ Teams: {', '.join(res['resource']['teams'])}")

            st.caption(f"_{res['disclaimer']}_")

        except Exception as e:
            st.error(f"❌ Connection Error: Backend server unreachable. {e}")

# This part ensures the page still works if opened directly from the sidebar
if __name__ == "__main__":
    st.set_page_config(page_title="Ambulance Intake System", layout="wide")
    
    # Check if user is logged in and is an Ambulance Admin
    if not st.session_state.get("logged_in", False) or st.session_state.get("auth_role") != "Ambulance Admin":
        st.warning("⚠️ Access Denied. Please login as Ambulance Admin.")
        st.stop()
        
    show_ambulance_ui()