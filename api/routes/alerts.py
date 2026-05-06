from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time

from api.models import AlertModel
from api.deps import verify_token, get_user_role
from api.firebase import init_firebase

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.post("/")
async def create_alert(data: AlertModel, user=Depends(verify_token)):
    init_firebase()

    uid = user["uid"]
    role = get_user_role(uid)

    if role not in ["officer", "commander", "admin"]:
        raise HTTPException(403, "No permission")

    db.reference("alerts").push({
        "lat": data.lat,
        "lng": data.lng,
        "name": data.name,
        "timestamp": int(time.time() * 1000),
        "created_by": uid
    })

    return {"success": True}
