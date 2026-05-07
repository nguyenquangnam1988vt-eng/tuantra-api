from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
from api.models import EncryptedRequest
from api.crypto import decrypt
from api.deps import verify_token

router = APIRouter(prefix="/api/move-orders", tags=["move-orders"])

@router.post("/")
async def create_move_order(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    try:
        data = decrypt(enc.data)
    except Exception:
        raise HTTPException(400, "Invalid encrypted data")

    # Lưu lệnh di chuyển
    order_ref = db.reference("move_orders").push({
        "officerId": data["officerId"],
        "fromLat": data["fromLat"],
        "fromLng": data["fromLng"],
        "toLat": data["toLat"],
        "toLng": data["toLng"],
        "commanderName": data["commanderName"],
        "commanderId": uid,
        "timestamp": data.get("timestamp", int(time.time() * 1000)),
        "status": data.get("status", "active"),
        "note": data.get("note", "")
    })

    # Tuỳ chọn: lưu log nếu cần (có thể tách riêng)
    log_data = {
        "commander": data["commanderName"],
        "commanderId": uid,
        "targetId": data["officerId"],
        "targetName": data.get("targetName", data["officerId"]),
        "lat": data["toLat"],
        "lng": data["toLng"],
        "time": data.get("timestamp", int(time.time() * 1000)),
        "action": "move_order",
        "note": data.get("note", "")
    }
    db.reference("logs").push(log_data)

    return {"success": True, "orderId": order_ref.key}
