import streamlit as st

def display_patient_info(patient_data):
    st.subheader("Patient Information")
    for k, v in patient_data.items():
        st.write(f"{k}: {v}")
