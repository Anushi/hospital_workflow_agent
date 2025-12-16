# backend/agents/admission_agent.py
"""
Admission Agent: classifies admission type based on measurable params.
This is conservative and uses only objective fields.
"""

def admission_agent(patient_row: dict, vitals_row: dict = None) -> dict:
    # simple rule-based admission decision: Emergency / Urgent / Routine
    score = 0
    age = safe_float(patient_row.get("age", 0))
    if age >= 75:
        score += 1

    # vital triggers
    if vitals_row:
        spo2 = safe_float(vitals_row.get("spo2", None))
        sbp = safe_float(vitals_row.get("sbp", None))
        rr = safe_float(vitals_row.get("rr", None))
        hr = safe_float(vitals_row.get("hr", None))

        if spo2 is not None and spo2 < 92:
            score += 3
        if sbp is not None and sbp < 90:
            score += 3
        if rr is not None and rr > 30:
            score += 2
        if hr is not None and hr > 130:
            score += 2

    # chronic conditions
    for k in ("dm", "htn", "cad", "ckd", "heart_failure"):
        if str(patient_row.get(k, "")).strip() in ("1", "True", "true"):
            score += 1

    # map score to admission type
    if score >= 6:
        admission_type = "Emergency"
    elif score >= 3:
        admission_type = "Urgent"
    else:
        admission_type = "Routine"

    # safety note
    message = "This is a recommendation only: classify as '{}' — clinical confirmation required.".format(admission_type)

    return {
        "agent": "admission_agent",
        "patient_id": patient_row.get("patien_id"),
        "score": score,
        "recommended_admission": admission_type,
        "message": message
    }

def safe_float(x):
    try:
        return float(x)
    except Exception:
        return None
