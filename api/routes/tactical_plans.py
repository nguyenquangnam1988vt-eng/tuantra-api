from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import json
import time
from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token, get_user_role
from api.firebase import init_firebase

router = APIRouter(prefix="/api/tactical-plans", tags=["tactical-plans"])

@router.post("/")
async def create_tactical_plan(enc_req: EncryptedRequest, user=Depends(verify_token)):
    init_firebase()
    uid = user["uid"]
    role = get_user_role(uid)
    if role not in ["commander", "admin"]:
        raise HTTPException(403, "Chỉ huy hoặc admin mới được tạo kế hoạch")
    try:
        payload = decrypt(enc_req.data)
        plan_id = payload["plan_id"]
        db.reference(f"tactical_plans/{plan_id}").set({
            "created_by": uid,
            "created_by_name": payload.get("created_by_name", ""),
            "timestamp": int(time.time() * 1000),
            "is_active": payload.get("is_active", True),
            "markers": payload["markers"]
        })
        return {"success": True}
    except Exception as e:
        raise HTTPException(400, f"Lỗi: {e}")
