from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import json
import time
from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token
from api.firebase import init_firebase

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/update")
async def update_user(enc_req: EncryptedRequest, user=Depends(verify_token)):
    init_firebase()
    uid = user["uid"]
    try:
        payload = decrypt(enc_req.data)
        db.reference(f"users/{uid}").set({
            "name": payload["name"],
            "role": payload["role"],
            "color": payload["color"],
            "last_seen": payload.get("last_seen", int(time.time() * 1000))
        })
        return {"success": True}
    except Exception as e:
        raise HTTPException(400, f"Lỗi giải mã: {e}")
