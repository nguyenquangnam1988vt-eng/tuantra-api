from fastapi import APIRouter, Depends
from firebase_admin import db
import time

from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token
from api.firebase import init_firebase

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

@router.post("/")
async def create_incident(req: EncryptedRequest, user=Depends(verify_token)):
    init_firebase()

    uid = user["uid"]

    payload = decrypt(req.data)

    db.reference("incidents").push({
        "lat": payload["lat"],
        "lng": payload["lng"],
        "image_url": payload["image_url"],
        "created_by": uid,
        "timestamp": int(time.time() * 1000)
    })

    return {"success": True}
