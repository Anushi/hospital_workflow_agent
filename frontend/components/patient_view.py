import streamlit as st
<<<<<<< HEAD
import pandas as pd
import os
import time
from datetime import datetime

# Centralized path to the backend data folder
REWARDS_FILE = "../backend/data/patient_rewards.xlsx"

def display_patient_info(patient_data):
    st.markdown("---")
    st.title("🌟 Staff Recognition & Feedback Analyzer")

    # ====================================
    # REAL-TIME ANALYZER SECTION
    # ====================================
    if os.path.exists(REWARDS_FILE):
        df = pd.read_excel(REWARDS_FILE)
        if not df.empty:
            st.subheader("📊 Real-Time Service Metrics")
            m1, m2, m3 = st.columns(3)
            
            with m1:
                avg_rating = df["Rating"].mean()
                st.metric("Avg Satisfaction", f"{avg_rating:.1f} / 5")
            with m2:
                total_nominations = len(df)
                st.metric("Total Rewards Given", total_nominations)
            with m3:
                top_cat = df["Category"].mode()[0]
                st.metric("Top Award Category", top_cat)

            # Bar Chart for Rewards by Category
            st.write("**Nominations by Category**")
            chart_data = df["Category"].value_counts()
            st.bar_chart(chart_data)
    else:
        st.info("No rewards data found yet. Metrics will appear after the first submission.")

    st.divider()

    # ====================================
    # THE FEEDBACK FORM
    # ====================================
    st.subheader("✍️ Submit New Feedback")
    
    # Display care summary
    with st.expander("View My Care Summary", expanded=False):
        for k, v in patient_data.items():
            st.write(f"**{k.replace('_', ' ').title()}**: {v}")

    with st.container():
        st.info("Nominate a staff member for a reward based on your care today.")
        
        rating = st.feedback("stars")
        nomination = st.text_input("Nominate a specific team or staff member:")
        reward_cat = st.selectbox(
            "Select Reward Category:",
            ["Compassionate Care", "High-Tech Efficiency", "Rapid Triage", "Life-Saver Award"]
        )
        comments = st.text_area("Additional comments:")

        if st.button("🚀 Submit & Refresh Analyzer"):
            if rating is not None:
                feedback_entry = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Rating": rating + 1,
                    "Nominee": nomination,
                    "Category": reward_cat,
                    "Comments": comments
                }
                
                save_feedback_to_backend(feedback_entry)
                st.balloons()
                st.success("Feedback saved! The analyzer above has been updated.")
                time.sleep(1) # Brief pause for user to see success
                st.rerun()    # Refresh to update the charts immediately
            else:
                st.warning("Please provide a star rating.")

def save_feedback_to_backend(data):
    os.makedirs(os.path.dirname(REWARDS_FILE), exist_ok=True)
    df = pd.DataFrame([data])
    
    if not os.path.exists(REWARDS_FILE):
        df.to_excel(REWARDS_FILE, index=False, engine='openpyxl')
    else:
        existing_df = pd.read_excel(REWARDS_FILE)
        pd.concat([existing_df, df], ignore_index=True).to_excel(REWARDS_FILE, index=False)
=======

def display_patient_info(patient_data):
    st.subheader("Patient Information")
    for k, v in patient_data.items():
        st.write(f"{k}: {v}")
>>>>>>> 0ba03eb97bf983192968a5a9d7e2672d39c2ba99
