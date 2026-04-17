import streamlit as st
import websocket
import json
import threading
import queue
import time
import pandas as pd
import os
from datetime import datetime
import streamlit.components.v1 as components
from components.patient_view import display_patient_info

# Define the paths to your downloaded images
LOGO_PATH = "assets/TN-Tamilnadu.png"  #
WATERMARK_PATH = "assets/watermark.png"  #

def apply_custom_styling():
    # CSS for the Watermark effect
    st.markdown(
        f"""
        <style>
        /* Logo Styling at the top */
        .header-logo {{
            display: flex;
            justify-content: center;
            padding-bottom: 20px;
        }}
        
        /* Watermark Styling */
        .main .block-container::before {{
            content: "";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%; /* Adjust size as needed */
            height: 80%;
            background-image: url("data:image/png;base64,{get_image_base64(WATERMARK_PATH)}");
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            opacity: 0.08; /* Low opacity for "lite shadow" effect */
            filter: blur(2px); /* Slight blur to make it soft */
            z-index: -1; /* Place behind all content */
            pointer-events: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def get_image_base64(path):
    import base64
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def show_hospital_ui():
    # 1. Apply the background watermark
    apply_custom_styling()

    # 2. Add the TN Government Logo at the top center
    if os.path.exists(LOGO_PATH):
        col1, col2, col3 = st.columns([4, 1, 4])
        with col2:
            st.image(LOGO_PATH, width=120)

# ====================================
# GLOBAL QUEUE & FILE PATHS
# ====================================
if 'shared_queue' not in globals():
    globals()['shared_queue'] = queue.Queue()
shared_queue = globals()['shared_queue']

LOG_FILE = "../backend/data/hospital_audit_log.xlsx"
# Unified file path used by both the dashboard and the feedback component
FEEDBACK_FILE = "../backend/data/patient_rewards.xlsx" 

# ====================================
# CORE FUNCTIONS
# ====================================

def auto_save_to_excel(result):
    new_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Ambulance_ID": result.get("ambulance_id"),
        "Risk_Priority": result["triage"].get("priority"),
        "Admission_Level": result["admission"].get("suggested_admission_level"),
        "Bed_Assigned": result["resource"].get("bed"),
        "Teams_Notified": ", ".join(result["resource"].get("teams", [])),
        "Clinical_Note": result["admission"].get("note")
    }
    
    df_new = pd.DataFrame([new_data])
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    if not os.path.isfile(LOG_FILE):
        df_new.to_excel(LOG_FILE, index=False, engine='openpyxl')
    else:
        try:
            with pd.ExcelWriter(LOG_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                existing_df = pd.read_excel(LOG_FILE)
                updated_df = pd.concat([existing_df, df_new], ignore_index=True)
                updated_df.to_excel(writer, index=False)
        except Exception as e:
            st.error(f"Excel Error: {e}")

def on_message(ws, message):
    try:
        result = json.loads(message)
        shared_queue.put(result)
    except Exception as e:
        print(f"Error parsing message: {e}")

def listen_hospital():
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/api/ws/hospital", on_message=on_message)
    ws.run_forever()

# ====================================
# MAIN UI FUNCTION (Called by app.py)
# ====================================

def show_hospital_ui():
    # Load CSS
    if os.path.exists("assets/css/alerts.css"):
        with open("assets/css/alerts.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Start WebSocket thread if not running
    if "listener_started" not in st.session_state:
        thread = threading.Thread(target=listen_hospital, daemon=True)
        thread.start()
        st.session_state.listener_started = True

    # NAVIGATION SIDEBAR
    with st.sidebar:
        st.title("📂 Navigation")
        page_selection = st.radio("Select View:", ["Live Feed", "Patient Feedback", "View Feedback"])
        
        st.divider()
        if os.path.exists(LOG_FILE):
            st.write("### 📂 Export Records")
            with open(LOG_FILE, "rb") as f:
                st.download_button("Download Hospital Log", f, file_name="hospital_log.xlsx")

    # UI DISPLAY LOGIC
    if page_selection == "Patient Feedback":
        st.title("🌟 Patient Experience & Rewards")
        display_patient_info({"Status": "Active Intake"})

    elif page_selection == "View Feedback":
        st.title("📋 Patient Feedback Logs")
        if os.path.exists(FEEDBACK_FILE):
            df_feedback = pd.read_excel(FEEDBACK_FILE)
            
            # Display metrics summary
            st.subheader("📊 Feedback Analytics")
            c1, c2 = st.columns(2)
            c1.metric("Total Submissions", len(df_feedback))
            if "Rating" in df_feedback.columns:
                c2.metric("Avg satisfaction", f"{df_feedback['Rating'].mean():.1f} / 5")

            # Table display
            st.dataframe(
                df_feedback.sort_values(by="Timestamp", ascending=False), 
                use_container_width=True,
                hide_index=True
            )
            
            # Download Feedback separately
            with open(FEEDBACK_FILE, "rb") as f:
                st.download_button("Download Feedback Log", f, file_name="patient_feedback.xlsx")
        else:
            st.info("No feedback records found. Submit feedback in the 'Patient Feedback' section first.")

    else:
        st.title("🏥 Hospital Command Center – Live Feed")
        placeholder = st.empty()

        while True:
            # Breaks the loop if user changes navigation
            if page_selection != "Live Feed":
                break

            if not shared_queue.empty():
                result = shared_queue.get()
                auto_save_to_excel(result)

                with placeholder.container():
                    st.subheader(f"🚑 Incoming Ambulance: {result['ambulance_id']}")
                    triage = result["triage"]
                    priority = triage["priority"].upper()
                    
                    alert_class = "blink-red" if priority in ["CRITICAL", "HIGH"] else \
                                  "blink-yellow" if priority == "MEDIUM" else "blink-green"

                    st.markdown(f'<div class="alert-box {alert_class}">🚨 {priority} RISK <br><br>{triage["message"]}</div>', unsafe_allow_html=True)
                    components.html('<audio autoplay hidden><source src="assets/sounds/notification.mp3" type="audio/mpeg"></audio>', height=0)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 🏥 Admission Plan")
                        st.metric("Suggested Level", result["admission"]["suggested_admission_level"])
                        st.info(result["admission"]["note"])

                    with col2:
                        st.markdown("### 🧰 Resource Preparation")
                        st.write(f"**Bed Type:** `{result['resource']['bed']}`")
                        st.write(f"**Teams:** {', '.join(result['resource']['teams'])}")
                        st.toast(f"Logged {result['ambulance_id']} to Excel", icon="💾")

            time.sleep(1)

if __name__ == "__main__":
    if "logged_in" not in st.session_state or st.session_state.get("auth_role") != "Hospital Command Center":
        st.set_page_config(page_title="Access Denied", layout="centered")
        st.warning("⚠️ Access Denied. Hospital Staff-aaga login seiyungal.")
        st.stop()
    else:
        st.set_page_config(page_title="Hospital Command Center", layout="wide")
        show_hospital_ui()