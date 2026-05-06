# api/routes/officers.py
from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json
from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token
from api.firebase import init_firebase

router = APIRouter(prefix="/api/officers", tags=["officers"])

@router.post("/update")
async def update_officer(enc_req: EncryptedRequest, user=Depends(verify_token)):
    init_firebase()
    uid = user["uid"]
    try:
        payload = decrypt(enc_req.data)
        lat = payload.get("lat")
        lng = payload.get("lng")
        name = payload.get("name")
        lastUpdate = payload.get("lastUpdate", int(time.time() * 1000))
        # Lưu vào Firebase
        db.reference(f"officers/{uid}").set({
            "lat": lat,
            "lng": lng,
            "name": name,
            "lastUpdate": lastUpdate
        })
        return {"success": True}
    except Exception as e:
        raise HTTPException(400, f"Decrypt error: {e}")
