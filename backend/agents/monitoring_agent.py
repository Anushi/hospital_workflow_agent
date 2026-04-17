# backend/agents/monitoring_agent.py
"""
Monitoring Agent: checks vital trends and flags deterioration.
As this skeleton is stateless, it performs single-sample checks.
"""

def monitoring_agent(vitals_row: dict) -> dict:
    alerts = []
    hr = safe_float(vitals_row.get("hr", None))
    sbp = safe_float(vitals_row.get("sbp", None))
    rr = safe_float(vitals_row.get("rr", None))
    spo2 = safe_float(vitals_row.get("spo2", None))

    if spo2 is not None and spo2 < 92:
        alerts.append("Potential respiratory compromise detected — clinical evaluation required.")
    if sbp is not None and sbp < 90:
        alerts.append("Potential hypotension detected — clinical evaluation required.")
    if hr is not None and hr > 130:
        alerts.append("Tachycardia detected — clinical evaluation required.")
    if rr is not None and rr > 30:
        alerts.append("Tachypnea detected — clinical evaluation required.")

    if not alerts:
        alerts = ["No immediate abnormality detected; continue monitoring."]

    return {
        "agent": "monitoring_agent",
        "vitals": vitals_row,
        "alerts": alerts
    }

def safe_float(x):
    try:
        return float(x)
    except Exception:
        return None
