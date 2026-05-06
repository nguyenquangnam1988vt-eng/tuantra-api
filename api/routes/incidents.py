from fastapi import APIRouter, Depends
from firebase_admin import db
import time

from api.models import IncidentModel
from api.deps import verify_token

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

@router.post("")
async def create_incident(data: IncidentModel, user=Depends(verify_token)):
    uid = user["uid"]

    db.reference("incidents").push({
        "lat": data.lat,
        "lng": data.lng,
        "image_url": data.image_url,
        "timestamp": int(time.time()*1000),
        "created_by": uid
    })

    return {"success": True}
