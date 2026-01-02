# backend/agents/resource_agent.py
"""
Resource Allocation Agent: simple bed / ICU / team recommendation
based on triage/admission outputs. Returns suggested actions only.
"""
from services.resource_status import allocate_icu

def resource_agent(triage):
    icu, remaining = allocate_icu(triage["priority"])

    if icu:
        return {
            "bed": "ICU",
            "teams": ["Emergency Physician", "ICU Nurse"],
            "note": f"ICU allocated. Remaining ICU beds: {remaining}"
        }

    return {
        "bed": "General Ward",
        "teams": ["General Physician"],
        "note": "ICU not available or not required"
    }
