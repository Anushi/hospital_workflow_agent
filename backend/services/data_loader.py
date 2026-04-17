import pandas as pd
from pathlib import Path
import os

# Updated to look at both 'processed' and the main 'data' folder
BASE_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROCESSED_DIR = BASE_DATA_DIR / "processed"

class DataLoader:
    def __init__(self):
        # Static Cleaned Data
        self.clinical = None
        self.admission = None
        self.vitals = None
        # Live System Data
        self.live_audit_log = None
        self.patient_rewards = None

    def _read_csv(self, fname):
        p = PROCESSED_DIR / fname
        if not p.exists():
            return None # Fail silently or log for static files
        return pd.read_csv(p)

    def _read_excel(self, fname):
        # Reads from the main data folder where your frontend saves
        p = BASE_DATA_DIR / fname
        if not p.exists():
            return pd.DataFrame() # Return empty DF if no data yet
        return pd.read_excel(p, engine='openpyxl')

    def load_all(self):
        """Loads historical static datasets."""
        self.clinical = self._read_csv("clinical_profile_cleaned.csv")
        self.admission = self._read_csv("final_admission_dataset.csv")
        self.vitals = self._read_csv("vitals_cleaned.csv")
        return {
            "status": "historical_data_loaded",
            "clinical_records": len(self.clinical) if self.clinical is not None else 0
        }

    def get_live_updates(self):
        """
        Fetches the latest real-time data saved by the frontend.
        Call this whenever an Agent needs to see recent history.
        """
        #
        self.live_audit_log = self._read_excel("hospital_audit_log.xlsx")
        self.patient_rewards = self._read_excel("patient_rewards.xlsx")
        
        return {
            "last_ambulance_intake": self.live_audit_log.tail(1).to_dict('records') if not self.live_audit_log.empty else None,
            "total_rewards_given": len(self.patient_rewards)
        }

# expose a singleton loader
loader = DataLoader()