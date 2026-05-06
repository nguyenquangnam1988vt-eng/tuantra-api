from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time

from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token

router = APIRouter(prefix="/api/officers", tags=["officers"])

@router.post("/update")
async def update_officer(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    try:
        data = decrypt(enc.data)
    except Exception:
        raise HTTPException(400, "Invalid encrypted data")

    db.reference(f"officers/{uid}").set({
        "lat": data["lat"],
        "lng": data["lng"],
        "name": data["name"],
        "lastUpdate": data.get("lastUpdate", int(time.time() * 1000))
    })
    return {"success": True}
