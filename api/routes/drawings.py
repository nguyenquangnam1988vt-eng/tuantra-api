from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json

from api.models import EncryptedRequest
from api.crypto import decrypt_message
from api.deps import verify_token

router = APIRouter(prefix="/api/drawings", tags=["drawings"])

@router.post("/")
async def create_drawing(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    try:
        decrypt_message(enc.data)
    except Exception:
        raise HTTPException(400, "Invalid encrypted data")

    db.reference("drawings").push({
        "points": data["points"],
        "color": data["color"],
        "weight": data["weight"],
        "author": data["author"],
        "authorId": uid,
        "timestamp": data.get("timestamp", int(time.time() * 1000)),
        "type": data["type"]
    })
    return {"success": True}
