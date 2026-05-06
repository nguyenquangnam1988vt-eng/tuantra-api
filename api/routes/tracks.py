from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json

from api.models import EncryptedRequest
from api.crypto import decrypt_message
from api.deps import verify_token

router = APIRouter(prefix="/api/tracks", tags=["tracks"])

@router.post("/")
async def save_track(enc: EncryptedRequest, user=Depends(verify_token)):
    try:
        data = json.loads(decrypt_message(enc.data))
    except:
        raise HTTPException(400, "Invalid encrypted data")

    uid = data.get("uid", user["uid"])
    db.reference(f"tracks/{uid}").push({
        "lat": data["lat"],
        "lng": data["lng"],
        "timestamp": data.get("timestamp", int(time.time() * 1000))
    })

    return {"success": True}
