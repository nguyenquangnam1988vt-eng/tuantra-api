from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json

from api.models import EncryptedRequest
from api.crypto import decrypt_message
from api.deps import verify_token, get_user_role

router = APIRouter(prefix="/api/tactical-plans", tags=["tactical-plans"])


@router.post("/")
async def create_tactical_plan(
    enc: EncryptedRequest,
    user=Depends(verify_token),
    role=Depends(get_user_role)
):
    uid = user["uid"]

    if role not in ["commander", "admin"]:
        raise HTTPException(403, "Permission denied")

    try:
        data = json.loads(decrypt_message(enc.data))
    except:
        raise HTTPException(400, "Invalid encrypted data")

    plan_id = data["plan_id"]

    db.reference(f"tactical_plans/{plan_id}").set({
        "created_by": uid,
        "created_by_name": data.get("created_by_name", ""),
        "timestamp": int(time.time() * 1000),
        "is_active": data.get("is_active", True),
        "markers": data["markers"]
    })

    return {"success": True}
