# backend/agents/triage_agent.py
"""
Simple rule-based triage agent.
It enforces safety rules: no diagnoses, only "potential risk detected" phrasing.
"""

def triage_agent(patient_row: dict, vitals_row: dict = None) -> dict:
    # patient_row: row from clinical_profile CSV as dict
    # vitals_row: optional vitals dict (hr, sbp, rr, spo2, temp)
    alerts = []
    score = 0

    # Basic risk from demographics / comorbidities
    age = safe_float(patient_row.get("age", 0))
    if age >= 75:
        score += 2
    elif age >= 60:
        score += 1

    # comorbidities (columns like dm, htn, cad expected as 0/1)
    for k in ("dm", "htn", "cad", "ckd", "heart_failure"):
        if str(patient_row.get(k, "")).strip() in ("1", "True", "true"):
            score += 1

    # vitals-based checks (if provided)
    if vitals_row:
        try:
            hr = safe_float(vitals_row.get("hr", None))
            sbp = safe_float(vitals_row.get("sbp", None))
            rr = safe_float(vitals_row.get("rr", None))
            spo2 = safe_float(vitals_row.get("spo2", None))
        except Exception:
            hr = sbp = rr = spo2 = None

        # Add points for abnormal vitals
        if spo2 is not None and spo2 < 92:
            score += 3
        elif spo2 is not None and spo2 < 95:
            score += 1

        if hr is not None and hr > 130:
            score += 2
        elif hr is not None and hr > 110:
            score += 1

        if rr is not None and rr > 30:
            score += 2
        elif rr is not None and rr > 24:
            score += 1

        if sbp is not None and sbp < 90:
            score += 3
        elif sbp is not None and sbp < 100:
            score += 1

    # derive priority label, but ALWAYS use "potential risk..." wording
    if score >= 6:
        priority = "High"
        alerts.append("Potential high risk detected — clinical evaluation required.")
    elif score >= 3:
        priority = "Medium"
        alerts.append("Potential moderate risk detected — clinical evaluation required.")
    else:
        priority = "Low"
        alerts.append("No immediate abnormality detected; continue monitoring and clinical assessment if needed.")

    return {
        "agent": "triage_agent",
        "patient_id": patient_row.get("patien_id", patient_row.get("patien_id", None)),
        "score": score,
        "priority": priority,
        "alerts": alerts,
        "vitals_used": vitals_row or {},
    }

def safe_float(x):
    try:
        return float(x)
    except Exception:
        return None
