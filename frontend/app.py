import streamlit as st
<<<<<<< HEAD

# 1. Page Configuration
st.set_page_config(page_title="AI Hospital Network", layout="wide")

# 2. Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "auth_role" not in st.session_state:
    st.session_state["auth_role"] = None

# ====================================
# 🔓 LOGIN SCREEN
# ====================================
if not st.session_state["logged_in"]:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.title("🏥 AI Hospital Network Login")
        st.write("Please enter your specific credentials below.")

        with st.form("login"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            
            if st.form_submit_button("Access Portal", use_container_width=True):
                # --- SEPARATE CREDENTIALS LOGIC ---
                
                # 🚑 Ambulance Credentials
                if user == "ambulance_user" and pwd == "amb789":
                    st.session_state["logged_in"] = True 
                    st.session_state["auth_role"] = "Ambulance Admin"
                    st.rerun()

                # 🏥 Hospital Credentials
                elif user == "hospital_user" and pwd == "hosp456":
                    st.session_state["logged_in"] = True 
                    st.session_state["auth_role"] = "Hospital Command Center"
                    st.rerun()
                
                else:
                    st.error("❌ Invalid Username or Password")

# ====================================
# 🚀 AUTOMATIC DASHBOARD REDIRECT
# ====================================
else:
    # Sidebar Logout Option
    st.sidebar.title(f"👤 {st.session_state['auth_role']}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["auth_role"] = None
        st.rerun()

    # Automatic Logic: Run the UI function based on the authenticated role
    if st.session_state["auth_role"] == "Ambulance Admin":
        try:
            from pages.Ambulance_Admin import show_ambulance_ui
            show_ambulance_ui()
        except ImportError:
            st.error("Could not find 'show_ambulance_ui' in pages/Ambulance_Admin.py")

    elif st.session_state["auth_role"] == "Hospital Command Center":
        try:
            from pages.hospital_dashboard import show_hospital_ui
            show_hospital_ui()
        except ImportError:
            st.error("Could not find 'show_hospital_ui' in pages/hospital_dashboard.py")
=======
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
>>>>>>> 0ba03eb97bf983192968a5a9d7e2672d39c2ba99
