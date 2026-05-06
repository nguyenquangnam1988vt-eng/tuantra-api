from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json

from api.models import EncryptedRequest
from api.crypto import decrypt_message
from api.deps import verify_token

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/update")
async def update_user(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]

    try:
        data = json.loads(decrypt_message(enc.data))
    except:
        raise HTTPException(400, "Invalid encrypted data")

    db.reference(f"users/{uid}").set({
        "name": data["name"],
        "role": data["role"],
        "color": data["color"],
        "last_seen": data.get("last_seen", int(time.time() * 1000))
    })

    return {"success": True}
