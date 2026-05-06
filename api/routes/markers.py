from fastapi import APIRouter, Depends
from firebase_admin import db
import time

from api.models import MarkerModel
from api.deps import verify_token

router = APIRouter(prefix="/api/markers", tags=["markers"])

@router.post("")
async def create_marker(data: MarkerModel, user=Depends(verify_token)):
    uid = user["uid"]

    db.reference(f"markers/{uid}").push({
        "lat": data.lat,
        "lng": data.lng,
        "timestamp": int(time.time()*1000)
    })

    return {"success": True}
