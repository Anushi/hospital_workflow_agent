# backend/main.py
from fastapi import FastAPI, WebSocket
from api.routes import router
import uvicorn

app = FastAPI(
    title="Hospital Multi-Agent System",
    description="Rule-based multi-agent backend for triage, admission and resource allocation",
)

app.include_router(router, prefix="/api")


@app.get("/")
def read_root():
    return {"status": "Backend running. See /api/docs for API docs"}
    
if __name__ == "__main__":
    # only used when running `python main.py`
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
