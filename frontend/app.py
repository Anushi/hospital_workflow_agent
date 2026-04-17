import streamlit as st

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