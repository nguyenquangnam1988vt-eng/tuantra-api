# api/index.py
import os
import json
from fastapi import FastAPI, Header, HTTPException, Depends
from firebase_admin import credentials, auth, db
import firebase_admin
from pydantic import BaseModel

# --- Khởi tạo Firebase ---
if not firebase_admin._apps:
    cred_json = os.getenv("FIREBASE_CRED_JSON")
    if not cred_json:
        raise Exception("Missing FIREBASE_CRED_JSON environment variable")
    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
    })

app = FastAPI()

# --- Models ---
class AlertModel(BaseModel):
    lat: float
    lng: float
    name: str

class MarkerModel(BaseModel):
    lat: float
    lng: float

class IncidentModel(BaseModel):
    lat: float
    lng: float
    image_url: str

# --- Xác thực ---
async def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing token")
    try:
        token = authorization.split(" ")[1]
        decoded = auth.verify_id_token(token)
        return decoded
    except:
        raise HTTPException(401, "Invalid token")

# --- Routes ---
@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/alerts")
async def create_alert(alert: AlertModel, user=Depends(verify_token)):
    data = alert.dict()
    data["created_by"] = user["uid"]
    data["timestamp"] = {"sv": "timestamp"}
    ref = db.reference("alerts").push(data)
    return {"success": True, "id": ref.key}

@app.post("/api/markers")
async def create_marker(marker: MarkerModel, user=Depends(verify_token)):
    data = marker.dict()
    data["created_by"] = user["uid"]
    data["timestamp"] = {"sv": "timestamp"}
    ref = db.reference(f"markers/{user['uid']}").push(data)
    return {"success": True, "id": ref.key}

@app.post("/api/incidents")
async def create_incident(incident: IncidentModel, user=Depends(verify_token)):
    data = incident.dict()
    data["created_by"] = user["uid"]
    data["timestamp"] = {"sv": "timestamp"}
    ref = db.reference("incidents").push(data)
    return {"success": True, "id": ref.key}
