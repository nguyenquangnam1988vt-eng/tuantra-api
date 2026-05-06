from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token

router = APIRouter(prefix="/api/drawings", tags=["drawings"])

@router.post("/")
async def create_drawing(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    try:
        data = decrypt(enc.data)
    except Exception:
        raise HTTPException(400, "Invalid encrypted data")

    # Lưu vào Firebase
    new_ref = db.reference("drawings").push({
        "points": data.get("points"),
        "color": data.get("color"),
        "weight": data.get("weight"),
        "author": data.get("author"),
        "authorId": uid,
        "timestamp": int(time.time() * 1000),
        "type": data.get("type", "normal")
    })
    return {"success": True, "id": new_ref.key}
