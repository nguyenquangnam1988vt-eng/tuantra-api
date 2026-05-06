from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import js
from api.models import EncryptedRequest, SpecialPointPayload
from api.crypto import decrypt
from api.deps import verify_token

router = APIRouter(prefix="/api/special-points", tags=["special-points"])

@router.post("/")
async def create_special_point(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    try:
        data = decrypt(enc.data)
        # Có thể validate bằng SpecialPointPayload(**data)
        payload = SpecialPointPayload(**data)
    except Exception as e:
        raise HTTPException(400, f"Invalid data: {e}")
    
    new_ref = db.reference("special_points").push({
        "lat": payload.lat,
        "lng": payload.lng,
        "type": payload.type,
        "typeLabel": payload.typeLabel,
        "icon": payload.icon,
        "color": payload.color,
        "note": payload.note,
        "createdBy": payload.createdBy,
        "createdById": uid,
        "timestamp": payload.timestamp
    })
    return {"success": True, "id": new_ref.key}

@router.put("/{point_id}")
async def update_special_point(point_id: str, enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    # Chỉ cho phép commander hoặc admin? Bạn có thể kiểm tra role
    try:
        data = decrypt(enc.data)
        # data có thể chứa các trường cần cập nhật (ví dụ note)
    except:
        raise HTTPException(400, "Invalid data")
    
    # Cập nhật các trường được phép
    updates = {}
    if "note" in data:
        updates["note"] = data["note"]
    if "updatedAt" in data:
        updates["updatedAt"] = data["updatedAt"]
    else:
        updates["updatedAt"] = int(time.time() * 1000)
    db.reference(f"special_points/{point_id}").update(updates)
    return {"success": True}

@router.delete("/{point_id}")
async def delete_special_point(point_id: str, user=Depends(verify_token)):
    # Kiểm tra quyền (commander/admin)
    db.reference(f"special_points/{point_id}").delete()
    return {"success": True}

@router.post("/visibility")
async def set_visibility(enc: EncryptedRequest, user=Depends(verify_token)):
    try:
        data = decrypt(enc.data)
        visible = data.get("visible", True)
    except:
        raise HTTPException(400, "Invalid data")
    db.reference("special_points_visibility").set(visible)
    return {"success": True}
