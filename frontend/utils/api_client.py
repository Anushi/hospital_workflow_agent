import requests

API_URL = "http://127.0.0.1:8000"

def get_triage(patient_id):
    return requests.get(f"{API_URL}/triage/{patient_id}").json()

def get_admission(patient_id):
    return requests.get(f"{API_URL}/admission/{patient_id}").json()

def get_monitor(patient_id):
    return requests.get(f"{API_URL}/monitor/{patient_id}").json()
