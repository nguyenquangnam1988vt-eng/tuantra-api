from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token, get_user_role

router = APIRouter(prefix="/api/special-points", tags=["special-points"])

@router.post("/")
async def create_special_point(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    role = get_user_role(uid)
    if role not in ["commander", "admin"]:
        raise HTTPException(403, "Chỉ huy hoặc admin mới được thêm điểm đặc biệt")

    try:
        data = decrypt(enc.data)
    except Exception:
        raise HTTPException(400, "Invalid encrypted data")

    # Bắt buộc phải có các trường cơ bản
    required = ["lat", "lng", "type", "typeLabel", "icon", "color", "note", "createdBy"]
    if not all(k in data for k in required):
        raise HTTPException(400, "Thiếu trường dữ liệu bắt buộc")

    point_ref = db.reference("special_points").push({
        "lat": data["lat"],
        "lng": data["lng"],
        "type": data["type"],
        "typeLabel": data["typeLabel"],
        "icon": data["icon"],
        "color": data["color"],
        "note": data["note"],
        "createdBy": data["createdBy"],
        "createdById": uid,
        "timestamp": data.get("timestamp", int(time.time() * 1000))
    })
    return {"success": True, "id": point_ref.key}

@router.put("/{point_id}")
async def update_special_point(point_id: str, enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    role = get_user_role(uid)
    if role not in ["commander", "admin"]:
        raise HTTPException(403, "Chỉ huy hoặc admin mới được sửa điểm đặc biệt")

    try:
        data = decrypt(enc.data)
    except Exception:
        raise HTTPException(400, "Invalid encrypted data")

    if "note" not in data:
        raise HTTPException(400, "Thiếu trường note")

    db.reference(f"special_points/{point_id}").update({
        "note": data["note"],
        "updatedAt": data.get("updatedAt", int(time.time() * 1000))
    })
    return {"success": True}

@router.delete("/{point_id}")
async def delete_special_point(point_id: str, user=Depends(verify_token)):
    uid = user["uid"]
    role = get_user_role(uid)
    if role not in ["commander", "admin"]:
        raise HTTPException(403, "Chỉ huy hoặc admin mới được xóa điểm đặc biệt")

    db.reference(f"special_points/{point_id}").delete()
    return {"success": True}

@router.post("/visibility")
async def set_visibility(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    role = get_user_role(uid)
    if role not in ["commander", "admin"]:
        raise HTTPException(403, "Chỉ huy hoặc admin mới được thay đổi hiển thị")

    try:
        data = decrypt(enc.data)
        visible = data.get("visible", True)
    except Exception:
        raise HTTPException(400, "Invalid encrypted data")

    db.reference("special_points_visibility").set(visible)
    return {"success": True}
