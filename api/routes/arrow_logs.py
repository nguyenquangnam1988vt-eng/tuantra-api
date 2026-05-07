from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json

from api.models import EncryptedRequest
from api.crypto import decrypt_message
from api.deps import verify_token

router = APIRouter(prefix="/api/arrow-logs", tags=["arrow-logs"])

@router.post("/")
async def create_arrow_log(enc: EncryptedRequest, user=Depends(verify_token)):
    data = json.loads(decrypt_message(enc.data))
    db.reference("arrow_logs").push({
        "action": data["action"],
        "drawingId": data.get("drawingId"),
        "drawingAuthor": data.get("drawingAuthor"),
        "performedBy": data.get("performedBy", user["uid"]),
        "performedByName": data.get("performedByName"),
        "timestamp": data.get("timestamp", int(time.time() * 1000))
    })
    return {"success": True}
