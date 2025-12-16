# backend/agents/resource_agent.py
"""
Resource Allocation Agent: simple bed / ICU / team recommendation
based on triage/admission outputs. Returns suggested actions only.
"""

def resource_agent(triage_result: dict, admission_result: dict) -> dict:
    # default suggested resources
    suggested = {
        "bed_type": "General ward",
        "priority": triage_result.get("priority", "Low"),
        "notify_team": [],
        "preparation_notes": []
    }

    priority = triage_result.get("priority", "").lower()
    admission = admission_result.get("recommended_admission", "").lower()

    # mapping rules
    if priority == "high" or admission == "emergency":
        suggested["bed_type"] = "ICU/High dependency"
        suggested["notify_team"] = ["Emergency Team", "Critical Care"]
        suggested["preparation_notes"].append("Prepare resuscitation equipment and ICU bed.")
    elif priority == "medium" or admission == "urgent":
        suggested["bed_type"] = "High dependency / Step down"
        suggested["notify_team"] = ["Admission Nurse", "On-call Physician"]
        suggested["preparation_notes"].append("Prepare monitoring bed and IV access.")
    else:
        suggested["bed_type"] = "General ward"
        suggested["notify_team"] = ["Ward Nurse"]
        suggested["preparation_notes"].append("Standard admission prep.")

    return {
        "agent": "resource_agent",
        "suggested": suggested,
        "note": "These are suggested preparations. Final allocation requires human confirmation."
    }
