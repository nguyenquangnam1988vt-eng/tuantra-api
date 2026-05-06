from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import json
from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token
from api.firebase import init_firebase

router = APIRouter(prefix="/api/tracks", tags=["tracks"])

@router.post("/")
async def save_track(enc_req: EncryptedRequest, user=Depends(verify_token)):
    init_firebase()
    try:
        payload = decrypt(enc_req.data)
        uid = payload["uid"]
        db.reference(f"tracks/{uid}").push({
            "lat": payload["lat"],
            "lng": payload["lng"],
            "timestamp": payload["timestamp"]
        })
        return {"success": True}
    except Exception as e:
        raise HTTPException(400, f"Lỗi: {e}")
