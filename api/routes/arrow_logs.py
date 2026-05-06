from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import json
from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token
from api.firebase import init_firebase

router = APIRouter(prefix="/api/arrow-logs", tags=["arrow-logs"])

@router.post("/")
async def log_arrow(enc_req: EncryptedRequest, user=Depends(verify_token)):
    init_firebase()
    try:
        payload = decrypt(enc_req.data)
        db.reference("arrow_logs").push({
            "from_uid": payload["from_uid"],
            "to_uid": payload["to_uid"],
            "coordinates": payload["coordinates"],
            "timestamp": payload["timestamp"]
        })
        return {"success": True}
    except Exception as e:
        raise HTTPException(400, f"Lỗi: {e}")
