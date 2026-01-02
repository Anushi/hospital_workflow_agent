# backend/api/routes.py
from fastapi import APIRouter, HTTPException
from services.data_loader import loader
from services.agent_manager import AgentManager
from pydantic import BaseModel
from typing import Optional
from agents.triage_agent import triage_agent
from agents.admission_agent import admission_agent
from agents.resource_agent import resource_agent
from services.ws_manager import connected_hospitals
from fastapi import WebSocket
from fastapi import WebSocket, APIRouter
from services.ws_manager import register_hospital, unregister_hospital
from services.ws_manager import broadcast_to_hospitals

import json

router = APIRouter()
agent_manager = AgentManager(loader)

@router.get("/load-data")
def load_data():
    try:
        info = loader.load_all()
        return {"status": "ok", "info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/triage/{patient_id}")
def triage(patient_id: int, use_vitals: Optional[bool] = True):
    res = agent_manager.run_triage(patient_id, use_vitals=use_vitals)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@router.get("/admission/{patient_id}")
def admission(patient_id: int, use_vitals: Optional[bool] = True):
    res = agent_manager.run_admission(patient_id, use_vitals=use_vitals)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@router.get("/resource/{patient_id}")
def resource(patient_id: int):
    triage_res = agent_manager.run_triage(patient_id)
    if "error" in triage_res: raise HTTPException(status_code=404, detail=triage_res["error"])
    admission_res = agent_manager.run_admission(patient_id)
    if "error" in admission_res: raise HTTPException(status_code=404, detail=admission_res["error"])
    res = agent_manager.run_resource_allocation(triage_res, admission_res)
    return res

@router.get("/monitor/{patient_id}")
def monitor(patient_id: int):
    res = agent_manager.run_monitoring(patient_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

# quick vitals POST API for testing dynamic inputs
class VitalsIn(BaseModel):
    hr: Optional[float] = None
    sbp: Optional[float] = None
    rr: Optional[float] = None
    spo2: Optional[float] = None
    temp: Optional[float] = None

@router.post("/triage-live/{patient_id}")
def triage_live(patient_id: int, vitals: VitalsIn):
    # create minimal patient lookup (no vitals stored) and run triage with provided vitals
    clinical_df = loader.clinical
    if clinical_df is None:
        raise HTTPException(status_code=400, detail="Data not loaded. Call /api/load-data first.")
    patient = clinical_df[clinical_df['patien_id'] == patient_id]
    if patient.empty:
        raise HTTPException(status_code=404, detail="patient not found")
    patient_row = patient.iloc[0].to_dict()
    vitals_row = vitals.dict()
    from agents.triage_agent import triage_agent as triage_fn
    res = triage_fn(patient_row, vitals_row)
    return res

@router.post("/ambulance/send")
async def receive_ambulance_data(payload: dict):
    # ✅ payload exists ONLY here
    print("🚑 Ambulance data received:", payload)

    # sample response
    return {
        "triage": {
            "priority": "HIGH",
            "message": "Patient needs immediate attention"
        },
        "admission": {
            "suggested_admission_level": "ICU",
            "note": "Prepare ICU bed"
        },
        "resource": {
            "bed": "ICU-2",
            "teams": ["Cardiology", "Emergency"],
            "note": "Teams alerted"
        },
        "disclaimer": "For clinical support only"
    }


@router.post("/ambulance/intake")
async def ambulance_intake(payload: dict):
    print("🚑 AUTOMATIC AMBULANCE DATA RECEIVED")
    print(payload)

    ambulance_id = payload.get("ambulance_id", "UNKNOWN")
    patient = payload.get("patient", {})
    vitals = payload.get("vitals", {})

    triage = triage_agent(patient, vitals)
    admission = admission_agent(triage)
    resource = resource_agent(triage)

    result = {
        "ambulance_id": ambulance_id,
        "triage": triage,
        "admission": admission,
        "resource": resource
    }

    if connected_hospitals:
        for ws in connected_hospitals:
            await ws.send_text(json.dumps(result))
            print(f"🏥 Hospital notified for {ambulance_id}")
    else:
        print("⚠️ No hospital dashboard connected")

    return {
        **result,
        "disclaimer": "AI-assisted workflow support only."
    }

@router.websocket("/ws/hospital")
async def hospital_ws(websocket: WebSocket):
    await websocket.accept()
    await register_hospital(websocket)

    try:
        while True:
            await websocket.receive_text()
    except:
        await unregister_hospital(websocket)