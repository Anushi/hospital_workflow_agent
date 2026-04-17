import streamlit as st
import pandas as pd

def show_vitals_chart(hr, sbp, spo2, rr):
    df = pd.DataFrame({
        "Vitals": ["Heart Rate", "Systolic BP", "SpO2", "Resp Rate"],
        "Value": [hr, sbp, spo2, rr]
    })
    st.bar_chart(df.set_index("Vitals"))
