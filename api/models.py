from pydantic import BaseModel
from typing import List, Dict, Any

# Request chung cho tất cả (dữ liệu đã mã hóa base64)
class EncryptedRequest(BaseModel):
    data: str

# Payload sau giải mã (validate cấu trúc) - dùng cho từng route
class AlertPayload(BaseModel):
    lat: float
    lng: float
    name: str

class IncidentPayload(BaseModel):
    lat: float
    lng: float
    image_url: str

class MarkerPayload(BaseModel):
    lat: float
    lng: float

class OfficerPayload(BaseModel):
    lat: float
    lng: float
    name: str
    lastUpdate: int

class UserPayload(BaseModel):
    name: str
    role: str
    color: str
    last_seen: int

class TacticalPlanPayload(BaseModel):
    plan_id: str
    markers: List[Dict[str, Any]]
    is_active: bool = True

class ArrowLogPayload(BaseModel):
    from_uid: str
    to_uid: str
    coordinates: List[float]   # [lng, lat] hoặc [lat, lng]
    timestamp: int

class TrackPayload(BaseModel):
    uid: str
    lat: float
    lng: float
    timestamp: int

class DrawingPayload(BaseModel):
    points: List[Dict[str, float]]    
    color: str
    weight: int
    author: str
    authorId: str
    timestamp: int
    type: str   

