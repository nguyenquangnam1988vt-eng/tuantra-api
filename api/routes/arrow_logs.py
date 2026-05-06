from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json

from api.models import EncryptedRequest
from api.crypto import decrypt_message
from api.deps import verify_token

router = APIRouter(prefix="/api/arrow-logs", tags=["arrow-logs"])

@router.post("/")
async def log_arrow(enc: EncryptedRequest, user=Depends(verify_token)):
    try:
        data = json.loads(decrypt_message(enc.data))
    except:
        raise HTTPException(400, "Invalid encrypted data")

    db.reference("arrow_logs").push({
        "from_uid": data["from_uid"],
        "to_uid": data["to_uid"],
        "coordinates": data["coordinates"],
        "timestamp": data.get("timestamp", int(time.time() * 1000))
    })

    return {"success": True}
