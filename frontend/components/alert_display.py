import streamlit as st
from utils.alert_mapper import map_priority

def show_alert(priority, message):
    css_class = map_priority(priority)

    st.markdown(
        f"""
        <div class="alert-box {css_class}">
            {priority} ALERT 🚨 <br><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )
