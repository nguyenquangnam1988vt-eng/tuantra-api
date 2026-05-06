from fastapi import FastAPI, Depends, HTTPException
from firebase_admin import db
import time

from api.models import AlertModel, MarkerModel, IncidentModel
from api.deps import verify_token, get_user_role
from api.firebase import init_firebase

app = FastAPI()

# ---------------- HEALTH ----------------
@app.get("/api/health")
async def health():
    return {"status": "ok"}

# ---------------- ALERT ----------------
@app.post("/api/alerts")
async def create_alert(data: AlertModel, user=Depends(verify_token)):
    init_firebase()

    uid = user["uid"]
    role = get_user_role(uid)

    if role not in ["officer", "commander", "admin"]:
        raise HTTPException(403, "No permission")

    db.reference("alerts").push({
        "lat": data.lat,
        "lng": data.lng,
        "name": data.name,
        "created_by": uid,
        "timestamp": int(time.time() * 1000)
    })

    return {"success": True}

# ---------------- MARKER ----------------
@app.post("/api/markers")
async def create_marker(data: MarkerModel, user=Depends(verify_token)):
    init_firebase()

    uid = user["uid"]

    db.reference(f"markers/{uid}").push({
        "lat": data.lat,
        "lng": data.lng,
        "timestamp": int(time.time() * 1000)
    })

    return {"success": True}

# ---------------- INCIDENT ----------------
@app.post("/api/incidents")
async def create_incident(data: IncidentModel, user=Depends(verify_token)):
    init_firebase()

    uid = user["uid"]

    db.reference("incidents").push({
        "lat": data.lat,
        "lng": data.lng,
        "image_url": data.image_url,
        "created_by": uid,
        "timestamp": int(time.time() * 1000)
    })

    return {"success": True}
