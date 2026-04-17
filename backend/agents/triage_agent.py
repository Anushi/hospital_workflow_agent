# backend/agents/triage_agent.py
"""
Simple rule-based triage agent.
It enforces safety rules: no diagnoses, only "potential risk detected" phrasing.
"""

def safe_float(x):
    try:
        return float(x)
    except:
        return None


def triage_agent(patient: dict, vitals: dict = None) -> dict:
    score = 0
    alerts = []

    age = safe_float(patient.get("age", 0))
    if age >= 75:
        score += 2
    elif age >= 60:
        score += 1

    # known medical history indicators (non-diagnostic)
    for k in ("dm", "htn", "heart_failure"):
        if str(patient.get(k, "0")) == "1":
            score += 1

    if vitals:
        hr = safe_float(vitals.get("hr"))
        sbp = safe_float(vitals.get("sbp"))
        rr = safe_float(vitals.get("rr"))
        spo2 = safe_float(vitals.get("spo2"))
        avpu = vitals.get("avpu")

        # unconscious safety rule
        if avpu in (0, 1):
            return {
                "priority": "High",
                "message": "Reduced consciousness detected — immediate clinical evaluation required."
            }

        if spo2 is not None and spo2 < 92:
            score += 3
        if sbp is not None and sbp < 90:
            score += 3
        if rr is not None and rr > 30:
            score += 2
        if hr is not None and hr > 130:
            score += 2

    if score >= 6:
        priority = "High"
        msg = "Potential high risk detected — clinical evaluation required."
    elif score >= 3:
        priority = "Medium"
        msg = "Potential moderate risk detected — clinical evaluation required."
    else:
        priority = "Low"
        msg = "No immediate abnormality detected; continue monitoring."

    return {
        "priority": priority,
        "message": msg
    }
