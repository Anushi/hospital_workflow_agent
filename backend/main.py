from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import router
import uvicorn
import os

app = FastAPI(
    title="Hospital Multi-Agent System",
    description="Professional Healthcare Command Center Backend",
)

# 1. AUTHENTICATION SETUP
USER_DB = {"admin": "123"} # Neenga app.py-la kudutha 123 password-kku match panniyiruken
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_password = USER_DB.get(form_data.username)
    if not user_password or form_data.password != user_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": form_data.username, "token_type": "bearer"}

# 2. INCLUDE ROUTES (Triage, Admission, etc.)
app.include_router(router, prefix="/api")

# 3. SERVE FRONTEND (Corrected Path)
# Unga folder structure-padi path-ai 'frontend' nu maathiyiruken
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "../frontend")

# Path irukkiraadha nu check panni mount pannum logic
if os.path.exists(FRONTEND_PATH):
    app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")
else:
    print(f"⚠️ Warning: FRONTEND_PATH not found at {FRONTEND_PATH}")

@app.get("/")
async def serve_login():
    """Serves the login page by default"""
    return FileResponse(os.path.join(FRONTEND_PATH, "app.py")) # Streamlit app use pannuvathal

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)