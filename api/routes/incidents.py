from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json

from api.models import EncryptedRequest
from api.crypto import decrypt_message
from api.deps import verify_token

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

@router.post("/")
async def create_incident(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]

    try:
        data = json.loads(decrypt_message(enc.data))
    except:
        raise HTTPException(400, "Invalid encrypted data")

    db.reference("incidents").push({
        "lat": data["lat"],
        "lng": data["lng"],
        "image_url": data["image_url"],
        "created_by": uid,
        "timestamp": int(time.time() * 1000)
    })

    return {"success": True}
