import requests


API_URL = "http://127.0.0.1:8000/api/ambulance/intake"

def get_triage(patient_id):
    return requests.get(f"{API_URL}/triage/{patient_id}").json()

def get_admission(patient_id):
    return requests.get(f"{API_URL}/admission/{patient_id}").json()

def get_monitor(patient_id):
    return requests.get(f"{API_URL}/monitor/{patient_id}").json()

def get_resource(patient_id):
    return requests.get(f"{API_URL}/resource/{patient_id}").json()

def send_live_vitals(patient_id, payload):
    return requests.post(f"{API_URL}/triage-live/{patient_id}", json=payload).json()

def send_ambulance_data(payload):
    response = requests.post(API_URL, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()