# backend/agents/admission_agent.py
"""
Admission Agent: classifies admission type based on measurable params.
This is conservative and uses only objective fields.
"""

def admission_agent(patient: dict, vitals: dict = None) -> dict:
    score = 0

    age = safe_float(patient.get("age", 0))
    if age >= 75:
        score += 1

    if vitals:
        spo2 = safe_float(vitals.get("spo2"))
        sbp = safe_float(vitals.get("sbp"))

        if spo2 is not None and spo2 < 92:
            score += 3
        if sbp is not None and sbp < 90:
            score += 3

    for k in ("dm", "htn", "heart_failure"):
        if str(patient.get(k, "0")) == "1":
            score += 1

    if score >= 6:
        level = "Emergency"
    elif score >= 3:
        level = "Urgent"
    else:
        level = "Routine"

    return {
        "suggested_admission_level": level,
        "note": "Workflow suggestion only — final decision requires clinical confirmation."
    }
def safe_float(x):
    try:
        return float(x)
    except Exception:
        return None
