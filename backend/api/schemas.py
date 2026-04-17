# backend/api/schemas.py
from pydantic import BaseModel
from typing import Optional

class Vitals(BaseModel):
    hr: Optional[float]
    sbp: Optional[float]
    rr: Optional[float]
    spo2: Optional[float]
    temp: Optional[float]
