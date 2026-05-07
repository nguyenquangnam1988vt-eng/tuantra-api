from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import db
import time
import json
from api.models import EncryptedRequest
from api.crypto import decrypt_message
from api.deps import verify_token

router = APIRouter(prefix="/api/move-orders", tags=["move-orders"])

@router.post("/")
async def create_move_order(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]
    try:
        # Giải mã và parse JSON
        decrypted_str = decrypt_message(enc.data)  # giả sử decrypt trả về string JSON
        data = json.loads(decrypted_str) if isinstance(decrypted_str, str) else decrypted_str
    except Exception as e:
        raise HTTPException(400, f"Invalid encrypted data: {e}")

    # Kiểm tra dữ liệu bắt buộc
    required = ["officerId", "fromLat", "fromLng", "toLat", "toLng", "commanderName"]
    missing = [f for f in required if f not in data]
    if missing:
        raise HTTPException(400, f"Missing fields: {missing}")

    # Lưu lệnh di chuyển
    order_data = {
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
    }
    order_ref = db.reference("move_orders").push(order_data)

    # (Tuỳ chọn) Log
    try:
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
    except:
        pass  # Log không bắt buộc, không fail request

    return {"success": True, "orderId": order_ref.key}
