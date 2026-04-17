import streamlit as st
import websocket
import json
import threading
import queue
import time

# ====================================
# Queue to receive messages from thread
# ====================================
message_queue = queue.Queue()

st.set_page_config(layout="wide")
st.title("🏥 Hospital Command Center – Live Ambulance Feed")

placeholder = st.empty()


# ====================================
# WebSocket message handler
# ====================================
def on_message(ws, message):
    try:
        result = json.loads(message)
        message_queue.put(result)
    except Exception as e:
        print("Error parsing message:", e)


# ====================================
# Background WebSocket listener thread
# ====================================
def listen_hospital():
    ws = websocket.WebSocketApp(
        "ws://127.0.0.1:8000/api/ws/hospital",
        on_message=on_message
    )
    ws.run_forever()        # keeps listening


# ====================================
# Start listener only once
# ====================================
if "listener_started" not in st.session_state:
    threading.Thread(target=listen_hospital, daemon=True).start()
    st.session_state.listener_started = True
    st.success("WebSocket listener started")


# ====================================
# UI Poll Loop
# Continuously check queue and update UI
# ====================================
while True:

    if not message_queue.empty():

        result = message_queue.get()

        with placeholder.container():

            st.subheader(f"🚑 Incoming Ambulance: {result['ambulance_id']}")

            # TRIAGE
            triage = result["triage"]
            priority = triage["priority"].upper()

            if priority in ["CRITICAL", "HIGH"]:
                st.error(f"🚨 {priority} RISK")
            else:
                st.success(f"🟢 {priority} RISK")

            st.write(triage["message"])


            # ADMISSION
            st.markdown("### 🏥 Admission Plan")
            st.write(result["admission"]["suggested_admission_level"])
            st.caption(result["admission"]["note"])


            # RESOURCE
            st.markdown("### 🧰 Resource Preparation")
            st.write(f"Bed Type: {result['resource']['bed']}")
            st.write("Teams: " + ", ".join(result["resource"]["teams"]))

    time.sleep(1)

st.info("🟢 Waiting for live ambulance data...")
