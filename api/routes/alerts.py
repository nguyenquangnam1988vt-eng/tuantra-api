from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time

from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token, get_user_role
from api.firebase import init_firebase

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.post("/")
async def create_alert(req: EncryptedRequest, user=Depends(verify_token)):
    init_firebase()

    uid = user["uid"]
    role = get_user_role(uid)

    if role not in ["officer", "commander", "admin"]:
        raise HTTPException(403, "No permission")

    payload = decrypt(req.data)

    db.reference("alerts").push({
        "lat": payload["lat"],
        "lng": payload["lng"],
        "name": payload["name"],
        "created_by": uid,
        "timestamp": int(time.time() * 1000)
    })

    return {"success": True}
