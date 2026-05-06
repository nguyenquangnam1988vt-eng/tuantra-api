from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json

from api.models import EncryptedRequest
from api.crypto import decrypt_message
from api.deps import verify_token

router = APIRouter(prefix="/api/markers", tags=["markers"])

@router.post("/")
async def create_marker(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]

    try:
        data = json.loads(decrypt_message(enc.data))
    except:
        raise HTTPException(400, "Invalid encrypted data")

    db.reference(f"markers/{uid}").push({
        "lat": data["lat"],
        "lng": data["lng"],
        "timestamp": int(time.time() * 1000)
    })

    return {"success": True}
