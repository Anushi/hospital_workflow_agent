# backend/services/data_loader.py
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

class DataLoader:
    def __init__(self):
        self.clinical = None
        self.admission = None
        self.stay = None
        self.lab = None
        self.experience = None
        self.vitals = None

    def _read(self, fname):
        p = DATA_DIR / fname
        if not p.exists():
            raise FileNotFoundError(f"{p} not found. Put CSV into backend/data/processed/")
        return pd.read_csv(p)

    def load_all(self):
        self.clinical = self._read("clinical_profile_cleaned.csv")
        self.admission = self._read("final_admission_dataset.csv")
        self.stay = self._read("hospital_stay_cleaned.csv")
        self.lab = self._read("lab_results_cleaned.csv")
        self.experience = self._read("patient_experience_cleaned.csv")
        self.vitals = self._read("vitals_cleaned.csv")
        return {
            "clinical_shape": self.clinical.shape,
            "vitals_shape": self.vitals.shape
        }

# expose a singleton loader
loader = DataLoader()
