# backend/services/agent_manager.py
from agents.triage_agent import triage_agent
from agents.admission_agent import admission_agent
from agents.resource_agent import resource_agent
from agents.monitoring_agent import monitoring_agent

class AgentManager:
    def __init__(self, loader):
        self.loader = loader

    def run_triage(self, patient_id: int, use_vitals=True):
        clinical_df = self.loader.clinical
        vitals_df = self.loader.vitals
        patient = clinical_df[clinical_df['patien_id'] == patient_id]
        if patient.empty:
            return {"error": "patient not found"}
        patient_row = patient.iloc[0].to_dict()

        vitals_row = None
        if use_vitals and 'patien_id' in vitals_df.columns:
            v = vitals_df[vitals_df['patien_id'] == patient_id]
            if not v.empty:
                vitals_row = v.iloc[-1].to_dict()  # take last vitals

        triage_res = triage_agent(patient_row, vitals_row)
        return triage_res

    def run_admission(self, patient_id: int, use_vitals=True):
        clinical_df = self.loader.clinical
        vitals_df = self.loader.vitals
        patient = clinical_df[clinical_df['patien_id'] == patient_id]
        if patient.empty:
            return {"error": "patient not found"}
        patient_row = patient.iloc[0].to_dict()
        vitals_row = None
        if use_vitals and 'patien_id' in vitals_df.columns:
            v = vitals_df[vitals_df['patien_id'] == patient_id]
            if not v.empty:
                vitals_row = v.iloc[-1].to_dict()
        admission_res = admission_agent(patient_row, vitals_row)
        return admission_res

    def run_resource_allocation(self, triage_res, admission_res):
        return resource_agent(triage_res, admission_res)

    def run_monitoring(self, patient_id: int):
        vitals_df = self.loader.vitals
        if 'patien_id' in vitals_df.columns:
            v = vitals_df[vitals_df['patien_id'] == patient_id]
            if v.empty:
                return {"error": "vitals not found for patient"}
            vitals_row = v.iloc[-1].to_dict()
        else:
            return {"error": "vitals dataset missing patien_id column"}
        return monitoring_agent(vitals_row)
