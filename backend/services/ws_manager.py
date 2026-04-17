connected_hospitals = []     # GLOBAL shared list

async def register_hospital(websocket):
    connected_hospitals.append(websocket)
    print("🏥 Hospital dashboard connected")

async def unregister_hospital(websocket):
    if websocket in connected_hospitals:
        connected_hospitals.remove(websocket)
        print("❌ Hospital dashboard disconnected")

async def broadcast_to_hospitals(data):
    print("👥 Connected hospitals:", len(connected_hospitals))
    for ws in connected_hospitals:
        await ws.send_text(data)
        print("📡 Sent data to hospital")
